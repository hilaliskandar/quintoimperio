#!/usr/bin/env python3
"""Renderiza mapa cartográfico de referência com costa real.

Este utilitário é deliberadamente separado do runtime Pygame. Ele usa Basemap
como ferramenta de desenvolvimento para produzir uma referência geográfica
reprodutível a partir das coordenadas de ``data/nodes.csv``. Linhas de rota são
arestas do grafo, não reconstruções das derrotas históricas efetivamente
navegadas.

A camada estética de inspiração náutica é totalmente programática. Ela não
substitui nem distorce a geometria da costa, as coordenadas dos nós ou as
arestas do grafo.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Polygon
from mpl_toolkits.basemap import Basemap

from quintoimperio.data.loader import RepositoryData
from quintoimperio.domain import KnowledgeLevel, KnowledgeModel

ROOT = Path(__file__).resolve().parents[1]

OCEAN = "#c8d3cf"
LAND = "#dcc59b"
COAST = "#554b3d"
GRID = "#8b775f"
LABEL_BG = "#efe0bf"
PARCHMENT = "#ead7ad"
PORTUGUESE = "#8b2e2e"
FOREIGN = "#24566b"
NAVIGATION = "#3f3a34"
PREEXISTING = "#6c7777"
RHUMB = "#7f6548"

PROVISIONAL_COORDINATE_NODES = {"MPI", "SOF"}

LABEL_OFFSETS = {
    "LIS": (0.9, 1.5),
    "CEU": (1.0, -1.7),
    "FUN": (1.2, 0.2),
    "ARG": (1.2, 0.5),
    "RGR": (1.1, -0.5),
    "ELM": (1.0, 1.3),
    "STO": (1.0, -1.6),
    "MPI": (1.0, -1.4),
    "CGH": (1.0, -1.4),
    "SOF": (1.0, -1.2),
    "MOZ": (1.1, -1.0),
    "MOM": (1.0, 1.4),
    "MAL": (1.0, -1.6),
    "KIL": (1.0, -1.4),
    "CAL": (1.2, -1.3),
    "ADE": (1.0, 1.1),
    "HUR": (1.0, 1.0),
    "CAM": (1.0, 1.2),
    "BHA": (1.0, 1.1),
    "MLK": (1.0, -1.1),
}


def node_group(row: dict[str, str]) -> str:
    if row["node_type"] == "NAVIGATION_POINT":
        return "navigation"
    if row["political_status"].startswith("PORTUGUESE") or row["political_status"] in {
        "CROWN_CORE",
        "ROYAL_FACTORY",
    }:
        return "portuguese"
    return "foreign"


def visible_node_ids(
    nodes: list[dict[str, str]], perspective: str, knowledge: KnowledgeModel
) -> set[str]:
    if perspective == "REFERENCE":
        return {
            row["node_id"]
            for row in nodes
            if row.get("latitude") and row.get("longitude")
        }
    visible: set[str] = set()
    for row in nodes:
        if not row.get("latitude") or not row.get("longitude"):
            continue
        state = knowledge.initial_for_node(row["node_id"], perspective)
        if state.geo >= KnowledgeLevel.RUMORED:
            visible.add(row["node_id"])
    return visible


def route_visible(route: dict[str, str], perspective: str, visible: set[str]) -> bool:
    if route["origin_node"] not in visible or route["destination_node"] not in visible:
        return False
    if perspective == "REFERENCE":
        return True
    field = "player_knowledge_default" if perspective == "PLAYER" else "crown_knowledge_1497"
    return route[field] != "UNKNOWN"


def draw_rhumb_network(ax: plt.Axes) -> None:
    """Adiciona linhas de rumo decorativas sem alterar geografia.

    As linhas são um motivo gráfico inspirado em cartas portulanas. Não
    representam derrotas, ventos, correntes ou rotas históricas.
    """

    centers = [(-18.0, 6.0), (18.0, -28.0), (66.0, -25.0), (103.0, 5.0)]
    bearings = range(0, 360, 15)
    radius = 180.0
    for lon, lat in centers:
        for bearing in bearings:
            radians = math.radians(bearing)
            x2 = lon + math.sin(radians) * radius
            y2 = lat + math.cos(radians) * radius * 0.55
            ax.plot(
                [lon, x2],
                [lat, y2],
                color=RHUMB,
                linewidth=0.30,
                alpha=0.12,
                zorder=0.35,
                clip_on=True,
            )


def draw_compass_rose(ax: plt.Axes, lon: float = 99.0, lat: float = 39.0, radius: float = 5.5) -> None:
    """Desenha rosa-dos-ventos ornamental em coordenadas do mapa."""

    ax.add_patch(
        Circle(
            (lon, lat),
            radius,
            facecolor=PARCHMENT,
            edgecolor=COAST,
            linewidth=0.8,
            alpha=0.90,
            zorder=7,
        )
    )
    for index, angle_deg in enumerate(range(0, 360, 45)):
        angle = math.radians(angle_deg)
        half_width = math.radians(8 if index % 2 == 0 else 5)
        tip = (lon + math.sin(angle) * radius * 0.88, lat + math.cos(angle) * radius * 0.88)
        left = (
            lon + math.sin(angle - half_width) * radius * 0.24,
            lat + math.cos(angle - half_width) * radius * 0.24,
        )
        right = (
            lon + math.sin(angle + half_width) * radius * 0.24,
            lat + math.cos(angle + half_width) * radius * 0.24,
        )
        fill = PORTUGUESE if index % 2 == 0 else FOREIGN
        ax.add_patch(
            Polygon(
                [left, tip, right, (lon, lat)],
                closed=True,
                facecolor=fill,
                edgecolor=COAST,
                linewidth=0.45,
                alpha=0.88,
                zorder=8,
            )
        )
    ax.add_patch(Circle((lon, lat), radius * 0.12, facecolor=LABEL_BG, edgecolor=COAST, zorder=9))
    ax.text(lon, lat + radius + 0.7, "N", ha="center", va="bottom", fontsize=9, color=COAST, zorder=9)
    ax.text(lon, lat - radius - 0.7, "S", ha="center", va="top", fontsize=9, color=COAST, zorder=9)
    ax.text(lon - radius - 0.7, lat, "O", ha="right", va="center", fontsize=9, color=COAST, zorder=9)
    ax.text(lon + radius + 0.7, lat, "L", ha="left", va="center", fontsize=9, color=COAST, zorder=9)


def render(output: Path, perspective: str) -> None:
    repository = RepositoryData(ROOT)
    nodes = repository.historical("nodes.csv")
    routes = repository.historical("routes.csv")
    knowledge = KnowledgeModel(ROOT)
    visible = visible_node_ids(nodes, perspective, knowledge)

    node_by_id = {row["node_id"]: row for row in nodes}
    drawable = [node_by_id[node_id] for node_id in visible]

    fig = plt.figure(figsize=(16, 9), facecolor=PARCHMENT)
    ax = plt.gca()
    ax.set_facecolor(PARCHMENT)

    m = Basemap(
        projection="cyl",
        llcrnrlon=-30,
        urcrnrlon=110,
        llcrnrlat=-40,
        urcrnrlat=50,
        resolution="l",
        ax=ax,
    )
    m.drawmapboundary(fill_color=OCEAN, linewidth=0.9, color=COAST)
    m.fillcontinents(color=LAND, lake_color=OCEAN)
    m.drawcoastlines(color=COAST, linewidth=0.75)

    draw_rhumb_network(ax)

    m.drawparallels(
        range(-40, 51, 10),
        labels=[1, 0, 0, 0],
        linewidth=0.25,
        dashes=[2, 4],
        color=GRID,
        fontsize=8,
    )
    m.drawmeridians(
        range(-20, 111, 20),
        labels=[0, 0, 0, 1],
        linewidth=0.25,
        dashes=[2, 4],
        color=GRID,
        fontsize=8,
    )

    for route in routes:
        if not route_visible(route, perspective, visible):
            continue
        origin = node_by_id[route["origin_node"]]
        destination = node_by_id[route["destination_node"]]
        x = [float(origin["longitude"]), float(destination["longitude"])]
        y = [float(origin["latitude"]), float(destination["latitude"])]
        if route["route_origin"] == "PORTUGUESE_EXPLORATION":
            ax.plot(x, y, color=PORTUGUESE, linewidth=1.55, alpha=0.88, zorder=2)
        else:
            ax.plot(
                x,
                y,
                color=PREEXISTING,
                linewidth=0.90,
                alpha=0.48,
                linestyle=(0, (4, 4)),
                zorder=1,
            )

    marker_by_group = {"portuguese": "o", "foreign": "s", "navigation": "D"}
    color_by_group = {
        "portuguese": PORTUGUESE,
        "foreign": FOREIGN,
        "navigation": NAVIGATION,
    }
    size_by_group = {"portuguese": 38, "foreign": 34, "navigation": 42}
    for group in ("portuguese", "foreign", "navigation"):
        subset = [row for row in drawable if node_group(row) == group]
        if not subset:
            continue
        ax.scatter(
            [float(row["longitude"]) for row in subset],
            [float(row["latitude"]) for row in subset],
            s=size_by_group[group],
            marker=marker_by_group[group],
            c=color_by_group[group],
            zorder=4,
            edgecolors="black",
            linewidths=0.55,
        )

    # Um segundo contorno identifica âncoras espaciais provisórias sem mover o ponto.
    provisional = [row for row in drawable if row["node_id"] in PROVISIONAL_COORDINATE_NODES]
    if provisional:
        ax.scatter(
            [float(row["longitude"]) for row in provisional],
            [float(row["latitude"]) for row in provisional],
            s=78,
            marker="o",
            facecolors="none",
            edgecolors=PORTUGUESE,
            linewidths=0.8,
            zorder=5,
        )

    for row in drawable:
        longitude = float(row["longitude"])
        latitude = float(row["latitude"])
        dx, dy = LABEL_OFFSETS.get(row["node_id"], (1.0, 1.0))
        suffix = " *" if row["node_id"] in PROVISIONAL_COORDINATE_NODES else ""
        ax.annotate(
            f"{row['historical_name']}{suffix}",
            xy=(longitude, latitude),
            xytext=(longitude + dx, latitude + dy),
            fontsize=9.1,
            zorder=6,
            arrowprops={
                "arrowstyle": "-",
                "linewidth": 0.45,
                "color": COAST,
                "alpha": 0.55,
                "shrinkA": 0,
                "shrinkB": 4,
            },
            bbox={
                "boxstyle": "round,pad=0.16",
                "facecolor": LABEL_BG,
                "edgecolor": "none",
                "alpha": 0.88,
            },
        )

    # Grandes rótulos são decorativos e não representam fronteiras políticas.
    ax.text(18, 17, "Á F R I C A", fontsize=15, color=COAST, alpha=0.55, ha="center", zorder=0.6)
    ax.text(83, 30, "Á S I A", fontsize=14, color=COAST, alpha=0.48, ha="center", zorder=0.6)
    ax.text(-8, -16, "O C E A N O   A T L Â N T I C O", fontsize=10, color=COAST, alpha=0.48, ha="center", zorder=0.6)
    ax.text(66, -18, "O C E A N O   Í N D I C O", fontsize=10, color=COAST, alpha=0.48, ha="center", zorder=0.6)

    draw_compass_rose(ax)

    subtitle = {
        "REFERENCE": "todos os nós georreferenciados da base",
        "PLAYER": "mundo inicialmente conhecido pelo personagem",
        "CROWN": "mundo inicialmente conhecido pela Coroa",
    }[perspective]
    ax.set_title(
        "Quinto Império — referência cartográfica programática v0.3\n"
        f"{subtitle}; costa real, estética náutica procedural e sem fronteiras políticas modernas",
        fontsize=15,
        color=COAST,
        pad=12,
    )

    handles = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="none",
            markerfacecolor=PORTUGUESE,
            markeredgecolor="black",
            label="presença portuguesa / atlântica",
        ),
        Line2D(
            [0],
            [0],
            marker="s",
            color="none",
            markerfacecolor=FOREIGN,
            markeredgecolor="black",
            label="porto ou entreposto estrangeiro",
        ),
        Line2D(
            [0],
            [0],
            marker="D",
            color="none",
            markerfacecolor=NAVIGATION,
            markeredgecolor="black",
            label="marco náutico",
        ),
        Line2D([0], [0], color=PORTUGUESE, linewidth=1.55, label="eixo português de exploração"),
        Line2D(
            [0],
            [0],
            color=PREEXISTING,
            linestyle=(0, (4, 4)),
            linewidth=0.9,
            label="rede preexistente registrada",
        ),
        Line2D(
            [0],
            [0],
            marker="o",
            color="none",
            markerfacecolor="none",
            markeredgecolor=PORTUGUESE,
            label="* âncora espacial provisória",
        ),
    ]
    legend = ax.legend(handles=handles, loc="lower right", framealpha=0.90, fontsize=8.8)
    legend.get_frame().set_facecolor(LABEL_BG)
    legend.get_frame().set_edgecolor(COAST)

    ax.text(
        0.01,
        0.015,
        "* Mpinda/Soyo ≈ (-6.1981, 12.3933) e Sofala ≈ (-20.1562, 34.7383) são âncoras cartográficas provisórias. "
        "Arestas são relações do grafo e não trajetos marítimos históricos exatos.",
        transform=ax.transAxes,
        fontsize=8.5,
        va="bottom",
        bbox={
            "boxstyle": "round,pad=0.25",
            "facecolor": LABEL_BG,
            "edgecolor": "none",
            "alpha": 0.88,
        },
    )

    for spine in ax.spines.values():
        spine.set_linewidth(1.4)
        spine.set_edgecolor(COAST)

    output.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output, dpi=220, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "build" / "map-reference.png")
    parser.add_argument(
        "--perspective",
        choices=("REFERENCE", "PLAYER", "CROWN"),
        default="REFERENCE",
    )
    args = parser.parse_args()
    render(args.output, args.perspective)
    print(args.output)


if __name__ == "__main__":
    main()
