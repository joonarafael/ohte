import os
from os import walk

CORRECT_AMOUNT = 198

WORKING_DIR = os.getcwd()

if WORKING_DIR[-3:] != "src":
    WORKING_DIR = WORKING_DIR + "/src"

FLAG_DIR = WORKING_DIR + "/flags"

COMPLETE_FLAG_LIST = next(walk(FLAG_DIR), (None, None, []))[2]

for flags in reversed(COMPLETE_FLAG_LIST):
    if not flags.endswith(".png"):
        COMPLETE_FLAG_LIST.remove(flags)

COMPLETE_FLAG_LIST.sort()


def flag_import(correct_amount: int):
    """
    flag importing defined as a function for debugging purposes (mostly during developing)

    Args:
        correct_amount (int): function receives information about the expected flag amount
    """

    with open(WORKING_DIR + "/logs/correctflags.txt", 'r', encoding="utf-8") as flag_file:
        correct_flags = [line.strip() for line in flag_file]

    if COMPLETE_FLAG_LIST != correct_flags or len(COMPLETE_FLAG_LIST) != correct_amount:
        print()
        print("ERROR")
        print("Error while trying to ensure integrity of flag image source files.")

        if len(COMPLETE_FLAG_LIST) != correct_amount:
            print((
                f"Found a total of {len(COMPLETE_FLAG_LIST)} out of {correct_amount}"
                f" .png files in {FLAG_DIR}."))

        print(("Please see flags subdirectory within src directory to ensure"
               " every flag file is present and in .png format."))

        print("Software is trying to find a .png file for every 195 independent state listed at:"
              " https://www.worldometers.info/geography/how-many-countries-are-there-in-the-world/"
              " and Taiwan, Western Sahara & Kosovo.")

        print("Ensure directory integrity by fetching flags again from"
              " github.com/joonarafael/ohte/flaggamee/src/flags.")

    else:
        print("All 198 flags have been found.")


def list_every_flag():
    """
    debugging option to print every flag source file
    """

    print()
    print("Debugging information about flag source files:")
    print("SOURCE Path:", WORKING_DIR)
    print("FLAGS  Path:", FLAG_DIR)
    print("Amount of flags counted:", len(COMPLETE_FLAG_LIST))
    print("Complete list:")

    COMPLETE_FLAG_LIST.sort()

    for individual_flag in COMPLETE_FLAG_LIST:
        print(individual_flag)


flag_import(CORRECT_AMOUNT)
