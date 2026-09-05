"""Modelo cartografico minimo baseado somente em coordenadas reais da base."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from quintoimperio.data.loader import RepositoryData

from .knowledge import KnowledgeLevel, KnowledgeModel


@dataclass(frozen=True)
class MapPoint:
    node_id: str
    label: str
    latitude: float
    longitude: float
    geo_knowledge: KnowledgeLevel


@dataclass(frozen=True)
class MapEdge:
    route_id: str
    origin_node: str
    destination_node: str


@dataclass(frozen=True)
class MapExtent:
    min_longitude: float
    max_longitude: float
    min_latitude: float
    max_latitude: float

    @classmethod
    def from_points(
        cls, points: list[MapPoint], padding_fraction: float = 0.08
    ) -> "MapExtent":
        if not points:
            raise ValueError("Nao ha pontos visiveis para definir a extensao do mapa")
        if padding_fraction < 0:
            raise ValueError("padding_fraction nao pode ser negativo")

        min_lon = min(point.longitude for point in points)
        max_lon = max(point.longitude for point in points)
        min_lat = min(point.latitude for point in points)
        max_lat = max(point.latitude for point in points)

        lon_span = max(max_lon - min_lon, 1.0)
        lat_span = max(max_lat - min_lat, 1.0)
        lon_padding = lon_span * padding_fraction
        lat_padding = lat_span * padding_fraction

        return cls(
            min_longitude=max(-180.0, min_lon - lon_padding),
            max_longitude=min(180.0, max_lon + lon_padding),
            min_latitude=max(-90.0, min_lat - lat_padding),
            max_latitude=min(90.0, max_lat + lat_padding),
        )


class WorldMapModel:
    """Seleciona e projeta o mundo conhecido sem fabricar geografia.

    A projecao v0.1 e equiretangular e serve somente a interface. Coordenadas
    sao lidas diretamente de ``nodes.csv``; nos sem coordenadas nao sao
    desenhados. Linhas de rota representam arestas do grafo, nao o percurso
    historico efetivamente navegado.
    """

    def __init__(self, root: Path | None = None) -> None:
        repository = RepositoryData(root)
        self.root = repository.root
        self.nodes = {
            row["node_id"]: row for row in repository.historical("nodes.csv")
        }
        self.routes = repository.historical("routes.csv")
        self.knowledge = KnowledgeModel(self.root)

    def point_for_node(
        self, node_id: str, perspective: str = "PLAYER"
    ) -> MapPoint | None:
        node = self.nodes[node_id]
        if not node.get("latitude") or not node.get("longitude"):
            return None
        state = self.knowledge.initial_for_node(node_id, perspective)
        return MapPoint(
            node_id=node_id,
            label=node["historical_name"],
            latitude=float(node["latitude"]),
            longitude=float(node["longitude"]),
            geo_knowledge=state.geo,
        )

    def visible_nodes(
        self,
        perspective: str = "PLAYER",
        minimum: KnowledgeLevel = KnowledgeLevel.RUMORED,
    ) -> list[MapPoint]:
        visible: list[MapPoint] = []
        for node_id in self.nodes:
            point = self.point_for_node(node_id, perspective)
            if point is None:
                continue
            if point.geo_knowledge >= minimum:
                visible.append(point)
        return visible

    def visible_routes(self, perspective: str = "PLAYER") -> list[MapEdge]:
        perspective = perspective.upper()
        if perspective not in {"PLAYER", "CROWN"}:
            raise ValueError("perspective deve ser PLAYER ou CROWN")
        visible_ids = {point.node_id for point in self.visible_nodes(perspective)}
        field = (
            "player_knowledge_default"
            if perspective == "PLAYER"
            else "crown_knowledge_1497"
        )
        edges: list[MapEdge] = []
        for route in self.routes:
            if route[field] == "UNKNOWN":
                continue
            if (
                route["origin_node"] not in visible_ids
                or route["destination_node"] not in visible_ids
            ):
                continue
            edges.append(
                MapEdge(
                    route_id=route["route_id"],
                    origin_node=route["origin_node"],
                    destination_node=route["destination_node"],
                )
            )
        return edges

    @staticmethod
    def project(
        point: MapPoint,
        extent: MapExtent,
        width: int,
        height: int,
        pixel_padding: int = 40,
    ) -> tuple[int, int]:
        if width <= pixel_padding * 2 or height <= pixel_padding * 2:
            raise ValueError("Dimensoes do mapa insuficientes para o padding solicitado")

        lon_span = extent.max_longitude - extent.min_longitude
        lat_span = extent.max_latitude - extent.min_latitude
        if lon_span <= 0 or lat_span <= 0:
            raise ValueError("Extensao cartografica invalida")

        usable_width = width - 2 * pixel_padding
        usable_height = height - 2 * pixel_padding
        x_ratio = (point.longitude - extent.min_longitude) / lon_span
        y_ratio = (extent.max_latitude - point.latitude) / lat_span
        x = pixel_padding + round(x_ratio * usable_width)
        y = pixel_padding + round(y_ratio * usable_height)
        return x, y
