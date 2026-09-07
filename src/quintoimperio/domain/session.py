"""Estado de sessão para o primeiro loop contínuo do jogo.

O módulo compõe modelos existentes. Valores monetários, capacidade, provisões,
desgaste, preços e custos de tempo de interações continuam índices de
simulação. Overrides com prefixo ``scenario_`` existem para testes/demonstrações
e não definem por si só o estado histórico da campanha.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date
from pathlib import Path

from quintoimperio.data.loader import RepositoryData

from .access import AccessModel, AccessStatus, AccessView
from .calendar import GameClock
from .expedition import ExpeditionModel
from .information import InformationChannel, InformationModel, InformationOpportunity
from .knowledge import KnowledgeLevel, KnowledgeModel, KnowledgeState
from .port import PortServiceKind, PortServiceModel, PortServiceQuote, PortServiceResult
from .relationship import HistoricalActor, RelationshipModel, RelationshipStatus
from .route_knowledge import RouteKnowledgeModel
from .stop import ChronologyMode, ExpeditionStop, ExpeditionStopModel
from .trade import CommercialState, TradeModel, TradeResult, TradeSide
from .travel import TravelModel, VesselState, VoyagePlan
from .voyage_event import VoyageEvent


@dataclass(frozen=True)
class NodeKnowledgeRecord:
    node_id: str
    state: KnowledgeState


@dataclass(frozen=True)
class RouteKnowledgeRecord:
    route_id: str
    nav: KnowledgeLevel


@dataclass(frozen=True)
class AccessRecord:
    node_id: str
    status: AccessStatus


@dataclass(frozen=True)
class RelationshipRecord:
    actor_id: str
    status: RelationshipStatus


@dataclass(frozen=True)
class MarketEntry:
    good_id: str
    buy_price_index: float
    sell_price_index: float
    bulk_per_unit: float
    restricted: bool = False


@dataclass(frozen=True)
class MarketView:
    node_id: str
    knowledge_level: KnowledgeLevel
    access_status: AccessStatus
    actionable: bool
    entries: tuple[MarketEntry, ...]


@dataclass(frozen=True)
class GameSessionState:
    vessel: VesselState
    commerce: CommercialState
    node_knowledge: tuple[NodeKnowledgeRecord, ...]
    route_knowledge: tuple[RouteKnowledgeRecord, ...]
    access_records: tuple[AccessRecord, ...] = ()
    relationship_records: tuple[RelationshipRecord, ...] = ()
    active_expedition_id: str | None = None
    expedition_leg_sequence: int | None = None
    chronology_mode: ChronologyMode = ChronologyMode.COUNTERFACTUAL
    active_stop_id: str | None = None
    information_history: tuple[str, ...] = ()
    voyage_event_history: tuple[VoyageEvent, ...] = ()
    expedition_action_history: tuple[str, ...] = ()


@dataclass(frozen=True)
class SessionTradeResult:
    executed: bool
    reasons: tuple[str, ...]
    state_before: GameSessionState
    state_after: GameSessionState
    trade_result: TradeResult | None


@dataclass(frozen=True)
class SessionPortServiceResult:
    executed: bool
    reasons: tuple[str, ...]
    state_before: GameSessionState
    state_after: GameSessionState
    service_result: PortServiceResult


@dataclass(frozen=True)
class SessionWaitResult:
    executed: bool
    reasons: tuple[str, ...]
    days_waited: int
    state_before: GameSessionState
    state_after: GameSessionState


@dataclass(frozen=True)
class SessionInformationResult:
    executed: bool
    reasons: tuple[str, ...]
    state_before: GameSessionState
    state_after: GameSessionState
    opportunity: InformationOpportunity | None


@dataclass(frozen=True)
class SessionAccessResult:
    executed: bool
    reasons: tuple[str, ...]
    days_spent: int
    state_before: GameSessionState
    state_after: GameSessionState
    view_before: AccessView
    view_after: AccessView


class GameSessionModel:
    """Compõe conhecimento, acesso, relações, informação, comércio e viagem."""

    def __init__(self, root: Path | None = None) -> None:
        repository = RepositoryData(root)
        self.root = repository.root
        self.knowledge = KnowledgeModel(self.root)
        self.route_knowledge_model = RouteKnowledgeModel(self.root)
        self.access = AccessModel(self.root)
        self.relationship = RelationshipModel(self.root)
        self.information = InformationModel(self.root)
        self.expedition = ExpeditionModel(self.root)
        self.stops = ExpeditionStopModel(self.root)
        self.trade = TradeModel(self.root)
        self.port = PortServiceModel(self.root)
        self.travel = TravelModel(self.root)
        self.routes = self.travel.routes
        self.rules = {
            (row["rule_type"], row["key"]): int(row["value"])
            for row in repository.simulation("session_rules.csv")
        }

    def initial_state(
        self,
        *,
        location_node: str = "LIS",
        start_date: date = date(1497, 7, 8),
        provision_days: float = 60.0,
        condition: float = 100.0,
        capital_index: float = 100.0,
        capacity_total: float = 30.0,
        active_expedition_id: str | None = None,
        expedition_leg_sequence: int | None = None,
        chronology_mode: ChronologyMode | str | None = None,
    ) -> GameSessionState:
        if active_expedition_id is not None:
            if active_expedition_id not in self.expedition.expeditions:
                raise KeyError(f"Expedicao desconhecida: {active_expedition_id}")
            if expedition_leg_sequence is None:
                expedition_leg_sequence = self.expedition.first_sequence(active_expedition_id)
            if self.expedition.leg(active_expedition_id, expedition_leg_sequence) is None:
                raise KeyError(
                    f"Perna inexistente: {active_expedition_id}/{expedition_leg_sequence}"
                )
        elif expedition_leg_sequence is not None:
            raise ValueError("expedition_leg_sequence exige active_expedition_id")

        chronology = (
            ChronologyMode(chronology_mode)
            if chronology_mode is not None
            else (
                ChronologyMode.GUIDED
                if active_expedition_id is not None
                else ChronologyMode.COUNTERFACTUAL
            )
        )
        return GameSessionState(
            vessel=VesselState(
                location_node=location_node,
                clock=GameClock(start_date),
                provision_days=provision_days,
                condition=condition,
            ),
            commerce=CommercialState(
                capital_index=capital_index,
                capacity_total=capacity_total,
                cargo=(),
            ),
            node_knowledge=tuple(
                NodeKnowledgeRecord(node_id=node_id, state=state)
                for node_id, state in sorted(self.knowledge.player_state.items())
            ),
            route_knowledge=tuple(
                RouteKnowledgeRecord(route_id=route_id, nav=level)
                for route_id, level in sorted(self.route_knowledge_model.player_default.items())
            ),
            access_records=tuple(
                AccessRecord(node_id=node_id, status=self.access.initial_status(node_id))
                for node_id in sorted(self.access.node_regime)
            ),
            relationship_records=tuple(
                RelationshipRecord(actor_id=actor_id, status=RelationshipStatus.UNESTABLISHED)
                for actor_id in sorted(self.relationship.actors)
            ),
            active_expedition_id=active_expedition_id,
            expedition_leg_sequence=expedition_leg_sequence,
            chronology_mode=chronology,
            active_stop_id=None,
            information_history=(),
            voyage_event_history=(),
            expedition_action_history=(),
        )

    # Os métodos abaixo permanecem inalterados; a nova coleção é carregada e
    # propagada automaticamente por ``dataclasses.replace`` nas transições.
