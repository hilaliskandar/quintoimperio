import unittest
from datetime import date

from quintoimperio.domain import (
    AccessStatus,
    GameSessionModel,
    KnowledgeLevel,
    KnowledgeState,
    PortServiceKind,
    RouteKnowledgeModel,
)


class RouteKnowledgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = RouteKnowledgeModel()

    def test_route_knowledge_is_distinct_from_node_knowledge(self):
        self.assertEqual(
            self.model.initial_for_route("R_LIS_CGH", "PLAYER"),
            KnowledgeLevel.PARTIAL,
        )
        self.assertEqual(
            self.model.initial_for_route("R_LIS_CGH", "CROWN"),
            KnowledgeLevel.OPERATIONAL,
        )

    def test_unknown_player_route_stays_unknown(self):
        self.assertEqual(
            self.model.initial_for_route("R_MAL_CAL", "PLAYER"),
            KnowledgeLevel.UNKNOWN,
        )


class GameSessionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = GameSessionModel()

    def test_initial_session_preserves_indirect_calicut_market_knowledge(self):
        state = self.model.initial_state()
        calicut = self.model.node_state(state, "CAL")
        self.assertEqual(calicut.market, KnowledgeLevel.RUMORED)
        self.assertEqual(
            self.model.route_nav(state, "R_CAL_ADE"), KnowledgeLevel.UNKNOWN
        )
        self.assertEqual(
            self.model.access_status(state, "CAL"), AccessStatus.NEGOTIATION_REQUIRED
        )

    def test_market_is_not_actionable_without_operational_knowledge(self):
        state = self.model.initial_state(
            location_node="CAL", start_date=date(1498, 5, 22)
        )
        view = self.model.market_view(state, seed=1)
        self.assertFalse(view.actionable)
        self.assertEqual(view.entries, ())
        blocked = self.model.buy(state, "PEPPER", 1.0, seed=1)
        self.assertFalse(blocked.executed)
        self.assertIn("MARKET_KNOWLEDGE_NOT_OPERATIONAL", blocked.reasons)

    def test_lisbon_port_services_are_exposed_through_session(self):
        state = self.model.initial_state(provision_days=10.0, condition=80.0)
        provisions = self.model.service_quote(state, PortServiceKind.PROVISIONS)
        repair = self.model.service_quote(state, PortServiceKind.REPAIR)
        self.assertTrue(provisions.actionable)
        self.assertTrue(repair.actionable)

        capital_before = state.commerce.capital_index
        reprovisioned = self.model.reprovision(state, 30.0)
        self.assertTrue(reprovisioned.executed)
        self.assertGreater(
            reprovisioned.state_after.vessel.provision_days,
            state.vessel.provision_days,
        )
        self.assertGreater(
            reprovisioned.state_after.vessel.clock.current_date,
            state.vessel.clock.current_date,
        )
        self.assertEqual(reprovisioned.state_after.commerce.capital_index, capital_before)
        self.assertEqual(reprovisioned.state_after.node_knowledge, state.node_knowledge)

        repaired = self.model.repair(reprovisioned.state_after, 20.0)
        self.assertTrue(repaired.executed)
        self.assertGreater(
            repaired.state_after.vessel.condition,
            reprovisioned.state_after.vessel.condition,
        )
        self.assertEqual(repaired.state_after.commerce.capital_index, capital_before)

    def test_unknown_port_service_does_not_mutate_session(self):
        state = self.model.initial_state(
            location_node="MAL",
            start_date=date(1498, 4, 24),
            provision_days=20.0,
        )
        quote = self.model.service_quote(state, PortServiceKind.PROVISIONS)
        self.assertFalse(quote.actionable)
        result = self.model.reprovision(state, 20.0)
        self.assertFalse(result.executed)
        self.assertIn("SERVICE_AVAILABILITY_UNKNOWN", result.reasons)
        self.assertEqual(result.state_after, state)

    def test_documented_malindi_pilot_teaches_route_destination_but_not_access(self):
        state = self.model.initial_state(
            location_node="MAL",
            start_date=date(1498, 4, 24),
            provision_days=50.0,
        )
        blocked = self.model.plan_voyage(state, "R_MAL_CAL", seed=1498)
        self.assertFalse(blocked.feasible)
        self.assertIn("NAVIGATION_KNOWLEDGE_OR_PILOT_REQUIRED", blocked.blockers)

        plan = self.model.plan_voyage(
            state,
            "R_MAL_CAL",
            pilot_id="PIL_MAL_GUJ_1498",
            seed=1498,
        )
        self.assertTrue(plan.feasible)
        arrived = self.model.execute_voyage(state, plan)
        self.assertEqual(arrived.vessel.location_node, "CAL")
        self.assertGreaterEqual(
            self.model.route_nav(arrived, "R_MAL_CAL"), KnowledgeLevel.OPERATIONAL
        )
        self.assertGreaterEqual(
            self.model.node_state(arrived, "CAL").market, KnowledgeLevel.OPERATIONAL
        )
        view = self.model.market_view(arrived, seed=1498)
        self.assertFalse(view.actionable)
        self.assertEqual(view.access_status, AccessStatus.NEGOTIATION_REQUIRED)
        negotiated = self.model.negotiate_access(arrived)
        self.assertTrue(negotiated.executed)
        self.assertTrue(self.model.market_view(negotiated.state_after, seed=1498).actionable)

    def test_technical_scenario_completes_buy_travel_negotiate_sell_cycle(self):
        # Cenário de integração deliberadamente não-histórico como estado inicial.
        state = self.model.initial_state(
            location_node="CAL",
            start_date=date(1498, 5, 22),
            provision_days=200.0,
            capital_index=100.0,
            capacity_total=30.0,
        )
        original_cal = self.model.node_state(state, "CAL")
        state = self.model.scenario_set_node_knowledge(
            state,
            "CAL",
            KnowledgeState(
                geo=original_cal.geo,
                nav=original_cal.nav,
                market=KnowledgeLevel.OPERATIONAL,
                political=original_cal.political,
            ),
        )
        state = self.model.scenario_set_route_knowledge(
            state, "R_CAL_ADE", KnowledgeLevel.OPERATIONAL
        )
        state = self.model.scenario_set_access(state, "CAL", AccessStatus.NEGOTIATED)

        bought = self.model.buy(state, "PEPPER", 2.0, seed=1498)
        self.assertTrue(bought.executed)
        self.assertEqual(bought.state_after.commerce.quantity_of("PEPPER"), 2.0)

        plan = self.model.plan_voyage(
            bought.state_after, "R_CAL_ADE", seed=1498
        )
        self.assertTrue(plan.feasible)
        arrived = self.model.execute_voyage(bought.state_after, plan)
        self.assertEqual(arrived.vessel.location_node, "ADE")
        self.assertGreaterEqual(
            self.model.node_state(arrived, "ADE").market,
            KnowledgeLevel.OPERATIONAL,
        )
        self.assertFalse(self.model.market_view(arrived, seed=1498).actionable)

        access = self.model.negotiate_access(arrived)
        self.assertTrue(access.executed)
        sold = self.model.sell(access.state_after, "PEPPER", 2.0, seed=1498)
        self.assertTrue(sold.executed)
        self.assertEqual(sold.state_after.commerce.quantity_of("PEPPER"), 0.0)
        self.assertGreater(
            sold.state_after.commerce.capital_index,
            bought.state_after.commerce.capital_index,
        )

    def test_scenario_overrides_do_not_mutate_original_state(self):
        state = self.model.initial_state()
        changed = self.model.scenario_set_route_knowledge(
            state, "R_CAL_ADE", KnowledgeLevel.OPERATIONAL
        )
        self.assertEqual(
            self.model.route_nav(state, "R_CAL_ADE"), KnowledgeLevel.UNKNOWN
        )
        self.assertEqual(
            self.model.route_nav(changed, "R_CAL_ADE"), KnowledgeLevel.OPERATIONAL
        )


if __name__ == "__main__":
    unittest.main()
