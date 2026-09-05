import unittest
from datetime import date

from quintoimperio.domain import (
    GameClock,
    MonsoonPhase,
    NavigationModel,
    great_circle_nm,
    monsoon_phase,
)


class NavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = NavigationModel()

    def test_great_circle_is_symmetric_and_zero_at_same_point(self):
        a = great_circle_nm(-3.2192, 40.1169, 11.2588, 75.7804)
        b = great_circle_nm(11.2588, 75.7804, -3.2192, 40.1169)
        self.assertAlmostEqual(a, b, places=9)
        self.assertEqual(great_circle_nm(1.0, 2.0, 1.0, 2.0), 0.0)

    def test_malindi_calicut_has_two_preserved_1498_observations(self):
        self.assertEqual(sorted(self.model.observed_days("R_MAL_CAL")), [26, 27])

    def test_reference_progress_is_plausible_but_not_historical_speed_claim(self):
        # Faixa larga: apenas protege contra erros de unidade/coordenada.
        self.assertGreater(self.model.reference_daily_nm, 50.0)
        self.assertLess(self.model.reference_daily_nm, 120.0)

    def test_reference_route_base_duration_is_mean_of_preserved_observations(self):
        base = self.model.base_duration_days("R_MAL_CAL", date(1498, 4, 24))
        self.assertIsNotNone(base)
        self.assertAlmostEqual(base, 26.5, places=6)

    def test_april_estimate_matches_reference_order_of_magnitude(self):
        days = self.model.estimate_duration_days(
            "R_MAL_CAL", date(1498, 4, 24), seed=1498
        )
        self.assertIsNotNone(days)
        self.assertGreater(days, 23.0)
        self.assertLess(days, 30.0)

    def test_june_july_high_monsoon_dependence_increases_duration(self):
        april = self.model.estimate_duration_days(
            "R_MAL_CAL", date(1498, 4, 24), seed=7
        )
        june = self.model.estimate_duration_days(
            "R_MAL_CAL", date(1498, 6, 24), seed=7
        )
        self.assertIsNotNone(april)
        self.assertIsNotNone(june)
        self.assertGreater(june, april * 1.4)

    def test_navigation_is_deterministic_for_same_seed(self):
        first = self.model.estimate_duration_days(
            "R_MAL_CAL", date(1498, 4, 24), seed=42
        )
        second = self.model.estimate_duration_days(
            "R_MAL_CAL", date(1498, 4, 24), seed=42
        )
        self.assertEqual(first, second)

    def test_missing_coordinates_are_not_fabricated(self):
        self.assertIsNone(self.model.route_geodesic_nm("R_SOF_KIL"))

    def test_general_monsoon_calendar(self):
        self.assertEqual(monsoon_phase(date(1498, 12, 1)), MonsoonPhase.NORTHEAST)
        self.assertEqual(monsoon_phase(date(1498, 3, 1)), MonsoonPhase.TRANSITION_NE_SW)
        self.assertEqual(monsoon_phase(date(1498, 5, 1)), MonsoonPhase.SOUTHWEST)
        self.assertEqual(monsoon_phase(date(1498, 9, 1)), MonsoonPhase.TRANSITION_SW_NE)

    def test_game_clock_advances_without_mutating_original(self):
        clock = GameClock(date(1498, 4, 24))
        later = clock.advance(27)
        self.assertEqual(clock.current_date, date(1498, 4, 24))
        self.assertEqual(later.current_date, date(1498, 5, 21))
        self.assertEqual(later.monsoon, MonsoonPhase.SOUTHWEST)


if __name__ == "__main__":
    unittest.main()
