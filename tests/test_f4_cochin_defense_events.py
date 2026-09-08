import unittest
from datetime import date

from quintoimperio.domain import ExpeditionEventModel, ExpeditionModel, NodeStateEventModel


class F4CochinDefenseEventTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.expeditions = ExpeditionModel()
        cls.events = ExpeditionEventModel()
        cls.node_states = NodeStateEventModel()

    def test_resident_defense_subcampaign_is_documentary_and_not_playable(self):
        expedition_id = "EXP_DUARTE_PACHECO_DEFENSE_1504"
        expedition = self.expeditions.expeditions[expedition_id]

        self.assertEqual(expedition["leader"], "Duarte Pacheco Pereira")
        self.assertEqual(expedition["expedition_type"], "RESIDENT_DEFENSE_SUBCAMPAIGN")
        self.assertEqual(self.expeditions.legs.get(expedition_id, ()), ())
        with self.assertRaisesRegex(KeyError, "Expedicao sem pernas"):
            self.expeditions.first_sequence(expedition_id)

    def test_defense_events_become_available_only_at_conservative_upper_bounds(self):
        expedition_id = "EXP_DUARTE_PACHECO_DEFENSE_1504"

        before_march_end = self.events.available_by(expedition_id, date(1504, 3, 30))
        at_march_end = self.events.available_by(expedition_id, date(1504, 3, 31))
        before_may_end = self.events.available_by(expedition_id, date(1504, 5, 30))
        at_may_end = self.events.available_by(expedition_id, date(1504, 5, 31))
        before_july_end = self.events.available_by(expedition_id, date(1504, 7, 30))
        at_july_end = self.events.available_by(expedition_id, date(1504, 7, 31))

        self.assertNotIn("DPP1504_E01", {event.event_id for event in before_march_end})
        self.assertIn("DPP1504_E01", {event.event_id for event in at_march_end})
        self.assertNotIn("DPP1504_E02", {event.event_id for event in before_may_end})
        self.assertIn("DPP1504_E02", {event.event_id for event in at_may_end})
        self.assertNotIn("DPP1504_E03", {event.event_id for event in before_july_end})
        self.assertIn("DPP1504_E03", {event.event_id for event in at_july_end})

        preferred = self.events.preferred_for_expedition(expedition_id)
        self.assertEqual(
            [event.event_type for event in preferred],
            [
                "DEFENSE_CAMPAIGN_BEGINS",
                "DEFENSIVE_OPERATIONS_REPEATED",
                "DEFENSE_CAMPAIGN_ENDS",
            ],
        )

    def test_defense_events_do_not_change_cochin_sovereignty_or_inherited_presence(self):
        for on_date in (date(1504, 3, 31), date(1504, 5, 31), date(1504, 7, 31)):
            state = self.node_states.effective_state("COC", on_date)
            self.assertEqual(state.institutional_presence, "FACTORY_RESTORED")
            self.assertEqual(state.fortification_state, "PORTUGUESE_FORT")
            self.assertEqual(state.garrison_state, "PORTUGUESE_GARRISON")
            self.assertIn("soberania local", state.sovereignty_note.lower())


if __name__ == "__main__":
    unittest.main()
