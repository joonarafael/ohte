import os
import unittest
import pytest
from rules import update, GAME_RULES_PATH


class TestRules(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def _pass_fixtures(self, tmpdir):
        self.tmpdir = tmpdir

    def test_update_with_valid_rules_file(self):
        tmp_rules_file = self.tmpdir.join('gamerules.txt')
        with open(tmp_rules_file, 'w') as f:
            f.write("line 1\n" * 70)

        os.environ['GAME_RULES_PATH'] = str(tmp_rules_file)
        updated_rules = update()
        self.assertEqual(len(updated_rules), 70)
