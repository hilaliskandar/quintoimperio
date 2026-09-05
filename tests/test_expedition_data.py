import unittest
from datetime import date

from quintoimperio.data.loader import RepositoryData


class ExpeditionDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo = RepositoryData()
        cls.expeditions = cls.repo.historical("expeditions.csv")
        cls.legs = cls.repo.historical("expedition_routes.csv")
        cls.stops = cls.repo.historical("expedition_stops.csv")
        cls.routes = {
            row["route_id"]: row for row in cls.repo.historical("routes.csv")
        }
        cls.nodes = {
            row["node_id"]: row for row in cls.repo.historical("nodes.csv")
        }

    def test_expedition_leg_references_and_sequences_are_valid(self):
        expedition_ids = {row["expedition_id"] for row in self.expeditions}
        grouped: dict[str, list[dict[str, str]]] = {}
        for row in self.legs:
            self.assertIn(row["expedition_id"], expedition_ids)
            self.assertIn(row["route_id"], self.routes)
            self.assertNotEqual(
                self.routes[row["route_id"]]["route_origin"],
                "STRATEGIC_AGGREGATE",
            )
            grouped.setdefault(row["expedition_id"], []).append(row)

        for rows in grouped.values():
            rows.sort(key=lambda row: int(row["sequence"]))
            self.assertEqual(
                [int(row["sequence"]) for row in rows],
                list(range(1, len(rows) + 1)),
            )
            for previous, current in zip(rows, rows[1:]):
                previous_route = self.routes[previous["route_id"]]
                current_route = self.routes[current["route_id"]]
                self.assertEqual(
                    previous_route["destination_node"], current_route["origin_node"]
                )

    def test_documented_stops_reference_real_nodes_and_expedition(self):
        expedition_ids = {row["expedition_id"] for row in self.expeditions}
        seen: set[str] = set()
        for row in self.stops:
            self.assertNotIn(row["stop_id"], seen)
            seen.add(row["stop_id"])
            self.assertIn(row["expedition_id"], expedition_ids)
            self.assertIn(row["node_id"], self.nodes)
            self.assertGreater(int(row["observed_stay_days"]), 0)
            arrival = date.fromisoformat(row["arrival_date"])
            departure = date.fromisoformat(row["departure_date"])
            self.assertGreater(departure, arrival)
            self.assertTrue(row["activities"])
            self.assertTrue(row["source_id"])

    def test_gama_logistics_stops_are_not_markets(self):
        for node_id in ("STG", "SHB", "SBR", "RCO", "RBS"):
            self.assertEqual(self.nodes[node_id]["market_scale"], "NONE")

    def test_long_atlantic_leg_fits_abstract_provision_cap(self):
        rules = {
            (row["rule_type"], row["key"]): float(row["value"])
            for row in self.repo.simulation("port_rules.csv")
        }
        observations = [
            row
            for row in self.repo.historical("voyage_observations.csv")
            if row["route_id"] == "R_STG_SHB"
        ]
        self.assertEqual(len(observations), 1)
        self.assertGreaterEqual(
            rules[("PROVISION_MAX_ONBOARD", "DEFAULT")],
            float(observations[0]["observed_days"]),
        )


if __name__ == "__main__":
    unittest.main()
