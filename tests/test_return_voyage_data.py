import unittest
from datetime import date

from quintoimperio.data.loader import RepositoryData


class ReturnVoyageDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo = RepositoryData()
        cls.nodes = {row["node_id"]: row for row in cls.repo.historical("nodes.csv")}
        cls.routes = {row["route_id"]: row for row in cls.repo.historical("routes.csv")}
        cls.legs = cls.repo.historical("expedition_routes.csv")
        cls.stops = cls.repo.historical("expedition_stops.csv")
        cls.observations = cls.repo.historical("voyage_observations.csv")

    def test_mvp_outbound_expedition_remains_exactly_ten_legs(self):
        outbound = [
            row for row in self.legs if row["expedition_id"] == "EXP_GAMA_1497"
        ]
        self.assertEqual(len(outbound), 10)
        self.assertEqual([int(row["sequence"]) for row in outbound], list(range(1, 11)))
        self.assertEqual(outbound[-1]["route_id"], "R_MAL_CAL")

    def test_return_subcampaign_is_continuous_to_rio_grande(self):
        return_legs = [
            row
            for row in self.legs
            if row["expedition_id"] == "EXP_GAMA_RETURN_1498"
        ]
        self.assertEqual(len(return_legs), 6)
        self.assertEqual([int(row["sequence"]) for row in return_legs], list(range(1, 7)))
        expected = [
            ("CAL", "ANJ"),
            ("ANJ", "MAL"),
            ("MAL", "BSR"),
            ("BSR", "SBR"),
            ("SBR", "CGH"),
            ("CGH", "BRG"),
        ]
        actual = [
            (
                self.routes[row["route_id"]]["origin_node"],
                self.routes[row["route_id"]]["destination_node"],
            )
            for row in return_legs
        ]
        self.assertEqual(actual, expected)

    def test_return_does_not_reuse_rgr_identifier(self):
        self.assertEqual(self.nodes["RGR"]["historical_name"], "Ribeira Grande de Santiago")
        self.assertEqual(self.nodes["BRG"]["historical_name"], "Baixos do Rio Grande")

    def test_new_return_nodes_do_not_invent_markets(self):
        self.assertEqual(self.nodes["ANJ"]["market_scale"], "NONE")
        self.assertEqual(self.nodes["BSR"]["node_type"], "NAVIGATION_POINT")
        self.assertEqual(self.nodes["BSR"]["access_regime"], "NAVIGATION_ONLY")
        self.assertEqual(self.nodes["BRG"]["node_type"], "NAVIGATION_POINT")
        self.assertEqual(self.nodes["BRG"]["access_regime"], "NAVIGATION_ONLY")
        self.assertEqual(self.nodes["BSR"]["latitude"], "")
        self.assertEqual(self.nodes["BRG"]["latitude"], "")

    def test_anjediva_is_only_new_full_logistical_stop(self):
        stop = next(row for row in self.stops if row["stop_id"] == "GAMA1498_RET_ANJ")
        self.assertEqual(stop["node_id"], "ANJ")
        self.assertIn("WATER", stop["activities"])
        self.assertIn("CARENING", stop["activities"])
        self.assertEqual(stop["observed_stay_days"], "12")
        self.assertEqual(self.nodes["ANJ"]["coordinate_confidence"], "HIGH")

    def test_sao_rafael_burn_is_specific_return_stop_evidence(self):
        stop = next(row for row in self.stops if row["stop_id"] == "GAMA1499_RET_BSR")
        self.assertEqual(stop["expedition_id"], "EXP_GAMA_RETURN_1498")
        self.assertIn("SHIP_ABANDONMENT", stop["activities"])
        self.assertIn("CARGO_TRANSFER", stop["activities"])
        self.assertIn("específico", stop["notes"])

    def test_return_observations_preserve_ravenstein_summary_durations(self):
        expected = {
            "R_CAL_ANJ": 21,
            "R_ANJ_MAL": 94,
            "R_MAL_BSR": 2,
            "R_BSR_SBR": 35,
            "R_SBR_CGH_RET": 8,
            "R_CGH_BRG": 36,
        }
        rows = {
            row["route_id"]: row
            for row in self.observations
            if row["route_id"] in expected
        }
        self.assertEqual(set(rows), set(expected))
        for route_id, days in expected.items():
            row = rows[route_id]
            self.assertEqual(int(row["observed_days"]), days)
            elapsed = (
                date.fromisoformat(row["arrival_date"])
                - date.fromisoformat(row["departure_date"])
            ).days
            self.assertEqual(elapsed, days)

    def test_primary_return_data_stops_at_april_25_1499(self):
        return_obs = [
            row
            for row in self.observations
            if row["observation_id"].startswith("GAMA149") and "_RET_" in row["observation_id"]
        ]
        self.assertTrue(return_obs)
        self.assertEqual(max(row["arrival_date"] for row in return_obs), "1499-04-25")
        self.assertFalse(
            any(
                row["arrival_node"] in {"LIS", "STG"}
                for row in return_obs
            )
        )


if __name__ == "__main__":
    unittest.main()
