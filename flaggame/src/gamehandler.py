import random
from math import log
from copy import deepcopy
import flaghandler
import timerlogic
import history
import csvhandler


class MasterGameHandler():
    """
    manage all core game logic and handle every game mode
    """

    def __init__(self, game_tab, stats_tab, history_tab):
        """
        initialize all variables and establish a connection to specific gui elements

        Args:
            game_tab: game tab gui element from master window (for function calling),
            stats_tab: stats tab gui element,
            history_tab: history tab gui element
        """

        print("Initializing GameHandler...")

        self.current_flag = None
        self.score = 0
        self.round = 0
        self.lives = 0
        self.streak = 0
        self.highest_streak = 0
        self.game_mode = -1
        self.all_flags = flaghandler.MASTER_FLAGHANDLER.complete_flag_list
        self.remaining_flags = None
        self.free_index = 0
        self.buttons = []

        self.game_tab = game_tab
        self.stats_tab = stats_tab
        self.history_tab = history_tab

    def reset_instance(self):
        """
        cancel any ongoing game and reset the whole class instance for debugging
        """

        print("Any ongoing game terminated, resetting GameHandler...")

        self.current_flag = None
        self.score = 0
        self.round = 0
        self.lives = 0
        self.streak = 0
        self.highest_streak = 0
        self.game_mode = -1
        self.all_flags = flaghandler.MASTER_FLAGHANDLER.complete_flag_list
        self.remaining_flags = None
        self.free_index = 0
        self.buttons = []

        self.game_tab.display_score(self.score)
        self.game_tab.display_streak(self.streak)
        self.game_tab.display_round(self.round)
        self.game_tab.display_timer()
        self.game_tab.display_lives(self.lives, "#e6e6e6")

        self.game_tab.inactive_buttons()
        self.game_tab.change_title("GAME CANCELLED", "#e6e6e6")
        self.game_tab.change_status(
            "Start a new game from File > New Game.", "#e6e6e6")

    def __str__(self):
        return (f"GameHandler Status: Game Mode {self.game_mode}; Round {self.round};"
                f" Score {self.score}; Lives {self.lives}; Streak {self.streak}.")

    def next_round(self):
        """
        prepare for the next round, pick a new flag and update the correct answer accordingly
        """

        self.game_tab.display_round(self.round)

        if len(self.remaining_flags) == 0:
            self.remaining_flags = set(self.all_flags)

        self.current_flag = random.choice(list(self.remaining_flags))

        if self.game_mode != 2:
            self.remaining_flags.remove(self.current_flag)

        self.current_flag = self.current_flag[:-4]

        timerlogic.clock.run_timer()
        self.game_tab.display_timer()

        self.update_gui()

    def terminated_game(self):
        """
        record any cancelled game to history & statistics before other resetting
        """

        self.game_tab.change_status("", "#000000")

        if self.game_mode >= 0:
            history.MASTER_HISTORY_HANDLER.game_terminated(
                [self.game_mode, self.score, self.highest_streak, self.lives])
            self.history_tab.history_update()

            if self.streak > 0:
                csvhandler.MASTER_RUNNING_GAME.record_new_streak(self.streak)

            if self.round > 1:
                csvhandler.MASTER_RUNNING_GAME.write_game_rounds_to_file(
                    self.game_mode)
                self.stats_tab.stats_update()

    def reset(self, desired_lives: int):
        """
        reset all game stats to 0, mainly used just not to write more duplicate code later

        Args:
            desired_lives (int): requested lives count at game start for specific game modes
        """

        self.terminated_game()

        self.remaining_flags = set(self.all_flags)
        self.round = 1
        self.score = 0
        self.streak = 0
        self.highest_streak = 0
        self.lives = desired_lives

        csvhandler.MASTER_RUNNING_GAME.launch_new_game()

        self.game_tab.display_score(self.score)
        self.game_tab.display_streak(self.streak)
        self.game_tab.display_round(self.round)

        if self.lives < 0:
            self.game_tab.display_lives("Inf", "#cfffd1")

        elif self.lives == 1:
            self.game_tab.display_lives(self.lives, "#ff6e6e")

        else:
            self.game_tab.display_lives(self.lives, "#e6e6e6")

    def classic(self):
        """
        initialize a classic game
        """

        if (len(flaghandler.MASTER_FLAGHANDLER.complete_flag_list)
                != flaghandler.MASTER_FLAGHANDLER.correct_amount):
            return

        self.game_tab.change_title("CLASSIC", "#e6e6e6")

        self.reset(3)
        self.game_mode = 0

        history.MASTER_HISTORY_HANDLER.game_start("Classic")
        self.history_tab.history_update()
        self.next_round()

    def advanced(self):
        """
        initialize an advanced game
        """

        if (len(flaghandler.MASTER_FLAGHANDLER.complete_flag_list)
                != flaghandler.MASTER_FLAGHANDLER.correct_amount):
            return

        self.game_tab.change_title("ADVANCED", "#e6e6e6")

        self.reset(3)
        self.game_mode = 1

        history.MASTER_HISTORY_HANDLER.game_start("Advanced")
        self.history_tab.history_update()
        self.next_round()

    def time_trial(self):
        """
        initialize a time trial game
        """

        if (len(flaghandler.MASTER_FLAGHANDLER.complete_flag_list)
                != flaghandler.MASTER_FLAGHANDLER.correct_amount):
            return

        self.game_tab.change_title("TIME TRIAL", "#e6e6e6")

        self.reset(3)
        self.game_mode = 2

        history.MASTER_HISTORY_HANDLER.game_start("Time Trial")
        self.history_tab.history_update()
        self.next_round()

    def one_life(self):
        """
        initialize an one life game
        """

        if (len(flaghandler.MASTER_FLAGHANDLER.complete_flag_list)
                != flaghandler.MASTER_FLAGHANDLER.correct_amount):
            return

        self.game_tab.change_title("ONE LIFE", "#e6e6e6")

        self.reset(1)
        self.game_mode = 3

        history.MASTER_HISTORY_HANDLER.game_start("One Life")
        self.history_tab.history_update()
        self.next_round()

    def free(self):
        """
        initialize a free mode game
        """

        if (len(flaghandler.MASTER_FLAGHANDLER.complete_flag_list)
                != flaghandler.MASTER_FLAGHANDLER.correct_amount):
            return

        self.game_tab.change_title("FREE MODE", "#e6e6e6")

        self.reset(-1)
        self.game_mode = 4

        history.MASTER_HISTORY_HANDLER.game_start("Free")
        self.history_tab.history_update()
        self.next_round()

    def player_answered(self, button: int):
        """
        check & handle the player answer input

        Args:
            button (int): player input (button as an integer)
        """

        if self.game_mode == -1:
            return

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

        round_time = timerlogic.clock.read_accurate()

        # check if answer was correct
        if self.buttons[button] == self.current_flag.upper().replace("_", " "):

            # advanced
            if self.game_mode == 1:
                self.streak += 1
                self.game_tab.change_status("CORRECT!", "#bbff78")

                if round_time < 5.0000:
                    points_gained = 180 + ((-4 * (round_time ** 2)) / 1.25)

                else:
                    points_gained = 100

                points_gained = points_gained * (log(self.streak, 20) + 1)

            # time trial
            elif self.game_mode == 2:
                if round_time <= 5.0000:
                    self.game_tab.change_status("CORRECT!", "#bbff78")
                    points_gained = 180 + ((-4 * (round_time ** 2)) / 1.25)
                    self.streak += 1

                # game over in time trial if round time > 5s
                else:
                    formatted = self.current_flag.upper().replace("_", " ")
                    self.game_tab.change_status(
                        f"TIME'S UP! CORRECT ANSWER WAS {formatted}.", "#ff7c78")
                    points_gained = 0
                    self.lives = 0

            # other game modes
            else:
                self.game_tab.change_status("CORRECT!", "#bbff78")
                points_gained = 100
                self.streak += 1

            self.score += int(points_gained)
            csvhandler.MASTER_RUNNING_GAME.record_new_round(
                int(points_gained), round_time)

            if self.streak > self.highest_streak:
                self.highest_streak = self.streak

        # wrong answer
        else:

            # reduce lives if other game mode than free
            if self.game_mode != 4:
                self.lives -= 1

                if 0 <= self.lives <= 1:
                    self.game_tab.display_lives(self.lives, "#ff6e6e")

                else:
                    self.game_tab.display_lives(self.lives, "#e6e6e6")

            formatted = self.current_flag.upper().replace("_", " ")
            self.game_tab.change_status(
                f"WRONG! CORRECT ANSWER WAS {formatted}.", "#ff7c78")

            if self.streak > 0:
                csvhandler.MASTER_RUNNING_GAME.record_new_streak(self.streak)

            self.streak = 0

            # time trial ends if round time > 5s even with a wrong answer
            if self.game_mode == 2 and round_time > 5.0000:
                self.game_tab.change_status(
                    f"TIME'S UP! CORRECT ANSWER WAS {formatted}.", "#ff7c78")
                self.lives = 0

            csvhandler.MASTER_RUNNING_GAME.record_new_round(0, round_time)

        self.game_tab.display_score(self.score)
        self.game_tab.display_streak(self.streak)

        # check if game is over
        if self.lives == 0:
            history.MASTER_HISTORY_HANDLER.game_over(
                [self.game_mode, self.score, self.highest_streak])

            csvhandler.MASTER_RUNNING_GAME.write_game_rounds_to_file(
                self.game_mode)

            self.game_tab.change_title("Game Over!", "#e6acac")
            self.game_mode = -1

            self.history_tab.history_update()
            self.stats_tab.stats_update()
            self.game_tab.inactive_buttons()

        else:
            self.round += 1
            self.next_round()

    def update_gui(self):
        """
        determine the path for the correct flag and choose the button options
        """

        photo_path = flaghandler.MASTER_FLAGHANDLER.flag_dir + \
            '/' + self.current_flag + ".png"

        self.game_tab.next_flag(photo_path)

        self.buttons = [self.current_flag.upper().replace("_", " ")]

        excluding_set = deepcopy(self.all_flags)
        excluding_set.remove(f"{self.current_flag}.png")

        dummy_picks = random.sample(excluding_set, 3)

        for dummy in dummy_picks:
            self.buttons.append(dummy.upper().replace("_", " ")[:-4])

        random.shuffle(self.buttons)

        self.game_tab.next_buttons(self.buttons)

    def flag_slide_show(self, direction: int):
        """
        initialize the free flag browsing

        Args:
            direction (int): flag rotation direction, back & forth, (steps 1 or 10)
        """

        if (len(flaghandler.MASTER_FLAGHANDLER.complete_flag_list)
                != flaghandler.MASTER_FLAGHANDLER.correct_amount):
            return

        self.terminated_game()

        self.game_mode = -2
        self.free_index = self.free_index + direction

        if self.free_index > 197:
            self.free_index = self.free_index - 198

        if self.free_index < 0:
            self.free_index = 198 - abs(self.free_index)

        flag_path = flaghandler.MASTER_FLAGHANDLER.flag_dir
        curr_flag = self.all_flags[self.free_index]

        self.game_tab.next_flag(flag_path + '/' + curr_flag)
        self.game_tab.change_title(
            curr_flag[:-4].upper().replace("_", " "), "#e6e6e6")

        self.buttons = ["PREVIOUS FLAG", "NEXT FLAG",
                        "MOVE TEN BACK", "MOVE TEN FORWARD"]

        self.game_tab.next_buttons(self.buttons)

    def reset_game_handler(self):
        """
        initiatize the complete GameHandler reset sequence (game cancelling)
        """

        self.terminated_game()
        self.reset_instance()
