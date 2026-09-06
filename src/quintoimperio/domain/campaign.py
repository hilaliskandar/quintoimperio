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
    recommended_margin_days: float
    margin_after_next_leg_days: float | None
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

        dates = {
            date.fromisoformat(row["departure_date"])
            for row in self.session.travel.navigation.observations
            if row["route_id"] == leg.route_id
            and row.get("departure_date")
            and row.get("departure_node") == state.vessel.location_node
        }
        if not dates:
            return None
        if len(dates) > 1:
            raise ValueError(
                f"Perna guiada {leg.route_id} possui datas de partida conflitantes: "
                + ", ".join(sorted(item.isoformat() for item in dates))
            )
        return next(iter(dates))

    def in_predeparture_phase(self, state: GameSessionState) -> bool:
        expected = self.guided_departure_date(state)
        return bool(
            state.active_expedition_id == "EXP_GAMA_1497"
            and state.expedition_leg_sequence == 1
            and state.vessel.location_node == "LIS"
            and expected == self.GAMA_DEPARTURE
            and state.vessel.clock.current_date < expected
        )

    def logistics_planning_view(self, state: GameSessionState) -> LogisticsPlanningView:
        """Expõe autonomia e margem de prudência sem automatizar decisões.

        Os 20 dias são uma heurística de robustez derivada dos playtests, não uma
        ração, duração ou requisito histórico. A indicação de incerteza consulta
        apenas o campo histórico de provisões do próximo destino.
        """
        leg = self.current_leg(state)
        expected = self.guided_departure_date(state)
        if leg is None:
            return LogisticsPlanningView(
                current_autonomy_days=state.vessel.provision_days,
                next_leg_required_days=None,
                recommended_margin_days=self.RECOMMENDED_LOGISTICS_MARGIN_DAYS,
                margin_after_next_leg_days=None,
                meets_recommended_margin=None,
                in_predeparture_phase=False,
                historical_departure_date=expected,
                next_destination_node=None,
                next_destination_provisions_evidence_indeterminate=False,
            )

        plan = self.session.plan_voyage(state, leg.route_id, seed=1498)
        required = plan.provision_days_required
        remaining = state.vessel.provision_days - required
        route = self.session.routes[leg.route_id]
        destination = route["destination_node"]
        destination_unknown = (
            self.session.port.availability(destination, PortServiceKind.PROVISIONS)
            is ServiceAvailability.UNKNOWN
        )
        return LogisticsPlanningView(
            current_autonomy_days=state.vessel.provision_days,
            next_leg_required_days=required,
            recommended_margin_days=self.RECOMMENDED_LOGISTICS_MARGIN_DAYS,
            margin_after_next_leg_days=remaining,
            meets_recommended_margin=remaining >= self.RECOMMENDED_LOGISTICS_MARGIN_DAYS,
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
