from typing import *


def valid_date(date: str) -> bool:
    l = date.split('.')
    if len(l) != 3:
        return False
    if list(map(len, l)) != [2, 2, 4]:
        return False
    if not all(x.isnumeric() for x in l):
        return False
    if int(l[0]) < 0 or int(l[0]) > 31 or int(l[1]) < 0 or int(l[1]) > 12:
        return False
    return True


def valid_time(date: str) -> bool:
    l = date.split(':')
    if not (len(l) == 3 or len(l) == 2):
        return False
    if len(l) == 2:
        l = ["0"] + l

    if list(map(len, l[1:])) != [2, 2]:
        return False
    if not all(x.isnumeric() for x in l):
        return False
    if int(l[0]) < 0  or int(l[1]) < 0 or int(l[1]) > 59 or int(l[1]) < 0 or int(l[2]) > 59:
        return False
    return True
