import unittest

from quintoimperio.domain import CommercialState, TradeModel


class TradeModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = TradeModel()

    def test_buy_documented_good_updates_capital_and_inventory(self):
        before = CommercialState(capital_index=100.0, capacity_total=100.0)
        result = self.model.buy(before, "CAL", "PEPPER", 2.0, year=1498, seed=7)
        self.assertTrue(result.executed)
        self.assertIs(result.state_before, before)
        self.assertGreater(result.state_after.quantity_of("PEPPER"), 0.0)
        self.assertLess(result.state_after.capital_index, before.capital_index)

    def test_buy_absent_market_is_blocked(self):
        before = CommercialState(capital_index=100.0, capacity_total=100.0)
        result = self.model.buy(before, "LIS", "PEPPER", 1.0, year=1498, seed=7)
        self.assertFalse(result.executed)
        self.assertIn("GOOD_NOT_DOCUMENTED_IN_MARKET", result.reasons)
        self.assertEqual(result.state_after, before)

    def test_restricted_good_is_blocked_independently_of_port_access_layer(self):
        before = CommercialState(capital_index=1000.0, capacity_total=100.0)
        result = self.model.buy(before, "ARG", "GOLD", 1.0, year=1498, seed=7)
        self.assertFalse(result.executed)
        self.assertIn("GOOD_RESTRICTED_BY_HISTORICAL_ACCESS_REGIME", result.reasons)
        self.assertEqual(result.state_after, before)

    def test_capacity_is_based_on_bulk_index(self):
        before = CommercialState(capital_index=1000.0, capacity_total=5.0)
        result = self.model.buy(before, "CAL", "PEPPER", 2.0, year=1498, seed=7)
        self.assertFalse(result.executed)
        self.assertIn("INSUFFICIENT_CARGO_CAPACITY", result.reasons)

    def test_insufficient_capital_blocks_purchase(self):
        before = CommercialState(capital_index=0.01, capacity_total=100.0)
        result = self.model.buy(before, "CAL", "PEPPER", 1.0, year=1498, seed=7)
        self.assertFalse(result.executed)
        self.assertIn("INSUFFICIENT_CAPITAL", result.reasons)

    def test_sell_requires_inventory(self):
        before = CommercialState(capital_index=10.0, capacity_total=100.0)
        result = self.model.sell(before, "ADE", "PEPPER", 1.0, year=1498, seed=7)
        self.assertFalse(result.executed)
        self.assertIn("INSUFFICIENT_INVENTORY", result.reasons)

    def test_cross_market_trade_can_sell_owned_good(self):
        start = CommercialState(capital_index=100.0, capacity_total=100.0)
        bought = self.model.buy(start, "CAL", "PEPPER", 1.0, year=1498, seed=7)
        self.assertTrue(bought.executed)
        sold = self.model.sell(bought.state_after, "ADE", "PEPPER", 1.0, year=1498, seed=7)
        self.assertTrue(sold.executed)
        self.assertAlmostEqual(sold.state_after.quantity_of("PEPPER"), 0.0)
        self.assertGreater(sold.state_after.capital_index, bought.state_after.capital_index)

    def test_same_market_round_trip_has_spread_cost(self):
        start = CommercialState(capital_index=100.0, capacity_total=100.0)
        bought = self.model.buy(start, "CAL", "PEPPER", 1.0, year=1498, seed=11)
        self.assertTrue(bought.executed)
        sold = self.model.sell(bought.state_after, "CAL", "PEPPER", 1.0, year=1498, seed=11)
        self.assertTrue(sold.executed)
        self.assertLess(sold.state_after.capital_index, start.capital_index)

    def test_trade_state_is_immutable(self):
        before = CommercialState(capital_index=100.0, capacity_total=100.0)
        result = self.model.buy(before, "CAL", "PEPPER", 1.0, year=1498, seed=7)
        self.assertEqual(before.capital_index, 100.0)
        self.assertEqual(before.cargo, ())
        self.assertNotEqual(result.state_after, before)


if __name__ == "__main__":
    unittest.main()
