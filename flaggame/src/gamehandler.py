# PYLINT WILL NOTIFY FOR CYCLIC IMPORT HERE EVEN IF
# IT IS CRUCIAL FOR GAME LOGIC AND DOES NOT PRODUCE
# ANY KIND OF ERROR DURING SOFTWARE EXECUTION

import random
from math import log
import flaghandler
import timerlogic
import history
import gui  # pylint: disable=cyclic-import

# Game Handler class is responsible for every game mode


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
        self.free_index = -1
        self.buttons = []

    def __str__(self):
        return (f"GameHandler Status: Game Mode {self.game_mode}; Round {self.round};"
                f" Score {self.score}; Lives {self.lives}; Streak {self.streak}")

    # call next round
    def next_round(self):
        gui.display_round(self.round)

        # reset flag queue if needed
        if len(self.remaining_flags) == 0:
            if self.game_mode == 2:
                self.remaining_flags = list(self.all_flags)

            else:
                self.remaining_flags = set(self.all_flags)

        # pick a random flag
        self.current_flag = random.choice(list(self.remaining_flags))

        # time trial has purely random flags
        # otherwise remove from remaining set
        if self.game_mode != 2:
            self.remaining_flags.remove(self.current_flag)

        self.current_flag = self.current_flag[:-4]

        # start timer if needed
        if self.game_mode in (1, 2):
            timerlogic.clock.run_classic_timer()

        # timer function also called for resetting the view
        gui.display_timer()

        # ask to update GUI
        self.update_gui()

    # if new game is launched while old one still running (or window is destroyed)
    # ask to record previous to history
    def terminated_game(self):
        gui.change_status(0)

        if self.game_mode >= 0:
            history.game_terminated(
                [self.game_mode, self.score, self.highest_streak, self.lives])

            gui.history_update()

    # reset counters
    def reset(self, desired_lives: int):
        self.terminated_game()

        # time trial purely random flags
        # other game modes flag set is curated (full rotations)
        if self.game_mode == 2:
            self.remaining_flags = list(self.all_flags)

        else:
            self.remaining_flags = set(self.all_flags)

        self.round = 1
        self.score = 0
        self.streak = 0
        self.highest_streak = 0
        self.lives = desired_lives

        gui.display_score(self.score)
        gui.display_streak(self.streak)
        gui.display_lives(self.lives)
        gui.display_round(self.round)

    # initialize classic game mode
    def classic(self):
        gui.change_title("Classic")

        self.reset(3)
        self.game_mode = 0

        history.game_start("Classic")
        gui.history_update()
        self.next_round()

    # initialize advanced game mode
    def advanced(self):
        gui.change_title("Advanced")

        self.reset(3)
        self.game_mode = 1

        history.game_start("Advanced")
        gui.history_update()
        self.next_round()

    # initialize time trial game mode
    def time_trial(self):
        gui.change_title("Time Trial")

        self.reset(3)
        self.game_mode = 2

        history.game_start("Time Trial")
        gui.history_update()
        self.next_round()

    # initialize one life game mode
    def one_life(self):
        gui.change_title("One Life")

        self.reset(1)
        self.game_mode = 3

        history.game_start("One Life")
        gui.history_update()
        self.next_round()

    # initialize free game mode
    def free(self):
        gui.change_title("Free Mode")

        self.reset(-1)
        self.game_mode = 4

        history.game_start("Free")
        gui.history_update()
        self.next_round()

    # button press triggers answer function
    def player_answered(self, button: int):
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

            # change score depending on the game mode
            # advanced score
            if self.game_mode == 1:
                gui.change_status("correct")
                round_time = timerlogic.clock.read_accurate()

                if round_time < 5.0000:
                    points_gained = 180 + ((-4 * (round_time ** 2)) / 1.25)

                else:
                    points_gained = 100

                points_gained = points_gained * (log(self.streak, 20) + 1)
                self.score += int(points_gained)

            # time trial score
            elif self.game_mode == 2:
                round_time = timerlogic.clock.read_accurate()

                # time trial game ends if round took more than 5 seconds
                if round_time <= 5.0000:
                    gui.change_status("correct")
                    points_gained = 180 + ((-4 * (round_time ** 2)) / 1.25)
                    self.score += int(points_gained)

                else:
                    gui.change_status("time's up")
                    self.lives = 0

            # classic, one life and free mode score
            else:
                gui.change_status("correct")
                self.score += 100

        # wrong answer handling
        else:
            gui.change_status(self.current_flag.upper().replace("_", " "))
            self.lives -= 1
            self.streak = 0

            # time trial ends in a wrong answer too
            # if elapsed time exceeds 5 seconds
            if self.game_mode == 2:
                round_time = timerlogic.clock.read_accurate()

                if round_time > 5.0000:
                    gui.change_status("time's up")
                    self.lives = 0

        # round is over, update game status for player
        gui.display_score(self.score)
        gui.display_streak(self.streak)
        gui.display_lives(self.lives)

        # check if game is over, ask to record history
        if self.lives == 0:
            history.game_over(
                [self.game_mode, self.score, self.highest_streak])
            gui.change_title("Game Over!")
            self.game_mode = -1

            gui.history_update()
            gui.inactive_buttons()

        # launch next round
        else:
            self.round += 1
            self.next_round()

    # general function to ask for gui updates
    def update_gui(self):
        # read new flag
        flag_path = flaghandler.FLAG_DIR
        photo_path = flag_path + '/' + self.current_flag + ".png"

        # update displayed flag to player
        gui.next_flag(photo_path)

        # generate 4 options with 3 dummies
        self.buttons = [self.current_flag.upper().replace("_", " ")]
        picked = [self.current_flag]

        for _ in range(3):
            wrong_answer = self.current_flag

            while wrong_answer == self.current_flag or wrong_answer in picked:
                wrong_answer = random.choice(self.all_flags)
                wrong_answer = wrong_answer[:-4]

            picked.append(wrong_answer)
            self.buttons.append(wrong_answer.upper().replace("_", " "))

        # shuffle buttons
        random.shuffle(self.buttons)

        # update displayed buttons to player
        gui.next_buttons(self.buttons)

    # debugging to scroll through every flag
    def flag_slide_show(self, direction: int):
        self.terminated_game()

        self.free_index = self.free_index + direction
        self.game_mode = -2

        if self.free_index > 197:
            self.free_index = self.free_index - 198

        if self.free_index < 0:
            self.free_index = 198 - abs(self.free_index)

        flag_path = flaghandler.FLAG_DIR
        curr_flag = self.all_flags[self.free_index]

        gui.next_flag(flag_path + '/' + curr_flag)
        gui.change_title(curr_flag[:-4].upper().replace("_", " "))

        self.buttons = ["PREVIOUS FLAG", "NEXT FLAG",
                        "MOVE TEN BACK", "MOVE TEN FORWARD"]

        gui.next_buttons(self.buttons)


MASTER_GAME_HANDLER = GameHandler()
