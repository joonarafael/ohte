from tkinter import *  # pylint: disable=wildcard-import disable=unused-wildcard-import


class StatsMenu:
    """
    'Stats' drop-down menu within the game master window (main menu)
    """

    def __init__(self, root: Tk, master_menu: Menu, menu_tearoff: int, stats_tab):
        """
       initialize the 'Stats' menu

        Args:
            root (tkinter.Tk): master game window instance,
            master_menu (tkinter.Menu): main menu instance within root,
            menu_tearoff (int): integer for menu tearoff,
            stats_tab: stats tab gui element from master window (for function calling)
        """

        self.root = root
        self.stats_tab = stats_tab

        self.stats_menu = Menu(master_menu, tearoff=menu_tearoff)
        self.print_selection = Menu(self.stats_menu, tearoff=0)

        self.stats_menu.add_command(
            label="Switch Game Browse View", command=self.switch_view)
        self.stats_menu.add_command(
            label="Force refresh stats", command=self.refresh_stats)
        self.stats_menu.add_command(
            label="Ignore / Include Free Mode Games", command=self.ignore_free_games)

    def switch_view(self):
        """
        change the view layout of the stats tab between lifelong stats / game browsing
        """

        self.stats_tab.view_switching()

    def refresh_stats(self):
        """
        force the statistics update (more of a debug option)
        """

        self.stats_tab.stats_update()

    def ignore_free_games(self):
        """
        player may choose to include/ignore free mode games within stats calculation
        """

        if self.stats_tab.ignore_free_mode_games:
            self.stats_tab.ignore_free_mode_games = False

        else:
            self.stats_tab.ignore_free_mode_games = True

        self.stats_tab.stats_update()
