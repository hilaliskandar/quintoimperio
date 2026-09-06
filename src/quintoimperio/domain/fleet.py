"""Camada experimental de frota fisica para a armada de 1497.

Os valores deste modulo nao substituem o ``VesselState`` abstrato do MVP. Eles
existem para testar uma representacao fisica auditavel da frota, mantendo
separados: evidencia historica, reconstrucao historiografica, analogia tardia e
parametro de simulacao.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from math import isclose


class EvidenceClass(str, Enum):
    """Natureza epistemica de um valor usado pelo modelo."""

    DOCUMENTED = "DOCUMENTED"
    RECONSTRUCTION = "RECONSTRUCTION"
    ANALOGY = "ANALOGY"
    SIMULATION = "SIMULATION"


@dataclass(frozen=True)
class ConsumableRates:
    """Consumo diario experimental por pessoa.

    Agua e vinho sao armazenados em litros; biscoito e carne, em kg. Para
    estimar massa total dos componentes principais, a densidade dos liquidos e
    aproximada por 1 kg/L. Essa aproximacao e uma regra de calculo, nao uma
    medicao historica.
    """

    water_l: float = 2.738
    wine_l: float = 1.006
    biscuit_kg: float = 0.989
    meat_kg: float = 0.250
    liquid_density_kg_l: float = 1.0
    evidence: EvidenceClass = EvidenceClass.ANALOGY

    def __post_init__(self) -> None:
        for value in (
            self.water_l,
            self.wine_l,
            self.biscuit_kg,
            self.meat_kg,
            self.liquid_density_kg_l,
        ):
            if value < 0:
                raise ValueError("consumption rates cannot be negative")

    @property
    def major_consumables_kg_per_person_day(self) -> float:
        return (
            (self.water_l + self.wine_l) * self.liquid_density_kg_l
            + self.biscuit_kg
            + self.meat_kg
        )

    def scaled(self, factor: float) -> "ConsumableRates":
        if factor <= 0:
            raise ValueError("consumption scale must be positive")
        return replace(
            self,
            water_l=self.water_l * factor,
            wine_l=self.wine_l * factor,
            biscuit_kg=self.biscuit_kg * factor,
            meat_kg=self.meat_kg * factor,
        )


@dataclass(frozen=True)
class ProvisionLoad:
    """Carga fisica dos quatro consumiveis principais."""

    water_l: float = 0.0
    wine_l: float = 0.0
    biscuit_kg: float = 0.0
    meat_kg: float = 0.0

    def __post_init__(self) -> None:
        for value in (self.water_l, self.wine_l, self.biscuit_kg, self.meat_kg):
            if value < -1e-9:
                raise ValueError("provision quantities cannot be negative")

    @property
    def liquid_volume_m3(self) -> float:
        return (self.water_l + self.wine_l) / 1000.0

    @property
    def major_consumables_mass_kg(self) -> float:
        return self.water_l + self.wine_l + self.biscuit_kg + self.meat_kg

    def plus(self, other: "ProvisionLoad") -> "ProvisionLoad":
        return ProvisionLoad(
            water_l=self.water_l + other.water_l,
            wine_l=self.wine_l + other.wine_l,
            biscuit_kg=self.biscuit_kg + other.biscuit_kg,
            meat_kg=self.meat_kg + other.meat_kg,
        )

    def minus(self, other: "ProvisionLoad") -> "ProvisionLoad":
        result = ProvisionLoad(
            water_l=self.water_l - other.water_l,
            wine_l=self.wine_l - other.wine_l,
            biscuit_kg=self.biscuit_kg - other.biscuit_kg,
            meat_kg=self.meat_kg - other.meat_kg,
        )
        return result


@dataclass(frozen=True)
class PhysicalVessel:
    """Embarcacao experimental sem conversao automatica de tonel em massa."""

    vessel_id: str
    name: str
    role: str
    burden_toneis: float
    burden_min_toneis: float
    burden_max_toneis: float
    persons: int
    burden_evidence: EvidenceClass
    persons_evidence: EvidenceClass
    provisions: ProvisionLoad = ProvisionLoad()

    def __post_init__(self) -> None:
        if self.burden_toneis <= 0:
            raise ValueError("burden_toneis must be positive")
        if not (self.burden_min_toneis <= self.burden_toneis <= self.burden_max_toneis):
            raise ValueError("base burden must be inside sensitivity range")
        if self.persons <= 0:
            raise ValueError("persons must be positive")


@dataclass(frozen=True)
class FleetState:
    vessels: tuple[PhysicalVessel, ...]

    def __post_init__(self) -> None:
        ids = [v.vessel_id for v in self.vessels]
        if len(ids) != len(set(ids)):
            raise ValueError("vessel ids must be unique")

    @property
    def persons(self) -> int:
        return sum(v.persons for v in self.vessels)

    @property
    def burden_toneis(self) -> float:
        return sum(v.burden_toneis for v in self.vessels)

    @property
    def provisions(self) -> ProvisionLoad:
        total = ProvisionLoad()
        for vessel in self.vessels:
            total = total.plus(vessel.provisions)
        return total

    def vessel(self, vessel_id: str) -> PhysicalVessel:
        for vessel in self.vessels:
            if vessel.vessel_id == vessel_id:
                return vessel
        raise KeyError(vessel_id)


class FleetModel:
    """Operacoes puras sobre a frota fisica experimental."""

    SUPPLY_VESSEL_ID = "SUPPLY"

    def __init__(self, rates: ConsumableRates | None = None) -> None:
        self.rates = rates or ConsumableRates()

    @staticmethod
    def base_gama_1497() -> FleetState:
        """Cenario-base v0.1 da pesquisa, deliberadamente provisório."""

        return FleetState(
            vessels=(
                PhysicalVessel(
                    "SAO_GABRIEL",
                    "Sao Gabriel",
                    "flagship",
                    100.0,
                    90.0,
                    120.0,
                    70,
                    EvidenceClass.RECONSTRUCTION,
                    EvidenceClass.RECONSTRUCTION,
                ),
                PhysicalVessel(
                    "SAO_RAFAEL",
                    "Sao Rafael",
                    "main_ship",
                    90.0,
                    90.0,
                    100.0,
                    50,
                    EvidenceClass.RECONSTRUCTION,
                    EvidenceClass.RECONSTRUCTION,
                ),
                PhysicalVessel(
                    "BERRIO",
                    "Berrio",
                    "light_vessel",
                    50.0,
                    50.0,
                    50.0,
                    30,
                    EvidenceClass.RECONSTRUCTION,
                    EvidenceClass.RECONSTRUCTION,
                ),
                PhysicalVessel(
                    "SUPPLY",
                    "Navio de mantimentos",
                    "supply",
                    110.0,
                    110.0,
                    200.0,
                    20,
                    EvidenceClass.RECONSTRUCTION,
                    EvidenceClass.RECONSTRUCTION,
                ),
            )
        )

    def provision_for(self, persons: int, days: float) -> ProvisionLoad:
        if persons < 0 or days < 0:
            raise ValueError("persons and days cannot be negative")
        scale = persons * days
        return ProvisionLoad(
            water_l=self.rates.water_l * scale,
            wine_l=self.rates.wine_l * scale,
            biscuit_kg=self.rates.biscuit_kg * scale,
            meat_kg=self.rates.meat_kg * scale,
        )

    def daily_consumption(self, vessel: PhysicalVessel) -> ProvisionLoad:
        return self.provision_for(vessel.persons, 1.0)

    def autonomy_days(self, vessel: PhysicalVessel) -> float:
        daily = self.daily_consumption(vessel)
        ratios = []
        for stock, need in (
            (vessel.provisions.water_l, daily.water_l),
            (vessel.provisions.wine_l, daily.wine_l),
            (vessel.provisions.biscuit_kg, daily.biscuit_kg),
            (vessel.provisions.meat_kg, daily.meat_kg),
        ):
            if need > 0:
                ratios.append(stock / need)
        return min(ratios) if ratios else 0.0

    def load_research_scenario(
        self,
        fleet: FleetState | None = None,
        own_days: float = 60.0,
        fleet_reserve_days: float = 30.0,
    ) -> FleetState:
        """Carrega o smoke de pesquisa sem afirmar que reproduz a estiva de 1497."""

        fleet = fleet or self.base_gama_1497()
        reserve = self.provision_for(fleet.persons, fleet_reserve_days)
        loaded = []
        for vessel in fleet.vessels:
            load = self.provision_for(vessel.persons, own_days)
            if vessel.vessel_id == self.SUPPLY_VESSEL_ID:
                load = load.plus(reserve)
            loaded.append(replace(vessel, provisions=load))
        return FleetState(tuple(loaded))

    @staticmethod
    def transfer_provisions(
        fleet: FleetState,
        source_id: str,
        destination_id: str,
        load: ProvisionLoad,
    ) -> FleetState:
        if source_id == destination_id:
            raise ValueError("source and destination must differ")
        source = fleet.vessel(source_id)
        destination = fleet.vessel(destination_id)
        before = fleet.provisions

        source_after = replace(source, provisions=source.provisions.minus(load))
        destination_after = replace(destination, provisions=destination.provisions.plus(load))
        vessels = tuple(
            source_after
            if vessel.vessel_id == source_id
            else destination_after
            if vessel.vessel_id == destination_id
            else vessel
            for vessel in fleet.vessels
        )
        result = FleetState(vessels)
        after = result.provisions
        if not all(
            isclose(a, b, rel_tol=0.0, abs_tol=1e-7)
            for a, b in (
                (before.water_l, after.water_l),
                (before.wine_l, after.wine_l),
                (before.biscuit_kg, after.biscuit_kg),
                (before.meat_kg, after.meat_kg),
            )
        ):
            raise AssertionError("provision transfer must conserve resources")
        return result
