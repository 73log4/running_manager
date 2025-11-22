from datetime import date, timedelta
import datetime
from typing import List, Dict


START_YEAR = 2023


def date_str_to_datetime(date: str) -> datetime.date:
    d, m, y = map(int, date.split('.'))
    return datetime.date(y, m, d)


def datetime_to_date_str(date: datetime.date) -> str:
    return f"{date.day:0>2}.{date.month:0>2}.{date.year:0>4}"


def days_in_year(year: int) -> List[date]:
    start = date(year, 1, 1)
    end = min(date(year, 12, 31), datetime.datetime.now().date())
    return [start + timedelta(n) for n in range(int((end-start).days) + 1)]


def days_by_week(year: int) -> Dict[int, str]:
    days = days_in_year(year)

    week = {}
    for day in days:
        _, i, _ = day.isocalendar()
        if i not in week:
            week[i] = []
        week[i].append(datetime_to_date_str(day))

    return week


def last_weeks(n: int) -> List[List[str]]:
    weeks = []

    for year in range(START_YEAR, datetime.datetime.now().year + 1):
        d = days_by_week(year)
        for i in sorted(d.keys()):
            weeks.append(d[i])

    return weeks[-n:]