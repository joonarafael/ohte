from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from PIL import Image, ImageTk

import gamemode_classic

print("Necessary libraries for GUI imported, drawing interface...")

window = Tk()
window.title("Flag Game")
window.geometry("525x600")

menu_bar = Menu(window)
window.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
about_menu = Menu(menu_bar, tearoff=0)
gamemode_selection = Menu(file_menu, tearoff=0)

menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="About", menu=about_menu)

file_menu.add_cascade(label="New game", menu=gamemode_selection)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=quit)

def onClick():
    tkinter.messagebox.showinfo("About", "Joona Kettunen, github.com/joonarafael/ohte, Flag Game v. 0.1.1, Ohjelmistotekniikka K2023")

about_menu.add_command(label="About...", command=onClick)

def start_classic_game():
    gamemode_classic.new_game()
    print("the fuck")

gamemode_selection.add_command(label="Classic", command=start_classic_game)
gamemode_selection.add_command(label="Advanced", command=None)
gamemode_selection.add_command(label="Time Trial", command=None)
gamemode_selection.add_command(label="One Life", command=None)
gamemode_selection.add_command(label="Free Mode", command=None)

notebook = ttk.Notebook(window)
tab0 = Frame(notebook, background="#c3e0dd")
tab1 = Frame(notebook, background="#cbe0c3")

notebook.add(tab0, text="Game")
notebook.add(tab1, text="History")
notebook.pack(expand=True, fill="both")

gameLabel = Label(tab0, text="Flag Game", font=("Arial", 12), background="#c3e0dd").grid(row=0, column=0, columnspan=2)

photoPath = "placeholder-image.png"
img = Image.open(photoPath)
img.thumbnail((500, 500), Image.ANTIALIAS)
im = ImageTk.PhotoImage(img)
photoLabel = Label(tab0, image=im).grid(row=1, column=0, columnspan=2)

button0 = Button(tab0, text="Option1").grid(row=2, column=0)
button1 = Button(tab0, text="Option2").grid(row=2, column=1)
button2 = Button(tab0, text="Option3").grid(row=3, column=0)
button3 = Button(tab0, text="Option4").grid(row=3, column=1)

window.mainloop()