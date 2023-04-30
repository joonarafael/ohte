import sys
from os import getcwd
from datetime import datetime
from csvhandler import clear_stats_and_rounds

WORKING_DIR = getcwd()
MASTER_ERROR = True

if WORKING_DIR[-3:] != "src":
    WORKING_DIR = WORKING_DIR + "/src"

HISTORY_PATH = WORKING_DIR + "/logs/history.txt"


def curr_date():
    return datetime.now().isoformat(sep=" ", timespec="minutes")


def curr_time():
    return datetime.now().strftime('%H:%M:%S')


print("Opening (creating if it doesn't exist) the game history file 'history.txt'...")

try:
    with open(HISTORY_PATH, 'r+', encoding="utf-8") as launch_file:
        file_len = len(launch_file.readlines())

    with open(HISTORY_PATH, 'a+', encoding="utf-8") as launch_file:
        if file_len == 0:
            launch_file.write(
                f"{curr_date()} NEW SESSION")

        else:
            launch_file.write(
                f"\n\n{curr_date()} NEW SESSION")

    MASTER_ERROR = False

except FileNotFoundError:
    with open(HISTORY_PATH, 'w+', encoding="utf-8") as launch_file:

        launch_file.write(
            f"{curr_date()} NEW SESSION")

    MASTER_ERROR = False

if MASTER_ERROR:
    print("ERROR while opening 'history.txt':")
    print("Please ensure file integrity or create it manually before continuing.")
    print("If continuing, no history will be recorded.")
    print("Software relaunch is required to record history again.")


def clear_history(remove_statistics: bool):
    """
    function to remove recorded game history

    Args:
        remove_statistics (bool): whether to remove the statistics also
    """

    if not MASTER_ERROR:
        with open(HISTORY_PATH, 'w+', encoding="utf-8"):
            print("Deleting all recorded history...")

        if remove_statistics:
            clear_stats_and_rounds()

        else:
            print("Closing program...")
            sys.exit(1)

    else:
        print("Recorded history cannot be erased as software is",
              f" unable to locate file '{HISTORY_PATH}'.")


def console_print():
    """
    debugging option to print the game history file to console
    """

    if not MASTER_ERROR:
        print()
        print("Contents of file 'history.txt':")

        with open(HISTORY_PATH, 'r', encoding="utf-8") as file:
            print(file.read())


def game_start(mode: str):
    """
    function to write a new game start to file

    Args:
        mode (str): game mode as a string
    """

    if not MASTER_ERROR:
        with open(HISTORY_PATH, 'a+', encoding="utf-8") as game_start_file:
            game_start_file.write(
                f"\n\n    {mode} Game start off at {curr_time()}.")


def game_over(info: list):
    """
    function to record game end

    Args:
        info (list): relevant information about the game is received in a list
                     [game mode, score, longest streak]
    """

    if not MASTER_ERROR:
        with open(HISTORY_PATH, 'a+', encoding="utf-8") as game_over_file:
            if info[0] == 0:
                mode = "Classic"

            elif info[0] == 1:
                mode = "Advanced"

            elif info[0] == 2:
                mode = "Time Trial"

            elif info[0] == 3:
                mode = "One Life"

            elif info[0] == 4:
                mode = "Free"

            game_over_file.write(
                f"\n    {mode} Game completed at {curr_time()}:")
            game_over_file.write(
                f"\n    Score: {info[1]} - Longest Continuous Streak: {info[2]}.")


def game_terminated(info: list):
    """
    function to record a cancelled game

    Args:
        info (list): relevant information about the game is received in a list
                     [game mode, score, longest streak, lives at termination]
    """

    if not MASTER_ERROR:
        with open(HISTORY_PATH, 'a+', encoding="utf-8") as game_terminated_file:
            if info[0] == 0:
                mode = "Classic"

            elif info[0] == 1:
                mode = "Advanced"

            elif info[0] == 2:
                mode = "Time Trial"

            elif info[0] == 3:
                mode = "One Life"

            elif info[0] == 4:
                mode = "Free"

            game_terminated_file.write(
                f"\n    {mode} Game cancelled at {curr_time()}:")

            if mode == "Free":
                game_terminated_file.write(
                    f"\n    Score: {info[1]} - Longest Continuous Streak: {info[2]}.")

            else:
                game_terminated_file.write((
                    f"\n    Score: {info[1]} - Longest Continuous Streak: {info[2]}."
                    f" {info[3]} lives left at termination."))


def update():
    """
    function to read the history file and return the content to gui

    Returns:
        list / None: every row of history file is a separate list item
    """

    if not MASTER_ERROR:
        with open(HISTORY_PATH, 'r', encoding="utf-8") as update_file:
            return_list = update_file.read().splitlines()

            return_list.insert(0, "")
            return_list.insert(0, "")
            return_list.insert(0, "GAME HISTORY")

            return return_list

    return None


def print_directories():
    """
    debugging option to print the working directories as well as the history file path
    """

    print("Main working directory path received from os.getcwd():")
    print(getcwd() + "/")
    print("Source folder path:")
    print(WORKING_DIR + "/")
    print("History file path:")
    print(HISTORY_PATH)
