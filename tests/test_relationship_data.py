import unittest

from quintoimperio.data.loader import RepositoryData


class RelationshipDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo = RepositoryData()
        cls.actors = cls.repo.historical("actors.csv")
        cls.node_actors = cls.repo.historical("node_actors.csv")
        cls.nodes = {row["node_id"] for row in cls.repo.historical("nodes.csv")}

    def test_actor_ids_are_unique_and_evidenced(self):
        seen = set()
        for row in self.actors:
            self.assertTrue(row["actor_id"])
            self.assertNotIn(row["actor_id"], seen)
            seen.add(row["actor_id"])
            self.assertIn(row["actor_type"], {"LOCAL_AUTHORITY", "MERCHANT_COMMUNITY"})
            self.assertIn(row["evidence_grade"], {"A", "B", "C", "D"})
            self.assertTrue(row["source_id"])

    def test_node_actor_links_reference_existing_nodes_and_actors(self):
        actor_ids = {row["actor_id"] for row in self.actors}
        seen = set()
        for row in self.node_actors:
            key = (row["node_id"], row["actor_id"], row["role"], row["period_from"], row["period_to"])
            self.assertNotIn(key, seen)
            seen.add(key)
            self.assertIn(row["node_id"], self.nodes)
            self.assertIn(row["actor_id"], actor_ids)
            self.assertIn(row["role"], {"AUTHORITY", "MERCHANT_COMMUNITY"})
            self.assertTrue(row["source_id"])

    def test_periods_are_not_broader_than_actor_periods(self):
        actors = {row["actor_id"]: row for row in self.actors}
        for row in self.node_actors:
            actor = actors[row["actor_id"]]
            if actor["period_from"] and row["period_from"]:
                self.assertGreaterEqual(int(row["period_from"]), int(actor["period_from"]))
            if actor["period_to"] and row["period_to"]:
                self.assertLessEqual(int(row["period_to"]), int(actor["period_to"]))


if __name__ == "__main__":
    unittest.main()
