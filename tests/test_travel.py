import unittest
from datetime import date

from quintoimperio.domain import (
    GameClock,
    KnowledgeLevel,
    NavigationBasis,
    TravelModel,
    VesselState,
)


class TravelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = TravelModel()

    def state(self, provisions=40.0, condition=100.0):
        return VesselState(
            location_node="MAL",
            clock=GameClock(date(1498, 4, 24)),
            provision_days=provisions,
            condition=condition,
        )

    def test_rumored_navigation_without_pilot_blocks_departure(self):
        plan = self.model.plan_voyage(
            self.state(),
            "R_MAL_CAL",
            KnowledgeLevel.RUMORED,
            seed=1498,
        )
        self.assertFalse(plan.feasible)
        self.assertIn("NAVIGATION_KNOWLEDGE_OR_PILOT_REQUIRED", plan.blockers)

    def test_documented_malindi_pilot_enables_route(self):
        plan = self.model.plan_voyage(
            self.state(),
            "R_MAL_CAL",
            KnowledgeLevel.RUMORED,
            pilot_id="PIL_MAL_GUJ_1498",
            seed=1498,
        )
        self.assertTrue(plan.feasible)
        self.assertEqual(plan.navigation_basis, NavigationBasis.PILOT)
        self.assertGreater(plan.travel_days, 20)
        self.assertLess(plan.travel_days, 31)

    def test_operational_own_knowledge_does_not_require_pilot(self):
        plan = self.model.plan_voyage(
            self.state(),
            "R_MAL_CAL",
            KnowledgeLevel.OPERATIONAL,
            seed=1498,
        )
        self.assertTrue(plan.feasible)
        self.assertEqual(plan.navigation_basis, NavigationBasis.OWN_KNOWLEDGE)

    def test_pilot_does_not_receive_hidden_speed_bonus(self):
        state = self.state()
        own = self.model.plan_voyage(
            state,
            "R_MAL_CAL",
            KnowledgeLevel.OPERATIONAL,
            seed=77,
        )
        pilot = self.model.plan_voyage(
            state,
            "R_MAL_CAL",
            KnowledgeLevel.RUMORED,
            pilot_id="PIL_MAL_GUJ_1498",
            seed=77,
        )
        self.assertEqual(own.estimated_duration_days, pilot.estimated_duration_days)
        self.assertEqual(own.travel_days, pilot.travel_days)

    def test_insufficient_provisions_block_departure(self):
        plan = self.model.plan_voyage(
            self.state(provisions=5.0),
            "R_MAL_CAL",
            KnowledgeLevel.OPERATIONAL,
            seed=1498,
        )
        self.assertFalse(plan.feasible)
        self.assertIn("INSUFFICIENT_PROVISIONS", plan.blockers)

    def test_low_condition_blocks_departure(self):
        plan = self.model.plan_voyage(
            self.state(condition=10.0),
            "R_MAL_CAL",
            KnowledgeLevel.OPERATIONAL,
            seed=1498,
        )
        self.assertFalse(plan.feasible)
        self.assertIn("VESSEL_CONDITION_TOO_LOW", plan.blockers)

    def test_execution_advances_clock_consumes_provisions_and_wears_ship(self):
        state = self.state()
        plan = self.model.plan_voyage(
            state,
            "R_MAL_CAL",
            KnowledgeLevel.RUMORED,
            pilot_id="PIL_MAL_GUJ_1498",
            seed=1498,
        )
        arrived = self.model.execute_voyage(state, plan)
        self.assertEqual(arrived.location_node, "CAL")
        self.assertEqual(arrived.clock.current_date, plan.arrival_date)
        self.assertEqual(arrived.provision_days, plan.provision_days_after)
        self.assertLess(arrived.condition, state.condition)

    def test_pilot_is_not_general_route_bonus(self):
        self.assertFalse(
            self.model.pilot_can_guide(
                "PIL_MAL_GUJ_1498",
                "R_MOM_MAL",
                date(1498, 4, 24),
                "MOM",
            )
        )

    def test_pilot_record_is_temporally_bounded(self):
        self.assertFalse(
            self.model.pilot_can_guide(
                "PIL_MAL_GUJ_1498",
                "R_MAL_CAL",
                date(1505, 4, 24),
                "MAL",
            )
        )


if __name__ == "__main__":
    unittest.main()
