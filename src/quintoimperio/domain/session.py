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
    active_expedition_id: str | None = None
    expedition_leg_sequence: int | None = None
    chronology_mode: ChronologyMode = ChronologyMode.COUNTERFACTUAL
    active_stop_id: str | None = None
    information_history: tuple[str, ...] = ()
    voyage_event_history: tuple[VoyageEvent, ...] = ()


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
    """Compõe conhecimento, acesso, informação, comércio, serviços e viagem."""

    def __init__(self, root: Path | None = None) -> None:
        repository = RepositoryData(root)
        self.root = repository.root
        self.knowledge = KnowledgeModel(self.root)
        self.route_knowledge_model = RouteKnowledgeModel(self.root)
        self.access = AccessModel(self.root)
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

        if chronology_mode is None:
            chronology = (
                ChronologyMode.GUIDED
                if active_expedition_id is not None
                else ChronologyMode.COUNTERFACTUAL
            )
        elif isinstance(chronology_mode, ChronologyMode):
            chronology = chronology_mode
        else:
            chronology = ChronologyMode(chronology_mode)

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
        access_records = tuple(
            AccessRecord(node_id=node_id, status=self.access.initial_status(node_id))
            for node_id in sorted(self.access.nodes)
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
            access_records=access_records,
            active_expedition_id=active_expedition_id,
            expedition_leg_sequence=expedition_leg_sequence,
            chronology_mode=chronology,
        )

    @staticmethod
    def _node_map(state: GameSessionState) -> dict[str, KnowledgeState]:
        return {record.node_id: record.state for record in state.node_knowledge}

    @staticmethod
    def _route_map(state: GameSessionState) -> dict[str, KnowledgeLevel]:
        return {record.route_id: record.nav for record in state.route_knowledge}

    @staticmethod
    def _access_map(state: GameSessionState) -> dict[str, AccessStatus]:
        return {record.node_id: record.status for record in state.access_records}

    def node_state(self, state: GameSessionState, node_id: str) -> KnowledgeState:
        return self._node_map(state)[node_id]

    def route_nav(self, state: GameSessionState, route_id: str) -> KnowledgeLevel:
        return self._route_map(state)[route_id]

    def access_status(self, state: GameSessionState, node_id: str) -> AccessStatus:
        return self._access_map(state).get(node_id, self.access.initial_status(node_id))

    def access_view(self, state: GameSessionState, node_id: str | None = None) -> AccessView:
        target = node_id or state.vessel.location_node
        return self.access.view(target, self.access_status(state, target))

    def active_stop(self, state: GameSessionState) -> ExpeditionStop | None:
        return self.stops.stop(state.active_stop_id)

    @staticmethod
    def _replace_node_knowledge(
        state: GameSessionState, node_id: str, knowledge: KnowledgeState
    ) -> GameSessionState:
        records = [record for record in state.node_knowledge if record.node_id != node_id]
        records.append(NodeKnowledgeRecord(node_id=node_id, state=knowledge))
        records.sort(key=lambda record: record.node_id)
        return replace(state, node_knowledge=tuple(records))

    @staticmethod
    def _replace_route_knowledge(
        state: GameSessionState, route_id: str, nav: KnowledgeLevel
    ) -> GameSessionState:
        records = [record for record in state.route_knowledge if record.route_id != route_id]
        records.append(RouteKnowledgeRecord(route_id=route_id, nav=nav))
        records.sort(key=lambda record: record.route_id)
        return replace(state, route_knowledge=tuple(records))

    @staticmethod
    def _replace_access(
        state: GameSessionState, node_id: str, status: AccessStatus
    ) -> GameSessionState:
        records = [record for record in state.access_records if record.node_id != node_id]
        records.append(AccessRecord(node_id=node_id, status=status))
        records.sort(key=lambda record: record.node_id)
        return replace(state, access_records=tuple(records))

    @staticmethod
    def _replace_vessel(state: GameSessionState, vessel: VesselState) -> GameSessionState:
        return replace(state, vessel=vessel)

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

    def scenario_set_access(
        self, state: GameSessionState, node_id: str, status: AccessStatus | str
    ) -> GameSessionState:
        """Override técnico explícito; não representa autorização histórica."""
        return self._replace_access(state, node_id, AccessStatus(status))

    @staticmethod
    def _at_least(current: KnowledgeLevel, minimum: int | KnowledgeLevel) -> KnowledgeLevel:
        return KnowledgeLevel(max(int(current), int(minimum)))

    def negotiate_access(self, state: GameSessionState) -> SessionAccessResult:
        """Satisfaz o gate institucional genérico sem inventar taxa ou presente."""
        node_id = state.vessel.location_node
        before_view = self.access_view(state, node_id)
        if not before_view.negotiable:
            return SessionAccessResult(
                executed=False,
                reasons=("ACCESS_NEGOTIATION_NOT_AVAILABLE",),
                days_spent=0,
                state_before=state,
                state_after=state,
                view_before=before_view,
                view_after=before_view,
            )
        new_status = self.access.negotiate(node_id, before_view.status)
        after = self._replace_access(state, node_id, new_status)
        if before_view.time_days:
            after = self._replace_vessel(
                after,
                replace(
                    after.vessel,
                    clock=after.vessel.clock.advance(before_view.time_days),
                ),
            )
        after_view = self.access_view(after, node_id)
        return SessionAccessResult(
            executed=True,
            reasons=(),
            days_spent=before_view.time_days,
            state_before=state,
            state_after=after,
            view_before=before_view,
            view_after=after_view,
        )

    def _information_would_improve(
        self, state: GameSessionState, opportunity: InformationOpportunity
    ) -> bool:
        node = self.node_state(state, opportunity.target_node_id)
        route = self.route_nav(state, opportunity.target_route_id)
        return any(
            (
                node.geo < opportunity.geo_min,
                node.market < opportunity.market_min,
                node.political < opportunity.political_min,
                route < opportunity.route_nav_min,
            )
        )

    def information_opportunities(
        self,
        state: GameSessionState,
        channel: InformationChannel | str | None = None,
    ) -> tuple[InformationOpportunity, ...]:
        """Lista somente interações que podem acrescentar conhecimento pessoal.

        Esta operação não consulta a perspectiva ``CROWN``. O alvo decorre da
        conectividade documentada a partir do nó atual.
        """
        parsed = None if channel is None else InformationChannel(channel)
        structural = self.information.opportunities(
            state.vessel.location_node,
            state.vessel.clock.current_date,
            channel=parsed,
            used_ids=state.information_history,
        )
        return tuple(
            item for item in structural if self._information_would_improve(state, item)
        )

    def acquire_information(
        self,
        state: GameSessionState,
        channel: InformationChannel | str,
        *,
        seed: int = 0,
    ) -> SessionInformationResult:
        """Executa uma interação genérica e melhora apenas o estado PLAYER."""
        parsed = InformationChannel(channel)
        opportunities = self.information_opportunities(state, parsed)
        chosen = self.information.choose(
            opportunities,
            seed=seed,
            node_id=state.vessel.location_node,
            on_date=state.vessel.clock.current_date,
            channel=parsed,
        )
        if chosen is None:
            return SessionInformationResult(
                executed=False,
                reasons=("NO_INFORMATION_OPPORTUNITY",),
                state_before=state,
                state_after=state,
                opportunity=None,
            )

        target = self.node_state(state, chosen.target_node_id)
        learned_node = KnowledgeState(
            geo=self._at_least(target.geo, chosen.geo_min),
            nav=target.nav,
            market=self._at_least(target.market, chosen.market_min),
            political=self._at_least(target.political, chosen.political_min),
        )
        after = self._replace_node_knowledge(state, chosen.target_node_id, learned_node)
        learned_route = self._at_least(
            self.route_nav(after, chosen.target_route_id), chosen.route_nav_min
        )
        after = self._replace_route_knowledge(after, chosen.target_route_id, learned_route)
        vessel = replace(
            after.vessel,
            clock=after.vessel.clock.advance(chosen.time_days),
        )
        after = replace(
            after,
            vessel=vessel,
            information_history=(*after.information_history, chosen.opportunity_id),
        )
        return SessionInformationResult(
            executed=True,
            reasons=(),
            state_before=state,
            state_after=after,
            opportunity=chosen,
        )

    def market_view(self, state: GameSessionState, seed: int = 0) -> MarketView:
        node_id = state.vessel.location_node
        knowledge = self.node_state(state, node_id).market
        access = self.access_view(state, node_id)
        if knowledge < KnowledgeLevel.OPERATIONAL:
            return MarketView(
                node_id=node_id,
                knowledge_level=knowledge,
                access_status=access.status,
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
                    restricted=self.trade.good_restricted(node_id, good_id, year),
                )
            )
        return MarketView(
            node_id=node_id,
            knowledge_level=knowledge,
            access_status=access.status,
            actionable=access.commercial_access,
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

    def wait_for_stop_release(self, state: GameSessionState) -> SessionWaitResult:
        """Avança somente o relógio até a partida documentada da escala ativa.

        Esperar não concede provisões, reparos, mercadorias ou qualquer outro
        efeito material. Esses efeitos continuam exigindo ações explícitas dos
        respectivos modelos.
        """
        stop = self.active_stop(state)
        if stop is None:
            return SessionWaitResult(
                executed=False,
                reasons=("NO_ACTIVE_EXPEDITION_STOP",),
                days_waited=0,
                state_before=state,
                state_after=state,
            )
        if state.chronology_mode is not ChronologyMode.GUIDED:
            return SessionWaitResult(
                executed=False,
                reasons=("COUNTERFACTUAL_CHRONOLOGY_NO_FORCED_WAIT",),
                days_waited=0,
                state_before=state,
                state_after=state,
            )
        days = self.stops.days_until_release(stop, state.vessel.clock.current_date)
        if days == 0:
            return SessionWaitResult(
                executed=False,
                reasons=("STOP_RELEASE_ALREADY_REACHED",),
                days_waited=0,
                state_before=state,
                state_after=state,
            )
        vessel = replace(state.vessel, clock=state.vessel.clock.advance(days))
        after = self._replace_vessel(state, vessel)
        return SessionWaitResult(
            executed=True,
            reasons=(),
            days_waited=days,
            state_before=state,
            state_after=after,
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

    @staticmethod
    def _access_block_reason(status: AccessStatus) -> str:
        return {
            AccessStatus.NEGOTIATION_REQUIRED: "PORT_ACCESS_NEGOTIATION_REQUIRED",
            AccessStatus.RESTRICTED: "PORT_ACCESS_RESTRICTED",
            AccessStatus.NONCOMMERCIAL: "PORT_HAS_NO_COMMERCIAL_ACCESS",
            AccessStatus.UNKNOWN: "PORT_ACCESS_UNKNOWN",
        }.get(status, "PORT_ACCESS_NOT_GRANTED")

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
        access = self.access_view(state)
        if not access.commercial_access:
            return self._blocked_trade(state, self._access_block_reason(access.status))
        result = self.trade.buy(
            state.commerce,
            state.vessel.location_node,
            good_id,
            quantity,
            year=state.vessel.clock.current_date.year,
            seed=seed,
        )
        after = replace(state, commerce=result.state_after)
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
        access = self.access_view(state)
        if not access.commercial_access:
            return self._blocked_trade(state, self._access_block_reason(access.status))
        result = self.trade.sell(
            state.commerce,
            state.vessel.location_node,
            good_id,
            quantity,
            year=state.vessel.clock.current_date.year,
            seed=seed,
        )
        after = replace(state, commerce=result.state_after)
        return SessionTradeResult(
            executed=result.executed,
            reasons=result.reasons,
            state_before=state,
            state_after=after,
            trade_result=result,
        )

    def expedition_authorizes(self, state: GameSessionState, route_id: str) -> bool:
        return self.expedition.authorizes(
            state.active_expedition_id,
            state.expedition_leg_sequence,
            route_id,
            state.vessel.clock.current_date,
        )

    def plan_voyage(
        self,
        state: GameSessionState,
        route_id: str,
        *,
        pilot_id: str | None = None,
        seed: int = 0,
    ) -> VoyagePlan:
        plan = self.travel.plan_voyage(
            state.vessel,
            route_id,
            self.route_nav(state, route_id),
            pilot_id=pilot_id,
            fleet_command=self.expedition_authorizes(state, route_id),
            seed=seed,
            preserve_observed_timing=(
                state.chronology_mode is ChronologyMode.GUIDED
            ),
        )
        stop = self.active_stop(state)
        if (
            stop is not None
            and state.chronology_mode is ChronologyMode.GUIDED
            and not self.stops.release_reached(stop, state.vessel.clock.current_date)
        ):
            blockers = tuple(dict.fromkeys((*plan.blockers, "HISTORICAL_STOP_NOT_RELEASED")))
            return replace(plan, feasible=False, blockers=blockers)
        return plan

    def execute_voyage(
        self, state: GameSessionState, plan: VoyagePlan
    ) -> GameSessionState:
        expedition_leg_completed = self.expedition_authorizes(state, plan.route_id)
        completed_sequence = state.expedition_leg_sequence
        completed_expedition_id = state.active_expedition_id

        chronology = state.chronology_mode
        departing_stop = self.active_stop(state)
        if (
            departing_stop is not None
            and chronology is ChronologyMode.GUIDED
            and state.vessel.clock.current_date > departing_stop.departure_date
        ):
            chronology = ChronologyMode.COUNTERFACTUAL

        vessel_after = self.travel.execute_voyage(state.vessel, plan)
        after = replace(
            state,
            vessel=vessel_after,
            chronology_mode=chronology,
            active_stop_id=None,
            voyage_event_history=(*state.voyage_event_history, *plan.events),
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
        after = self._replace_route_knowledge(after, plan.route_id, learned_route)

        if expedition_leg_completed:
            assert completed_expedition_id is not None
            assert completed_sequence is not None
            stop = self.stops.for_leg(completed_expedition_id, completed_sequence)
            if stop is not None:
                if (
                    chronology is ChronologyMode.GUIDED
                    and not self.stops.arrives_on_schedule(
                        stop, vessel_after.clock.current_date
                    )
                ):
                    chronology = ChronologyMode.COUNTERFACTUAL
                after = replace(
                    after,
                    chronology_mode=chronology,
                    active_stop_id=stop.stop_id,
                )

            next_id, next_sequence = self.expedition.advance(
                completed_expedition_id, completed_sequence
            )
            after = replace(
                after,
                active_expedition_id=next_id,
                expedition_leg_sequence=next_sequence,
            )
        return after
