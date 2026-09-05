import unittest
from datetime import date

from quintoimperio.domain import (
    ExpeditionModel,
    GameSessionModel,
    KnowledgeLevel,
    NavigationBasis,
)


class ExpeditionModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = ExpeditionModel()

    def test_gama_expedition_has_ordered_outbound_legs(self):
        legs = self.model.legs["EXP_GAMA_1497"]
        self.assertEqual([leg.sequence for leg in legs], [1, 2, 3, 4, 5])
        self.assertEqual(
            [leg.route_id for leg in legs],
            ["R_LIS_CGH", "R_CGH_MOZ", "R_MOZ_MOM", "R_MOM_MAL", "R_MAL_CAL"],
        )

    def test_command_authorization_is_route_and_period_specific(self):
        self.assertTrue(
            self.model.authorizes(
                "EXP_GAMA_1497", 1, "R_LIS_CGH", date(1497, 7, 8)
            )
        )
        self.assertFalse(
            self.model.authorizes(
                "EXP_GAMA_1497", 1, "R_CAL_ADE", date(1497, 7, 8)
            )
        )
        self.assertFalse(
            self.model.authorizes(
                "EXP_GAMA_1497", 1, "R_LIS_CGH", date(1498, 7, 8)
            )
        )


class ExpeditionSessionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = GameSessionModel()

    def test_fleet_command_enables_first_leg_without_upgrading_knowledge_before_departure(self):
        state = self.model.initial_state(
            active_expedition_id="EXP_GAMA_1497",
            provision_days=1000.0,
        )
        self.assertEqual(
            self.model.route_nav(state, "R_LIS_CGH"), KnowledgeLevel.PARTIAL
        )
        plan = self.model.plan_voyage(state, "R_LIS_CGH", seed=1497)
        self.assertTrue(plan.feasible)
        self.assertEqual(plan.navigation_basis, NavigationBasis.FLEET_COMMAND)
        self.assertEqual(plan.travel_days, 134)
        self.assertEqual(plan.arrival_date, date(1497, 11, 19))
        self.assertEqual(
            self.model.route_nav(state, "R_LIS_CGH"), KnowledgeLevel.PARTIAL
        )

        arrived = self.model.execute_voyage(state, plan)
        self.assertEqual(arrived.vessel.location_node, "CGH")
        self.assertEqual(arrived.vessel.clock.current_date, date(1497, 11, 19))
        self.assertGreaterEqual(
            self.model.route_nav(arrived, "R_LIS_CGH"), KnowledgeLevel.OPERATIONAL
        )
        self.assertEqual(arrived.active_expedition_id, "EXP_GAMA_1497")
        self.assertEqual(arrived.expedition_leg_sequence, 2)

    def test_expedition_does_not_authorize_unrelated_route(self):
        state = self.model.initial_state(
            location_node="CAL",
            start_date=date(1498, 5, 22),
            active_expedition_id="EXP_GAMA_1497",
            expedition_leg_sequence=1,
            provision_days=200.0,
        )
        plan = self.model.plan_voyage(state, "R_CAL_ADE", seed=1)
        self.assertFalse(plan.feasible)
        self.assertIsNone(plan.navigation_basis)

    def test_documented_pilot_precedes_fleet_command_on_malindi_calicut_leg(self):
        state = self.model.initial_state(
            location_node="MAL",
            start_date=date(1498, 4, 24),
            active_expedition_id="EXP_GAMA_1497",
            expedition_leg_sequence=5,
            provision_days=60.0,
        )
        plan = self.model.plan_voyage(
            state,
            "R_MAL_CAL",
            pilot_id="PIL_MAL_GUJ_1498",
            seed=1498,
        )
        self.assertTrue(plan.feasible)
        self.assertEqual(plan.navigation_basis, NavigationBasis.PILOT)
        arrived = self.model.execute_voyage(state, plan)
        self.assertIsNone(arrived.active_expedition_id)
        self.assertIsNone(arrived.expedition_leg_sequence)


if __name__ == "__main__":
    unittest.main()
