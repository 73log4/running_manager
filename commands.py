from data_operations import RunningManager
from utils import *
from input_checks import *
import datetime


def add_command(manager: RunningManager, edit=False):
    date = input(MSG_ENTER_DATE)
    if not valid_date(date):
        print(MSG_INVALID_DATE)
        return
    km = float(input(MSG_ENTER_KILOMETERS))
    time = input(MSG_ENTER_TIME)
    if not valid_time(time):
        print(MSG_INVALID_TIME)
        return
    terrain = input(MSG_ENTER_TERRAIN)
    elev = int(input(MSG_ENTER_ELEVATION))

    if edit:
        if date not in manager.dates:
            print(MSG_RUN_NOT_EXISTS)
            return
        check = input(MSG_EDIT_CHECK)
        if check != 'y':
            print(MSG_EDIT_NO_CHANGE)
            return
    else:
        if date in manager.dates:
            print(MSG_RUN_EXISTS)
            return

    manager.add_run(date, km, time, terrain, elev)

    if edit:
        print(MSG_EDIT_SUCCESS)
    else:
        print(MSG_ADD_SUCCESS)


def edit_command(manager: RunningManager):
    add_command(manager, edit=True)


def print_command(manager: RunningManager):
    last = input(MSG_ENTER_LAST)
    last = int(last) if last != '' else 0
    print(manager.get_summary(last))


def backup_command(manager: RunningManager):
    manager.create_backup()
    print(MSG_BACKUP + f"{datetime.date.today()}.json")

def delete_command(manager: RunningManager):
    date = input(MSG_ENTER_DATE)
    if not valid_date(date):
        print(MSG_INVALID_DATE)
        return

    check = input(MSG_DELETE_CHECK + date + " (y/n): ")
    if check != 'y':
        print(MSG_DELETE_NO_CHANGE)
        return

    manager.delete_run(date)
    print(MSG_DELETE_SUCCESS)

def print_smart_command(manager: RunningManager):
    filter_type = input(MSG_ENTER_FILTER_TYPE)
    if filter_type not in ["km", "location", "none"]:
        print(MSG_FILTER_TYPE_NOT_EXISTS)
        return

    if filter_type != "none":
        filter_value = input(MSG_ENTER_FILTER_VALUE)
    else:
        filter_value = "none"

    sort_key = input(MSG_ENTER_SORT_KEY)
    if sort_key not in ["km", "pace", "date"]:
        print(MSG_SORT_KEY_NOT_EXISTS)
        return

    print(manager.get_smart_summary(filter_type, filter_value, sort_key))
