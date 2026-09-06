#!/usr/bin/env python3
"""Interface M6: save/load versionado em um único slot local.

A persistência registra apenas estado do domínio e seed. Seleções visuais,
histórico curto e confirmação modal continuam efêmeros e são reiniciados após
um carregamento.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pygame

from quintoimperio.domain import CampaignPersistence

try:
    from prototype.game import BG, BUTTON, HEIGHT, INK, LINE, MUTED, SEED, WIDTH, ClickTarget
    from prototype.game_m5 import M5HistoricalCampaignPrototype
except ModuleNotFoundError:
    from game import BG, BUTTON, HEIGHT, INK, LINE, MUTED, SEED, WIDTH, ClickTarget
    from game_m5 import M5HistoricalCampaignPrototype


DEFAULT_SAVE_PATH = Path("quintoimperio-save.json")


class M6HistoricalCampaignPrototype(M5HistoricalCampaignPrototype):
    """Interface v0.2 acrescida apenas do comando persistente de slot único."""

    def __init__(self, save_path: str | Path = DEFAULT_SAVE_PATH) -> None:
        super().__init__()
        self.persistence = CampaignPersistence()
        self.save_path = Path(save_path)
        self.session_seed = SEED

    def save_slot(self) -> None:
        self.persistence.save_file(
            self.save_path,
            self.state,
            seed=self.session_seed,
        )
        self.message = f"Campanha salva em {self.save_path.name}."
        self._remember()

    def load_slot(self) -> None:
        if not self.save_path.exists():
            self.message = f"Nenhum save encontrado em {self.save_path.name}."
            self._remember()
            return
        loaded = self.persistence.load_file(self.save_path)
        self.state = loaded.state
        self.session_seed = loaded.seed
        self.selected_good = None
        self.selected_route = None
        self.pending_travel_route = None
        self.action_history = []
        self.message = (
            f"Campanha carregada de {self.save_path.name}; "
            f"schema v{loaded.schema_version}."
        )
        self._remember()

    def _draw_persistence_controls(self, surface: pygame.Surface) -> None:
        small = pygame.font.SysFont("sans", 13)
        micro = pygame.font.SysFont("monospace", 11)
        save_rect = pygame.Rect(620, 18, 104, 30)
        load_rect = pygame.Rect(734, 18, 112, 30)
        pygame.draw.rect(surface, BUTTON, save_rect, border_radius=4)
        pygame.draw.rect(surface, BG, load_rect, border_radius=4)
        pygame.draw.rect(surface, LINE, load_rect, width=1, border_radius=4)
        self._draw_text(surface, small, "Salvar [S]", (save_rect.x + 19, save_rect.y + 6), INK)
        self._draw_text(surface, small, "Carregar [L]", (load_rect.x + 15, load_rect.y + 6), INK)
        self.targets.append(ClickTarget(save_rect, "action", "save_slot"))
        self.targets.append(ClickTarget(load_rect, "action", "load_slot"))
        self._draw_text(
            surface,
            micro,
            f"slot: {self.save_path.name}",
            (620, 52),
            MUTED,
        )

    def render(self, surface: pygame.Surface) -> None:
        super().render(surface)
        self._draw_persistence_controls(surface)

    def handle_click(self, pos: tuple[int, int]) -> None:
        for target in reversed(self.targets):
            if not target.rect.collidepoint(pos):
                continue
            if target.kind == "action" and target.value == "save_slot":
                self.save_slot()
                return
            if target.kind == "action" and target.value == "load_slot":
                self.load_slot()
                return
        super().handle_click(pos)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", help="renderiza um quadro PNG e encerra")
    parser.add_argument(
        "--save-path",
        default=str(DEFAULT_SAVE_PATH),
        help="caminho do slot único de save",
    )
    parser.add_argument(
        "--roundtrip-smoke",
        action="store_true",
        help="salva, altera a sessão em memória e carrega novamente o mesmo estado",
    )
    args = parser.parse_args()

    pygame.init()
    surface = (
        pygame.Surface((WIDTH, HEIGHT))
        if args.output or args.roundtrip_smoke
        else pygame.display.set_mode((WIDTH, HEIGHT))
    )
    app = M6HistoricalCampaignPrototype(args.save_path)

    if args.roundtrip_smoke:
        original = app.state
        app.save_slot()
        if app.session.in_predeparture_phase(app.state):
            app.state = app.session.wait_for_guided_departure(app.state).state_after
        app.state = app.session.execute_voyage(
            app.state,
            app.session.plan_current_leg(app.state, seed=app.session_seed),
        )
        if app.state == original:
            raise RuntimeError("Smoke M6 não alterou o estado antes do load")
        app.load_slot()
        if app.state != original:
            raise RuntimeError("Round-trip M6 não restaurou o estado original")
        app.render(surface)
        print(app.message)
        if args.output:
            pygame.image.save(surface, args.output)
        pygame.quit()
        return

    app.render(surface)
    if args.output:
        pygame.image.save(surface, args.output)
        pygame.quit()
        return

    pygame.display.set_caption("Quinto Império — interface histórica com save M6")
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if app.pending_travel_route:
                        app.cancel_travel()
                        app.render(surface)
                        pygame.display.flip()
                    else:
                        running = False
                elif event.key == pygame.K_r:
                    app.__init__(app.save_path)
                    app.render(surface)
                    pygame.display.flip()
                elif event.key == pygame.K_s:
                    app.save_slot()
                    app.render(surface)
                    pygame.display.flip()
                elif event.key == pygame.K_l:
                    app.load_slot()
                    app.render(surface)
                    pygame.display.flip()
        clock.tick(30)
    pygame.quit()


if __name__ == "__main__":
    main()
