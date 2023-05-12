from tkinter import *  # pylint: disable=wildcard-import disable=unused-wildcard-import
import rules


class RulesTab:
    """
    handle the fourth tab within the game master window,
    displays the game rulebook
    """

    def __init__(self, root: Tk, frame: Frame):
        """
        initialize all neccessary elements for the game rulebook to be displayed

        Args:
            root (Tk): master game window instance,
            frame (Frame): notebook tab element within the master window
        """

        self.root = root
        self.frame = frame

        self.rules_label = Label(
            self.frame, relief="flat", borderwidth=0, highlightthickness=0)
        self.rules_label.grid(sticky="NSEW")
        self.rules_label.grid_rowconfigure(0, weight=1)

        self.rules_text = Text(self.rules_label, state="disabled", fg="#e6e6e6", bg="#333333",
                               relief="flat", borderwidth=0, highlightthickness=0)
        self.rules_text.grid(row=0, column=1, sticky="NSEW")

        self.rules_scroll = Scrollbar(
            self.rules_label, command=self.rules_text.yview)
        self.rules_text.config(yscrollcommand=self.rules_scroll.set)
        self.rules_scroll.grid(row=0, column=0, sticky="ns")

        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(0, minsize=20)
        self.frame.rowconfigure(0, weight=1)

        self.write_rulebook()

    def write_rulebook(self):
        """
        write the rulebook
        """

        self.rules_text.config(state='normal')
        self.rules_text.delete('1.0', END)
        rules_content = rules.RULES_READER.read_rules()

        if rules_content is not None:
            for rows in rules_content:
                self.rules_text.insert(END, f"{rows}\n")

        else:
            self.rules_text.insert(END, "RULEBOOK IMPORT ERROR")

        self.rules_text.config(state='disabled')
