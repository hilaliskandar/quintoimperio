#!/usr/bin/env python3
"""Interface v0.2 da campanha histórica, com retorno opt-in após o MVP.

A camada M5 reorganiza feedback e confirmação sem introduzir fatos históricos.
O baseline Lisboa-Calecute permanece encerrável como MVP; após a primeira compra
elegível em Calecute, o jogador pode ativar explicitamente a subcampanha de
retorno até os Baixos do Rio Grande.
"""

from __future__ import annotations

import argparse

import pygame

from quintoimperio.domain import CampaignProgressModel, ReturnCampaignModel

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
    "DOCUMENTED_PROVISION_ACTION_ALREADY_USED": "oportunidade documental já utilizada",
    "DOCUMENTED_REPAIR_ACTION_ALREADY_USED": "carena documental já realizada",
}


class M5HistoricalCampaignPrototype(HistoricalCampaignPrototype):
    """Interface v0.2: MVP intacto e retorno documental explicitamente opcional."""

    HISTORY_LIMIT = 4

    def __init__(self) -> None:
        super().__init__()
        self.session = ReturnCampaignModel()
        self.state = self.session.initial_playable_state()
        self.progress_model = CampaignProgressModel(self.session.session)
        self.pending_travel_route: str | None = None
        self.action_history: list[str] = [self.message]

    @staticmethod
    def friendly_reasons(reasons: tuple[str, ...]) -> str:
        return "; ".join(
            BLOCKER_LABELS.get(reason, reason.replace("_", " ").lower())
            for reason in reasons
        )

    def _remember(self) -> None:
        if not self.message:
            return
        if self.action_history and self.action_history[-1] == self.message:
            return
        self.action_history.append(self.message)
        del self.action_history[:-self.HISTORY_LIMIT]

    def campaign_status(self):
        return self.progress_model.progress(self.state)

    def activate_return_action(self) -> None:
        progress = self.campaign_status()
        if not progress.completed:
            self.message = "O retorno só fica disponível após a conclusão do MVP em Calecute."
            self._remember()
            return
        try:
            self.state = self.session.activate_return(self.state)
        except ValueError as exc:
            self.message = f"Retorno indisponível: {exc}."
            self._remember()
            return
        self.message = (
            "Retorno documental ativado. Próxima partida histórica: 1498-08-30; "
            "o epílogo posterior a 1499-04-25 continua fora do loop jogável."
        )
        self._remember()

    def documented_provision_action(self) -> None:
        node = self.state.vessel.location_node
        requested = 5.0 if node == "SMI" else 50.0
        result = self.session.reprovision_at_documented_stop(self.state, requested)
        if not result.executed:
            self.message = "Provisões documentais indisponíveis: " + self.friendly_reasons(result.reasons)
            self._remember()
            return
        self.state = result.state_after
        qualifier = "SIM; contato breve" if node == "SMI" else "SIM; permanência documentada"
        self.message = (
            f"Provisões específicas em {node}: +{result.service_result.effect:.1f} dias-eq. "
            f"({qualifier}); +{result.service_result.days_spent} dia(s)."
        )
        self._remember()

    def documented_careening_action(self) -> None:
        result = self.session.repair_at_documented_stop(self.state, 2.0)
        if not result.executed:
            self.message = "Carena documental indisponível: " + self.friendly_reasons(result.reasons)
            self._remember()
            return
        self.state = result.state_after
        self.message = (
            f"Carena em Anjediva: +{result.service_result.effect:.1f} pontos de condição "
            f"SIM; +{result.service_result.days_spent} dia(s)."
        )
        self._remember()

    def travel_selected(self) -> None:
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

        if self.state.active_expedition_id == self.session.RETURN_EXPEDITION_ID:
            leg = self.session.current_leg(self.state)
            destination = "?" if leg is None else self.session.routes[leg.route_id]["destination_node"]
            objective = f"Retorno histórico: {self.state.vessel.location_node} → {destination}"
        elif self.state.vessel.location_node == self.session.RETURN_END_NODE:
            objective = "Retorno documental concluído nos Baixos do Rio Grande"
        elif progress.completed:
            objective = "MVP concluído em Calecute — retorno histórico disponível"
        else:
            objective = f"Objetivo atual: {progress.current_objective}"

        self._draw_text(surface, small, objective, (strip.x + 12, strip.y + 9), INK)
        completed = sum(1 for item in progress.milestones if item.completed)
        mode = self.state.chronology_mode.value
        mode_note = "trajetória histórica" if mode == "GUIDED" else "trajetória divergente"
        self._draw_text(
            surface,
            micro,
            f"Progresso MVP {completed}/{len(progress.milestones)} | {mode} — {mode_note}",
            (strip.x + 12, strip.y + 34),
            MUTED if mode == "GUIDED" else BAD,
        )

    def _draw_return_actions(self, surface: pygame.Surface) -> None:
        actions: list[tuple[str, str]] = []
        progress = self.campaign_status()
        if (
            progress.completed
            and self.state.vessel.location_node == "CAL"
            and self.state.active_expedition_id is None
        ):
            actions.append(("Continuar: retorno 1498–1499", "activate_return"))
        if self.state.active_expedition_id == self.session.RETURN_EXPEDITION_ID:
            if self.session.documented_stop_can_reprovision(self.state):
                label = (
                    "Aceitar peixe em Santa Maria [SIM]"
                    if self.state.vessel.location_node == "SMI"
                    else "Obter provisões da permanência [SIM]"
                )
                actions.append((label, "return_provisions"))
            if self.session.documented_stop_can_repair(self.state):
                actions.append(("Realizar carena documentada +2 [SIM]", "return_careening"))
        if not actions:
            return

        rect = pygame.Rect(MAP_RECT.left + 10, MAP_RECT.top + 73, 365, 12 + 36 * len(actions))
        pygame.draw.rect(surface, BG, rect, border_radius=4)
        pygame.draw.rect(surface, LINE, rect, width=1, border_radius=4)
        small = pygame.font.SysFont("sans", 13)
        y = rect.y + 7
        for label, value in actions:
            button = pygame.Rect(rect.x + 7, y, rect.width - 14, 29)
            pygame.draw.rect(surface, BUTTON, button, border_radius=4)
            self._draw_text(surface, small, label, (button.x + 10, button.y + 6), INK)
            self.targets.append(ClickTarget(button, "action", value))
            y += 36

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
        self._draw_text(
            surface,
            micro,
            f"Duração prevista: {plan.travel_days} dias | base: {basis}",
            (rect.x + 18, rect.y + 76),
            MUTED,
        )
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
        self._draw_return_actions(surface)
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
            if target.kind == "action" and target.value == "activate_return":
                self.activate_return_action()
                return
            if target.kind == "action" and target.value == "return_provisions":
                self.documented_provision_action()
                return
            if target.kind == "action" and target.value == "return_careening":
                self.documented_careening_action()
                return
        before = self.message
        super().handle_click(pos)
        if self.message != before:
            self._remember()

    def run_scripted_return(self) -> None:
        """Continua, pela mesma fachada de UI, um estado que já concluiu o MVP."""
        self.activate_return_action()
        if self.state.active_expedition_id != self.session.RETURN_EXPEDITION_ID:
            raise RuntimeError(f"Retorno não foi ativado: {self.message}")

        while self.state.active_expedition_id == self.session.RETURN_EXPEDITION_ID:
            while self.session.documented_stop_can_reprovision(self.state):
                before = self.state.vessel.provision_days
                self.documented_provision_action()
                if self.state.vessel.provision_days <= before:
                    break
                if self.state.vessel.location_node == "SMI" or self.state.vessel.provision_days >= 120.0:
                    break
            if self.session.documented_stop_can_repair(self.state):
                self.documented_careening_action()

            departure = self.session.guided_departure_date(self.state)
            if departure is not None and self.state.vessel.clock.current_date < departure:
                self.wait_stop()

            leg = self.session.current_leg(self.state)
            if leg is None:
                raise RuntimeError("Retorno ativo sem perna corrente")
            self.selected_route = leg.route_id
            self.travel_selected()
            if self.pending_travel_route != leg.route_id:
                raise RuntimeError(f"Viagem do retorno não entrou em confirmação: {self.message}")
            self.confirm_travel()

        if self.state.vessel.location_node != "BRG":
            raise RuntimeError(f"Retorno terminou em {self.state.vessel.location_node}, não BRG")
        if self.state.vessel.clock.current_date.isoformat() != "1499-04-25":
            raise RuntimeError(f"Data final inesperada: {self.state.vessel.clock.current_date}")
        if self.state.chronology_mode.value != "GUIDED":
            raise RuntimeError(f"Retorno saiu da cronologia guiada: {self.state.chronology_mode.value}")
        self.message = "Retorno concluído em BRG em 1499-04-25; epílogo posterior permanece fora do loop."
        self._remember()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", help="renderiza um quadro PNG e encerra")
    parser.add_argument(
        "--campaign-smoke",
        action="store_true",
        help="executa Lisboa-Calecute e renderiza o estado final v0.2",
    )
    parser.add_argument(
        "--return-smoke",
        action="store_true",
        help="executa Lisboa-Calecute e continua explicitamente até BRG",
    )
    args = parser.parse_args()

    pygame.init()
    surface = (
        pygame.Surface((WIDTH, HEIGHT))
        if args.output or args.campaign_smoke or args.return_smoke
        else pygame.display.set_mode((WIDTH, HEIGHT))
    )
    app = M5HistoricalCampaignPrototype()

    if args.campaign_smoke or args.return_smoke:
        runner = HistoricalCampaignPrototype()
        runner.run_scripted_campaign()
        app.state = runner.state
        app.message = runner.message
        app._remember()
        if args.return_smoke:
            app.run_scripted_return()
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
