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

    def advance_to_mozambique(self):
        state = self.model.initial_cabral_state(provision_days=180.0)
        first = self.model.plan_current_leg(state, seed=1500)
        at_vera_cruz = self.model.execute_voyage(state, first)
        waited = self.model.wait_for_stop_release(at_vera_cruz)
        self.assertTrue(waited.executed)
        second = self.model.plan_current_leg(waited.state_after, seed=1500)
        self.assertTrue(second.feasible, second.blockers)
        return self.model.execute_voyage(waited.state_after, second)

    def advance_to_kilwa(self):
        at_mozambique = self.advance_to_mozambique()
        plan = self.model.plan_current_leg(at_mozambique, seed=1500)
        self.assertTrue(plan.feasible, plan.blockers)
        return self.model.execute_voyage(at_mozambique, plan)

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
        self.assertEqual(at_mozambique.active_expedition_id, "EXP_CABRAL_1500")
        self.assertEqual(at_mozambique.expedition_leg_sequence, 3)
        self.assertIsNone(at_mozambique.active_stop_id)

    def test_mozambique_to_kilwa_reaches_documented_reunion_and_activates_stop(self):
        at_mozambique = self.advance_to_mozambique()
        plan = self.model.plan_current_leg(at_mozambique, seed=1500)
        self.assertTrue(plan.feasible, plan.blockers)
        self.assertEqual(plan.route_id, "R_MOZ_KIL_CAB")
        self.assertEqual(plan.navigation_basis, NavigationBasis.FLEET_COMMAND)
        self.assertEqual(plan.travel_days, 6)
        self.assertEqual(plan.arrival_date, date(1500, 7, 26))

        at_kilwa = self.model.execute_voyage(at_mozambique, plan)
        self.assertEqual(at_kilwa.vessel.location_node, "KIL")
        self.assertEqual(at_kilwa.vessel.clock.current_date, date(1500, 7, 26))
        self.assertEqual(at_kilwa.active_stop_id, "CABRAL1500_KIL")
        stop = self.model.active_stop(at_kilwa)
        self.assertIsNotNone(stop)
        assert stop is not None
        self.assertEqual(stop.departure_date, date(1500, 7, 29))
        self.assertEqual(stop.activities, ("FLEET_REUNION",))

    def test_kilwa_stop_releases_on_july_29_and_leg_reaches_malindi(self):
        at_kilwa = self.advance_to_kilwa()
        blocked = self.model.plan_current_leg(at_kilwa, seed=1500)
        self.assertFalse(blocked.feasible)
        self.assertIn("HISTORICAL_STOP_NOT_RELEASED", blocked.blockers)

        waited = self.model.wait_for_stop_release(at_kilwa)
        self.assertTrue(waited.executed)
        self.assertEqual(waited.state_after.vessel.clock.current_date, date(1500, 7, 29))
        plan = self.model.plan_current_leg(waited.state_after, seed=1500)
        self.assertTrue(plan.feasible, plan.blockers)
        self.assertEqual(plan.route_id, "R_KIL_MAL_CAB")
        self.assertEqual(plan.navigation_basis, NavigationBasis.FLEET_COMMAND)
        self.assertEqual(plan.travel_days, 4)
        self.assertEqual(plan.arrival_date, date(1500, 8, 2))

        at_malindi = self.model.execute_voyage(waited.state_after, plan)
        self.assertEqual(at_malindi.vessel.location_node, "MAL")
        self.assertEqual(at_malindi.vessel.clock.current_date, date(1500, 8, 2))
        self.assertEqual(at_malindi.active_stop_id, "CABRAL1500_MAL")
        stop = self.model.active_stop(at_malindi)
        self.assertIsNotNone(stop)
        assert stop is not None
        self.assertEqual(stop.departure_date, date(1500, 8, 7))
        self.assertEqual(
            stop.activities,
            ("DIPLOMATIC_CONTACT", "DEGREDADOS_DISEMBARKED", "PILOTS_PROVIDED"),
        )
        self.assertIsNone(at_malindi.active_expedition_id)
        self.assertIsNone(at_malindi.expedition_leg_sequence)

    def test_two_gujarati_pilots_remain_documentary_event_in_1500(self):
        events = self.expedition_events.preferred_for_expedition("EXP_CABRAL_1500")
        pilots = [event for event in events if event.event_id == "CABRAL1500_E08"]
        self.assertEqual(len(pilots), 1)
        event = pilots[0]
        self.assertEqual(event.event_type, "PILOTS_PROVIDED")
        self.assertEqual(event.subject_label, "Dois pilotos guzerates")
        self.assertEqual(event.date_from, date(1500, 8, 6))
        self.assertEqual(event.date_to, date(1500, 8, 6))
        self.assertNotIn("PIL_MAL_GUJ_1498", self.model.session.travel.pilots_for_route("R_KIL_MAL_CAB", date(1500, 8, 2), "KIL"))

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
