#!/usr/bin/env python3
"""Interface histórica contínua da vertical slice Lisboa–Calecute.

Reutiliza a interface Pygame do MVP e troca a orquestração da sessão pela
fachada ``HistoricalCampaignModel``. A espera em Moçambique, Mombaça e Melinde
serve somente para alinhar o relógio às partidas já observadas; esses nós não
são promovidos a novas permanências em ``expedition_stops.csv``.

A campanha jogável abre em uma fase explicitamente simulada de preparação dois
dias antes da partida histórica de 8 de julho de 1497. Essa janela não altera a
data documentada da partida e não concede recursos automaticamente.
"""

from __future__ import annotations

import argparse

import pygame

from game import (
    BG,
    BUTTON,
    HEIGHT,
    INK,
    LINE,
    MAP_RECT,
    MUTED,
    SEED,
    WIDTH,
    ClickTarget,
)
from game_m3 import M3PlayablePrototype
from quintoimperio.domain import (
    ChronologyMode,
    HistoricalCampaignModel,
    RelationshipStatus,
)
from quintoimperio.domain.campaign_progress import CampaignProgressModel


class HistoricalCampaignPrototype(M3PlayablePrototype):
    """Versão histórica do painel do MVP com cronologia guiada ponta a ponta."""

    def __init__(self) -> None:
        super().__init__("HISTORICAL")
        self.session = HistoricalCampaignModel()
        self.progress_model = CampaignProgressModel(self.session.session)
        self.state = self.session.initial_playable_state()
        self.message = (
            "Preparação simulada em Lisboa: partida histórica em 1497-07-08; "
            "margem logística de 20 dias-equivalentes é heurística de simulação."
        )

    def plan_for_route(self, route_id: str):
        pilot_id = self.session.recommended_pilot_id(self.state, route_id)
        return self.session.plan_voyage(
            self.state,
            route_id,
            pilot_id=pilot_id,
            seed=SEED,
        )

    def wait_stop(self) -> None:
        result = self.session.wait_for_guided_departure(self.state)
        if result.executed:
            self.state = result.state_after
            self.message = (
                f"Espera guiada: {result.days_waited} dia(s); "
                f"data {self.state.vessel.clock.current_date}."
            )
        else:
            self.message = "Espera indisponível: " + ", ".join(result.reasons)

    def contact_authority_action(self) -> None:
        result = self.session.contact_authority(self.state)
        if not result.executed:
            self.message = "Contato indisponível: " + ", ".join(result.reasons)
            return
        if result.actor is None:
            raise RuntimeError(
                "Contato relacional foi executado sem autoridade histórica normalizada"
            )
        self.state = result.state_after
        self.message = (
            f"Contato estabelecido: {result.actor.label}; "
            f"+{result.days_spent} dia(s). Acesso comercial não foi alterado."
        )

    def _guided_wait_overlay(self, surface: pygame.Surface) -> None:
        if self.state.chronology_mode is not ChronologyMode.GUIDED:
            return
        if self.session.active_stop(self.state) is not None:
            return
        expected = self.session.guided_departure_date(self.state)
        if expected is None:
            return
        current = self.state.vessel.clock.current_date
        if current >= expected:
            return

        days = (expected - current).days
        planning = self.session.logistics_planning_view(self.state, seed=SEED)
        rect = pygame.Rect(MAP_RECT.left + 12, MAP_RECT.bottom - 78, 550, 64)
        pygame.draw.rect(surface, BG, rect, border_radius=3)
        pygame.draw.rect(surface, LINE, rect, width=1, border_radius=3)
        font = pygame.font.SysFont("monospace", 11)
        required = (
            "?"
            if planning.next_leg_required_days is None
            else f"{planning.next_leg_required_days:.0f}d"
        )
        status = "OK" if planning.meets_recommended_margin else "abaixo"
        if planning.in_predeparture_phase:
            line1 = f"PREPARAÇÃO SIMULADA | partida histórica {expected} | esperar {days}d"
        else:
            line1 = f"Próxima partida observada: {expected} | esperar {days}d"
        line2 = (
            f"Autonomia {planning.current_autonomy_days:.0f}d | próxima perna {required} | "
            f"margem heurística +{planning.recommended_margin_days:.0f}d ({status})"
        )
        if planning.next_destination_provisions_evidence_indeterminate:
            line3 = (
                f"Destino {planning.next_destination_node}: evidência histórica de provisões "
                "indeterminada."
            )
        else:
            line3 = "Margem é heurística de simulação; esperar não concede recursos."
        surface.blit(font.render(line1, True, INK), (rect.x + 8, rect.y + 6))
        surface.blit(font.render(line2, True, MUTED), (rect.x + 8, rect.y + 24))
        surface.blit(font.render(line3, True, MUTED), (rect.x + 8, rect.y + 42))
        self.targets.append(ClickTarget(rect, "action", "wait_stop"))

    def _authority_contact_overlay(self, surface: pygame.Surface) -> None:
        node_id = self.state.vessel.location_node
        on_date = self.state.vessel.clock.current_date
        authority = self.session.relationship.actor_for_role(
            node_id, on_date, "AUTHORITY"
        )
        if authority is None:
            return
        if (
            self.session.relationship_status(self.state, authority.actor_id)
            is RelationshipStatus.CONTACTED
        ):
            return

        rect = pygame.Rect(MAP_RECT.left + 12, MAP_RECT.bottom - 118, 345, 34)
        pygame.draw.rect(surface, BUTTON, rect, border_radius=3)
        pygame.draw.rect(surface, LINE, rect, width=1, border_radius=3)
        font = pygame.font.SysFont("monospace", 12)
        text = "Contatar autoridade local documentada"
        surface.blit(font.render(text, True, INK), (rect.x + 8, rect.y + 9))
        self.targets.append(ClickTarget(rect, "action", "contact_authority"))

    def _campaign_progress_overlay(self, surface: pygame.Surface) -> None:
        progress = self.progress_model.progress(self.state)
        rect = pygame.Rect(MAP_RECT.left + 12, MAP_RECT.top + 12, 430, 56)
        pygame.draw.rect(surface, BG, rect, border_radius=3)
        pygame.draw.rect(surface, LINE, rect, width=1, border_radius=3)
        font = pygame.font.SysFont("monospace", 12)
        title = "M4 CONCLUÍDO" if progress.completed else "Objetivo atual"
        surface.blit(font.render(title, True, MUTED), (rect.x + 8, rect.y + 7))
        surface.blit(
            font.render(progress.current_objective[:56], True, INK),
            (rect.x + 8, rect.y + 27),
        )

    def render(self, surface: pygame.Surface) -> None:
        super().render(surface)
        self._campaign_progress_overlay(surface)
        self._authority_contact_overlay(surface)
        self._guided_wait_overlay(surface)

    def handle_click(self, pos: tuple[int, int]) -> None:
        for target in reversed(self.targets):
            if (
                target.rect.collidepoint(pos)
                and target.kind == "action"
                and target.value == "contact_authority"
            ):
                self.contact_authority_action()
                return
        super().handle_click(pos)

    def _travel(self, route_id: str) -> None:
        self.selected_route = route_id
        self.travel_selected()
        if self.state.vessel.location_node != self.session.routes[route_id]["destination_node"]:
            raise RuntimeError(f"Smoke da campanha não chegou ao destino de {route_id}: {self.message}")

    def _wait(self) -> None:
        before = self.state.vessel.clock.current_date
        self.wait_stop()
        if self.state.vessel.clock.current_date < before:
            raise RuntimeError("Relógio regressou durante espera guiada")

    def run_scripted_campaign(self) -> None:
        """Percorre a vertical slice usando as mesmas ações expostas pela UI."""
        # A campanha jogável começa em 6 de julho. O smoke não recebe provisões
        # automaticamente: apenas sincroniza a partida histórica antes da viagem.
        if self.session.in_predeparture_phase(self.state):
            self._wait()

        self._travel("R_LIS_STG")
        for _ in range(3):
            self.reprovision()
        self._wait()

        self._travel("R_STG_SHB")
        self._wait()
        self._travel("R_SHB_CGH")
        self._travel("R_CGH_SBR")

        for _ in range(4):
            self.reprovision()
        self._wait()
        self._travel("R_SBR_RCO")

        self.reprovision()
        self._wait()
        self._travel("R_RCO_RBS")

        self.reprovision()
        self._wait()
        self._travel("R_RBS_MOZ")

        self._wait()
        self._travel("R_MOZ_MOM")
        self._wait()
        self._travel("R_MOM_MAL")

        self.contact_authority_action()
        if "Contato estabelecido" not in self.message:
            raise RuntimeError(f"Contato de Melinde não foi estabelecido: {self.message}")
        self._wait()
        pilot_id = self.session.recommended_pilot_id(self.state, "R_MAL_CAL")
        if pilot_id != "PIL_MAL_GUJ_1498":
            raise RuntimeError("Piloto guzerate não ficou disponível após o contato em Melinde")
        self._travel("R_MAL_CAL")

        if self.state.vessel.location_node != "CAL":
            raise RuntimeError("Campanha histórica não terminou em Calecute")
        if self.state.active_expedition_id is not None:
            raise RuntimeError("Expedição permaneceu ativa após a décima perna")
        if self.progress_model.progress(self.state).completed:
            raise RuntimeError("M4 encerrou a campanha apenas pela chegada a Calecute")

        access_result = self.session.negotiate_access(self.state)
        if not access_result.executed:
            raise RuntimeError(
                "Negociação de acesso em Calecute falhou no smoke: "
                + ", ".join(access_result.reasons)
            )
        self.state = access_result.state_after
        if self.progress_model.progress(self.state).completed:
            raise RuntimeError("M4 encerrou a campanha antes da operação comercial")

        self.selected_good = "PEPPER"
        self.trade_quantity = 2.0
        before_quantity = self.state.commerce.quantity_of("PEPPER")
        self.buy_selected()
        after_quantity = self.state.commerce.quantity_of("PEPPER")
        if after_quantity <= before_quantity:
            raise RuntimeError(f"Comércio M3 não foi executado em Calecute: {self.message}")

        progress = self.progress_model.progress(self.state)
        if not progress.completed:
            raise RuntimeError(f"M4 não encerrou após o comércio elegível: {progress.current_objective}")
        summary = self.progress_model.summary(self.state)
        self.message = (
            f"Campanha concluída: Calecute em {summary.current_date}; "
            f"cronologia {summary.chronology_mode.value}; piloto {pilot_id}; "
            f"compra={after_quantity - before_quantity:g} PEPPER; "
            f"contatos={len(summary.contacted_actor_ids)}; "
            f"capital={summary.capital_index:.1f}; "
            f"carga={summary.capacity_used:.1f}/{summary.capacity_total:.1f}."
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", help="salva o quadro final em PNG")
    parser.add_argument(
        "--campaign-smoke",
        action="store_true",
        help="executa automaticamente Lisboa–Calecute pelas ações da interface",
    )
    args = parser.parse_args()

    pygame.init()
    surface = (
        pygame.Surface((WIDTH, HEIGHT))
        if args.output or args.campaign_smoke
        else pygame.display.set_mode((WIDTH, HEIGHT))
    )
    app = HistoricalCampaignPrototype()

    if args.campaign_smoke:
        app.run_scripted_campaign()
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

    pygame.display.set_caption("Quinto Império — campanha histórica 1497–1498")
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
                    app.__init__()
                    app.render(surface)
                    pygame.display.flip()
        clock.tick(30)
    pygame.quit()


if __name__ == "__main__":
    main()
