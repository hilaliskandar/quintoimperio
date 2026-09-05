"""Permanencias documentadas de expedicoes e cronologia guiada.

A camada registra escalas historicas sem transformar automaticamente atividades
como agua, carenagem ou reparo em quantidades fisicas. Datas de chegada/partida
e ``observed_stay_days`` permanecem campos distintos porque uma duracao narrada
pode nao coincidir com a diferenca aritmetica entre datas editoriais.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum
from pathlib import Path

from quintoimperio.data.loader import RepositoryData


class ChronologyMode(str, Enum):
    """Modo temporal da campanha em relacao a cronologia documentada."""

    GUIDED = "GUIDED"
    COUNTERFACTUAL = "COUNTERFACTUAL"


@dataclass(frozen=True)
class ExpeditionStop:
    stop_id: str
    expedition_id: str
    sequence: int
    node_id: str
    arrival_date: date
    departure_date: date
    observed_stay_days: int
    activities: tuple[str, ...]
    evidence_grade: str
    evidence_scope: str
    source_id: str
    notes: str


class ExpeditionStopModel:
    """Le permanencias historicas sem aplicar efeitos materiais automaticos."""

    def __init__(self, root: Path | None = None) -> None:
        repository = RepositoryData(root)
        self.root = repository.root
        stops: list[ExpeditionStop] = []
        for row in repository.historical("expedition_stops.csv"):
            stops.append(
                ExpeditionStop(
                    stop_id=row["stop_id"],
                    expedition_id=row["expedition_id"],
                    sequence=int(row["sequence"]),
                    node_id=row["node_id"],
                    arrival_date=date.fromisoformat(row["arrival_date"]),
                    departure_date=date.fromisoformat(row["departure_date"]),
                    observed_stay_days=int(row["observed_stay_days"]),
                    activities=tuple(
                        item for item in row["activities"].split("|") if item
                    ),
                    evidence_grade=row["evidence_grade"],
                    evidence_scope=row["evidence_scope"],
                    source_id=row["source_id"],
                    notes=row["notes"],
                )
            )
        self.stops = {stop.stop_id: stop for stop in stops}
        self.by_leg = {
            (stop.expedition_id, stop.sequence): stop for stop in stops
        }

    def stop(self, stop_id: str | None) -> ExpeditionStop | None:
        if stop_id is None:
            return None
        return self.stops.get(stop_id)

    def for_leg(self, expedition_id: str, sequence: int) -> ExpeditionStop | None:
        return self.by_leg.get((expedition_id, sequence))

    @staticmethod
    def arrives_on_schedule(stop: ExpeditionStop, arrival_date: date) -> bool:
        """Regra auditavel v0.1: cronologia guiada exige a data registrada."""
        return arrival_date == stop.arrival_date

    @staticmethod
    def days_until_release(stop: ExpeditionStop, current_date: date) -> int:
        return max(0, (stop.departure_date - current_date).days)

    @staticmethod
    def release_reached(stop: ExpeditionStop, current_date: date) -> bool:
        return current_date >= stop.departure_date
