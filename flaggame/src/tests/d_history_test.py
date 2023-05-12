import unittest
import pytest
import history
from os import getcwd
from unittest.mock import patch, MagicMock


class TestHistory(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def _pass_fixtures(self, tmpdir, capsys):
        self.tmpdir = tmpdir
        self.capsys = capsys
        self.maxDiff = None

    def test_write_to_empty_history_file(self):
        """
        test logic with an empty file
        """

        tmp_history_file = self.tmpdir.join('history.txt')

        with open(tmp_history_file, 'w+') as f:
            pass

        new_history_handler = history.MasterHistoryHandler(
            str(tmp_history_file))
        answer = new_history_handler.update()

        self.assertEqual(len(answer), 4)

        new_history_handler.console_print()

        captured = self.capsys.readouterr()
        self.assertEqual(62, len(captured.out))

    def test_write_to_nonempty_history_file(self):
        """
        test logic with a non-empty file
        """

        tmp_history_file = self.tmpdir.join('history.txt')

        with open(tmp_history_file, 'w+') as f:
            f.write("line 1\n" * 6)

        new_history_handler = history.MasterHistoryHandler(
            str(tmp_history_file))
        answer = new_history_handler.update()

        self.assertEqual(len(answer), 12)

    def test_create_history_file(self):
        """
        test file creation
        """

        new_history_handler = history.MasterHistoryHandler(
            str(self.tmpdir.join('history_wrong.txt')))
        answer = new_history_handler.update()

        self.assertEqual(len(answer), 4)

        new_history_handler.console_print()

        captured = self.capsys.readouterr()
        self.assertEqual(62, len(captured.out))

    def test_print_directories(self):
        """
        test printing out the directories
        """

        history.print_directories()

        expected_length = 97 + \
            len(getcwd()) + len(history.WORKING_DIR) + \
            len(history.HISTORY_PATH)

        captured = self.capsys.readouterr()
        self.assertEqual(expected_length, len(captured.out))

    def test_write_game_start(self):
        """
        test game start writing
        """

        tmp_history_file = self.tmpdir.join('history.txt')

        with open(tmp_history_file, 'w+') as f:
            pass

        new_history_handler = history.MasterHistoryHandler(
            str(tmp_history_file))
        answer = new_history_handler.update()

        self.assertEqual(len(answer), 4)

        new_history_handler.game_start("Classic")
        answer = new_history_handler.update()

        self.assertEqual(len(answer), 6)

        new_history_handler.game_start("Advanced")
        new_history_handler.game_start("Time Trial")
        new_history_handler.game_start("One Life")
        new_history_handler.game_start("Free Mode")
        answer = new_history_handler.update()

        self.assertEqual(len(answer), 14)

    def test_write_game_over(self):
        """
        test game over writing
        """

        tmp_history_file = self.tmpdir.join('history.txt')

        with open(tmp_history_file, 'w+') as f:
            pass

        new_history_handler = history.MasterHistoryHandler(
            str(tmp_history_file))
        answer = new_history_handler.update()

        self.assertEqual(len(answer), 4)

        new_history_handler.game_over([0, 400, 3])
        answer = new_history_handler.update()

        self.assertEqual(len(answer), 6)

        new_history_handler.game_over([1, 2374, 18])
        new_history_handler.game_over([2, 657, 3])
        new_history_handler.game_over([3, 1400, 14])
        answer = new_history_handler.update()

        self.assertEqual(len(answer), 12)

    def test_write_game_terminated(self):
        """
        test game termination writing
        """

        tmp_history_file = self.tmpdir.join('history.txt')

        with open(tmp_history_file, 'w+') as f:
            pass

        new_history_handler = history.MasterHistoryHandler(
            str(tmp_history_file))
        answer = new_history_handler.update()

        self.assertEqual(len(answer), 4)

        new_history_handler.game_terminated([0, 400, 3, 1])
        answer = new_history_handler.update()

        self.assertEqual(len(answer), 6)

        new_history_handler.game_terminated([1, 2374, 18, 2])
        new_history_handler.game_terminated([2, 657, 3, 1])
        new_history_handler.game_terminated([3, 1400, 14, 1])
        new_history_handler.game_terminated([4, 900, 2])
        answer = new_history_handler.update()

        self.assertEqual(len(answer), 14)

    def test_clear_history(self):
        """
        test if history is correctly cleared
        """

        tmp_history_file = self.tmpdir.join('history.txt')

        with open(tmp_history_file, 'w+') as f:
            f.write('some data')

        new_history_handler = history.MasterHistoryHandler(
            str(tmp_history_file))

        with patch('sys.exit') as exit_mock:
            exit_mock.side_effect = MagicMock()
            new_history_handler.clear_history(remove_statistics=False)

        with open(tmp_history_file, 'r') as f:
            contents = f.read()
            self.assertEqual(contents, '')
