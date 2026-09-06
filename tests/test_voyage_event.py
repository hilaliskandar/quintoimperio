import unittest
from datetime import date

from quintoimperio.domain import (
    ChronologyMode,
    GameClock,
    GameSessionModel,
    KnowledgeLevel,
    TravelModel,
    VesselState,
)
from quintoimperio.domain.voyage_event import VoyageEventModel, VoyageEventType


class VoyageEventModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.events = VoyageEventModel()
        cls.travel = TravelModel()

    def malindi_state(self):
        return VesselState(
            location_node="MAL",
            clock=GameClock(date(1498, 4, 24)),
            provision_days=80.0,
            condition=100.0,
        )

    def test_selection_is_deterministic_for_same_seed(self):
        a = self.events.select("R_CAL_ADE", date(1498, 5, 22), seed=77)
        b = self.events.select("R_CAL_ADE", date(1498, 5, 22), seed=77)
        self.assertEqual(a, b)

    def test_event_effects_remain_inside_declared_v02_limits(self):
        found = []
        for seed in range(1000):
            candidate = self.events.select("R_CAL_ADE", date(1498, 5, 22), seed=seed)
            if candidate:
                found.append(candidate[0])
        self.assertTrue(found)
        self.assertTrue(all(0 <= event.extra_days <= 3 for event in found))
        self.assertTrue(all(0.0 <= event.condition_loss <= 5.0 for event in found))
        self.assertTrue(all(-8.0 <= event.provision_delta <= 5.0 for event in found))
        self.assertTrue(all(event.simulation_only for event in found))

    def test_positive_and_negative_resource_events_are_reachable(self):
        types = set()
        for seed in range(5000):
            candidate = self.events.select(
                "R_MAL_CAL",
                date(1498, 4, 24),
                seed=seed,
                timing_safe_only=True,
            )
            if candidate:
                types.add(candidate[0].event_type)
            if {
                VoyageEventType.PROVISION_SPOILAGE,
                VoyageEventType.EFFICIENT_RATIONING,
            }.issubset(types):
                break
        self.assertIn(VoyageEventType.PROVISION_SPOILAGE, types)
        self.assertIn(VoyageEventType.EFFICIENT_RATIONING, types)

    def test_guided_exact_observation_preserves_timing_but_can_change_resources(self):
        selected = None
        for seed in range(5000):
            plan = self.travel.plan_voyage(
                self.malindi_state(),
                "R_MAL_CAL",
                KnowledgeLevel.OPERATIONAL,
                seed=seed,
                preserve_observed_timing=True,
            )
            if plan.events:
                selected = plan
                break
        self.assertIsNotNone(selected)
        assert selected is not None
        self.assertTrue(selected.events_suppressed_by_observation)
        self.assertTrue(all(event.observed_timing_safe for event in selected.events))
        self.assertEqual(selected.travel_days, 27)
        self.assertEqual(selected.arrival_date, date(1498, 5, 21))
        self.assertNotEqual(selected.event_provision_delta, 0.0)
        self.assertEqual(
            selected.provision_days_after,
            80.0 - selected.provision_days_required + selected.event_provision_delta,
        )

    def test_counterfactual_exact_departure_can_receive_timing_event(self):
        selected = None
        for seed in range(5000):
            plan = self.travel.plan_voyage(
                self.malindi_state(),
                "R_MAL_CAL",
                KnowledgeLevel.OPERATIONAL,
                seed=seed,
                preserve_observed_timing=False,
            )
            if any(event.extra_days > 0 for event in plan.events):
                selected = plan
                break
        self.assertIsNotNone(selected)
        assert selected is not None
        self.assertFalse(selected.events_suppressed_by_observation)
        self.assertGreater(selected.travel_days, 27)

    def test_negative_provision_event_can_block_marginal_voyage(self):
        selected = None
        state = VesselState(
            location_node="MAL",
            clock=GameClock(date(1498, 4, 24)),
            provision_days=28.0,
            condition=100.0,
        )
        for seed in range(5000):
            plan = self.travel.plan_voyage(
                state,
                "R_MAL_CAL",
                KnowledgeLevel.OPERATIONAL,
                seed=seed,
                preserve_observed_timing=True,
            )
            if plan.event_provision_delta < 0:
                selected = plan
                break
        self.assertIsNotNone(selected)
        assert selected is not None
        self.assertIn("INSUFFICIENT_PROVISIONS", selected.blockers)


class VoyageEventSessionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = GameSessionModel()

    def test_guided_session_preserves_exact_first_leg_timing(self):
        state = self.session.initial_state(
            active_expedition_id="EXP_GAMA_1497",
            provision_days=120.0,
        )
        self.assertEqual(state.chronology_mode, ChronologyMode.GUIDED)
        plan = self.session.plan_voyage(state, "R_LIS_STG", seed=17)
        self.assertTrue(plan.events_suppressed_by_observation)
        self.assertTrue(all(event.observed_timing_safe for event in plan.events))

    def test_counterfactual_session_can_apply_and_log_event_on_exact_route_date(self):
        state = self.session.initial_state(
            location_node="MAL",
            start_date=date(1498, 4, 24),
            provision_days=120.0,
            chronology_mode=ChronologyMode.COUNTERFACTUAL,
        )
        state = self.session.scenario_set_route_knowledge(
            state, "R_MAL_CAL", KnowledgeLevel.OPERATIONAL
        )
        selected = None
        for seed in range(5000):
            candidate = self.session.plan_voyage(state, "R_MAL_CAL", seed=seed)
            if candidate.events:
                selected = candidate
                break
        self.assertIsNotNone(selected)
        assert selected is not None
        self.assertFalse(selected.events_suppressed_by_observation)
        after = self.session.execute_voyage(state, selected)
        self.assertEqual(after.voyage_event_history, selected.events)


if __name__ == "__main__":
    unittest.main()
