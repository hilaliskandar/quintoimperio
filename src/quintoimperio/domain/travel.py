"""Estado de viagem, provisoes abstratas, desgaste, pilotos, comando e eventos v0.3."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date
from enum import Enum
from math import ceil
from pathlib import Path

from quintoimperio.data.loader import RepositoryData

from .calendar import GameClock
from .knowledge import KnowledgeLevel
from .navigation import NavigationModel
from .voyage_event import VoyageEvent, VoyageEventModel


class NavigationBasis(str, Enum):
    """Base pela qual o personagem participa da operacao de uma rota."""

    OWN_KNOWLEDGE = "OWN_KNOWLEDGE"
    PILOT = "PILOT"
    FLEET_COMMAND = "FLEET_COMMAND"


@dataclass(frozen=True)
class VesselState:
    """Estado minimo do navio para o primeiro loop de viagem."""

    location_node: str
    clock: GameClock
    provision_days: float
    condition: float = 100.0

    def __post_init__(self) -> None:
        if self.provision_days < 0:
            raise ValueError("provision_days nao pode ser negativo")
        if not 0.0 <= self.condition <= 100.0:
            raise ValueError("condition deve permanecer entre 0 e 100")


@dataclass(frozen=True)
class VoyagePlan:
    """Plano conhecido antes da partida e, opcionalmente, resolução da viagem.

    Enquanto ``events_resolved`` for falso, os campos de duração, provisões e
    condição representam apenas o cenário-base conhecido pelo jogador. O evento
    específico só é selecionado em ``resolve_voyage``/execução.
    """

    route_id: str
    origin_node: str
    destination_node: str
    departure_date: date
    arrival_date: date
    base_estimated_duration_days: float
    estimated_duration_days: float
    travel_days: int
    provision_days_required: float
    event_provision_delta: float
    provision_days_after: float
    condition_before: float
    condition_after: float
    pilot_id: str | None
    navigation_basis: NavigationBasis | None
    events: tuple[VoyageEvent, ...]
    events_suppressed_by_observation: bool
    timing_events_suppressed_by_observation: bool
    simulation_seed: int
    events_resolved: bool
    feasible: bool
    blockers: tuple[str, ...]


class TravelModel:
    """Orquestra navegação, recursos abstratos, bases de viagem e eventos.

    A v0.3 separa previsão e resolução. ``plan_voyage`` nunca revela o evento
    específico: calcula apenas duração/consumo/desgaste-base e os bloqueios já
    conhecidos na partida. ``resolve_voyage`` usa a seed armazenada no plano e
    aplica a contingência somente quando a viagem é executada.

    Em cronologia observada, ``timing_events_suppressed_by_observation`` restringe
    a resolução a eventos ``observed_timing_safe``. Assim, a data histórica pode
    ser preservada sem eliminar a incerteza de recursos.
    """

    def __init__(self, root: Path | None = None) -> None:
        repository = RepositoryData(root)
        self.root = repository.root
        self.navigation = NavigationModel(self.root)
        self.events = VoyageEventModel(self.root)
        self.routes = self.navigation.routes
        self.pilots = {
            row["pilot_id"]: row for row in repository.historical("pilots.csv")
        }
        self.pilot_routes = repository.historical("pilot_routes.csv")
        self.rules: dict[tuple[str, str], str] = {}
        for row in repository.simulation("travel_rules.csv"):
            self.rules[(row["rule_type"], row["key"])] = row["value"]

    @staticmethod
    def _active(row: dict[str, str], on_date: date) -> bool:
        start = row.get("period_from", "")
        end = row.get("period_to", "")
        if start and on_date.year < int(start):
            return False
        if end and on_date.year > int(end):
            return False
        return True

    def pilot_can_guide(
        self, pilot_id: str, route_id: str, on_date: date, origin_node: str
    ) -> bool:
        pilot = self.pilots.get(pilot_id)
        if pilot is None or not self._active(pilot, on_date):
            return False
        if pilot["available_node"] != origin_node:
            return False
        return any(
            row["pilot_id"] == pilot_id
            and row["route_id"] == route_id
            and row["competence"] == "CONFIRMED"
            and self._active(row, on_date)
            for row in self.pilot_routes
        )

    def navigation_basis(
        self,
        route_id: str,
        nav_knowledge: KnowledgeLevel,
        on_date: date,
        origin_node: str,
        pilot_id: str | None = None,
        fleet_command: bool = False,
    ) -> NavigationBasis | None:
        if nav_knowledge >= KnowledgeLevel.OPERATIONAL:
            return NavigationBasis.OWN_KNOWLEDGE
        if pilot_id and self.pilot_can_guide(pilot_id, route_id, on_date, origin_node):
            return NavigationBasis.PILOT
        if fleet_command:
            return NavigationBasis.FLEET_COMMAND
        return None

    def wear_per_day(self, route_id: str) -> float:
        route_type = self.routes[route_id]["route_type"]
        key = f"{route_type}_PER_DAY"
        raw = self.rules.get(("WEAR", key))
        if raw is None:
            raw = self.rules[("WEAR", "DEFAULT_PER_DAY")]
        return float(raw)

    def _validate_state_for_plan(self, state: VesselState, plan: VoyagePlan) -> None:
        if state.location_node != plan.origin_node:
            raise ValueError("Estado do navio nao corresponde a origem do plano")
        if state.clock.current_date != plan.departure_date:
            raise ValueError("Data atual nao corresponde a data de partida do plano")

    def plan_voyage(
        self,
        state: VesselState,
        route_id: str,
        nav_knowledge: KnowledgeLevel,
        pilot_id: str | None = None,
        fleet_command: bool = False,
        seed: int = 0,
        preserve_observed_timing: bool = True,
    ) -> VoyagePlan:
        route = self.routes[route_id]
        if state.location_node != route["origin_node"]:
            raise ValueError(
                f"Navio esta em {state.location_node}, mas {route_id} parte de {route['origin_node']}"
            )

        duration = self.navigation.estimate_duration_days(
            route_id, state.clock.current_date, seed=seed
        )
        if duration is None:
            raise ValueError(
                f"Rota {route_id} nao possui coordenadas suficientes para estimar duracao"
            )

        exact_observation = bool(
            self.navigation.observed_days_for_departure(route_id, state.clock.current_date)
        )
        suppress_timing_events = preserve_observed_timing and exact_observation
        base_travel_days = max(1, ceil(duration))
        provision_rate = float(
            self.rules[("PROVISIONS", "DAY_EQUIVALENT_PER_TRAVEL_DAY")]
        )
        provisions_required = base_travel_days * provision_rate
        normal_wear = base_travel_days * self.wear_per_day(route_id)
        condition_after = max(0.0, state.condition - normal_wear)
        basis = self.navigation_basis(
            route_id,
            nav_knowledge,
            state.clock.current_date,
            state.location_node,
            pilot_id,
            fleet_command,
        )

        blockers: list[str] = []
        if route.get("route_origin") == "STRATEGIC_AGGREGATE":
            blockers.append("STRATEGIC_AGGREGATE_NOT_EXECUTABLE")
        if basis is None:
            blockers.append("NAVIGATION_KNOWLEDGE_OR_PILOT_REQUIRED")
        if state.provision_days < provisions_required:
            blockers.append("INSUFFICIENT_PROVISIONS")
        min_condition = float(self.rules[("DEPARTURE", "MIN_CONDITION")])
        if state.condition < min_condition:
            blockers.append("VESSEL_CONDITION_TOO_LOW")

        return VoyagePlan(
            route_id=route_id,
            origin_node=route["origin_node"],
            destination_node=route["destination_node"],
            departure_date=state.clock.current_date,
            arrival_date=state.clock.advance(base_travel_days).current_date,
            base_estimated_duration_days=duration,
            estimated_duration_days=duration,
            travel_days=base_travel_days,
            provision_days_required=provisions_required,
            event_provision_delta=0.0,
            provision_days_after=max(0.0, state.provision_days - provisions_required),
            condition_before=state.condition,
            condition_after=condition_after,
            pilot_id=pilot_id,
            navigation_basis=basis,
            events=(),
            events_suppressed_by_observation=False,
            timing_events_suppressed_by_observation=suppress_timing_events,
            simulation_seed=int(seed),
            events_resolved=False,
            feasible=not blockers,
            blockers=tuple(blockers),
        )

    def resolve_voyage(self, state: VesselState, plan: VoyagePlan) -> VoyagePlan:
        """Resolve a contingência sem retroagir ao conhecimento pré-partida."""
        if not plan.feasible:
            raise ValueError(f"Plano de viagem bloqueado: {', '.join(plan.blockers)}")
        self._validate_state_for_plan(state, plan)
        if plan.events_resolved:
            return plan

        events = self.events.select(
            plan.route_id,
            plan.departure_date,
            seed=plan.simulation_seed,
            timing_safe_only=plan.timing_events_suppressed_by_observation,
        )
        extra_days = sum(event.extra_days for event in events)
        event_condition_loss = sum(event.condition_loss for event in events)
        event_provision_delta = sum(event.provision_delta for event in events)
        base_travel_days = max(1, ceil(plan.base_estimated_duration_days))
        travel_days = base_travel_days + extra_days
        provision_rate = float(
            self.rules[("PROVISIONS", "DAY_EQUIVALENT_PER_TRAVEL_DAY")]
        )
        provisions_required = travel_days * provision_rate
        provision_days_after_raw = (
            state.provision_days - provisions_required + event_provision_delta
        )
        normal_wear = base_travel_days * self.wear_per_day(plan.route_id)
        condition_after = max(
            0.0, state.condition - normal_wear - event_condition_loss
        )
        return replace(
            plan,
            arrival_date=state.clock.advance(travel_days).current_date,
            estimated_duration_days=plan.base_estimated_duration_days + extra_days,
            travel_days=travel_days,
            provision_days_required=provisions_required,
            event_provision_delta=event_provision_delta,
            provision_days_after=max(0.0, provision_days_after_raw),
            condition_after=condition_after,
            events=events,
            events_suppressed_by_observation=(
                plan.timing_events_suppressed_by_observation and not events
            ),
            events_resolved=True,
        )

    def execute_voyage(self, state: VesselState, plan: VoyagePlan) -> VesselState:
        """Executa plano; resolução tardia é aplicada se ainda não ocorreu."""
        resolved = self.resolve_voyage(state, plan)
        return VesselState(
            location_node=resolved.destination_node,
            clock=state.clock.advance(resolved.travel_days),
            provision_days=resolved.provision_days_after,
            condition=resolved.condition_after,
        )
