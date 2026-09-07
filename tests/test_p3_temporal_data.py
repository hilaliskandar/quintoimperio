import unittest
from datetime import date

from quintoimperio.data.loader import RepositoryData


class P3TemporalDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo = RepositoryData()
        cls.nodes = {row["node_id"]: row for row in cls.repo.historical("nodes.csv")}
        cls.expeditions = {
            row["expedition_id"]: row for row in cls.repo.historical("expeditions.csv")
        }
        cls.events = cls.repo.historical("expedition_events.csv")
        cls.node_events = cls.repo.historical("node_state_events.csv")

    def test_vera_cruz_is_regional_anchorage_not_market(self):
        node = self.nodes["VCR"]
        self.assertEqual(node["node_type"], "ANCHORAGE")
        self.assertEqual(node["market_scale"], "NONE")
        self.assertEqual(node["access_regime"], "ANCHORAGE_CONTACT")
        self.assertEqual(node["coordinate_confidence"], "MEDIUM")

    def test_cannanore_starts_without_retroactive_fortification(self):
        node = self.nodes["CAN"]
        self.assertEqual(node["node_type"], "FOREIGN_PORT")
        self.assertEqual(node["fortification"], "NONE")
        self.assertEqual(node["active_from"], "1501")

    def test_joao_da_nova_information_event_is_local_and_one_shot_candidate(self):
        row = next(event for event in self.events if event["event_id"] == "NOVA1501_E01")
        self.assertEqual(row["event_type"], "INFORMATION_ACQUISITION")
        self.assertEqual(row["origin_node"], "SBR")
        self.assertEqual(row["destination_node"], "SBR")
        self.assertEqual(row["preferred_for_simulation"], "TRUE")

    def test_cochin_fortification_is_temporal_not_node_baseline(self):
        self.assertEqual(self.nodes["COC"]["fortification"], "NONE")
        fort = next(row for row in self.node_events if row["event_id"] == "COC1503_E03")
        self.assertEqual(fort["event_type"], "FORTIFICATION_ESTABLISHED")
        self.assertEqual(fort["fortification_state"], "PORTUGUESE_FORT")
        self.assertIn("soberania local", fort["sovereignty_note"].lower())

    def test_cannanore_factory_is_not_present_at_first_contact(self):
        contact = next(row for row in self.node_events if row["event_id"] == "CAN1501_E01")
        factory = next(row for row in self.node_events if row["event_id"] == "CAN1501_E02")
        self.assertEqual(contact["institutional_presence"], "NONE")
        self.assertEqual(factory["institutional_presence"], "FACTORY")
        self.assertLess(date.fromisoformat(contact["date_from"]), date.fromisoformat(factory["date_from"]))

    def test_all_temporal_events_reference_known_nodes(self):
        for row in self.node_events:
            self.assertIn(row["node_id"], self.nodes)

    def test_all_expedition_events_reference_normalized_expeditions_and_nodes(self):
        for row in self.events:
            self.assertIn(row["expedition_id"], self.expeditions)
            if row["origin_node"]:
                self.assertIn(row["origin_node"], self.nodes)
            if row["destination_node"]:
                self.assertIn(row["destination_node"], self.nodes)


if __name__ == "__main__":
    unittest.main()
