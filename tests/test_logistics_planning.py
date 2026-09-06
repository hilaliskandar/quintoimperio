import unittest
from datetime import date

from quintoimperio.domain import CampaignPersistence, HistoricalCampaignModel


class LogisticsPlanningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = HistoricalCampaignModel()
        cls.persistence = CampaignPersistence()

    def test_playable_campaign_opens_two_days_before_historical_departure(self):
        state = self.model.initial_playable_state()
        self.assertEqual(state.vessel.clock.current_date, date(1497, 7, 6))
        self.assertEqual(self.model.guided_departure_date(state), date(1497, 7, 8))
        self.assertTrue(self.model.in_predeparture_phase(state))

        plan = self.model.plan_current_leg(state, seed=1498)
        self.assertFalse(plan.feasible)
        self.assertIn("HISTORICAL_DEPARTURE_NOT_REACHED", plan.blockers)

    def test_planning_view_exposes_margin_as_advice_not_resource(self):
        state = self.model.initial_playable_state()
        before = state.vessel.provision_days
        view = self.model.logistics_planning_view(state)

        self.assertEqual(view.current_autonomy_days, before)
        self.assertEqual(view.recommended_margin_days, 20.0)
        self.assertTrue(view.in_predeparture_phase)
        self.assertIsNotNone(view.next_leg_required_days)
        self.assertEqual(state.vessel.provision_days, before)
        self.assertEqual(view.next_destination_node, "STG")

    def test_predeparture_service_consumes_time_without_automatic_grant(self):
        state = self.model.initial_playable_state()
        result = self.model.reprovision(state, 30.0)
        self.assertTrue(result.executed)
        self.assertEqual(result.service_result.days_spent, 1)
        self.assertEqual(result.state_after.vessel.clock.current_date, date(1497, 7, 7))
        self.assertGreater(result.state_after.vessel.provision_days, state.vessel.provision_days)
        self.assertTrue(self.model.in_predeparture_phase(result.state_after))

        waited = self.model.wait_for_guided_departure(result.state_after)
        self.assertTrue(waited.executed)
        self.assertEqual(waited.state_after.vessel.clock.current_date, date(1497, 7, 8))
        self.assertFalse(self.model.in_predeparture_phase(waited.state_after))

    def test_save_load_preserves_predeparture_phase_by_domain_state(self):
        state = self.model.initial_playable_state()
        text = self.persistence.dumps(state, seed=1498)
        loaded = self.persistence.loads(text).state

        self.assertEqual(loaded.vessel.clock.current_date, date(1497, 7, 6))
        self.assertEqual(loaded.active_expedition_id, "EXP_GAMA_1497")
        self.assertEqual(loaded.expedition_leg_sequence, 1)
        self.assertTrue(self.model.in_predeparture_phase(loaded))
        self.assertEqual(
            self.model.logistics_planning_view(loaded).recommended_margin_days,
            20.0,
        )

    def test_waiting_without_preparation_reaches_historical_departure_without_resources(self):
        state = self.model.initial_playable_state()
        provisions = state.vessel.provision_days
        waited = self.model.wait_for_guided_departure(state)

        self.assertTrue(waited.executed)
        self.assertEqual(waited.days_waited, 2)
        self.assertEqual(waited.state_after.vessel.provision_days, provisions)
        self.assertEqual(waited.state_after.vessel.clock.current_date, date(1497, 7, 8))


if __name__ == "__main__":
    unittest.main()
