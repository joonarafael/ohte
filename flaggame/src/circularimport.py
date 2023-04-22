from gamehandler import receive_terminated_game, receive_flag_slide_show
from gamehandler import receive_input, return_current_flag
from gamehandler import return_current_game_mode, launch_game
from gamehandler import reset_game


def send_terminated_game():
    receive_terminated_game()


def send_flag_slide_show(direction: int):
    receive_flag_slide_show(direction)


def send_input(button: int):
    receive_input(button)


def read_current_flag():
    return return_current_flag()


def read_current_game_mode():
    return return_current_game_mode()


def send_launch(game_mode: int):
    launch_game(game_mode)


def send_reset():
    reset_game()
