import csv
from os import getcwd
import timeit
import statscalc

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

        full_stats_row = [game_mode, game_time, rounds_total, sum(scores),
                          min(non_zero_scores, default='n/a'),
                          max(non_zero_scores, default='n/a'), avg_earned_score,
                          streaks_total, min(self.streaks, default='n/a'),
                          max(self.streaks, default='n/a'),
                          average_streak, min(times, default='n/a'),
                          max(times, default='n/a'), round(sum(times) / rounds_total, 2)]

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

        return statscalc.calculate_true_statistics(all_games, all_streaks)

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

    def stats_formatting(self, shorter: bool):
        """
        format the stats.csv to look nice

        THIS ALGORITHM IS CREATED BY STACKOVERFLOW USER
        Matt Messersmith https://stackoverflow.com/a/52521862/

        Args:
            shorter (bool): select True if going to GUI

        Returns:
            list: individual lines bundled into one list
        """

        formatted_text = []

        def pad_col(col, max_width):
            return col.ljust(max_width)

        if shorter:
            all_prints = [["M", "tme", "rns", "scr", "hiS", "avS",
                           "srs", "loE", "avE", "fsT", "avT"]]

            content = self.read_stats(False)

            for row in content:
                del row[4]
                del row[7]
                del row[10]

                row[0] = row[0][0].upper()

                all_prints.extend([row])

        else:
            all_prints = [["mde", "tme", "rns", "scr", "loS", "hiS", "avS",
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

            formatted_text.append("-"*len(to_print))
            formatted_text.append(to_print)

        if shorter:
            legend = """
            LEGEND:
            M   = game mode
            tme = total time
            rns = total rounds
            scr = final score
            hiS = highest earned score
            avS = average earned score
            srs = total individual streaks
            loE = longest continuous streak
            avE = average streak length
            fsT = fastest round (s)
            avT = average round time (s)

            SEE EXTENDED TABLE:
            Debug > Print to console... > Recorded Games.
            """

        else:
            legend = """
            LEGEND:
            mde = game mode
            tme = total time
            rns = total rounds
            scr = final score
            loS = lowest earned score > 0
            hiS = highest earned score
            avS = average earned score
            srs = total individual streaks
            shE = shortest continuous streak
            loE = longest continuous streak
            avE = average streak length
            fsT = fastest round (s)
            slT = slowest round (s)
            avT = average round time (s)
            """

        formatted_text.append(legend)

        return formatted_text

    def print_stats(self):
        """
        print the games to console (contents of stats.csv)
        """

        print()
        print("!! WIDEN CONSOLE WINDOW AS MUCH AS POSSIBLE FOR PROPER VISIBILITY !!"
              " THIS SHOULD BE JUST ONE LINE !!")
        print()
        print("Contents of file 'stats.csv':")

        content = self.stats_formatting(False)

        for row in content:
            print(row)

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
