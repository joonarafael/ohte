from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from PIL import Image, ImageTk
import game_handler
import flaghandler
import timerlogic

game_handler

print("Necessary libraries for GUI imported, drawing interface...")

#master window settings
window = Tk()
window.title("Flag Game")
window.geometry("500x600")

#define "are you sure" screen
def exit_game():
    ans = tkinter.messagebox.askyesno("Exit?", "Are you sure you want to exit? Any unsaved progress will be lost.")

    if ans:
        window.destroy()

#create menubar
menu_bar = Menu(window)
window.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
debug_menu = Menu(menu_bar, tearoff=0)
about_menu = Menu(menu_bar, tearoff=0)
gamemode_selection = Menu(file_menu, tearoff=0)

menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="Debug", menu=debug_menu)
menu_bar.add_cascade(label="About", menu=about_menu)

file_menu.add_cascade(label="New game", menu=gamemode_selection)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_game)

#define debug options
def flagList():
    flaghandler.listEverything()

debug_menu.add_command(label="List flag source files to console", command=flagList)

#define 'about' message
def onClick():
    tkinter.messagebox.showinfo("About", "Joona Kettunen, github.com/joonarafael/ohte, Flag Game v. 0.1.3, Ohjelmistotekniikka K2023")

about_menu.add_command(label="About...", command=onClick)

#define game starts
def start_classic_game():
    if len(flaghandler.completeFlagList) == 200:
        game_handler.masterGameHandler.classic()

def start_advanced_game():
    if len(flaghandler.completeFlagList) == 200:
        game_handler.masterGameHandler.advanced()

gamemode_selection.add_command(label="Classic", command=start_classic_game)
gamemode_selection.add_command(label="Advanced", command=start_advanced_game)
gamemode_selection.add_command(label="Time Trial", command=None)
gamemode_selection.add_command(label="One Life", command=None)
gamemode_selection.add_command(label="Free Mode", command=None)

#define 'tab' system
notebook = ttk.Notebook(window)
tab0 = Frame(notebook, background="#c3e0dd")
tab1 = Frame(notebook, background="#cbe0c3")
tab2 = Frame(notebook, background="#cce0f2")

notebook.add(tab0, text="Game")
notebook.add(tab1, text="History")
notebook.add(tab2, text="Learn")
notebook.pack(expand=True, fill="both")

#main title
if len(flaghandler.completeFlagList) != 200:
    gameLabel = Label(tab0, text="FLAG IMAGES IMPORT ERROR, SEE CONSOLE FOR DETAILS", font=("Arial", 12), background="#c3e0dd")

else:
    gameLabel = Label(tab0, text="Flag Game", font=("Arial", 12), background="#c3e0dd")

gameLabel.grid(row=0, column=0, columnspan=5)

#change title
def changeTitle(newtext):
    gameLabel.configure(text=newtext)

#subtitles config
def timer():
    timerLabel.config(text=timerlogic.clock.readDisplayed())

    if game_handler.masterGameHandler.gamemode != -1:
        timerLabel.after(100, timer)

def displayRound(round):
    roundLabel.config(text=f"Round: {round}")

def displayScore(score):
    scoreLabel.config(text=f"Score: {score}")

def displayLives(lives):
    livesLabel.config(text=f"Lives: {lives}")

def displayStreak(streak):
    streakLabel.config(text=f"Streak: {streak}")

#timer, round, score, lives
roundLabel = Label(tab0, text="Round", font=("Arial", 12), background="#c3e0dd")
roundLabel.grid(row=1, column=0)

scoreLabel = Label(tab0, text="Score", font=("Arial", 12), background="#c3e0dd")
scoreLabel.grid(row=1, column=1)

timerLabel = Label(tab0, text="Timer", font=("Arial", 12), background="#c3e0dd")
timerLabel.grid(row=1, column=2)

livesLabel = Label(tab0, text="Lives", font=("Arial", 12), background="#c3e0dd")
livesLabel.grid(row=1, column=3)

streakLabel = Label(tab0, text="Streak", font=("Arial", 12), background="#c3e0dd")
streakLabel.grid(row=1, column=4)

#image (flags) processing, resizing and general handling
img = Image.open(flaghandler.workingdir + "/placeholder-image.png")
img.thumbnail((500, 500), Image.ANTIALIAS)
im = ImageTk.PhotoImage(img)
photoLabel = Label(tab0, image=im)
photoLabel.grid(row=2, column=0, columnspan=5)

#change flag
def nextflag(path: str):
    img2 = Image.open(path)
    img2.thumbnail((500, 500), Image.ANTIALIAS)
    im2 = ImageTk.PhotoImage(img2)
    photoLabel.configure(image=im2)
    photoLabel.image = im2

#define button functions
def button0Function():
    game_handler.masterGameHandler.playerAnswered(0)

def button1Function():
    game_handler.masterGameHandler.playerAnswered(1)

def button2Function():
    game_handler.masterGameHandler.playerAnswered(2)

def button3Function():
    game_handler.masterGameHandler.playerAnswered(3)

#generate buttons
button0 = Button(tab0, text="OPTION 1", command=button0Function)
button0.grid(row=3, column=0, columnspan=2)
button1 = Button(tab0, text="OPTION 2", command=button1Function)
button1.grid(row=3, column=3, columnspan=2)
button2 = Button(tab0, text="OPTION 3", command=button2Function)
button2.grid(row=4, column=0, columnspan=2)
button3 = Button(tab0, text="OPTION 4", command=button3Function)
button3.grid(row=4, column=3, columnspan=2)

#update buttons
def nextbuttons(options: list):
    button0.configure(text=options[0])
    button1.configure(text=options[1])
    button2.configure(text=options[2])
    button3.configure(text=options[3])

print("GUI generated and fully operational.")
print()

#Tkinter mainloop
window.mainloop()