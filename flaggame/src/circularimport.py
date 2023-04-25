# MODULE DESCRIPTION

# circularimport is utilized to dodge the circular import errors caused by Python

# gui and gamehandler modules communicate through this module

# gamehandler functions
from gamehandler import receive_terminated_game, receive_flag_slide_show
# ...
from gamehandler import receive_input, reset_game
# ...
from gamehandler import return_current_game_mode, launch_game
# flaghandler constants
from flaghandler import CORRECT_AMOUNT, COMPLETE_FLAG_LIST

# window is destroyed


def send_terminated_game():
    receive_terminated_game()

# user launches the free flag browsing


def send_flag_slide_show(direction: int):
    receive_flag_slide_show(direction)

# buttton is pressed


def send_input(button: int):
    receive_input(button)

# gui asks for current game mode


def read_current_game_mode():
    return return_current_game_mode()

# game launch event


def send_launch(game_mode: int):
    if len(COMPLETE_FLAG_LIST) == CORRECT_AMOUNT:
        launch_game(game_mode)

    else:
        print("Game cannot be launched as flag image files have not been found.")

# user cancels game through menu (or for debug options)


def send_reset():
    reset_game()
