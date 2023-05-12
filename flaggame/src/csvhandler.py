import csv
from os import getcwd
import timeit
from stats import stats_calc, game_calc

WORKING_DIR = getcwd()

if WORKING_DIR[-3:] != "src":
    WORKING_DIR = WORKING_DIR + "/src"

STATS_PATH = WORKING_DIR + '/logs/stats.csv'
ROUNDS_PATH = WORKING_DIR + '/logs/rounds.csv'
STREAKS_PATH = WORKING_DIR + '/logs/streaks.csv'


class MasterStatsHandler():
    """
    manage all statistics recording and other general handling,
    calculates the statistics, writes to file, and returns data to gui elements
    """

    def __init__(self, stats_path, rounds_path, streaks_path):
        """
        initialize variables to record both rounds and streaks
        """

        self.stats_path = stats_path
        self.rounds_path = rounds_path
        self.streaks_path = streaks_path
        self.rounds = []
        self.streaks = []
        self.game_start = 0

        self.check_or_create_files()

    def check_or_create_files(self):
        """
        check the integrity of the statistics files, create new ones if missing
        """

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

    def launch_new_game(self):
        """
        reset variables for a new game
        """

        self.rounds = []
        self.streaks = []
        self.game_start = timeit.default_timer()

    def record_new_round(self, r_score: int, r_time: float):
        """
        every single round is recorded & timed

        Args:
            r_score (int): score earned
            r_time (float): time elapsed
        """

        self.rounds.append((r_score, r_time))

    def record_new_streak(self, s_length: int):
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

        game_time = round(timeit.default_timer() - self.game_start, 1)

        full_stats_row = game_calc.calculate_game_statistics(
            game_mode, self.rounds, self.streaks, game_time)

        with open(self.stats_path, 'a+', newline='', encoding='utf-8') as stats_file:
            writer = csv.writer(stats_file, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

            writer.writerow(full_stats_row)

        with open(self.streaks_path, 'a+', newline='', encoding='utf-8') as streaks_file:
            writer = csv.writer(streaks_file, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

            self.streaks.insert(0, game_mode)

            writer.writerow(self.streaks)

    def read_stats_file(self, ignore_free: bool):
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

    def read_streaks_file(self, ignore_free: bool):
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

        all_games = self.read_stats_file(ignore_free)
        all_streaks = self.read_streaks_file(ignore_free)

        return stats_calc.calculate_true_statistics(all_games, all_streaks)

    def print_rounds_file(self):
        """
        print the rounds.csv file to console
        """

        print("\nContents of file 'rounds.csv':")

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

        print("\nContents of file 'streaks.csv':")

        with open(self.streaks_path, 'r+', encoding='utf-8') as streaks_file:
            file_reader = csv.reader(
                streaks_file, delimiter=' ', quotechar='|')

            for i, row in enumerate(file_reader):
                print("row", i)
                print(', '.join(row))

    def print_stats(self):
        """
        print the games to console (contents of stats.csv)
        """

        print("\n!! WIDEN CONSOLE WINDOW AS MUCH AS POSSIBLE FOR PROPER VISIBILITY !!"
              " THIS SHOULD BE JUST ONE LINE !!\n")
        print("Contents of file 'stats.csv':")

        content = self.stats_formatting(False)

        for row in content:
            print(row)

    def shorter_stats_formatting(self):
        """
        create a shorter version of the games list for gui

        Returns:
            list: list of lists containing every game with some stats removed
        """

        all_prints = [["M", "tme", "rns", "scr", "hiS", "avS",
                       "srs", "loE", "avE", "fsT", "avT"]]

        content = self.read_stats_file(False)

        for row in content:
            unwanted = [4, 8, 12]

            for ele in sorted(unwanted, reverse=True):
                del row[ele]

            row[0] = row[0][0].upper()

            all_prints.extend([row])

        return all_prints

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
            all_prints = self.shorter_stats_formatting()

        else:
            all_prints = [["mde", "tme", "rns", "scr", "loS", "hiS", "avS",
                           "srs", "shE", "loE", "avE", "fsT", "slT", "avT"]]

            all_prints.extend(self.read_stats_file(False))

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

    def clear_stats_and_rounds(self):
        """
        remove any recorded rounds, streaks, and games
        exit the software
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
