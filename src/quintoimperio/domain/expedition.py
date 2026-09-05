"""Expedicoes e permissao institucional de navegacao.

A camada distingue capacidade individual de navegar uma rota da participacao em
uma armada comandada por terceiros. ``FLEET_COMMAND`` habilita somente a perna
corrente documentada da expedicao; nao eleva o conhecimento nautico pessoal e
nao concede bonus quantitativo.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

from quintoimperio.data.loader import RepositoryData


@dataclass(frozen=True)
class ExpeditionLeg:
    expedition_id: str
    sequence: int
    route_id: str
    period_from: int | None
    period_to: int | None
    command_basis: str


class ExpeditionModel:
    """Le expedicoes historicas e suas pernas agregadas."""

    def __init__(self, root: Path | None = None) -> None:
        repository = RepositoryData(root)
        self.root = repository.root
        self.expeditions = {
            row["expedition_id"]: row
            for row in repository.historical("expeditions.csv")
        }
        self.legs: dict[str, tuple[ExpeditionLeg, ...]] = {}
        grouped: dict[str, list[ExpeditionLeg]] = {}
        for row in repository.historical("expedition_routes.csv"):
            leg = ExpeditionLeg(
                expedition_id=row["expedition_id"],
                sequence=int(row["sequence"]),
                route_id=row["route_id"],
                period_from=int(row["period_from"]) if row["period_from"] else None,
                period_to=int(row["period_to"]) if row["period_to"] else None,
                command_basis=row["command_basis"],
            )
            grouped.setdefault(leg.expedition_id, []).append(leg)
        for expedition_id, legs in grouped.items():
            self.legs[expedition_id] = tuple(sorted(legs, key=lambda leg: leg.sequence))

    def first_sequence(self, expedition_id: str) -> int:
        try:
            return self.legs[expedition_id][0].sequence
        except (KeyError, IndexError) as exc:
            raise KeyError(f"Expedicao sem pernas: {expedition_id}") from exc

    def leg(self, expedition_id: str, sequence: int) -> ExpeditionLeg | None:
        for leg in self.legs.get(expedition_id, ()):
            if leg.sequence == sequence:
                return leg
        return None

    @staticmethod
    def _active(leg: ExpeditionLeg, on_date: date) -> bool:
        if leg.period_from is not None and on_date.year < leg.period_from:
            return False
        if leg.period_to is not None and on_date.year > leg.period_to:
            return False
        return True

    def authorizes(
        self,
        expedition_id: str | None,
        sequence: int | None,
        route_id: str,
        on_date: date,
    ) -> bool:
        if expedition_id is None or sequence is None:
            return False
        leg = self.leg(expedition_id, sequence)
        return bool(
            leg
            and leg.route_id == route_id
            and leg.command_basis == "FLEET_COMMAND"
            and self._active(leg, on_date)
        )

    def advance(
        self, expedition_id: str, completed_sequence: int
    ) -> tuple[str | None, int | None]:
        legs = self.legs.get(expedition_id, ())
        for leg in legs:
            if leg.sequence > completed_sequence:
                return expedition_id, leg.sequence
        return None, None
