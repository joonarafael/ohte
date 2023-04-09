import game_handler
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from PIL import Image, ImageTk
import flaghandler
import timerlogic
import history

# THIS IS THE PLACE TO CHANGE CORRECT FLAG AMOUNT !!!
CORRECT_AMOUNT = 198

# call to import flags for the first time
flaghandler.flagImport(CORRECT_AMOUNT)

# game handler called only after flags have been imported successfully

print("Necessary libraries for GUI imported, drawing interface...")

# master window settings
window = Tk()
window.title("Flag Game")
window.geometry("660x600")
window.minsize(660, 600)
window.maxsize(660, 600)

# define "are you sure" screen


def exit_game():
    ans = tkinter.messagebox.askyesno(
        "Exit?", "Are you sure you want to exit? Any unsaved progress will be lost.")

    if ans:
        game_handler.masterGameHandler.terminatedGame()
        print("Program exit...")
        window.destroy()


# create menubar
menu_bar = Menu(window)
window.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
debug_menu = Menu(menu_bar, tearoff=0)
about_menu = Menu(menu_bar, tearoff=0)
gamemode_selection = Menu(file_menu, tearoff=0)

menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="Debug", menu=debug_menu)
menu_bar.add_cascade(label="About", menu=about_menu)

# define file menu commands


def history_print():
    history.console_print()


def clear_history():
    result = tkinter.messagebox.askyesno(
        "Are you sure?", "Are You sure you wish to clear all history from file and exit program? All progress will be lost permanently.")

    if not result:
        return

    history.clear_history()


# define file menu
file_menu.add_cascade(label="New game", menu=gamemode_selection)
file_menu.add_command(label="Print history to console", command=history_print)
file_menu.add_command(label="Clear history...", command=clear_history)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_game)

# define debug menu commands


def directories():
    print("CRITICAL DIRECTORIES:")
    history.print_directories()
    print("Flag Directory:")
    print(flaghandler.flagdir)


def flag_list():
    flaghandler.listEverything()


def retry_import():
    flaghandler.flagImport(CORRECT_AMOUNT)


def toggle_status_print():
    if game_handler.masterGameHandler.devstatusprint:
        print("Dev print game status disabled.")
        game_handler.masterGameHandler.devstatusprint = False

    else:
        print("Dev print game status enabled.")
        game_handler.masterGameHandler.devstatusprint = True


def flag_slide_show():
    game_handler.masterGameHandler.flagSlideShow()


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
        "About", "Joona Kettunen, github.com/joonarafael/ohte, Flag Game v. 0.1.65, Ohjelmistotekniikka K2023")


# define about menu
about_menu.add_command(label="About...", command=show_about)

# define different game starts


def start_classic_game():
    if len(flaghandler.completeFlagList) == CORRECT_AMOUNT:
        game_handler.masterGameHandler.classic()


def start_advanced_game():
    if len(flaghandler.completeFlagList) == CORRECT_AMOUNT:
        game_handler.masterGameHandler.advanced()


def start_free_game():
    if len(flaghandler.completeFlagList) == CORRECT_AMOUNT:
        game_handler.masterGameHandler.free()


# define game mode selection menu
gamemode_selection.add_command(label="Classic", command=start_classic_game)
gamemode_selection.add_command(label="Advanced", command=start_advanced_game)
gamemode_selection.add_command(label="Time Trial", command=None)
gamemode_selection.add_command(label="One Life", command=None)
gamemode_selection.add_command(label="Free Mode", command=start_free_game)

# define 'tab' system
notebook = ttk.Notebook(window)
tab0 = Frame(notebook, bg="#333333")
tab1 = Frame(notebook, bg="#cbe0c3")
tab2 = Frame(notebook, bg="#cce0f2")

notebook.add(tab0, text="Game")
notebook.add(tab1, text="History")
notebook.add(tab2, text="Learn")
notebook.pack(expand=True, fill="both")

# main title
if len(flaghandler.completeFlagList) != CORRECT_AMOUNT:
    gameLabel = Label(tab0, text="FLAG IMAGES IMPORT ERROR, SEE CONSOLE FOR DETAILS", font=(
        "Arial", 12), fg="#e6e6e6", bg="#333333")

else:
    gameLabel = Label(tab0, text="Flag Game", font=(
        "Arial", 14), fg="#e6e6e6", bg="#333333")

gameLabel.grid(row=0, column=0, columnspan=5)

# change title


def change_title(newtext):
    gameLabel.configure(text=newtext)

    if game_handler.masterGameHandler.gamemode == 0:
        timerLabel.config(text="Timer")

    elif game_handler.masterGameHandler.gamemode == 4:
        timerLabel.config(text="Timer")

# update game status


def display_round(round):
    roundLabel.config(text=f"Round: {round}")


def display_score(score):
    scoreLabel.config(text=f"Score: {score}")


def displayTimer():
    if game_handler.masterGameHandler.gamemode == 1:
        timerLabel.config(text=timerlogic.clock.readDisplayed())
        timerLabel.after(100, displayTimer)


def displayLives(lives):
    if lives < 0:
        livesLabel.config(text=f"Lives: Inf")

    else:
        livesLabel.config(text=f"Lives: {lives}")


def displayStreak(streak):
    streakLabel.config(text=f"Streak: {streak}")


# 'timer', 'round', 'score' and 'lives' labels for player
roundLabel = Label(tab0, text="Round", font=(
    "Arial", 12), fg="#e6e6e6", bg="#333333")
roundLabel.grid(row=1, column=0)

scoreLabel = Label(tab0, text="Score", font=(
    "Arial", 12), fg="#e6e6e6", bg="#333333")
scoreLabel.grid(row=1, column=1)

timerLabel = Label(tab0, text="Timer", font=(
    "Arial", 12), fg="#e6e6e6", bg="#333333")
timerLabel.grid(row=1, column=2)

livesLabel = Label(tab0, text="Lives", font=(
    "Arial", 12), fg="#e6e6e6", bg="#333333")
livesLabel.grid(row=1, column=3)

streakLabel = Label(tab0, text="Streak", font=(
    "Arial", 12), fg="#e6e6e6", bg="#333333")
streakLabel.grid(row=1, column=4)

# set size for flag display
img = Image.open(flaghandler.workingdir + "/placeholder-image.png")
img.thumbnail((600, 600), Image.LANCZOS)
im = ImageTk.PhotoImage(img)
photoLabel = Label(tab0, image=im)
photoLabel.grid(row=2, column=0, columnspan=5)

# change flag


def nextflag(path: str):
    img2 = Image.open(path)
    img2.thumbnail((450, 450), Image.LANCZOS)
    im2 = ImageTk.PhotoImage(img2)
    photoLabel.configure(image=im2)
    photoLabel.image = im2

# define button functions


def button0Function():
    game_handler.masterGameHandler.playerAnswered(0)


def button1Function():
    game_handler.masterGameHandler.playerAnswered(1)


def button2Function():
    game_handler.masterGameHandler.playerAnswered(2)


def button3Function():
    game_handler.masterGameHandler.playerAnswered(3)


# generate buttons
button0 = Button(tab0, text="OPTION 1", width=34, pady=10,
                 padx=10, relief="groove", command=button0Function)
button0.grid(row=3, column=0, columnspan=2)
button1 = Button(tab0, text="OPTION 2", width=34, pady=10,
                 padx=10, relief="groove", command=button1Function)
button1.grid(row=3, column=3, columnspan=2)
button2 = Button(tab0, text="OPTION 3", width=34, pady=10,
                 padx=10, relief="groove", command=button2Function)
button2.grid(row=4, column=0, columnspan=2)
button3 = Button(tab0, text="OPTION 4", width=34, pady=10,
                 padx=10, relief="groove", command=button3Function)
button3.grid(row=4, column=3, columnspan=2)

# def button update function


def nextbuttons(options: list):
    button0.configure(text=options[0])
    button1.configure(text=options[1])
    button2.configure(text=options[2])
    button3.configure(text=options[3])


# keep window dimensions locked, disable dynamic scaling on the grid element
tab0.rowconfigure(0, weight=0, uniform='titles')
tab0.rowconfigure(1, weight=0, uniform='titles')
tab0.rowconfigure(2, weight=1, uniform='viewport')
tab0.rowconfigure(3, weight=0, uniform='buttons')
tab0.rowconfigure(4, weight=0, uniform='buttons')

# define the history tab, Label and Text modules used to achieve proper visibility
historyLabel = Label(tab1)
historyLabel.grid()

historyText = Text(historyLabel, state="disabled")
historyText.grid(row=0, column=0)

historyScroll = Scrollbar(historyLabel, command=historyText.yview)
historyText.config(yscrollcommand=historyScroll.set)
historyScroll.grid(row=0, column=1, sticky=NSEW)

# history view update


def historyUpdate():
    historyText.config(state='normal')
    historyText.delete('1.0', END)
    content = history.update()

    for x in content:
        historyText.insert(END, f"{x}\n")

    historyText.config(state='disabled')


# function called to update history at launch
historyUpdate()

print("GUI generated and fully operational.")

# Tkinter mainloop
window.mainloop()
