from tkinter import *  # pylint: disable=wildcard-import disable=unused-wildcard-import
import flaghandler
import csvhandler
from history import print_directories, console_print
from rules import GAME_RULES_PATH


class DebugMenu:
    """
    class is responsible for the 'Debug' drop-down menu within the game master window
    """

    def __init__(self, root: Tk, master_menu: Menu, menu_tearoff: int, stats_tab):
        """
        constructor initializes both the parent 'Debug' menu and child drop-down
        (the menu for print selection)

        Args:
            root (Tk): master game window instance
            master_menu (Menu): main menu instance within root
            menu_tearoff (int): integer to determine menu tearoff
            stats_tab: receive the stats tab gui element from master window (for function calling)
        """

        self.root = root
        self.stats_tab = stats_tab

        self.debug_menu = Menu(master_menu, tearoff=menu_tearoff)
        self.print_selection = Menu(self.debug_menu, tearoff=0)

        self.debug_menu.add_cascade(
            label="Print to console...", menu=self.print_selection)
        self.debug_menu.add_command(
            label="Retry flag import", command=self.retry_import)

        self.print_selection.add_command(
            label="Recorded history", command=self.history_print)
        self.print_selection.add_command(
            label="Recorded rounds", command=self.rounds_print)
        self.print_selection.add_command(
            label="Recorded streaks", command=self.streaks_print)
        self.print_selection.add_command(
            label="Recorded games", command=self.games_print)
        self.print_selection.add_command(
            label="Recorded stats", command=self.stats_print)
        self.print_selection.add_command(
            label="Critical directory paths", command=self.directories)
        self.print_selection.add_command(
            label="Flag source files", command=self.flag_list)

    def directories(self):
        """
        debug option to print all critical directories and file paths used by the software
        """

        print("\nCRITICAL DIRECTORIES:")
        print_directories()
        print("Flag directory:")
        print(flaghandler.FLAG_DIR + "/")
        print("Rulebook directory:")
        print(GAME_RULES_PATH)
        print("Statistics files paths:")
        print(csvhandler.ROUNDS_PATH)
        print(csvhandler.STREAKS_PATH)
        print(csvhandler.STATS_PATH)

    def flag_list(self):
        flaghandler.list_every_flag()

    def retry_import(self):
        flaghandler.flag_import(flaghandler.CORRECT_AMOUNT)

    def history_print(self):
        console_print()

    def rounds_print(self):
        csvhandler.MASTER_RUNNING_GAME.print_round_file()

    def streaks_print(self):
        csvhandler.MASTER_RUNNING_GAME.print_streaks_file()

    def games_print(self):
        csvhandler.MASTER_RUNNING_GAME.print_stats()

    def stats_print(self):
        """
        player lifelong statistics need formatting before printed to console
        """

        ignore_status = self.stats_tab.ignore_free_mode_games

        content = csvhandler.MASTER_RUNNING_GAME.calculate_true_stats(
            ignore_status)

        print()
        print("Statistics recorded:")

        for key, value in content.items():
            print(f"{key:<30} : {value}")
