import unittest
import pytest
import gamehandler


class TestGameHandler(unittest.TestCase):
    def test_init_successful(self):
        game = gamehandler.MASTER_GAME_HANDLER

        self.assertEqual(str(
            game), "GameHandler Status: Game Mode -1; Round 0; Score 0; Lives 0; Streak 0")