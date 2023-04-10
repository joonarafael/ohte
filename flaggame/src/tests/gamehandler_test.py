import unittest
import pytest
import gamehandler

# utilize the capsys to capture terminal output


class TestGameHandler(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def _pass_fixtures(self, capsys):
        self.capsys = capsys
        self.maxDiff = None

    # flaghandler prints that everything is okay if the flags found equal to 198.
    def test_game_handler_init(self):
        self.game = gamehandler.GameHandler()

        self.assertEqual(str(
            self.game), "GameHandler Status: Game Mode -1; Round 0; Score 0; Lives 0; Streak 0; DevPrint False.")
