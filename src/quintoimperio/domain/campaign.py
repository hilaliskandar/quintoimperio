"""Orquestração mínima da campanha histórica Lisboa–Calecute.

Esta camada compõe ``ServiceKnowledgeSessionModel`` sem alterar dados históricos.
Ela usa as datas de partida já registradas em ``voyage_observations.csv`` como
referência de cronologia quando a sessão está em ``ChronologyMode.GUIDED``.

Uma espera guiada fora de ``expedition_stops.csv`` apenas sincroniza o relógio
com a próxima partida observada. Ela não cria uma nova permanência histórica,
não atribui atividades e não concede recursos automaticamente.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date
from math import ceil
from pathlib import Path

from .expedition import ExpeditionLeg
from .port import PortServiceKind, ServiceAvailability
from .service_knowledge import ServiceKnowledgeSessionModel
from .session import GameSessionState, SessionWaitResult
from .stop import ChronologyMode
from .travel import VoyagePlan


@dataclass(frozen=True)
class LogisticsPlanningView:
    """Leitura de planejamento; não concede recursos nem altera evidência histórica."""

    current_autonomy_days: float
    next_leg_required_days: float | None
    logistics_horizon_required_days: float | None
    logistics_horizon_end_node: str | None
    recommended_margin_days: float
    margin_after_next_leg_days: float | None
    margin_after_logistics_horizon_days: float | None
    meets_recommended_margin: bool | None
    in_predeparture_phase: bool
    historical_departure_date: date | None
    next_destination_node: str | None
    next_destination_provisions_evidence_indeterminate: bool


class HistoricalCampaignModel:
    """Fachada da sessão para a vertical slice histórica de 1497–1498."""

    PREDEPARTURE_START = date(1497, 7, 6)
    GAMA_DEPARTURE = date(1497, 7, 8)
    RECOMMENDED_LOGISTICS_MARGIN_DAYS = 20.0

    def __init__(self, root: Path | None = None) -> None:
        self.session = ServiceKnowledgeSessionModel(root)

    def __getattr__(self, name: str):
        """Delega os demais sistemas ao modelo de sessão composto."""
        return getattr(self.session, name)

    def initial_playable_state(self) -> GameSessionState:
        """Abre a campanha em uma fase simulada de preparação de dois dias.

        A data de 1497-07-06 é uma camada de jogo. A partida histórica da primeira
        perna continua sendo 1497-07-08 e é obtida das observações da viagem.
        """
        return self.session.initial_state(
            active_expedition_id="EXP_GAMA_1497",
            start_date=self.PREDEPARTURE_START,
            chronology_mode=ChronologyMode.GUIDED,
        )

    def current_leg(self, state: GameSessionState) -> ExpeditionLeg | None:
        if state.active_expedition_id is None or state.expedition_leg_sequence is None:
            return None
        return self.session.expedition.leg(
            state.active_expedition_id,
            state.expedition_leg_sequence,
        )

    def _observed_departure_date(self, route_id: str, origin_node: str) -> date | None:
        dates = {
            date.fromisoformat(row["departure_date"])
            for row in self.session.travel.navigation.observations
            if row["route_id"] == route_id
            and row.get("departure_date")
            and row.get("departure_node") == origin_node
        }
        if not dates:
            return None
        if len(dates) > 1:
            raise ValueError(
                f"Rota {route_id} possui datas de partida conflitantes: "
                + ", ".join(sorted(item.isoformat() for item in dates))
            )
        return next(iter(dates))

    def guided_departure_date(self, state: GameSessionState) -> date | None:
        """Retorna a data observada da partida da perna ativa, quando inequívoca."""
        if state.chronology_mode is not ChronologyMode.GUIDED:
            return None
        leg = self.current_leg(state)
        if leg is None:
            return None
        route = self.session.routes[leg.route_id]
        if route["origin_node"] != state.vessel.location_node:
            return None
        return self._observed_departure_date(leg.route_id, state.vessel.location_node)

    def in_predeparture_phase(self, state: GameSessionState) -> bool:
        expected = self.guided_departure_date(state)
        return bool(
            state.active_expedition_id == "EXP_GAMA_1497"
            and state.expedition_leg_sequence == 1
            and state.vessel.location_node == "LIS"
            and expected == self.GAMA_DEPARTURE
            and state.vessel.clock.current_date < expected
        )

    def _historical_leg_provision_requirement(
        self, leg: ExpeditionLeg, *, seed: int = 0
    ) -> float | None:
        """Requisito abstrato da perna em sua partida observada, sem executar viagem."""
        route = self.session.routes[leg.route_id]
        departure = self._observed_departure_date(leg.route_id, route["origin_node"])
        if departure is None:
            return None
        duration = self.session.travel.navigation.estimate_duration_days(
            leg.route_id, departure, seed=seed
        )
        if duration is None:
            return None
        rate = float(
            self.session.travel.rules[("PROVISIONS", "DAY_EQUIVALENT_PER_TRAVEL_DAY")]
        )
        return max(1, ceil(duration)) * rate

    def _logistics_horizon(
        self,
        state: GameSessionState,
        *,
        current_required: float,
        seed: int = 0,
    ) -> tuple[float, str]:
        """Soma pernas até abastecimento historicamente documentado ou fim da expedição.

        O cálculo não presume serviço em ``UNKNOWN`` nem em ``NONE``. Ele apenas
        identifica quanto da sequência guiada precisa ser coberto antes de alcançar
        um destino cuja disponibilidade de provisões esteja documentada como LOW,
        MEDIUM ou HIGH. Se nenhum destino restante tiver serviço documentado, o
        horizonte termina no último nó da expedição.
        """
        leg = self.current_leg(state)
        if leg is None:
            raise ValueError("Nenhuma perna ativa para horizonte logístico")

        route = self.session.routes[leg.route_id]
        total = current_required
        end_node = route["destination_node"]
        availability = self.session.port.availability(end_node, PortServiceKind.PROVISIONS)
        if availability not in {ServiceAvailability.UNKNOWN, ServiceAvailability.NONE}:
            return total, end_node

        expedition_id = state.active_expedition_id
        if expedition_id is None:
            return total, end_node
        for future_leg in self.session.expedition.legs.get(expedition_id, ()):
            if future_leg.sequence <= leg.sequence:
                continue
            required = self._historical_leg_provision_requirement(future_leg, seed=seed)
            if required is None:
                break
            total += required
            future_route = self.session.routes[future_leg.route_id]
            end_node = future_route["destination_node"]
            availability = self.session.port.availability(
                end_node, PortServiceKind.PROVISIONS
            )
            if availability not in {ServiceAvailability.UNKNOWN, ServiceAvailability.NONE}:
                break
        return total, end_node

    def logistics_planning_view(
        self, state: GameSessionState, *, seed: int = 0
    ) -> LogisticsPlanningView:
        """Expõe autonomia, horizonte e margem de prudência sem automatizar decisões.

        Os 20 dias são uma heurística de robustez derivada dos playtests, não uma
        ração, duração ou requisito histórico. Para cronologia guiada, o requisito
        da próxima perna é calculado na data em que ela pode efetivamente partir.
        Quando o próximo destino não oferece provisões historicamente documentadas,
        o horizonte prossegue pelas pernas seguintes até o próximo abastecimento
        documentado ou até o fim da expedição. Isso não converte ``UNKNOWN`` em
        serviço e não concede recursos ao jogador.
        """
        leg = self.current_leg(state)
        expected = self.guided_departure_date(state)
        if leg is None:
            return LogisticsPlanningView(
                current_autonomy_days=state.vessel.provision_days,
                next_leg_required_days=None,
                logistics_horizon_required_days=None,
                logistics_horizon_end_node=None,
                recommended_margin_days=self.RECOMMENDED_LOGISTICS_MARGIN_DAYS,
                margin_after_next_leg_days=None,
                margin_after_logistics_horizon_days=None,
                meets_recommended_margin=None,
                in_predeparture_phase=False,
                historical_departure_date=expected,
                next_destination_node=None,
                next_destination_provisions_evidence_indeterminate=False,
            )

        planning_state = state
        if expected is not None and state.vessel.clock.current_date < expected:
            days = (expected - state.vessel.clock.current_date).days
            planning_state = replace(
                state,
                vessel=replace(
                    state.vessel,
                    clock=state.vessel.clock.advance(days),
                ),
            )
        pilot_id = self.recommended_pilot_id(planning_state, leg.route_id)
        plan = self.session.plan_voyage(
            planning_state,
            leg.route_id,
            pilot_id=pilot_id,
            seed=seed,
        )
        required = plan.provision_days_required
        remaining = state.vessel.provision_days - required
        horizon_required, horizon_end = self._logistics_horizon(
            state,
            current_required=required,
            seed=seed,
        )
        horizon_remaining = state.vessel.provision_days - horizon_required
        route = self.session.routes[leg.route_id]
        destination = route["destination_node"]
        destination_unknown = (
            self.session.port.availability(destination, PortServiceKind.PROVISIONS)
            is ServiceAvailability.UNKNOWN
        )
        return LogisticsPlanningView(
            current_autonomy_days=state.vessel.provision_days,
            next_leg_required_days=required,
            logistics_horizon_required_days=horizon_required,
            logistics_horizon_end_node=horizon_end,
            recommended_margin_days=self.RECOMMENDED_LOGISTICS_MARGIN_DAYS,
            margin_after_next_leg_days=remaining,
            margin_after_logistics_horizon_days=horizon_remaining,
            meets_recommended_margin=(
                horizon_remaining >= self.RECOMMENDED_LOGISTICS_MARGIN_DAYS
            ),
            in_predeparture_phase=self.in_predeparture_phase(state),
            historical_departure_date=expected,
            next_destination_node=destination,
            next_destination_provisions_evidence_indeterminate=destination_unknown,
        )

    def wait_for_guided_departure(self, state: GameSessionState) -> SessionWaitResult:
        """Avança somente o relógio até a próxima partida histórica observada.

        Se a perna atual possui uma escala normalizada em ``expedition_stops.csv``,
        preserva-se a semântica existente de ``wait_for_stop_release``. Nos nós
        sem uma permanência normalizada, a espera representa apenas alinhamento
        cronológico com a data de partida observada da próxima perna.
        """
        stop = self.session.active_stop(state)
        if stop is not None:
            return self.session.wait_for_stop_release(state)
        if state.chronology_mode is not ChronologyMode.GUIDED:
            return SessionWaitResult(
                executed=False,
                reasons=("COUNTERFACTUAL_CHRONOLOGY_NO_FORCED_WAIT",),
                days_waited=0,
                state_before=state,
                state_after=state,
            )

        expected = self.guided_departure_date(state)
        if expected is None:
            return SessionWaitResult(
                executed=False,
                reasons=("NO_GUIDED_DEPARTURE_DATE",),
                days_waited=0,
                state_before=state,
                state_after=state,
            )
        current = state.vessel.clock.current_date
        if current == expected:
            return SessionWaitResult(
                executed=False,
                reasons=("GUIDED_DEPARTURE_REACHED",),
                days_waited=0,
                state_before=state,
                state_after=state,
            )
        if current > expected:
            return SessionWaitResult(
                executed=False,
                reasons=("GUIDED_DEPARTURE_ALREADY_PASSED",),
                days_waited=0,
                state_before=state,
                state_after=state,
            )

        days = (expected - current).days
        vessel = replace(state.vessel, clock=state.vessel.clock.advance(days))
        after = replace(state, vessel=vessel)
        return SessionWaitResult(
            executed=True,
            reasons=(),
            days_waited=days,
            state_before=state,
            state_after=after,
        )

    def recommended_pilot_id(
        self, state: GameSessionState, route_id: str
    ) -> str | None:
        """Retorna piloto elegível e relacionalmente disponível ao personagem."""
        return self.session.recommended_pilot_id(state, route_id)

    def plan_voyage(
        self,
        state: GameSessionState,
        route_id: str,
        *,
        pilot_id: str | None = None,
        seed: int = 0,
    ) -> VoyagePlan:
        """Planeja viagem e impede partida precoce na perna guiada ativa."""
        plan = self.session.plan_voyage(
            state,
            route_id,
            pilot_id=pilot_id,
            seed=seed,
        )
        leg = self.current_leg(state)
        if (
            state.chronology_mode is ChronologyMode.GUIDED
            and leg is not None
            and leg.route_id == route_id
        ):
            expected = self.guided_departure_date(state)
            if expected is not None and state.vessel.clock.current_date < expected:
                blockers = tuple(
                    dict.fromkeys((*plan.blockers, "HISTORICAL_DEPARTURE_NOT_REACHED"))
                )
                return replace(plan, feasible=False, blockers=blockers)
        return plan

    def plan_current_leg(self, state: GameSessionState, *, seed: int = 0) -> VoyagePlan:
        """Planeja a perna ativa e só atribui piloto após o requisito relacional."""
        leg = self.current_leg(state)
        if leg is None:
            raise ValueError("Nenhuma perna de expedição ativa")
        pilot_id = self.recommended_pilot_id(state, leg.route_id)
        return self.plan_voyage(
            state,
            leg.route_id,
            pilot_id=pilot_id,
            seed=seed,
        )

    def execute_voyage(
        self, state: GameSessionState, plan: VoyagePlan
    ) -> GameSessionState:
        """Executa a viagem e torna atraso guiado explicitamente contrafactual."""
        leg = self.current_leg(state)
        expected = None
        if (
            state.chronology_mode is ChronologyMode.GUIDED
            and leg is not None
            and leg.route_id == plan.route_id
        ):
            expected = self.guided_departure_date(state)
            if expected is not None and plan.departure_date < expected:
                raise ValueError("Partida anterior à data histórica guiada")

        after = self.session.execute_voyage(state, plan)
        if (
            state.chronology_mode is ChronologyMode.GUIDED
            and expected is not None
            and plan.departure_date > expected
            and after.chronology_mode is ChronologyMode.GUIDED
        ):
            after = replace(after, chronology_mode=ChronologyMode.COUNTERFACTUAL)
        return after
