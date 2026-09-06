import unittest
from dataclasses import replace
from datetime import date

from quintoimperio.domain import (
    ChronologyMode,
    HistoricalCampaignModel,
    KnowledgeLevel,
)


class MVPRobustnessTests(unittest.TestCase):
    SEEDS = (0, 1, 7, 42, 1498)

    @classmethod
    def setUpClass(cls):
        cls.model = HistoricalCampaignModel()

    def _execute_current_leg(self, state, seed=1498):
        plan = self.model.plan_current_leg(state, seed=seed)
        self.assertTrue(
            plan.feasible,
            (plan.route_id, plan.blockers, state.vessel.clock.current_date, seed),
        )
        return self.model.execute_voyage(state, plan)

    def _guided_to_calicut(self, seed=1498):
        state = self.model.initial_state(active_expedition_id="EXP_GAMA_1497")

        state = self._execute_current_leg(state, seed)
        for _ in range(3):
            result = self.model.reprovision(state, 30.0)
            self.assertTrue(result.executed)
            state = result.state_after
        state = self.model.wait_for_guided_departure(state).state_after

        state = self._execute_current_leg(state, seed)
        state = self.model.wait_for_guided_departure(state).state_after
        state = self._execute_current_leg(state, seed)
        state = self._execute_current_leg(state, seed)

        for _ in range(4):
            result = self.model.reprovision(state, 30.0)
            self.assertTrue(result.executed)
            state = result.state_after
        state = self.model.wait_for_guided_departure(state).state_after

        state = self._execute_current_leg(state, seed)
        result = self.model.reprovision(state, 30.0)
        self.assertTrue(result.executed)
        state = result.state_after
        state = self.model.wait_for_guided_departure(state).state_after

        state = self._execute_current_leg(state, seed)
        result = self.model.reprovision(state, 30.0)
        self.assertTrue(result.executed)
        state = result.state_after
        state = self.model.wait_for_guided_departure(state).state_after

        state = self._execute_current_leg(state, seed)
        state = self.model.wait_for_guided_departure(state).state_after
        state = self._execute_current_leg(state, seed)
        state = self.model.wait_for_guided_departure(state).state_after
        state = self._execute_current_leg(state, seed)

        contacted = self.model.contact_authority(state)
        self.assertTrue(contacted.executed)
        state = contacted.state_after
        state = self.model.wait_for_guided_departure(state).state_after
        state = self._execute_current_leg(state, seed)
        return state

    def test_guided_campaign_preserves_chronology_across_stochastic_seeds(self):
        terminal_states = []
        for seed in self.SEEDS:
            state = self._guided_to_calicut(seed)
            self.assertEqual(state.vessel.location_node, "CAL")
            self.assertEqual(state.vessel.clock.current_date, date(1498, 5, 21))
            self.assertEqual(state.chronology_mode, ChronologyMode.GUIDED)
            self.assertTrue(
                all(
                    event.observed_timing_safe and event.extra_days == 0
                    for event in state.voyage_event_history
                )
            )
            terminal_states.append(state)

        # A cronologia permanece invariável; recursos e histórico de eventos
        # podem variar por seed a partir da v0.2.
        signatures = {
            (round(state.vessel.provision_days, 6), state.voyage_event_history)
            for state in terminal_states
        }
        self.assertGreater(len(signatures), 1)

    def test_counterfactual_events_are_bounded_and_deterministic(self):
        state = self.model.initial_state(
            location_node="MOZ",
            start_date=date(1498, 3, 30),
            provision_days=120.0,
            condition=100.0,
            active_expedition_id="EXP_GAMA_1497",
            expedition_leg_sequence=8,
            chronology_mode=ChronologyMode.COUNTERFACTUAL,
        )

        eventful = 0
        for seed in range(100):
            first = self.model.plan_current_leg(state, seed=seed)
            second = self.model.plan_current_leg(state, seed=seed)
            self.assertEqual(first, second)
            self.assertTrue(first.feasible, (seed, first.blockers))
            self.assertLessEqual(len(first.events), 1)
            if first.events:
                eventful += 1
                event = first.events[0]
                self.assertLessEqual(event.extra_days, 3)
                self.assertLessEqual(event.condition_loss, 5.0)
                self.assertGreaterEqual(event.provision_delta, -8.0)
                self.assertLessEqual(event.provision_delta, 5.0)
                self.assertTrue(event.simulation_only)

        self.assertLess(eventful, 70)

    def test_same_market_round_trip_cannot_create_free_capital(self):
        state = self._guided_to_calicut()
        access = self.model.negotiate_access(state)
        self.assertTrue(access.executed)
        state = access.state_after
        market = self.model.market_view(state, seed=1498)
        self.assertTrue(market.actionable)
        self.assertIn("PEPPER", {entry.good_id for entry in market.entries})

        initial_capital = state.commerce.capital_index
        capital_series = [initial_capital]
        for _ in range(5):
            bought = self.model.buy(state, "PEPPER", 1.0, seed=1498)
            self.assertTrue(bought.executed, bought.reasons)
            state = bought.state_after
            sold = self.model.sell(state, "PEPPER", 1.0, seed=1498)
            self.assertTrue(sold.executed, sold.reasons)
            state = sold.state_after
            capital_series.append(state.commerce.capital_index)

        self.assertLess(state.commerce.capital_index, initial_capital)
        self.assertTrue(
            all(later < earlier for earlier, later in zip(capital_series, capital_series[1:]))
        )

    def test_unknown_market_and_uncontacted_actors_do_not_leak(self):
        state = self.model.initial_state(
            location_node="HUR",
            start_date=date(1498, 1, 1),
        )
        self.assertLess(
            self.model.node_state(state, "HUR").market,
            KnowledgeLevel.OPERATIONAL,
        )
        market = self.model.market_view(state, seed=1498)
        self.assertFalse(market.actionable)
        self.assertEqual(market.entries, ())
        self.assertEqual(self.model.contacted_relationships(state), ())

    def test_waiting_does_not_generate_material_resources(self):
        state = self.model.initial_state(
            location_node="MOZ",
            start_date=date(1498, 3, 2),
            provision_days=41.0,
            condition=73.0,
            capital_index=87.0,
            active_expedition_id="EXP_GAMA_1497",
            expedition_leg_sequence=8,
            chronology_mode=ChronologyMode.GUIDED,
        )
        before = state
        waited = self.model.wait_for_guided_departure(state)
        self.assertTrue(waited.executed)
        after = waited.state_after
        self.assertGreater(after.vessel.clock.current_date, before.vessel.clock.current_date)
        self.assertEqual(after.vessel.provision_days, before.vessel.provision_days)
        self.assertEqual(after.vessel.condition, before.vessel.condition)
        self.assertEqual(after.commerce, before.commerce)
        self.assertEqual(after.node_knowledge, before.node_knowledge)
        self.assertEqual(after.route_knowledge, before.route_knowledge)
        self.assertEqual(after.relationship_records, before.relationship_records)


if __name__ == "__main__":
    unittest.main()
