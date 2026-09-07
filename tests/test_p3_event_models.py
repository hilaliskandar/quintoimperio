import unittest
from datetime import date

from quintoimperio.domain import ExpeditionEventModel, NodeStateEventModel


class P3EventModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.node_states = NodeStateEventModel()
        cls.expedition_events = ExpeditionEventModel()

    def test_cochin_is_not_fortified_before_1503_transition(self):
        state = self.node_states.effective_state("COC", date(1502, 12, 31))
        self.assertEqual(state.fortification_state, "NONE")
        self.assertNotIn("COC1503_E03", state.applied_event_ids)

    def test_cochin_becomes_fortified_without_sovereignty_change(self):
        state = self.node_states.effective_state("COC", date(1503, 12, 31))
        self.assertEqual(state.fortification_state, "PORTUGUESE_FORT")
        self.assertEqual(state.garrison_state, "PORTUGUESE_GARRISON")
        self.assertIn("soberania local", state.sovereignty_note.lower())
        self.assertIn("COC1503_E03", state.applied_event_ids)
        self.assertIn("COC1503_E04", state.applied_event_ids)

    def test_cannanore_contact_precedes_factory(self):
        at_contact = self.node_states.effective_state("CAN", date(1501, 1, 15))
        self.assertEqual(at_contact.institutional_presence, "NONE")
        after_factory = self.node_states.effective_state("CAN", date(1501, 12, 31))
        self.assertEqual(after_factory.institutional_presence, "FACTORY")

    def test_uncertain_transition_is_not_applied_before_upper_bound(self):
        during_range = self.node_states.effective_state("CAN", date(1501, 12, 15))
        self.assertEqual(during_range.institutional_presence, "NONE")
        after_range = self.node_states.effective_state("CAN", date(1501, 12, 31))
        self.assertEqual(after_range.institutional_presence, "FACTORY")

    def test_joao_da_nova_warning_is_available_only_after_documentary_window(self):
        before = self.expedition_events.available_by("EXP_JOAO_NOVA_1501", date(1501, 8, 1))
        self.assertFalse(any(event.event_id == "NOVA1501_E01" for event in before))
        after = self.expedition_events.available_by("EXP_JOAO_NOVA_1501", date(1501, 8, 31))
        self.assertTrue(any(event.event_id == "NOVA1501_E01" for event in after))

    def test_cabral_trajectory_events_are_separate_from_generic_fleet_state(self):
        events = self.expedition_events.preferred_for_expedition("EXP_CABRAL_1500")
        event_types = {event.event_type for event in events}
        self.assertIn("VESSEL_LOST_CONTACT", event_types)
        self.assertIn("VESSEL_LOSS", event_types)
        self.assertIn("TRAJECTORY_SPLIT", event_types)


if __name__ == "__main__":
    unittest.main()
