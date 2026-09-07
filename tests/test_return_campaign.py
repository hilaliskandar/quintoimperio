import unittest
from datetime import date

from quintoimperio.domain.persistence import CampaignPersistence
from quintoimperio.domain.port import PortServiceKind, ServiceAvailability
from quintoimperio.domain.return_campaign import ReturnCampaignModel
from quintoimperio.domain.stop import ChronologyMode


class ReturnCampaignTests(unittest.TestCase):
    def setUp(self):
        self.model = ReturnCampaignModel()
        self.persistence = CampaignPersistence()

    def completed_mvp_state(self, *, provisions: float = 120.0, on_date=date(1498, 5, 22)):
        return self.model.session.initial_state(
            location_node="CAL",
            start_date=on_date,
            provision_days=provisions,
            active_expedition_id=None,
            chronology_mode=ChronologyMode.GUIDED,
        )

    def state_at_santa_maria(self, *, provisions: float = 120.0):
        state = self.completed_mvp_state(provisions=provisions)
        state = self.model.activate_return(state)
        waited = self.model.wait_for_guided_departure(state)
        state = waited.state_after
        plan = self.model.plan_current_leg(state, seed=1498)
        self.assertTrue(plan.feasible, plan.blockers)
        return self.model.execute_voyage(state, plan)

    def state_at_anjediva(self):
        state = self.state_at_santa_maria()
        if self.model.documented_stop_can_reprovision(state):
            result = self.model.reprovision_at_documented_stop(state, 5.0)
            self.assertTrue(result.executed, result.reasons)
            state = result.state_after
        plan = self.model.plan_current_leg(state, seed=1498)
        self.assertTrue(plan.feasible, plan.blockers)
        return self.model.execute_voyage(state, plan)

    def round_trip(self, state):
        return self.persistence.loads(self.persistence.dumps(state, seed=1498)).state

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

    def test_anjediva_generic_port_services_remain_unknown(self):
        for service in (PortServiceKind.PROVISIONS, PortServiceKind.REPAIR):
            with self.subTest(service=service.value):
                self.assertEqual(
                    self.model.session.port.availability("ANJ", service),
                    ServiceAvailability.UNKNOWN,
                )
                quote = self.model.session.port.quote("ANJ", service)
                self.assertFalse(quote.documented)
                self.assertFalse(quote.actionable)

    def test_santa_maria_contact_bridges_low_provision_state_without_port_service(self):
        state = self.state_at_santa_maria(provisions=19.366)
        self.assertEqual(state.vessel.location_node, "SMI")
        self.assertEqual(state.vessel.clock.current_date, date(1498, 9, 15))
        self.assertTrue(self.model.documented_stop_can_reprovision(state))
        generic = self.model.session.port.quote("SMI", PortServiceKind.PROVISIONS)
        self.assertFalse(generic.actionable)

        before = state.vessel.provision_days
        result = self.model.reprovision_at_documented_stop(state, 2.0)
        self.assertTrue(result.executed, result.reasons)
        self.assertAlmostEqual(result.service_result.effect, 2.0)
        self.assertEqual(result.service_result.days_spent, 0)
        self.assertEqual(result.state_after.vessel.clock.current_date, date(1498, 9, 15))
        self.assertAlmostEqual(result.state_after.vessel.provision_days, before + 2.0)
        self.assertFalse(self.model.documented_stop_can_reprovision(result.state_after))
        plan = self.model.plan_current_leg(result.state_after, seed=1498)
        self.assertTrue(plan.feasible, plan.blockers)

    def test_santa_maria_action_is_capped_at_five_days_equivalent(self):
        state = self.state_at_santa_maria(provisions=30.0)
        result = self.model.reprovision_at_documented_stop(state, 50.0)
        self.assertTrue(result.executed)
        self.assertAlmostEqual(result.service_result.effect, 5.0)
        self.assertEqual(result.service_result.days_spent, 0)
        repeated = self.model.reprovision_at_documented_stop(result.state_after, 1.0)
        self.assertFalse(repeated.executed)
        self.assertIn("DOCUMENTED_PROVISION_ACTION_ALREADY_USED", repeated.reasons)

    def test_santa_maria_one_shot_survives_save_load(self):
        state = self.state_at_santa_maria(provisions=30.0)
        result = self.model.reprovision_at_documented_stop(state, 5.0)
        loaded = self.round_trip(result.state_after)
        self.assertFalse(self.model.documented_stop_can_reprovision(loaded))
        repeated = self.model.reprovision_at_documented_stop(loaded, 1.0)
        self.assertFalse(repeated.executed)
        self.assertIn("DOCUMENTED_PROVISION_ACTION_ALREADY_USED", repeated.reasons)

    def test_documented_stop_reprovision_is_specific_not_generic(self):
        state = self.state_at_anjediva()
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

    def test_documented_careening_repairs_without_generic_port_service(self):
        state = self.state_at_anjediva()
        self.assertTrue(self.model.documented_stop_can_repair(state))
        before = state.vessel.condition
        result = self.model.repair_at_documented_stop(state, 1.0)
        self.assertTrue(result.executed, result.reasons)
        self.assertAlmostEqual(result.service_result.effect, 1.0)
        self.assertEqual(result.service_result.days_spent, 1)
        self.assertAlmostEqual(result.state_after.vessel.condition, before + 1.0)
        self.assertFalse(self.model.documented_stop_can_repair(result.state_after))
        self.assertEqual(
            self.model.session.port.availability("ANJ", PortServiceKind.REPAIR),
            ServiceAvailability.UNKNOWN,
        )

    def test_careening_one_shot_survives_save_load(self):
        state = self.state_at_anjediva()
        result = self.model.repair_at_documented_stop(state, 2.0)
        self.assertTrue(result.executed)
        loaded = self.round_trip(result.state_after)
        self.assertFalse(self.model.documented_stop_can_repair(loaded))
        repeated = self.model.repair_at_documented_stop(loaded, 1.0)
        self.assertFalse(repeated.executed)
        self.assertIn("DOCUMENTED_REPAIR_ACTION_ALREADY_USED", repeated.reasons)

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
                "R_CAL_SMI",
                "R_SMI_ANJ",
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
