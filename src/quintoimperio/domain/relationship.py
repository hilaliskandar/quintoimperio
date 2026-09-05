"""Relações do personagem com atores históricos explicitamente documentados.

A v0.1 não usa uma reputação global nem números de confiança/hostilidade. Um
ator só existe neste modelo quando está normalizado em ``data/actors.csv`` e
associado a um nó em ``data/node_actors.csv``. O estado da relação registra
apenas se houve contato explícito no loop.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import IntEnum
from pathlib import Path

from quintoimperio.data.loader import RepositoryData


class RelationshipStatus(IntEnum):
    UNESTABLISHED = 0
    CONTACTED = 1


@dataclass(frozen=True)
class HistoricalActor:
    actor_id: str
    label: str
    actor_type: str
    period_from: int | None
    period_to: int | None


@dataclass(frozen=True)
class NodeActor:
    node_id: str
    actor_id: str
    role: str
    period_from: int | None
    period_to: int | None


class RelationshipModel:
    """Consulta atores documentados e resolve contatos por nó/papel."""

    def __init__(self, root: Path | None = None) -> None:
        repository = RepositoryData(root)
        self.root = repository.root
        self.actors: dict[str, HistoricalActor] = {}
        for row in repository.historical("actors.csv"):
            self.actors[row["actor_id"]] = HistoricalActor(
                actor_id=row["actor_id"],
                label=row["label"],
                actor_type=row["actor_type"],
                period_from=int(row["period_from"]) if row["period_from"] else None,
                period_to=int(row["period_to"]) if row["period_to"] else None,
            )
        self.node_actors: tuple[NodeActor, ...] = tuple(
            NodeActor(
                node_id=row["node_id"],
                actor_id=row["actor_id"],
                role=row["role"],
                period_from=int(row["period_from"]) if row["period_from"] else None,
                period_to=int(row["period_to"]) if row["period_to"] else None,
            )
            for row in repository.historical("node_actors.csv")
        )

    @staticmethod
    def _active(start: int | None, end: int | None, on_date: date) -> bool:
        if start is not None and on_date.year < start:
            return False
        if end is not None and on_date.year > end:
            return False
        return True

    def actors_at(
        self,
        node_id: str,
        on_date: date,
        *,
        role: str | None = None,
    ) -> tuple[HistoricalActor, ...]:
        result: list[HistoricalActor] = []
        for link in self.node_actors:
            if link.node_id != node_id:
                continue
            if role is not None and link.role != role:
                continue
            if not self._active(link.period_from, link.period_to, on_date):
                continue
            actor = self.actors[link.actor_id]
            if not self._active(actor.period_from, actor.period_to, on_date):
                continue
            result.append(actor)
        return tuple(sorted(result, key=lambda actor: actor.actor_id))

    def actor_for_role(
        self, node_id: str, on_date: date, role: str
    ) -> HistoricalActor | None:
        actors = self.actors_at(node_id, on_date, role=role)
        if len(actors) > 1:
            raise ValueError(
                f"Mais de um ator para {node_id}/{role}/{on_date.year}; "
                "a v0.1 exige associação não ambígua"
            )
        return actors[0] if actors else None
