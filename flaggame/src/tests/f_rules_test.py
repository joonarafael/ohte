import unittest
import pytest
import rules


class TestRules(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def _pass_fixtures(self, tmpdir):
        self.tmpdir = tmpdir

    def test_valid_rules_file(self):
        """
        test successful rules reading
        """

        tmp_rules_file = self.tmpdir.join('gamerules.txt')

        with open(tmp_rules_file, 'w+') as f:
            f.write("line 1\n" * 70)

        new_rule_reader = rules.MasterRulesReader(str(tmp_rules_file))
        answer = new_rule_reader.read_rules()

        self.assertEqual(len(answer), 70)

    def test_invalid_rules_file(self):
        """
        test what happens if rulebook is modified
        """

        tmp_rules_file = self.tmpdir.join('gamerules.txt')

        with open(tmp_rules_file, 'w+') as f:
            f.write("line 1\n" * 71)

        new_rule_reader = rules.MasterRulesReader(str(tmp_rules_file))
        answer = new_rule_reader.read_rules()

        self.assertEqual(answer, None)

    def test_missing_rules_file(self):
        """
        test what happens if file cannot be found
        """

        tmp_rules_file = self.tmpdir.join('gamerules.txt')

        with open(tmp_rules_file, 'w+') as f:
            f.write("line 1\n" * 70)

        new_rule_reader = rules.MasterRulesReader(
            str(self.tmpdir.join('gamerules_wrong.txt')))
        answer = new_rule_reader.read_rules()

        self.assertEqual(answer, None)
