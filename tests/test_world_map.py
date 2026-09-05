import unittest

from quintoimperio.domain import KnowledgeLevel, MapExtent, WorldMapModel


class WorldMapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = WorldMapModel()

    def test_player_map_shows_known_atlantic_nodes_and_indirect_calicut(self):
        visible = {point.node_id for point in self.model.visible_nodes("PLAYER")}
        self.assertIn("LIS", visible)
        self.assertIn("CGH", visible)
        self.assertIn("CAL", visible)
        self.assertIn("MPI", visible)
        self.assertNotIn("MAL", visible)
        self.assertNotIn("MOZ", visible)
        self.assertNotIn("SOF", visible)

    def test_all_current_nodes_have_explicit_coordinate_anchors(self):
        for node_id, row in self.model.nodes.items():
            with self.subTest(node_id=node_id):
                self.assertTrue(row["latitude"])
                self.assertTrue(row["longitude"])

    def test_provisional_anchor_coordinates_are_explicit(self):
        mpinda = self.model.point_for_node("MPI", "PLAYER")
        sofal = self.model.point_for_node("SOF", "CROWN")
        self.assertIsNotNone(mpinda)
        self.assertIsNotNone(sofal)
        self.assertAlmostEqual(mpinda.latitude, -6.1981, places=4)
        self.assertAlmostEqual(mpinda.longitude, 12.3933, places=4)
        self.assertAlmostEqual(sofal.latitude, -20.1562, places=4)
        self.assertAlmostEqual(sofal.longitude, 34.7383, places=4)
        self.assertEqual(self.model.nodes["MPI"]["coordinate_confidence"], "MEDIUM")
        self.assertEqual(self.model.nodes["SOF"]["coordinate_confidence"], "MEDIUM")

    def test_calicut_is_visible_as_partial_geographic_knowledge(self):
        point = self.model.point_for_node("CAL", "PLAYER")
        self.assertIsNotNone(point)
        self.assertEqual(point.geo_knowledge, KnowledgeLevel.PARTIAL)

    def test_player_route_visibility_does_not_reveal_unknown_indian_ocean_routes(self):
        edges = {edge.route_id for edge in self.model.visible_routes("PLAYER")}
        self.assertIn("R_LIS_CGH", edges)
        self.assertNotIn("R_MAL_CAL", edges)
        self.assertNotIn("R_CAL_MLK", edges)

    def test_visible_routes_rejects_invalid_perspective_locally(self):
        with self.assertRaisesRegex(ValueError, "perspective deve ser PLAYER ou CROWN"):
            self.model.visible_routes("INVALID")

    def test_projection_preserves_east_west_order(self):
        lisbon = self.model.point_for_node("LIS", "PLAYER")
        calicut = self.model.point_for_node("CAL", "PLAYER")
        self.assertIsNotNone(lisbon)
        self.assertIsNotNone(calicut)
        extent = MapExtent.from_points(self.model.visible_nodes("PLAYER"))
        x_lisbon, _ = self.model.project(lisbon, extent, 1200, 700)
        x_calicut, _ = self.model.project(calicut, extent, 1200, 700)
        self.assertLess(x_lisbon, x_calicut)

    def test_map_point_uses_exact_node_coordinates(self):
        point = self.model.point_for_node("MAL", "CROWN")
        node = self.model.nodes["MAL"]
        self.assertIsNotNone(point)
        self.assertEqual(point.latitude, float(node["latitude"]))
        self.assertEqual(point.longitude, float(node["longitude"]))


if __name__ == "__main__":
    unittest.main()
