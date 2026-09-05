"""Conhecimento de rota separado do conhecimento de nós e mercados."""

from __future__ import annotations

from pathlib import Path

from quintoimperio.data.loader import RepositoryData

from .knowledge import KnowledgeLevel


class RouteKnowledgeModel:
    """Converte os campos textuais de ``routes.csv`` em nível náutico.

    O mapeamento pertence à simulação e fica em
    ``simulation/route_knowledge_rules.csv``. Conhecer um porto não implica
    conhecer operacionalmente qualquer rota que parte dele.
    """

    def __init__(self, root: Path | None = None) -> None:
        repository = RepositoryData(root)
        self.root = repository.root
        self.routes = {
            row["route_id"]: row for row in repository.historical("routes.csv")
        }
        self.rules: dict[tuple[str, str], KnowledgeLevel] = {}
        for row in repository.simulation("route_knowledge_rules.csv"):
            self.rules[(row["perspective"], row["source_value"])] = KnowledgeLevel(
                int(row["nav"])
            )

    def initial_for_route(
        self, route_id: str, perspective: str = "PLAYER"
    ) -> KnowledgeLevel:
        perspective = perspective.upper()
        route = self.routes[route_id]
        if perspective == "PLAYER":
            source_value = route["player_knowledge_default"]
        elif perspective == "CROWN":
            source_value = route["crown_knowledge_1497"]
        else:
            raise ValueError("perspective deve ser PLAYER ou CROWN")

        try:
            return self.rules[(perspective, source_value)]
        except KeyError as exc:
            raise KeyError(
                f"Mapeamento de conhecimento de rota ausente para {perspective}/{source_value}"
            ) from exc
