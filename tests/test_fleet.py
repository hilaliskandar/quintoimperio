import math

import pytest

from quintoimperio.domain.fleet import (
    ConsumableRates,
    EvidenceClass,
    FleetModel,
    ProvisionLoad,
)


def test_base_gama_1497_matches_research_scenario() -> None:
    fleet = FleetModel.base_gama_1497()

    assert fleet.persons == 170
    assert fleet.burden_toneis == 350
    assert [v.persons for v in fleet.vessels] == [70, 50, 30, 20]
    assert [v.burden_toneis for v in fleet.vessels] == [100, 90, 50, 110]
    assert all(v.burden_evidence is EvidenceClass.RECONSTRUCTION for v in fleet.vessels)


def test_daily_consumption_order_of_magnitude_is_reproducible() -> None:
    model = FleetModel()
    fleet = model.base_gama_1497()
    total = sum(model.daily_consumption(v).major_consumables_mass_kg for v in fleet.vessels)

    assert math.isclose(model.rates.major_consumables_kg_per_person_day, 4.983)
    assert math.isclose(total, 847.11)


def test_research_loading_scenario_reproduces_spreadsheet_mass() -> None:
    model = FleetModel()
    fleet = model.load_research_scenario()

    assert math.isclose(fleet.provisions.major_consumables_mass_kg / 1000, 76.2399)
    assert math.isclose(fleet.provisions.liquid_volume_m3, 57.2832)
    assert math.isclose(model.autonomy_days(fleet.vessel("SAO_GABRIEL")), 60.0)
    # O navio de mantimentos leva sua autonomia propria mais reserva da armada;
    # a autonomia calculada para sua propria tripulacao e, portanto, maior que 60.
    assert model.autonomy_days(fleet.vessel("SUPPLY")) > 60.0


def test_transfer_conserves_each_resource() -> None:
    model = FleetModel()
    fleet = model.load_research_scenario()
    before = fleet.provisions
    transfer = model.provision_for(persons=10, days=2)

    after_fleet = model.transfer_provisions(fleet, "SUPPLY", "BERRIO", transfer)
    after = after_fleet.provisions

    assert after == before
    assert after_fleet.vessel("SUPPLY").provisions != fleet.vessel("SUPPLY").provisions
    assert after_fleet.vessel("BERRIO").provisions != fleet.vessel("BERRIO").provisions


def test_transfer_rejects_resource_creation_by_overdraw() -> None:
    model = FleetModel()
    fleet = model.load_research_scenario()
    impossible = ProvisionLoad(water_l=10**9)

    with pytest.raises(ValueError):
        model.transfer_provisions(fleet, "BERRIO", "SAO_GABRIEL", impossible)


def test_consumption_sensitivity_scales_only_rates() -> None:
    base = ConsumableRates()
    low = base.scaled(0.8)
    high = base.scaled(1.2)

    assert math.isclose(low.major_consumables_kg_per_person_day, 4.983 * 0.8)
    assert math.isclose(high.major_consumables_kg_per_person_day, 4.983 * 1.2)
    assert low.evidence is EvidenceClass.ANALOGY
    assert high.evidence is EvidenceClass.ANALOGY
