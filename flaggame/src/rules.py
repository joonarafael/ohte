# system imported for file handling
from os import getcwd

# determine directory for the rulebook file
WORKING_DIR = getcwd()
MASTER_ERROR = True

if WORKING_DIR[-3:] != "src":
    WORKING_DIR = WORKING_DIR + "/src"

GAME_RULES_PATH = WORKING_DIR + "/gamerules.txt"


print("Opening the game rule book file 'gamerules.txt'...")

# check rulebook file
try:
    with open(GAME_RULES_PATH, 'r+', encoding="utf-8") as launch_file:
        file_len = len(launch_file.readlines())

        MASTER_ERROR = False

        if file_len != 70:
            MASTER_ERROR = True
            print("Game rule book file 'gamerules.txt' integrity compromised.")
            print(f"Please replace {GAME_RULES_PATH} with correct file.")

except FileNotFoundError:
    print("Can't find the game rule book file 'gamerules.txt'.")
    print(f"Please replace {GAME_RULES_PATH} with correct file.")

    MASTER_ERROR = True

if MASTER_ERROR:
    print("ERROR while opening 'gamerules.txt'.")
    print("Software relaunch needed to display rules again.")

# define a function for the gui module to display game rules for the player


def update():
    if not MASTER_ERROR:
        with open(GAME_RULES_PATH, 'r', encoding="utf-8") as update_file:
            return update_file.read().splitlines()

    return None
