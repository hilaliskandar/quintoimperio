import unittest
from datetime import date

from quintoimperio.domain import KnowledgeLevel, NavigationBasis, P3CampaignModel


class P3CampaignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = P3CampaignModel()

    def test_cabral_state_uses_documented_expedition_and_departure(self):
        state = self.model.initial_cabral_state()
        self.assertEqual(state.active_expedition_id, "EXP_CABRAL_1500")
        self.assertEqual(state.expedition_leg_sequence, 1)
        self.assertEqual(state.vessel.location_node, "LIS")
        self.assertEqual(state.vessel.clock.current_date, date(1500, 3, 9))

    def test_cabral_first_leg_uses_documented_timing_and_fleet_command(self):
        state = self.model.initial_cabral_state(provision_days=180.0)
        plan = self.model.plan_current_leg(state, seed=1500)
        self.assertTrue(plan.feasible, plan.blockers)
        self.assertEqual(plan.route_id, "R_LIS_VCR_CAB")
        self.assertEqual(plan.navigation_basis, NavigationBasis.FLEET_COMMAND)
        self.assertEqual(plan.travel_days, 44)
        self.assertEqual(plan.arrival_date, date(1500, 4, 22))
        after = self.model.execute_voyage(state, plan)
        self.assertEqual(after.vessel.location_node, "VCR")
        self.assertEqual(after.vessel.clock.current_date, date(1500, 4, 22))
        self.assertIsNone(after.active_expedition_id)
        self.assertIsNone(after.expedition_leg_sequence)

    def test_fleet_command_does_not_pregrant_operational_route_knowledge(self):
        state = self.model.initial_cabral_state(provision_days=180.0)
        self.assertNotEqual(
            self.model.route_nav(state, "R_LIS_VCR_CAB"),
            KnowledgeLevel.OPERATIONAL,
        )
        plan = self.model.plan_current_leg(state, seed=1500)
        self.assertEqual(plan.navigation_basis, NavigationBasis.FLEET_COMMAND)
        after = self.model.execute_voyage(state, plan)
        self.assertEqual(
            self.model.route_nav(after, "R_LIS_VCR_CAB"),
            KnowledgeLevel.OPERATIONAL,
        )


if __name__ == "__main__":
    unittest.main()
