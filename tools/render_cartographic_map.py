#!/usr/bin/env python3
"""Renderiza mapa cartográfico de referência com costa real.

Este utilitário é deliberadamente separado do runtime Pygame. Ele usa Basemap
como ferramenta de desenvolvimento para produzir uma referência geográfica
reprodutível a partir das coordenadas de ``data/nodes.csv``. Linhas de rota são
arestas do grafo, não reconstruções das derrotas históricas efetivamente
navegadas.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from mpl_toolkits.basemap import Basemap

from quintoimperio.data.loader import RepositoryData
from quintoimperio.domain import KnowledgeLevel, KnowledgeModel

ROOT = Path(__file__).resolve().parents[1]

OCEAN = "#c8d3cf"
LAND = "#dcc59b"
COAST = "#554b3d"
GRID = "#8b775f"
LABEL_BG = "#efe0bf"
PORTUGUESE = "#8b2e2e"
FOREIGN = "#24566b"
NAVIGATION = "#3f3a34"
PREEXISTING = "#6c7777"

LABEL_OFFSETS = {
    "LIS": (0.9, 1.5),
    "CEU": (1.0, -1.7),
    "FUN": (1.2, 0.2),
    "ARG": (1.2, 0.5),
    "RGR": (1.1, -0.5),
    "ELM": (1.0, 1.3),
    "STO": (1.0, -1.6),
    "CGH": (1.0, -1.4),
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


def render(output: Path, perspective: str) -> None:
    repository = RepositoryData(ROOT)
    nodes = repository.historical("nodes.csv")
    routes = repository.historical("routes.csv")
    knowledge = KnowledgeModel(ROOT)
    visible = visible_node_ids(nodes, perspective, knowledge)

    node_by_id = {row["node_id"]: row for row in nodes}
    drawable = [node_by_id[node_id] for node_id in visible]

    fig = plt.figure(figsize=(16, 9))
    ax = plt.gca()

    m = Basemap(
        projection="cyl",
        llcrnrlon=-30,
        urcrnrlon=110,
        llcrnrlat=-40,
        urcrnrlat=50,
        resolution="l",
        ax=ax,
    )
    m.drawmapboundary(fill_color=OCEAN, linewidth=0.8)
    m.fillcontinents(color=LAND, lake_color=OCEAN)
    m.drawcoastlines(color=COAST, linewidth=0.75)
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
            ax.plot(x, y, color=PORTUGUESE, linewidth=1.5, alpha=0.82, zorder=2)
        else:
            ax.plot(
                x,
                y,
                color=PREEXISTING,
                linewidth=0.85,
                alpha=0.40,
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

    for row in drawable:
        longitude = float(row["longitude"])
        latitude = float(row["latitude"])
        dx, dy = LABEL_OFFSETS.get(row["node_id"], (1.0, 1.0))
        ax.annotate(
            row["historical_name"],
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
                "alpha": 0.82,
            },
        )

    subtitle = {
        "REFERENCE": "todos os nós georreferenciados da base",
        "PLAYER": "mundo inicialmente conhecido pelo personagem",
        "CROWN": "mundo inicialmente conhecido pela Coroa",
    }[perspective]
    ax.set_title(
        "Quinto Império — referência cartográfica programática v0.2\n"
        f"{subtitle}; costa real e sem fronteiras políticas modernas",
        fontsize=15,
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
        Line2D([0], [0], color=PORTUGUESE, linewidth=1.5, label="eixo português de exploração"),
        Line2D(
            [0],
            [0],
            color=PREEXISTING,
            linestyle=(0, (4, 4)),
            linewidth=0.9,
            label="rede preexistente registrada",
        ),
    ]
    ax.legend(handles=handles, loc="lower right", framealpha=0.88, fontsize=9)

    ax.text(
        0.01,
        0.015,
        "Nós sem coordenadas defensáveis permanecem fora. Arestas não representam trajetos marítimos exatos.",
        transform=ax.transAxes,
        fontsize=9,
        va="bottom",
        bbox={
            "boxstyle": "round,pad=0.25",
            "facecolor": LABEL_BG,
            "edgecolor": "none",
            "alpha": 0.85,
        },
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output, dpi=220, bbox_inches="tight")
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
