import unittest

from prototype.game_m5 import M5HistoricalCampaignPrototype


class InterfaceM5Tests(unittest.TestCase):
    def test_initial_campaign_status_is_derived_from_m4(self):
        app = M5HistoricalCampaignPrototype()
        progress = app.campaign_status()
        self.assertFalse(progress.completed)
        self.assertTrue(progress.current_objective)
        self.assertEqual(app.state.vessel.location_node, "LIS")

    def test_travel_requires_explicit_confirmation(self):
        app = M5HistoricalCampaignPrototype()
        app.selected_route = "R_LIS_STG"
        before = app.state

        app.travel_selected()

        self.assertEqual(app.state, before)
        self.assertEqual(app.pending_travel_route, "R_LIS_STG")
        self.assertIn("Confirmar viagem", app.message)

        app.confirm_travel()

        self.assertIsNone(app.pending_travel_route)
        self.assertEqual(app.state.vessel.location_node, "STG")
        self.assertNotEqual(app.state, before)

    def test_cancel_keeps_state_unchanged(self):
        app = M5HistoricalCampaignPrototype()
        app.selected_route = "R_LIS_STG"
        before = app.state
        app.travel_selected()
        app.cancel_travel()
        self.assertEqual(app.state, before)
        self.assertIsNone(app.pending_travel_route)
        self.assertIn("cancelada", app.message)

    def test_blockers_are_presented_in_short_language(self):
        text = M5HistoricalCampaignPrototype.friendly_reasons(
            ("HISTORICAL_DEPARTURE_NOT_REACHED", "INSUFFICIENT_PROVISIONS")
        )
        self.assertIn("aguarde a data histórica", text)
        self.assertIn("provisões insuficientes", text)
        self.assertNotIn("HISTORICAL_DEPARTURE_NOT_REACHED", text)

    def test_history_is_short_and_deduplicated(self):
        app = M5HistoricalCampaignPrototype()
        for index in range(10):
            app.message = f"evento {index}"
            app._remember()
        self.assertEqual(len(app.action_history), app.HISTORY_LIMIT)
        self.assertEqual(app.action_history[-1], "evento 9")
        before = tuple(app.action_history)
        app._remember()
        self.assertEqual(tuple(app.action_history), before)


if __name__ == "__main__":
    unittest.main()
