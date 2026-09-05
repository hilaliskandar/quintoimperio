import unittest

import pygame

from prototype.game import MAP_RECT, PlayablePrototype
from quintoimperio.domain import MapExtent


class InterfaceMapLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.font.init()
        cls.font = pygame.font.SysFont("sans", 15)

    @classmethod
    def tearDownClass(cls):
        pygame.font.quit()

    def assert_default_labels_do_not_overlap(self, scenario: str) -> None:
        app = PlayablePrototype(scenario)
        points = app.visible_points()
        extent = MapExtent.from_points(points)
        occupied: list[pygame.Rect] = []

        for point in points:
            x, y = app.world.project(
                point, extent, MAP_RECT.width, MAP_RECT.height, 35
            )
            x += MAP_RECT.left
            y += MAP_RECT.top
            label = self.font.render(point.label, True, (0, 0, 0))
            rect = app._place_map_label(label, x, y, occupied)
            for previous in occupied:
                self.assertFalse(
                    rect.colliderect(previous.inflate(4, 2)),
                    msg=(
                        f"Sobreposição de rótulos em {scenario}: "
                        f"{point.node_id} {rect} contra {previous}"
                    ),
                )
            self.assertTrue(MAP_RECT.inflate(-8, -8).contains(rect))
            occupied.append(rect)

    def test_historical_default_map_labels_do_not_overlap(self):
        self.assert_default_labels_do_not_overlap("HISTORICAL")

    def test_technical_default_map_labels_do_not_overlap(self):
        self.assert_default_labels_do_not_overlap("TECHNICAL")


if __name__ == "__main__":
    unittest.main()
