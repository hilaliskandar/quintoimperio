import unittest
from collections import Counter, defaultdict
from datetime import date

from quintoimperio.data.loader import RepositoryData


class ExpeditionEpilogueDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo = RepositoryData()
        cls.rows = cls.repo.historical("expedition_epilogue_events.csv")
        cls.expeditions = {
            row["expedition_id"] for row in cls.repo.historical("expeditions.csv")
        }
        cls.nodes = {
            row["node_id"] for row in cls.repo.historical("nodes.csv")
        }

    def test_events_reference_existing_expedition_and_nodes(self):
        self.assertTrue(self.rows)
        for row in self.rows:
            with self.subTest(event_id=row["event_id"]):
                self.assertIn(row["expedition_id"], self.expeditions)
                if row["origin_node"]:
                    self.assertIn(row["origin_node"], self.nodes)
                if row["destination_node"]:
                    self.assertIn(row["destination_node"], self.nodes)

    def test_date_precision_semantics_are_explicit(self):
        allowed = {"EXACT", "BEFORE", "AFTER", "RANGE"}
        for row in self.rows:
            with self.subTest(event_id=row["event_id"]):
                self.assertIn(row["date_precision"], allowed)
                start = row["date_from"]
                end = row["date_to"]
                if row["date_precision"] == "EXACT":
                    self.assertTrue(start)
                    self.assertEqual(start, end)
                elif row["date_precision"] == "BEFORE":
                    self.assertFalse(start)
                    self.assertTrue(end)
                elif row["date_precision"] == "AFTER":
                    self.assertTrue(start)
                    self.assertFalse(end)
                elif row["date_precision"] == "RANGE":
                    self.assertTrue(start)
                    self.assertTrue(end)
                    self.assertLessEqual(date.fromisoformat(start), date.fromisoformat(end))

    def test_vasco_lisbon_arrival_preserves_three_unresolved_variants(self):
        rows = [
            row
            for row in self.rows
            if row["variant_group"] == "GAMA_LISBON_ARRIVAL_1499"
        ]
        self.assertEqual(len(rows), 3)
        self.assertEqual(
            {row["date_from"] for row in rows},
            {"1499-08-29", "1499-09-08", "1499-09-18"},
        )
        self.assertTrue(all(row["preferred_for_simulation"] == "FALSE" for row in rows))

    def test_berrio_variant_group_has_one_documented_working_preference(self):
        rows = [
            row
            for row in self.rows
            if row["variant_group"] == "BERRIO_ARRIVAL_1499"
        ]
        self.assertEqual(len(rows), 2)
        self.assertEqual(Counter(row["preferred_for_simulation"] for row in rows), Counter({"TRUE": 1, "FALSE": 1}))
        preferred = next(row for row in rows if row["preferred_for_simulation"] == "TRUE")
        self.assertEqual(preferred["date_from"], "1499-07-10")

    def test_epilogue_preserves_three_distinct_trajectories(self):
        trajectories = defaultdict(list)
        for row in self.rows:
            trajectories[row["trajectory_id"]].append(row)
        self.assertEqual(
            set(trajectories),
            {"BERRIO_RETURN", "SAO_GABRIEL_RETURN", "GAMA_PERSONAL_RETURN"},
        )
        self.assertTrue(
            any(row["event_type"] == "COMMAND_CHANGE" for row in trajectories["SAO_GABRIEL_RETURN"])
        )
        self.assertTrue(
            any(row["event_type"] == "TRAJECTORY_SPLIT" for row in trajectories["GAMA_PERSONAL_RETURN"])
        )

    def test_epilogue_is_editorial_not_primary_narrative(self):
        self.assertTrue(
            all(row["evidence_scope"] == "EDITORIAL_SYNTHESIS" for row in self.rows)
        )


if __name__ == "__main__":
    unittest.main()
