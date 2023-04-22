import csv
from os import getcwd
import timeit

# determine directory for the history file
WORKING_DIR = getcwd()

if WORKING_DIR[-3:] != "src":
    WORKING_DIR = WORKING_DIR + "/src"

STATS_PATH = WORKING_DIR + '/stats.csv'
ROUNDS_PATH = WORKING_DIR + '/rounds.csv'

STATS_MASTER_ERROR = True
ROUNDS_MASTER_ERROR = True

print("Opening (creating if it doesn't exist) the game stats file 'stats.csv'...")

# check stats file
try:
    with open(STATS_PATH, 'r+', encoding="utf-8") as launch_file:
        file_len = len(launch_file.readlines())

    STATS_MASTER_ERROR = False

except FileNotFoundError:
    with open(STATS_PATH, 'w+', encoding="utf-8") as launch_file:
        file_len = len(launch_file.readlines())

    STATS_MASTER_ERROR = False

if STATS_MASTER_ERROR:
    print("ERROR while opening 'stats.csv':")
    print("Please ensure file integrity or create it manually before continuing.")
    print("If continuing, no stats will be recorded.")
    print("Software relaunch is required to record stats again.")

print("Opening (creating if it doesn't exist) the game stats file 'rounds.csv'...")

# check rounds file
try:
    with open(ROUNDS_PATH, 'r+', encoding="utf-8") as launch_file:
        file_len = len(launch_file.readlines())

    ROUNDS_MASTER_ERROR = False

except FileNotFoundError:
    with open(ROUNDS_PATH, 'w+', encoding="utf-8") as launch_file:
        file_len = len(launch_file.readlines())

    ROUNDS_MASTER_ERROR = False

if ROUNDS_MASTER_ERROR:
    print("ERROR while opening 'rounds.csv':")
    print("Please ensure file integrity or create it manually before continuing.")
    print("If continuing, no rounds will be recorded.")
    print("Software relaunch is required to record rounds again.")


class RunningGame():
    def __init__(self):
        self.rounds = []
        self.streaks = []
        self.game_start = 0

    def new_running_game(self):
        self.rounds = []
        self.streaks = []
        self.game_start = timeit.default_timer()

    def write_new_round(self, r_score, r_time):
        self.rounds.append((r_score, r_time))

    def record_streak(self, s_length):
        self.streaks.append(s_length)

    def record_game_rounds_to_file(self, game_mode):
        if len(self.rounds) > 0 and not ROUNDS_MASTER_ERROR:
            with open(ROUNDS_PATH, 'a+', newline='', encoding='utf-8') as round_file:
                writer = csv.writer(round_file, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(self.rounds)

            self.record_game_to_stats_file(game_mode)

    def record_game_to_stats_file(self, game_mode):
        if len(self.rounds) > 0 and not STATS_MASTER_ERROR:
            if game_mode == 0:
                game_mode = "Classic"

            elif game_mode == 1:
                game_mode = "Advanced"

            elif game_mode == 2:
                game_mode = "Time Trial"

            elif game_mode == 3:
                game_mode = "One Life"

            elif game_mode == 4:
                game_mode = "Free"

            game_time = round(timeit.default_timer() - self.game_start, 1)
            rounds_total = len(self.rounds)

            scores = []
            non_zero_scores = []
            times = []

            for i_round in self.rounds:
                scores.append(i_round[0])

                if i_round[0] > 0:
                    non_zero_scores.append(i_round[0])

                times.append(round(i_round[1], 2))

            if len(non_zero_scores) == 0:
                non_zero_scores = [0]

            avg_earned_score = round(sum(scores) / rounds_total, 1)
            streaks_total = len(self.streaks)

            if streaks_total > 0:
                average_streak = round(sum(self.streaks) / streaks_total, 1)

            else:
                average_streak = 0

            round_avg_time = round(sum(times) / rounds_total, 2)

            full_stats_row = [game_mode, game_time, rounds_total, sum(scores),
                              min(non_zero_scores, default='n/a'),
                              max(scores, default='n/a'), avg_earned_score,
                              streaks_total, min(self.streaks, default='n/a'),
                              max(self.streaks, default='n/a'),
                              average_streak, min(times, default='n/a'),
                              max(times, default='n/a'), round_avg_time]

            with open(STATS_PATH, 'a+', newline='', encoding='utf-8') as stats_file:
                writer = csv.writer(stats_file, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

                writer.writerow(full_stats_row)

    def print_round_file(self):
        print()

        if not ROUNDS_MASTER_ERROR:
            print("Contents of file 'rounds.csv':")

            with open(ROUNDS_PATH, 'r+', newline='', encoding='utf-8') as rounds_file:
                file_reader = csv.reader(
                    rounds_file, delimiter=' ', quotechar='|')

                for row in file_reader:
                    print(', '.join(row))

    def print_stats_file(self):
        # CSV File print algorithm from https://stackoverflow.com/a/52521862/16834984

        if not STATS_MASTER_ERROR:
            def pad_col(col, max_width):
                return col.ljust(max_width)

            print()
            print("!! WIDEN CONSOLE WINDOW AS MUCH AS POSSIBLE FOR PROPER VISIBILITY !!"
                  " THIS SHOULD BE JUST ONE LINE !!")
            print("Contents of file 'stats.csv':")

            with open(STATS_PATH, 'r+', newline='', encoding='utf-8') as stats_file:
                file_reader = csv.reader(
                    stats_file, delimiter=' ', quotechar='|')
                all_rows = [["mode", "time", "rnds", "scre", "loS", "hiS", "avS",
                             "srs", "shE", "loE", "avE", "fsT", "slT", "avT"]]

                for row in file_reader:
                    all_rows.append(row)

            max_col_width = [0] * len(all_rows[0])

            for row in all_rows:
                for idx, col in enumerate(row):
                    max_col_width[idx] = max(len(col), max_col_width[idx])

            for row in all_rows:
                to_print = ""

                for idx, col in enumerate(row):
                    to_print += pad_col(col, max_col_width[idx]) + " | "

                print("-"*len(to_print))
                print(to_print)

            legend = """
            LEGEND:
            mode = game mode
            time = total time
            rnds = total rounds
            scre = final score
            loS  = lowest earned score > 0
            hiS  = highest earned score
            avS  = average earned score
            srs  = total individual streaks
            shE  = shortest continuous streak
            loE  = longest continuous streak
            avE  = average streak length
            fsT  = fastest round (s)
            slT  = slowest round (s)
            avT  = average round time (s)
            """

            print(legend)

    # function to update stats for gui
    def stats_for_gui(self):
        return_list = []

        if not STATS_MASTER_ERROR:
            return_list = ["GAME STATISTICS"]

            with open(STATS_PATH, 'r+', newline='', encoding='utf-8') as stats_file:
                file_reader = csv.reader(
                    stats_file, delimiter=' ', quotechar='|')

                for row in file_reader:
                    return_list.append("")
                    return_list.append(row)

            return return_list

        return None


MASTER_RUNNING_GAME = RunningGame()

# to dodge circular imports, specific functions defined to run stats handler

# gui asks for stats


def update():
    return MASTER_RUNNING_GAME.stats_for_gui()

# master game handler calls these functions


def new_game():
    MASTER_RUNNING_GAME.new_running_game()


def write_round(round_score, round_time):
    MASTER_RUNNING_GAME.write_new_round(round_score, round_time)


def write_game(game_mode: int):
    MASTER_RUNNING_GAME.record_game_rounds_to_file(game_mode)


def write_streak(length: int):
    MASTER_RUNNING_GAME.record_streak(length)

# user can call these functions from gui (debug options)


def rounds_console_print():
    MASTER_RUNNING_GAME.print_round_file()


def stats_console_print():
    MASTER_RUNNING_GAME.print_stats_file()

# user has option to erase all file contents and reset rounds & stats


def clear_stats_and_rounds():
    if ROUNDS_MASTER_ERROR and STATS_MASTER_ERROR:
        print("Software is unable to erase any recorded rounds",
              f" or statistics as neither '{ROUNDS_PATH}' or",
              f" '{STATS_PATH}' can be located.")

        return

    if not ROUNDS_MASTER_ERROR:
        with open(ROUNDS_PATH, 'w+', newline='', encoding='utf-8'):
            print("Deleting all recorded rounds...")

    else:
        print("Recorded rounds cannot be erased from file",
              " as software is unable to locate 'rounds.csv'.")

    if not STATS_MASTER_ERROR:
        with open(STATS_PATH, 'w+', newline='', encoding='utf-8'):
            print("Deleting all recorded statistics...")

    else:
        print("Recorded statistics cannot be erased from file",
              " as software is unable to locate 'stats.csv'.")

    print("Closing program...")

    exit(1) # pylint: disable=consider-using-sys-exit
    