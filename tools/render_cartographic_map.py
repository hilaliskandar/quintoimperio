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

LABEL_OFFSETS = {
    "LIS": (0.9, 1.2),
    "CEU": (0.9, -1.2),
    "FUN": (1.2, -0.5),
    "ARG": (1.2, 0.2),
    "RGR": (1.2, -0.7),
    "ELM": (1.0, 1.0),
    "STO": (1.0, -1.0),
    "CGH": (1.0, -1.1),
    "MOZ": (1.0, -0.7),
    "MOM": (1.0, 1.0),
    "MAL": (1.0, -0.8),
    "KIL": (1.0, -0.9),
    "CAL": (1.0, 0.9),
    "ADE": (1.0, 1.0),
    "HUR": (1.0, 1.0),
    "CAM": (1.0, -1.1),
    "BHA": (1.0, -0.9),
    "MLK": (1.0, -0.7),
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
    ax.set_facecolor("#d9c8a8")

    m = Basemap(
        projection="cyl",
        llcrnrlon=-30,
        urcrnrlon=110,
        llcrnrlat=-40,
        urcrnrlat=50,
        resolution="l",
        ax=ax,
    )
    m.drawmapboundary(fill_color="#c8d2cf", linewidth=0.8)
    m.fillcontinents(color="#d8c39b", lake_color="#c8d2cf")
    m.drawcoastlines(color="#5d5142", linewidth=0.65)
    m.drawparallels(
        range(-40, 51, 10),
        labels=[1, 0, 0, 0],
        linewidth=0.25,
        dashes=[2, 4],
        color="#8b775f",
        fontsize=8,
    )
    m.drawmeridians(
        range(-20, 111, 20),
        labels=[0, 0, 0, 1],
        linewidth=0.25,
        dashes=[2, 4],
        color="#8b775f",
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
            ax.plot(x, y, linewidth=1.35, alpha=0.75, zorder=2)
        else:
            ax.plot(x, y, linewidth=0.8, alpha=0.30, linestyle="--", zorder=1)

    marker_by_group = {"portuguese": "o", "foreign": "s", "navigation": "D"}
    size_by_group = {"portuguese": 36, "foreign": 32, "navigation": 38}
    for group in ("portuguese", "foreign", "navigation"):
        subset = [row for row in drawable if node_group(row) == group]
        if not subset:
            continue
        ax.scatter(
            [float(row["longitude"]) for row in subset],
            [float(row["latitude"]) for row in subset],
            s=size_by_group[group],
            marker=marker_by_group[group],
            zorder=4,
            edgecolors="black",
            linewidths=0.5,
        )

    for row in drawable:
        dx, dy = LABEL_OFFSETS.get(row["node_id"], (1.0, 1.0))
        ax.text(
            float(row["longitude"]) + dx,
            float(row["latitude"]) + dy,
            row["historical_name"],
            fontsize=9.2,
            zorder=5,
            bbox={
                "boxstyle": "round,pad=0.15",
                "facecolor": "#eadbbd",
                "edgecolor": "none",
                "alpha": 0.72,
            },
        )

    subtitle = {
        "REFERENCE": "todos os nós georreferenciados da base",
        "PLAYER": "mundo inicialmente conhecido pelo personagem",
        "CROWN": "mundo inicialmente conhecido pela Coroa",
    }[perspective]
    ax.set_title(
        "Quinto Império — mapa cartográfico de referência v0.2\n"
        f"{subtitle}; costa real e sem fronteiras políticas modernas",
        fontsize=15,
    )

    handles = [
        Line2D([0], [0], marker="o", linestyle="", markeredgecolor="black", label="presença portuguesa / atlântica"),
        Line2D([0], [0], marker="s", linestyle="", markeredgecolor="black", label="porto ou entreposto estrangeiro"),
        Line2D([0], [0], marker="D", linestyle="", markeredgecolor="black", label="marco náutico"),
        Line2D([0], [0], linestyle="-", linewidth=1.35, label="eixo português de exploração"),
        Line2D([0], [0], linestyle="--", linewidth=0.8, alpha=0.5, label="rede preexistente registrada"),
    ]
    ax.legend(handles=handles, loc="lower right", framealpha=0.82, fontsize=9)

    ax.text(
        0.01,
        0.015,
        "Nós sem coordenadas defensáveis permanecem fora. As linhas são arestas do grafo, não trajetos históricos exatos.",
        transform=ax.transAxes,
        fontsize=9,
        va="bottom",
        bbox={
            "boxstyle": "round,pad=0.25",
            "facecolor": "#eadbbd",
            "edgecolor": "none",
            "alpha": 0.80,
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
