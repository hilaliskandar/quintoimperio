import unittest
from datetime import date

from quintoimperio.domain import ChronologyMode, HistoricalCampaignModel
from quintoimperio.domain.voyage_event import VoyageEventType


class DeferredVoyageEventTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = HistoricalCampaignModel()

    def malindi_guided_state(self, provisions=80.0):
        return self.model.initial_state(
            location_node="MAL",
            start_date=date(1498, 4, 24),
            provision_days=provisions,
            active_expedition_id="EXP_GAMA_1497",
            expedition_leg_sequence=10,
            chronology_mode=ChronologyMode.GUIDED,
        )

    def test_playable_plan_does_not_reveal_specific_event(self):
        state = self.malindi_guided_state()
        for seed in (0, 1, 7, 42, 1498):
            plan = self.model.plan_current_leg(state, seed=seed)
            self.assertTrue(plan.feasible)
            self.assertFalse(plan.events_resolved)
            self.assertEqual(plan.events, ())
            self.assertEqual(plan.event_provision_delta, 0.0)
            self.assertEqual(plan.travel_days, 27)
            self.assertEqual(plan.arrival_date, date(1498, 5, 21))
            self.assertTrue(plan.timing_events_suppressed_by_observation)

    def test_execution_resolves_and_logs_event_reproducibly(self):
        state = self.malindi_guided_state()
        chosen = None
        for seed in range(5000):
            event = self.model.session.travel.events.select(
                "R_MAL_CAL",
                date(1498, 4, 24),
                seed=seed,
                timing_safe_only=True,
            )
            if event:
                chosen = seed
                break
        self.assertIsNotNone(chosen)
        plan = self.model.plan_current_leg(state, seed=chosen)
        self.assertEqual(plan.events, ())
        first = self.model.execute_voyage(state, plan)
        second = self.model.execute_voyage(state, plan)
        self.assertEqual(first, second)
        self.assertEqual(len(first.voyage_event_history), 1)
        self.assertTrue(first.voyage_event_history[0].observed_timing_safe)
        self.assertEqual(first.vessel.clock.current_date, date(1498, 5, 21))

    def test_spoilage_is_not_a_predeparture_block_when_baseline_is_sufficient(self):
        state = self.malindi_guided_state(provisions=28.0)
        chosen = None
        for seed in range(5000):
            event = self.model.session.travel.events.select(
                "R_MAL_CAL",
                date(1498, 4, 24),
                seed=seed,
                timing_safe_only=True,
            )
            if event and event[0].event_type is VoyageEventType.PROVISION_SPOILAGE:
                chosen = seed
                break
        self.assertIsNotNone(chosen)
        plan = self.model.plan_current_leg(state, seed=chosen)
        self.assertTrue(plan.feasible)
        self.assertNotIn("INSUFFICIENT_PROVISIONS", plan.blockers)
        self.assertEqual(plan.events, ())

        after = self.model.execute_voyage(state, plan)
        self.assertEqual(len(after.voyage_event_history), 1)
        self.assertLess(after.voyage_event_history[0].provision_delta, 0)
        self.assertEqual(after.vessel.provision_days, 0.0)

    def test_counterfactual_timing_event_is_hidden_until_execution(self):
        state = self.model.initial_state(
            location_node="MAL",
            start_date=date(1498, 4, 24),
            provision_days=120.0,
            active_expedition_id="EXP_GAMA_1497",
            expedition_leg_sequence=10,
            chronology_mode=ChronologyMode.COUNTERFACTUAL,
        )
        chosen = None
        for seed in range(5000):
            event = self.model.session.travel.events.select(
                "R_MAL_CAL", date(1498, 4, 24), seed=seed
            )
            if event and event[0].extra_days > 0:
                chosen = seed
                break
        self.assertIsNotNone(chosen)
        plan = self.model.plan_current_leg(state, seed=chosen)
        self.assertEqual(plan.events, ())
        self.assertEqual(plan.travel_days, 27)
        after = self.model.execute_voyage(state, plan)
        self.assertGreater(after.vessel.clock.current_date, date(1498, 5, 21))
        self.assertTrue(after.voyage_event_history)


if __name__ == "__main__":
    unittest.main()
