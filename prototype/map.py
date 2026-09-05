"""Primeiro mapa 2D: somente nos georreferenciados e arestas conhecidas.

Nao ha costa desenhada nesta versao. O fundo e deliberadamente esquematico ate
que um conjunto cartografico real seja incorporado ao repositorio.
"""

from __future__ import annotations

import argparse

import pygame

from quintoimperio.domain import MapExtent, WorldMapModel


WIDTH = 1200
HEIGHT = 700
PADDING = 50


def render(surface: pygame.Surface, perspective: str = "PLAYER") -> None:
    model = WorldMapModel()
    points = model.visible_nodes(perspective)
    extent = MapExtent.from_points(points)
    point_by_id = {point.node_id: point for point in points}

    surface.fill((235, 239, 241))

    # Grade de referencia. Nao representa costa, fronteira ou rota historica.
    for fraction in (0.25, 0.50, 0.75):
        x = PADDING + round((WIDTH - 2 * PADDING) * fraction)
        y = PADDING + round((HEIGHT - 2 * PADDING) * fraction)
        pygame.draw.line(surface, (210, 215, 218), (x, PADDING), (x, HEIGHT - PADDING), 1)
        pygame.draw.line(surface, (210, 215, 218), (PADDING, y), (WIDTH - PADDING, y), 1)

    for edge in model.visible_routes(perspective):
        origin = point_by_id[edge.origin_node]
        destination = point_by_id[edge.destination_node]
        p1 = model.project(origin, extent, WIDTH, HEIGHT, PADDING)
        p2 = model.project(destination, extent, WIDTH, HEIGHT, PADDING)
        pygame.draw.line(surface, (112, 120, 126), p1, p2, 2)

    font = pygame.font.SysFont(None, 22)
    small = pygame.font.SysFont(None, 17)
    for point in points:
        x, y = model.project(point, extent, WIDTH, HEIGHT, PADDING)
        pygame.draw.circle(surface, (35, 54, 66), (x, y), 6)
        label = font.render(point.label, True, (24, 32, 38))
        surface.blit(label, (x + 9, y - 8))
        knowledge = small.render(point.geo_knowledge.name, True, (75, 83, 88))
        surface.blit(knowledge, (x + 9, y + 11))

    note = small.render(
        "v0.1: coordenadas reais; linhas = arestas conhecidas do grafo; sem costa ate incorporar dado cartografico real",
        True,
        (55, 63, 68),
    )
    surface.blit(note, (PADDING, HEIGHT - 30))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", help="salva PNG e encerra sem abrir janela interativa")
    parser.add_argument("--perspective", choices=("PLAYER", "CROWN"), default="PLAYER")
    args = parser.parse_args()

    pygame.init()
    surface = pygame.Surface((WIDTH, HEIGHT)) if args.output else pygame.display.set_mode((WIDTH, HEIGHT))
    render(surface, args.perspective)

    if args.output:
        pygame.image.save(surface, args.output)
        pygame.quit()
        return

    pygame.display.set_caption("Quinto Imperio — mapa v0.1")
    pygame.display.flip()
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(30)
    pygame.quit()


if __name__ == "__main__":
    main()
