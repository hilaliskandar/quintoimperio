import sys
import tempfile
import unittest
from pathlib import Path

PROTOTYPE_DIR = Path(__file__).resolve().parents[1] / "prototype"
if str(PROTOTYPE_DIR) not in sys.path:
    sys.path.insert(0, str(PROTOTYPE_DIR))

from quintoimperio.domain import SAVE_SCHEMA_VERSION
from game_m6 import M6HistoricalCampaignPrototype


class InterfaceM6Tests(unittest.TestCase):
    def test_save_and_load_restore_domain_state_and_seed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "slot.json"
            app = M6HistoricalCampaignPrototype(path)
            original = app.state
            self.assertTrue(app.session.in_predeparture_phase(original))
            app.session_seed = 1777
            app.save_slot()
            self.assertTrue(path.exists())

            app.state = app.session.wait_for_guided_departure(app.state).state_after
            plan = app.session.plan_current_leg(app.state, seed=app.session_seed)
            self.assertTrue(plan.feasible)
            app.state = app.session.execute_voyage(app.state, plan)
            app.session_seed = 1
            app.selected_route = "R_STG_SHB"
            app.pending_travel_route = "R_STG_SHB"

            app.load_slot()

            self.assertEqual(app.state, original)
            self.assertTrue(app.session.in_predeparture_phase(app.state))
            self.assertEqual(app.session_seed, 1777)
            self.assertIsNone(app.selected_route)
            self.assertIsNone(app.pending_travel_route)
            self.assertIn(f"schema v{SAVE_SCHEMA_VERSION}", app.message)

    def test_missing_slot_does_not_change_state(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "absent.json"
            app = M6HistoricalCampaignPrototype(path)
            before = app.state
            app.load_slot()
            self.assertEqual(app.state, before)
            self.assertIn("Nenhum save encontrado", app.message)


if __name__ == "__main__":
    unittest.main()
