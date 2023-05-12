import sys
from os import getcwd
from datetime import datetime
import csvhandler

WORKING_DIR = getcwd()

if WORKING_DIR[-3:] != "src":
    WORKING_DIR = WORKING_DIR + "/src"

HISTORY_PATH = WORKING_DIR + "/logs/history.txt"


class MasterHistoryHandler():
    """
    manage all game history
    """

    def __init__(self, history_path):
        """
        initialize the path to history file and record software launch

        Args:
            history_path (_type_): path to history.txt
        """

        self.history_path = history_path

        try:
            with open(self.history_path, 'r+', encoding="utf-8") as launch_file:
                file_len = len(launch_file.readlines())

            with open(self.history_path, 'a+', encoding="utf-8") as launch_file:
                if file_len == 0:
                    launch_file.write(
                        f"{self.curr_date()} NEW SESSION")

                else:
                    launch_file.write(
                        f"\n\n{self.curr_date()} NEW SESSION")

        except FileNotFoundError:
            with open(self.history_path, 'w+', encoding="utf-8") as launch_file:

                launch_file.write(
                    f"{self.curr_date()} NEW SESSION")

    def curr_date(self):
        """
        software launch is recorded within minutes accuracy

        Returns:
            string: date and hours:minutes '2023-05-02 14:20'
        """

        return datetime.now().isoformat(sep=" ", timespec="minutes")

    def curr_time(self):
        """
        game starts and ends are recorded within seconds accuracy

        Returns:
            string: time in hours:minutes:seconds '14:21:43'
        """

        return datetime.now().strftime('%H:%M:%S')

    def clear_history(self, remove_statistics: bool):
        """
        remove recorded game history

        Args:
            remove_statistics (bool): remove the statistics also or not
        """

        with open(self.history_path, 'w+', encoding="utf-8"):
            print("Deleting all recorded history...")

        if remove_statistics:
            csvhandler.MASTER_RUNNING_GAME.clear_stats_and_rounds()

        else:
            print("Closing program...")
            sys.exit(1)

    def console_print(self):
        """
        print the game history file to console
        """

        print()
        print("Contents of file 'history.txt':")

        with open(self.history_path, 'r', encoding="utf-8") as file:
            print(file.read())

    def game_start(self, mode: str):
        """
        write a new game start to file

        Args:
            mode (str): game mode as a string
        """

        with open(self.history_path, 'a+', encoding="utf-8") as game_start_file:
            game_start_file.write(
                f"\n\n    {mode} Game start off at {self.curr_time()}.")

    def game_over(self, info: list):
        """
        record game end

        Args:
            info (list): relevant information about the game is received in a 3-item list
            [game mode, score, longest streak]
        """

        with open(self.history_path, 'a+', encoding="utf-8") as game_over_file:
            if info[0] == 0:
                mode = "Classic"

            elif info[0] == 1:
                mode = "Advanced"

            elif info[0] == 2:
                mode = "Time Trial"

            else:
                mode = "One Life"

            game_over_file.write(
                f"\n    {mode} Game completed at {self.curr_time()}:")
            game_over_file.write(
                f"\n    Score: {info[1]} - Longest Continuous Streak: {info[2]}.")

    def game_terminated(self, info: list):
        """
        record a cancelled game

        Args:
            info (list): relevant information about the game is received in a 3- or 4-item list
            [game mode, score, longest streak, lives at termination]
        """

        with open(self.history_path, 'a+', encoding="utf-8") as game_terminated_file:
            if info[0] == 0:
                mode = "Classic"

            elif info[0] == 1:
                mode = "Advanced"

            elif info[0] == 2:
                mode = "Time Trial"

            elif info[0] == 3:
                mode = "One Life"

            else:
                mode = "Free"

            game_terminated_file.write(
                f"\n    {mode} Game cancelled at {self.curr_time()}:")

            if mode == "Free":
                game_terminated_file.write(
                    f"\n    Score: {info[1]} - Longest Continuous Streak: {info[2]}.")

            else:
                game_terminated_file.write((
                    f"\n    Score: {info[1]} - Longest Continuous Streak: {info[2]}."
                    f" {info[3]} lives left at termination."))

    def update(self):
        """
        read the history file and return the content to gui

        Returns:
            list / None: every row of history file is a separate list item
            ['GAME HISTORY', '', '', '2023-05-02 14:20 NEW SESSION', ...]
        """

        with open(self.history_path, 'r', encoding="utf-8") as update_file:
            return_list = update_file.read().splitlines()

            return_list.insert(0, "")
            return_list.insert(0, "")
            return_list.insert(0, "GAME HISTORY")

            return return_list


MASTER_HISTORY_HANDLER = MasterHistoryHandler(HISTORY_PATH)


def print_directories():
    """
    print the working directory (src) as well as the history file path
    """

    print("Main working directory path received from os.getcwd():")
    print(getcwd())
    print("Source folder path:")
    print(WORKING_DIR)
    print("History file path:")
    print(HISTORY_PATH)
