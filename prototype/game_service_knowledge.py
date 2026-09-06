#!/usr/bin/env python3
"""Interface experimental pós-MVP para evidência e conhecimento de serviços."""

from __future__ import annotations

import argparse

import pygame

from quintoimperio.domain import PortServiceKind, ServiceKnowledgeStatus

try:
    from prototype.game import INK, LINE, MAP_RECT, MUTED, PANEL, HEIGHT, WIDTH
    from prototype.game_m6 import M6HistoricalCampaignPrototype
except ModuleNotFoundError:
    from game import INK, LINE, MAP_RECT, MUTED, PANEL, HEIGHT, WIDTH
    from game_m6 import M6HistoricalCampaignPrototype


class ServiceKnowledgePrototype(M6HistoricalCampaignPrototype):
    """Acrescenta apenas leitura epistêmica; não altera serviços materiais."""

    def service_label(self, service: PortServiceKind) -> str:
        view = self.session.service_view(self.state, service)
        if view.knowledge_status is ServiceKnowledgeStatus.UNASSESSED:
            return "não avaliado pelo jogador"
        if view.knowledge_status is ServiceKnowledgeStatus.EVIDENCE_INDETERMINATE:
            return "evidência histórica indeterminada"
        assert view.revealed_availability is not None
        return f"documentado: {view.revealed_availability.value}"

    def _draw_service_evidence(self, surface: pygame.Surface) -> None:
        rect = pygame.Rect(MAP_RECT.left + 10, MAP_RECT.top + 76, 365, 64)
        pygame.draw.rect(surface, PANEL, rect, border_radius=5)
        pygame.draw.rect(surface, LINE, rect, width=1, border_radius=5)
        tiny = pygame.font.SysFont("monospace", 11)
        self._draw_text(surface, tiny, "Serviços — estado da evidência", (rect.x + 10, rect.y + 8), INK)
        self._draw_text(
            surface,
            tiny,
            "provisões: " + self.service_label(PortServiceKind.PROVISIONS),
            (rect.x + 10, rect.y + 25),
            MUTED,
        )
        self._draw_text(
            surface,
            tiny,
            "reparo: " + self.service_label(PortServiceKind.REPAIR),
            (rect.x + 10, rect.y + 42),
            MUTED,
        )

    def render(self, surface: pygame.Surface) -> None:
        super().render(surface)
        self._draw_service_evidence(surface)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", help="renderiza um quadro PNG e encerra")
    args = parser.parse_args()
    pygame.init()
    surface = pygame.Surface((WIDTH, HEIGHT)) if args.output else pygame.display.set_mode((WIDTH, HEIGHT))
    app = ServiceKnowledgePrototype()
    app.render(surface)
    if args.output:
        pygame.image.save(surface, args.output)
        pygame.quit()
        return
    pygame.display.set_caption("Quinto Império — evidência de serviços")
    pygame.display.flip()
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                app.handle_click(event.pos)
                app.render(surface)
                pygame.display.flip()
        clock.tick(30)
    pygame.quit()


if __name__ == "__main__":
    main()
