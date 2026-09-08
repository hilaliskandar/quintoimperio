import unittest
from datetime import date

from quintoimperio.domain import ExpeditionEventModel, NodeStateEventModel


class F4End1504TransitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.events = ExpeditionEventModel()
        cls.node_states = NodeStateEventModel()

    def test_lopo_soares_departs_cochin_on_26_december(self):
        expedition_id = "EXP_LOPO_SOARES_1504"

        before = self.events.available_by(expedition_id, date(1504, 12, 25))
        on_departure = self.events.available_by(expedition_id, date(1504, 12, 26))

        self.assertNotIn("LS1504_E02", {event.event_id for event in before})
        self.assertIn("LS1504_E02", {event.event_id for event in on_departure})

        event = next(event for event in on_departure if event.event_id == "LS1504_E02")
        self.assertEqual(event.event_type, "ROYAL_FLEET_DEPARTS_COCHIN")
        self.assertEqual(event.date_from, date(1504, 12, 26))
        self.assertEqual(event.date_to, date(1504, 12, 26))
        self.assertEqual(event.date_precision, "EXACT")
        self.assertEqual(event.origin_node, "COC")
        self.assertIsNone(event.destination_node)

    def test_end_1504_cochin_keeps_resident_state_after_royal_fleet_departure(self):
        state = self.node_states.effective_state("COC", date(1504, 12, 31))

        self.assertEqual(state.institutional_presence, "FACTORY_RESTORED")
        self.assertEqual(state.fortification_state, "PORTUGUESE_FORT")
        self.assertEqual(state.garrison_state, "PORTUGUESE_GARRISON")
        self.assertEqual(state.access_state, "NEGOTIATED")
        self.assertEqual(state.relationship_state, "FAVORABLE")
        self.assertIn("soberania local", state.sovereignty_note.lower())

    def test_lopo_arrival_and_departure_are_documentary_without_playable_route(self):
        events = self.events.preferred_for_expedition("EXP_LOPO_SOARES_1504")

        self.assertEqual(
            [(event.event_id, event.origin_node, event.destination_node) for event in events],
            [
                ("LS1504_E01", None, "COC"),
                ("LS1504_E02", "COC", None),
            ],
        )


if __name__ == "__main__":
    unittest.main()
