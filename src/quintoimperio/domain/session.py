"""Estado de sessão para o primeiro loop contínuo do jogo.

O módulo apenas compõe modelos já existentes. Valores monetários, capacidade,
provisões, desgaste e preços continuam índices de simulação. Overrides com
prefixo ``scenario_`` existem para testes/demonstrações técnicas e não definem
o estado histórico inicial da campanha.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

from quintoimperio.data.loader import RepositoryData

from .calendar import GameClock
from .knowledge import KnowledgeLevel, KnowledgeModel, KnowledgeState
from .port import PortServiceKind, PortServiceModel, PortServiceQuote, PortServiceResult
from .route_knowledge import RouteKnowledgeModel
from .trade import CommercialState, TradeModel, TradeResult, TradeSide
from .travel import TravelModel, VesselState, VoyagePlan


@dataclass(frozen=True)
class NodeKnowledgeRecord:
    node_id: str
    state: KnowledgeState


@dataclass(frozen=True)
class RouteKnowledgeRecord:
    route_id: str
    nav: KnowledgeLevel


@dataclass(frozen=True)
class MarketEntry:
    good_id: str
    buy_price_index: float
    sell_price_index: float
    bulk_per_unit: float


@dataclass(frozen=True)
class MarketView:
    node_id: str
    knowledge_level: KnowledgeLevel
    actionable: bool
    entries: tuple[MarketEntry, ...]


@dataclass(frozen=True)
class GameSessionState:
    vessel: VesselState
    commerce: CommercialState
    node_knowledge: tuple[NodeKnowledgeRecord, ...]
    route_knowledge: tuple[RouteKnowledgeRecord, ...]


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


class GameSessionModel:
    """Compõe conhecimento, comércio, serviços portuários e viagem."""

    def __init__(self, root: Path | None = None) -> None:
        repository = RepositoryData(root)
        self.root = repository.root
        self.knowledge = KnowledgeModel(self.root)
        self.route_knowledge_model = RouteKnowledgeModel(self.root)
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
    ) -> GameSessionState:
        node_records = tuple(
            NodeKnowledgeRecord(
                node_id=node_id,
                state=self.knowledge.initial_for_node(node_id, "PLAYER"),
            )
            for node_id in sorted(self.knowledge.nodes)
        )
        route_records = tuple(
            RouteKnowledgeRecord(
                route_id=route_id,
                nav=self.route_knowledge_model.initial_for_route(route_id, "PLAYER"),
            )
            for route_id in sorted(self.route_knowledge_model.routes)
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
            ),
            node_knowledge=node_records,
            route_knowledge=route_records,
        )

    @staticmethod
    def _node_map(state: GameSessionState) -> dict[str, KnowledgeState]:
        return {record.node_id: record.state for record in state.node_knowledge}

    @staticmethod
    def _route_map(state: GameSessionState) -> dict[str, KnowledgeLevel]:
        return {record.route_id: record.nav for record in state.route_knowledge}

    def node_state(self, state: GameSessionState, node_id: str) -> KnowledgeState:
        return self._node_map(state)[node_id]

    def route_nav(self, state: GameSessionState, route_id: str) -> KnowledgeLevel:
        return self._route_map(state)[route_id]

    @staticmethod
    def _replace_node_knowledge(
        state: GameSessionState, node_id: str, knowledge: KnowledgeState
    ) -> GameSessionState:
        records = [record for record in state.node_knowledge if record.node_id != node_id]
        records.append(NodeKnowledgeRecord(node_id=node_id, state=knowledge))
        records.sort(key=lambda record: record.node_id)
        return GameSessionState(
            vessel=state.vessel,
            commerce=state.commerce,
            node_knowledge=tuple(records),
            route_knowledge=state.route_knowledge,
        )

    @staticmethod
    def _replace_route_knowledge(
        state: GameSessionState, route_id: str, nav: KnowledgeLevel
    ) -> GameSessionState:
        records = [record for record in state.route_knowledge if record.route_id != route_id]
        records.append(RouteKnowledgeRecord(route_id=route_id, nav=nav))
        records.sort(key=lambda record: record.route_id)
        return GameSessionState(
            vessel=state.vessel,
            commerce=state.commerce,
            node_knowledge=state.node_knowledge,
            route_knowledge=tuple(records),
        )

    @staticmethod
    def _replace_vessel(state: GameSessionState, vessel: VesselState) -> GameSessionState:
        return GameSessionState(
            vessel=vessel,
            commerce=state.commerce,
            node_knowledge=state.node_knowledge,
            route_knowledge=state.route_knowledge,
        )

    def scenario_set_node_knowledge(
        self, state: GameSessionState, node_id: str, knowledge: KnowledgeState
    ) -> GameSessionState:
        """Override explícito para cenário técnico; não altera regras históricas."""
        return self._replace_node_knowledge(state, node_id, knowledge)

    def scenario_set_route_knowledge(
        self, state: GameSessionState, route_id: str, nav: KnowledgeLevel
    ) -> GameSessionState:
        """Override explícito para cenário técnico; não altera regras históricas."""
        return self._replace_route_knowledge(state, route_id, nav)

    def market_view(self, state: GameSessionState, seed: int = 0) -> MarketView:
        node_id = state.vessel.location_node
        knowledge = self.node_state(state, node_id).market
        if knowledge < KnowledgeLevel.OPERATIONAL:
            return MarketView(
                node_id=node_id,
                knowledge_level=knowledge,
                actionable=False,
                entries=(),
            )

        year = state.vessel.clock.current_date.year
        entries: list[MarketEntry] = []
        for good_id in sorted(self.trade.economy.goods):
            buy = self.trade.quote(node_id, good_id, TradeSide.BUY, year=year, seed=seed)
            if buy is None:
                continue
            sell = self.trade.quote(node_id, good_id, TradeSide.SELL, year=year, seed=seed)
            assert sell is not None
            entries.append(
                MarketEntry(
                    good_id=good_id,
                    buy_price_index=buy.unit_price_index,
                    sell_price_index=sell.unit_price_index,
                    bulk_per_unit=buy.bulk_per_unit,
                )
            )
        return MarketView(
            node_id=node_id,
            knowledge_level=knowledge,
            actionable=True,
            entries=tuple(entries),
        )

    def service_quote(
        self, state: GameSessionState, service: PortServiceKind
    ) -> PortServiceQuote:
        return self.port.quote(state.vessel.location_node, service)

    def reprovision(
        self, state: GameSessionState, requested_days: float
    ) -> SessionPortServiceResult:
        result = self.port.reprovision(
            state.vessel, state.vessel.location_node, requested_days
        )
        after = self._replace_vessel(state, result.state_after)
        return SessionPortServiceResult(
            executed=result.success,
            reasons=result.blockers,
            state_before=state,
            state_after=after,
            service_result=result,
        )

    def repair(
        self, state: GameSessionState, requested_points: float
    ) -> SessionPortServiceResult:
        result = self.port.repair(
            state.vessel, state.vessel.location_node, requested_points
        )
        after = self._replace_vessel(state, result.state_after)
        return SessionPortServiceResult(
            executed=result.success,
            reasons=result.blockers,
            state_before=state,
            state_after=after,
            service_result=result,
        )

    def _blocked_trade(
        self, state: GameSessionState, reason: str
    ) -> SessionTradeResult:
        return SessionTradeResult(
            executed=False,
            reasons=(reason,),
            state_before=state,
            state_after=state,
            trade_result=None,
        )

    def buy(
        self,
        state: GameSessionState,
        good_id: str,
        quantity: float,
        *,
        seed: int = 0,
    ) -> SessionTradeResult:
        if self.node_state(state, state.vessel.location_node).market < KnowledgeLevel.OPERATIONAL:
            return self._blocked_trade(state, "MARKET_KNOWLEDGE_NOT_OPERATIONAL")
        result = self.trade.buy(
            state.commerce,
            state.vessel.location_node,
            good_id,
            quantity,
            year=state.vessel.clock.current_date.year,
            seed=seed,
        )
        after = GameSessionState(
            vessel=state.vessel,
            commerce=result.state_after,
            node_knowledge=state.node_knowledge,
            route_knowledge=state.route_knowledge,
        )
        return SessionTradeResult(
            executed=result.executed,
            reasons=result.reasons,
            state_before=state,
            state_after=after,
            trade_result=result,
        )

    def sell(
        self,
        state: GameSessionState,
        good_id: str,
        quantity: float,
        *,
        seed: int = 0,
    ) -> SessionTradeResult:
        if self.node_state(state, state.vessel.location_node).market < KnowledgeLevel.OPERATIONAL:
            return self._blocked_trade(state, "MARKET_KNOWLEDGE_NOT_OPERATIONAL")
        result = self.trade.sell(
            state.commerce,
            state.vessel.location_node,
            good_id,
            quantity,
            year=state.vessel.clock.current_date.year,
            seed=seed,
        )
        after = GameSessionState(
            vessel=state.vessel,
            commerce=result.state_after,
            node_knowledge=state.node_knowledge,
            route_knowledge=state.route_knowledge,
        )
        return SessionTradeResult(
            executed=result.executed,
            reasons=result.reasons,
            state_before=state,
            state_after=after,
            trade_result=result,
        )

    def plan_voyage(
        self,
        state: GameSessionState,
        route_id: str,
        *,
        pilot_id: str | None = None,
        seed: int = 0,
    ) -> VoyagePlan:
        return self.travel.plan_voyage(
            state.vessel,
            route_id,
            self.route_nav(state, route_id),
            pilot_id=pilot_id,
            seed=seed,
        )

    @staticmethod
    def _at_least(current: KnowledgeLevel, minimum: int) -> KnowledgeLevel:
        return KnowledgeLevel(max(int(current), minimum))

    def execute_voyage(
        self, state: GameSessionState, plan: VoyagePlan
    ) -> GameSessionState:
        vessel_after = self.travel.execute_voyage(state.vessel, plan)
        after = GameSessionState(
            vessel=vessel_after,
            commerce=state.commerce,
            node_knowledge=state.node_knowledge,
            route_knowledge=state.route_knowledge,
        )

        destination = self.node_state(after, plan.destination_node)
        learned_destination = KnowledgeState(
            geo=self._at_least(destination.geo, self.rules[("ARRIVAL", "GEO_MIN")]),
            nav=self._at_least(destination.nav, self.rules[("ARRIVAL", "NAV_MIN")]),
            market=self._at_least(
                destination.market, self.rules[("ARRIVAL", "MARKET_MIN")]
            ),
            political=self._at_least(
                destination.political, self.rules[("ARRIVAL", "POLITICAL_MIN")]
            ),
        )
        after = self._replace_node_knowledge(
            after, plan.destination_node, learned_destination
        )
        route_nav = self.route_nav(after, plan.route_id)
        learned_route = self._at_least(
            route_nav, self.rules[("ROUTE_COMPLETION", "NAV_MIN")]
        )
        return self._replace_route_knowledge(after, plan.route_id, learned_route)
