import os
from os import walk

WORKING_DIR = os.getcwd()

if WORKING_DIR[-3:] != "src":
    WORKING_DIR = WORKING_DIR + "/src"

FLAG_DIR = WORKING_DIR + "/flags"


class MasterFlagHandler():
    """
    find and manage all flag source files
    """

    def __init__(self, working_dir: str, flag_dir: str):
        """
        initialize the critical directories, fetch trough the flag source files

        Args:
            working_dir (str): main working directory path,
            flag_dir (str): flag source files directory path
        """

        self.correct_amount = 0
        self.working_dir = working_dir
        self.flag_dir = flag_dir

        self.complete_flag_list = next(
            walk(self.flag_dir), (None, None, []))[2]

        for flags in reversed(self.complete_flag_list):
            if not flags.endswith(".png"):
                self.complete_flag_list.remove(flags)

        self.complete_flag_list.sort()

    def flag_import(self):
        """
        check if the flags found match to the correctflags.txt file
        """

        try:
            with open(self.working_dir + "/logs/correctflags.txt",
                      'r', encoding="utf-8") as flag_file:
                correct_flags = [line.strip() for line in flag_file]

                self.correct_amount = len(correct_flags)

        except FileNotFoundError:
            print("\nERROR\nSoftware is unable to find the file '/src/logs/correctflags.txt'"
                  " listing the correct flags.\nPlease ensure the integrity of this specified file"
                  " or manually fetch it again from"
                  " github.com/joonarafael/ohte/flaggame/src/logs/correctflags.txt.\n")
            self.correct_amount = -1
            return

        if self.complete_flag_list != correct_flags:
            print(f"\nERROR\nError while trying to ensure integrity of flag image source files."
                  f"\nFound a total of {len(self.complete_flag_list)} out of {self.correct_amount}"
                  f" .png files in {self.flag_dir}."
                  "\nPlease see flags subdirectory within src directory to ensure every flag file"
                  " is present and in .png format.\nSoftware is trying to find a .png file for"
                  " every 195 independent state listed at:"
                  " www.worldometers.info/geography/how-many-countries-are-there-in-the-world/"
                  " and Taiwan, Western Sahara & Kosovo."
                  "\nEnsure directory integrity by fetching flags again from"
                  " github.com/joonarafael/ohte/flaggame/src/flags.\n")

        else:
            print(f"All {self.correct_amount} flags have been found.")

    def list_every_flag(self):
        """
        print every flag source file to console
        """

        print()
        print("Debugging information about flag source files:")
        print("SOURCE Path:", self.working_dir)
        print("FLAGS  Path:", self.flag_dir)
        print("Amount of flags counted:", len(self.complete_flag_list))
        print("Complete list:")

        self.complete_flag_list.sort()

        for individual_flag in self.complete_flag_list:
            print(individual_flag)


MASTER_FLAGHANDLER = MasterFlagHandler(WORKING_DIR, FLAG_DIR)

MASTER_FLAGHANDLER.flag_import()
