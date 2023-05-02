import csv
from os import getcwd
import timeit

WORKING_DIR = getcwd()

if WORKING_DIR[-3:] != "src":
    WORKING_DIR = WORKING_DIR + "/src"

STATS_PATH = WORKING_DIR + '/logs/stats.csv'
ROUNDS_PATH = WORKING_DIR + '/logs/rounds.csv'
STREAKS_PATH = WORKING_DIR + '/logs/streaks.csv'


class MasterStatsHandler():
    """
    manage all statistics recording and other general handling
    it calculates the statistics, writes to file, and returns data to gui elements
    """

    def __init__(self, stats_path, rounds_path, streaks_path):
        """
        initialize variables to record both rounds and streaks
        """

        self.stats_path = stats_path
        self.rounds_path = rounds_path
        self.streaks_path = streaks_path

        print("Opening (creating if it doesn't exist) the game stats file 'stats.csv'...")

        try:
            with open(self.stats_path, 'r+', encoding="utf-8") as _:
                pass

        except FileNotFoundError:
            with open(self.stats_path, 'w+', newline='', encoding="utf-8") as _:
                pass

        try:
            with open(self.rounds_path, 'r+', encoding="utf-8") as _:
                pass

        except FileNotFoundError:
            with open(self.rounds_path, 'w+', newline='', encoding="utf-8") as _:
                pass

        try:
            with open(self.streaks_path, 'r+', encoding="utf-8") as _:
                pass

        except FileNotFoundError:
            with open(self.streaks_path, 'w+', newline='', encoding="utf-8") as _:
                pass

        self.rounds = []
        self.streaks = []
        self.game_start = 0

    def launch_new_game(self):
        """
        reset variables for a new game
        """

        self.rounds = []
        self.streaks = []
        self.game_start = timeit.default_timer()

    def write_new_round(self, r_score: int, r_time: float):
        """
        every single round is recorded & timed

        Args:
            r_score (int): score earned
            r_time (float): time elapsed
        """

        self.rounds.append((r_score, r_time))

    def write_new_streak(self, s_length: int):
        """
        streak length recorded each time it ends (or when game is terminated)

        Args:
            s_length (int): streak length
        """

        self.streaks.append(s_length)

    def write_game_rounds_to_file(self, game_mode: int):
        """
        game over (or cancelled), all recorded rounds are written to file

        Args:
            game_mode (int): game mode as an integer
        """

        if len(self.rounds) > 0:
            with open(self.rounds_path, 'a+', newline='', encoding='utf-8') as round_file:
                writer = csv.writer(round_file, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(self.rounds)

                self.write_game_stats_to_file(game_mode)

    def write_game_stats_to_file(self, game_mode: int):
        """
        game over (or cancelled), all game statistics are calculated and then written to file

        Args:
            game_mode (int): game mode as an integer
        """

        if game_mode == 0:
            game_mode = "Classic"

        elif game_mode == 1:
            game_mode = "Advanced"

        elif game_mode == 2:
            game_mode = "Time Trial"

        elif game_mode == 3:
            game_mode = "One Life"

        else:
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

        full_stats_row = [game_mode, game_time, rounds_total, sum(scores),
                          min(non_zero_scores, default='n/a'),
                          max(non_zero_scores, default='n/a'), avg_earned_score,
                          streaks_total, min(self.streaks, default='n/a'),
                          max(self.streaks, default='n/a'),
                          average_streak, min(times, default='n/a'),
                          max(times, default='n/a'), round_avg_time]

        with open(self.stats_path, 'a+', newline='', encoding='utf-8') as stats_file:
            writer = csv.writer(stats_file, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

            writer.writerow(full_stats_row)

        with open(self.streaks_path, 'a+', newline='', encoding='utf-8') as streaks_file:
            writer = csv.writer(streaks_file, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

            self.streaks.insert(0, game_mode)

            writer.writerow(self.streaks)

    def read_stats(self, ignore_free: bool):
        """
        read the statistics file stats.csv (games)

        Args:
            ignore_free (bool): include free mode games or not

        Returns:
            list: returns a list of lists containing all the recorded games
            [[game 1], [game 2], ...]
        """

        with open(self.stats_path, 'r+', encoding='utf-8') as stats_file:
            file_reader = csv.reader(
                stats_file, delimiter=' ', quotechar='|')
            all_rows = []

            for row in file_reader:
                if row[0] != "Free":
                    all_rows.append(row)

                elif not ignore_free:
                    all_rows.append(row)

        return all_rows

    def read_streaks(self, ignore_free: bool):
        """
        read the streaks file

        Args:
            ignore_free (bool): include free mode games or not

        Returns:
            list: returns a list of lists containing all recorded streaks by game
            [[game 1 streaks], [game 2 streaks], ...]
        """

        with open(self.streaks_path, 'r+', encoding='utf-8') as streaks_file:
            file_reader = csv.reader(
                streaks_file, delimiter=' ', quotechar='|')
            all_rows = []

            for row in file_reader:
                if row[0] != "Free":
                    all_rows.append([int(i) for i in row[1:]])

                elif not ignore_free:
                    all_rows.append([int(i) for i in row[1:]])

        return all_rows

    def calculate_true_stats(self, ignore_free: bool):
        """
        calculate the true player lifelong statistics

        Args:
            ignore_free (bool): include free mode games or not

        Returns:
            dict: returns a dictionary containing (key, value) pairs of all recorded statistics
            {'total_games': 4, 'total_playtime': 3.2min, ...}
        """

        all_games = self.read_stats(ignore_free)
        all_streaks = self.read_streaks(ignore_free)

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

    def print_round_file(self):
        """
        print the rounds.csv file to console
        """

        print()

        print("Contents of file 'rounds.csv':")

        with open(self.rounds_path, 'r+', encoding='utf-8') as rounds_file:
            file_reader = csv.reader(
                rounds_file, delimiter=' ', quotechar='|')

            for i, row in enumerate(file_reader):
                print("row", i)
                print(', '.join(row))

    def print_streaks_file(self):
        """
        print the streaks.csv file to console
        """

        print()

        print("Contents of file 'streaks.csv':")

        with open(self.streaks_path, 'r+', encoding='utf-8') as streaks_file:
            file_reader = csv.reader(
                streaks_file, delimiter=' ', quotechar='|')

            for i, row in enumerate(file_reader):
                print("row", i)
                print(', '.join(row))

    def print_stats(self):
        """
        print the games to console (contents of stats.csv)

        THIS PRINTING ALGORITHM IS CREATED BY STACKOVERFLOW USER
        Matt Messersmith https://stackoverflow.com/a/52521862/
        """

        def pad_col(col, max_width):
            return col.ljust(max_width)

        print()
        print("!! WIDEN CONSOLE WINDOW AS MUCH AS POSSIBLE FOR PROPER VISIBILITY !!"
              " THIS SHOULD BE JUST ONE LINE !!")
        print()
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

    def clear_stats_and_rounds(self):
        """
        remove any recorded rounds, streaks, and games
        exits the software
        """

        with open(self.rounds_path, 'w+', newline='', encoding='utf-8'):
            print("Deleting all recorded rounds...")

        with open(self.stats_path, 'w+', newline='', encoding='utf-8'):
            print("Deleting all recorded statistics...")

        with open(self.streaks_path, 'w+', newline='', encoding='utf-8'):
            print("Deleting all recorded streaks...")

        print("Closing program...")

        exit(1)  # pylint: disable=consider-using-sys-exit


MASTER_RUNNING_GAME = MasterStatsHandler(STATS_PATH, ROUNDS_PATH, STREAKS_PATH)
