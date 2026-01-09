import json
from typing import List, Dict
from dataclasses import dataclass
import math
import datetime
from datetime_manipulations import *


MAX_PACE = 360  # 06:00 pace
MIN_PACE = 180  # 03:00 pace


RUNS_SUMMARY_HEADING = (" | {0:^12} | {1:^8} | {2:^8} | {3:^8} | {4:^12} | {5:^23} | {6:^8}"
                     .format("date", "km", "time (m)", "pace (m)", "pace bar", "terrain", "elev (m)"))


WEEKS_SUMMARY_HEADING = (" | {0:^23} | {1:^4} | {2:^9} | {3:^8} | {4:^10} | {5:^10} "
                     .format("week", "runs", "map", "total km", "avrg pace", "max pace"))


KM_CATEGORIES = ["1k", "3k", "5k", "10k", "10k+"]


def run_km_category(km: float) -> str:
    if km < 2:
        return '1k'
    elif 2 <= km < 4:
        return '3k'
    elif 4 <= km < 7:
        return '5k'
    elif 7 <= km < 12:
        return '10k'
    else:
        return '10k+'


def add_numbering(summary: str) -> str:
    summary_lines = summary.split("\n")[:-1:]
    summary_lines[0] = "   " + summary_lines[0]
    summary_lines[1] = "---" + summary_lines[1]

    for i, line in enumerate(summary_lines):
        if i >= 2:
            summary_lines[i] = "{0:>3}".format(i - 1) + line

    return "\n".join(summary_lines)


@dataclass
class Run:
    date: str
    kilometers: float
    time: int
    pace: int
    terrain: str
    elevation_gain: int
    calories: float


class RunningManager:

    def __init__(self):
        running_data = self.load_running_data()
        self.runs: Dict[str, Run] = {r.date: r for r in running_data}
        self.dates: List[str] = [r.date for r in running_data]

    def __getitem__(self, date: str) -> Run:
        return self.runs[date]

    @staticmethod
    def load_running_data():
        with open("running_times.json", "r") as running_times:
            return [Run(r["date"], r["kilometers"], r["time"], r["pace"], r["terrain"], r["elevation_gain"],
                        r["calories"]) for r in json.load(running_times)]

    @staticmethod
    def get_runs_table_heading() -> str:
        return RUNS_SUMMARY_HEADING + '\n' + '-' * len(RUNS_SUMMARY_HEADING)
    
    @staticmethod
    def get_weeks_table_heading() -> str:
        return WEEKS_SUMMARY_HEADING+ '\n' + '-' * len(WEEKS_SUMMARY_HEADING)

    def save_changes(self, file_path: str = "running_times.json"):
        data = []
        for d in self.dates:
            r = self[d]
            run_dict = {
                "date": r.date,
                "kilometers": r.kilometers,
                "time": r.time,
                "pace": r.pace,
                "terrain": r.terrain,
                "elevation_gain": r.elevation_gain,
                "calories": r.calories,
            }
            data.append(run_dict)
        with open(file_path, "w") as running_times:
            json.dump(data, running_times)

    def sort_dates(self):
        new_dates = list(map(date_str_to_datetime, self.dates))
        new_dates.sort()
        self.dates = list(map(datetime_to_date_str, new_dates))

    def create_backup(self):
        backup_path = f"backups/running_times_backup_{datetime.date.today()}.json"
        self.save_changes(backup_path)

    def add_run(self, date: str, km: float, time: str, terrain: str, elev: int):
        new_time = format_str_to_time(time)
        pace = math.ceil(new_time / km)
        calories = -1

        run = Run(date, km, new_time, pace, terrain, elev, calories)

        self.runs[run.date] = run
        if date not in self.dates:
            self.dates.append(date)

        self.sort_dates()
        self.save_changes()

    def delete_run(self, date: str):
        del self.runs[date]
        self.dates.remove(date)

        self.sort_dates()
        self.save_changes()

    def get_run_str(self, date: str) -> str:
        run = self[date]

        rounded_pace = min(max(MIN_PACE, run.pace), MAX_PACE)
        bar_unit = (MAX_PACE - MIN_PACE) / 12
        pace_bar = "*" * round((rounded_pace - MIN_PACE) / bar_unit)

        s = " | {0:>12} | {1:>5} km | {2:>8} | {3:>8} | {4:<12} | {5:<23} | {6:>8}"
        return s.format(run.date, run.kilometers, format_time_to_str(run.time), format_time_to_str(run.pace), pace_bar, run.terrain,
                        run.elevation_gain if run.elevation_gain is not None else '-')

    def get_summary(self, last: int = 0) -> str:
        summary = self.get_runs_table_heading() + '\n'
        for date in self.dates[-last:]:
            summary += self.get_run_str(date) + '\n'
        return add_numbering(summary)
    
    def get_smart_summary(self, filter_type: str, filter_value: str, sort_key="date") -> str:
        if sort_key == "km":
            key_func = lambda d: -self.runs[d].kilometers
        elif sort_key == "pace":
            key_func = lambda d: self.runs[d].pace
        elif sort_key == "date":
            key_func = lambda d: d

        if filter_type == "none":
            filter_func = lambda d: "none"
        if filter_type == "location":
            filter_func = lambda d: self[d].terrain
        elif filter_type == "km":
            filter_func = lambda d: str(round(self[d].kilometers))

        summary = self.get_runs_table_heading() + '\n'
        for date in sorted(self.dates, key=key_func):
            if filter_func(date) == filter_value:
                summary += self.get_run_str(date) + '\n'
        return add_numbering(summary)
    
    def get_week_str(self, week_dates: List[str]) -> str:
        runs_in_week = [self.runs[d] for d in week_dates if d in self.runs]

        num_of_runs = len(runs_in_week)
        week_map = ''.join('#' if week_dates[i] in self.runs else '-' for i in range(len(week_dates))) + ' ' * (7 - len(week_dates))
        total_km = round(sum(r.kilometers for r in runs_in_week), 1)
        average_pace = format_time_to_str(round(sum(r.pace * r.kilometers for r in runs_in_week) / total_km)) if num_of_runs > 0 else '-'
        max_pace = format_time_to_str(min(r.pace for r in runs_in_week)) if num_of_runs > 0 else '-'

        week_summary = (" | {0:^23} | {1:^4} | {2:^9} | {3:^8} | {4:^10} | {5:^10} "
                     .format(f"{week_dates[0]} - {week_dates[-1]}" , num_of_runs, week_map, total_km, average_pace, max_pace))
        
        return week_summary
        
    def get_week_summary(self, last) -> str:
        weeks = last_weeks(last)

        summary = self.get_weeks_table_heading() + '\n'
        for week in weeks:
            summary += self.get_week_str(week) + '\n'

        return add_numbering(summary)
    
    def get_yearly_summary(self, year) -> str:
        dates = [datetime_to_date_str(d) for d in days_in_year(year)]
        runs = {d: self.runs[d] for d in dates if d in self.runs}
        category_map = {d: run_km_category(runs[d].kilometers) for d in runs}

        num_of_runs = len(runs)

        total_km = round(sum(r.kilometers for r in runs.values()))

        total_km_by_category = dict()
        for c in KM_CATEGORIES:
            runs_in_category = [r.kilometers for r in runs.values() if run_km_category(r.kilometers) == c]
            if len(runs_in_category) == 0:
                total_km_by_category[c] = None
            else:
                total_km_by_category[c] = round(sum(runs_in_category))

        total_km_by_category_str = ""
        for c in KM_CATEGORIES:
            if total_km_by_category[c] == None:
                total_km_by_category_str += f"{c:<4}: -\n"
            else:
                total_km_by_category_str += f"{c:<4}: {total_km_by_category[c]} km\n"
        
        best_run_by_category = dict()
        for c in KM_CATEGORIES:
            runs_in_category = [r for r in runs.values() if run_km_category(r.kilometers) == c]
            if len(runs_in_category) == 0:
                best_run_by_category[c] = None
            else:
                best_run_by_category[c] =  min(runs_in_category, key=lambda x: x.pace)

        best_run_by_category_str = ""
        for c in KM_CATEGORIES:
            r = best_run_by_category[c]
            if r != None:
                best_run_by_category_str += f"{c:<4}: {r.date} - {r.terrain:<16} - {format_time_to_str(r.pace)} /km\n"
            else:
                best_run_by_category_str += f"{c:<4}: -\n"


        longest_run = sorted(runs.values(), key=lambda r: r.kilometers)[-1]

        largest_climb_run = sorted(runs.values(), key=lambda r: r.elevation_gain if r.elevation_gain != None else -1)[-1]


        report = \
        f"""
--- [{year} yearly report] ---

total number of runs: {num_of_runs}

total km: {total_km} km

total km by category: \n{total_km_by_category_str}
best run by category: \n{best_run_by_category_str}
longest run: {longest_run.date} - {longest_run.kilometers} km

largest climb: {largest_climb_run.date} - {largest_climb_run.elevation_gain} m

"""

        return report



