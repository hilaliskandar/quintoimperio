"""Gate funcional mínimo para João da Nova 1501–1502.

Este módulo introduz apenas o estado inicial da expedição e a aquisição tardia
do aviso deixado pela armada de Cabral em São Brás. A data exata do encontro
não é inventada: a ação só é elegível dentro da janela documental já registrada
em ``expedition_events.csv`` e o teste conservador usa o limite superior dessa
janela. Rotas posteriores continuam fora deste incremento.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import date
from pathlib import Path

from .expedition_event import ExpeditionEvent, ExpeditionEventModel
from .p3_campaign import P3CampaignModel
from .session import GameSessionState
from .stop import ChronologyMode


class JoaoNovaCampaignModel(P3CampaignModel):
    """Extensão mínima da tranche P3 para a terceira armada da Índia."""

    EXPEDITION_ID = "EXP_JOAO_NOVA_1501"
    DEPARTURE = date(1501, 3, 5)
    MALABAR_WARNING_EVENT_ID = "NOVA1501_E01"
    MALABAR_WARNING_KEY = "P3_INFO:CABRAL_MALABAR_WARNING"

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

    def malabar_warning_event(self) -> ExpeditionEvent:
        """Retorna o evento documental preferido de aquisição em São Brás."""
        matches = tuple(
            event
            for event in self.expedition_events.preferred_for_expedition(self.EXPEDITION_ID)
            if event.event_id == self.MALABAR_WARNING_EVENT_ID
        )
        if len(matches) != 1:
            raise ValueError("Evento documental único de São Brás não encontrado.")
        return matches[0]

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
