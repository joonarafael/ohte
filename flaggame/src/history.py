# system imported for file handling
import sys
from os import getcwd
from datetime import datetime


# determine directory for history file
workingdir = getcwd()

if workingdir[-3:] != "src":
    workingdir = workingdir + "/src"
    print(workingdir)

historyPath = workingdir + "/history.txt"

# current time is read with minutes accuracy


def curr_time():
    return datetime.now().isoformat(sep=" ", timespec="minutes")


print("Opening (creating if it doesn't exist) the game history file 'history.txt'...")

# check history file
try:
    f = open(historyPath, 'r+', encoding="utf-8")
    fileLen = len(f.readlines())
    f.close()

    f = open(historyPath, 'a+', encoding="utf-8")

    if fileLen == 0:
        f.write(
            f"/// /// /// /// /// /// /// ///\nNEW SESSION AT {curr_time()}")

    else:
        f.write(
            f"\n\n/// /// /// /// /// /// /// ///\nNEW SESSION AT {curr_time()}")

    f.close()

except FileNotFoundError:
    f = open(historyPath, 'w+', encoding="utf-8")

    f.write(
        f"/// /// /// /// /// /// /// ///\nNEW SESSION AT {curr_time()}")

    f.close()

# if history file cannot be read at launch, software launch is terminated
# no history will be recorded anyway
except Exception as e:
    print("ERROR while opening 'history.txt.':")
    print(e)
    print("Please ensure file integrity or create it manually before continuing.")
    print("You may have to close the file before running the software again.")
    sys.exit(1)


def clear_history():
    print("Deleting all progress and history permantently.")
    f = open(historyPath, 'w+', encoding="utf-8")
    f.close()
    print("Closing program...")
    sys.exit(1)

# debug option to print history file


def console_print():
    print("Contents of file 'history.txt':")
    with open(historyPath, 'r', encoding="utf-8") as f:
        print(f.read())

# game_handler calls history changes
# game start recorded


def gameStart(mode: str):
    with open(historyPath, 'a+', encoding="utf-8") as f:
        f.write(f"\n\n{mode} Game start off at {curr_time()}.")

# game is over, game info & score recorded


def gameOver(info: list):
    with open(historyPath, 'a+', encoding="utf-8") as f:
        if info[0] == 0:
            mode = "Classic"

        elif info[0] == 1:
            mode = "Advanced"

        elif info[0] == 4:
            mode = "Free"

        f.write(f"\n{mode} Game completed at {curr_time()}:")
        f.write(f"\nScore: {info[1]} - Longest Continuous Streak: {info[2]}.")

# game is terminated, game info & score recorded


def terminated(info: list):
    with open(historyPath, 'a+', encoding="utf-8") as f:
        if info[0] == 0:
            mode = "Classic"

        elif info[0] == 1:
            mode = "Advanced"

        elif info[0] == 4:
            mode = "Free"

        f.write(f"\n{mode} Game cancelled at {curr_time()}:")

        if mode == "Free":
            f.write(
                f"\nScore: {info[1]} - Longest Continuous Streak: {info[2]}.")

        else:
            f.write(
                f"\nScore: {info[1]} - Longest Continuous Streak: {info[2]}. Still {info[3]} lives left at termination.")

# reading the history from file and returning for gui


def update():
    with open(historyPath, 'r') as f:
        return f.read().splitlines()


def print_directories():
    print("Main working directory path received from os.getcwd():")
    print(getcwd())
    print("Source folder path:")
    print(workingdir)
    print("History file path:")
    print(historyPath)
