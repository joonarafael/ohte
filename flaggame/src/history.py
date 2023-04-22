# system imported for file handling
import sys
from os import getcwd
from datetime import datetime
from csvhandler import clear_stats_and_rounds


# determine directory for the history file
WORKING_DIR = getcwd()
MASTER_ERROR = True

if WORKING_DIR[-3:] != "src":
    WORKING_DIR = WORKING_DIR + "/src"

HISTORY_PATH = WORKING_DIR + "/history.txt"

# current time is read with minutes accuracy for session starts


def curr_date():
    return datetime.now().isoformat(sep=" ", timespec="minutes")


# only HH:MM:SS recorded for game start


def curr_time():
    return datetime.now().strftime('%H:%M:%S')


print("Opening (creating if it doesn't exist) the game history file 'history.txt'...")

# check history file
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

# define a function to clear all history


def clear_history(statistics: bool):
    if not MASTER_ERROR:
        with open(HISTORY_PATH, 'w+', encoding="utf-8"):
            print("Deleting all recorded history...")

        if statistics:
            clear_stats_and_rounds()

        else:
            print("Closing program...")
            sys.exit(1)

    else:
        print("Recorded history cannot be erased as software is",
              f" unable to locate file '{HISTORY_PATH}'.")

# define a function to print history file to console (debug option)


def console_print():
    if not MASTER_ERROR:
        print()
        print("Contents of file 'history.txt':")

        with open(HISTORY_PATH, 'r', encoding="utf-8") as file:
            print(file.read())

# Master Game Handler calls all history changes
# game start recorded


def game_start(mode: str):
    if not MASTER_ERROR:
        with open(HISTORY_PATH, 'a+', encoding="utf-8") as game_start_file:
            game_start_file.write(
                f"\n\n    {mode} Game start off at {curr_time()}.")

# game is over, game info & score recorded


def game_over(info: list):
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

# game is terminated, game info & score recorded


def game_terminated(info: list):
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

# define a function to read the history and return it for the gui
# to display it visually for the player


def update():
    if not MASTER_ERROR:
        with open(HISTORY_PATH, 'r', encoding="utf-8") as update_file:
            return_list = update_file.read().splitlines()

            return_list.insert(0, "")
            return_list.insert(0, "")
            return_list.insert(0, "GAME HISTORY")

            return return_list

    return None


# define a function to print history file directories (debug option)

def print_directories():
    print("Main working directory path received from os.getcwd():")
    print(getcwd() + "/")
    print("Source folder path:")
    print(WORKING_DIR + "/")
    print("History file path:")
    print(HISTORY_PATH)
