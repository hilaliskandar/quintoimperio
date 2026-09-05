"""Serviços portuários mínimos baseados em disponibilidade documentada."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import ceil
from pathlib import Path

from quintoimperio.data.loader import RepositoryData

from .travel import VesselState


class PortServiceKind(str, Enum):
    PROVISIONS = "PROVISIONS"
    REPAIR = "REPAIR"


class ServiceAvailability(str, Enum):
    UNKNOWN = "UNKNOWN"
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

    @classmethod
    def from_historical_field(cls, value: str | None) -> "ServiceAvailability":
        if value is None or value == "":
            return cls.UNKNOWN
        return cls(value)


@dataclass(frozen=True)
class PortServiceQuote:
    node_id: str
    service: PortServiceKind
    availability: ServiceAvailability
    documented: bool
    actionable: bool
    capacity_or_rate: float | None
    unit: str | None


@dataclass(frozen=True)
class PortServiceResult:
    node_id: str
    service: PortServiceKind
    success: bool
    state_before: VesselState
    state_after: VesselState
    effect: float
    days_spent: int
    blockers: tuple[str, ...]


class PortServiceModel:
    """Converte categorias históricas de serviço em ações abstratas de jogo.

    Os campos ``provisions`` e ``repair`` em ``nodes.csv`` descrevem a base
    histórica disponível. Campo vazio significa desconhecido, e não ausência.
    A conversão LOW/MEDIUM/HIGH para capacidade, duração ou taxa está somente em
    ``simulation/port_rules.csv`` e não deve ser interpretada como medida
    histórica.
    """

    NODE_FIELDS = {
        PortServiceKind.PROVISIONS: "provisions",
        PortServiceKind.REPAIR: "repair",
    }

    def __init__(self, root: Path | None = None) -> None:
        repository = RepositoryData(root)
        self.root = repository.root
        self.nodes = {
            row["node_id"]: row for row in repository.historical("nodes.csv")
        }
        self.rules: dict[tuple[str, str], float] = {}
        for row in repository.simulation("port_rules.csv"):
            self.rules[(row["rule_type"], row["key"])] = float(row["value"])

    def availability(
        self, node_id: str, service: PortServiceKind
    ) -> ServiceAvailability:
        node = self.nodes[node_id]
        field = self.NODE_FIELDS[service]
        return ServiceAvailability.from_historical_field(node.get(field))

    def quote(self, node_id: str, service: PortServiceKind) -> PortServiceQuote:
        availability = self.availability(node_id, service)
        if availability == ServiceAvailability.UNKNOWN:
            return PortServiceQuote(
                node_id=node_id,
                service=service,
                availability=availability,
                documented=False,
                actionable=False,
                capacity_or_rate=None,
                unit=None,
            )
        if availability == ServiceAvailability.NONE:
            return PortServiceQuote(
                node_id=node_id,
                service=service,
                availability=availability,
                documented=True,
                actionable=False,
                capacity_or_rate=0.0,
                unit=None,
            )

        if service == PortServiceKind.PROVISIONS:
            value = self.rules[("PROVISION_CAPACITY_PER_VISIT", availability.value)]
            unit = "provision_days_per_action"
        else:
            value = self.rules[("REPAIR_POINTS_PER_DAY", availability.value)]
            unit = "condition_points_per_day"

        return PortServiceQuote(
            node_id=node_id,
            service=service,
            availability=availability,
            documented=True,
            actionable=True,
            capacity_or_rate=value,
            unit=unit,
        )

    @staticmethod
    def _location_blocker(state: VesselState, node_id: str) -> tuple[str, ...]:
        if state.location_node != node_id:
            return ("VESSEL_NOT_AT_PORT",)
        return ()

    def _availability_blockers(
        self, node_id: str, service: PortServiceKind
    ) -> tuple[str, ...]:
        availability = self.availability(node_id, service)
        if availability == ServiceAvailability.UNKNOWN:
            return ("SERVICE_AVAILABILITY_UNKNOWN",)
        if availability == ServiceAvailability.NONE:
            return ("SERVICE_UNAVAILABLE",)
        return ()

    def reprovision(
        self, state: VesselState, node_id: str, requested_days: float
    ) -> PortServiceResult:
        if requested_days <= 0:
            raise ValueError("requested_days deve ser positivo")

        blockers = list(self._location_blocker(state, node_id))
        blockers.extend(self._availability_blockers(node_id, PortServiceKind.PROVISIONS))
        if blockers:
            return PortServiceResult(
                node_id=node_id,
                service=PortServiceKind.PROVISIONS,
                success=False,
                state_before=state,
                state_after=state,
                effect=0.0,
                days_spent=0,
                blockers=tuple(blockers),
            )

        availability = self.availability(node_id, PortServiceKind.PROVISIONS)
        capacity = self.rules[("PROVISION_CAPACITY_PER_VISIT", availability.value)]
        max_onboard = self.rules[("PROVISION_MAX_ONBOARD", "DEFAULT")]
        remaining_capacity = max(0.0, max_onboard - state.provision_days)
        added = min(requested_days, capacity, remaining_capacity)
        if added <= 0:
            return PortServiceResult(
                node_id=node_id,
                service=PortServiceKind.PROVISIONS,
                success=False,
                state_before=state,
                state_after=state,
                effect=0.0,
                days_spent=0,
                blockers=("ONBOARD_PROVISION_CAP_REACHED",),
            )

        service_days = int(self.rules[("PROVISION_SERVICE_DAYS", "DEFAULT")])
        after = VesselState(
            location_node=state.location_node,
            clock=state.clock.advance(service_days),
            provision_days=state.provision_days + added,
            condition=state.condition,
        )
        return PortServiceResult(
            node_id=node_id,
            service=PortServiceKind.PROVISIONS,
            success=True,
            state_before=state,
            state_after=after,
            effect=added,
            days_spent=service_days,
            blockers=(),
        )

    def repair(
        self, state: VesselState, node_id: str, requested_points: float
    ) -> PortServiceResult:
        if requested_points <= 0:
            raise ValueError("requested_points deve ser positivo")

        blockers = list(self._location_blocker(state, node_id))
        blockers.extend(self._availability_blockers(node_id, PortServiceKind.REPAIR))
        if blockers:
            return PortServiceResult(
                node_id=node_id,
                service=PortServiceKind.REPAIR,
                success=False,
                state_before=state,
                state_after=state,
                effect=0.0,
                days_spent=0,
                blockers=tuple(blockers),
            )

        missing = max(0.0, 100.0 - state.condition)
        if missing <= 0:
            return PortServiceResult(
                node_id=node_id,
                service=PortServiceKind.REPAIR,
                success=False,
                state_before=state,
                state_after=state,
                effect=0.0,
                days_spent=0,
                blockers=("VESSEL_ALREADY_FULL_CONDITION",),
            )

        availability = self.availability(node_id, PortServiceKind.REPAIR)
        rate = self.rules[("REPAIR_POINTS_PER_DAY", availability.value)]
        max_days = int(self.rules[("REPAIR_MAX_DAYS_PER_ACTION", "DEFAULT")])
        max_effect = rate * max_days
        restored = min(requested_points, missing, max_effect)
        service_days = max(1, ceil(restored / rate))

        after = VesselState(
            location_node=state.location_node,
            clock=state.clock.advance(service_days),
            provision_days=state.provision_days,
            condition=min(100.0, state.condition + restored),
        )
        return PortServiceResult(
            node_id=node_id,
            service=PortServiceKind.REPAIR,
            success=True,
            state_before=state,
            state_after=after,
            effect=restored,
            days_spent=service_days,
            blockers=(),
        )
