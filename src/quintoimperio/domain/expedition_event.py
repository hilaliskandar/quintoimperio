"""Eventos documentais de expedição reutilizáveis além do epílogo de 1499."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

from quintoimperio.data.loader import RepositoryData


@dataclass(frozen=True)
class ExpeditionEvent:
    event_id: str
    expedition_id: str
    sequence: int
    trajectory_id: str
    subject_type: str
    subject_label: str
    event_type: str
    origin_node: str | None
    destination_node: str | None
    date_from: date
    date_to: date
    date_precision: str
    variant_group: str | None
    preferred_for_simulation: bool
    evidence_grade: str
    evidence_scope: str
    source_id: str
    notes: str


class ExpeditionEventModel:
    """Consulta eventos históricos sem convertê-los automaticamente em mecânicas."""

    def __init__(self, root: Path | None = None) -> None:
        repository = RepositoryData(root)
        self.root = repository.root
        self.events = tuple(
            sorted(
                (self._parse(row) for row in repository.historical("expedition_events.csv")),
                key=lambda item: (item.expedition_id, item.sequence, item.event_id),
            )
        )

    @staticmethod
    def _parse(row: dict[str, str]) -> ExpeditionEvent:
        start = date.fromisoformat(row["date_from"])
        end = date.fromisoformat(row["date_to"] or row["date_from"])
        return ExpeditionEvent(
            event_id=row["event_id"],
            expedition_id=row["expedition_id"],
            sequence=int(row["sequence"]),
            trajectory_id=row["trajectory_id"],
            subject_type=row["subject_type"],
            subject_label=row["subject_label"],
            event_type=row["event_type"],
            origin_node=row["origin_node"] or None,
            destination_node=row["destination_node"] or None,
            date_from=start,
            date_to=end,
            date_precision=row["date_precision"],
            variant_group=row["variant_group"] or None,
            preferred_for_simulation=row["preferred_for_simulation"] == "TRUE",
            evidence_grade=row["evidence_grade"],
            evidence_scope=row["evidence_scope"],
            source_id=row["source_id"],
            notes=row["notes"],
        )

    def for_expedition(self, expedition_id: str) -> tuple[ExpeditionEvent, ...]:
        return tuple(event for event in self.events if event.expedition_id == expedition_id)

    def preferred_for_expedition(self, expedition_id: str) -> tuple[ExpeditionEvent, ...]:
        return tuple(
            event
            for event in self.for_expedition(expedition_id)
            if event.preferred_for_simulation
        )

    def available_by(self, expedition_id: str, on_date: date) -> tuple[ExpeditionEvent, ...]:
        """Eventos seguramente ocorridos até a data, usando o limite superior da fonte."""
        return tuple(
            event
            for event in self.for_expedition(expedition_id)
            if event.date_to <= on_date
        )
