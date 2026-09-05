"""Conhecimento do mundo separado entre personagem e Coroa."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import IntEnum
from pathlib import Path

from quintoimperio.data.loader import RepositoryData


class KnowledgeLevel(IntEnum):
    UNKNOWN = 0
    RUMORED = 1
    PARTIAL = 2
    OPERATIONAL = 3
    CONFIRMED = 4


@dataclass(frozen=True)
class KnowledgeState:
    geo: KnowledgeLevel
    nav: KnowledgeLevel
    market: KnowledgeLevel
    political: KnowledgeLevel

    def improve(self, dimension: str, amount: int = 1) -> "KnowledgeState":
        if dimension not in {"geo", "nav", "market", "political"}:
            raise ValueError(f"Dimensão de conhecimento inválida: {dimension}")
        current = int(getattr(self, dimension))
        value = KnowledgeLevel(min(int(KnowledgeLevel.CONFIRMED), current + amount))
        return replace(self, **{dimension: value})


class KnowledgeModel:
    """Converte descrições históricas do estado inicial em índices de jogo.

    A conversão é explicitamente uma regra de simulação armazenada em
    ``simulation/knowledge_rules.csv``. O campo da Coroa e o campo do personagem
    são lidos separadamente de ``nodes.csv``.
    """

    def __init__(self, root: Path | None = None) -> None:
        repository = RepositoryData(root)
        self.nodes = {
            row["node_id"]: row for row in repository.historical("nodes.csv")
        }
        self.rules: dict[tuple[str, str], KnowledgeState] = {}
        for row in repository.simulation("knowledge_rules.csv"):
            self.rules[(row["perspective"], row["source_value"])] = KnowledgeState(
                geo=KnowledgeLevel(int(row["geo"])),
                nav=KnowledgeLevel(int(row["nav"])),
                market=KnowledgeLevel(int(row["market"])),
                political=KnowledgeLevel(int(row["political"])),
            )

    def initial_for_node(self, node_id: str, perspective: str = "PLAYER") -> KnowledgeState:
        perspective = perspective.upper()
        node = self.nodes[node_id]
        if perspective == "PLAYER":
            source_value = node["player_default_knowledge"]
        elif perspective == "CROWN":
            source_value = node["known_to_portugal_1497"]
        else:
            raise ValueError("perspective deve ser PLAYER ou CROWN")

        try:
            return self.rules[(perspective, source_value)]
        except KeyError as exc:
            raise KeyError(
                f"Mapeamento de conhecimento ausente para {perspective}/{source_value}"
            ) from exc
