import unittest
import pytest
import csvhandler
from unittest.mock import patch
import builtins
import time


class TestStatsHandler(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def _pass_fixtures(self, tmpdir, capsys):
        self.tmpdir = tmpdir
        self.capsys = capsys
        self.maxDiff = None

    def test_write_to_empty_files(self):
        """
        test if writing to empty files works
        """

        tmp_stats_file = self.tmpdir.join('stats.csv')
        tmp_rounds_file = self.tmpdir.join('rounds.csv')
        tmp_streaks_file = self.tmpdir.join('streaks.csv')

        with open(tmp_stats_file, 'w+') as f:
            pass

        with open(tmp_rounds_file, 'w+') as f:
            pass

        with open(tmp_streaks_file, 'w+') as f:
            pass

        new_stats_handler = csvhandler.MasterStatsHandler(
            str(tmp_stats_file), str(tmp_rounds_file), str(tmp_streaks_file))

        new_stats_handler.print_rounds_file()
        captured = self.capsys.readouterr()
        self.assertEqual(2, len(captured))

        new_stats_handler.print_streaks_file()
        captured = self.capsys.readouterr()
        self.assertEqual(2, len(captured))

        new_stats_handler.print_stats()
        captured = self.capsys.readouterr()
        self.assertEqual(2, len(captured))

    def test_create_empty_files(self):
        """
        test to create new files if no files are found
        """

        new_stats_handler = csvhandler.MasterStatsHandler(str(self.tmpdir.join('stats_wrong.csv')), str(
            self.tmpdir.join('rounds_wrong.csv')), str(self.tmpdir.join('streaks_wrong.csv')))

        new_stats_handler.print_rounds_file()
        captured = self.capsys.readouterr()
        self.assertEqual(2, len(captured))

        new_stats_handler.print_streaks_file()
        captured = self.capsys.readouterr()
        self.assertEqual(2, len(captured))

        new_stats_handler.print_stats()
        captured = self.capsys.readouterr()
        self.assertEqual(2, len(captured))

    def test_clear_stats(self):
        """
        test clearing the stats
        """

        tmp_stats_file = self.tmpdir.join('stats.csv')
        tmp_rounds_file = self.tmpdir.join('rounds.csv')
        tmp_streaks_file = self.tmpdir.join('streaks.csv')

        with open(tmp_stats_file, 'w+') as f:
            f.write('some data')

        with open(tmp_rounds_file, 'w+') as f:
            f.write('some data')

        with open(tmp_streaks_file, 'w+') as f:
            f.write('some data')

        new_stats_handler = csvhandler.MasterStatsHandler(
            str(tmp_stats_file), str(tmp_rounds_file), str(tmp_streaks_file))

        with patch.object(builtins, 'exit') as mock_exit:
            new_stats_handler.clear_stats_and_rounds()
            mock_exit.assert_called()

        with open(tmp_stats_file, 'r') as f:
            contents = f.read()
            self.assertEqual(contents, '')

        with open(tmp_rounds_file, 'r') as f:
            contents = f.read()
            self.assertEqual(contents, '')

        with open(tmp_streaks_file, 'r') as f:
            contents = f.read()
            self.assertEqual(contents, '')

    def test_failsafes(self):
        """
        test what happens if game record is requested with no stats
        """

        tmp_stats_file = self.tmpdir.join('stats.csv')
        tmp_rounds_file = self.tmpdir.join('rounds.csv')
        tmp_streaks_file = self.tmpdir.join('streaks.csv')

        with open(tmp_stats_file, 'w+') as f:
            pass

        with open(tmp_rounds_file, 'w+') as f:
            pass

        with open(tmp_streaks_file, 'w+') as f:
            pass

        new_stats_handler = csvhandler.MasterStatsHandler(
            str(tmp_stats_file), str(tmp_rounds_file), str(tmp_streaks_file))

        new_stats_handler.launch_new_game()
        new_stats_handler.write_game_rounds_to_file(0)

        answer = new_stats_handler.read_streaks_file(False)
        self.assertEqual(0, len(answer))

        answer = new_stats_handler.read_stats_file(False)
        self.assertEqual(0, len(answer))

    def test_game_recording(self):
        """
        test the actual game statistics recording sequence
        """

        tmp_stats_file = self.tmpdir.join('stats.csv')
        tmp_rounds_file = self.tmpdir.join('rounds.csv')
        tmp_streaks_file = self.tmpdir.join('streaks.csv')

        with open(tmp_stats_file, 'w+') as f:
            pass

        with open(tmp_rounds_file, 'w+') as f:
            pass

        with open(tmp_streaks_file, 'w+') as f:
            pass

        new_stats_handler = csvhandler.MasterStatsHandler(
            str(tmp_stats_file), str(tmp_rounds_file), str(tmp_streaks_file))

        new_stats_handler.launch_new_game()
        new_stats_handler.record_new_round(100, 1.5)
        new_stats_handler.record_new_round(100, 7.0)
        new_stats_handler.record_new_round(100, 3.25)
        new_stats_handler.record_new_round(100, 2.75)
        new_stats_handler.record_new_round(0, 3.5)
        new_stats_handler.record_new_streak(4)
        new_stats_handler.record_new_round(100, 5.75)
        new_stats_handler.record_new_round(0, 0.5)
        new_stats_handler.record_new_streak(1)
        new_stats_handler.record_new_round(0, 6.25)
        new_stats_handler.write_game_rounds_to_file(0)

        answer = new_stats_handler.read_streaks_file(False)
        self.assertEqual(1, len(answer))
        self.assertEqual(2, len(answer[0]))

        answer = new_stats_handler.read_stats_file(False)
        self.assertEqual(1, len(answer))
        self.assertEqual(14, len(answer[0]))

        new_stats_handler.launch_new_game()
        new_stats_handler.record_new_round(176, 1.1)
        new_stats_handler.record_new_round(182, 2.1)
        new_stats_handler.record_new_round(135, 4.75)
        new_stats_handler.record_new_round(198, 0.25)
        new_stats_handler.record_new_round(0, 3.5)
        new_stats_handler.record_new_streak(4)
        new_stats_handler.write_game_rounds_to_file(1)

        answer = new_stats_handler.read_streaks_file(False)
        self.assertEqual(2, len(answer))
        self.assertEqual(1, len(answer[1]))

        answer = new_stats_handler.read_stats_file(False)
        self.assertEqual(2, len(answer))
        self.assertEqual(14, len(answer[1]))

    def test_free_mode_ignore(self):
        """
        test how the free games ignore functionality works
        """

        tmp_stats_file = self.tmpdir.join('stats.csv')
        tmp_rounds_file = self.tmpdir.join('rounds.csv')
        tmp_streaks_file = self.tmpdir.join('streaks.csv')

        with open(tmp_stats_file, 'w+') as f:
            pass

        with open(tmp_rounds_file, 'w+') as f:
            pass

        with open(tmp_streaks_file, 'w+') as f:
            pass

        new_stats_handler = csvhandler.MasterStatsHandler(
            str(tmp_stats_file), str(tmp_rounds_file), str(tmp_streaks_file))

        new_stats_handler.launch_new_game()
        new_stats_handler.record_new_round(100, 1.5)
        new_stats_handler.record_new_round(100, 7.0)
        new_stats_handler.record_new_round(100, 3.25)
        new_stats_handler.record_new_round(100, 2.75)
        new_stats_handler.record_new_round(0, 3.5)
        new_stats_handler.record_new_streak(4)
        new_stats_handler.record_new_round(100, 5.75)
        new_stats_handler.record_new_round(0, 0.5)
        new_stats_handler.record_new_streak(1)
        new_stats_handler.record_new_round(0, 6.25)
        new_stats_handler.write_game_rounds_to_file(4)

        answer = new_stats_handler.read_streaks_file(True)
        self.assertEqual(1, len(answer))

        answer = new_stats_handler.read_stats_file(True)
        self.assertEqual(0, len(answer))

        answer = new_stats_handler.read_streaks_file(False)
        self.assertEqual(1, len(answer))
        self.assertEqual(2, len(answer[0]))

        answer = new_stats_handler.read_stats_file(False)
        self.assertEqual(1, len(answer))
        self.assertEqual(14, len(answer[0]))

    def test_calculate_true_stats(self):
        """
        test calculating the complete player lifelong statistics
        """

        tmp_stats_file = self.tmpdir.join('stats.csv')
        tmp_rounds_file = self.tmpdir.join('rounds.csv')
        tmp_streaks_file = self.tmpdir.join('streaks.csv')

        with open(tmp_stats_file, 'w+') as f:
            pass

        with open(tmp_rounds_file, 'w+') as f:
            pass

        with open(tmp_streaks_file, 'w+') as f:
            pass

        new_stats_handler = csvhandler.MasterStatsHandler(
            str(tmp_stats_file), str(tmp_rounds_file), str(tmp_streaks_file))

        new_stats_handler.launch_new_game()
        time.sleep(6)
        new_stats_handler.record_new_round(175, 1.179)
        new_stats_handler.record_new_round(213, 1.4798)
        new_stats_handler.record_new_round(236, 1.4966)
        new_stats_handler.record_new_round(260, 0.755)
        new_stats_handler.record_new_round(269, 1.1812)
        new_stats_handler.record_new_round(279, 1.2924)
        new_stats_handler.record_new_round(254, 2.8456)
        new_stats_handler.record_new_round(252, 3.1058)
        new_stats_handler.record_new_round(292, 1.8773)
        new_stats_handler.record_new_round(0, 0.8571)
        new_stats_handler.record_new_streak(9)
        new_stats_handler.record_new_round(176, 1.1043)
        new_stats_handler.record_new_round(218, 0.8259)
        new_stats_handler.record_new_round(235, 1.5436)
        new_stats_handler.record_new_round(259, 0.9442)
        new_stats_handler.record_new_round(0, 2.0903)
        new_stats_handler.record_new_streak(4)
        new_stats_handler.record_new_round(169, 1.8166)
        new_stats_handler.record_new_round(213, 1.4055)
        new_stats_handler.record_new_round(0, 0.8333)
        new_stats_handler.record_new_streak(2)
        new_stats_handler.write_game_rounds_to_file(1)

        answer = new_stats_handler.calculate_true_stats(True)

        expected_answer = {'total_games': 1, 'total_playtime': '0.1min',
                           'total_rounds': 18, 'total_score': 3500,
                           'total_streaks': 3, 'best_game_score': 3500,
                           'worst_game_score': 3500, 'average_game_score': 3500,
                           'average_score_per_second': 583.3, 'most_rounds_in_a_game': 18,
                           'least_rounds_in_a_game': 18, 'average_rounds_in_a_game': 18,
                           'shortest_game_duration': '6.0s', 'longest_game_duration': '6.0s',
                           'average_game_duration': '6.0s', 'longest_streak': 9,
                           'shortest_streak': 2, 'average_streak': 5.0,
                           'average_round_score': 194, 'average_round_time': '0.3s'}

        self.assertAlmostEqual(expected_answer, answer, delta=0.2)

        new_stats_handler.print_rounds_file()
        captured = self.capsys.readouterr()
        self.assertEqual(2, len(captured))

        new_stats_handler.print_streaks_file()
        captured = self.capsys.readouterr()
        self.assertEqual(2, len(captured))

        new_stats_handler.print_stats()
        captured = self.capsys.readouterr()
        self.assertEqual(2, len(captured))

    def test_na_game(self):
        """
        test the zero division avoiding mechanisms
        """

        tmp_stats_file = self.tmpdir.join('stats.csv')
        tmp_rounds_file = self.tmpdir.join('rounds.csv')
        tmp_streaks_file = self.tmpdir.join('streaks.csv')

        with open(tmp_stats_file, 'w+') as f:
            pass

        with open(tmp_rounds_file, 'w+') as f:
            pass

        with open(tmp_streaks_file, 'w+') as f:
            pass

        new_stats_handler = csvhandler.MasterStatsHandler(
            str(tmp_stats_file), str(tmp_rounds_file), str(tmp_streaks_file))

        new_stats_handler.launch_new_game()
        time.sleep(5.5)
        new_stats_handler.record_new_round(0, 5.001)
        new_stats_handler.write_game_rounds_to_file(2)

        answer = new_stats_handler.calculate_true_stats(True)

        expected_answer = {'total_games': 1, 'total_playtime': '0.1min',
                           'total_rounds': 1, 'total_score': 0,
                           'total_streaks': 0, 'best_game_score': 0,
                           'worst_game_score': 0, 'average_game_score': 0,
                           'average_score_per_second': 0.0, 'most_rounds_in_a_game': 1,
                           'least_rounds_in_a_game': 1, 'average_rounds_in_a_game': 1,
                           'shortest_game_duration': '5.5s', 'longest_game_duration': '5.5s',
                           'average_game_duration': '5.5s', 'longest_streak': 0,
                           'shortest_streak': float('inf'), 'average_streak': 0,
                           'average_round_score': 0, 'average_round_time': '5.5s'}

        self.assertAlmostEqual(expected_answer, answer, delta=0.2)

    def test_shorter_formatting(self):
        """
        test the shorter formatting option for gui
        """

        tmp_stats_file = self.tmpdir.join('stats.csv')
        tmp_rounds_file = self.tmpdir.join('rounds.csv')
        tmp_streaks_file = self.tmpdir.join('streaks.csv')

        with open(tmp_stats_file, 'w+') as f:
            pass

        with open(tmp_rounds_file, 'w+') as f:
            pass

        with open(tmp_streaks_file, 'w+') as f:
            pass

        new_stats_handler = csvhandler.MasterStatsHandler(
            str(tmp_stats_file), str(tmp_rounds_file), str(tmp_streaks_file))

        new_stats_handler.launch_new_game()
        time.sleep(5.5)
        new_stats_handler.record_new_round(0, 5.001)
        new_stats_handler.write_game_rounds_to_file(2)

        answer = new_stats_handler.stats_formatting(True)

        self.assertEqual(64, len(answer[1]))
