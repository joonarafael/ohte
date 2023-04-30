from os import getcwd

WORKING_DIR = getcwd()
MASTER_ERROR = True

if WORKING_DIR[-3:] != "src":
    WORKING_DIR = WORKING_DIR + "/src"

GAME_RULES_PATH = WORKING_DIR + "/logs/gamerules.txt"

print("Opening the game rule book file 'gamerules.txt'...")

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


def update():
    """
    function to read the rulebook and return the content to gui

    Returns:
        list / None: every row of rulebook file is a separate list item
    """
    if not MASTER_ERROR:
        with open(GAME_RULES_PATH, 'r', encoding="utf-8") as update_file:
            return update_file.read().splitlines()

    return None
