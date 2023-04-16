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

CURRENT_VERSION = "0.2.0"

LAUNCH_RESOLUTION = (663, 700)
RESOLUTION_LOCKED = True

# master window settings
window = Tk()
window.title("Flag Game")
window.geometry(f"{LAUNCH_RESOLUTION[0]}x{LAUNCH_RESOLUTION[1]}")
window.minsize(LAUNCH_RESOLUTION[0], LAUNCH_RESOLUTION[1])
window.maxsize(LAUNCH_RESOLUTION[0], LAUNCH_RESOLUTION[1])

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


def unlock_resolution():
    global RESOLUTION_LOCKED

    if RESOLUTION_LOCKED:
        RESOLUTION_LOCKED = False
        print("Window resolution unlocked.")

        window.minsize(0, 0)
        window.maxsize(0, 0)

        return

    lock_height = window.winfo_height()
    lock_width = window.winfo_width()

    print(f"Window resolution locked to {lock_width}x{lock_height}.")

    window.minsize(lock_width, lock_height)
    window.maxsize(lock_width, lock_height)

    RESOLUTION_LOCKED = True


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
file_menu.add_command(label="Lock / Unlock resolution",
                      command=unlock_resolution)
file_menu.add_command(label="Print history to console", command=history_print)
file_menu.add_separator()
file_menu.add_command(label="Clear history...", command=clear_history)
file_menu.add_command(label="Exit", command=exit_game)

# define debug menu commands


def directories():
    print("CRITICAL DIRECTORIES:")
    history.print_directories()
    print("Rulebook Directory:")
    print(rules.GAME_RULES_PATH)
    print("Flag Directory:")
    print(flaghandler.FLAG_DIR)


def flag_list():
    flaghandler.list_every_flag()


def retry_import():
    flaghandler.flag_import(flaghandler.CORRECT_AMOUNT)


def flag_slide_show():
    if len(flaghandler.COMPLETE_FLAG_LIST) == flaghandler.CORRECT_AMOUNT:
        gamehandler.MASTER_GAME_HANDLER.flag_slide_show(1)


# define debug menu
debug_menu.add_command(
    label="List critical directory paths to console", command=directories)
debug_menu.add_command(
    label="List flag source files to console", command=flag_list)
debug_menu.add_command(label="Retry flag import...", command=retry_import)
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
tab0 = Frame(notebook, bg="#333333", relief="flat",
             borderwidth=0, highlightthickness=0)
tab1 = Frame(notebook, bg="#333333", relief="flat",
             borderwidth=0, highlightthickness=0)
tab2 = Frame(notebook, bg="#333333", relief="flat",
             borderwidth=0, highlightthickness=0)

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


# correct / wrong answer display

answerLabel = Label(tab0, text="Start a new game from File > New Game.", font=(
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


# update game statistics for player


def display_round(current_round):
    roundLabel.config(text=f"Round: {current_round}")


def display_score(score: int):
    scoreLabel.config(text=f"Score: {score}")


def display_timer():
    # timer counts up for advanced game
    if gamehandler.MASTER_GAME_HANDLER.game_mode == 1:
        timerLabel.config(text=timerlogic.clock.read_displayed())
        timerLabel.after(100, display_timer)

    # timer counts down for time trial
    elif gamehandler.MASTER_GAME_HANDLER.game_mode == 2:
        timer = timerlogic.clock.read_accurate()

        # if more than 5 seconds has elapsed, dummy answer is forced
        if timer >= 5.001:
            gamehandler.MASTER_GAME_HANDLER.player_answered(0)

        else:
            displayed_time = round(5.0 - timerlogic.clock.read_displayed(), 1)
            displayed_time = max(displayed_time, 0.0)

            timerLabel.config(text=displayed_time)
            timerLabel.after(100, display_timer)

    else:
        timerLabel.config(text="Timer")


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
photoLabel = Label(tab0, image=im, borderwidth=0,
                   highlightthickness=0, relief="flat")
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
                 padx=10, relief="groove", borderwidth=0, highlightthickness=0,
                 command=button_0_function)
button0.grid(row=4, column=0, columnspan=2)
button1 = Button(tab0, text="OPTION 2", state=DISABLED, width=34, pady=10,
                 padx=10, relief="groove", borderwidth=0, highlightthickness=0,
                 command=button_1_function)
button1.grid(row=4, column=3, columnspan=2)
button2 = Button(tab0, text="OPTION 3", state=DISABLED, width=34, pady=10,
                 padx=10, relief="groove", borderwidth=0, highlightthickness=0,
                 command=button_2_function)
button2.grid(row=5, column=0, columnspan=2)
button3 = Button(tab0, text="OPTION 4", state=DISABLED, width=34, pady=10,
                 padx=10, relief="groove", borderwidth=0, highlightthickness=0,
                 command=button_3_function)
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


# define the history tab
# Label and Text modules used to achieve proper visibility


history_label = Label(tab1, relief="flat", borderwidth=0, highlightthickness=0)
history_label.grid(sticky="NSEW")
history_label.grid_rowconfigure(0, weight=1)

history_text = Text(history_label, state="disabled", fg="#ffffff", bg="#333333",
                    relief="flat", borderwidth=0, highlightthickness=0)
history_text.grid(row=0, column=1, sticky="NSEW")

history_scroll = Scrollbar(history_label, command=history_text.yview)
history_text.config(yscrollcommand=history_scroll.set)
history_scroll.grid(row=0, column=0, sticky="ns")

# fill entire available vertical space
tab1.columnconfigure(1, weight=1)
tab1.columnconfigure(0, minsize=20)
tab1.rowconfigure(0, weight=1)

# history view update


def history_update():
    history_text.config(state='normal')
    history_text.delete('1.0', END)
    content = history.update()

    for row in content:
        history_text.insert(END, f"{row}\n")

    history_text.config(state='disabled')


# function called to update history at launch
history_update()

# define the learn tab
# Label and Text modules used to achieve proper visibility

rules_label = Label(tab2, relief="flat", borderwidth=0, highlightthickness=0)
rules_label.grid(sticky="NSEW")
rules_label.grid_rowconfigure(0, weight=1)

rules_text = Text(rules_label, state="disabled", fg="#ffffff", bg="#333333",
                  relief="flat", borderwidth=0, highlightthickness=0)
rules_text.grid(row=0, column=1, sticky="NSEW")

rules_scroll = Scrollbar(rules_label, command=rules_text.yview)
rules_text.config(yscrollcommand=rules_scroll.set)
rules_scroll.grid(row=0, column=0, sticky="ns")

# fill entire available vertical space
tab2.columnconfigure(1, weight=1)
tab2.columnconfigure(0, minsize=20)
tab2.rowconfigure(0, weight=1)

rules_text.config(state='normal')
rules_text.delete('1.0', END)
rules_content = rules.update()

if rules_content is not None:
    for rows in rules_content:
        rules_text.insert(END, f"{rows}\n")

else:
    rules_text.insert(END, "RULEBOOK IMPORT ERROR")

rules_text.config(state='disabled')

print("GUI generated and fully operational.")
print("Game ready.")

# Tkinter mainloop
window.mainloop()
