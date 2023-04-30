import unittest
import timerlogic
import time


class TestTimerLogic(unittest.TestCase):
    # test the .1 digit return
    def test_displayed_reading(self):
        timerlogic.clock.run_timer()
        time.sleep(3)
        self.assertAlmostEqual(
            3.0, timerlogic.clock.read_displayed(), delta=0.3)

    # test the accurate method
    def test_accurate_reading(self):
        timerlogic.clock.run_timer()
        time.sleep(2)
        self.assertAlmostEqual(
            2.0000, timerlogic.clock.read_accurate(), delta=0.2500)
