import random
from math import log
from copy import deepcopy
import flaghandler
import timerlogic
import history
import csvhandler
import gui # pylint: disable=cyclic-import

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

    def __str__(self):
        return (f"GameHandler Status: Game Mode {self.game_mode}; Round {self.round};"
                f" Score {self.score}; Lives {self.lives}; Streak {self.streak}")

    # call next round
    def next_round(self):
        gui.display_round(self.round)

        # reset flag queue if needed
        if len(self.remaining_flags) == 0:
            self.remaining_flags = set(self.all_flags)

        # pick a random flag
        self.current_flag = random.choice(list(self.remaining_flags))

        # time trial has purely random flags
        # otherwise remove from remaining set
        if self.game_mode != 2:
            self.remaining_flags.remove(self.current_flag)

        # remove .png suffix
        self.current_flag = self.current_flag[:-4]

        # run timer always for stats recording
        timerlogic.clock.run_classic_timer()

        # timer function called as it also resets the view
        # (reverts back to plain text "Timer")
        gui.display_timer()

        # ask own class function to send gui update requests
        self.update_gui()

    # if new game is launched while old one still running (or window is destroyed)
    # ask to record history
    def terminated_game(self):
        gui.change_status(0)

        # free flag browsing or debug modes won't record history
        if self.game_mode >= 0:
            history.game_terminated(
                [self.game_mode, self.score, self.highest_streak, self.lives])

            if self.round > 1:
                csvhandler.write_game(self.game_mode)

            gui.history_update()
            gui.stats_update()

    # reset counters
    def reset(self, desired_lives: int):
        self.terminated_game()

        self.remaining_flags = set(self.all_flags)

        self.round = 1
        self.score = 0
        self.streak = 0
        self.highest_streak = 0
        self.lives = desired_lives

        csvhandler.new_game()

        gui.display_score(self.score)
        gui.display_streak(self.streak)
        gui.display_lives(self.lives)
        gui.display_round(self.round)

    # initialize classic game mode
    def classic(self):
        gui.change_title("CLASSIC")

        self.reset(3)
        self.game_mode = 0

        history.game_start("Classic")
        gui.history_update()
        self.next_round()

    # initialize advanced game mode
    def advanced(self):
        gui.change_title("ADVANCED")

        self.reset(3)
        self.game_mode = 1

        history.game_start("Advanced")
        gui.history_update()
        self.next_round()

    # initialize time trial game mode
    def time_trial(self):
        gui.change_title("TIME TRIAL")

        self.reset(3)
        self.game_mode = 2

        history.game_start("Time Trial")
        gui.history_update()
        self.next_round()

    # initialize one life game mode
    def one_life(self):
        gui.change_title("ONE LIFE")

        self.reset(1)
        self.game_mode = 3

        history.game_start("One Life")
        gui.history_update()
        self.next_round()

    # initialize free game mode
    def free(self):
        gui.change_title("FREE MODE")

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

        # check if answer was correct
        if self.buttons[button] == self.current_flag.upper().replace("_", " "):
            self.streak += 1

            if self.streak > self.highest_streak:
                self.highest_streak = self.streak

            round_time = timerlogic.clock.read_accurate()

            # change score depending on the game mode
            # advanced score (details in rulebook)
            if self.game_mode == 1:
                gui.change_status("correct")

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
                    gui.change_status("correct")
                    points_gained = 180 + ((-4 * (round_time ** 2)) / 1.25)

                else:
                    gui.change_status("time's up")
                    self.lives = 0

            # classic, one life and free mode score (details in rulebook)
            else:
                gui.change_status("correct")
                points_gained = 100

            self.score += int(points_gained)
            csvhandler.write_round(int(points_gained), round_time)

        # wrong answer handling
        else:
            round_time = timerlogic.clock.read_accurate()

            gui.change_status(self.current_flag.upper().replace("_", " "))
            self.lives -= 1

            csvhandler.write_streak(self.streak)
            self.streak = 0

            # time trial ends in a wrong answer too
            # if elapsed time exceeds 5 seconds
            if self.game_mode == 2:
                round_time = timerlogic.clock.read_accurate()

                if round_time > 5.0000:
                    gui.change_status("time's up")
                    self.lives = 0

            csvhandler.write_round(0, round_time)

        # round is over, update game status for player
        gui.display_score(self.score)
        gui.display_streak(self.streak)
        gui.display_lives(self.lives)

        # check if game is over, ask to record history
        if self.lives == 0:
            history.game_over(
                [self.game_mode, self.score, self.highest_streak])
            csvhandler.write_game(self.game_mode)
            gui.change_title("Game Over!")
            self.game_mode = -1

            gui.history_update()
            gui.stats_update()
            gui.inactive_buttons()

        # launch next round
        else:
            self.round += 1
            self.next_round()

    # general function to ask for gui updates every round
    def update_gui(self):
        # find path for the new flag
        flag_path = flaghandler.FLAG_DIR
        photo_path = flag_path + '/' + self.current_flag + ".png"

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
        gui.change_title(curr_flag[:-4].upper().replace("_", " "))

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


def return_current_flag():
    return MASTER_GAME_HANDLER.current_flag.upper().replace("_", " ")


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
    gui.change_title("GAMEHANDLER RESET")
    gui.change_status("Start a new game from File > New Game.")
