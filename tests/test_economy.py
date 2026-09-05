import unittest

from prototype.economy import EconomyModel


class EconomyPrototypeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = EconomyModel()

    def test_pepper_is_more_available_in_calicut_than_lisbon(self):
        self.assertGreater(
            self.model.availability_score("CAL", "PEPPER", 1498),
            self.model.availability_score("LIS", "PEPPER", 1498),
        )

    def test_african_gold_has_high_exchange_power(self):
        self.assertEqual(self.model.exchange_power("GOLD"), 5.0)
        self.assertGreater(
            self.model.exchange_power("GOLD"),
            self.model.exchange_power("SUGAR"),
        )

    def test_transit_stock_in_mozambique_is_more_volatile_than_malabar_hinterland(self):
        self.assertGreater(
            self.model.volatility("MOZ", "PEPPER", 1498),
            self.model.volatility("CAL", "PEPPER", 1498),
        )

    def test_indian_textiles_enable_eastern_route(self):
        self.assertTrue(
            self.model.route_supports_good("R_CAM_MLK", "TEXTILE_IND", 1498)
        )
        flows = self.model.goods_on_route("R_CAM_MLK", 1498)
        textile = [row for row in flows if row["good_id"] == "TEXTILE_IND"]
        self.assertEqual(len(textile), 1)
        self.assertEqual(textile[0]["flow_direction"], "EASTBOUND")

    def test_market_shocks_are_deterministic_for_same_seed(self):
        first = self.model.market_quote("MOZ", "PEPPER", 1498, seed=42)
        second = self.model.market_quote("MOZ", "PEPPER", 1498, seed=42)
        self.assertEqual(first, second)

    def test_different_seed_changes_transit_stock(self):
        first = self.model.market_quote("MOZ", "PEPPER", 1498, seed=1)
        second = self.model.market_quote("MOZ", "PEPPER", 1498, seed=2)
        self.assertIsNotNone(first)
        self.assertIsNotNone(second)
        self.assertNotEqual(first["stock_index"], second["stock_index"])

    def test_route_cost_exposes_required_components(self):
        cost = self.model.route_cost("R_CAM_MLK", "TEXTILE_IND", 1498, seed=7)
        for key in (
            "freight_index",
            "provisions_index",
            "taxation_access_index",
            "intermediation_index",
            "total_cost_index",
        ):
            self.assertGreater(cost[key], 0.0)

    def test_absent_market_is_not_fabricated(self):
        self.assertIsNone(self.model.market_quote("LIS", "PEPPER", 1498, seed=0))


if __name__ == "__main__":
    unittest.main()
