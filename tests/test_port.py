import unittest
from datetime import date

from quintoimperio.domain import (
    GameClock,
    PortServiceKind,
    PortServiceModel,
    ServiceAvailability,
    VesselState,
)


class PortServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = PortServiceModel()

    @staticmethod
    def state(node="LIS", provisions=20.0, condition=70.0):
        return VesselState(
            location_node=node,
            clock=GameClock(date(1497, 7, 1)),
            provision_days=provisions,
            condition=condition,
        )

    def test_lisbon_provision_service_is_documented_and_actionable(self):
        quote = self.model.quote("LIS", PortServiceKind.PROVISIONS)
        self.assertEqual(quote.availability, ServiceAvailability.HIGH)
        self.assertTrue(quote.documented)
        self.assertTrue(quote.actionable)
        self.assertEqual(quote.capacity_or_rate, 50.0)

    def test_unknown_service_is_not_treated_as_none(self):
        malindi = self.model.quote("MAL", PortServiceKind.PROVISIONS)
        cape = self.model.quote("CGH", PortServiceKind.PROVISIONS)
        self.assertEqual(malindi.availability, ServiceAvailability.UNKNOWN)
        self.assertFalse(malindi.documented)
        self.assertEqual(cape.availability, ServiceAvailability.NONE)
        self.assertTrue(cape.documented)

    def test_reprovision_is_capped_by_service_capacity(self):
        state = self.state(provisions=20.0)
        result = self.model.reprovision(state, "LIS", requested_days=80.0)
        self.assertTrue(result.success)
        self.assertEqual(result.effect, 50.0)
        self.assertEqual(result.state_after.provision_days, 70.0)
        self.assertEqual(result.days_spent, 1)
        self.assertEqual(result.state_after.clock.current_date, date(1497, 7, 2))

    def test_reprovision_respects_abstract_onboard_cap(self):
        state = self.state(provisions=85.0)
        result = self.model.reprovision(state, "LIS", requested_days=20.0)
        self.assertTrue(result.success)
        self.assertEqual(result.effect, 5.0)
        self.assertEqual(result.state_after.provision_days, 90.0)

    def test_unknown_provision_service_blocks_without_inventing_it(self):
        state = self.state(node="MAL")
        result = self.model.reprovision(state, "MAL", requested_days=20.0)
        self.assertFalse(result.success)
        self.assertIn("SERVICE_AVAILABILITY_UNKNOWN", result.blockers)
        self.assertEqual(result.state_after, state)

    def test_none_service_is_explicitly_unavailable(self):
        state = self.state(node="CGH")
        result = self.model.reprovision(state, "CGH", requested_days=10.0)
        self.assertFalse(result.success)
        self.assertIn("SERVICE_UNAVAILABLE", result.blockers)

    def test_repair_restores_only_missing_condition(self):
        state = self.state(condition=70.0)
        result = self.model.repair(state, "LIS", requested_points=50.0)
        self.assertTrue(result.success)
        self.assertEqual(result.effect, 30.0)
        self.assertEqual(result.state_after.condition, 100.0)
        self.assertEqual(result.days_spent, 3)
        self.assertEqual(result.state_after.clock.current_date, date(1497, 7, 4))

    def test_low_repair_service_limits_one_action(self):
        state = self.state(node="CEU", condition=50.0)
        result = self.model.repair(state, "CEU", requested_points=30.0)
        self.assertTrue(result.success)
        self.assertEqual(result.effect, 10.0)
        self.assertEqual(result.days_spent, 5)
        self.assertEqual(result.state_after.condition, 60.0)

    def test_service_requires_vessel_at_same_port(self):
        state = self.state(node="LIS")
        result = self.model.repair(state, "CEU", requested_points=10.0)
        self.assertFalse(result.success)
        self.assertIn("VESSEL_NOT_AT_PORT", result.blockers)

    def test_full_condition_does_not_consume_time(self):
        state = self.state(condition=100.0)
        result = self.model.repair(state, "LIS", requested_points=10.0)
        self.assertFalse(result.success)
        self.assertIn("VESSEL_ALREADY_FULL_CONDITION", result.blockers)
        self.assertEqual(result.days_spent, 0)
        self.assertEqual(result.state_after, state)


if __name__ == "__main__":
    unittest.main()
