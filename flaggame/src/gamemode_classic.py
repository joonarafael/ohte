import random
import timeit
import flaghandler
import gui

def new_game():
    round = 0
    score = 0
    time = 0
    lives = 0

    flagPath = flaghandler.flagdir
    list_order = flaghandler.completeFlagList

    random.shuffle(list_order)

    gui.photoPath = flagPath + '/' + list_order[round]
    gui.nextFlag()