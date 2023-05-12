from tkinter import *  # pylint: disable=wildcard-import disable=unused-wildcard-import
import history


class HistoryTab:
    """
    handle the third tab within the game master window,
    displays the game history with dynamic updating
    """

    def __init__(self, root: Tk, frame: Frame):
        """
        initialize all neccessary elements for the game history to be displayed

        Args:
            root (Tk): master game window instance,
            frame (Frame): notebook tab element within the master window
        """

        self.root = root
        self.frame = frame

        self.history_label = Label(
            self.frame, relief="flat", borderwidth=0, highlightthickness=0)
        self.history_label.grid(sticky="NSEW")
        self.history_label.grid_rowconfigure(0, weight=1)

        self.history_text = Text(self.history_label, state="disabled", fg="#e6e6e6", bg="#333333",
                                 relief="flat", borderwidth=0, highlightthickness=0)
        self.history_text.grid(row=0, column=1, sticky="NSEW")

        self.history_scroll = Scrollbar(
            self.history_label, command=self.history_text.yview)
        self.history_text.config(yscrollcommand=self.history_scroll.set)
        self.history_scroll.grid(row=0, column=0, sticky="ns")

        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(0, minsize=20)
        self.frame.rowconfigure(0, weight=1)

    def history_update(self):
        """
        update the content within the text element (write whole page from scratch)
        """

        self.history_text.config(state='normal')
        self.history_text.delete('1.0', END)
        content = history.MASTER_HISTORY_HANDLER.update()

        for row in content:
            self.history_text.insert(END, f"{row}\n")

        self.history_text.config(state='disabled')
