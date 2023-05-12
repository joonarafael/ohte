from tkinter import *  # pylint: disable=wildcard-import disable=unused-wildcard-import
from tkinter import ttk

from gui_elements import gui_stats, gui_history, gui_rules, gui_game
from gui_elements import gui_file_menu, gui_debug_menu
from gui_elements import gui_stats_menu, gui_about_menu

from gamehandler import MasterGameHandler

print("Necessary libraries for GUI imported, drawing interface...")


class MasterGameWindow:
    """
    master game window instance
    """

    def __init__(self, version: str):
        """
        initialize all master window settings,
        generate the main menu and the 4-tab notebook system

        Args:
            version (str): software version
        """

        self.current_version = version
        self.launch_resolution = (663, 700)

        self.window = Tk()
        self.window.title("Flag Quiz Game")
        self.window.geometry(
            f"{self.launch_resolution[0]}x{self.launch_resolution[1]}")
        self.window.minsize(
            self.launch_resolution[0], self.launch_resolution[1])
        self.window.maxsize(
            self.launch_resolution[0], self.launch_resolution[1])

        self.notebook = ttk.Notebook(self.window)
        self.tab0 = Frame(self.notebook, bg="#333333", relief="flat",
                          borderwidth=0, highlightthickness=0)
        self.tab1 = Frame(self.notebook, bg="#333333", relief="flat",
                          borderwidth=0, highlightthickness=0)
        self.tab2 = Frame(self.notebook, bg="#333333", relief="flat",
                          borderwidth=0, highlightthickness=0)
        self.tab3 = Frame(self.notebook, bg="#333333", relief="flat",
                          borderwidth=0, highlightthickness=0)

        self.tab0.rowconfigure(0, weight=0, uniform='titles')
        self.tab0.rowconfigure(1, weight=0, uniform='titles')
        self.tab0.rowconfigure(2, weight=0, uniform='titles')
        self.tab0.rowconfigure(3, weight=1, uniform='viewport')
        self.tab0.rowconfigure(4, weight=0, uniform='buttons')
        self.tab0.rowconfigure(5, weight=0, uniform='buttons')

        self.notebook.add(self.tab0, text="Game")
        self.notebook.add(self.tab1, text="Stats")
        self.notebook.add(self.tab2, text="History")
        self.notebook.add(self.tab3, text="Rules")
        self.notebook.pack(expand=True, fill="both")

        self.game_tab = gui_game.GameTab(self.window, self.tab0)
        self.stats_tab = gui_stats.StatsTab(self.window, self.tab1)
        self.stats_tab.stats_update()
        self.history_tab = gui_history.HistoryTab(self.window, self.tab2)
        self.history_tab.history_update()
        self.rules_tab = gui_rules.RulesTab(self.window, self.tab3)

        self.game_handler = MasterGameHandler(
            self.game_tab, self.stats_tab, self.history_tab)

        self.game_tab.set_game_handler(self.game_handler)

        self.menu_bar = Menu(self.window)
        self.window.config(menu=self.menu_bar)

        self.file_menu = gui_file_menu.FileMenu(
            self.window, self.menu_bar, 0, self.game_handler)
        self.debug_menu = gui_debug_menu.DebugMenu(
            self.window, self.menu_bar, 0, self.stats_tab)
        self.stats_menu = gui_stats_menu.StatsMenu(
            self.window, self.menu_bar, 0, self.stats_tab)
        self.about_menu = gui_about_menu.AboutMenu(self.window, self.menu_bar,
                                                   0, self.current_version)

        self.menu_bar.add_cascade(label="File", menu=self.file_menu.file_menu)
        self.menu_bar.add_cascade(
            label="Stats", menu=self.stats_menu.stats_menu)
        self.menu_bar.add_cascade(
            label="Debug", menu=self.debug_menu.debug_menu)
        self.menu_bar.add_cascade(
            label="About", menu=self.about_menu.about_menu)

        print("GUI generated and fully operational.")
        print("Game ready.")

    def start(self):
        """
        run the Tkinter mainloop
        """

        self.window.protocol("WM_DELETE_WINDOW", self.file_menu.exit_game)
        self.window.mainloop()
