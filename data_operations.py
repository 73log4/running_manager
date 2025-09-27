import json
from typing import *
from dataclasses import dataclass
import math
import datetime


TABLE_HEADING_STR = (" | {0:^12} | {1:^8} | {2:^8} | {3:^8} | {4:^23} | {5:^8}"
                     .format("date", "km", "time (m)", "pace (m)", "terrain", "elev (m)"))


def format_time_to_str(sec: int) -> str:
    hours = sec // 3600
    minutes = (sec - 3600 * hours) // 60
    seconds = sec - 3600 * hours - 60 * minutes
    return f"{hours}:{minutes:0>2}:{seconds:0>2}"


def format_str_to_time(time: str) -> int:
    l = time.split(':')
    return sum(60 ** i * int(l[-i - 1]) for i in range(len(l)))


def date_str_to_datetime(date: str) -> datetime.date:
    d, m, y = map(int, date.split('.'))
    return datetime.date(y, m, d)


def datetime_to_date_str(date: datetime.date) -> str:
    return f"{date.day:0>2}.{date.month:0>2}.{date.year:0>4}"


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
    def get_table_heading() -> str:
        return TABLE_HEADING_STR + '\n' + '-' * len(TABLE_HEADING_STR)

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
        calories = None

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
        s = " | {0:>12} | {1:>5} km | {2:>8} | {3:>8} | {4:<23} | {5:>8}"
        return s.format(run.date, run.kilometers, format_time_to_str(run.time), format_time_to_str(run.pace), run.terrain,
                        run.elevation_gain if run.elevation_gain is not None else '-')

    def get_summary(self, last: int = 0) -> str:
        summary = self.get_table_heading() + '\n'
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

        summary = self.get_table_heading() + '\n'
        for date in sorted(self.dates, key=key_func):
            if filter_func(date) == filter_value:
                summary += self.get_run_str(date) + '\n'
        return add_numbering(summary)
    

