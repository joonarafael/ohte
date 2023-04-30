from tkinter import *  # pylint: disable=wildcard-import disable=unused-wildcard-import
from PIL import Image, ImageTk
import timerlogic
from gamehandler import GameHandler
from flaghandler import WORKING_DIR


class GameTab:
    """
    class is responsible for showing the first tab within the game master window
    it displays all relevant content for the actual game
    """

    def __init__(self, root: Tk, frame: Frame):
        """
        constructor sets all neccessary elements for the actual game to be displayed

        Args:
            root (Tk): master game window instance
            frame (Frame): the notebook tab element within the master window
        """

        self.root = root
        self.frame = frame

        self.game_label = Label(self.frame, text="FLAG QUIZ GAME", font=(
            "Arial", 14, 'bold'), fg="#e6e6e6", bg="#333333")
        self.game_label.grid(row=0, column=0, columnspan=5)

        self.answer_label = Label(self.frame, text="Start a new game from File > New Game.", font=(
            "Arial", 12), fg="#e6e6e6", bg="#333333")
        self.answer_label.grid(row=1, column=0, columnspan=5)

        self.round_label = Label(self.frame, text="Round", font=(
            "Arial", 12), fg="#e6e6e6", bg="#333333")
        self.round_label.grid(row=2, column=0)

        self.score_label = Label(self.frame, text="Score", font=(
            "Arial", 12), fg="#e6e6e6", bg="#333333")
        self.score_label.grid(row=2, column=1)

        self.timer_label = Label(self.frame, text="Timer", font=(
            "Arial", 12), fg="#e6e6e6", bg="#333333")
        self.timer_label.grid(row=2, column=2)

        self.lives_label = Label(self.frame, text="Lives", font=(
            "Arial", 12), fg="#e6e6e6", bg="#333333")
        self.lives_label.grid(row=2, column=3)

        self.streak_label = Label(self.frame, text="Streak", font=(
            "Arial", 12), fg="#e6e6e6", bg="#333333")
        self.streak_label.grid(row=2, column=4)

        self.img = Image.open(WORKING_DIR + "/placeholder-image.png")
        self.img.thumbnail((500, 500), Image.LANCZOS)
        photo_image = ImageTk.PhotoImage(self.img)
        self.photo_label = Label(self.frame, image=photo_image, borderwidth=0,
                                 highlightthickness=0, relief="flat")
        self.photo_label.grid(row=3, column=0, columnspan=5)

        self.button0 = Button(self.frame, text="OPTION 1", state=DISABLED, width=36, pady=10,
                              padx=10, relief="groove", borderwidth=0, highlightthickness=0,
                              command=self.button_0_function)
        self.button0.grid(row=4, column=0, columnspan=2)
        self.button1 = Button(self.frame, text="OPTION 2", state=DISABLED, width=36, pady=10,
                              padx=10, relief="groove", borderwidth=0, highlightthickness=0,
                              command=self.button_1_function)
        self.button1.grid(row=4, column=3, columnspan=2)
        self.button2 = Button(self.frame, text="OPTION 3", state=DISABLED, width=36, pady=10,
                              padx=10, relief="groove", borderwidth=0, highlightthickness=0,
                              command=self.button_2_function)
        self.button2.grid(row=5, column=0, columnspan=2)
        self.button3 = Button(self.frame, text="OPTION 4", state=DISABLED, width=36, pady=10,
                              padx=10, relief="groove", borderwidth=0, highlightthickness=0,
                              command=self.button_3_function)
        self.button3.grid(row=5, column=3, columnspan=2)

    def set_game_handler(self, game_handler: GameHandler):
        """
        game tab needs to access master gamehandler properties & functions
        however, this gamehandler instance can be only passed after game tab (this class)
        has been first initialized

        Args:
            game_handler (GameHandler): receive the master gamehandler instance from
                                        master game window
        """

        self.game_handler = game_handler  # pylint: disable=attribute-defined-outside-init

    def next_flag(self, path: str):
        """
        function to update the next flag to player through the viewport

        Args:
            path (str): string containing the full path to next flag (source file on disk)
        """

        img2 = Image.open(path)
        img2.thumbnail((450, 450), Image.LANCZOS)
        im2 = ImageTk.PhotoImage(img2)
        self.photo_label.configure(image=im2)
        self.photo_label.image = im2

    def change_title(self, new_text: str, new_color: str):
        """
        function to update the game title (e.g. game modes or 'Game Over!')

        Args:
            new_text (str): new displayed text as a string
            new_color (str): new color for the text (hex value in str as '#12AB56')
        """

        self.game_label.configure(text=new_text, fg=new_color)

    def change_status(self, new_text: str, new_color: str):
        """
        function to update the game status (e.g. 'Correct!' or what was the right answer)

        Args:
            new_text (str): new displayed text as a string
            new_color (str): new color for the text (hex value in str as '#12AB56')
        """

        self.answer_label.configure(text=new_text, fg=new_color)

    def display_round(self, current_round: int):
        """
        function to update current round number

        Args:
            current_round (int): new round as an integer
        """

        self.round_label.config(text=f"Round: {current_round}")

    def display_score(self, score: int):
        """
        function to update current score number

        Args:
            score (int): new score as an integer
        """

        self.score_label.config(text=f"Score: {score}")

    def display_timer(self):
        """
        function to update the timer
        """

        game_mode = self.game_handler.game_mode
        displayed_time = round(timerlogic.clock.read_displayed(), 1)

        if game_mode == 1:
            self.timer_label.config(
                text=f"{displayed_time:>7}", fg="#e6e6e6")
            self.timer_label.after(100, self.display_timer)

        elif game_mode == 2:
            if timerlogic.clock.read_accurate() >= 5.001:
                self.game_handler.player_answered(0)
                self.timer_label.config(text="  0.0  ", fg="#ff6e6e")

            else:
                displayed_time = round(5.0 - displayed_time, 1)
                displayed_time = max(displayed_time, 0.0)

                if displayed_time <= 1.5:
                    self.timer_label.config(
                        text=f"{displayed_time:>7}", fg="#ff6e6e")

                else:
                    self.timer_label.config(
                        text=f"{displayed_time:>7}", fg="#e6e6e6")

                self.timer_label.after(100, self.display_timer)

        else:
            self.timer_label.config(text="Timer", fg="#e6e6e6")

    def display_lives(self, lives: int, color: str):
        """
        function to update current lives count

        Args:
            lives (int): new lives count as an integer
            color (str): new color for the text (hex value in str as '#12AB56')
        """

        self.lives_label.config(text=f"Lives: {lives}", fg=color)

    def display_streak(self, streak: int):
        """
        function to update current streak length

        Args:
            streak (int): new streak length as an integer
        """

        self.streak_label.config(text=f"Streak: {streak}")

    def button_0_function(self):
        self.game_handler.player_answered(0)

    def button_1_function(self):
        self.game_handler.player_answered(1)

    def button_2_function(self):
        self.game_handler.player_answered(2)

    def button_3_function(self):
        self.game_handler.player_answered(3)

    def next_buttons(self, options: list):
        """
        function to update button texts

        Args:
            options (list): 4-item list containing 4 new country names to display
        """

        self.button0.configure(text=options[0], state=NORMAL)
        self.button1.configure(text=options[1], state=NORMAL)
        self.button2.configure(text=options[2], state=NORMAL)
        self.button3.configure(text=options[3], state=NORMAL)

    def inactive_buttons(self):
        """
        function to disable buttons and to make them look 'inactive'
        """

        self.button0.configure(text="OPTION 1", state=DISABLED)
        self.button1.configure(text="OPTION 2", state=DISABLED)
        self.button2.configure(text="OPTION 3", state=DISABLED)
        self.button3.configure(text="OPTION 4", state=DISABLED)
