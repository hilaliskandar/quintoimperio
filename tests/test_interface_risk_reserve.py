import sys
import unittest
from pathlib import Path

PROTOTYPE_DIR = Path(__file__).resolve().parents[1] / "prototype"
if str(PROTOTYPE_DIR) not in sys.path:
    sys.path.insert(0, str(PROTOTYPE_DIR))

from historical_campaign import HistoricalCampaignPrototype
from game_m5 import M5HistoricalCampaignPrototype


class RiskReserveInterfaceTests(unittest.TestCase):
    @staticmethod
    def _at_departure(app):
        if app.session.in_predeparture_phase(app.state):
            app.state = app.session.wait_for_guided_departure(app.state).state_after
        return app

    def test_selecting_reserve_does_not_create_resources(self):
        app = HistoricalCampaignPrototype()
        before = app.state
        app.set_secured_reserve(10)
        self.assertEqual(app.state, before)
        self.assertEqual(app.secured_reserve_days, 10.0)
        self.assertIn("Estoque não aumenta", app.message)

    def test_reserve_cost_is_charged_only_when_voyage_executes(self):
        app = self._at_departure(HistoricalCampaignPrototype())
        app.set_secured_reserve(10)
        capital_before = app.state.commerce.capital_index
        provisions_before = app.state.vessel.provision_days
        app.selected_route = "R_LIS_STG"
        app.travel_selected()
        self.assertEqual(app.state.vessel.location_node, "STG")
        self.assertAlmostEqual(app.state.commerce.capital_index, capital_before - 2.5)
        self.assertLess(app.state.vessel.provision_days, provisions_before)
        self.assertIn("proteção SIM 10d preparada", app.message)

    def test_m5_confirmation_preserves_selected_risk_policy(self):
        app = self._at_departure(M5HistoricalCampaignPrototype())
        app.set_secured_reserve(5)
        capital_before = app.state.commerce.capital_index
        app.selected_route = "R_LIS_STG"
        app.travel_selected()
        self.assertEqual(app.state.vessel.location_node, "LIS")
        self.assertEqual(app.pending_travel_route, "R_LIS_STG")
        app.confirm_travel()
        self.assertEqual(app.state.vessel.location_node, "STG")
        self.assertAlmostEqual(app.state.commerce.capital_index, capital_before - 1.25)

    def test_only_discrete_reserve_choices_are_accepted(self):
        app = HistoricalCampaignPrototype()
        with self.assertRaises(ValueError):
            app.set_secured_reserve(7)


if __name__ == "__main__":
    unittest.main()
