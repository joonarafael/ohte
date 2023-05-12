import unittest
import pytest
import flaghandler


class TestFlagHandler(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def _pass_fixtures(self, capsys):
        self.capsys = capsys
        self.maxDiff = None

    def test_flaghandler_successful(self):
        """
        test successful flag importing
        """

        new_flaghandler = flaghandler.MasterFlagHandler(
            flaghandler.WORKING_DIR, flaghandler.FLAG_DIR)
        new_flaghandler.flag_import()

        captured = self.capsys.readouterr()
        self.assertEqual("All 198 flags have been found.\n", captured.out)

    def test_no_correctflags_file(self):
        """
        test if no reference for correct flags is found
        """

        new_flaghandler = flaghandler.MasterFlagHandler(
            "", flaghandler.FLAG_DIR)
        new_flaghandler.flag_import()

        captured = self.capsys.readouterr()

        expected_output = ("\nERROR\n"
                           "Software is unable to find the file '/src/logs/correctflags.txt' listing the correct flags.\n"
                           "Please ensure the integrity of this specified file or manually fetch it again from github.com/joonarafael/ohte/flaggame/src/logs/correctflags.txt.\n\n")

        self.assertEqual(expected_output, captured.out)

    def test_no_flags(self):
        """
        test if correct amount of flags is not found
        """

        new_flaghandler = flaghandler.MasterFlagHandler(
            flaghandler.WORKING_DIR, "")
        new_flaghandler.flag_import()

        captured = self.capsys.readouterr()

        expected_output = ("\nERROR\n"
                           "Error while trying to ensure integrity of flag image source files.\n"
                           f"Found a total of 0 out of 198 .png files in .\n"
                           "Please see flags subdirectory within src directory to ensure every flag file is present and in .png format.\n"
                           "Software is trying to find a .png file for every 195 independent state listed at: www.worldometers.info/geography/how-many-countries-are-there-in-the-world/ and Taiwan, Western Sahara & Kosovo.\n"
                           "Ensure directory integrity by fetching flags again from github.com/joonarafael/ohte/flaggame/src/flags.\n\n")

        self.assertEqual(expected_output, captured.out)

    def test_debug_option(self):
        """
        test retrying the flag import sequence
        """

        new_flaghandler = flaghandler.MasterFlagHandler(
            flaghandler.WORKING_DIR, flaghandler.FLAG_DIR)
        new_flaghandler.flag_import()
        new_flaghandler.list_every_flag()

        captured = self.capsys.readouterr()
        self.assertEqual(2, len(captured))
