# MODULE DESCRIPTION

# gui is responsible for the game graphical user interface

# FOR PRACTICAL REASONS AND OWN MENTAL WELL-BEING I WANT TO IMPORT
# ALL TKINTER LIBRARIES, PYLINT DISABLE ADDED TO IGNORRE THESE !!!

from tkinter import *          # pylint: disable=wildcard-import disable=unused-wildcard-import
from tkinter import ttk        # pylint: disable=unused-import
import tkinter.messagebox      # pop-up screen to ask 'are you sure?'
from PIL import Image, ImageTk  # handle flag images
import flaghandler             # fetch flag data from flaghandler
import timerlogic              # utilize master time class for timer display
import history                 # ask for updated history information after games
import rules                   # ask for game rule book
import csvhandler              # ask for updated game statistics
# dodge circular-import error
from circularimport import send_terminated_game, send_flag_slide_show
from circularimport import send_input, send_reset                     # ...
from circularimport import read_current_game_mode, send_launch        # ...

print("Necessary libraries for GUI imported, drawing interface...")

# UPDATE GAME VERSION HERE
CURRENT_VERSION = "0.2.3"

# select most optimal resolution and lock it
LAUNCH_RESOLUTION = (663, 700)
RESOLUTION_LOCKED = True
IGNORE_FREE_MODE_GAMES = False

# master window settings
window = Tk()
window.title("Flag Quiz Game")
window.geometry(f"{LAUNCH_RESOLUTION[0]}x{LAUNCH_RESOLUTION[1]}")
window.minsize(LAUNCH_RESOLUTION[0], LAUNCH_RESOLUTION[1])
window.maxsize(LAUNCH_RESOLUTION[0], LAUNCH_RESOLUTION[1])

# create menu bar
menu_bar = Menu(window)
window.config(menu=menu_bar)

# add file, debug & about menus
file_menu = Menu(menu_bar, tearoff=0)
stats_menu = Menu(menu_bar, tearoff=0)
debug_menu = Menu(menu_bar, tearoff=0)
about_menu = Menu(menu_bar, tearoff=0)
game_mode_selection = Menu(file_menu, tearoff=0)
clear_memory = Menu(file_menu, tearoff=0)
print_selection = Menu(debug_menu, tearoff=0)

menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="Stats", menu=stats_menu)
menu_bar.add_cascade(label="Debug", menu=debug_menu)
menu_bar.add_cascade(label="About", menu=about_menu)

# define file menu commands


def reset_gamehandler():
    send_reset()


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


def clear_history():
    result = tkinter.messagebox.askyesno(
        "Sure?", ("Are You sure You wish to clear all history from file and exit program?"
                  " Statistics are saved, recorded history will be lost."))

    if not result:
        return

    history.clear_history(False)


def clear_stats():
    result = tkinter.messagebox.askyesno(
        "Sure?", ("Are You sure You wish to clear all history"
                  " and recorded statistics from file and exit program?"
                  " All progress will be permanently lost."))

    if not result:
        return

    history.clear_history(True)


def flag_slide_show():
    if len(flaghandler.COMPLETE_FLAG_LIST) == flaghandler.CORRECT_AMOUNT:
        send_flag_slide_show(0)


def exit_game():
    ans = tkinter.messagebox.askyesno(
        "Exit?", ("Are You sure You want to exit?"
                  " Any ongoing game will be terminated."))

    if ans:
        send_terminated_game()
        print("Program exit...")
        window.destroy()


# define file menu
file_menu.add_cascade(label="New game...", menu=game_mode_selection)
file_menu.add_command(label="Cancel game", command=reset_gamehandler)
file_menu.add_command(label="Lock / Unlock resolution",
                      command=unlock_resolution)
file_menu.add_command(label="Free flag browsing", command=flag_slide_show)
file_menu.add_cascade(label="Clear history...", menu=clear_memory)
file_menu.add_command(label="Exit", command=exit_game)

clear_memory.add_command(label="Clear history only", command=clear_history)
clear_memory.add_command(label="Clear history & stats", command=clear_stats)

# define different game starts


def start_classic_game():
    send_launch(0)


def start_advanced_game():
    send_launch(1)


def start_time_game():
    send_launch(2)


def start_one_life_game():
    send_launch(3)


def start_free_game():
    send_launch(4)


# define game mode selection drop down menu
game_mode_selection.add_command(label="Classic", command=start_classic_game)
game_mode_selection.add_command(label="Advanced", command=start_advanced_game)
game_mode_selection.add_command(label="Time Trial", command=start_time_game)
game_mode_selection.add_command(label="One Life", command=start_one_life_game)
game_mode_selection.add_command(label="Free Mode", command=start_free_game)

# define debug menu commands


def directories():
    print()
    print("CRITICAL DIRECTORIES:")
    history.print_directories()
    print("Flag directory:")
    print(flaghandler.FLAG_DIR + "/")
    print("Rulebook directory:")
    print(rules.GAME_RULES_PATH)
    print("Statistics files paths:")
    print(csvhandler.ROUNDS_PATH)
    print(csvhandler.STREAKS_PATH)
    print(csvhandler.STATS_PATH)


def flag_list():
    flaghandler.list_every_flag()


def retry_import():
    flaghandler.flag_import(flaghandler.CORRECT_AMOUNT)


def history_print():
    history.console_print()


def rounds_print():
    csvhandler.MASTER_RUNNING_GAME.print_round_file()


def streaks_print():
    csvhandler.MASTER_RUNNING_GAME.print_streak_file()


def games_print():
    csvhandler.MASTER_RUNNING_GAME.print_stats_file()


def stats_print():
    content = csvhandler.MASTER_RUNNING_GAME.calculate_true_stats(
        IGNORE_FREE_MODE_GAMES)

    print()
    print("Statistics recorded:")

    for key, value in content.items():
        print(f"{key:<30} : {value}")


# define debug menu
debug_menu.add_cascade(label="Print to console...", menu=print_selection)
debug_menu.add_command(label="Retry flag import", command=retry_import)

print_selection.add_command(
    label="Recorded history", command=history_print)
print_selection.add_command(
    label="Recorded rounds", command=rounds_print)
print_selection.add_command(
    label="Recorded streaks", command=streaks_print)
print_selection.add_command(
    label="Recorded games", command=games_print)
print_selection.add_command(
    label="Recorded stats", command=stats_print)
print_selection.add_command(
    label="Critical directory paths", command=directories)
print_selection.add_command(label="Flag source files", command=flag_list)


# define about pop-up screen


def show_about():
    tkinter.messagebox.showinfo(
        "About", ("Joona Kettunen"
                  " github.com/joonarafael/ohte"
                  f" Flag Quiz Game v. {CURRENT_VERSION}"
                  " Ohjelmistotekniikka K2023"))


# define about menu
about_menu.add_command(label="Show about", command=show_about)


# define stats commands
def ignore_free_games():
    global IGNORE_FREE_MODE_GAMES

    if IGNORE_FREE_MODE_GAMES:
        IGNORE_FREE_MODE_GAMES = False

    else:
        IGNORE_FREE_MODE_GAMES = True

    stats_update()


# define stats menu
stats_menu.add_command(
    label="Ignore / Include Free Mode Games", command=ignore_free_games)

# define 'tab' system within the master window
notebook = ttk.Notebook(window)
tab0 = Frame(notebook, bg="#333333", relief="flat",
             borderwidth=0, highlightthickness=0)
tab1 = Frame(notebook, bg="#333333", relief="flat",
             borderwidth=0, highlightthickness=0)
tab2 = Frame(notebook, bg="#333333", relief="flat",
             borderwidth=0, highlightthickness=0)
tab3 = Frame(notebook, bg="#333333", relief="flat",
             borderwidth=0, highlightthickness=0)

notebook.add(tab0, text="Game")
notebook.add(tab1, text="Stats")
notebook.add(tab2, text="History")
notebook.add(tab3, text="Rules")
notebook.pack(expand=True, fill="both")

# adjust & configure the visual layout of the game tab
# keep window dimensions locked, disable dynamic scaling on the grid element
tab0.rowconfigure(0, weight=0, uniform='titles')
tab0.rowconfigure(1, weight=0, uniform='titles')
tab0.rowconfigure(2, weight=0, uniform='titles')
tab0.rowconfigure(3, weight=1, uniform='viewport')
tab0.rowconfigure(4, weight=0, uniform='buttons')
tab0.rowconfigure(5, weight=0, uniform='buttons')

# define the main title for the game tab
game_label = Label(tab0, text="FLAG QUIZ GAME", font=(
    "Arial", 14, 'bold'), fg="#e6e6e6", bg="#333333")
game_label.grid(row=0, column=0, columnspan=5)

# function to change title to any new text


def change_title(new_text, new_color):
    game_label.configure(text=new_text, fg=new_color)


# correct / wrong answer display underneath main title
answer_label = Label(tab0, text="Start a new game from File > New Game.", font=(
    "Arial", 12), fg="#e6e6e6", bg="#333333")
answer_label.grid(row=1, column=0, columnspan=5)

# function to change status based on correct / wrong answer


def change_status(new_text, new_color):
    answer_label.configure(text=new_text, fg=new_color)

# functions to update game statistics for player
# including round, score, timer, lives & streak


def display_round(current_round):
    round_label.config(text=f"Round: {current_round}")


def display_score(score: int):
    score_label.config(text=f"Score: {score}")


def display_timer():
    game_mode = read_current_game_mode()
    displayed_time = round(timerlogic.clock.read_displayed(), 1)

    # timer counts UP for advanced game
    if game_mode == 1:
        timer_label.config(
            text=f"{displayed_time:>7}", fg="#e6e6e6")
        # function calls itself again after 100 ms
        timer_label.after(100, display_timer)

    # timer counts DOWN for time trial
    elif game_mode == 2:
        # if more than 5 seconds has elapsed, dummy answer is forced
        # to end the game
        if timerlogic.clock.read_accurate() >= 5.001:
            send_input(0)

        else:
            displayed_time = round(5.0 - displayed_time, 1)
            displayed_time = max(displayed_time, 0.0)

            if displayed_time <= 1.5:
                timer_label.config(text=f"{displayed_time:>7}", fg="#ff6e6e")

            else:
                timer_label.config(text=f"{displayed_time:>7}", fg="#e6e6e6")

            # function calls itself again after 100 ms
            timer_label.after(100, display_timer)

    # function is also called to change the displayed text back to "Timer"
    # for other game modes
    else:
        timer_label.config(text="Timer", fg="#e6e6e6")


def display_lives(lives, color):
    lives_label.config(text=f"Lives: {lives}", fg=color)


def display_streak(streak):
    streak_label.config(text=f"Streak: {streak}")


# define 'timer', 'round', 'score' and 'lives' labels for player
round_label = Label(tab0, text="Round", font=(
    "Arial", 12), fg="#e6e6e6", bg="#333333")
round_label.grid(row=2, column=0)

score_label = Label(tab0, text="Score", font=(
    "Arial", 12), fg="#e6e6e6", bg="#333333")
score_label.grid(row=2, column=1)

timer_label = Label(tab0, text="Timer", font=(
    "Arial", 12), fg="#e6e6e6", bg="#333333")
timer_label.grid(row=2, column=2)

lives_label = Label(tab0, text="Lives", font=(
    "Arial", 12), fg="#e6e6e6", bg="#333333")
lives_label.grid(row=2, column=3)

streak_label = Label(tab0, text="Streak", font=(
    "Arial", 12), fg="#e6e6e6", bg="#333333")
streak_label.grid(row=2, column=4)

# set size for flag viewport
img = Image.open(flaghandler.WORKING_DIR + "/placeholder-image.png")
img.thumbnail((500, 500), Image.LANCZOS)
im = ImageTk.PhotoImage(img)
photo_label = Label(tab0, image=im, borderwidth=0,
                    highlightthickness=0, relief="flat")
photo_label.grid(row=3, column=0, columnspan=5)

# define a function to change flag


def next_flag(path: str):
    img2 = Image.open(path)
    img2.thumbnail((450, 450), Image.LANCZOS)
    im2 = ImageTk.PhotoImage(img2)
    photo_label.configure(image=im2)
    photo_label.image = im2

# define button functions


def button_0_function():
    send_input(0)


def button_1_function():
    send_input(1)


def button_2_function():
    send_input(2)


def button_3_function():
    send_input(3)


# define the buttons
button0 = Button(tab0, text="OPTION 1", state=DISABLED, width=36, pady=10,
                 padx=10, relief="groove", borderwidth=0, highlightthickness=0,
                 command=button_0_function)
button0.grid(row=4, column=0, columnspan=2)
button1 = Button(tab0, text="OPTION 2", state=DISABLED, width=36, pady=10,
                 padx=10, relief="groove", borderwidth=0, highlightthickness=0,
                 command=button_1_function)
button1.grid(row=4, column=3, columnspan=2)
button2 = Button(tab0, text="OPTION 3", state=DISABLED, width=36, pady=10,
                 padx=10, relief="groove", borderwidth=0, highlightthickness=0,
                 command=button_2_function)
button2.grid(row=5, column=0, columnspan=2)
button3 = Button(tab0, text="OPTION 4", state=DISABLED, width=36, pady=10,
                 padx=10, relief="groove", borderwidth=0, highlightthickness=0,
                 command=button_3_function)
button3.grid(row=5, column=3, columnspan=2)

# define a function to update buttons every round


def next_buttons(options: list):
    button0.configure(text=options[0], state=NORMAL)
    button1.configure(text=options[1], state=NORMAL)
    button2.configure(text=options[2], state=NORMAL)
    button3.configure(text=options[3], state=NORMAL)


# define a function to grey out and disable the buttons after game termination


def inactive_buttons():
    button0.configure(text="OPTION 1", state=DISABLED)
    button1.configure(text="OPTION 2", state=DISABLED)
    button2.configure(text="OPTION 3", state=DISABLED)
    button3.configure(text="OPTION 4", state=DISABLED)


# define the stats tab
# Label and Text modules used to achieve proper visibility
stats_label = Label(tab1, relief="flat", borderwidth=0, highlightthickness=0)
stats_label.grid(sticky="NSEW")
stats_label.grid_rowconfigure(0, weight=1)

# text element is used to display the actual content
stats_text = Text(stats_label, state="disabled", fg="#e6e6e6", bg="#333333",
                  relief="flat", borderwidth=0, highlightthickness=0)
stats_text.grid(row=0, column=1, sticky="NSEW")

# fill the entire available vertical space
tab1.columnconfigure(1, weight=1)
tab1.columnconfigure(0, minsize=20)
tab1.rowconfigure(0, weight=1)

# function to update stats after every finished game


def stats_update():
    stats_text.config(state='normal')
    stats_text.delete('1.0', END)
    content = csvhandler.MASTER_RUNNING_GAME.calculate_true_stats(
        IGNORE_FREE_MODE_GAMES)

    if IGNORE_FREE_MODE_GAMES:
        stats_text.insert(END, "STATISTICS IGNORING FREE MODE GAMES\n\n")

    else:
        stats_text.insert(END, "PLAYER LIFELONG STATISTICS\n\n")

    text_line = []

    for key, value in content.items():
        text_line.append((key.replace("_", " "), value))

    r_i = 0

    # properly justify the content in to columns
    while True:
        if r_i <= len(text_line) - 2:
            gui_row = (f"{text_line[r_i][0]:<30}{text_line[r_i][1]:<8}"
                       f" | {text_line[r_i + 1][0]:<30}{text_line[r_i + 1][1]:<8}\n\n")

        elif r_i == len(text_line) - 1:
            gui_row = f"{text_line[r_i][0]:<30}{text_line[r_i][1]:<8}"

        else:
            break

        stats_text.insert(END, gui_row)
        r_i += 2

    stats_text.config(state='disabled')


# call function immediately at launch
stats_update()

# define the history tab
# Label and Text modules used to achieve proper visibility
history_label = Label(tab2, relief="flat", borderwidth=0, highlightthickness=0)
history_label.grid(sticky="NSEW")
history_label.grid_rowconfigure(0, weight=1)

# text element is used to display the actual content
history_text = Text(history_label, state="disabled", fg="#e6e6e6", bg="#333333",
                    relief="flat", borderwidth=0, highlightthickness=0)
history_text.grid(row=0, column=1, sticky="NSEW")

# scrollbar added to navigate the page
history_scroll = Scrollbar(history_label, command=history_text.yview)
history_text.config(yscrollcommand=history_scroll.set)
history_scroll.grid(row=0, column=0, sticky="ns")

# fill the entire available vertical space
tab2.columnconfigure(1, weight=1)
tab2.columnconfigure(0, minsize=20)
tab2.rowconfigure(0, weight=1)

# define a function to update the history


def history_update():
    history_text.config(state='normal')
    history_text.delete('1.0', END)
    content = history.update()

    for row in content:
        history_text.insert(END, f"{row}\n")

    history_text.config(state='disabled')


# function called immediately to update history at launch
history_update()

# define the learn tab
# Label and Text modules used to achieve proper visibility

# rules_label contains all content within the tab
rules_label = Label(tab3, relief="flat", borderwidth=0, highlightthickness=0)
rules_label.grid(sticky="NSEW")
rules_label.grid_rowconfigure(0, weight=1)

# text element is used to display the actual content
rules_text = Text(rules_label, state="disabled", fg="#e6e6e6", bg="#333333",
                  relief="flat", borderwidth=0, highlightthickness=0)
rules_text.grid(row=0, column=1, sticky="NSEW")

# scrollbar added to navigate the page
rules_scroll = Scrollbar(rules_label, command=rules_text.yview)
rules_text.config(yscrollcommand=rules_scroll.set)
rules_scroll.grid(row=0, column=0, sticky="ns")

# fill the entire available vertical space
tab3.columnconfigure(1, weight=1)
tab3.columnconfigure(0, minsize=20)
tab3.rowconfigure(0, weight=1)

# rules won't change
# they're written out once at launch
rules_text.config(state='normal')
rules_text.delete('1.0', END)
rules_content = rules.update()

if rules_content is not None:
    for rows in rules_content:
        rules_text.insert(END, f"{rows}\n")

else:
    rules_text.insert(END, "RULEBOOK IMPORT ERROR")

rules_text.config(state='disabled')

# inform finally to console these approx. 600 lines have been executed successfully
print("GUI generated and fully operational.")
print("Game ready.")

# set protocol for sudden user quit event
window.protocol("WM_DELETE_WINDOW", exit_game)

# Tkinter mainloop
window.mainloop()
