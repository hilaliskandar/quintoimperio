"""Fachada incremental para campanhas P3 já normalizadas.

A classe reutiliza integralmente ``HistoricalCampaignModel``. Ela só define
estados iniciais das novas expedições; rotas, cronologia, logística, risco e
persistência continuam pertencendo aos modelos existentes. Valores de
provisões são parâmetros abstratos de simulação e não alegações históricas.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from .campaign import HistoricalCampaignModel
from .session import GameSessionState
from .stop import ChronologyMode


class P3CampaignModel(HistoricalCampaignModel):
    """Extensão opt-in para as campanhas documentadas a partir de 1500."""

    CABRAL_DEPARTURE = date(1500, 3, 9)

    def __init__(self, root: Path | None = None) -> None:
        super().__init__(root)

    def initial_cabral_state(
        self,
        *,
        provision_days: float = 60.0,
        condition: float = 100.0,
        capital_index: float = 100.0,
        capacity_total: float = 30.0,
    ) -> GameSessionState:
        """Abre a tranche Cabral na partida documental de 09/03/1500."""
        return self.session.initial_state(
            location_node="LIS",
            start_date=self.CABRAL_DEPARTURE,
            provision_days=provision_days,
            condition=condition,
            capital_index=capital_index,
            capacity_total=capacity_total,
            active_expedition_id="EXP_CABRAL_1500",
            chronology_mode=ChronologyMode.GUIDED,
        )
