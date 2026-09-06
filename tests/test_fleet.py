import math
import unittest

from quintoimperio.domain.fleet import (
    ConsumableRates,
    EvidenceClass,
    FleetModel,
    ProvisionLoad,
)


class FleetModelTests(unittest.TestCase):
    def test_base_gama_1497_matches_research_scenario(self) -> None:
        fleet = FleetModel.base_gama_1497()

        self.assertEqual(fleet.persons, 170)
        self.assertEqual(fleet.burden_toneis, 350)
        self.assertEqual([v.persons for v in fleet.vessels], [70, 50, 30, 20])
        self.assertEqual([v.burden_toneis for v in fleet.vessels], [100, 90, 50, 110])
        self.assertTrue(
            all(v.burden_evidence is EvidenceClass.RECONSTRUCTION for v in fleet.vessels)
        )

    def test_daily_consumption_order_of_magnitude_is_reproducible(self) -> None:
        model = FleetModel()
        fleet = model.base_gama_1497()
        total = sum(model.daily_consumption(v).major_consumables_mass_kg for v in fleet.vessels)

        self.assertTrue(math.isclose(model.rates.major_consumables_kg_per_person_day, 4.983))
        self.assertTrue(math.isclose(total, 847.11))

    def test_research_loading_scenario_reproduces_spreadsheet_mass(self) -> None:
        model = FleetModel()
        fleet = model.load_research_scenario()

        self.assertTrue(math.isclose(fleet.provisions.major_consumables_mass_kg / 1000, 76.2399))
        self.assertTrue(math.isclose(fleet.provisions.liquid_volume_m3, 57.2832))
        self.assertTrue(math.isclose(model.autonomy_days(fleet.vessel("SAO_GABRIEL")), 60.0))
        # O navio de mantimentos leva sua autonomia propria mais reserva da armada;
        # a autonomia calculada para sua propria tripulacao e, portanto, maior que 60.
        self.assertGreater(model.autonomy_days(fleet.vessel("SUPPLY")), 60.0)

    def test_transfer_conserves_each_resource(self) -> None:
        model = FleetModel()
        fleet = model.load_research_scenario()
        before = fleet.provisions
        transfer = model.provision_for(persons=10, days=2)

        after_fleet = model.transfer_provisions(fleet, "SUPPLY", "BERRIO", transfer)
        after = after_fleet.provisions

        for resource in ("water_l", "wine_l", "biscuit_kg", "meat_kg"):
            self.assertTrue(
                math.isclose(
                    getattr(after, resource),
                    getattr(before, resource),
                    rel_tol=0.0,
                    abs_tol=1e-9,
                )
            )
        self.assertNotEqual(
            after_fleet.vessel("SUPPLY").provisions,
            fleet.vessel("SUPPLY").provisions,
        )
        self.assertNotEqual(
            after_fleet.vessel("BERRIO").provisions,
            fleet.vessel("BERRIO").provisions,
        )

    def test_transfer_rejects_resource_creation_by_overdraw(self) -> None:
        model = FleetModel()
        fleet = model.load_research_scenario()
        impossible = ProvisionLoad(water_l=10**9)

        with self.assertRaises(ValueError):
            model.transfer_provisions(fleet, "BERRIO", "SAO_GABRIEL", impossible)

    def test_consumption_sensitivity_scales_only_rates(self) -> None:
        base = ConsumableRates()
        low = base.scaled(0.8)
        high = base.scaled(1.2)

        self.assertTrue(math.isclose(low.major_consumables_kg_per_person_day, 4.983 * 0.8))
        self.assertTrue(math.isclose(high.major_consumables_kg_per_person_day, 4.983 * 1.2))
        self.assertIs(low.evidence, EvidenceClass.ANALOGY)
        self.assertIs(high.evidence, EvidenceClass.ANALOGY)


if __name__ == "__main__":
    unittest.main()
