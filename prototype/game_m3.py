#!/usr/bin/env python3
"""Interface M3: comércio operacional dentro da campanha do MVP.

Esta camada reutiliza a interface v0.1 e acrescenta apenas os controles mínimos
necessários ao gate M3: quantidade selecionável, leitura de capacidade livre e
inventário da mercadoria selecionada, além de mensagens curtas para bloqueios.
Valores de capital, capacidade, quantidade e preço permanecem índices abstratos
de simulação e não representam unidades monetárias ou físicas históricas.
"""

from __future__ import annotations

import argparse

import pygame

try:
    from prototype.game import (
        BUTTON,
        BUTTON_DISABLED,
        INK,
        LINE,
        MAP_RECT,
        MUTED,
        WIDTH,
        HEIGHT,
        ClickTarget,
        PlayablePrototype,
    )
except ModuleNotFoundError:
    from game import (
        BUTTON,
        BUTTON_DISABLED,
        INK,
        LINE,
        MAP_RECT,
        MUTED,
        WIDTH,
        HEIGHT,
        ClickTarget,
        PlayablePrototype,
    )


REASON_LABELS = {
    "MARKET_KNOWLEDGE_NOT_OPERATIONAL": "conhecimento do mercado ainda insuficiente",
    "PORT_ACCESS_NEGOTIATION_REQUIRED": "acesso comercial exige negociação",
    "PORT_ACCESS_RESTRICTED": "acesso comercial restrito neste porto",
    "PORT_HAS_NO_COMMERCIAL_ACCESS": "este ponto não possui acesso comercial",
    "PORT_ACCESS_UNKNOWN": "condição de acesso comercial ainda desconhecida",
    "PORT_ACCESS_NOT_GRANTED": "acesso comercial ainda não concedido",
    "GOOD_NOT_DOCUMENTED_IN_MARKET": "mercadoria não documentada neste mercado",
    "GOOD_RESTRICTED_BY_HISTORICAL_ACCESS_REGIME": "mercadoria sujeita a restrição específica",
    "INSUFFICIENT_CARGO_CAPACITY": "capacidade de carga insuficiente",
    "INSUFFICIENT_CAPITAL": "capital insuficiente",
    "INSUFFICIENT_INVENTORY": "quantidade em posse insuficiente",
    "QUANTITY_MUST_BE_POSITIVE": "quantidade deve ser positiva",
}


class M3PlayablePrototype(PlayablePrototype):
    """Extensão deliberadamente pequena da interface v0.1 para o gate M3."""

    MIN_TRADE_QUANTITY = 1.0
    MAX_TRADE_QUANTITY = 20.0

    def __init__(self, scenario: str = "HISTORICAL") -> None:
        super().__init__(scenario)
        self.trade_quantity = self.MIN_TRADE_QUANTITY
        self.trade_overlay_rect = pygame.Rect(
            MAP_RECT.right - 225,
            MAP_RECT.bottom - 105,
            208,
            88,
        )

    def reset(self, scenario: str | None = None) -> None:
        super().reset(scenario)
        self.trade_quantity = self.MIN_TRADE_QUANTITY

    @staticmethod
    def _friendly_reasons(reasons: tuple[str, ...]) -> str:
        return "; ".join(REASON_LABELS.get(reason, reason) for reason in reasons)

    def adjust_trade_quantity(self, delta: float) -> None:
        self.trade_quantity = min(
            self.MAX_TRADE_QUANTITY,
            max(self.MIN_TRADE_QUANTITY, self.trade_quantity + delta),
        )
        self.message = f"Quantidade comercial selecionada: {self.trade_quantity:g}."

    def buy_selected(self) -> None:
        if not self.selected_good:
            self.message = "Nenhuma mercadoria selecionada."
            return
        result = self.session.buy(
            self.state,
            self.selected_good,
            self.trade_quantity,
            seed=1498,
        )
        if result.executed:
            self.state = result.state_after
            self.message = (
                f"Compra: {self.trade_quantity:g} {self.selected_good}; "
                f"valor índice {result.trade_result.total_value_index:.2f}."
            )
        else:
            self.message = "Compra bloqueada: " + self._friendly_reasons(result.reasons)

    def sell_selected(self) -> None:
        if not self.selected_good:
            self.message = "Nenhuma mercadoria selecionada."
            return
        result = self.session.sell(
            self.state,
            self.selected_good,
            self.trade_quantity,
            seed=1498,
        )
        if result.executed:
            self.state = result.state_after
            self.message = (
                f"Venda: {self.trade_quantity:g} {self.selected_good}; "
                f"valor índice {result.trade_result.total_value_index:.2f}."
            )
        else:
            self.message = "Venda bloqueada: " + self._friendly_reasons(result.reasons)

    def _draw_trade_overlay(
        self,
        surface: pygame.Surface,
        small: pygame.font.Font,
        micro: pygame.font.Font,
    ) -> None:
        """Redesenha apenas os controles comerciais da interface base."""
        for target in self.targets:
            if target.kind != "action" or target.value not in {"buy", "sell"}:
                continue
            pygame.draw.rect(surface, BUTTON, target.rect, border_radius=3)
            label = (
                f"Comprar {self.trade_quantity:g}"
                if target.value == "buy"
                else f"Vender {self.trade_quantity:g}"
            )
            self._draw_text(surface, micro, label, (target.rect.x + 9, target.rect.y + 6))

        overlay = self.trade_overlay_rect
        pygame.draw.rect(surface, (246, 241, 221), overlay, border_radius=4)
        pygame.draw.rect(surface, LINE, overlay, width=1, border_radius=4)

        used = self.session.trade.capacity_used(self.state.commerce)
        free = self.session.trade.capacity_free(self.state.commerce)
        self._draw_text(
            surface,
            micro,
            f"Carga: {used:.1f}/{self.state.commerce.capacity_total:.1f} | livre {free:.1f}",
            (overlay.x + 8, overlay.y + 8),
            MUTED,
        )
        owned = (
            self.state.commerce.quantity_of(self.selected_good)
            if self.selected_good
            else 0.0
        )
        selected = self.selected_good or "-"
        self._draw_text(
            surface,
            micro,
            f"Selecionado: {selected} | posse {owned:.1f}",
            (overlay.x + 8, overlay.y + 25),
            INK,
        )

        minus = pygame.Rect(overlay.x + 8, overlay.y + 49, 42, 26)
        plus = pygame.Rect(overlay.x + 158, overlay.y + 49, 42, 26)
        qty = pygame.Rect(overlay.x + 58, overlay.y + 49, 92, 26)
        can_decrease = self.trade_quantity > self.MIN_TRADE_QUANTITY
        can_increase = self.trade_quantity < self.MAX_TRADE_QUANTITY
        pygame.draw.rect(
            surface,
            BUTTON if can_decrease else BUTTON_DISABLED,
            minus,
            border_radius=3,
        )
        pygame.draw.rect(
            surface,
            BUTTON if can_increase else BUTTON_DISABLED,
            plus,
            border_radius=3,
        )
        pygame.draw.rect(surface, (232, 225, 202), qty, border_radius=3)
        self._draw_text(surface, small, "-", (minus.x + 17, minus.y + 3))
        self._draw_text(surface, micro, f"qtd {self.trade_quantity:g}", (qty.x + 17, qty.y + 7))
        self._draw_text(surface, small, "+", (plus.x + 15, plus.y + 3))
        if can_decrease:
            self.targets.append(ClickTarget(minus, "trade_quantity", "-1"))
        if can_increase:
            self.targets.append(ClickTarget(plus, "trade_quantity", "+1"))

    def render(self, surface: pygame.Surface) -> None:
        super().render(surface)
        small = pygame.font.SysFont("sans", 15)
        micro = pygame.font.SysFont("monospace", 12)
        self._draw_trade_overlay(surface, small, micro)

    def handle_click(self, pos: tuple[int, int]) -> None:
        for target in reversed(self.targets):
            if target.rect.collidepoint(pos) and target.kind == "trade_quantity":
                self.adjust_trade_quantity(float(target.value))
                return
        if self.trade_overlay_rect.collidepoint(pos):
            return
        super().handle_click(pos)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scenario",
        choices=("HISTORICAL", "TECHNICAL"),
        default="HISTORICAL",
    )
    parser.add_argument("--output", help="renderiza um quadro PNG e encerra")
    args = parser.parse_args()

    pygame.init()
    surface = (
        pygame.Surface((WIDTH, HEIGHT))
        if args.output
        else pygame.display.set_mode((WIDTH, HEIGHT))
    )
    app = M3PlayablePrototype(args.scenario)
    app.render(surface)

    if args.output:
        pygame.image.save(surface, args.output)
        pygame.quit()
        return

    pygame.display.set_caption("Quinto Império — comércio operacional M3")
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
                    running = False
                elif event.key == pygame.K_r:
                    app.reset()
                    app.render(surface)
                    pygame.display.flip()
                elif event.key == pygame.K_TAB:
                    app.reset(
                        "TECHNICAL"
                        if app.scenario == "HISTORICAL"
                        else "HISTORICAL"
                    )
                    app.render(surface)
                    pygame.display.flip()
        clock.tick(30)
    pygame.quit()


if __name__ == "__main__":
    main()
