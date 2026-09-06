import unittest
from datetime import date

from quintoimperio.domain import (
    AccessStatus,
    ChronologyMode,
    HistoricalCampaignModel,
    KnowledgeLevel,
    NavigationBasis,
)


class HistoricalCampaignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = HistoricalCampaignModel()

    def _execute_current_leg(self, state):
        plan = self.model.plan_current_leg(state, seed=1498)
        self.assertTrue(plan.feasible, (plan.route_id, plan.blockers, state.vessel.clock.current_date))
        return self.model.execute_voyage(state, plan), plan

    def test_guided_campaign_runs_lisbon_to_calicut(self):
        state = self.model.initial_state(active_expedition_id="EXP_GAMA_1497")
        expected_routes = [
            "R_LIS_STG",
            "R_STG_SHB",
            "R_SHB_CGH",
            "R_CGH_SBR",
            "R_SBR_RCO",
            "R_RCO_RBS",
            "R_RBS_MOZ",
            "R_MOZ_MOM",
            "R_MOM_MAL",
            "R_MAL_CAL",
        ]
        seen_routes = []
        seen_stops = []

        state, plan = self._execute_current_leg(state)
        seen_routes.append(plan.route_id)
        seen_stops.append(self.model.active_stop(state).stop_id)
        self.assertEqual(state.vessel.clock.current_date, date(1497, 7, 27))

        for _ in range(3):
            result = self.model.reprovision(state, 30.0)
            self.assertTrue(result.executed)
            state = result.state_after
        waited = self.model.wait_for_guided_departure(state)
        self.assertTrue(waited.executed)
        state = waited.state_after
        self.assertEqual(state.vessel.clock.current_date, date(1497, 8, 3))

        state, plan = self._execute_current_leg(state)
        seen_routes.append(plan.route_id)
        seen_stops.append(self.model.active_stop(state).stop_id)
        self.assertEqual(state.vessel.clock.current_date, date(1497, 11, 7))

        state = self.model.wait_for_guided_departure(state).state_after
        state, plan = self._execute_current_leg(state)
        seen_routes.append(plan.route_id)
        self.assertIsNone(self.model.active_stop(state))
        self.assertEqual(state.vessel.clock.current_date, date(1497, 11, 22))

        state, plan = self._execute_current_leg(state)
        seen_routes.append(plan.route_id)
        seen_stops.append(self.model.active_stop(state).stop_id)
        self.assertEqual(state.vessel.clock.current_date, date(1497, 11, 25))

        for _ in range(4):
            result = self.model.reprovision(state, 30.0)
            self.assertTrue(result.executed)
            state = result.state_after
        state = self.model.wait_for_guided_departure(state).state_after
        state, plan = self._execute_current_leg(state)
        seen_routes.append(plan.route_id)
        seen_stops.append(self.model.active_stop(state).stop_id)
        self.assertEqual(state.vessel.clock.current_date, date(1498, 1, 11))

        result = self.model.reprovision(state, 30.0)
        self.assertTrue(result.executed)
        state = result.state_after
        state = self.model.wait_for_guided_departure(state).state_after
        state, plan = self._execute_current_leg(state)
        seen_routes.append(plan.route_id)
        seen_stops.append(self.model.active_stop(state).stop_id)
        self.assertEqual(state.vessel.clock.current_date, date(1498, 1, 24))

        result = self.model.reprovision(state, 30.0)
        self.assertTrue(result.executed)
        state = result.state_after
        state = self.model.wait_for_guided_departure(state).state_after
        state, plan = self._execute_current_leg(state)
        seen_routes.append(plan.route_id)
        self.assertIsNone(self.model.active_stop(state))
        self.assertEqual(state.vessel.clock.current_date, date(1498, 3, 2))

        state = self.model.wait_for_guided_departure(state).state_after
        self.assertEqual(state.vessel.clock.current_date, date(1498, 3, 29))
        state, plan = self._execute_current_leg(state)
        seen_routes.append(plan.route_id)
        self.assertEqual(state.vessel.clock.current_date, date(1498, 4, 7))

        state = self.model.wait_for_guided_departure(state).state_after
        self.assertEqual(state.vessel.clock.current_date, date(1498, 4, 13))
        state, plan = self._execute_current_leg(state)
        seen_routes.append(plan.route_id)
        self.assertEqual(state.vessel.clock.current_date, date(1498, 4, 14))

        self.assertIsNone(self.model.recommended_pilot_id(state, "R_MAL_CAL"))
        access_before = self.model.access_status(state, "MAL")
        contacted = self.model.contact_authority(state)
        self.assertTrue(contacted.executed)
        state = contacted.state_after
        self.assertEqual(state.vessel.clock.current_date, date(1498, 4, 15))
        self.assertEqual(self.model.access_status(state, "MAL"), access_before)

        state = self.model.wait_for_guided_departure(state).state_after
        self.assertEqual(state.vessel.clock.current_date, date(1498, 4, 24))
        final_plan = self.model.plan_current_leg(state, seed=1498)
        self.assertEqual(final_plan.route_id, "R_MAL_CAL")
        self.assertEqual(final_plan.pilot_id, "PIL_MAL_GUJ_1498")
        self.assertEqual(final_plan.navigation_basis, NavigationBasis.PILOT)
        self.assertTrue(final_plan.feasible)
        state = self.model.execute_voyage(state, final_plan)
        seen_routes.append(final_plan.route_id)

        self.assertEqual(seen_routes, expected_routes)
        self.assertEqual(
            seen_stops,
            [
                "GAMA1497_STG",
                "GAMA1497_SHB",
                "GAMA1497_SBR",
                "GAMA1498_RCO",
                "GAMA1498_RBS",
            ],
        )
        self.assertEqual(state.vessel.location_node, "CAL")
        self.assertEqual(state.vessel.clock.current_date, date(1498, 5, 21))
        self.assertIsNone(state.active_expedition_id)
        self.assertIsNone(state.expedition_leg_sequence)
        self.assertEqual(state.chronology_mode, ChronologyMode.GUIDED)
        self.assertGreaterEqual(
            self.model.node_state(state, "CAL").market,
            KnowledgeLevel.OPERATIONAL,
        )
        self.assertEqual(
            self.model.access_status(state, "CAL"),
            AccessStatus.NEGOTIATION_REQUIRED,
        )

    def test_guided_wait_changes_only_clock(self):
        state = self.model.initial_state(
            location_node="MOZ",
            start_date=date(1498, 3, 2),
            provision_days=77.0,
            condition=91.0,
            capital_index=83.0,
            active_expedition_id="EXP_GAMA_1497",
            expedition_leg_sequence=8,
            chronology_mode=ChronologyMode.GUIDED,
        )
        before_commerce = state.commerce
        before_nodes = state.node_knowledge
        before_routes = state.route_knowledge
        before_access = state.access_records
        before_relationships = state.relationship_records
        before_information = state.information_history
        before_events = state.voyage_event_history
        before_provisions = state.vessel.provision_days
        before_condition = state.vessel.condition

        waited = self.model.wait_for_guided_departure(state)
        self.assertTrue(waited.executed)
        after = waited.state_after
        self.assertEqual(after.vessel.clock.current_date, date(1498, 3, 29))
        self.assertEqual(after.vessel.provision_days, before_provisions)
        self.assertEqual(after.vessel.condition, before_condition)
        self.assertEqual(after.commerce, before_commerce)
        self.assertEqual(after.node_knowledge, before_nodes)
        self.assertEqual(after.route_knowledge, before_routes)
        self.assertEqual(after.access_records, before_access)
        self.assertEqual(after.relationship_records, before_relationships)
        self.assertEqual(after.information_history, before_information)
        self.assertEqual(after.voyage_event_history, before_events)

    def test_guided_departure_blocks_early_departure_without_normalized_stop(self):
        state = self.model.initial_state(
            location_node="MOZ",
            start_date=date(1498, 3, 2),
            provision_days=120.0,
            active_expedition_id="EXP_GAMA_1497",
            expedition_leg_sequence=8,
            chronology_mode=ChronologyMode.GUIDED,
        )
        self.assertIsNone(self.model.active_stop(state))
        self.assertEqual(self.model.guided_departure_date(state), date(1498, 3, 29))

        blocked = self.model.plan_current_leg(state, seed=1498)
        self.assertFalse(blocked.feasible)
        self.assertIn("HISTORICAL_DEPARTURE_NOT_REACHED", blocked.blockers)

        waited = self.model.wait_for_guided_departure(state)
        self.assertTrue(waited.executed)
        self.assertEqual(waited.days_waited, 27)
        plan = self.model.plan_current_leg(waited.state_after, seed=1498)
        self.assertTrue(plan.feasible)
        self.assertTrue(plan.timing_events_suppressed_by_observation)
        self.assertFalse(plan.events_resolved)
        self.assertEqual(plan.events, ())

    def test_late_guided_departure_becomes_counterfactual_and_stays_so(self):
        state = self.model.initial_state(
            location_node="MOZ",
            start_date=date(1498, 3, 2),
            provision_days=120.0,
            active_expedition_id="EXP_GAMA_1497",
            expedition_leg_sequence=8,
            chronology_mode=ChronologyMode.GUIDED,
        )
        state = self.model.wait_for_guided_departure(state).state_after
        access = self.model.negotiate_access(state)
        self.assertTrue(access.executed)
        state = access.state_after
        self.assertEqual(state.vessel.clock.current_date, date(1498, 3, 30))

        plan = self.model.plan_current_leg(state, seed=1498)
        self.assertTrue(plan.feasible)
        state = self.model.execute_voyage(state, plan)
        self.assertEqual(state.chronology_mode, ChronologyMode.COUNTERFACTUAL)

        wait = self.model.wait_for_guided_departure(state)
        self.assertFalse(wait.executed)
        self.assertIn("COUNTERFACTUAL_CHRONOLOGY_NO_FORCED_WAIT", wait.reasons)
        next_plan = self.model.plan_current_leg(state, seed=1498)
        self.assertTrue(next_plan.feasible)
        state = self.model.execute_voyage(state, next_plan)
        self.assertEqual(state.chronology_mode, ChronologyMode.COUNTERFACTUAL)

    def test_strategic_aggregate_remains_non_executable(self):
        state = self.model.initial_state(active_expedition_id="EXP_GAMA_1497")
        plan = self.model.plan_voyage(state, "R_LIS_CGH", seed=1498)
        self.assertFalse(plan.feasible)
        self.assertIn("STRATEGIC_AGGREGATE_NOT_EXECUTABLE", plan.blockers)


if __name__ == "__main__":
    unittest.main()
