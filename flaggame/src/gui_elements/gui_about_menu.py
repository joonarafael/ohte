from tkinter import *  # pylint: disable=wildcard-import disable=unused-wildcard-import
import tkinter.messagebox


class AboutMenu:
    """
    class is responsible for the 'About' drop-down menu within the game master window
    """

    def __init__(self, root: tkinter.Tk, master_menu: tkinter.Menu,
                 menu_tearoff: int, version: str):
        """
        constructor initializes the 'About' menu

        Args:
            root (tkinter.Tk): master game window instance
            master_menu (tkinter.Menu): main menu instance within root
            menu_tearoff (int): integer to determine menu tearoff
            version (str): current software version to be displayed in 'about' pop-up
        """

        self.root = root
        self.version = version

        self.about_menu = Menu(master_menu, tearoff=menu_tearoff)
        self.print_selection = Menu(self.about_menu, tearoff=0)

        self.about_menu.add_command(
            label="Show about", command=self.show_about)

    def show_about(self):
        """
        function to display the 'about' pop-up when called
        """

        tkinter.messagebox.showinfo(
            "About", ("Joona Kettunen"
                      " github.com/joonarafael/ohte"
                      f" Flag Quiz Game v. {self.version}"
                      " Ohjelmistotekniikka K2023"))
