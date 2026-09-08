import unittest

from quintoimperio.domain import ExpeditionModel


class F5AnhaiaRegistryTests(unittest.TestCase):
    def test_anhaia_1505_is_separate_documentary_expedition(self):
        model = ExpeditionModel()
        expedition = model.expeditions["EXP_ANHAIA_1505"]

        self.assertEqual(expedition["leader"], "Pêro de Anhaia")
        self.assertEqual(expedition["period_from"], "1505")
        self.assertEqual(expedition["period_to"], "1506")
        self.assertEqual(expedition["expedition_type"], "ROYAL_FORTIFICATION_MISSION")
        self.assertIn("18/05/1505", expedition["finance_notes"])

    def test_anhaia_1505_has_no_playable_legs_or_almeida_compression(self):
        model = ExpeditionModel()

        self.assertIn("EXP_ALMEIDA_1505", model.expeditions)
        self.assertIn("EXP_ANHAIA_1505", model.expeditions)
        self.assertEqual(model.legs.get("EXP_ANHAIA_1505", ()), ())
        with self.assertRaisesRegex(KeyError, "Expedicao sem pernas"):
            model.first_sequence("EXP_ANHAIA_1505")


if __name__ == "__main__":
    unittest.main()
