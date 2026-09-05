"""Calendário do domínio e fases gerais da monção do Índico."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from enum import Enum


class MonsoonPhase(str, Enum):
    """Fases gerais usadas pela v0.1.

    A classificação segue o regime amplo descrito por Alpers: monção de
    nordeste aproximadamente de novembro a janeiro e monção de sudoeste de
    abril a agosto. Fevereiro-março e setembro-outubro ficam como transições.
    Isso não substitui regras regionais específicas de navegação.
    """

    NORTHEAST = "NORTHEAST"
    TRANSITION_NE_SW = "TRANSITION_NE_SW"
    SOUTHWEST = "SOUTHWEST"
    TRANSITION_SW_NE = "TRANSITION_SW_NE"


def monsoon_phase(day: date) -> MonsoonPhase:
    if day.month in (11, 12, 1):
        return MonsoonPhase.NORTHEAST
    if day.month in (4, 5, 6, 7, 8):
        return MonsoonPhase.SOUTHWEST
    if day.month in (2, 3):
        return MonsoonPhase.TRANSITION_NE_SW
    return MonsoonPhase.TRANSITION_SW_NE


@dataclass(frozen=True)
class GameClock:
    """Relógio imutável simples para permitir testes determinísticos."""

    current_date: date

    def advance(self, days: int) -> "GameClock":
        if days < 0:
            raise ValueError("O calendário do jogo não pode retroceder por esta operação.")
        return GameClock(self.current_date + timedelta(days=days))

    @property
    def monsoon(self) -> MonsoonPhase:
        return monsoon_phase(self.current_date)
