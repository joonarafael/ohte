import unittest
import pytest
import random
from unittest.mock import MagicMock
import gamehandler
import time


class TestGameHandler(unittest.TestCase):
    def test_gamehandler_init(self):
        """
        test the class __init__ function
        """

        new_gamehandler = gamehandler.MasterGameHandler(None, None, None)

        self.assertEqual(str(
            new_gamehandler), "GameHandler Status: Game Mode -1; Round 0; Score 0; Lives 0; Streak 0.")

    def test_gamehandler_instance_reset(self):
        """
        test the game cancellation logic and gamehandler reset
        """

        mock_game_tab = MagicMock()
        mock_stats_tab = MagicMock()
        mock_history_tab = MagicMock()
        new_gamehandler = gamehandler.MasterGameHandler(
            mock_game_tab, mock_stats_tab, mock_history_tab)

        new_gamehandler.classic()
        new_gamehandler.player_answered(0)
        new_gamehandler.reset_game_handler()

        self.assertEqual(str(
            new_gamehandler), "GameHandler Status: Game Mode -1; Round 0; Score 0; Lives 0; Streak 0.")

        assert mock_game_tab.display_score.call_count == 3
        assert mock_game_tab.display_streak.call_count == 3
        assert mock_game_tab.display_round.call_count == 4
        assert mock_game_tab.display_timer.call_count == 3
        assert mock_game_tab.display_lives.call_count == 3 or mock_game_tab.display_lives.call_count == 2
        assert mock_game_tab.next_buttons.call_count == 2
        assert mock_game_tab.next_flag.call_count == 2
        assert mock_game_tab.inactive_buttons.call_count == 1
        assert mock_game_tab.change_title.call_count == 2
        assert mock_history_tab.history_update.call_count == 2
        assert mock_stats_tab.stats_update.call_count == 1

    def test_function_calls_launch(self):
        """
        test to ensure all necessary function calls are made after game launch
        """

        mock_game_tab = MagicMock()
        mock_stats_tab = MagicMock()
        mock_history_tab = MagicMock()
        new_gamehandler = gamehandler.MasterGameHandler(
            mock_game_tab, mock_stats_tab, mock_history_tab)

        new_gamehandler.classic()

        self.assertEqual(str(
            new_gamehandler), "GameHandler Status: Game Mode 0; Round 1; Score 0; Lives 3; Streak 0.")

        assert mock_game_tab.display_score.call_count == 1
        assert mock_game_tab.display_streak.call_count == 1
        assert mock_game_tab.display_round.call_count == 2
        assert mock_game_tab.display_timer.call_count == 1
        assert mock_game_tab.display_lives.call_count == 1
        assert mock_game_tab.next_buttons.call_count == 1
        assert mock_game_tab.next_flag.call_count == 1
        assert mock_game_tab.change_title.call_count == 1

    def test_classic_launch(self):
        """
        test classic game mode launch
        """

        mock_game_tab = MagicMock()
        mock_stats_tab = MagicMock()
        mock_history_tab = MagicMock()
        new_gamehandler = gamehandler.MasterGameHandler(
            mock_game_tab, mock_stats_tab, mock_history_tab)

        new_gamehandler.classic()

        self.assertEqual(str(
            new_gamehandler), "GameHandler Status: Game Mode 0; Round 1; Score 0; Lives 3; Streak 0.")

    def test_advanced_launch(self):
        """
        test advanced game mode launch
        """

        mock_game_tab = MagicMock()
        mock_stats_tab = MagicMock()
        mock_history_tab = MagicMock()
        new_gamehandler = gamehandler.MasterGameHandler(
            mock_game_tab, mock_stats_tab, mock_history_tab)

        new_gamehandler.advanced()

        self.assertEqual(str(
            new_gamehandler), "GameHandler Status: Game Mode 1; Round 1; Score 0; Lives 3; Streak 0.")

    def test_time_trial_launch(self):
        """
        test time trial game mode launch
        """

        mock_game_tab = MagicMock()
        mock_stats_tab = MagicMock()
        mock_history_tab = MagicMock()
        new_gamehandler = gamehandler.MasterGameHandler(
            mock_game_tab, mock_stats_tab, mock_history_tab)

        new_gamehandler.time_trial()

        self.assertEqual(str(
            new_gamehandler), "GameHandler Status: Game Mode 2; Round 1; Score 0; Lives 3; Streak 0.")

    def test_one_life_launch(self):
        """
        test one life game mode launch
        """

        mock_game_tab = MagicMock()
        mock_stats_tab = MagicMock()
        mock_history_tab = MagicMock()
        new_gamehandler = gamehandler.MasterGameHandler(
            mock_game_tab, mock_stats_tab, mock_history_tab)

        new_gamehandler.one_life()

        self.assertEqual(str(
            new_gamehandler), "GameHandler Status: Game Mode 3; Round 1; Score 0; Lives 1; Streak 0.")

    def test_free_mode_launch(self):
        """
        test free mode game launch
        """

        mock_game_tab = MagicMock()
        mock_stats_tab = MagicMock()
        mock_history_tab = MagicMock()
        new_gamehandler = gamehandler.MasterGameHandler(
            mock_game_tab, mock_stats_tab, mock_history_tab)

        new_gamehandler.free()

        self.assertEqual(str(
            new_gamehandler), "GameHandler Status: Game Mode 4; Round 1; Score 0; Lives -1; Streak 0.")

    def test_flag_slide_show_launch(self):
        """
        test the free flag browsing mode
        """

        mock_game_tab = MagicMock()
        mock_stats_tab = MagicMock()
        mock_history_tab = MagicMock()
        new_gamehandler = gamehandler.MasterGameHandler(
            mock_game_tab, mock_stats_tab, mock_history_tab)

        new_gamehandler.flag_slide_show(10)

        self.assertEqual(str(
            new_gamehandler), "GameHandler Status: Game Mode -2; Round 0; Score 0; Lives 0; Streak 0.")

        assert mock_game_tab.next_buttons.call_count == 1
        assert mock_game_tab.next_flag.call_count == 1
        assert mock_game_tab.change_title.call_count == 1

        new_gamehandler.player_answered(2)
        self.assertEqual(new_gamehandler.free_index, 0)

        new_gamehandler.player_answered(2)
        self.assertEqual(new_gamehandler.free_index, 188)

        new_gamehandler.player_answered(0)
        self.assertEqual(new_gamehandler.free_index, 187)

        new_gamehandler.player_answered(3)
        self.assertEqual(new_gamehandler.free_index, 197)

        new_gamehandler.player_answered(1)
        self.assertEqual(new_gamehandler.free_index, 0)

    def test_failsafe_answer(self):
        """
        test if gamehandler notices that no game has yet been launched when input is given
        """

        mock_game_tab = MagicMock()
        mock_stats_tab = MagicMock()
        mock_history_tab = MagicMock()
        new_gamehandler = gamehandler.MasterGameHandler(
            mock_game_tab, mock_stats_tab, mock_history_tab)

        new_gamehandler.player_answered(0)

        assert mock_game_tab.display_score.call_count == 0

    def test_classic_score(self):
        """
        check score awarding in a classic game mode
        """

        mock_game_tab = MagicMock()
        mock_stats_tab = MagicMock()
        mock_history_tab = MagicMock()
        new_gamehandler = gamehandler.MasterGameHandler(
            mock_game_tab, mock_stats_tab, mock_history_tab)

        new_gamehandler.classic()

        correct_answer = new_gamehandler.current_flag.upper().replace("_", " ")
        correct_button = new_gamehandler.buttons.index(correct_answer)

        new_gamehandler.player_answered(correct_button)

        self.assertEqual(str(
            new_gamehandler), "GameHandler Status: Game Mode 0; Round 2; Score 100; Lives 3; Streak 1.")

        correct_answer = new_gamehandler.current_flag.upper().replace("_", " ")
        correct_button = new_gamehandler.buttons.index(correct_answer)

        false_button = random.randint(0, 3)

        while false_button == correct_button:
            false_button = random.randint(0, 3)

        new_gamehandler.remaining_flags = set()
        new_gamehandler.player_answered(false_button)

        self.assertEqual(str(
            new_gamehandler), "GameHandler Status: Game Mode 0; Round 3; Score 100; Lives 2; Streak 0.")

        self.assertEqual(len(new_gamehandler.remaining_flags), 197)

    def test_advanced_score(self):
        """
        check score awarding in an advanced game mode
        """

        mock_game_tab = MagicMock()
        mock_stats_tab = MagicMock()
        mock_history_tab = MagicMock()
        new_gamehandler = gamehandler.MasterGameHandler(
            mock_game_tab, mock_stats_tab, mock_history_tab)

        new_gamehandler.advanced()

        correct_answer = new_gamehandler.current_flag.upper().replace("_", " ")
        correct_button = new_gamehandler.buttons.index(correct_answer)

        time.sleep(1)
        new_gamehandler.player_answered(correct_button)

        self.assertAlmostEqual(new_gamehandler.score, 176.8, delta=7.5)
        self.assertEqual(str(
            new_gamehandler), f"GameHandler Status: Game Mode 1; Round 2; Score {new_gamehandler.score}; Lives 3; Streak 1.")

        correct_answer = new_gamehandler.current_flag.upper().replace("_", " ")
        correct_button = new_gamehandler.buttons.index(correct_answer)

        false_button = random.randint(0, 3)

        while false_button == correct_button:
            false_button = random.randint(0, 3)

        new_gamehandler.player_answered(false_button)

        self.assertEqual(str(
            new_gamehandler), f"GameHandler Status: Game Mode 1; Round 3; Score {new_gamehandler.score}; Lives 2; Streak 0.")

        old_score = new_gamehandler.score

        correct_answer = new_gamehandler.current_flag.upper().replace("_", " ")
        correct_button = new_gamehandler.buttons.index(correct_answer)

        time.sleep(6)
        new_gamehandler.player_answered(correct_button)

        self.assertAlmostEqual(new_gamehandler.score, old_score + 100, delta=5)
        self.assertEqual(str(
            new_gamehandler), f"GameHandler Status: Game Mode 1; Round 4; Score {new_gamehandler.score}; Lives 2; Streak 1.")

    def test_time_trial_score(self):
        """
        check score awarding in a time trial game mode
        """

        mock_game_tab = MagicMock()
        mock_stats_tab = MagicMock()
        mock_history_tab = MagicMock()
        new_gamehandler = gamehandler.MasterGameHandler(
            mock_game_tab, mock_stats_tab, mock_history_tab)

        new_gamehandler.time_trial()

        correct_answer = new_gamehandler.current_flag.upper().replace("_", " ")
        correct_button = new_gamehandler.buttons.index(correct_answer)

        time.sleep(2)
        new_gamehandler.player_answered(correct_button)

        self.assertAlmostEqual(new_gamehandler.score, 167.2, delta=7.5)
        self.assertEqual(str(
            new_gamehandler), f"GameHandler Status: Game Mode 2; Round 2; Score {new_gamehandler.score}; Lives 3; Streak 1.")

        correct_answer = new_gamehandler.current_flag.upper().replace("_", " ")
        correct_button = new_gamehandler.buttons.index(correct_answer)

        false_button = random.randint(0, 3)

        while false_button == correct_button:
            false_button = random.randint(0, 3)

        new_gamehandler.player_answered(false_button)

        self.assertEqual(str(
            new_gamehandler), f"GameHandler Status: Game Mode 2; Round 3; Score {new_gamehandler.score}; Lives 2; Streak 0.")

        old_score = new_gamehandler.score

        correct_answer = new_gamehandler.current_flag.upper().replace("_", " ")
        correct_button = new_gamehandler.buttons.index(correct_answer)

        time.sleep(6)
        new_gamehandler.player_answered(correct_button)

        self.assertEqual(new_gamehandler.score, old_score)
        self.assertEqual(str(
            new_gamehandler), f"GameHandler Status: Game Mode -1; Round 3; Score {old_score}; Lives 0; Streak 0.")

        new_gamehandler.time_trial()

        correct_answer = new_gamehandler.current_flag.upper().replace("_", " ")
        correct_button = new_gamehandler.buttons.index(correct_answer)

        false_button = random.randint(0, 3)

        while false_button == correct_button:
            false_button = random.randint(0, 3)

        time.sleep(6)
        new_gamehandler.player_answered(false_button)

        self.assertEqual(str(
            new_gamehandler), f"GameHandler Status: Game Mode -1; Round 1; Score 0; Lives 0; Streak 0.")

    def test_one_life_score(self):
        """
        check score awarding in an one life game mode
        """

        mock_game_tab = MagicMock()
        mock_stats_tab = MagicMock()
        mock_history_tab = MagicMock()
        new_gamehandler = gamehandler.MasterGameHandler(
            mock_game_tab, mock_stats_tab, mock_history_tab)

        new_gamehandler.one_life()

        correct_answer = new_gamehandler.current_flag.upper().replace("_", " ")
        correct_button = new_gamehandler.buttons.index(correct_answer)

        new_gamehandler.player_answered(correct_button)

        self.assertEqual(str(
            new_gamehandler), f"GameHandler Status: Game Mode 3; Round 2; Score 100; Lives 1; Streak 1.")

        correct_answer = new_gamehandler.current_flag.upper().replace("_", " ")
        correct_button = new_gamehandler.buttons.index(correct_answer)

        false_button = random.randint(0, 3)

        while false_button == correct_button:
            false_button = random.randint(0, 3)

        new_gamehandler.player_answered(false_button)

        self.assertEqual(str(
            new_gamehandler), f"GameHandler Status: Game Mode -1; Round 2; Score 100; Lives 0; Streak 0.")

    def test_free_mode_score(self):
        """
        check score awarding in a free mode game
        """

        mock_game_tab = MagicMock()
        mock_stats_tab = MagicMock()
        mock_history_tab = MagicMock()
        new_gamehandler = gamehandler.MasterGameHandler(
            mock_game_tab, mock_stats_tab, mock_history_tab)

        new_gamehandler.free()

        correct_answer = new_gamehandler.current_flag.upper().replace("_", " ")
        correct_button = new_gamehandler.buttons.index(correct_answer)

        new_gamehandler.player_answered(correct_button)

        self.assertEqual(str(
            new_gamehandler), f"GameHandler Status: Game Mode 4; Round 2; Score 100; Lives -1; Streak 1.")

        correct_answer = new_gamehandler.current_flag.upper().replace("_", " ")
        correct_button = new_gamehandler.buttons.index(correct_answer)

        false_button = random.randint(0, 3)

        while false_button == correct_button:
            false_button = random.randint(0, 3)

        new_gamehandler.player_answered(false_button)

        self.assertEqual(str(
            new_gamehandler), f"GameHandler Status: Game Mode 4; Round 3; Score 100; Lives -1; Streak 0.")
