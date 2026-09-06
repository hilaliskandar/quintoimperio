import unittest

import pygame

from prototype.game_m3 import M3PlayablePrototype


class InterfaceTradeM3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.font.init()

    @classmethod
    def tearDownClass(cls):
        pygame.font.quit()

    def test_quantity_is_selectable_and_bounded(self):
        app = M3PlayablePrototype("TECHNICAL")
        self.assertEqual(app.trade_quantity, 1.0)
        app.adjust_trade_quantity(4.0)
        self.assertEqual(app.trade_quantity, 5.0)
        app.adjust_trade_quantity(-99.0)
        self.assertEqual(app.trade_quantity, 1.0)
        app.adjust_trade_quantity(99.0)
        self.assertEqual(app.trade_quantity, 20.0)

    def test_buy_and_sell_use_selected_quantity(self):
        app = M3PlayablePrototype("TECHNICAL")
        app.selected_good = "PEPPER"
        app.trade_quantity = 3.0
        before_capital = app.state.commerce.capital_index
        before_free = app.session.trade.capacity_free(app.state.commerce)

        app.buy_selected()
        self.assertAlmostEqual(app.state.commerce.quantity_of("PEPPER"), 3.0)
        self.assertLess(app.state.commerce.capital_index, before_capital)
        self.assertLess(app.session.trade.capacity_free(app.state.commerce), before_free)
        self.assertIn("Compra: 3 PEPPER", app.message)

        app.trade_quantity = 2.0
        app.sell_selected()
        self.assertAlmostEqual(app.state.commerce.quantity_of("PEPPER"), 1.0)
        self.assertIn("Venda: 2 PEPPER", app.message)

    def test_inventory_block_is_presented_in_plain_language(self):
        app = M3PlayablePrototype("TECHNICAL")
        app.selected_good = "PEPPER"
        app.trade_quantity = 2.0
        app.sell_selected()
        self.assertIn("quantidade em posse insuficiente", app.message)
        self.assertNotIn("INSUFFICIENT_INVENTORY", app.message)

    def test_session_access_and_knowledge_blocks_are_translated(self):
        friendly = M3PlayablePrototype._friendly_reasons(
            (
                "MARKET_KNOWLEDGE_NOT_OPERATIONAL",
                "PORT_ACCESS_NEGOTIATION_REQUIRED",
                "PORT_ACCESS_RESTRICTED",
                "PORT_HAS_NO_COMMERCIAL_ACCESS",
                "PORT_ACCESS_UNKNOWN",
                "PORT_ACCESS_NOT_GRANTED",
            )
        )
        for internal_code in (
            "MARKET_KNOWLEDGE_NOT_OPERATIONAL",
            "PORT_ACCESS_NEGOTIATION_REQUIRED",
            "PORT_ACCESS_RESTRICTED",
            "PORT_HAS_NO_COMMERCIAL_ACCESS",
            "PORT_ACCESS_UNKNOWN",
            "PORT_ACCESS_NOT_GRANTED",
        ):
            self.assertNotIn(internal_code, friendly)
        self.assertIn("conhecimento do mercado", friendly)
        self.assertIn("exige negociação", friendly)

    def test_render_exposes_quantity_controls_and_capacity(self):
        app = M3PlayablePrototype("TECHNICAL")
        surface = pygame.Surface((1400, 820))
        app.render(surface)
        quantity_targets = [
            target for target in app.targets if target.kind == "trade_quantity"
        ]
        self.assertTrue(quantity_targets)
        self.assertTrue(any(target.value == "+1" for target in quantity_targets))

    def test_plus_control_is_disabled_at_maximum(self):
        app = M3PlayablePrototype("TECHNICAL")
        app.trade_quantity = app.MAX_TRADE_QUANTITY
        surface = pygame.Surface((1400, 820))
        app.render(surface)
        quantity_targets = [
            target for target in app.targets if target.kind == "trade_quantity"
        ]
        self.assertFalse(any(target.value == "+1" for target in quantity_targets))
        self.assertTrue(any(target.value == "-1" for target in quantity_targets))

    def test_reset_restores_trade_quantity(self):
        app = M3PlayablePrototype("TECHNICAL")
        app.trade_quantity = 7.0
        app.reset()
        self.assertEqual(app.trade_quantity, 1.0)


if __name__ == "__main__":
    unittest.main()
