# os imported to read and manage flags directory
import os
from os import walk

# PLACE TO CHANGE CORRECT FLAG AMOUNT
CORRECT_AMOUNT = 198

# determine current working directory
WORKING_DIR = os.getcwd()

if WORKING_DIR[-3:] != "src":
    WORKING_DIR = WORKING_DIR + "/src"

# establish path to flags
FLAG_DIR = WORKING_DIR + "/flags"

# ask os to list every file inside flag directory, remove any non .png files
COMPLETE_FLAG_LIST = next(walk(FLAG_DIR), (None, None, []))[2]

for flags in reversed(COMPLETE_FLAG_LIST):
    if not flags.endswith(".png"):
        COMPLETE_FLAG_LIST.remove(flags)

COMPLETE_FLAG_LIST.sort()

# define the flag import function to enable later importing for debugging purposes


def flag_import(correct_amount):
    # add correct flag list to memory
    with open(WORKING_DIR + "/correctflags.txt", 'r', encoding="utf-8") as flag_file:
        correct_flags = [line.strip() for line in flag_file]

    # check if found flags match the correct flag list
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


# call function immediately at launch
flag_import(CORRECT_AMOUNT)

# debugging option


def list_every_flag():
    print("Debugging information about flag source files:")
    print("SOURCE Path:", WORKING_DIR)
    print("FLAGS  Path:", FLAG_DIR)
    print("Amount of flags counted:", len(COMPLETE_FLAG_LIST))
    print("Complete list:")

    COMPLETE_FLAG_LIST.sort()

    for individual_flag in COMPLETE_FLAG_LIST:
        print(individual_flag)
