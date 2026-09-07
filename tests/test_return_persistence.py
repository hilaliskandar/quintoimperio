import unittest
from datetime import date

from quintoimperio.domain.persistence import CampaignPersistence
from quintoimperio.domain.return_campaign import ReturnCampaignModel
from quintoimperio.domain.stop import ChronologyMode


class ReturnPersistenceTests(unittest.TestCase):
    def test_save_load_preserves_return_state_seed_and_one_shot_action(self):
        model = ReturnCampaignModel()
        persistence = CampaignPersistence()
        state = model.session.initial_state(
            location_node="CAL",
            start_date=date(1498, 5, 22),
            provision_days=30.0,
            active_expedition_id=None,
            chronology_mode=ChronologyMode.GUIDED,
        )
        state = model.activate_return(state)
        state = model.wait_for_guided_departure(state).state_after
        plan = model.plan_current_leg(state, seed=23001)
        self.assertTrue(plan.feasible, plan.blockers)
        state = model.execute_voyage(state, plan)
        self.assertEqual(state.vessel.location_node, "SMI")
        self.assertEqual(state.active_stop_id, "GAMA1498_RET_SMI")

        provision = model.reprovision_at_documented_stop(state, 5.0)
        self.assertTrue(provision.executed, provision.reasons)
        state = provision.state_after

        loaded = persistence.loads(persistence.dumps(state, seed=23001))
        self.assertEqual(loaded.seed, 23001)
        self.assertEqual(loaded.state.active_expedition_id, model.RETURN_EXPEDITION_ID)
        self.assertEqual(loaded.state.expedition_leg_sequence, 2)
        self.assertEqual(loaded.state.active_stop_id, "GAMA1498_RET_SMI")
        self.assertIs(loaded.state.chronology_mode, ChronologyMode.GUIDED)
        self.assertEqual(loaded.state.vessel.location_node, "SMI")
        self.assertFalse(model.documented_stop_can_reprovision(loaded.state))
        repeated = model.reprovision_at_documented_stop(loaded.state, 1.0)
        self.assertFalse(repeated.executed)
        self.assertIn("DOCUMENTED_PROVISION_ACTION_ALREADY_USED", repeated.reasons)


if __name__ == "__main__":
    unittest.main()
