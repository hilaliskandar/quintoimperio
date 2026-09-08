"""Gate funcional mínimo para Vasco da Gama 1502–1503.

A primeira fatia executável termina em Cananor. Sofala, Quiloa e Cananor são
âncoras documentais com resolução mensal; na ausência de observações diárias,
o timing das pernas é explicitamente de simulação. A força de Vicente Sodré
permanece, nesta etapa, um efeito histórico consultável e não uma segunda frota
ativa no mesmo save.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from .expedition_event import ExpeditionEvent, ExpeditionEventModel
from .p3_campaign import P3CampaignModel
from .session import GameSessionState
from .stop import ChronologyMode


class Gama1502CampaignModel(P3CampaignModel):
    """Extensão mínima da tranche F2 para a segunda armada de Vasco da Gama."""

    EXPEDITION_ID = "EXP_GAMA_1502"
    DEPARTURE = date(1502, 2, 1)
    SODRE_FORCE_EVENT_ID = "GAMA1502_E03"

    def __init__(self, root: Path | None = None) -> None:
        super().__init__(root)
        self.expedition_events = ExpeditionEventModel(root)

    def initial_gama_1502_state(
        self,
        *,
        provision_days: float = 500.0,
        condition: float = 100.0,
        capital_index: float = 100.0,
        capacity_total: float = 30.0,
    ) -> GameSessionState:
        """Abre a campanha na partida documental principal de 01/02/1502."""
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

    def sodre_force_remains_event(self) -> ExpeditionEvent:
        """Retorna o estado documental da força residente sem ativá-la no save."""
        matches = tuple(
            event
            for event in self.expedition_events.preferred_for_expedition(self.EXPEDITION_ID)
            if event.event_id == self.SODRE_FORCE_EVENT_ID
        )
        if len(matches) != 1:
            raise ValueError(
                f"Evento documental único não encontrado: {self.SODRE_FORCE_EVENT_ID}"
            )
        return matches[0]
