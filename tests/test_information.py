import unittest
from datetime import date

from quintoimperio.domain import (
    ChronologyMode,
    GameSessionModel,
    InformationChannel,
    KnowledgeLevel,
)


class InformationAcquisitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = GameSessionModel()

    def test_rumor_never_produces_operational_navigation(self):
        state = self.model.initial_state(
            location_node="MAL",
            start_date=date(1498, 4, 20),
        )
        before_market = self.model.node_state(state, "CAL").market
        result = self.model.acquire_information(state, InformationChannel.RUMOR, seed=10)
        self.assertTrue(result.executed)
        self.assertIsNotNone(result.opportunity)
        assert result.opportunity is not None
        self.assertEqual(result.opportunity.target_route_id, "R_MAL_CAL")
        self.assertEqual(self.model.route_nav(result.state_after, "R_MAL_CAL"), KnowledgeLevel.RUMORED)
        self.assertLess(self.model.route_nav(result.state_after, "R_MAL_CAL"), KnowledgeLevel.OPERATIONAL)
        self.assertEqual(self.model.node_state(result.state_after, "CAL").market, before_market)

    def test_documented_pilot_consultation_is_route_specific_and_partial(self):
        state = self.model.initial_state(
            location_node="MAL",
            start_date=date(1498, 4, 24),
        )
        result = self.model.acquire_information(
            state, InformationChannel.PILOT_CONSULTATION, seed=1498
        )
        self.assertTrue(result.executed)
        assert result.opportunity is not None
        self.assertEqual(result.opportunity.pilot_id, "PIL_MAL_GUJ_1498")
        self.assertEqual(result.opportunity.target_route_id, "R_MAL_CAL")
        self.assertEqual(
            self.model.route_nav(result.state_after, "R_MAL_CAL"),
            KnowledgeLevel.PARTIAL,
        )
        self.assertLess(
            self.model.route_nav(result.state_after, "R_MAL_CAL"),
            KnowledgeLevel.OPERATIONAL,
        )

    def test_merchant_contact_improves_commercial_but_not_operational_nav(self):
        state = self.model.initial_state(
            location_node="CAL",
            start_date=date(1498, 5, 22),
        )
        result = self.model.acquire_information(
            state, InformationChannel.MERCHANT_CONTACT, seed=42
        )
        self.assertTrue(result.executed)
        assert result.opportunity is not None
        target = result.opportunity.target_node_id
        route = result.opportunity.target_route_id
        learned = self.model.node_state(result.state_after, target)
        self.assertGreaterEqual(learned.geo, KnowledgeLevel.PARTIAL)
        self.assertGreaterEqual(learned.market, KnowledgeLevel.PARTIAL)
        self.assertLess(self.model.route_nav(result.state_after, route), KnowledgeLevel.OPERATIONAL)

    def test_same_seed_and_state_choose_same_opportunity(self):
        a = self.model.initial_state(
            location_node="CAL",
            start_date=date(1498, 5, 22),
        )
        b = self.model.initial_state(
            location_node="CAL",
            start_date=date(1498, 5, 22),
        )
        ra = self.model.acquire_information(a, InformationChannel.MERCHANT_CONTACT, seed=77)
        rb = self.model.acquire_information(b, InformationChannel.MERCHANT_CONTACT, seed=77)
        self.assertTrue(ra.executed)
        self.assertTrue(rb.executed)
        assert ra.opportunity is not None and rb.opportunity is not None
        self.assertEqual(ra.opportunity.opportunity_id, rb.opportunity.opportunity_id)

    def test_same_opportunity_is_not_reused_in_session(self):
        state = self.model.initial_state(
            location_node="MAL",
            start_date=date(1498, 4, 20),
        )
        first = self.model.acquire_information(state, InformationChannel.RUMOR, seed=1)
        self.assertTrue(first.executed)
        second = self.model.acquire_information(
            first.state_after, InformationChannel.RUMOR, seed=1
        )
        self.assertFalse(second.executed)
        self.assertIn("NO_INFORMATION_OPPORTUNITY", second.reasons)

    def test_information_time_consumes_guided_stop_interval(self):
        state = self.model.initial_state(
            active_expedition_id="EXP_GAMA_1497",
            provision_days=120.0,
        )
        plan = self.model.plan_voyage(state, "R_LIS_STG", seed=1497)
        arrived = self.model.execute_voyage(state, plan)
        self.assertEqual(arrived.vessel.clock.current_date, date(1497, 7, 27))
        self.assertEqual(arrived.chronology_mode, ChronologyMode.GUIDED)

        informed = self.model.acquire_information(
            arrived, InformationChannel.RUMOR, seed=1497
        )
        self.assertTrue(informed.executed)
        self.assertEqual(informed.state_after.vessel.clock.current_date, date(1497, 7, 28))
        self.assertEqual(informed.state_after.active_stop_id, "GAMA1497_STG")

        waited = self.model.wait_for_stop_release(informed.state_after)
        self.assertTrue(waited.executed)
        self.assertEqual(waited.days_waited, 6)
        self.assertEqual(waited.state_after.vessel.clock.current_date, date(1497, 8, 3))

    def test_cape_navigation_point_has_no_generic_rumor(self):
        state = self.model.initial_state(
            location_node="CGH",
            start_date=date(1497, 11, 22),
        )
        result = self.model.acquire_information(state, InformationChannel.RUMOR, seed=1)
        self.assertFalse(result.executed)
        self.assertIn("NO_INFORMATION_OPPORTUNITY", result.reasons)


if __name__ == "__main__":
    unittest.main()
