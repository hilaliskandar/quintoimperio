import unittest

from quintoimperio.domain import P3CampaignModel


class P3ExpeditionCapacityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = P3CampaignModel()

    def test_cabral_uses_expedition_specific_150_cap_without_changing_global_mvp_cap(self):
        self.assertEqual(self.model.cabral_provision_cap, 150.0)
        self.assertEqual(
            self.model.session.port.rules[("PROVISION_MAX_ONBOARD", "DEFAULT")],
            120.0,
        )
        historical = self.model.initial_cabral_state()
        playable = self.model.initial_cabral_playable_state()
        self.assertEqual(historical.vessel.provision_days, 150.0)
        self.assertEqual(playable.vessel.provision_days, 150.0)

    def test_documented_stop_action_respects_cabral_cap_not_global_cap(self):
        state = self.model.initial_cabral_state()
        first = self.model.plan_current_leg(state, seed=24001)
        self.assertTrue(first.feasible, first.blockers)
        state = self.model.execute_voyage(state, first)
        self.assertGreater(state.vessel.provision_days, 120.0)
        result = self.model.reprovision_at_documented_cabral_stop(state)
        self.assertTrue(result.executed, result.reasons)
        self.assertLessEqual(result.state_after.vessel.provision_days, 150.0)
        self.assertEqual(result.service_result.effect, 5.0)


if __name__ == "__main__":
    unittest.main()
