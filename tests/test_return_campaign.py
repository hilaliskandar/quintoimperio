import unittest
from datetime import date

from quintoimperio.domain.port import PortServiceKind, ServiceAvailability
from quintoimperio.domain.return_campaign import ReturnCampaignModel
from quintoimperio.domain.stop import ChronologyMode


class ReturnCampaignTests(unittest.TestCase):
    def setUp(self):
        self.model = ReturnCampaignModel()

    def completed_mvp_state(self, *, provisions: float = 120.0, on_date=date(1498, 5, 22)):
        return self.model.session.initial_state(
            location_node="CAL",
            start_date=on_date,
            provision_days=provisions,
            active_expedition_id=None,
            chronology_mode=ChronologyMode.GUIDED,
        )

    def test_return_is_explicit_and_preserves_mvp_completion_state(self):
        state = self.completed_mvp_state()
        self.assertIsNone(state.active_expedition_id)
        self.assertEqual(state.vessel.location_node, "CAL")

        activated = self.model.activate_return(state)
        self.assertEqual(activated.active_expedition_id, "EXP_GAMA_RETURN_1498")
        self.assertEqual(activated.expedition_leg_sequence, 1)
        self.assertEqual(activated.vessel.location_node, "CAL")
        self.assertEqual(activated.vessel.clock.current_date, date(1498, 5, 22))
        self.assertIs(activated.chronology_mode, ChronologyMode.GUIDED)

    def test_late_return_activation_becomes_counterfactual(self):
        state = self.completed_mvp_state(on_date=date(1498, 9, 1))
        activated = self.model.activate_return(state)
        self.assertIs(activated.chronology_mode, ChronologyMode.COUNTERFACTUAL)

    def test_return_cannot_be_activated_outside_calicut(self):
        state = self.model.session.initial_state(location_node="MAL")
        with self.assertRaises(ValueError):
            self.model.activate_return(state)

    def test_anjediva_generic_port_service_remains_unknown(self):
        self.assertEqual(
            self.model.session.port.availability("ANJ", PortServiceKind.PROVISIONS),
            ServiceAvailability.UNKNOWN,
        )
        quote = self.model.session.port.quote("ANJ", PortServiceKind.PROVISIONS)
        self.assertFalse(quote.documented)
        self.assertFalse(quote.actionable)

    def test_documented_stop_reprovision_is_specific_not_generic(self):
        state = self.completed_mvp_state()
        state = self.model.activate_return(state)
        waited = self.model.wait_for_guided_departure(state)
        state = waited.state_after
        plan = self.model.plan_current_leg(state, seed=1498)
        self.assertTrue(plan.feasible, plan.blockers)
        state = self.model.execute_voyage(state, plan)

        self.assertEqual(state.vessel.location_node, "ANJ")
        self.assertTrue(self.model.documented_stop_can_reprovision(state))
        before = state.vessel.provision_days
        result = self.model.reprovision_at_documented_stop(state, 50.0)
        self.assertTrue(result.executed, result.reasons)
        self.assertGreater(result.state_after.vessel.provision_days, before)
        self.assertEqual(
            self.model.session.port.availability("ANJ", PortServiceKind.PROVISIONS),
            ServiceAvailability.UNKNOWN,
        )

    def test_guided_return_reaches_rio_grande(self):
        state = self.completed_mvp_state(provisions=120.0)
        state = self.model.activate_return(state)
        completed_routes = []

        while state.active_expedition_id == "EXP_GAMA_RETURN_1498":
            if self.model.documented_stop_can_reprovision(state):
                result = self.model.reprovision_at_documented_stop(state, 120.0)
                if result.executed:
                    state = result.state_after

            expected = self.model.guided_departure_date(state)
            if expected is not None and state.vessel.clock.current_date < expected:
                wait = self.model.wait_for_guided_departure(state)
                self.assertTrue(wait.executed, wait.reasons)
                state = wait.state_after

            leg = self.model.current_leg(state)
            self.assertIsNotNone(leg)
            plan = self.model.plan_current_leg(state, seed=1499)
            self.assertTrue(plan.feasible, (leg.route_id, plan.blockers, state.vessel.provision_days))
            completed_routes.append(leg.route_id)
            state = self.model.execute_voyage(state, plan)

        self.assertEqual(
            completed_routes,
            [
                "R_CAL_ANJ",
                "R_ANJ_MAL",
                "R_MAL_BSR",
                "R_BSR_SBR",
                "R_SBR_CGH_RET",
                "R_CGH_BRG",
            ],
        )
        self.assertEqual(state.vessel.location_node, "BRG")
        self.assertEqual(state.vessel.clock.current_date, date(1499, 4, 25))
        self.assertIsNone(state.active_expedition_id)
        self.assertIsNone(state.expedition_leg_sequence)
        self.assertIs(state.chronology_mode, ChronologyMode.GUIDED)


if __name__ == "__main__":
    unittest.main()
