import unittest
import pytest
import flaghandler

#utilize the capsys to capture terminal output
class TestFlagHandler(unittest.TestCase):
    @pytest.fixture(autouse=True)
    
    def _pass_fixtures(self, capsys):
        self.capsys = capsys
        self.maxDiff = None

    #flaghandler prints that everything is okay if the flags found equal to 198.
    def test_flag_importing_files_existing(self):
        flaghandler.flagImport(198)
        captured = self.capsys.readouterr()
        self.assertEqual('All 198 flags have been found.\n', captured.out)
    
    #flaghandler should raise an error if any other amount of flags would be suddenly needed.
    def test_flag_importing_too_few_files(self):
        flaghandler.flagImport(200)
        captured = self.capsys.readouterr()
        self.assertEqual(f'\nERROR\nError while trying to ensure integrity of flag image source files.\nFound a total of 198 out of 200 .png files in {flaghandler.flagdir}.\nPlease see flags subdirectory within src directory to ensure every flag file is present and in .png format.\nSoftware is trying to find a matching .png file for every 195 independent state listed at: https://www.worldometers.info/geography/how-many-countries-are-there-in-the-world/ and Taiwan, Western Sahara & Kosovo.\n', captured.out)