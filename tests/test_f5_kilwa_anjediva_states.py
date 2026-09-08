import unittest
from datetime import date

from quintoimperio.domain import NodeStateEventModel


class F5KilwaAnjedivaStateTests(unittest.TestCase):
    def test_kilwa_state_applies_at_conservative_end_of_occupation_window(self):
        model = NodeStateEventModel()

        before = model.effective_state("KIL", date(1505, 7, 23))
        after = model.effective_state("KIL", date(1505, 7, 24))

        self.assertEqual(before.fortification_state, "LOW")
        self.assertEqual(before.garrison_state, "NONE")
        self.assertNotIn("KIL1505_E01", before.applied_event_ids)

        self.assertEqual(after.institutional_presence, "PORTUGUESE_RESIDENT_PRESENCE")
        self.assertEqual(after.fortification_state, "PORTUGUESE_FORT")
        self.assertEqual(after.garrison_state, "PORTUGUESE_GARRISON")
        self.assertEqual(after.relationship_state, "TENSE")
        self.assertIn("não é modelado como anexação", after.sovereignty_note)
        self.assertIn("KIL1505_E01", after.applied_event_ids)

    def test_anjediva_month_window_does_not_promote_candidate_daily_dates(self):
        model = NodeStateEventModel()

        candidate_day = model.effective_state("ANJ", date(1505, 9, 14))
        after = model.effective_state("ANJ", date(1505, 9, 30))

        self.assertNotEqual(candidate_day.fortification_state, "PORTUGUESE_FORT")
        self.assertEqual(candidate_day.garrison_state, "NONE")
        self.assertNotIn("ANJ1505_E01", candidate_day.applied_event_ids)

        self.assertEqual(after.institutional_presence, "PORTUGUESE_RESIDENT_PRESENCE")
        self.assertEqual(after.fortification_state, "PORTUGUESE_FORT")
        self.assertEqual(after.garrison_state, "PORTUGUESE_GARRISON")
        self.assertIn("não é convertida automaticamente", after.sovereignty_note)
        self.assertIn("ANJ1505_E01", after.applied_event_ids)


if __name__ == "__main__":
    unittest.main()
