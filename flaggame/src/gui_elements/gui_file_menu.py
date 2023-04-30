from tkinter import *  # pylint: disable=wildcard-import disable=unused-wildcard-import
import tkinter.messagebox
from history import clear_history
from gamehandler import GameHandler
from flaghandler import COMPLETE_FLAG_LIST, CORRECT_AMOUNT


class FileMenu:
    """
    class is responsible for the 'File' drop-down menu within the game master window
    """

    def __init__(self, root: tkinter.Tk, master_menu: tkinter.Menu,
                 menu_tearoff: int, game_handler: GameHandler):
        """
        constructor initializes both the parent 'File' menu and child drop-downs
        (the menu for game mode selection and history clearing)

        Args:
            root (tkinter.Tk): master game window instance
            master_menu (tkinter.Menu): main menu instance within root
            menu_tearoff (int): integer to determine menu tearoff
            game_handler (GameHandler): receive the master gamehandler instance from master window
        """

        self.root = root
        self.game_handler = game_handler
        self.resolution_locked = True

        self.file_menu = Menu(master_menu, tearoff=menu_tearoff)
        self.game_mode_selection = Menu(self.file_menu, tearoff=0)
        self.clear_memory = Menu(self.file_menu, tearoff=0)

        self.file_menu.add_cascade(
            label="New game...", menu=self.game_mode_selection)
        self.file_menu.add_command(
            label="Cancel game", command=self.reset_gamehandler)
        self.file_menu.add_command(
            label="Lock / Unlock resolution", command=self.unlock_resolution)
        self.file_menu.add_command(
            label="Free flag browsing", command=self.flag_slide_show)
        self.file_menu.add_cascade(
            label="Clear history...", menu=self.clear_memory)
        self.file_menu.add_command(label="Exit", command=self.exit_game)

        self.clear_memory.add_command(
            label="Clear history only", command=self.clear_history)
        self.clear_memory.add_command(
            label="Clear history & stats", command=self.clear_stats)

        self.game_mode_selection.add_command(
            label="Classic", command=self.start_classic_game)
        self.game_mode_selection.add_command(
            label="Advanced", command=self.start_advanced_game)
        self.game_mode_selection.add_command(
            label="Time Trial", command=self.start_time_game)
        self.game_mode_selection.add_command(
            label="One Life", command=self.start_one_life_game)
        self.game_mode_selection.add_command(
            label="Free Mode", command=self.start_free_game)

    def reset_gamehandler(self):
        self.game_handler.reset_game_handler()

    def unlock_resolution(self):
        """
        function locks and unlocks the master window resolution when called
        """

        if self.resolution_locked:
            self.resolution_locked = False
            self.root.minsize(0, 0)
            self.root.maxsize(0, 0)

            print("Window resolution unlocked.")

            return

        lock_height = self.root.winfo_height()
        lock_width = self.root.winfo_width()

        print(f"Window resolution locked to {lock_width}x{lock_height}.")

        self.root.minsize(lock_width, lock_height)
        self.root.maxsize(lock_width, lock_height)

        self.resolution_locked = True

    def clear_history(self):
        """
        function requests history deletion
        """

        result = tkinter.messagebox.askyesno(
            "Sure?", ("Are You sure You wish to clear all history from file and exit program?"
                      " Statistics are saved, recorded history will be lost."))

        if not result:
            return

        clear_history(False)

    def clear_stats(self):
        """
        function requests full history & stats deletion
        """

        result = tkinter.messagebox.askyesno(
            "Sure?", ("Are You sure You wish to clear all history"
                      " and recorded statistics from file and exit program?"
                      " All progress will be permanently lost."))

        if not result:
            return

        clear_history(True)

    def flag_slide_show(self):
        if len(COMPLETE_FLAG_LIST) == CORRECT_AMOUNT:
            self.game_handler.flag_slide_show(0)

    def exit_game(self):
        """
        function to ask 'are you sure?' when exiting
        """

        ans = tkinter.messagebox.askyesno(
            "Exit?", ("Are You sure You want to exit?"
                      " Any ongoing game will be terminated."))

        if ans:
            self.game_handler.terminated_game()

            print("Program exit...")
            self.root.destroy()

    def start_classic_game(self):
        self.game_handler.classic()

    def start_advanced_game(self):
        self.game_handler.advanced()

    def start_time_game(self):
        self.game_handler.time_trial()

    def start_one_life_game(self):
        self.game_handler.one_life()

    def start_free_game(self):
        self.game_handler.free()
