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
from quintoimperio.domain.voyage_event import VoyageEventModel


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

    def test_event_effects_remain_inside_declared_v01_limits(self):
        found = None
        for seed in range(1000):
            candidate = self.events.select("R_CAL_ADE", date(1498, 5, 22), seed=seed)
            if candidate:
                found = candidate[0]
                break
        self.assertIsNotNone(found)
        assert found is not None
        self.assertGreaterEqual(found.extra_days, 0)
        self.assertLessEqual(found.extra_days, 3)
        self.assertGreaterEqual(found.condition_loss, 0.0)
        self.assertLessEqual(found.condition_loss, 5.0)
        self.assertTrue(found.simulation_only)

    def test_guided_exact_observation_suppresses_random_events(self):
        plan = self.travel.plan_voyage(
            self.malindi_state(),
            "R_MAL_CAL",
            KnowledgeLevel.OPERATIONAL,
            seed=13,
            preserve_observed_timing=True,
        )
        self.assertTrue(plan.events_suppressed_by_observation)
        self.assertEqual(plan.events, ())
        self.assertEqual(plan.travel_days, 27)
        self.assertEqual(plan.arrival_date, date(1498, 5, 21))

    def test_counterfactual_exact_departure_can_receive_event(self):
        selected = None
        for seed in range(1000):
            plan = self.travel.plan_voyage(
                self.malindi_state(),
                "R_MAL_CAL",
                KnowledgeLevel.OPERATIONAL,
                seed=seed,
                preserve_observed_timing=False,
            )
            if plan.events:
                selected = plan
                break
        self.assertIsNotNone(selected)
        assert selected is not None
        self.assertFalse(selected.events_suppressed_by_observation)
        self.assertGreaterEqual(selected.travel_days, 27)
        self.assertGreaterEqual(selected.estimated_duration_days, 26.5)

    def test_event_delay_consumes_provisions_and_event_damage_affects_condition(self):
        selected = None
        for seed in range(1000):
            plan = self.travel.plan_voyage(
                VesselState(
                    location_node="CAL",
                    clock=GameClock(date(1498, 5, 22)),
                    provision_days=200.0,
                    condition=100.0,
                ),
                "R_CAL_ADE",
                KnowledgeLevel.OPERATIONAL,
                seed=seed,
                preserve_observed_timing=False,
            )
            if plan.events:
                selected = plan
                break
        self.assertIsNotNone(selected)
        assert selected is not None
        self.assertEqual(selected.provision_days_required, float(selected.travel_days))
        self.assertLessEqual(selected.condition_after, selected.condition_before)


class VoyageEventSessionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = GameSessionModel()

    def test_guided_session_preserves_exact_first_leg(self):
        state = self.session.initial_state(
            active_expedition_id="EXP_GAMA_1497",
            provision_days=120.0,
        )
        self.assertEqual(state.chronology_mode, ChronologyMode.GUIDED)
        plan = self.session.plan_voyage(state, "R_LIS_STG", seed=17)
        self.assertTrue(plan.events_suppressed_by_observation)
        self.assertEqual(plan.events, ())
        after = self.session.execute_voyage(state, plan)
        self.assertEqual(after.voyage_event_history, ())

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
        for seed in range(1000):
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
