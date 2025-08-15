import json
from typing import *
from dataclasses import dataclass


TABLE_HEADING_STR = "{0:^12} | {1:^8} | {2:^8} | {3:^8} | {4:^30} | {5:^8} | {6:^8}".format("date", "km", "time (m)", "pace (m)", "terrain", "elev (m)", "kcal")


@dataclass
class Run:
    date: str
    kilometers: float
    time: float
    pace: float
    terrain: str
    elevation_gain: float
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

    def add_run(self, run: Run):
        self.runs[run.date] = run
        with open("running_times.json", "w") as running_times:
            json.dump(self.runs, running_times)

    def edit_run(self, run: Run):
        self.add_run(run)

    def get_run_str(self, date: str) -> str:
        run = self[date]
        s = "{0:>12} | {1:>8} | {2:>8} | {3:>8} | {4:<30} | {5:>8} | {6:>8}"
        return s.format(run.date, run.kilometers, run.time, run.pace, run.terrain,
                        run.elevation_gain if run.elevation_gain is not None else '-',
                        run.calories if run.calories is not None else '-')

    def get_summary(self, last: int = 0) -> str:
        summary = self.get_table_heading() + '\n'
        for date in self.dates[-last:]:
            summary += self.get_run_str(date) + '\n'
        return summary

