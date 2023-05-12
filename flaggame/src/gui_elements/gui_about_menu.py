from tkinter import *  # pylint: disable=wildcard-import disable=unused-wildcard-import
import tkinter.messagebox


class AboutMenu:
    """
    'About' drop-down menu within the game master window (main menu)
    """

    def __init__(self, root: tkinter.Tk, master_menu: tkinter.Menu,
                 menu_tearoff: int, version: str):
        """
        initialize the 'About' menu

        Args:
            root (tkinter.Tk): master game window instance,
            master_menu (tkinter.Menu): main menu instance within root,
            menu_tearoff (int): integer for menu tearoff,
            version (str): current software version
        """

        self.root = root
        self.version = version

        self.about_menu = Menu(master_menu, tearoff=menu_tearoff)
        self.print_selection = Menu(self.about_menu, tearoff=0)

        self.about_menu.add_command(
            label="Show about", command=self.show_about)

    def show_about(self):
        """
        display the 'about' pop-up screen
        """

        tkinter.messagebox.showinfo(
            "About", ("Joona Kettunen"
                      " github.com/joonarafael/ohte"
                      f" Flag Quiz Game v. {self.version}"
                      " Ohjelmistotekniikka K2023"))
