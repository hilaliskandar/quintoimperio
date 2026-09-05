import unittest
from datetime import date

from quintoimperio.data.loader import RepositoryData
from quintoimperio.domain.voyage_event import VoyageEventModel, VoyageEventType


class VoyageEventDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo = RepositoryData()
        cls.rows = cls.repo.simulation("voyage_event_rules.csv")
        cls.routes = cls.repo.historical("routes.csv")
        cls.model = VoyageEventModel()

    def test_event_rules_have_valid_ranges_and_categories(self):
        ids = set()
        route_types = {row["route_type"] for row in self.routes}
        monsoon_values = {row["monsoon_dependence"] or "NONE" for row in self.routes}
        allowed_events = {item.value for item in VoyageEventType}

        for row in self.rows:
            self.assertNotIn(row["event_id"], ids)
            ids.add(row["event_id"])
            self.assertIn(row["event_type"], allowed_events)
            self.assertTrue(row["route_type"] == "ANY" or row["route_type"] in route_types)

            dependencies = [value for value in row["monsoon_dependence"].split("|") if value]
            for value in dependencies:
                self.assertTrue(value == "ANY" or value in monsoon_values)

            months = [int(value) for value in row["months"].split("|") if value]
            self.assertTrue(all(1 <= month <= 12 for month in months))

            probability = float(row["probability"])
            self.assertGreaterEqual(probability, 0.0)
            self.assertLessEqual(probability, 1.0)

            extra_min = int(row["extra_days_min"])
            extra_max = int(row["extra_days_max"])
            loss_min = float(row["condition_loss_min"])
            loss_max = float(row["condition_loss_max"])
            self.assertGreaterEqual(extra_min, 0)
            self.assertGreaterEqual(extra_max, extra_min)
            self.assertGreaterEqual(loss_min, 0.0)
            self.assertGreaterEqual(loss_max, loss_min)

    def test_applicable_probability_never_exceeds_one(self):
        for route in self.routes:
            route_id = route["route_id"]
            for month in range(1, 13):
                rules = self.model.applicable_rules(route_id, date(1498, month, 1))
                total = sum(rule.probability for rule in rules)
                self.assertLessEqual(
                    total,
                    1.0,
                    msg=f"{route_id} month={month} cumulative probability={total}",
                )


if __name__ == "__main__":
    unittest.main()
