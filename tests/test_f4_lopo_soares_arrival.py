import unittest
from datetime import date

from quintoimperio.domain import ExpeditionEventModel, NodeStateEventModel


class F4LopoSoaresArrivalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.events = ExpeditionEventModel()
        cls.node_states = NodeStateEventModel()

    def test_lopo_soares_arrival_is_exact_and_not_available_early(self):
        expedition_id = "EXP_LOPO_SOARES_1504"

        before = self.events.available_by(expedition_id, date(1504, 9, 13))
        on_arrival = self.events.available_by(expedition_id, date(1504, 9, 14))

        self.assertNotIn("LS1504_E01", {event.event_id for event in before})
        self.assertIn("LS1504_E01", {event.event_id for event in on_arrival})

        event = next(event for event in on_arrival if event.event_id == "LS1504_E01")
        self.assertEqual(event.event_type, "ROYAL_FLEET_ARRIVES_COCHIN")
        self.assertEqual(event.date_from, date(1504, 9, 14))
        self.assertEqual(event.date_to, date(1504, 9, 14))
        self.assertEqual(event.date_precision, "EXACT")
        self.assertIsNone(event.origin_node)
        self.assertEqual(event.destination_node, "COC")

    def test_lopo_arrival_does_not_overwrite_cochin_local_sovereignty(self):
        before = self.node_states.effective_state("COC", date(1504, 9, 13))
        after = self.node_states.effective_state("COC", date(1504, 9, 14))

        self.assertEqual(before, after)
        self.assertEqual(after.institutional_presence, "FACTORY_RESTORED")
        self.assertEqual(after.fortification_state, "PORTUGUESE_FORT")
        self.assertEqual(after.garrison_state, "PORTUGUESE_GARRISON")
        self.assertIn("soberania local", after.sovereignty_note.lower())


if __name__ == "__main__":
    unittest.main()
