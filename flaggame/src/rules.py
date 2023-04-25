# MODULE DESCRIPTION

# rules module reads rulebook file and returns it to gui

from os import getcwd  # working directory determined with getcwd

# determine directory for the rulebook file
WORKING_DIR = getcwd()
MASTER_ERROR = True

# (during developing, handle main.py & poetry run invoke starts)
if WORKING_DIR[-3:] != "src":
    WORKING_DIR = WORKING_DIR + "/src"

GAME_RULES_PATH = WORKING_DIR + "/logs/gamerules.txt"

print("Opening the game rule book file 'gamerules.txt'...")

# check rulebook file
try:
    with open(GAME_RULES_PATH, 'r+', encoding="utf-8") as launch_file:
        file_len = len(launch_file.readlines())

        if file_len != 70:
            print("Game rule book file 'gamerules.txt' integrity compromised.")
            print(f"Please replace {GAME_RULES_PATH} with correct file.")
        
        else:
            MASTER_ERROR = False

except FileNotFoundError:
    print("Can't find the game rule book file 'gamerules.txt'.")
    print(f"Please replace {GAME_RULES_PATH} with correct file.")

if MASTER_ERROR:
    print("ERROR while opening 'gamerules.txt'.")
    print("Software relaunch needed to display rules again.")

# define a function for the gui module to display game rules for the player


def update():
    if not MASTER_ERROR:
        with open(GAME_RULES_PATH, 'r', encoding="utf-8") as update_file:
            return update_file.read().splitlines()

    return None
