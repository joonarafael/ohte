# system imported for file handling
import sys
from os import getcwd
from datetime import datetime


# determine directory for history file
WORKING_DIR = getcwd()
MASTER_ERROR = False

if WORKING_DIR[-3:] != "src":
    WORKING_DIR = WORKING_DIR + "/src"

HISTORY_PATH = WORKING_DIR + "/history.txt"

# current time is read with minutes accuracy


def curr_time():
    return datetime.now().isoformat(sep=" ", timespec="minutes")


print("Opening (creating if it doesn't exist) the game history file 'history.txt'...")

# check history file
try:
    with open(HISTORY_PATH, 'r+', encoding="utf-8") as launch_file:
        file_len = len(launch_file.readlines())

    with open(HISTORY_PATH, 'a+', encoding="utf-8") as launch_file:
        if file_len == 0:
            launch_file.write(
                f"/// /// /// /// /// /// /// ///\nNEW SESSION AT {curr_time()}")

        else:
            launch_file.write(
                f"\n\n/// /// /// /// /// /// /// ///\nNEW SESSION AT {curr_time()}")

except FileNotFoundError:
    with open(HISTORY_PATH, 'w+', encoding="utf-8") as launch_file:

        launch_file.write(
            f"/// /// /// /// /// /// /// ///\nNEW SESSION AT {curr_time()}")

# if no history file can be established, history will not be recorded
except Exception as e:
    MASTER_ERROR = True
    print("ERROR while opening 'history.txt.':")
    print(e)
    print("Please ensure file integrity or create it manually before continuing.")
    print("If continuing, no history will be recorded.")
    print("Software relaunch is required to record history again.")


def clear_history():
    if not MASTER_ERROR:
        print("Deleting all progress and history permantently.")
        with open(HISTORY_PATH, 'w+', encoding="utf-8"):
            print("Closing program...")

        sys.exit(1)

# debug option to print history file


def console_print():
    if not MASTER_ERROR:
        print("Contents of file 'history.txt':")

        with open(HISTORY_PATH, 'r', encoding="utf-8") as file:
            print(file.read())

# game_handler calls history changes
# game start recorded


def game_start(mode: str):
    if not MASTER_ERROR:
        with open(HISTORY_PATH, 'a+', encoding="utf-8") as game_start_file:
            game_start_file.write(
                f"\n\n{mode} Game start off at {curr_time()}.")

# game is over, game info & score recorded


def game_over(info: list):
    if not MASTER_ERROR:
        with open(HISTORY_PATH, 'a+', encoding="utf-8") as game_over_file:
            if info[0] == 0:
                mode = "Classic"

            elif info[0] == 1:
                mode = "Advanced"

            elif info[0] == 4:
                mode = "Free"

            game_over_file.write(f"\n{mode} Game completed at {curr_time()}:")
            game_over_file.write(
                f"\nScore: {info[1]} - Longest Continuous Streak: {info[2]}.")

# game is terminated, game info & score recorded


def game_terminated(info: list):
    if not MASTER_ERROR:
        with open(HISTORY_PATH, 'a+', encoding="utf-8") as game_terminated_file:
            if info[0] == 0:
                mode = "Classic"

            elif info[0] == 1:
                mode = "Advanced"

            elif info[0] == 4:
                mode = "Free"

            game_terminated_file.write(
                f"\n{mode} Game cancelled at {curr_time()}:")

            if mode == "Free":
                game_terminated_file.write(
                    f"\nScore: {info[1]} - Longest Continuous Streak: {info[2]}.")

            else:
                game_terminated_file.write((
                    f"\nScore: {info[1]} - Longest Continuous Streak: {info[2]}."
                    f" Still {info[3]} lives left at termination."))

# reading the history from file and returning for gui


def update():
    if not MASTER_ERROR:
        with open(HISTORY_PATH, 'r', encoding="utf-8") as update_file:
            return update_file.read().splitlines()

    return None


def print_directories():
    print("Main working directory path received from os.getcwd():")
    print(getcwd())
    print("Source folder path:")
    print(WORKING_DIR)
    print("History file path:")
    print(HISTORY_PATH)
