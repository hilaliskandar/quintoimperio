#!/usr/bin/env python3
"""Interface v0.2 da vertical slice histórica do MVP.

A camada M5 reorganiza feedback e confirmação sem introduzir regras de negócio.
Todo estado jogável continua pertencendo a ``HistoricalCampaignModel`` e aos
modelos compostos de domínio; Pygame apenas apresenta esse estado e envia
comandos já existentes.
"""

from __future__ import annotations

import argparse

import pygame

try:
    from prototype.game import (
        BAD,
        BG,
        BUTTON,
        HEIGHT,
        INK,
        LINE,
        MAP_RECT,
        MUTED,
        PANEL,
        SEED,
        WIDTH,
        ClickTarget,
    )
    from prototype.historical_campaign import HistoricalCampaignPrototype
except ModuleNotFoundError:
    from game import (
        BAD,
        BG,
        BUTTON,
        HEIGHT,
        INK,
        LINE,
        MAP_RECT,
        MUTED,
        PANEL,
        SEED,
        WIDTH,
        ClickTarget,
    )
    from historical_campaign import HistoricalCampaignPrototype


BLOCKER_LABELS = {
    "HISTORICAL_DEPARTURE_NOT_REACHED": "aguarde a data histórica de partida",
    "HISTORICAL_STOP_NOT_RELEASED": "a permanência histórica ainda não terminou",
    "STRATEGIC_AGGREGATE_NOT_EXECUTABLE": "conexão estratégica não executável",
    "ROUTE_KNOWLEDGE_INSUFFICIENT": "conhecimento de navegação insuficiente",
    "INSUFFICIENT_PROVISIONS": "provisões insuficientes",
    "VESSEL_CONDITION_TOO_LOW": "condição do navio insuficiente",
    "PILOT_NOT_AVAILABLE": "piloto não disponível",
    "PILOT_ROUTE_NOT_AUTHORIZED": "piloto não habilitado para esta rota",
    "NO_NAVIGATION_BASIS": "não há base de navegação suficiente",
    "PORT_ACCESS_NEGOTIATION_REQUIRED": "é preciso negociar acesso comercial",
    "MARKET_KNOWLEDGE_NOT_OPERATIONAL": "conhecimento do mercado insuficiente",
    "NO_INFORMATION_OPPORTUNITY": "não há nova informação disponível",
}


class M5HistoricalCampaignPrototype(HistoricalCampaignPrototype):
    """Interface v0.2: hierarquia de campanha, feedback curto e confirmação."""

    HISTORY_LIMIT = 4

    def __init__(self) -> None:
        super().__init__()
        self.pending_travel_route: str | None = None
        self.action_history: list[str] = [self.message]

    @staticmethod
    def friendly_reasons(reasons: tuple[str, ...]) -> str:
        return "; ".join(BLOCKER_LABELS.get(reason, reason.replace("_", " ").lower()) for reason in reasons)

    def _remember(self) -> None:
        if not self.message:
            return
        if self.action_history and self.action_history[-1] == self.message:
            return
        self.action_history.append(self.message)
        del self.action_history[:-self.HISTORY_LIMIT]

    def campaign_status(self):
        """Retorna a projeção M4; não mantém estado paralelo de objetivos."""
        return self.session.progress(self.state)

    def travel_selected(self) -> None:
        """Primeiro comando de viagem apenas solicita confirmação."""
        if not self.selected_route:
            self.message = "Selecione uma rota antes de viajar."
            self._remember()
            return
        plan = self.plan_for_route(self.selected_route)
        if not plan.feasible:
            self.pending_travel_route = None
            self.message = "Viagem bloqueada: " + self.friendly_reasons(plan.blockers)
            self._remember()
            return
        self.pending_travel_route = self.selected_route
        destination = self.session.routes[self.selected_route]["destination_node"]
        self.message = f"Confirmar viagem para {destination} ({plan.travel_days} dias)."
        self._remember()

    def confirm_travel(self) -> None:
        if not self.pending_travel_route:
            self.message = "Não há viagem aguardando confirmação."
            self._remember()
            return
        self.selected_route = self.pending_travel_route
        self.pending_travel_route = None
        # Chama a implementação executora herdada da interface base, evitando a
        # sobrescrita acima que apenas abre a confirmação.
        super().travel_selected()
        self._remember()

    def cancel_travel(self) -> None:
        if self.pending_travel_route:
            self.message = "Viagem cancelada antes da partida."
        self.pending_travel_route = None
        self._remember()

    def _draw_campaign_strip(self, surface: pygame.Surface) -> None:
        progress = self.campaign_status()
        strip = pygame.Rect(MAP_RECT.left + 10, MAP_RECT.top + 10, MAP_RECT.width - 20, 58)
        pygame.draw.rect(surface, PANEL, strip, border_radius=5)
        pygame.draw.rect(surface, LINE, strip, width=1, border_radius=5)
        small = pygame.font.SysFont("sans", 15, bold=True)
        micro = pygame.font.SysFont("monospace", 12)
        objective = (
            "Campanha concluída em Calecute"
            if progress.completed
            else f"Objetivo atual: {progress.current_objective}"
        )
        self._draw_text(surface, small, objective, (strip.x + 12, strip.y + 9), INK)
        completed = sum(1 for item in progress.milestones if item.completed)
        mode = self.state.chronology_mode.value
        mode_note = "trajetória histórica" if mode == "GUIDED" else "trajetória divergente"
        self._draw_text(
            surface,
            micro,
            f"Progresso {completed}/{len(progress.milestones)} | {mode} — {mode_note}",
            (strip.x + 12, strip.y + 34),
            MUTED if mode == "GUIDED" else BAD,
        )

    def _draw_history(self, surface: pygame.Surface) -> None:
        rect = pygame.Rect(MAP_RECT.left + 10, MAP_RECT.bottom - 92, MAP_RECT.width - 20, 78)
        pygame.draw.rect(surface, BG, rect, border_radius=4)
        pygame.draw.rect(surface, LINE, rect, width=1, border_radius=4)
        tiny = pygame.font.SysFont("monospace", 11)
        self._draw_text(surface, tiny, "Acontecimentos recentes", (rect.x + 10, rect.y + 7), MUTED)
        y = rect.y + 23
        for entry in self.action_history[-3:]:
            lines = self._wrap(tiny, entry, rect.width - 24)
            if not lines:
                continue
            self._draw_text(surface, tiny, "• " + lines[0], (rect.x + 10, y), INK)
            y += 16

    def _draw_travel_confirmation(self, surface: pygame.Surface) -> None:
        if not self.pending_travel_route:
            return
        route_id = self.pending_travel_route
        plan = self.plan_for_route(route_id)
        route = self.session.routes[route_id]
        rect = pygame.Rect(MAP_RECT.centerx - 210, MAP_RECT.centery - 88, 420, 176)
        pygame.draw.rect(surface, PANEL, rect, border_radius=7)
        pygame.draw.rect(surface, LINE, rect, width=2, border_radius=7)
        body = pygame.font.SysFont("serif", 20, bold=True)
        small = pygame.font.SysFont("sans", 14)
        micro = pygame.font.SysFont("monospace", 12)
        self._draw_text(surface, body, "Confirmar partida", (rect.x + 18, rect.y + 15))
        self._draw_text(
            surface,
            small,
            f"{route_id}: {self.state.vessel.location_node} → {route['destination_node']}",
            (rect.x + 18, rect.y + 49),
        )
        basis = plan.navigation_basis.value if plan.navigation_basis else "sem base"
        self._draw_text(surface, micro, f"Duração prevista: {plan.travel_days} dias | base: {basis}", (rect.x + 18, rect.y + 76), MUTED)
        confirm = pygame.Rect(rect.x + 18, rect.bottom - 48, 170, 30)
        cancel = pygame.Rect(rect.right - 188, rect.bottom - 48, 170, 30)
        pygame.draw.rect(surface, BUTTON, confirm, border_radius=4)
        pygame.draw.rect(surface, BG, cancel, border_radius=4)
        pygame.draw.rect(surface, LINE, cancel, width=1, border_radius=4)
        self._draw_text(surface, small, "Confirmar viagem", (confirm.x + 22, confirm.y + 6))
        self._draw_text(surface, small, "Cancelar", (cancel.x + 51, cancel.y + 6))
        self.targets.append(ClickTarget(confirm, "action", "confirm_travel"))
        self.targets.append(ClickTarget(cancel, "action", "cancel_travel"))

    def render(self, surface: pygame.Surface) -> None:
        super().render(surface)
        self._draw_campaign_strip(surface)
        self._draw_history(surface)
        self._draw_travel_confirmation(surface)

    def handle_click(self, pos: tuple[int, int]) -> None:
        for target in reversed(self.targets):
            if not target.rect.collidepoint(pos):
                continue
            if target.kind == "action" and target.value == "confirm_travel":
                self.confirm_travel()
                return
            if target.kind == "action" and target.value == "cancel_travel":
                self.cancel_travel()
                return
            if target.kind == "action" and target.value == "travel":
                self.travel_selected()
                return
        before = self.message
        super().handle_click(pos)
        if self.message != before:
            self._remember()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", help="renderiza um quadro PNG e encerra")
    parser.add_argument(
        "--campaign-smoke",
        action="store_true",
        help="executa a campanha histórica e renderiza o estado final v0.2",
    )
    args = parser.parse_args()

    pygame.init()
    surface = (
        pygame.Surface((WIDTH, HEIGHT))
        if args.output or args.campaign_smoke
        else pygame.display.set_mode((WIDTH, HEIGHT))
    )
    app = M5HistoricalCampaignPrototype()

    if args.campaign_smoke:
        # O smoke M1–M4 usa as ações herdadas diretamente; a confirmação M5 é
        # exercitada em teste próprio para não transformar o roteiro automático
        # em um driver de cliques.
        HistoricalCampaignPrototype.run_scripted_campaign(app)
        app._remember()
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

    pygame.display.set_caption("Quinto Império — interface histórica v0.2")
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
                    app.__init__()
                    app.render(surface)
                    pygame.display.flip()
        clock.tick(30)
    pygame.quit()


if __name__ == "__main__":
    main()
