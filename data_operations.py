import json
from typing import *
from dataclasses import dataclass


@dataclass
class Run:
    date: str
    kilometers: float
    time: float
    pace: float
    terrain: str
    calories: float
    elevation_gain: float


def load_running_data() -> List[Run]:
    pass


def add_run(run: Run):
    pass
