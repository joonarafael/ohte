# MODULE DESCRIPTION

# gamehandler is responsible for all the core game logic

# it handles every game mode and sends update events to
# history & statistics modules

# it also needs to update gui, but gui needs to send launch
# events back, so pylint cyclic-import disabled here just this once

import random             # flag queue & buttons are randomized
from math import log      # advanced game mode points are calculated with log
from copy import deepcopy  # deepcopy made from complete flaglist for button randomizing
import flaghandler        # information about flags needed from flaghandler
import timerlogic         # timerlogic includes the master clock class
import history            # send history update events
import csvhandler         # send statistics update events
import gui  # pylint: disable=cyclic-import

# GameHandler class is responsible for every game mode


class GameHandler():
    def __init__(self):
        print("Initializing GameHandler...")

        self.current_flag = None
        self.score = 0
        self.round = 0
        self.lives = 0
        self.streak = 0
        self.highest_streak = 0
        self.game_mode = -1
        self.all_flags = flaghandler.COMPLETE_FLAG_LIST
        self.remaining_flags = None
        self.free_index = 0
        self.buttons = []

    # resetting (or cancelling a game) the GameHandler instance
    def reset_instance(self):
        print("Initializing GameHandler...")

        self.current_flag = None
        self.score = 0
        self.round = 0
        self.lives = 0
        self.streak = 0
        self.highest_streak = 0
        self.game_mode = -1
        self.all_flags = flaghandler.COMPLETE_FLAG_LIST
        self.remaining_flags = None
        self.free_index = 0
        self.buttons = []

        gui.display_score(self.score)
        gui.display_streak(self.streak)
        gui.display_round(self.round)
        gui.display_timer()
        gui.display_lives(self.lives, "#e6e6e6")

    # test to check status (pytest)
    def __str__(self):
        return (f"GameHandler Status: Game Mode {self.game_mode}; Round {self.round};"
                f" Score {self.score}; Lives {self.lives}; Streak {self.streak}")

    # next round
    def next_round(self):
        gui.display_round(self.round)

        # reset flag queue if needed
        if len(self.remaining_flags) == 0:
            self.remaining_flags = set(self.all_flags)

        # pick a random flag
        self.current_flag = random.choice(list(self.remaining_flags))

        # time trial has purely random flags
        # otherwise remove current flag from remaining set
        if self.game_mode != 2:
            self.remaining_flags.remove(self.current_flag)

        # remove .png suffix
        self.current_flag = self.current_flag[:-4]

        # run timer for all game modes to enable round length recording
        timerlogic.clock.run_classic_timer()
        gui.display_timer()

        self.update_gui()

    # if new game is launched while old one still running (or window is destroyed)
    # ask to record history
    def terminated_game(self):
        gui.change_status("", "#000000")

        # free flag browsing or debug modes won't record history
        if self.game_mode >= 0:
            history.game_terminated(
                [self.game_mode, self.score, self.highest_streak, self.lives])
            gui.history_update()

            if self.streak > 0:
                csvhandler.MASTER_RUNNING_GAME.write_new_streak(self.streak)

            if self.round > 1:
                csvhandler.MASTER_RUNNING_GAME.write_game_rounds_to_file(
                    self.game_mode)
                gui.stats_update()

    # reset counters for a new game
    def reset(self, desired_lives: int):
        self.terminated_game()

        self.remaining_flags = set(self.all_flags)
        self.round = 1
        self.score = 0
        self.streak = 0
        self.highest_streak = 0
        self.lives = desired_lives

        csvhandler.MASTER_RUNNING_GAME.launch_new_game()

        gui.display_score(self.score)
        gui.display_streak(self.streak)
        gui.display_round(self.round)

        if self.lives < 0:
            gui.display_lives("Inf", "#cfffd1")

        elif self.lives == 1:
            gui.display_lives(self.lives, "#ff6e6e")

        else:
            gui.display_lives(self.lives, "#e6e6e6")

    # initialize classic game mode
    def classic(self):
        gui.change_title("CLASSIC", "#e6e6e6")

        self.reset(3)
        self.game_mode = 0

        history.game_start("Classic")
        gui.history_update()
        self.next_round()

    # initialize advanced game mode
    def advanced(self):
        gui.change_title("ADVANCED", "#e6e6e6")

        self.reset(3)
        self.game_mode = 1

        history.game_start("Advanced")
        gui.history_update()
        self.next_round()

    # initialize time trial game mode
    def time_trial(self):
        gui.change_title("TIME TRIAL", "#e6e6e6")

        self.reset(3)
        self.game_mode = 2

        history.game_start("Time Trial")
        gui.history_update()
        self.next_round()

    # initialize one life game mode
    def one_life(self):
        gui.change_title("ONE LIFE", "#e6e6e6")

        self.reset(1)
        self.game_mode = 3

        history.game_start("One Life")
        gui.history_update()
        self.next_round()

    # initialize free game mode
    def free(self):
        gui.change_title("FREE MODE", "#e6e6e6")

        self.reset(-1)
        self.game_mode = 4

        history.game_start("Free")
        gui.history_update()
        self.next_round()

    # button press event triggers answer function
    def player_answered(self, button: int):
        # fail-safe mechanism:
        # if no game yet launched, skip function
        if self.game_mode == -1:
            return

        # debug option (free flag browsing)
        if self.game_mode == -2:
            if button == 0:
                self.flag_slide_show(-1)

            elif button == 1:
                self.flag_slide_show(1)

            elif button == 2:
                self.flag_slide_show(-10)

            else:
                self.flag_slide_show(10)

            return

        # check round time
        round_time = timerlogic.clock.read_accurate()

        # check if answer was correct
        if self.buttons[button] == self.current_flag.upper().replace("_", " "):
            # change score depending on the game mode
            # advanced score (details in rulebook)
            if self.game_mode == 1:
                self.streak += 1
                gui.change_status("CORRECT!", "#bbff78")

                if round_time < 5.0000:
                    points_gained = 180 + ((-4 * (round_time ** 2)) / 1.25)

                else:
                    points_gained = 100

                points_gained = points_gained * (log(self.streak, 20) + 1)

            # time trial score (details in rulebook)
            elif self.game_mode == 2:
                # time trial game ends if round took more than 5 seconds
                # gui forces any dummy answer, round time checked nonetheless
                # here once again for accurate and fair gameplay
                if round_time <= 5.0000:
                    gui.change_status("CORRECT!", "#bbff78")
                    points_gained = 180 + ((-4 * (round_time ** 2)) / 1.25)
                    self.streak += 1

                else:
                    formatted = self.current_flag.upper().replace("_", " ")
                    gui.change_status(
                        f"TIME'S UP! CORRECT ANSWER WAS {formatted}.", "#ff7c78")
                    points_gained = 0
                    self.lives = 0

            # classic, one life and free mode score (details in rulebook)
            else:
                gui.change_status("CORRECT!", "#bbff78")
                points_gained = 100
                self.streak += 1

            self.score += int(points_gained)
            csvhandler.MASTER_RUNNING_GAME.write_new_round(
                int(points_gained), round_time)

            if self.streak > self.highest_streak:
                self.highest_streak = self.streak

        # wrong answer handling
        else:
            if self.game_mode != 4:
                self.lives -= 1

                if 0 <= self.lives <= 1:
                    gui.display_lives(self.lives, "#ff6e6e")

                else:
                    gui.display_lives(self.lives, "#e6e6e6")

            # update the correct answer to player
            formatted = self.current_flag.upper().replace("_", " ")
            gui.change_status(
                f"WRONG! CORRECT ANSWER WAS {formatted}.", "#ff7c78")

            if self.streak > 0:
                csvhandler.MASTER_RUNNING_GAME.write_new_streak(self.streak)

            self.streak = 0

            # time trial ends in a wrong answer too
            # if elapsed time exceeds 5 seconds
            if self.game_mode == 2:
                if round_time > 5.0000:
                    gui.change_status(
                        f"TIME'S UP! CORRECT ANSWER WAS {formatted}.", "#ff7c78")
                    self.lives = 0

            csvhandler.MASTER_RUNNING_GAME.write_new_round(0, round_time)

        # round is over, update game status for player
        gui.display_score(self.score)
        gui.display_streak(self.streak)

        # check if game is over, ask to record history
        if self.lives == 0:
            history.game_over(
                [self.game_mode, self.score, self.highest_streak])

            csvhandler.MASTER_RUNNING_GAME.write_game_rounds_to_file(
                self.game_mode)

            gui.change_title("Game Over!", "#e6acac")
            self.game_mode = -1

            gui.history_update()
            gui.stats_update()
            gui.inactive_buttons()

        # else launch next round
        else:
            self.round += 1
            self.next_round()

    # general function to ask for gui updates every round (buttons)
    def update_gui(self):
        # find path for the new flag
        photo_path = flaghandler.FLAG_DIR + '/' + self.current_flag + ".png"

        # update displayed flag to player
        gui.next_flag(photo_path)

        # generate 4 options with 3 dummies
        self.buttons = [self.current_flag.upper().replace("_", " ")]

        excluding_set = deepcopy(self.all_flags)
        excluding_set.remove(f"{self.current_flag}.png")

        dummy_picks = random.sample(excluding_set, 3)

        for dummy in dummy_picks:
            self.buttons.append(dummy.upper().replace("_", " ")[:-4])

        # shuffle buttons
        random.shuffle(self.buttons)

        # update displayed buttons to player
        gui.next_buttons(self.buttons)

    # debugging to scroll through every flag
    def flag_slide_show(self, direction: int):
        # terminate any ongoing game
        self.terminated_game()

        self.game_mode = -2
        self.free_index = self.free_index + direction

        # handle overflow
        if self.free_index > 197:
            self.free_index = self.free_index - 198

        if self.free_index < 0:
            self.free_index = 198 - abs(self.free_index)

        # display flag to player
        flag_path = flaghandler.FLAG_DIR
        curr_flag = self.all_flags[self.free_index]

        gui.next_flag(flag_path + '/' + curr_flag)
        gui.change_title(curr_flag[:-4].upper().replace("_", " "), "#e6e6e6")

        self.buttons = ["PREVIOUS FLAG", "NEXT FLAG",
                        "MOVE TEN BACK", "MOVE TEN FORWARD"]

        gui.next_buttons(self.buttons)

    # debugging to reset GameHandler completely
    def reset_game_handler(self):
        self.terminated_game()
        self.reset_instance()


# launch the Master Game Handler
MASTER_GAME_HANDLER = GameHandler()


def receive_terminated_game():
    MASTER_GAME_HANDLER.terminated_game()


def receive_flag_slide_show(direction: int):
    MASTER_GAME_HANDLER.flag_slide_show(direction)


def receive_input(button: int):
    MASTER_GAME_HANDLER.player_answered(button)


def return_current_game_mode():
    return MASTER_GAME_HANDLER.game_mode


def launch_game(game: int):
    if game == 0:
        MASTER_GAME_HANDLER.classic()

    elif game == 1:
        MASTER_GAME_HANDLER.advanced()

    elif game == 2:
        MASTER_GAME_HANDLER.time_trial()

    elif game == 3:
        MASTER_GAME_HANDLER.one_life()

    else:
        MASTER_GAME_HANDLER.free()


def reset_game():
    MASTER_GAME_HANDLER.reset_game_handler()

    gui.inactive_buttons()
    gui.change_title("GAME CANCELLED", "#e6e6e6")
    gui.change_status("Start a new game from File > New Game.", "#e6e6e6")
