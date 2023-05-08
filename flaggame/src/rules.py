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
        establish a path to game rulebook

        Args:
            rules_path (_type_): path to rulebook gamerules.txt
        """

        self.rules_path = rules_path

    def read_rules(self):
        """
        read the rulebook and return the content to gui

        Returns:
            list / None: every row of rulebook file is a separate list item
            ['RULEBOOK', '', '', 'CLASSIC', ...]
        """

        try:
            with open(self.rules_path, 'r+', encoding="utf-8") as update_file:
                lines = update_file.readlines()

                if len(lines) == 70:
                    return [line.strip() for line in lines]

                print("Rulebook integrity compromised. Please fetch the correct rulebook"
                      " from github.com/joonarafael/ohte/flaggame/src/logs/gamerules.txt."
                      "\nSoftware relaunch needed to display rules again.")

                return None

        except FileNotFoundError:
            print(f"Can't find the game rule book file 'gamerules.txt'."
                  f"\nPlease replace {self.rules_path} with the correct file."
                  "\nSoftware relaunch needed to display rules again.")
            return None


RULES_READER = MasterRulesReader(GAME_RULES_PATH)
