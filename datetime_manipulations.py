from datetime import date, timedelta
import datetime
from typing import List, Dict, Tuple


START_YEAR = 2023


def format_time_to_str(sec: int) -> str:
    """ formats seconds to hh:mm:ss """
    hours = sec // 3600
    minutes = (sec - 3600 * hours) // 60
    seconds = sec - 3600 * hours - 60 * minutes
    return f"{hours}:{minutes:0>2}:{seconds:0>2}"


def format_str_to_time(time: str) -> int:
    """ formats hh:mm:ss to seconds """
    l = time.split(':')
    return sum(60 ** i * int(l[-i - 1]) for i in range(len(l)))


def date_str_to_datetime(date: str) -> datetime.date:
    d, m, y = map(int, date.split('.'))
    return datetime.date(y, m, d)


def datetime_to_date_str(date: datetime.date) -> str:
    return f"{date.day:0>2}.{date.month:0>2}.{date.year:0>4}"


def days_in_year(year: int) -> List[date]:
    start = date(year, 1, 1)
    end = min(date(year, 12, 31), datetime.datetime.now().date())
    return [start + timedelta(n) for n in range(int((end-start).days) + 1)]


def days_by_week(year: int) -> Tuple[Dict[int, List[str]], List]:
    """
    Returns a dict with keys as week numbers and the days
    in the week as the values. Also retunrs a list of days 
    that are in the last week of the year but not in the year
    """
    days = days_in_year(year)

    week = {}
    left_over = []
    for day in days:
        y, i, _ = day.isocalendar()
        if i not in week:
            week[i] = []
        if y == year:
            week[i].append(datetime_to_date_str(day))
        else:
            left_over.append(datetime_to_date_str(day))

    return week, left_over


def last_weeks(n: int) -> List[List[str]]:
    """
    Return the last n weeks from prsent as list of days. 
    """
    weeks = []

    left_over = []
    for year in range(START_YEAR, datetime.datetime.now().year + 1):
        d, new_left_over = days_by_week(year)
        for i in sorted(d.keys()):
            weeks.append(d[i])
            if i == 1 and year > START_YEAR:
                weeks[-1] = left_over + weeks[-1]
        left_over = new_left_over

    # fix monday problem
    for i in range(len(weeks) - 1):
        weeks[i + 1].insert(0, weeks[i].pop())
    if len(weeks[-1]) == 8:
        weeks.append([weeks[-1].pop()])


    return weeks[-n:]