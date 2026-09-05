"""Estado de viagem, provisoes abstratas, desgaste, pilotos e comando v0.1."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum
from math import ceil
from pathlib import Path

from quintoimperio.data.loader import RepositoryData

from .calendar import GameClock
from .knowledge import KnowledgeLevel
from .navigation import NavigationModel


class NavigationBasis(str, Enum):
    """Base pela qual o personagem participa da operacao de uma rota."""

    OWN_KNOWLEDGE = "OWN_KNOWLEDGE"
    PILOT = "PILOT"
    FLEET_COMMAND = "FLEET_COMMAND"


@dataclass(frozen=True)
class VesselState:
    """Estado minimo do navio para o primeiro loop de viagem.

    ``provision_days`` usa dias-equivalentes abstratos. ``condition`` usa uma
    escala de simulacao 0-100. Nenhum dos dois campos representa uma unidade
    historica documentada.
    """

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
    route_id: str
    origin_node: str
    destination_node: str
    departure_date: date
    arrival_date: date
    estimated_duration_days: float
    travel_days: int
    provision_days_required: float
    provision_days_after: float
    condition_before: float
    condition_after: float
    pilot_id: str | None
    navigation_basis: NavigationBasis | None
    feasible: bool
    blockers: tuple[str, ...]


class TravelModel:
    """Orquestra navegacao, recursos abstratos e bases de participacao na rota.

    Pilotos historicos podem habilitar uma rota quando o conhecimento nautico
    do personagem ainda nao e operacional. Uma expedicao ativa pode fornecer a
    base institucional ``FLEET_COMMAND`` sem transformar o comando da armada em
    conhecimento pessoal do personagem. Nenhuma dessas bases concede bonus
    quantitativo de velocidade, consumo ou desgaste na v0.1.

    Rotas com ``route_origin=STRATEGIC_AGGREGATE`` existem apenas para leitura
    do grafo em escala estratégica. Elas nunca são executáveis como uma única
    perna de viagem quando a base já possui a sequência histórica segmentada.
    """

    def __init__(self, root: Path | None = None) -> None:
        repository = RepositoryData(root)
        self.root = repository.root
        self.navigation = NavigationModel(self.root)
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

    def plan_voyage(
        self,
        state: VesselState,
        route_id: str,
        nav_knowledge: KnowledgeLevel,
        pilot_id: str | None = None,
        fleet_command: bool = False,
        seed: int = 0,
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

        travel_days = max(1, ceil(duration))
        provision_rate = float(
            self.rules[("PROVISIONS", "DAY_EQUIVALENT_PER_TRAVEL_DAY")]
        )
        provisions_required = travel_days * provision_rate
        wear = travel_days * self.wear_per_day(route_id)
        condition_after = max(0.0, state.condition - wear)
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
            # Identificador preservado por compatibilidade com testes/telemetria v0.1.
            blockers.append("NAVIGATION_KNOWLEDGE_OR_PILOT_REQUIRED")
        if state.provision_days < provisions_required:
            blockers.append("INSUFFICIENT_PROVISIONS")
        min_condition = float(self.rules[("DEPARTURE", "MIN_CONDITION")])
        if state.condition < min_condition:
            blockers.append("VESSEL_CONDITION_TOO_LOW")

        arrival = state.clock.advance(travel_days).current_date
        return VoyagePlan(
            route_id=route_id,
            origin_node=route["origin_node"],
            destination_node=route["destination_node"],
            departure_date=state.clock.current_date,
            arrival_date=arrival,
            estimated_duration_days=duration,
            travel_days=travel_days,
            provision_days_required=provisions_required,
            provision_days_after=max(0.0, state.provision_days - provisions_required),
            condition_before=state.condition,
            condition_after=condition_after,
            pilot_id=pilot_id,
            navigation_basis=basis,
            feasible=not blockers,
            blockers=tuple(blockers),
        )

    def execute_voyage(self, state: VesselState, plan: VoyagePlan) -> VesselState:
        if not plan.feasible:
            raise ValueError(f"Plano de viagem bloqueado: {', '.join(plan.blockers)}")
        if state.location_node != plan.origin_node:
            raise ValueError("Estado do navio nao corresponde a origem do plano")
        if state.clock.current_date != plan.departure_date:
            raise ValueError("Data atual nao corresponde a data de partida do plano")
        if state.provision_days < plan.provision_days_required:
            raise ValueError("Provisoes atuais nao suportam o plano")

        return VesselState(
            location_node=plan.destination_node,
            clock=state.clock.advance(plan.travel_days),
            provision_days=state.provision_days - plan.provision_days_required,
            condition=plan.condition_after,
        )
