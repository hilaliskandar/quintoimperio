import unittest
from datetime import date

from quintoimperio.domain import (
    ChronologyMode,
    NavigationBasis,
    NodeStateEventModel,
    P3CampaignModel,
)


class P3CalicutCochinTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = P3CampaignModel()
        cls.node_states = NodeStateEventModel()

    def advance_to_calicut(self):
        state = self.model.initial_cabral_state(provision_days=400.0)
        for _ in range(12):
            if state.vessel.location_node == "CAL":
                return state
            plan = self.model.plan_current_leg(state, seed=1500)
            if not plan.feasible and "HISTORICAL_STOP_NOT_RELEASED" in plan.blockers:
                waited = self.model.wait_for_stop_release(state)
                self.assertTrue(waited.executed)
                state = waited.state_after
                plan = self.model.plan_current_leg(state, seed=1500)
            self.assertTrue(plan.feasible, plan.blockers)
            state = self.model.execute_voyage(state, plan)
        self.fail("Cabral did not reach Calicut within the expected guided legs")

    def test_calicut_stop_blocks_until_rupture_then_reaches_cochin(self):
        at_calicut = self.advance_to_calicut()
        self.assertEqual(at_calicut.vessel.clock.current_date, date(1500, 9, 13))
        self.assertEqual(at_calicut.active_stop_id, "CABRAL1500_CAL")
        self.assertEqual(at_calicut.active_expedition_id, "EXP_CABRAL_1500")
        self.assertEqual(at_calicut.expedition_leg_sequence, 7)
        self.assertEqual(at_calicut.chronology_mode, ChronologyMode.GUIDED)

        blocked = self.model.plan_current_leg(at_calicut, seed=1500)
        self.assertFalse(blocked.feasible)
        self.assertIn("HISTORICAL_STOP_NOT_RELEASED", blocked.blockers)

        waited = self.model.wait_for_stop_release(at_calicut)
        self.assertTrue(waited.executed)
        self.assertEqual(waited.state_after.vessel.clock.current_date, date(1500, 12, 18))

        plan = self.model.plan_current_leg(waited.state_after, seed=1500)
        self.assertTrue(plan.feasible, plan.blockers)
        self.assertEqual(plan.route_id, "R_CAL_COC")
        self.assertEqual(plan.navigation_basis, NavigationBasis.FLEET_COMMAND)
        self.assertEqual(plan.travel_days, 6)
        self.assertEqual(plan.arrival_date, date(1500, 12, 24))

        at_cochin = self.model.execute_voyage(waited.state_after, plan)
        self.assertEqual(at_cochin.vessel.location_node, "COC")
        self.assertEqual(at_cochin.vessel.clock.current_date, date(1500, 12, 24))
        self.assertEqual(at_cochin.chronology_mode, ChronologyMode.GUIDED)
        self.assertIsNone(at_cochin.active_expedition_id)
        self.assertIsNone(at_cochin.expedition_leg_sequence)

    def test_calicut_rupture_is_temporal_state_not_combat_mechanic(self):
        before = self.node_states.effective_state("CAL", date(1500, 12, 17))
        self.assertNotIn("CAL1500_E01", before.applied_event_ids)

        after = self.node_states.effective_state("CAL", date(1500, 12, 18))
        self.assertIn("CAL1500_E01", after.applied_event_ids)
        self.assertEqual(after.institutional_presence, "NONE")
        self.assertEqual(after.access_state, "RESTRICTED")
        self.assertEqual(after.relationship_state, "HOSTILE")
        self.assertIn("Samorim", after.sovereignty_note)
        self.assertEqual(after.fortification_state, "NONE")
        self.assertEqual(after.garrison_state, "NONE")


if __name__ == "__main__":
    unittest.main()
