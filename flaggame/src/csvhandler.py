# MODULE DESCRIPTION

# csvhandler is responsible for the game statistics handling

# it reads and writes the csv files and manages (calculates) stats in general

import csv            # module to read & write .csv files
from os import getcwd  # getcwd informs current working directory
import timeit         # record game start event to determine total play time

# determine directory for the statistics files
WORKING_DIR = getcwd()

# (during developing, handle main.py & poetry run invoke starts)
if WORKING_DIR[-3:] != "src":
    WORKING_DIR = WORKING_DIR + "/src"

STATS_PATH = WORKING_DIR + '/logs/stats.csv'
ROUNDS_PATH = WORKING_DIR + '/logs/rounds.csv'
STREAKS_PATH = WORKING_DIR + '/logs/streaks.csv'

STATS_MASTER_ERROR = True
ROUNDS_MASTER_ERROR = True
STREAKS_MASTER_ERROR = True

print("Opening (creating if it doesn't exist) the game stats file 'stats.csv'...")

# check the main statistics file (recorded games)
try:
    with open(STATS_PATH, 'r+', encoding="utf-8") as launch_file:
        file_len = len(launch_file.readlines())

    STATS_MASTER_ERROR = False

except FileNotFoundError:
    with open(STATS_PATH, 'w+', newline='', encoding="utf-8") as launch_file:
        file_len = len(launch_file.readlines())

    STATS_MASTER_ERROR = False

if STATS_MASTER_ERROR:
    print("ERROR while opening 'stats.csv':")
    print("Please ensure file integrity or create it manually before continuing.")
    print("If continuing, no stats will be recorded.")
    print("Software relaunch is required to record stats again.")

print("Opening (creating if it doesn't exist) the game rounds file 'rounds.csv'...")

# check rounds file
try:
    with open(ROUNDS_PATH, 'r+', encoding="utf-8") as launch_file:
        file_len = len(launch_file.readlines())

    ROUNDS_MASTER_ERROR = False

except FileNotFoundError:
    with open(ROUNDS_PATH, 'w+', newline='', encoding="utf-8") as launch_file:
        file_len = len(launch_file.readlines())

    ROUNDS_MASTER_ERROR = False

if ROUNDS_MASTER_ERROR:
    print("ERROR while opening 'rounds.csv':")
    print("Please ensure file integrity or create it manually before continuing.")
    print("If continuing, no rounds will be recorded.")
    print("Software relaunch is required to record rounds again.")

print("Opening (creating if it doesn't exist) the streaks rounds file 'streaks.csv'...")

# check streaks file
try:
    with open(STREAKS_PATH, 'r+', encoding="utf-8") as launch_file:
        file_len = len(launch_file.readlines())

    STREAKS_MASTER_ERROR = False

except FileNotFoundError:
    with open(STREAKS_PATH, 'w+', newline='', encoding="utf-8") as launch_file:
        file_len = len(launch_file.readlines())

    STREAKS_MASTER_ERROR = False

if STREAKS_MASTER_ERROR:
    print("ERROR while opening 'streajs.csv':")
    print("Please ensure file integrity or create it manually before continuing.")
    print("If continuing, no streaks will be recorded.")
    print("Software relaunch is required to record rounds again.")

# RunningGame class is responsible for recording all played rounds & games
# It calculates all statistics and returns them to gui


class RunningGame():
    def __init__(self):
        self.rounds = []
        self.streaks = []
        self.game_start = 0

    # new game is launched, reset all variables
    def launch_new_game(self):
        self.rounds = []
        self.streaks = []
        self.game_start = timeit.default_timer()

    # player finished a round, append it to memory
    def write_new_round(self, r_score, r_time):
        self.rounds.append((r_score, r_time))

    # a streak just ended, append it to memory
    def write_new_streak(self, s_length: int):
        self.streaks.append(s_length)

    # a game just ended, write all rounds to file
    def write_game_rounds_to_file(self, game_mode):
        if len(self.rounds) > 0 and not ROUNDS_MASTER_ERROR:
            with open(ROUNDS_PATH, 'a+', newline='', encoding='utf-8') as round_file:
                writer = csv.writer(round_file, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(self.rounds)

                self.write_game_stats_to_file(game_mode)

    # a game just ended, write the game to file
    def write_game_stats_to_file(self, game_mode):
        if len(self.rounds) > 0 and not STATS_MASTER_ERROR:
            # check game mode
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

            # determine game time, total rounds, individual round scores, etc.
            game_time = round(timeit.default_timer() - self.game_start, 1)
            rounds_total = len(self.rounds)

            scores = []
            non_zero_scores = []
            times = []

            # logic to calculate all remaining statistics about the finished game
            for i_round in self.rounds:
                scores.append(i_round[0])

                if i_round[0] > 0:
                    non_zero_scores.append(i_round[0])

                times.append(round(i_round[1], 2))

            if len(non_zero_scores) > 0:
                avg_earned_score = round(
                    sum(non_zero_scores) / len(non_zero_scores), 1)

            else:
                avg_earned_score = "n/a"

            streaks_total = len(self.streaks)

            if streaks_total > 0:
                average_streak = round(sum(self.streaks) / streaks_total, 1)

            else:
                average_streak = "n/a"

            round_avg_time = round(sum(times) / rounds_total, 2)

            # data structure where everything is finally stored
            full_stats_row = [game_mode, game_time, rounds_total, sum(scores),
                              min(non_zero_scores, default='n/a'),
                              max(non_zero_scores, default='n/a'), avg_earned_score,
                              streaks_total, min(self.streaks, default='n/a'),
                              max(self.streaks, default='n/a'),
                              average_streak, min(times, default='n/a'),
                              max(times, default='n/a'), round_avg_time]

            # write the list determined above to file
            with open(STATS_PATH, 'a+', newline='', encoding='utf-8') as stats_file:
                writer = csv.writer(stats_file, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

                writer.writerow(full_stats_row)

            # write the streaks to file
            with open(STREAKS_PATH, 'a+', newline='', encoding='utf-8') as streaks_file:
                writer = csv.writer(streaks_file, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

                self.streaks.insert(0, game_mode)

                writer.writerow(self.streaks)

    # define a general function to read the stats file (individual games)
    def read_stats(self, ignore: bool):
        if not STATS_MASTER_ERROR:
            with open(STATS_PATH, 'r+', encoding='utf-8') as stats_file:
                file_reader = csv.reader(
                    stats_file, delimiter=' ', quotechar='|')
                all_rows = []

                for row in file_reader:
                    # don't append free games if ignore is enabled
                    if row[0] != "Free":
                        all_rows.append(row)

                    elif not ignore:
                        all_rows.append(row)

            return all_rows

        return []

    # define a general function to read the streaks file
    def read_streaks(self, ignore: bool):
        if not STREAKS_MASTER_ERROR:
            with open(STREAKS_PATH, 'r+', encoding='utf-8') as streaks_file:
                file_reader = csv.reader(
                    streaks_file, delimiter=' ', quotechar='|')
                all_rows = []

                for row in file_reader:
                    # don't append free games if ignore is enabled
                    if row[0] != "Free":
                        all_rows.append([int(i) for i in row[1:]])

                    elif not ignore:
                        all_rows.append([int(i) for i in row[1:]])

            return all_rows

        return []

    # function to calculate the PLAYER LIFELONG STATISTICS
    def calculate_true_stats(self, free_boolean):
        if not STATS_MASTER_ERROR:
            # fetch all games from file (ignore free games if needed)
            all_games = self.read_stats(free_boolean)
            all_streaks = self.read_streaks(free_boolean)

            # player dictionary is used to store all data
            player = {'total_games': 0, 'total_playtime': 0,
                      'total_rounds': 0, 'total_score': 0,
                      'total_streaks': 0, 'best_game_score': 0,
                      'worst_game_score': float('inf'), 'average_game_score': 'N/A',
                      'average_score_per_second': 'N/A', 'most_rounds_in_a_game': 0,
                      'least_rounds_in_a_game': float('inf'), 'average_rounds_in_a_game': 'N/A',
                      'shortest_game_duration': float('inf'), 'longest_game_duration': 0.0,
                      'average_game_duration': 'N/A', 'longest_streak': 0,
                      'shortest_streak': float('inf'), 'average_streak': 0,
                      'average_round_score': 'N/A', 'average_round_time': 'N/A'}

            # run through every game
            for game in all_games:
                player['total_games'] += 1
                player['total_playtime'] += float(game[1])
                player['total_rounds'] += int(game[2])
                player['total_score'] += int(game[3])
                player['total_streaks'] += int(game[7])

                if game[10] != 'n/a':
                    player['average_streak'] += float(game[10])

                if float(game[1]) > player['longest_game_duration']:
                    player['longest_game_duration'] = float(game[1])

                if float(game[1]) < player['shortest_game_duration']:
                    player['shortest_game_duration'] = float(game[1])

                if int(game[2]) > player['most_rounds_in_a_game']:
                    player['most_rounds_in_a_game'] = int(game[2])

                if int(game[2]) < player['least_rounds_in_a_game']:
                    player['least_rounds_in_a_game'] = int(game[2])

                if int(game[3]) > player['best_game_score']:
                    player['best_game_score'] = int(game[3])

                if int(game[3]) < player['worst_game_score']:
                    player['worst_game_score'] = int(game[3])

                if game[9] != 'n/a':
                    if int(game[9]) > player['longest_streak']:
                        player['longest_streak'] = int(game[9])

                if game[8] != 'n/a':
                    if int(game[8]) < player['shortest_streak']:
                        player['shortest_streak'] = int(game[8])

            # calculate averages
            if player['total_games'] > 0:
                player['average_game_score'] = round(
                    player['total_score'] / player['total_games'])

            if player['total_playtime'] > 0:
                player['average_score_per_second'] = round(
                    player['total_score'] / player['total_playtime'], 1)

            if player['total_games'] > 0:
                player['average_rounds_in_a_game'] = round(
                    player['total_rounds'] / player['total_games'])

            if player['total_games'] > 0:
                player['average_game_duration'] = round(
                    player['total_playtime'] / player['total_games'], 1)

            if player['total_rounds'] > 0:
                player['average_round_score'] = round(
                    player['total_score'] / player['total_rounds'])

            if player['total_rounds'] > 0:
                player['average_round_time'] = round(
                    player['total_playtime'] / player['total_rounds'], 1)

            streak_sum = 0

            for streaks in all_streaks:
                streak_sum += sum(streaks)

            if player['total_streaks'] > 0:
                player['average_streak'] = round(
                    streak_sum / player['total_streaks'], 1)

            # apply some formatting (units)
            player['total_playtime'] = str(
                round(player['total_playtime'] / 60, 1)) + "min"
            player['longest_game_duration'] = str(
                player['longest_game_duration']) + "s"
            player['shortest_game_duration'] = str(
                player['shortest_game_duration']) + "s"
            player['average_game_duration'] = str(
                player['average_game_duration']) + "s"
            player['average_round_time'] = str(
                player['average_round_time']) + "s"

            return player

        return None

    # debug option to print all played rounds to console
    def print_round_file(self):
        print()

        if not ROUNDS_MASTER_ERROR:
            print("Contents of file 'rounds.csv':")

            with open(ROUNDS_PATH, 'r+', encoding='utf-8') as rounds_file:
                file_reader = csv.reader(
                    rounds_file, delimiter=' ', quotechar='|')

                for i, row in enumerate(file_reader):
                    print("row", i)
                    print(', '.join(row))

    # debug option to print all streaks to console
    def print_streak_file(self):
        print()

        if not ROUNDS_MASTER_ERROR:
            print("Contents of file 'streaks.csv':")

            with open(STREAKS_PATH, 'r+', encoding='utf-8') as streaks_file:
                file_reader = csv.reader(
                    streaks_file, delimiter=' ', quotechar='|')

                for i, row in enumerate(file_reader):
                    print("row", i)
                    print(', '.join(row))

    # debug option to print statistics file (games)
    def print_stats_file(self):
        if not STATS_MASTER_ERROR:
            # THIS PRINTING ALGORITHM IS CREATED BY STACKOVERFLOW USER
            # Matt Messersmith https://stackoverflow.com/a/52521862/

            def pad_col(col, max_width):
                return col.ljust(max_width)

            print()
            print("!! WIDEN CONSOLE WINDOW AS MUCH AS POSSIBLE FOR PROPER VISIBILITY !!"
                  " THIS SHOULD BE JUST ONE LINE !!")
            print("Contents of file 'stats.csv':")

            all_prints = [["mode", "time", "rnds", "scre", "loS", "hiS", "avS",
                           "srs", "shE", "loE", "avE", "fsT", "slT", "avT"]]
            all_prints.extend(self.read_stats(False))

            max_col_width = [0] * len(all_prints[0])

            for row in all_prints:
                for idx, col in enumerate(row):
                    max_col_width[idx] = max(len(col), max_col_width[idx])

            for row in all_prints:
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


# create a new instance
MASTER_RUNNING_GAME = RunningGame()

# user has option to erase all file contents and reset rounds & stats


def clear_stats_and_rounds():
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

    if not STREAKS_MASTER_ERROR:
        with open(STREAKS_PATH, 'w+', newline='', encoding='utf-8'):
            print("Deleting all recorded streaks...")

    else:
        print("Recorded streaks cannot be erased from file",
              " as software is unable to locate 'streaks.csv'.")

    print("Closing program...")

    exit(1)  # pylint: disable=consider-using-sys-exit
    # no reason to import sys library for this one exit call
