"""Estados históricos temporais de nós sem reescrever o baseline estático.

A tabela ``node_state_events.csv`` registra transições documentais. Como muitas
datas são intervalos de incerteza, o estado efetivo só incorpora um evento
quando a data consultada é igual ou posterior ao limite superior documentado.
Isso evita antecipar fortificações, feitorias ou guarnições para datas em que
a fonte ainda permite que a transição não tivesse ocorrido.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date
from pathlib import Path

from quintoimperio.data.loader import RepositoryData


@dataclass(frozen=True)
class NodeHistoricalState:
    node_id: str
    institutional_presence: str
    fortification_state: str
    garrison_state: str
    access_state: str
    relationship_state: str
    sovereignty_note: str
    applied_event_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class NodeStateEvent:
    event_id: str
    node_id: str
    date_from: date
    date_to: date
    date_precision: str
    event_type: str
    institutional_presence: str
    fortification_state: str
    garrison_state: str
    access_state: str
    relationship_state: str
    sovereignty_note: str
    evidence_grade: str
    evidence_scope: str
    source_id: str
    notes: str


class NodeStateEventModel:
    """Resolve estados históricos datados sobre o baseline de ``nodes.csv``."""

    def __init__(self, root: Path | None = None) -> None:
        repository = RepositoryData(root)
        self.root = repository.root
        self.nodes = {
            row["node_id"]: row for row in repository.historical("nodes.csv")
        }
        self.events = tuple(
            sorted(
                (self._parse(row) for row in repository.historical("node_state_events.csv")),
                key=lambda item: (item.date_to, item.event_id),
            )
        )

    @staticmethod
    def _parse(row: dict[str, str]) -> NodeStateEvent:
        start = date.fromisoformat(row["date_from"])
        end = date.fromisoformat(row["date_to"] or row["date_from"])
        return NodeStateEvent(
            event_id=row["event_id"],
            node_id=row["node_id"],
            date_from=start,
            date_to=end,
            date_precision=row["date_precision"],
            event_type=row["event_type"],
            institutional_presence=row["institutional_presence"],
            fortification_state=row["fortification_state"],
            garrison_state=row["garrison_state"],
            access_state=row["access_state"],
            relationship_state=row["relationship_state"],
            sovereignty_note=row["sovereignty_note"],
            evidence_grade=row["evidence_grade"],
            evidence_scope=row["evidence_scope"],
            source_id=row["source_id"],
            notes=row["notes"],
        )

    def events_for(self, node_id: str) -> tuple[NodeStateEvent, ...]:
        if node_id not in self.nodes:
            raise KeyError(f"No desconhecido: {node_id}")
        return tuple(event for event in self.events if event.node_id == node_id)

    def baseline(self, node_id: str) -> NodeHistoricalState:
        try:
            node = self.nodes[node_id]
        except KeyError as exc:
            raise KeyError(f"No desconhecido: {node_id}") from exc
        return NodeHistoricalState(
            node_id=node_id,
            institutional_presence="NONE",
            fortification_state=node.get("fortification", "") or "UNKNOWN",
            garrison_state="NONE",
            access_state=node.get("access_regime", "") or "UNKNOWN",
            relationship_state="UNESTABLISHED",
            sovereignty_note=node.get("polity_1497", ""),
        )

    def effective_state(self, node_id: str, on_date: date) -> NodeHistoricalState:
        state = self.baseline(node_id)
        applied: list[str] = []
        for event in self.events_for(node_id):
            if on_date < event.date_to:
                continue
            state = replace(
                state,
                institutional_presence=(
                    event.institutional_presence or state.institutional_presence
                ),
                fortification_state=event.fortification_state or state.fortification_state,
                garrison_state=event.garrison_state or state.garrison_state,
                access_state=event.access_state or state.access_state,
                relationship_state=event.relationship_state or state.relationship_state,
                sovereignty_note=event.sovereignty_note or state.sovereignty_note,
            )
            applied.append(event.event_id)
        return replace(state, applied_event_ids=tuple(applied))
