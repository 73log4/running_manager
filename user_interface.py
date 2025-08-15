from data_operations import RunningManager, Run
from enum import Enum


MSG_WELCOME = "Welcome !"

MSG_CMD_TYPES = ""
MSG_ENTER_CMD = "enter command: "
MSG_INVALID_CMD = ""

MSG_EXIT = ""

MSG_ENTER_DATE = ""
MSG_INVALID_DATE = ""

MSG_ENTER_TIME = ""
MSG_INVALID_TIME = ""

MSG_ENTER_KILOMETERS = ""
MSG_INVALID_KILOMETERS = ""

MSG_ENTER_TERRAIN = ""
MSG_INVALID_TERRAIN = ""

MSG_ENTER_ELEVATION = ""
MSG_INVALID_ELEVATION = ""


class ManagerCMD(Enum):
    Error = -1
    Exit = 0
    Print = 1
    Add = 2
    Edit = 3


CMD_TABLE = {
    "exit": ManagerCMD.Exit,
    "print": ManagerCMD.Print,
    "add": ManagerCMD.Add,
    "edit": ManagerCMD.Edit,
}


def edit_command(manager: RunningManager):
    pass


def add_command(manager: RunningManager):
    pass


def print_command(manager: RunningManager):
    print(manager.get_summary())


def get_command() -> ManagerCMD:
    cmd = input(MSG_ENTER_CMD)
    return CMD_TABLE.get(cmd, ManagerCMD.Error)


def run_manager():
    manager = RunningManager()
    command = ManagerCMD.Print

    print(MSG_WELCOME)

    while command != ManagerCMD.Exit:
        command = get_command()

        if command == ManagerCMD.Print:
            print_command(manager)
        elif command == ManagerCMD.Add:
            add_command(manager)
        elif command == ManagerCMD.Edit:
            edit_command(manager)
        elif command == ManagerCMD.Error:
            print(MSG_INVALID_CMD)

    print(MSG_EXIT)


if __name__ == "__main__":
    run_manager()