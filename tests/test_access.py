import unittest
from datetime import date

from quintoimperio.domain import (
    AccessModel,
    AccessStatus,
    GameSessionModel,
    KnowledgeLevel,
    KnowledgeState,
)


class AccessModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = AccessModel()

    def test_initial_access_follows_documented_regime_mapping(self):
        self.assertEqual(cls_status := self.model.initial_status("LIS"), AccessStatus.OPEN)
        self.assertEqual(self.model.initial_status("CAL"), AccessStatus.NEGOTIATION_REQUIRED)
        self.assertEqual(self.model.initial_status("COC"), AccessStatus.NEGOTIATION_REQUIRED)
        self.assertEqual(self.model.initial_status("ARG"), AccessStatus.RESTRICTED)
        self.assertEqual(self.model.initial_status("ELM"), AccessStatus.RESTRICTED)
        self.assertEqual(self.model.initial_status("CGH"), AccessStatus.NONCOMMERCIAL)
        self.assertEqual(cls_status.value, "OPEN")

    def test_foreign_negotiated_market_is_negotiable_without_inventing_broker(self):
        view = self.model.view("CAL", AccessStatus.NEGOTIATION_REQUIRED)
        self.assertTrue(view.negotiable)
        self.assertFalse(view.commercial_access)
        self.assertEqual(view.time_days, 1)
        self.assertEqual(view.broker_availability, "HIGH")

    def test_generic_negotiation_does_not_open_royal_monopoly(self):
        view = self.model.view("ARG", AccessStatus.RESTRICTED)
        self.assertFalse(view.negotiable)
        with self.assertRaisesRegex(ValueError, "ACCESS_NEGOTIATION_NOT_AVAILABLE"):
            self.model.negotiate("ARG", AccessStatus.RESTRICTED)


class AccessSessionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = GameSessionModel()

    def operational_market(self, node_id, start_date):
        state = self.session.initial_state(
            location_node=node_id,
            start_date=start_date,
            provision_days=100.0,
        )
        current = self.session.node_state(state, node_id)
        return self.session.scenario_set_node_knowledge(
            state,
            node_id,
            KnowledgeState(
                geo=current.geo,
                nav=current.nav,
                market=KnowledgeLevel.OPERATIONAL,
                political=current.political,
            ),
        )

    def operational_calicut(self):
        return self.operational_market("CAL", date(1498, 5, 22))

    def operational_cochin(self):
        return self.operational_market("COC", date(1500, 12, 24))

    def test_known_market_can_be_seen_but_not_traded_before_negotiation(self):
        state = self.operational_calicut()
        view = self.session.market_view(state, seed=7)
        self.assertEqual(view.access_status, AccessStatus.NEGOTIATION_REQUIRED)
        self.assertFalse(view.actionable)
        self.assertTrue(any(entry.good_id == "PEPPER" for entry in view.entries))
        blocked = self.session.buy(state, "PEPPER", 1.0, seed=7)
        self.assertFalse(blocked.executed)
        self.assertIn("PORT_ACCESS_NEGOTIATION_REQUIRED", blocked.reasons)

    def test_negotiation_consumes_time_and_grants_port_access(self):
        state = self.operational_calicut()
        before = state.vessel.clock.current_date
        result = self.session.negotiate_access(state)
        self.assertTrue(result.executed)
        self.assertEqual(result.days_spent, 1)
        self.assertEqual(result.state_after.vessel.clock.current_date, date(1498, 5, 23))
        self.assertEqual(result.view_after.status, AccessStatus.NEGOTIATED)
        self.assertTrue(result.view_after.commercial_access)
        self.assertNotEqual(result.state_after.vessel.clock.current_date, before)
        bought = self.session.buy(result.state_after, "PEPPER", 1.0, seed=7)
        self.assertTrue(bought.executed)

    def test_cochin_reuses_generic_negotiation_and_minimal_pepper_market(self):
        state = self.operational_cochin()
        view = self.session.market_view(state, seed=11)
        self.assertEqual(view.access_status, AccessStatus.NEGOTIATION_REQUIRED)
        self.assertFalse(view.actionable)
        self.assertEqual({entry.good_id for entry in view.entries}, {"PEPPER"})
        blocked = self.session.buy(state, "PEPPER", 1.0, seed=11)
        self.assertFalse(blocked.executed)
        self.assertIn("PORT_ACCESS_NEGOTIATION_REQUIRED", blocked.reasons)

        negotiated = self.session.negotiate_access(state)
        self.assertTrue(negotiated.executed)
        self.assertEqual(negotiated.days_spent, 1)
        self.assertEqual(negotiated.view_after.status, AccessStatus.NEGOTIATED)
        self.assertTrue(negotiated.view_after.commercial_access)
        bought = self.session.buy(negotiated.state_after, "PEPPER", 1.0, seed=11)
        self.assertTrue(bought.executed)

    def test_negotiation_is_not_repeatable_after_access_is_granted(self):
        first = self.session.negotiate_access(self.operational_calicut())
        second = self.session.negotiate_access(first.state_after)
        self.assertFalse(second.executed)
        self.assertIn("ACCESS_NEGOTIATION_NOT_AVAILABLE", second.reasons)

    def test_scenario_access_override_is_explicit_and_immutable(self):
        state = self.operational_calicut()
        changed = self.session.scenario_set_access(state, "CAL", AccessStatus.NEGOTIATED)
        self.assertEqual(self.session.access_status(state, "CAL"), AccessStatus.NEGOTIATION_REQUIRED)
        self.assertEqual(self.session.access_status(changed, "CAL"), AccessStatus.NEGOTIATED)


if __name__ == "__main__":
    unittest.main()
