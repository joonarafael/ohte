# FOR PRACTICAL REASONS AND OWN MENTAL WELL-BEING I WANT TO IMPORT
# ALL TKINTER LIBRARIES, PYLINT DISABLE ADDED TO IGNORRE THESE !!!

from tkinter import *  # pylint: disable=wildcard-import disable=unused-wildcard-import
from tkinter import ttk  # pylint: disable=unused-import
import tkinter.messagebox
from PIL import Image, ImageTk
import flaghandler
import timerlogic
import history
import rules
import gamehandler

print("Necessary libraries for GUI imported, drawing interface...")

CURRENT_VERSION = "0.1.8"


# master window settings
window = Tk()
window.title("Flag Game")
window.geometry("660x750")
window.minsize(660, 750)
window.maxsize(660, 750)

# define "are you sure" screen


def exit_game():
    ans = tkinter.messagebox.askyesno(
        "Exit?", ("Are You sure You want to exit?"
                  " Any ongoing game will be terminated."))

    if ans:
        gamehandler.MASTER_GAME_HANDLER.terminated_game()
        print("Program exit...")
        window.destroy()


# create menubar
menu_bar = Menu(window)
window.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
debug_menu = Menu(menu_bar, tearoff=0)
about_menu = Menu(menu_bar, tearoff=0)
game_mode_selection = Menu(file_menu, tearoff=0)

menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="Debug", menu=debug_menu)
menu_bar.add_cascade(label="About", menu=about_menu)

# define file menu commands


def history_print():
    history.console_print()


def clear_history():
    result = tkinter.messagebox.askyesno(
        "Sure?", ("Are You sure You wish to clear all history from file and exit program?"
                  " All progress will be permanently lost."))

    if not result:
        return

    history.clear_history()


# define file menu
file_menu.add_cascade(label="New game", menu=game_mode_selection)
file_menu.add_command(label="Print history to console", command=history_print)
file_menu.add_command(label="Clear history...", command=clear_history)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_game)

# define debug menu commands


def directories():
    print("CRITICAL DIRECTORIES:")
    history.print_directories()
    print("Flag Directory:")
    print(flaghandler.FLAG_DIR)


def flag_list():
    flaghandler.list_every_flag()


def retry_import():
    flaghandler.flag_import(flaghandler.CORRECT_AMOUNT)


def toggle_status_print():
    if gamehandler.MASTER_GAME_HANDLER.dev_status_print:
        print("Dev print game status disabled.")
        gamehandler.MASTER_GAME_HANDLER.dev_status_print = False

    else:
        print("Dev print game status enabled.")
        gamehandler.MASTER_GAME_HANDLER.dev_status_print = True


def flag_slide_show():
    if len(flaghandler.COMPLETE_FLAG_LIST) == flaghandler.CORRECT_AMOUNT:
        gamehandler.MASTER_GAME_HANDLER.flag_slide_show(1)


# define debug menu
debug_menu.add_command(
    label="List critical directory paths to console", command=directories)
debug_menu.add_command(
    label="List flag source files to console", command=flag_list)
debug_menu.add_command(label="Retry flag import...", command=retry_import)
debug_menu.add_command(
    label="Toggle Dev print game status to console", command=toggle_status_print)
debug_menu.add_command(label="Free flag browsing", command=flag_slide_show)

# define about menu commands


def show_about():
    tkinter.messagebox.showinfo(
        "About", ("Joona Kettunen"
                  " github.com/joonarafael/ohte"
                  f" Flag Game v. {CURRENT_VERSION}"
                  " Ohjelmistotekniikka K2023"))


# define about menu
about_menu.add_command(label="About...", command=show_about)

# define different game starts


def start_classic_game():
    if len(flaghandler.COMPLETE_FLAG_LIST) == flaghandler.CORRECT_AMOUNT:
        gamehandler.MASTER_GAME_HANDLER.classic()


def start_advanced_game():
    if len(flaghandler.COMPLETE_FLAG_LIST) == flaghandler.CORRECT_AMOUNT:
        gamehandler.MASTER_GAME_HANDLER.advanced()


def start_time_game():
    if len(flaghandler.COMPLETE_FLAG_LIST) == flaghandler.CORRECT_AMOUNT:
        gamehandler.MASTER_GAME_HANDLER.time_trial()


def start_one_life_game():
    if len(flaghandler.COMPLETE_FLAG_LIST) == flaghandler.CORRECT_AMOUNT:
        gamehandler.MASTER_GAME_HANDLER.one_life()


def start_free_game():
    if len(flaghandler.COMPLETE_FLAG_LIST) == flaghandler.CORRECT_AMOUNT:
        gamehandler.MASTER_GAME_HANDLER.free()


# define game mode selection menu
game_mode_selection.add_command(label="Classic", command=start_classic_game)
game_mode_selection.add_command(label="Advanced", command=start_advanced_game)
game_mode_selection.add_command(label="Time Trial", command=start_time_game)
game_mode_selection.add_command(label="One Life", command=start_one_life_game)
game_mode_selection.add_command(label="Free Mode", command=start_free_game)

# define 'tab' system
notebook = ttk.Notebook(window)
tab0 = Frame(notebook, bg="#333333")
tab1 = Frame(notebook, bg="#cbe0c3")
tab2 = Frame(notebook, bg="#cce0f2")

notebook.add(tab0, text="Game")
notebook.add(tab1, text="History")
notebook.add(tab2, text="Rules")
notebook.pack(expand=True, fill="both")

# main title
if len(flaghandler.COMPLETE_FLAG_LIST) != flaghandler.CORRECT_AMOUNT:
    gameLabel = Label(tab0, text="FLAG IMAGES IMPORT ERROR, SEE CONSOLE FOR DETAILS", font=(
        "Arial", 12), fg="#e6e6e6", bg="#333333")

else:
    gameLabel = Label(tab0, text="Flag Game", font=(
        "Arial", 14), fg="#e6e6e6", bg="#333333")

gameLabel.grid(row=0, column=0, columnspan=5)

# change title


def change_title(new_text):
    gameLabel.configure(text=new_text)

    if gamehandler.MASTER_GAME_HANDLER.game_mode == 0:
        timerLabel.config(text="Timer")

    elif gamehandler.MASTER_GAME_HANDLER.game_mode == 4:
        timerLabel.config(text="Timer")


# correct / wrong answer display

answerLabel = Label(tab0, text="", font=(
    "Arial", 12), fg="#e6e6e6", bg="#333333")

answerLabel.grid(row=1, column=0, columnspan=5)

# change status based on correct / wrong answer


def change_status(status):
    if status == "correct":
        answerLabel.configure(text="CORRECT!", fg="#bbff78")

    elif status == 0:
        answerLabel.configure(text="")

    elif status == "time's up":
        correct_flag = gamehandler.MASTER_GAME_HANDLER.current_flag.upper().replace("_", " ")
        answerLabel.configure(
            text=f"TIME'S UP - CORRECT ANSWER WAS: {correct_flag}", fg="#ff7c78")

    else:
        answerLabel.configure(
            text=f"WRONG - CORRECT ANSWER: {status}", fg="#ff7c78")

# update game status


def display_round(current_round):
    roundLabel.config(text=f"Round: {current_round}")


def display_score(score: int):
    scoreLabel.config(text=f"Score: {score}")


def display_timer():
    if gamehandler.MASTER_GAME_HANDLER.game_mode == 1:
        timerLabel.config(text=timerlogic.clock.read_displayed())
        timerLabel.after(100, display_timer)

    elif gamehandler.MASTER_GAME_HANDLER.game_mode == 2:
        timer = timerlogic.clock.read_accurate()

        if timer >= 5.1:
            gamehandler.MASTER_GAME_HANDLER.player_answered(0)

        else:
            timerLabel.config(text=timerlogic.clock.read_displayed())
            timerLabel.after(100, display_timer)


def display_lives(lives):
    if lives < 0:
        livesLabel.config(text="Lives: Inf")

    else:
        livesLabel.config(text=f"Lives: {lives}")


def display_streak(streak):
    streakLabel.config(text=f"Streak: {streak}")


# 'timer', 'round', 'score' and 'lives' labels for player
roundLabel = Label(tab0, text="Round", font=(
    "Arial", 12), fg="#e6e6e6", bg="#333333")
roundLabel.grid(row=2, column=0)

scoreLabel = Label(tab0, text="Score", font=(
    "Arial", 12), fg="#e6e6e6", bg="#333333")
scoreLabel.grid(row=2, column=1)

timerLabel = Label(tab0, text="Timer", font=(
    "Arial", 12), fg="#e6e6e6", bg="#333333")
timerLabel.grid(row=2, column=2)

livesLabel = Label(tab0, text="Lives", font=(
    "Arial", 12), fg="#e6e6e6", bg="#333333")
livesLabel.grid(row=2, column=3)

streakLabel = Label(tab0, text="Streak", font=(
    "Arial", 12), fg="#e6e6e6", bg="#333333")
streakLabel.grid(row=2, column=4)

# set size for flag display
img = Image.open(flaghandler.WORKING_DIR + "/placeholder-image.png")
img.thumbnail((600, 600), Image.LANCZOS)
im = ImageTk.PhotoImage(img)
photoLabel = Label(tab0, image=im)
photoLabel.grid(row=3, column=0, columnspan=5)

# change flag


def next_flag(path: str):
    img2 = Image.open(path)
    img2.thumbnail((450, 450), Image.LANCZOS)
    im2 = ImageTk.PhotoImage(img2)
    photoLabel.configure(image=im2)
    photoLabel.image = im2

# define button functions


def button_0_function():
    gamehandler.MASTER_GAME_HANDLER.player_answered(0)


def button_1_function():
    gamehandler.MASTER_GAME_HANDLER.player_answered(1)


def button_2_function():
    gamehandler.MASTER_GAME_HANDLER.player_answered(2)


def button_3_function():
    gamehandler.MASTER_GAME_HANDLER.player_answered(3)


# generate buttons
button0 = Button(tab0, text="OPTION 1", state=DISABLED, width=34, pady=10,
                 padx=10, relief="groove", command=button_0_function)
button0.grid(row=4, column=0, columnspan=2)
button1 = Button(tab0, text="OPTION 2", state=DISABLED, width=34, pady=10,
                 padx=10, relief="groove", command=button_1_function)
button1.grid(row=4, column=3, columnspan=2)
button2 = Button(tab0, text="OPTION 3", state=DISABLED, width=34, pady=10,
                 padx=10, relief="groove", command=button_2_function)
button2.grid(row=5, column=0, columnspan=2)
button3 = Button(tab0, text="OPTION 4", state=DISABLED, width=34, pady=10,
                 padx=10, relief="groove", command=button_3_function)
button3.grid(row=5, column=3, columnspan=2)

# define button update function


def next_buttons(options: list):
    button0.configure(text=options[0], state=NORMAL)
    button1.configure(text=options[1], state=NORMAL)
    button2.configure(text=options[2], state=NORMAL)
    button3.configure(text=options[3], state=NORMAL)


# define button grey out function after game end


def inactive_buttons():
    button0.configure(text="OPTION 1", state=DISABLED)
    button1.configure(text="OPTION 2", state=DISABLED)
    button2.configure(text="OPTION 3", state=DISABLED)
    button3.configure(text="OPTION 4", state=DISABLED)


# keep window dimensions locked, disable dynamic scaling on the grid element
tab0.rowconfigure(0, weight=0, uniform='titles')
tab0.rowconfigure(1, weight=0, uniform='titles')
tab0.rowconfigure(2, weight=0, uniform='titles')
tab0.rowconfigure(3, weight=1, uniform='viewport')
tab0.rowconfigure(4, weight=0, uniform='buttons')
tab0.rowconfigure(5, weight=0, uniform='buttons')

# define the history tab, Label and Text modules used to achieve proper visibility
historyLabel = Label(tab1)
historyLabel.grid()

historyText = Text(historyLabel, state="disabled")
historyText.grid(row=0, column=0)

historyScroll = Scrollbar(historyLabel, command=historyText.yview)
historyText.config(yscrollcommand=historyScroll.set)
historyScroll.grid(row=0, column=1, sticky=NSEW)

# history view update


def history_update():
    historyText.config(state='normal')
    historyText.delete('1.0', END)
    content = history.update()

    for row in content:
        historyText.insert(END, f"{row}\n")

    historyText.config(state='disabled')


# function called to update history at launch
history_update()

# define the learn tab, Label and Text modules used to achieve proper visibility
learnRulesLabel = Label(tab2)
learnRulesLabel.grid()

learnRulesText = Text(learnRulesLabel, state="disabled")
learnRulesText.grid(row=0, column=0)

learnRulesScroll = Scrollbar(learnRulesLabel, command=learnRulesText.yview)
learnRulesText.config(yscrollcommand=learnRulesScroll.set)
learnRulesScroll.grid(row=0, column=1, sticky=NSEW)

learnRulesText.config(state='normal')
learnRulesText.delete('1.0', END)
rules_content = rules.update()

for rows in rules_content:
    learnRulesText.insert(END, f"{rows}\n")

learnRulesText.config(state='disabled')

print("GUI generated and fully operational.")
print("Game ready.")

# Tkinter mainloop
window.mainloop()
