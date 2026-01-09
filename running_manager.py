from manager_class import RunningManager
from enum import Enum
from commands import *
from utils import *


class ManagerCMD(Enum):
    Error = -1
    Exit = 0
    Print = 1
    Add = 2
    Edit = 3
    Backup = 4
    Delete = 5
    PrintSmart = 6,
    WeekReport = 7,
    YearlyReport = 8,


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
    cmd = input(MSG_ENTER_CMD)
    return CMD_TABLE.get(cmd, ManagerCMD.Error)


def run_manager():
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