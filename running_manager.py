from manager_class import RunningManager
from enum import Enum
from commands import *
from utils import *


# Possible commands
class ManagerCMD(Enum):
    Error = -1
    Exit = 9
    Print = 1
    Add = 5
    Edit = 6
    Backup = 8
    Delete = 7
    PrintSmart = 2
    WeekReport = 3
    YearlyReport = 4


# Command names
CMD_TABLE = {
    "exit": ManagerCMD.Exit,
    "print": ManagerCMD.Print,
    "add": ManagerCMD.Add,
    "edit": ManagerCMD.Edit,
    "backup": ManagerCMD.Backup,
    "delete": ManagerCMD.Delete,
    "print-smart": ManagerCMD.PrintSmart,
    "week-report": ManagerCMD.WeekReport,
    "yearly-report": ManagerCMD.YearlyReport,
}


# Functions to be called for each command
CMD_FUNC = {
    ManagerCMD.Print: print_command,
    ManagerCMD.Add: add_command,
    ManagerCMD.Edit: edit_command,
    ManagerCMD.Backup: backup_command,
    ManagerCMD.Delete: delete_command,
    ManagerCMD.PrintSmart: print_smart_command,
    ManagerCMD.WeekReport: week_report_command,
    ManagerCMD.YearlyReport: yearly_summary,
}


def get_command() -> ManagerCMD:
    """ Asks user for command and returns a appropriate ManagerCMD object. """
    cmd = input(MSG_ENTER_CMD)

    if cmd.isdecimal():
        cmd_int = int(cmd)
        if 0 < cmd_int < len(ManagerCMD):
            return ManagerCMD(cmd_int)
        else:
            return ManagerCMD.Error

    return CMD_TABLE.get(cmd, ManagerCMD.Error)


def run_manager():
    """ Main loop. """
    manager = RunningManager()
    command = ManagerCMD.Print

    print(MSG_WELCOME)
    print(MSG_CMD_TYPES)

    while command != ManagerCMD.Exit:
        command = get_command()

        if command == ManagerCMD.Error:
            print(MSG_INVALID_CMD)
            print(MSG_CMD_TYPES)
        elif command != ManagerCMD.Exit:
            CMD_FUNC[command](manager)

    print(MSG_EXIT)


if __name__ == "__main__":
    run_manager()