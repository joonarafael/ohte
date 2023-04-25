import unittest
import pytest
import csvhandler

# utilize the capsys to capture terminal output


class TestFlagHandler(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def _pass_fixtures(self, capsys):
        self.capsys = capsys
        self.maxDiff = None

    # check basic csvhandler functionality
    def test_initialize_mastergame(self):
        csv_class = csvhandler.MASTER_RUNNING_GAME
        csv_class.launch_new_game()
        csv_class.write_new_round(100, 0.5)
        csv_class.write_new_streak(4)

        self.assertEqual(csv_class.rounds, [(100, 0.5)])
        self.assertEqual(csv_class.streaks, [4])
