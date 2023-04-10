import unittest
import timerlogic
import time


class TestTimerLogic(unittest.TestCase):
    # test basic timer functionality
    def test_flag_importing_files_existing(self):
        timerlogic.clock.run_classic_timer()
        time.sleep(2)
        self.assertAlmostEqual(
            2.0000, timerlogic.clock.read_accurate(), delta=0.5000)
