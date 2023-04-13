# system imported for file handling
from os import getcwd

# determine directory for history file
WORKING_DIR = getcwd()
MASTER_ERROR = False

if WORKING_DIR[-3:] != "src":
    WORKING_DIR = WORKING_DIR + "/src"

GAME_RULES_PATH = WORKING_DIR + "/gamerules.txt"


print("Opening the game rule book file 'gamerules.txt'...")

# check game rules file
try:
    with open(GAME_RULES_PATH, 'r+', encoding="utf-8") as launch_file:
        file_len = len(launch_file.readlines())

        if file_len != 60:
            MASTER_ERROR = True
            print("Game rule book file 'gamerules.txt' integrity compromised.")
            print(f"Please replace {GAME_RULES_PATH} with correct file.")

# if no history file can be established, history will not be recorded
except Exception as e:
    MASTER_ERROR = True
    print("ERROR while opening 'gamerules.txt.':")
    print(e)
    print("Please ensure file integrity, game rules cannot be currently displayed.")
    print("Software relaunch needed to display rules again.")


def update():
    if not MASTER_ERROR:
        with open(GAME_RULES_PATH, 'r', encoding="utf-8") as update_file:
            return update_file.read().splitlines()

    return None
