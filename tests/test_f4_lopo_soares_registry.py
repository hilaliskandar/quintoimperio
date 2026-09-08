import unittest

from quintoimperio.domain import ExpeditionModel


class F4LopoSoaresRegistryTests(unittest.TestCase):
    def test_lopo_soares_1504_is_registered_as_documentary_expedition(self):
        model = ExpeditionModel()
        expedition = model.expeditions["EXP_LOPO_SOARES_1504"]

        self.assertEqual(expedition["leader"], "Lopo Soares de Albergaria")
        self.assertEqual(expedition["period_from"], "1504")
        self.assertEqual(expedition["period_to"], "1505")
        self.assertEqual(expedition["source_id"], "EVE_ARMADAS_MANUEL")

    def test_lopo_soares_1504_has_no_playable_legs_yet(self):
        model = ExpeditionModel()

        self.assertEqual(model.legs.get("EXP_LOPO_SOARES_1504", ()), ())
        with self.assertRaisesRegex(KeyError, "Expedicao sem pernas"):
            model.first_sequence("EXP_LOPO_SOARES_1504")


if __name__ == "__main__":
    unittest.main()
