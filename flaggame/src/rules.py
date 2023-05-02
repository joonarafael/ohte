from os import getcwd

WORKING_DIR = getcwd()

if WORKING_DIR[-3:] != "src":
    WORKING_DIR = WORKING_DIR + "/src"

GAME_RULES_PATH = WORKING_DIR + "/logs/gamerules.txt"


class MasterRulesReader():
    """
    read the rules find and handle any errors
    """

    def __init__(self, rules_path):
        """
        check integrity of rulebook file, handle any errors

        Args:
            rules_path (_type_): path to rulebook gamerules.txt
        """

        self.rules_path = rules_path
        self.master_error = True

        print("Opening the game rule book file 'gamerules.txt'...")

        try:
            with open(self.rules_path, 'r+', encoding="utf-8") as launch_file:
                file_len = len(launch_file.readlines())

                if file_len != 70:
                    print("Game rule book file 'gamerules.txt' integrity compromised.")
                    print(
                        f"Please replace {self.rules_path} with correct file.")

                else:
                    self.master_error = False

        except FileNotFoundError:
            print("Can't find the game rule book file 'gamerules.txt'.")
            print(f"Please replace {self.rules_path} with correct file.")

        if self.master_error:
            print("ERROR while opening 'gamerules.txt'.")
            print("Software relaunch needed to display rules again.")

    def read_rules(self):
        """
        read the rulebook and return the content to gui

        Returns:
            list / None: every row of rulebook file is a separate list item
            ['RULEBOOK', '', '', 'CLASSIC', ...]
        """

        if not self.master_error:
            with open(self.rules_path, 'r', encoding="utf-8") as update_file:
                return update_file.read().splitlines()

        return None


RULES_READER = MasterRulesReader(GAME_RULES_PATH)
