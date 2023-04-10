# PYLINT WILL NOTIFY FOR CYCLIC IMPORT HERE EVEN IF
# IT IS CRUCIAL FOR GAME LOGIC AND DOES NOT PRODUCE
# ANY KIND OF ERROR DURING SOFTWARE EXECUTION

import random
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
        self.dev_status_print = False
        self.all_flags = flaghandler.COMPLETE_FLAG_LIST
        self.remaining_flags = None
        self.free_index = -1
        self.buttons = []

    def __str__(self):
        return (f"GameHandler Status: Game Mode {self.game_mode}; Round {self.round};"
                f" Score {self.score}; Lives {self.lives}; Streak {self.streak};"
                f" DevPrint {self.dev_status_print}.")

    # call next round
    def next_round(self):
        if self.dev_status_print:
            print("Current Round", self.round)

        gui.display_round(self.round)

        # pick a random  flag, remove from remaining set
        self.current_flag = random.choice(list(self.remaining_flags))
        self.remaining_flags.remove(self.current_flag)
        self.current_flag = self.current_flag[:-4]

        # start timer if needed
        if self.game_mode == 1:
            gui.display_timer()
            timerlogic.clock.run_classic_timer()

        # ask to update GUI
        self.update_gui()

    # if new game is launched while old one still running (or window is destroyed)
    # ask to record previous to history
    def terminated_game(self):
        if self.game_mode >= 0:
            history.game_terminated(
                [self.game_mode, self.score, self.highest_streak, self.lives])

            gui.history_update()

    # reset counters
    def reset(self, desired_lives: int):
        self.terminated_game()

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
        print("Launching Classic Game...")
        gui.change_title("Classic")

        self.reset(3)
        self.game_mode = 0

        print("Game Start!")
        history.game_start("Classic")
        gui.history_update()
        self.next_round()

    # initialize advanced game mode
    def advanced(self):
        print("Launching Advanced Game...")
        gui.change_title("Advanced")

        self.reset(3)
        self.game_mode = 1

        print("Game Start!")
        history.game_start("Advanced")
        gui.history_update()
        self.next_round()

    # initialize free game mode
    def free(self):
        print("Launching Free Game...")
        gui.change_title("Free Mode")

        self.reset(-1)
        self.game_mode = 4

        print("Game Start!")
        history.game_start("Free")
        gui.history_update()
        self.next_round()

    def player_answered(self, button: int):
        # if no game yet launched, skip function
        if self.game_mode == -1:
            return

        # debug option
        if self.game_mode == -2:
            if button in (0, 2):
                self.flag_slide_show(-1)
                return

            self.flag_slide_show(1)
            return

        # check if answer was correct
        if self.buttons[button] == self.current_flag.upper().replace("_", " "):
            self.streak += 1

            if self.streak > self.highest_streak:
                self.highest_streak = self.streak

            # change score depending on the game mode
            # classic score
            if self.game_mode == 0:
                self.score += 100

            # advanced score
            elif self.game_mode == 1:
                round_time = timerlogic.clock.read_accurate()

                if round_time < 5:
                    points_gained = 100 + (20 * (5 - round_time))

                else:
                    points_gained = 100

                points_gained = points_gained * \
                    (((1 / -self.streak) + 2) ** 1.5)
                self.score += int(points_gained)

            # free game mode
            elif self.game_mode == 4:
                self.score += 100

            # developer print
            if self.dev_status_print:
                print("Correct! You have answered",
                      self.streak, "times correct in a row!")

        # wrong answer handling
        else:
            self.lives -= 1
            self.streak = 0

            if self.dev_status_print:
                print("Wrong!", self.lives, "lives remaining.")

        if self.dev_status_print:
            print("Current score:", self.score)

        # round is over, update game status for player
        gui.display_score(self.score)
        gui.display_streak(self.streak)
        gui.display_lives(self.lives)

        # check if game is over, ask to record history
        if self.lives == 0:
            history.game_over(
                [self.game_mode, self.score, self.highest_streak])
            gui.change_title("Flag Game")
            self.game_mode = -1

            if self.dev_status_print:
                print(
                    "Game over, you're out of lives! Start new game from File > New game.")

            gui.history_update()

        # launch next round
        else:
            self.round += 1
            self.next_round()

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

        if self.dev_status_print:
            print("Generated options", self.buttons, "out of which",
                  self.current_flag.upper().replace("_", " "), "is correct.")

        # update displayed buttons to player
        gui.next_buttons(self.buttons)

    # debugging to scroll through every flag
    def flag_slide_show(self, direction: int):
        self.terminated_game()

        self.free_index = self.free_index + direction
        self.game_mode = -2

        if self.free_index == 198:
            self.free_index = 0

        if self.free_index == -1:
            self.free_index = 197

        flag_path = flaghandler.FLAG_DIR
        curr_flag = self.all_flags[self.free_index]

        gui.next_flag(flag_path + '/' + curr_flag)

        self.buttons = ["PREVIOUS FLAG", "NEXT FLAG",
                        "PREVIOUS FLAG", "NEXT FLAG"]

        gui.next_buttons(self.buttons)


MASTER_GAME_HANDLER = GameHandler()
