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
        outbound = sorted(
            (row for row in self.legs if row["expedition_id"] == "EXP_GAMA_1497"),
            key=lambda row: int(row["sequence"]),
        )
        self.assertEqual(len(outbound), 10)
        self.assertEqual([int(row["sequence"]) for row in outbound], list(range(1, 11)))
        self.assertEqual(outbound[-1]["route_id"], "R_MAL_CAL")

    def test_return_subcampaign_is_continuous_to_rio_grande(self):
        return_legs = sorted(
            (
                row
                for row in self.legs
                if row["expedition_id"] == "EXP_GAMA_RETURN_1498"
            ),
            key=lambda row: int(row["sequence"]),
        )
        self.assertEqual(len(return_legs), 7)
        self.assertEqual([int(row["sequence"]) for row in return_legs], list(range(1, 8)))
        expected = [
            ("CAL", "SMI"),
            ("SMI", "ANJ"),
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
        for node_id in ("SMI", "BSR", "BRG"):
            node = self.nodes[node_id]
            self.assertEqual(node["node_type"], "NAVIGATION_POINT")
            self.assertEqual(node["access_regime"], "NAVIGATION_ONLY")
            self.assertEqual(node["market_scale"], "NONE")
            self.assertTrue(node["latitude"])
            self.assertTrue(node["longitude"])

        self.assertEqual(self.nodes["SMI"]["coordinate_confidence"], "MEDIUM")
        self.assertIn("Netrani", self.nodes["SMI"]["modern_name"])
        self.assertIn("alternativa", self.nodes["SMI"]["historical_notes"])
        for node_id in ("BSR", "BRG"):
            self.assertEqual(self.nodes[node_id]["coordinate_confidence"], "LOW")
            self.assertIn("proxy", self.nodes[node_id]["historical_notes"].lower())

    def test_santa_maria_is_brief_documented_contact_not_full_logistical_stop(self):
        stop = next(row for row in self.stops if row["stop_id"] == "GAMA1498_RET_SMI")
        self.assertEqual(stop["node_id"], "SMI")
        self.assertEqual(stop["observed_stay_days"], "0")
        self.assertIn("FISH_EXCHANGE", stop["activities"])
        self.assertNotIn("WATER", stop["activities"])
        self.assertNotIn("CARENING", stop["activities"])

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

    def test_return_observations_preserve_segmented_durations(self):
        expected = {
            "R_CAL_SMI": 16,
            "R_SMI_ANJ": 5,
            "R_ANJ_MAL": 94,
            "R_MAL_BSR": 2,
            "R_BSR_SBR": 35,
            "R_SBR_CGH_RET": 8,
            "R_CGH_BRG": 36,
        }
        selected = [
            row for row in self.observations if row["route_id"] in expected
        ]
        counts = {
            route_id: sum(row["route_id"] == route_id for row in selected)
            for route_id in expected
        }
        self.assertEqual(counts, {route_id: 1 for route_id in expected})
        rows = {row["route_id"]: row for row in selected}
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
