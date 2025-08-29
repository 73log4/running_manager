VERSION = "0.0.2"


MSG_WELCOME = f"\n--- [ Welcome to the Running Manager {VERSION} ] ---"

MSG_CMD_TYPES = """
available commands:

print   - print a specified number of last runs
add     - add a new run
edit    - edit a existing run
delete  - delete a run
backup  - create a backup
exit    - exit the manager
"""
MSG_ENTER_CMD = ">>> "
MSG_INVALID_CMD = "invalid command. valid commands are: "

MSG_EXIT = "exiting manager"

MSG_ENTER_DATE = "enter date of run (dd.mm.yyyy): "
MSG_INVALID_DATE = "invalid date"

MSG_ENTER_TIME = "enter time (hh:mm:ss): "
MSG_INVALID_TIME = "invalid time"

MSG_ENTER_KILOMETERS = "enter kilometers (km): "
MSG_INVALID_KILOMETERS = ""

MSG_ENTER_TERRAIN = "enter terrain:"
MSG_INVALID_TERRAIN = ""

MSG_ENTER_ELEVATION = "enter elevation gain (m): "
MSG_INVALID_ELEVATION = ""

MSG_RUN_EXISTS = "a run with the same day already exists - to edit a run use the edit command"
MSG_ADD_SUCCESS = "added run successfully"
MSG_EDIT_CHECK = "are you sure you want to overwrite the run (y/n)? "
MSG_EDIT_NO_CHANGE = "data left unchanged"
MSG_EDIT_SUCCESS  = "edited run successfully"
MSG_RUN_NOT_EXISTS = "run does not exists - data left unchanged"

MSG_ENTER_LAST = "enter number of last runs to be printed (leave empty to print all runs): "

MSG_BACKUP = "backup saved successfully in backups/running_times_backup_"

MSG_DELETE_CHECK = "are you sure you want to delete the run at date "
MSG_DELETE_NO_CHANGE = "delete canceled"
MSG_DELETE_SUCCESS = "run deleted successfully"