import unittest
from datetime import date

from quintoimperio.domain import (
    ExpeditionEventModel,
    KnowledgeLevel,
    NavigationBasis,
    P3CampaignModel,
)


class P3CampaignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = P3CampaignModel()
        cls.expedition_events = ExpeditionEventModel()

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
        self.assertEqual(after.active_expedition_id, "EXP_CABRAL_1500")
        self.assertEqual(after.expedition_leg_sequence, 2)
        self.assertEqual(after.active_stop_id, "CABRAL1500_VCR")

    def test_vera_cruz_stop_blocks_early_departure_and_second_leg_reaches_mozambique(self):
        state = self.model.initial_cabral_state(provision_days=180.0)
        first = self.model.plan_current_leg(state, seed=1500)
        at_vera_cruz = self.model.execute_voyage(state, first)
        second = self.model.plan_current_leg(at_vera_cruz, seed=1500)
        self.assertFalse(second.feasible)
        self.assertIn("HISTORICAL_STOP_NOT_RELEASED", second.blockers)

        waited = self.model.wait_for_stop_release(at_vera_cruz)
        self.assertTrue(waited.executed)
        self.assertEqual(waited.state_after.vessel.clock.current_date, date(1500, 5, 2))

        released = self.model.plan_current_leg(waited.state_after, seed=1500)
        self.assertTrue(released.feasible, released.blockers)
        self.assertEqual(released.route_id, "R_VCR_MOZ_CAB")
        self.assertEqual(released.navigation_basis, NavigationBasis.FLEET_COMMAND)
        self.assertEqual(released.travel_days, 79)
        self.assertEqual(released.arrival_date, date(1500, 7, 20))

        at_mozambique = self.model.execute_voyage(waited.state_after, released)
        self.assertEqual(at_mozambique.vessel.location_node, "MOZ")
        self.assertEqual(at_mozambique.vessel.clock.current_date, date(1500, 7, 20))
        self.assertIsNone(at_mozambique.active_expedition_id)
        self.assertIsNone(at_mozambique.expedition_leg_sequence)

    def test_cape_is_documentary_marker_not_operational_stop(self):
        route = self.model.session.routes["R_VCR_CGH_CAB"]
        self.assertEqual(route["route_type"], "STRATEGIC_AGGREGATE")
        self.assertNotEqual(
            self.model.current_leg(
                self.model.initial_cabral_state(provision_days=180.0)
            ).route_id,
            "R_VCR_CGH_CAB",
        )

    def test_cape_losses_remain_documentary_events_not_generic_wreck_mechanics(self):
        events = self.expedition_events.preferred_for_expedition("EXP_CABRAL_1500")
        losses = [event for event in events if event.event_id == "CABRAL1500_E03"]
        splits = [event for event in events if event.event_id == "CABRAL1500_E04"]
        self.assertEqual(len(losses), 1)
        self.assertEqual(losses[0].event_type, "VESSEL_LOSS")
        self.assertEqual(losses[0].date_from, date(1500, 5, 23))
        self.assertEqual(losses[0].date_to, date(1500, 5, 24))
        self.assertEqual(len(splits), 1)
        self.assertEqual(splits[0].trajectory_id, "DIOGO_DIAS_SPLIT")

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
