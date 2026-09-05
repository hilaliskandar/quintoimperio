import unittest
from datetime import date

from quintoimperio.domain import (
    ChronologyMode,
    ExpeditionStopModel,
    GameSessionModel,
)


class ExpeditionStopModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = ExpeditionStopModel()

    def test_narrated_stay_is_distinct_from_editorial_date_difference(self):
        stop = self.model.stop("GAMA1497_SHB")
        self.assertIsNotNone(stop)
        assert stop is not None
        self.assertEqual(stop.observed_stay_days, 8)
        self.assertEqual((stop.departure_date - stop.arrival_date).days, 9)

    def test_stop_exposes_documented_activities_without_material_effects(self):
        stop = self.model.stop("GAMA1497_STG")
        self.assertIsNotNone(stop)
        assert stop is not None
        self.assertEqual(stop.node_id, "STG")
        self.assertEqual(stop.departure_date, date(1497, 8, 3))
        self.assertIn("WATER", stop.activities)
        self.assertIn("YARD_REPAIR", stop.activities)


class GuidedStopSessionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = GameSessionModel()

    def arrive_santiago(self):
        state = self.model.initial_state(
            active_expedition_id="EXP_GAMA_1497",
            provision_days=120.0,
        )
        plan = self.model.plan_voyage(state, "R_LIS_STG", seed=1497)
        self.assertTrue(plan.feasible)
        return self.model.execute_voyage(state, plan)

    def test_historical_arrival_activates_guided_stop(self):
        arrived = self.arrive_santiago()
        self.assertEqual(arrived.chronology_mode, ChronologyMode.GUIDED)
        self.assertEqual(arrived.active_stop_id, "GAMA1497_STG")
        stop = self.model.active_stop(arrived)
        self.assertIsNotNone(stop)
        assert stop is not None
        self.assertEqual(stop.departure_date, date(1497, 8, 3))

    def test_next_leg_is_blocked_before_documented_release(self):
        arrived = self.arrive_santiago()
        plan = self.model.plan_voyage(arrived, "R_STG_SHB", seed=1497)
        self.assertFalse(plan.feasible)
        self.assertIn("HISTORICAL_STOP_NOT_RELEASED", plan.blockers)

    def test_service_time_consumes_stop_interval_but_does_not_complete_it(self):
        arrived = self.arrive_santiago()
        before_provisions = arrived.vessel.provision_days
        serviced = self.model.reprovision(arrived, 10.0)
        self.assertTrue(serviced.executed)
        self.assertEqual(serviced.state_after.vessel.clock.current_date, date(1497, 7, 28))
        self.assertEqual(
            serviced.state_after.vessel.provision_days,
            before_provisions + 10.0,
        )
        self.assertEqual(serviced.state_after.active_stop_id, "GAMA1497_STG")

        waited = self.model.wait_for_stop_release(serviced.state_after)
        self.assertTrue(waited.executed)
        self.assertEqual(waited.days_waited, 6)
        self.assertEqual(waited.state_after.vessel.clock.current_date, date(1497, 8, 3))
        self.assertEqual(
            waited.state_after.vessel.provision_days,
            serviced.state_after.vessel.provision_days,
        )
        self.assertEqual(
            waited.state_after.vessel.condition,
            serviced.state_after.vessel.condition,
        )
        self.assertEqual(waited.state_after.commerce, serviced.state_after.commerce)

    def test_departing_late_switches_permanently_to_counterfactual_chronology(self):
        arrived = self.arrive_santiago()
        waited = self.model.wait_for_stop_release(arrived)
        self.assertTrue(waited.executed)
        # Uma ação explícita depois da data histórica de saída cria atraso.
        serviced = self.model.reprovision(waited.state_after, 1.0)
        self.assertTrue(serviced.executed)
        self.assertEqual(serviced.state_after.vessel.clock.current_date, date(1497, 8, 4))

        plan = self.model.plan_voyage(serviced.state_after, "R_STG_SHB", seed=1497)
        self.assertTrue(plan.feasible)
        after = self.model.execute_voyage(serviced.state_after, plan)
        self.assertEqual(after.chronology_mode, ChronologyMode.COUNTERFACTUAL)

    def test_counterfactual_stop_does_not_force_wait(self):
        arrived = self.arrive_santiago()
        counterfactual = arrived.__class__(
            vessel=arrived.vessel,
            commerce=arrived.commerce,
            node_knowledge=arrived.node_knowledge,
            route_knowledge=arrived.route_knowledge,
            active_expedition_id=arrived.active_expedition_id,
            expedition_leg_sequence=arrived.expedition_leg_sequence,
            chronology_mode=ChronologyMode.COUNTERFACTUAL,
            active_stop_id=arrived.active_stop_id,
        )
        result = self.model.wait_for_stop_release(counterfactual)
        self.assertFalse(result.executed)
        self.assertIn("COUNTERFACTUAL_CHRONOLOGY_NO_FORCED_WAIT", result.reasons)


if __name__ == "__main__":
    unittest.main()
