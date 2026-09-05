#!/usr/bin/env python3
"""Primeira interface jogável Pygame para o núcleo integrado.

A interface não cria regras econômicas, náuticas ou históricas. Ela apenas
expõe ``GameSessionModel``. Valores de capital, capacidade, quantidade, preço,
tempo de negociação e eventos marítimos genéricos são parâmetros abstratos de
simulação.

Dois estados são oferecidos:

- ``HISTORICAL``: 8 de julho de 1497 em Lisboa, com participação institucional
  na armada de Vasco da Gama registrada separadamente do conhecimento pessoal;
- ``TECHNICAL``: cenário explícito de integração Calecute -> Aden já usado nos
  testes do domínio. Não representa o estado histórico inicial do personagem.

A participação na armada não fixa identidade ou profissão do protagonista.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date

import pygame

from quintoimperio.domain import (
    AccessStatus,
    ChronologyMode,
    GameSessionModel,
    GameSessionState,
    InformationChannel,
    KnowledgeLevel,
    KnowledgeState,
    MapExtent,
    MapPoint,
    PortServiceKind,
    WorldMapModel,
)


WIDTH = 1400
HEIGHT = 820
MAP_RECT = pygame.Rect(20, 70, 830, 720)
SIDE_RECT = pygame.Rect(870, 70, 510, 720)
SEED = 1498

BG = (232, 225, 202)
PANEL = (246, 241, 221)
INK = (45, 42, 35)
MUTED = (102, 95, 78)
LINE = (166, 151, 116)
SEA = (202, 218, 218)
PORT = (74, 68, 53)
CURRENT = (143, 57, 45)
SELECTED = (190, 168, 111)
BUTTON = (219, 205, 166)
BUTTON_DISABLED = (208, 203, 188)
GOOD = (51, 105, 72)
BAD = (137, 58, 48)


@dataclass(frozen=True)
class ClickTarget:
    rect: pygame.Rect
    kind: str
    value: str


class PlayablePrototype:
    def __init__(self, scenario: str = "HISTORICAL") -> None:
        self.session = GameSessionModel()
        self.world = WorldMapModel(self.session.root)
        self.scenario = scenario.upper()
        self.state = self._make_state(self.scenario)
        self.selected_good: str | None = None
        self.selected_route: str | None = None
        self.message = "Selecione uma ação, mercadoria ou rota."
        self.targets: list[ClickTarget] = []

    def _make_state(self, scenario: str) -> GameSessionState:
        if scenario == "HISTORICAL":
            return self.session.initial_state(active_expedition_id="EXP_GAMA_1497")
        if scenario != "TECHNICAL":
            raise ValueError("scenario deve ser HISTORICAL ou TECHNICAL")

        state = self.session.initial_state(
            location_node="CAL",
            start_date=date(1498, 5, 22),
            provision_days=200.0,
            capital_index=100.0,
            capacity_total=30.0,
        )
        cal = self.session.node_state(state, "CAL")
        state = self.session.scenario_set_node_knowledge(
            state,
            "CAL",
            KnowledgeState(
                geo=cal.geo,
                nav=cal.nav,
                market=KnowledgeLevel.OPERATIONAL,
                political=cal.political,
            ),
        )
        state = self.session.scenario_set_route_knowledge(
            state, "R_CAL_ADE", KnowledgeLevel.OPERATIONAL
        )
        return self.session.scenario_set_access(
            state, "CAL", AccessStatus.NEGOTIATED
        )

    def reset(self, scenario: str | None = None) -> None:
        if scenario is not None:
            self.scenario = scenario.upper()
        self.state = self._make_state(self.scenario)
        self.selected_good = None
        self.selected_route = None
        self.message = "Sessão reiniciada."

    def visible_relationships(self):
        """Retorna somente atores já contatados pelo personagem."""
        return self.session.contacted_relationships(self.state)

    def visible_points(self) -> list[MapPoint]:
        points: list[MapPoint] = []
        for record in self.state.node_knowledge:
            if record.state.geo < KnowledgeLevel.RUMORED:
                continue
            row = self.world.nodes[record.node_id]
            if not row.get("latitude") or not row.get("longitude"):
                continue
            points.append(
                MapPoint(
                    node_id=record.node_id,
                    label=row["historical_name"],
                    latitude=float(row["latitude"]),
                    longitude=float(row["longitude"]),
                    geo_knowledge=record.state.geo,
                )
            )
        return points

    def outgoing_routes(self) -> list[str]:
        current = self.state.vessel.location_node
        return sorted(
            route_id
            for route_id, row in self.session.routes.items()
            if row["origin_node"] == current
        )

    def _pilot_for_route(self, route_id: str) -> str | None:
        current = self.state.vessel.location_node
        on_date = self.state.vessel.clock.current_date
        for pilot_id in sorted(self.session.travel.pilots):
            if self.session.travel.pilot_can_guide(pilot_id, route_id, on_date, current):
                return pilot_id
        return None

    def plan_for_route(self, route_id: str):
        pilot_id = self._pilot_for_route(route_id)
        if pilot_id:
            with_pilot = self.session.plan_voyage(
                self.state, route_id, pilot_id=pilot_id, seed=SEED
            )
            if with_pilot.feasible:
                return with_pilot
        return self.session.plan_voyage(self.state, route_id, seed=SEED)

    def negotiate_access(self) -> None:
        result = self.session.negotiate_access(self.state)
        if not result.executed:
            self.message = "Negociação indisponível: " + ", ".join(result.reasons)
            return
        self.state = result.state_after
        self.message = (
            f"Acesso institucional negociado; +{result.days_spent} dia(s). "
            "Nenhum valor de taxa ou presente foi presumido."
        )

    def acquire_information(self, channel: InformationChannel) -> None:
        result = self.session.acquire_information(self.state, channel, seed=SEED)
        if not result.executed:
            self.message = f"Informação indisponível ({channel.value}): " + ", ".join(result.reasons)
            return
        self.state = result.state_after
        assert result.opportunity is not None
        opportunity = result.opportunity
        pilot = f"; piloto={opportunity.pilot_id}" if opportunity.pilot_id else ""
        self.message = (
            f"{channel.value}: informação sobre {opportunity.target_node_id} / "
            f"{opportunity.target_route_id}; +{opportunity.time_days} dia{pilot}."
        )

    def buy_selected(self) -> None:
        if not self.selected_good:
            self.message = "Nenhuma mercadoria selecionada."
            return
        result = self.session.buy(self.state, self.selected_good, 1.0, seed=SEED)
        if result.executed:
            self.state = result.state_after
            self.message = f"Compra: 1 {self.selected_good}."
        else:
            self.message = "Compra bloqueada: " + ", ".join(result.reasons)

    def sell_selected(self) -> None:
        if not self.selected_good:
            self.message = "Nenhuma mercadoria selecionada."
            return
        result = self.session.sell(self.state, self.selected_good, 1.0, seed=SEED)
        if result.executed:
            self.state = result.state_after
            self.message = f"Venda: 1 {self.selected_good}."
        else:
            self.message = "Venda bloqueada: " + ", ".join(result.reasons)

    def reprovision(self) -> None:
        result = self.session.reprovision(self.state, 30.0)
        if result.executed:
            self.state = result.state_after
            self.message = (
                f"Reabastecimento: +{result.service_result.effect:.1f} dias-eq.; "
                f"{result.service_result.days_spent} dia(s)."
            )
        else:
            self.message = "Reabastecimento bloqueado: " + ", ".join(result.reasons)

    def repair(self) -> None:
        result = self.session.repair(self.state, 20.0)
        if result.executed:
            self.state = result.state_after
            self.message = (
                f"Reparo: +{result.service_result.effect:.1f} condição; "
                f"{result.service_result.days_spent} dia(s)."
            )
        else:
            self.message = "Reparo bloqueado: " + ", ".join(result.reasons)

    def wait_stop(self) -> None:
        result = self.session.wait_for_stop_release(self.state)
        if result.executed:
            self.state = result.state_after
            self.message = f"Espera na escala: {result.days_waited} dia(s); data {self.state.vessel.clock.current_date}."
        else:
            self.message = "Espera indisponível: " + ", ".join(result.reasons)

    def travel_selected(self) -> None:
        if not self.selected_route:
            self.message = "Nenhuma rota selecionada."
            return
        plan = self.plan_for_route(self.selected_route)
        if not plan.feasible:
            self.message = "Viagem bloqueada: " + ", ".join(plan.blockers)
            return
        self.state = self.session.execute_voyage(self.state, plan)
        self.selected_route = None
        self.selected_good = None
        pilot = f"; piloto={plan.pilot_id}" if plan.pilot_id else ""
        basis = plan.navigation_basis.value if plan.navigation_basis else "SEM_BASE"
        if plan.events:
            event = plan.events[0]
            event_note = (
                f"; evento SIM={event.event_type.value} "
                f"(+{event.extra_days}d, condição -{event.condition_loss:.1f})"
            )
        elif plan.events_suppressed_by_observation:
            event_note = "; eventos aleatórios suprimidos por observação histórica"
        else:
            event_note = ""
        self.message = (
            f"Chegada a {plan.destination_node} em {plan.arrival_date}; "
            f"{plan.travel_days} dias; base={basis}{pilot}{event_note}."
        )

    @staticmethod
    def _draw_text(
        surface: pygame.Surface,
        font: pygame.font.Font,
        text: str,
        pos: tuple[int, int],
        color=INK,
    ) -> None:
        surface.blit(font.render(text, True, color), pos)

    @staticmethod
    def _wrap(font: pygame.font.Font, text: str, width: int) -> list[str]:
        words = text.split()
        lines: list[str] = []
        current = ""
        for word in words:
            candidate = word if not current else f"{current} {word}"
            if font.size(candidate)[0] <= width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    @staticmethod
    def _place_map_label(
        label: pygame.Surface,
        x: int,
        y: int,
        occupied: list[pygame.Rect],
    ) -> pygame.Rect:
        """Posiciona rótulos sem alterar coordenadas dos nós."""
        width, height = label.get_size()
        offsets = [
            (8, -8),
            (8, 10),
            (8, -26),
            (8, 28),
            (8, -44),
            (8, 46),
            (-width - 8, -8),
            (-width - 8, 10),
            (-width - 8, -26),
            (-width - 8, 28),
        ]
        bounds = MAP_RECT.inflate(-8, -8)
        fallback = label.get_rect(topleft=(x + 8, y - 8))
        fallback.clamp_ip(bounds)
        for dx, dy in offsets:
            candidate = label.get_rect(topleft=(x + dx, y + dy))
            candidate.clamp_ip(bounds)
            if not any(candidate.colliderect(rect.inflate(4, 2)) for rect in occupied):
                return candidate
        return fallback

    def _draw_map(self, surface: pygame.Surface, small: pygame.font.Font) -> None:
        pygame.draw.rect(surface, SEA, MAP_RECT, border_radius=4)
        pygame.draw.rect(surface, LINE, MAP_RECT, width=1, border_radius=4)
        points = self.visible_points()
        if not points:
            return
        extent = MapExtent.from_points(points)
        by_id = {point.node_id: point for point in points}

        for fraction in (0.25, 0.5, 0.75):
            x = MAP_RECT.left + round(MAP_RECT.width * fraction)
            y = MAP_RECT.top + round(MAP_RECT.height * fraction)
            pygame.draw.line(surface, (181, 199, 199), (x, MAP_RECT.top), (x, MAP_RECT.bottom), 1)
            pygame.draw.line(surface, (181, 199, 199), (MAP_RECT.left, y), (MAP_RECT.right, y), 1)

        visible_ids = set(by_id)
        route_levels = {
            record.route_id: record.nav for record in self.state.route_knowledge
        }
        for route_id, level in route_levels.items():
            institutionally_visible = self.session.expedition_authorizes(self.state, route_id)
            if level <= KnowledgeLevel.UNKNOWN and not institutionally_visible:
                continue
            route = self.session.routes[route_id]
            if route["origin_node"] not in visible_ids or route["destination_node"] not in visible_ids:
                continue
            p1 = self.world.project(
                by_id[route["origin_node"]], extent, MAP_RECT.width, MAP_RECT.height, 35
            )
            p2 = self.world.project(
                by_id[route["destination_node"]], extent, MAP_RECT.width, MAP_RECT.height, 35
            )
            p1 = (p1[0] + MAP_RECT.left, p1[1] + MAP_RECT.top)
            p2 = (p2[0] + MAP_RECT.left, p2[1] + MAP_RECT.top)
            pygame.draw.line(surface, (125, 119, 101), p1, p2, 2)

        occupied_labels: list[pygame.Rect] = []
        for point in points:
            x, y = self.world.project(point, extent, MAP_RECT.width, MAP_RECT.height, 35)
            x += MAP_RECT.left
            y += MAP_RECT.top
            color = CURRENT if point.node_id == self.state.vessel.location_node else PORT
            radius = 8 if point.node_id == self.state.vessel.location_node else 5
            pygame.draw.circle(surface, color, (x, y), radius)
            label = small.render(point.label, True, INK)
            label_rect = self._place_map_label(label, x, y, occupied_labels)
            if abs(label_rect.centery - y) > 10 or label_rect.left < x:
                anchor_x = label_rect.left if label_rect.centerx >= x else label_rect.right
                pygame.draw.line(
                    surface,
                    LINE,
                    (x, y),
                    (anchor_x, label_rect.centery),
                    1,
                )
            surface.blit(label, label_rect)
            occupied_labels.append(label_rect)

            for route_id in self.outgoing_routes():
                route = self.session.routes[route_id]
                if route["destination_node"] == point.node_id:
                    self.targets.append(
                        ClickTarget(pygame.Rect(x - 10, y - 10, 20, 20), "route", route_id)
                    )

    def _draw_header(
        self, surface: pygame.Surface, title: pygame.font.Font, small: pygame.font.Font
    ) -> None:
        self._draw_text(surface, title, "Quinto Império — protótipo jogável v0.1", (20, 18))
        banner = (
            "ARMADA DE 1497 — comando institucional ≠ conhecimento pessoal"
            if self.scenario == "HISTORICAL"
            else "CENÁRIO TÉCNICO — NÃO REPRESENTA O ESTADO HISTÓRICO INICIAL"
        )
        color = MUTED if self.scenario == "HISTORICAL" else BAD
        self._draw_text(surface, small, banner, (870, 27), color)

    def _draw_side_panel(
        self,
        surface: pygame.Surface,
        body: pygame.font.Font,
        small: pygame.font.Font,
        tiny: pygame.font.Font,
        micro: pygame.font.Font,
    ) -> None:
        pygame.draw.rect(surface, PANEL, SIDE_RECT, border_radius=4)
        pygame.draw.rect(surface, LINE, SIDE_RECT, width=1, border_radius=4)
        x = SIDE_RECT.left + 16
        y = SIDE_RECT.top + 13

        node = self.world.nodes[self.state.vessel.location_node]
        self._draw_text(surface, body, f"Porto: {node['historical_name']} [{self.state.vessel.location_node}]", (x, y))
        y += 26
        self._draw_text(surface, small, f"Data: {self.state.vessel.clock.current_date.isoformat()}", (x, y))
        y += 20
        self._draw_text(
            surface,
            small,
            f"Navio: condição {self.state.vessel.condition:.1f}/100 | provisões {self.state.vessel.provision_days:.1f} dias-eq.",
            (x, y),
        )
        y += 20
        used = self.session.trade.capacity_used(self.state.commerce)
        self._draw_text(
            surface,
            small,
            f"Capital índice: {self.state.commerce.capital_index:.2f} | carga {used:.1f}/{self.state.commerce.capacity_total:.1f}",
            (x, y),
        )
        y += 20
        if self.state.active_expedition_id:
            self._draw_text(
                surface,
                micro,
                f"Armada: {self.state.active_expedition_id} | perna {self.state.expedition_leg_sequence} | cronologia {self.state.chronology_mode.value}",
                (x, y),
                MUTED,
            )
            y += 18
        else:
            self._draw_text(surface, micro, f"Cronologia: {self.state.chronology_mode.value}", (x, y), MUTED)
            y += 18

        if self.state.voyage_event_history:
            event = self.state.voyage_event_history[-1]
            self._draw_text(
                surface,
                micro,
                f"Último evento SIM: {event.event_type.value} (+{event.extra_days}d / -{event.condition_loss:.1f} condição)",
                (x, y),
                MUTED,
            )
            y += 17

        stop = self.session.active_stop(self.state)
        if stop is not None:
            self._draw_text(surface, tiny, f"Escala histórica: {stop.node_id} | permanência narrada {stop.observed_stay_days}d", (x, y), INK)
            y += 17
            activities = ", ".join(stop.activities)
            for line in self._wrap(micro, f"Atividades documentadas: {activities}", SIDE_RECT.width - 34)[:2]:
                self._draw_text(surface, micro, line, (x, y), MUTED)
                y += 14
            self._draw_text(surface, micro, f"Partida documentada: {stop.departure_date.isoformat()}", (x, y), MUTED)
            y += 17
            wait_days = self.session.stops.days_until_release(stop, self.state.vessel.clock.current_date)
            can_wait = self.state.chronology_mode is ChronologyMode.GUIDED and wait_days > 0
            wait_rect = pygame.Rect(x + 5, y, 160, 25)
            pygame.draw.rect(surface, BUTTON if can_wait else BUTTON_DISABLED, wait_rect, border_radius=3)
            label = f"Esperar {wait_days} dia(s)" if wait_days else "Partida liberada"
            self._draw_text(surface, micro, label, (wait_rect.x + 12, wait_rect.y + 6))
            if can_wait:
                self.targets.append(ClickTarget(wait_rect, "action", "wait_stop"))
            y += 32

        access = self.session.access_view(self.state)
        self._draw_text(
            surface,
            tiny,
            f"Acesso: {access.status.value} | regime {access.access_regime}",
            (x, y),
            MUTED,
        )
        y += 19
        if access.negotiable:
            access_rect = pygame.Rect(x + 5, y, 185, 24)
            pygame.draw.rect(surface, BUTTON, access_rect, border_radius=3)
            self._draw_text(
                surface,
                micro,
                f"Negociar acesso ({access.time_days}d)",
                (access_rect.x + 10, access_rect.y + 5),
            )
            self.targets.append(ClickTarget(access_rect, "action", "negotiate_access"))
            y += 30

        provisions = self.session.service_quote(self.state, PortServiceKind.PROVISIONS)
        repair = self.session.service_quote(self.state, PortServiceKind.REPAIR)
        self._draw_text(
            surface,
            tiny,
            f"Serviços: provisões {provisions.availability.value} | reparo {repair.availability.value}",
            (x, y),
            MUTED,
        )
        y += 20
        prov_rect = pygame.Rect(x + 5, y, 130, 25)
        repair_rect = pygame.Rect(x + 145, y, 120, 25)
        pygame.draw.rect(surface, BUTTON if provisions.actionable else BUTTON_DISABLED, prov_rect, border_radius=3)
        pygame.draw.rect(surface, BUTTON if repair.actionable else BUTTON_DISABLED, repair_rect, border_radius=3)
        self._draw_text(surface, micro, "Reabastecer +30", (prov_rect.x + 10, prov_rect.y + 6))
        self._draw_text(surface, micro, "Reparar +20", (repair_rect.x + 17, repair_rect.y + 6))
        self.targets.extend(
            [
                ClickTarget(prov_rect, "action", "provisions"),
                ClickTarget(repair_rect, "action", "repair"),
            ]
        )
        y += 32

        self._draw_text(surface, tiny, "Informação", (x, y), MUTED)
        y += 18
        info_specs = [
            (InformationChannel.RUMOR, "Ouvir rumor", 125),
            (InformationChannel.MERCHANT_CONTACT, "Falar mercador", 135),
            (InformationChannel.PILOT_CONSULTATION, "Consultar piloto", 145),
        ]
        info_x = x + 5
        for channel, label, width in info_specs:
            available = bool(self.session.information_opportunities(self.state, channel))
            rect = pygame.Rect(info_x, y, width, 24)
            pygame.draw.rect(surface, BUTTON if available else BUTTON_DISABLED, rect, border_radius=3)
            self._draw_text(surface, micro, label, (rect.x + 8, rect.y + 5))
            if available:
                self.targets.append(ClickTarget(rect, "information", channel.value))
            info_x += width + 6
        y += 31

        contacts = self.visible_relationships()
        if contacts:
            self._draw_text(surface, tiny, "Relações estabelecidas", (x, y), MUTED)
            y += 17
            for actor in contacts[:2]:
                lines = self._wrap(micro, actor.label, SIDE_RECT.width - 50)
                if lines:
                    self._draw_text(surface, micro, f"- {lines[0]}", (x + 8, y), INK)
                    y += 15
            y += 2

        self._draw_text(surface, body, "Carga", (x, y))
        y += 21
        if self.state.commerce.cargo:
            for item in self.state.commerce.cargo[:2]:
                self._draw_text(surface, tiny, f"{item.good_id}: {item.quantity:.1f}", (x + 8, y))
                y += 17
        else:
            self._draw_text(surface, tiny, "vazia", (x + 8, y), MUTED)
            y += 17
        y += 3

        market = self.session.market_view(self.state, seed=SEED)
        self._draw_text(surface, body, "Mercado", (x, y))
        self._draw_text(
            surface,
            micro,
            f"conh. {market.knowledge_level.name} | acesso {market.access_status.value}",
            (x + 150, y + 3),
            MUTED,
        )
        y += 22
        if market.knowledge_level < KnowledgeLevel.OPERATIONAL:
            self._draw_text(surface, micro, "Mercado oculto: conhecimento insuficiente.", (x + 8, y), BAD)
            y += 20
        else:
            if not market.actionable:
                self._draw_text(surface, micro, "Cotações conhecidas; compra/venda bloqueadas pelo acesso.", (x + 8, y), BAD)
                y += 18
            for entry in market.entries[:4]:
                rect = pygame.Rect(x + 3, y - 2, 460, 18)
                if entry.good_id == self.selected_good:
                    pygame.draw.rect(surface, SELECTED, rect, border_radius=2)
                marker = "*" if entry.restricted else " "
                self._draw_text(
                    surface,
                    micro,
                    f"{marker}{entry.good_id:<13} compra {entry.buy_price_index:>5.2f} | venda {entry.sell_price_index:>5.2f}",
                    (x + 8, y),
                )
                self.targets.append(ClickTarget(rect, "good", entry.good_id))
                y += 19

            buy_rect = pygame.Rect(x + 5, y + 1, 105, 25)
            sell_rect = pygame.Rect(x + 120, y + 1, 105, 25)
            trade_enabled = bool(self.selected_good) and market.actionable
            pygame.draw.rect(surface, BUTTON if trade_enabled else BUTTON_DISABLED, buy_rect, border_radius=3)
            pygame.draw.rect(surface, BUTTON if trade_enabled else BUTTON_DISABLED, sell_rect, border_radius=3)
            self._draw_text(surface, micro, "Comprar 1", (buy_rect.x + 18, buy_rect.y + 6))
            self._draw_text(surface, micro, "Vender 1", (sell_rect.x + 22, sell_rect.y + 6))
            if trade_enabled:
                self.targets.extend(
                    [ClickTarget(buy_rect, "action", "buy"), ClickTarget(sell_rect, "action", "sell")]
                )
            y += 31

        self._draw_text(surface, body, "Rotas de saída", (x, y))
        y += 22
        outgoing = self.outgoing_routes()
        if not outgoing:
            self._draw_text(surface, micro, "Nenhuma rota de saída na base atual.", (x + 8, y), MUTED)
            y += 19
        for route_id in outgoing[:4]:
            route = self.session.routes[route_id]
            plan = self.plan_for_route(route_id)
            status = "OK" if plan.feasible else "BLOQ"
            status_color = GOOD if plan.feasible else BAD
            basis = plan.navigation_basis.value if plan.navigation_basis else "-"
            rect = pygame.Rect(x + 3, y - 2, 460, 19)
            if route_id == self.selected_route:
                pygame.draw.rect(surface, SELECTED, rect, border_radius=2)
            self._draw_text(
                surface,
                micro,
                f"{route_id} -> {route['destination_node']} {status} {plan.travel_days}d {basis}",
                (x + 8, y),
                status_color,
            )
            self.targets.append(ClickTarget(rect, "route", route_id))
            y += 20

        travel_rect = pygame.Rect(x + 5, y + 2, 130, 26)
        pygame.draw.rect(surface, BUTTON if self.selected_route else BUTTON_DISABLED, travel_rect, border_radius=3)
        self._draw_text(surface, micro, "Executar viagem", (travel_rect.x + 14, travel_rect.y + 6))
        if self.selected_route:
            self.targets.append(ClickTarget(travel_rect, "action", "travel"))
        y += 34

        self._draw_text(surface, micro, "Mensagem:", (x, y), MUTED)
        y += 15
        for line in self._wrap(micro, self.message, SIDE_RECT.width - 34)[:2]:
            self._draw_text(surface, micro, line, (x, y), INK)
            y += 15

        note_y = SIDE_RECT.bottom - 33
        note = "Acesso, informação, relações, eventos e índices são simulação; nenhuma taxa/presente é presumida."
        for line in self._wrap(micro, note, SIDE_RECT.width - 34)[:2]:
            self._draw_text(surface, micro, line, (x, note_y), MUTED)
            note_y += 14

    def render(self, surface: pygame.Surface) -> None:
        self.targets = []
        surface.fill(BG)
        title = pygame.font.SysFont("serif", 30, bold=True)
        body = pygame.font.SysFont("serif", 20, bold=True)
        small = pygame.font.SysFont("sans", 15)
        tiny = pygame.font.SysFont("monospace", 13)
        micro = pygame.font.SysFont("monospace", 12)
        self._draw_header(surface, title, small)
        self._draw_map(surface, small)
        self._draw_side_panel(surface, body, small, tiny, micro)

    def handle_click(self, pos: tuple[int, int]) -> None:
        for target in reversed(self.targets):
            if not target.rect.collidepoint(pos):
                continue
            if target.kind == "good":
                self.selected_good = target.value
                self.message = f"Mercadoria selecionada: {target.value}."
            elif target.kind == "route":
                self.selected_route = target.value
                plan = self.plan_for_route(target.value)
                if plan.feasible:
                    basis = plan.navigation_basis.value if plan.navigation_basis else "SEM_BASE"
                    self.message = f"Rota {target.value}: disponível por {basis}."
                else:
                    self.message = f"Rota {target.value}: " + ", ".join(plan.blockers)
            elif target.kind == "information":
                self.acquire_information(InformationChannel(target.value))
            elif target.kind == "action":
                if target.value == "buy":
                    self.buy_selected()
                elif target.value == "sell":
                    self.sell_selected()
                elif target.value == "provisions":
                    self.reprovision()
                elif target.value == "repair":
                    self.repair()
                elif target.value == "wait_stop":
                    self.wait_stop()
                elif target.value == "negotiate_access":
                    self.negotiate_access()
                elif target.value == "travel":
                    self.travel_selected()
            return


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", choices=("HISTORICAL", "TECHNICAL"), default="HISTORICAL")
    parser.add_argument("--output", help="renderiza um quadro PNG e encerra")
    args = parser.parse_args()

    pygame.init()
    surface = pygame.Surface((WIDTH, HEIGHT)) if args.output else pygame.display.set_mode((WIDTH, HEIGHT))
    app = PlayablePrototype(args.scenario)
    app.render(surface)

    if args.output:
        pygame.image.save(surface, args.output)
        pygame.quit()
        return

    pygame.display.set_caption("Quinto Império — protótipo jogável v0.1")
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
                    app.reset("TECHNICAL" if app.scenario == "HISTORICAL" else "HISTORICAL")
                    app.render(surface)
                    pygame.display.flip()
        clock.tick(30)
    pygame.quit()


if __name__ == "__main__":
    main()