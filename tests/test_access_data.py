import unittest

from quintoimperio.data.loader import RepositoryData
from quintoimperio.domain import AccessStatus


class AccessRuleDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo = RepositoryData()
        cls.nodes = cls.repo.historical("nodes.csv")
        cls.rules = cls.repo.simulation("access_rules.csv")

    def test_every_documented_node_access_regime_has_rule(self):
        node_regimes = {row["access_regime"] for row in self.nodes if row["access_regime"]}
        rule_regimes = {row["access_regime"] for row in self.rules}
        self.assertEqual(node_regimes - rule_regimes, set())

    def test_access_rules_have_valid_status_boolean_and_time(self):
        seen = set()
        statuses = {status.value for status in AccessStatus}
        for row in self.rules:
            self.assertNotIn(row["access_regime"], seen)
            seen.add(row["access_regime"])
            self.assertIn(row["initial_status"], statuses)
            self.assertIn(row["negotiable"], {"TRUE", "FALSE"})
            days = int(row["time_days"])
            self.assertGreaterEqual(days, 0)
            if row["negotiable"] == "TRUE":
                self.assertGreater(days, 0)
                self.assertEqual(row["initial_status"], "NEGOTIATION_REQUIRED")


if __name__ == "__main__":
    unittest.main()
