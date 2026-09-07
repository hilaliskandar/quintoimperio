import unittest

from quintoimperio.domain import P3CampaignModel
from quintoimperio.domain.port import PortServiceKind, ServiceAvailability


class P3DocumentedProvisioningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = P3CampaignModel()

    def at_vera_cruz(self, seed: int):
        state = self.model.initial_cabral_state(provision_days=120.0)
        first = self.model.plan_current_leg(state, seed=seed)
        self.assertTrue(first.feasible, first.blockers)
        return self.model.execute_voyage(state, first)

    def at_mozambique_with_documented_vcr_action(self, seed: int):
        state = self.at_vera_cruz(seed)
        water = self.model.reprovision_at_documented_cabral_stop(state)
        self.assertTrue(water.executed, water.reasons)
        released = self.model.wait_for_stop_release(water.state_after)
        self.assertTrue(released.executed, released.reasons)
        plan = self.model.plan_current_leg(released.state_after, seed=seed)
        self.assertTrue(plan.feasible, plan.blockers)
        return self.model.execute_voyage(released.state_after, plan)

    def at_malindi_with_documented_africa_actions(self, seed: int):
        state = self.at_mozambique_with_documented_vcr_action(seed)
        moz = self.model.reprovision_at_documented_cabral_stop(state)
        self.assertTrue(moz.executed, moz.reasons)
        moz_kil = self.model.plan_current_leg(moz.state_after, seed=seed)
        self.assertTrue(moz_kil.feasible, moz_kil.blockers)
        state = self.model.execute_voyage(moz.state_after, moz_kil)
        released = self.model.wait_for_stop_release(state)
        self.assertTrue(released.executed, released.reasons)
        kil_mal = self.model.plan_current_leg(released.state_after, seed=seed)
        self.assertTrue(kil_mal.feasible, kil_mal.blockers)
        return self.model.execute_voyage(released.state_after, kil_mal)

    def test_vera_cruz_remains_unknown_as_generic_port_service(self):
        self.assertEqual(
            self.model.session.port.availability("VCR", PortServiceKind.PROVISIONS),
            ServiceAvailability.UNKNOWN,
        )

    def test_mozambique_generic_service_is_not_changed_by_cabral_stop(self):
        before = self.model.session.port.availability("MOZ", PortServiceKind.PROVISIONS)
        state = self.at_mozambique_with_documented_vcr_action(24001)
        self.assertEqual(state.active_stop_id, "CABRAL1500_MOZ")
        self.assertTrue(self.model.documented_cabral_stop_can_reprovision(state))
        self.assertEqual(
            self.model.session.port.availability("MOZ", PortServiceKind.PROVISIONS),
            before,
        )

    def test_malindi_generic_service_is_not_changed_by_cabral_stop(self):
        before = self.model.session.port.availability("MAL", PortServiceKind.PROVISIONS)
        state = self.at_malindi_with_documented_africa_actions(24001)
        self.assertEqual(state.active_stop_id, "CABRAL1500_MAL")
        self.assertTrue(self.model.documented_cabral_stop_can_reprovision(state))
        self.assertEqual(
            self.model.session.port.availability("MAL", PortServiceKind.PROVISIONS),
            before,
        )

    def test_documented_water_wood_action_is_specific_one_shot_and_zero_day(self):
        state = self.at_vera_cruz(24001)
        self.assertTrue(self.model.documented_cabral_stop_can_reprovision(state))
        before_date = state.vessel.clock.current_date
        before = state.vessel.provision_days
        result = self.model.reprovision_at_documented_cabral_stop(state)
        self.assertTrue(result.executed, result.reasons)
        self.assertEqual(result.service_result.effect, 5.0)
        self.assertEqual(result.service_result.days_spent, 0)
        self.assertEqual(result.state_after.vessel.clock.current_date, before_date)
        self.assertEqual(result.state_after.vessel.provision_days, before + 5.0)
        self.assertFalse(
            self.model.documented_cabral_stop_can_reprovision(result.state_after)
        )
        repeated = self.model.reprovision_at_documented_cabral_stop(result.state_after)
        self.assertFalse(repeated.executed)
        self.assertIn("DOCUMENTED_PROVISION_ACTION_ALREADY_USED", repeated.reasons)

    def test_five_day_effect_resolves_typical_vera_cruz_shortfall(self):
        state = self.at_vera_cruz(24001)
        result = self.model.reprovision_at_documented_cabral_stop(state)
        released = self.model.wait_for_stop_release(result.state_after)
        self.assertTrue(released.executed, released.reasons)
        plan = self.model.plan_current_leg(released.state_after, seed=24001)
        self.assertTrue(plan.feasible, plan.blockers)
        self.assertEqual(plan.route_id, "R_VCR_MOZ_CAB")
        self.assertEqual(plan.provision_days_required, 79.0)

    def test_mozambique_ten_day_effect_supports_horizon_to_malindi(self):
        state = self.at_mozambique_with_documented_vcr_action(24001)
        before_date = state.vessel.clock.current_date
        result = self.model.reprovision_at_documented_cabral_stop(state)
        self.assertTrue(result.executed, result.reasons)
        self.assertEqual(result.service_result.effect, 10.0)
        self.assertEqual(result.service_result.days_spent, 0)
        self.assertEqual(result.state_after.vessel.clock.current_date, before_date)
        self.assertFalse(
            self.model.documented_cabral_stop_can_reprovision(result.state_after)
        )
        moz_kil = self.model.plan_current_leg(result.state_after, seed=24001)
        self.assertTrue(moz_kil.feasible, moz_kil.blockers)
        state = self.model.execute_voyage(result.state_after, moz_kil)
        released = self.model.wait_for_stop_release(state)
        self.assertTrue(released.executed)
        kil_mal = self.model.plan_current_leg(released.state_after, seed=24001)
        self.assertTrue(kil_mal.feasible, kil_mal.blockers)
        self.assertEqual(kil_mal.route_id, "R_KIL_MAL_CAB")

    def test_malindi_fifteen_day_effect_supports_departure_to_anjediva(self):
        state = self.at_malindi_with_documented_africa_actions(24001)
        before_date = state.vessel.clock.current_date
        result = self.model.reprovision_at_documented_cabral_stop(state)
        self.assertTrue(result.executed, result.reasons)
        self.assertEqual(result.service_result.effect, 15.0)
        self.assertEqual(result.service_result.days_spent, 0)
        self.assertEqual(result.state_after.vessel.clock.current_date, before_date)
        released = self.model.wait_for_stop_release(result.state_after)
        self.assertTrue(released.executed)
        plan = self.model.plan_current_leg(released.state_after, seed=24001)
        self.assertTrue(plan.feasible, plan.blockers)
        self.assertEqual(plan.route_id, "R_MAL_ANJ_CAB")
        self.assertEqual(plan.provision_days_required, 15.0)

    def test_rare_first_leg_loss_is_not_erased_by_vera_cruz_action(self):
        state = self.at_vera_cruz(24002)
        self.assertLess(state.vessel.provision_days, 60.0)
        result = self.model.reprovision_at_documented_cabral_stop(state)
        self.assertTrue(result.executed)
        released = self.model.wait_for_stop_release(result.state_after)
        self.assertTrue(released.executed)
        plan = self.model.plan_current_leg(released.state_after, seed=24002)
        self.assertFalse(plan.feasible)
        self.assertIn("INSUFFICIENT_PROVISIONS", plan.blockers)


if __name__ == "__main__":
    unittest.main()
