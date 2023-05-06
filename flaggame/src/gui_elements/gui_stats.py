from tkinter import *  # pylint: disable=wildcard-import disable=unused-wildcard-import
import csvhandler


class StatsTab:
    """
    handle the second tab within the game master window
    displays the player lifelong statistics
    """

    def __init__(self, root: Tk, frame: Frame):
        """
        initialize all neccessary elements for the player statistics to be displayed

        Args:
            root (Tk): master game window instance
            frame (Frame): notebook tab element within the master window
        """

        self.root = root
        self.frame = frame
        self.ignore_free_mode_games = False
        self.view = 0

        self.stats_label = Label(
            self.frame, relief="flat", borderwidth=0, highlightthickness=0)
        self.stats_label.grid(sticky="NSEW")
        self.stats_label.grid_rowconfigure(0, weight=1)

        self.stats_text = Text(self.stats_label, state="disabled", fg="#e6e6e6", bg="#333333",
                               relief="flat", borderwidth=0, highlightthickness=0)
        self.stats_text.grid(row=0, column=1, sticky="NSEW")

        self.stats_scroll = Scrollbar(
            self.stats_label, command=self.stats_text.yview)
        self.stats_text.config(yscrollcommand=self.stats_scroll.set)
        self.stats_scroll.grid(row=0, column=0, sticky="ns")

        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(0, minsize=20)
        self.frame.rowconfigure(0, weight=1)

    def stats_update(self):
        """
        update the content within the text element always when statistics change
        also writes statistics again if player wishes to include/ignore
        free moode games in calculations
        """

        self.view = 0
        self.stats_text.config(state='normal')
        self.stats_text.delete('1.0', END)

        content = csvhandler.MASTER_RUNNING_GAME.calculate_true_stats(
            self.ignore_free_mode_games)

        if self.ignore_free_mode_games:
            self.stats_text.insert(
                END, "STATISTICS IGNORING FREE MODE GAMES\n\n")

        else:
            self.stats_text.insert(END, "PLAYER LIFELONG STATISTICS\n\n")

        text_line = []

        for key, value in content.items():
            text_line.append((key.replace("_", " "), value))

        r_i = 0

        while True:
            if r_i <= len(text_line) - 2:
                gui_row = (f"{text_line[r_i][0]:<30}{text_line[r_i][1]:<8}"
                           f" | {text_line[r_i + 1][0]:<30}{text_line[r_i + 1][1]:<8}\n\n")

            elif r_i == len(text_line) - 1:
                gui_row = f"{text_line[r_i][0]:<30}{text_line[r_i][1]:<8}"

            else:
                break

            self.stats_text.insert(END, gui_row)
            r_i += 2

        self.stats_text.config(state='disabled')

    def games_update(self):
        """
        update the content within the text element always when statistics change
        also writes statistics again if player wishes to include/ignore
        free moode games in calculations
        """

        self.view = 1
        self.stats_text.config(state='normal')
        self.stats_text.delete('1.0', END)

        content = csvhandler.MASTER_RUNNING_GAME.stats_formatting(True)

        self.stats_text.insert(END, "ALL RECORDED GAMES\n\n")

        for row in content:
            self.stats_text.insert(END, f"{row}\n")

        self.stats_text.config(state='disabled')

    def view_switching(self):
        """
        switch the stats view from lifelong to individual games (and back)
        """

        if self.view == 0:
            self.games_update()

        else:
            self.stats_update()
