import unittest

from quintoimperio.domain import ExpeditionModel


class F5AlmeidaRegistryTests(unittest.TestCase):
    def test_almeida_1505_is_registered_without_fixed_fleet_size(self):
        model = ExpeditionModel()
        expedition = model.expeditions["EXP_ALMEIDA_1505"]

        self.assertEqual(expedition["leader"], "D. Francisco de Almeida")
        self.assertEqual(expedition["period_from"], "1505")
        self.assertEqual(expedition["period_to"], "1509")
        self.assertEqual(expedition["expedition_type"], "ROYAL_EXPEDITION_VICEROYAL_MISSION")
        self.assertNotIn("fleet_size", expedition)
        self.assertIn("20, 21, 22 e 23", expedition["finance_notes"])

    def test_almeida_1505_has_no_playable_legs_in_first_increment(self):
        model = ExpeditionModel()

        self.assertEqual(model.legs.get("EXP_ALMEIDA_1505", ()), ())
        with self.assertRaisesRegex(KeyError, "Expedicao sem pernas"):
            model.first_sequence("EXP_ALMEIDA_1505")


if __name__ == "__main__":
    unittest.main()
