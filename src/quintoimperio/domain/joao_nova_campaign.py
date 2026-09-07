"""Gate funcional mínimo para João da Nova 1501–1502.

Este módulo preserva o estado inicial da expedição, a aquisição tardia do aviso
deixado pela armada de Cabral em São Brás e a ordem das pernas normalizadas.
Datas diárias não documentadas permanecem fora de ``voyage_observations.csv``:
essas pernas usam timing de simulação sem abandonar ``ChronologyMode.GUIDED``.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import date
from pathlib import Path

from .expedition_event import ExpeditionEvent, ExpeditionEventModel
from .p3_campaign import P3CampaignModel
from .session import GameSessionState, SessionWaitResult
from .stop import ChronologyMode


class JoaoNovaCampaignModel(P3CampaignModel):
    """Extensão mínima da tranche P3 para a terceira armada da Índia."""

    EXPEDITION_ID = "EXP_JOAO_NOVA_1501"
    DEPARTURE = date(1501, 3, 5)
    MALABAR_WARNING_EVENT_ID = "NOVA1501_E01"
    MALABAR_WARNING_KEY = "P3_INFO:CABRAL_MALABAR_WARNING"
    WARNING_REQUIRED_BLOCKER = "CABRAL_MALABAR_WARNING_NOT_ACQUIRED"
    CANNANORE_BLOCKADE_EVENT_ID = "NOVA1501_E03"
    CANNANORE_BLOCKADE_START = date(1501, 12, 30)

    def __init__(self, root: Path | None = None) -> None:
        super().__init__(root)
        self.expedition_events = ExpeditionEventModel(root)

    def initial_joao_nova_state(
        self,
        *,
        provision_days: float = 120.0,
        condition: float = 100.0,
        capital_index: float = 100.0,
        capacity_total: float = 30.0,
    ) -> GameSessionState:
        """Abre a expedição em Lisboa sem conhecimento do aviso de São Brás."""
        return self.session.initial_state(
            location_node="LIS",
            start_date=self.DEPARTURE,
            provision_days=provision_days,
            condition=condition,
            capital_index=capital_index,
            capacity_total=capacity_total,
            active_expedition_id=self.EXPEDITION_ID,
            chronology_mode=ChronologyMode.GUIDED,
        )

    def _preferred_event(self, event_id: str) -> ExpeditionEvent:
        matches = tuple(
            event
            for event in self.expedition_events.preferred_for_expedition(self.EXPEDITION_ID)
            if event.event_id == event_id
        )
        if len(matches) != 1:
            raise ValueError(f"Evento documental único não encontrado: {event_id}")
        return matches[0]

    def malabar_warning_event(self) -> ExpeditionEvent:
        """Retorna o evento documental preferido de aquisição em São Brás."""
        return self._preferred_event(self.MALABAR_WARNING_EVENT_ID)

    def cannanore_blockade_event(self) -> ExpeditionEvent:
        """Retorna apenas o marco exato de início do bloqueio em 30/12/1501."""
        return self._preferred_event(self.CANNANORE_BLOCKADE_EVENT_ID)

    def joao_nova_has_malabar_warning(self, state: GameSessionState) -> bool:
        return self.MALABAR_WARNING_KEY in state.information_history

    def can_acquire_malabar_warning(self, state: GameSessionState) -> bool:
        """Exige a expedição correta, São Brás e a janela documental do evento."""
        if state.active_expedition_id != self.EXPEDITION_ID:
            return False
        if state.vessel.location_node != "SBR":
            return False
        if self.joao_nova_has_malabar_warning(state):
            return False
        event = self.malabar_warning_event()
        current = state.vessel.clock.current_date
        return event.date_from <= current <= event.date_to

    def acquire_malabar_warning(self, state: GameSessionState) -> GameSessionState:
        """Registra a informação como conhecimento da expedição, em operação one-shot."""
        if not self.can_acquire_malabar_warning(state):
            return state
        return replace(
            state,
            information_history=state.information_history + (self.MALABAR_WARNING_KEY,),
        )

    def plan_current_leg(self, state: GameSessionState, *, seed: int = 0):
        """Impede SBR→KIL no histórico guiado enquanto o aviso não foi adquirido.

        A restrição é específica desta expedição e não cria um sistema geral de
        mensagens. Ela torna causal a latência já documentada: João da Nova parte
        de Lisboa sem conhecer a ruptura em Calecute e só prossegue pela sequência
        historicamente informada depois de encontrar o aviso em São Brás.
        """
        plan = super().plan_current_leg(state, seed=seed)
        if (
            state.active_expedition_id == self.EXPEDITION_ID
            and state.expedition_leg_sequence == 2
            and state.vessel.location_node == "SBR"
            and state.chronology_mode is ChronologyMode.GUIDED
            and not self.joao_nova_has_malabar_warning(state)
        ):
            blockers = tuple(
                dict.fromkeys((*plan.blockers, self.WARNING_REQUIRED_BLOCKER))
            )
            return replace(plan, feasible=False, blockers=blockers)
        return plan

    def wait_until_cannanore_blockade(self, state: GameSessionState) -> SessionWaitResult:
        """Sincroniza o relógio com 30/12 sem tratar a data como chegada a Cananor.

        As pernas intermediárias de F1 não possuem observações diárias e podem
        terminar antes do marco exato documentado. Esta espera representa somente
        permanência temporal entre a conclusão simulada da sequência comercial e o
        início conhecido do bloqueio; não cria atividades, recursos ou uma data de
        chegada histórica inexistente.
        """
        if state.chronology_mode is not ChronologyMode.GUIDED:
            return SessionWaitResult(
                executed=False,
                reasons=("COUNTERFACTUAL_CHRONOLOGY_NO_FORCED_WAIT",),
                days_waited=0,
                state_before=state,
                state_after=state,
            )
        if state.vessel.location_node != "CAN":
            return SessionWaitResult(
                executed=False,
                reasons=("VESSEL_NOT_AT_CANNANORE_BLOCKADE_MARKER",),
                days_waited=0,
                state_before=state,
                state_after=state,
            )
        current = state.vessel.clock.current_date
        if current == self.CANNANORE_BLOCKADE_START:
            return SessionWaitResult(
                executed=False,
                reasons=("CANNANORE_BLOCKADE_DATE_REACHED",),
                days_waited=0,
                state_before=state,
                state_after=state,
            )
        if current > self.CANNANORE_BLOCKADE_START:
            return SessionWaitResult(
                executed=False,
                reasons=("CANNANORE_BLOCKADE_DATE_ALREADY_PASSED",),
                days_waited=0,
                state_before=state,
                state_after=state,
            )
        days = (self.CANNANORE_BLOCKADE_START - current).days
        after = replace(
            state,
            vessel=replace(state.vessel, clock=state.vessel.clock.advance(days)),
        )
        return SessionWaitResult(
            executed=True,
            reasons=(),
            days_waited=days,
            state_before=state,
            state_after=after,
        )
