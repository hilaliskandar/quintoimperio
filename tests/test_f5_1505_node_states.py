import unittest
from datetime import date

from quintoimperio.domain import NodeStateEventModel


class F5NodeStateTests(unittest.TestCase):
    def test_sofala_presence_precedes_fortification_and_garrison(self):
        model = NodeStateEventModel()

        before = model.effective_state("SOF", date(1505, 9, 3))
        presence = model.effective_state("SOF", date(1505, 9, 4))
        fortified = model.effective_state("SOF", date(1505, 9, 21))

        self.assertEqual(before.institutional_presence, "NONE")
        self.assertEqual(before.fortification_state, "LOW")
        self.assertEqual(before.garrison_state, "NONE")

        self.assertEqual(presence.institutional_presence, "FACTORY_INITIAL")
        self.assertEqual(presence.fortification_state, "LOW")
        self.assertEqual(presence.garrison_state, "NONE")
        self.assertIn("SOF1505_E01", presence.applied_event_ids)

        self.assertEqual(fortified.institutional_presence, "FACTORY")
        self.assertEqual(fortified.fortification_state, "PORTUGUESE_FORT")
        self.assertEqual(fortified.garrison_state, "PORTUGUESE_GARRISON")
        self.assertIn("SOF1505_E02", fortified.applied_event_ids)
        self.assertNotIn("Portugal", fortified.sovereignty_note.split(";")[0])

    def test_cannanore_october_range_applies_only_at_upper_bound(self):
        model = NodeStateEventModel()

        before = model.effective_state("CAN", date(1505, 10, 30))
        after = model.effective_state("CAN", date(1505, 10, 31))

        self.assertEqual(before.fortification_state, "NONE")
        self.assertEqual(before.garrison_state, "NONE")
        self.assertNotIn("CAN1505_E01", before.applied_event_ids)

        self.assertEqual(after.institutional_presence, "FACTORY_REORGANIZED")
        self.assertEqual(after.fortification_state, "PORTUGUESE_FORT")
        self.assertEqual(after.garrison_state, "PORTUGUESE_GARRISON")
        self.assertEqual(after.access_state, "NEGOTIATED")
        self.assertEqual(after.relationship_state, "TENSE")
        self.assertIn("Kolathunad", after.sovereignty_note)
        self.assertIn("CAN1505_E01", after.applied_event_ids)

    def test_1505_states_do_not_retroproject_into_earlier_campaigns(self):
        model = NodeStateEventModel()

        sofala_1504 = model.effective_state("SOF", date(1504, 12, 31))
        cannanore_1504 = model.effective_state("CAN", date(1504, 12, 31))

        self.assertEqual(sofala_1504.fortification_state, "LOW")
        self.assertEqual(sofala_1504.garrison_state, "NONE")
        self.assertEqual(cannanore_1504.fortification_state, "NONE")
        self.assertEqual(cannanore_1504.garrison_state, "NONE")


if __name__ == "__main__":
    unittest.main()
