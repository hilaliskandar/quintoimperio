"""Aquisição ativa de informação sem copiar conhecimento institucional.

As oportunidades são derivadas somente de nós/rotas já existentes na base. Os
canais genéricos são mecânicas de simulação apoiadas na existência da rede e
não representam diálogos históricos documentados. Pilotos, quando usados, são
restritos aos registros históricos de ``pilots.csv`` e ``pilot_routes.csv``.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import date
from enum import Enum
from pathlib import Path

from quintoimperio.data.loader import RepositoryData

from .knowledge import KnowledgeLevel


class InformationChannel(str, Enum):
    RUMOR = "RUMOR"
    MERCHANT_CONTACT = "MERCHANT_CONTACT"
    PILOT_CONSULTATION = "PILOT_CONSULTATION"


@dataclass(frozen=True)
class InformationRule:
    channel: InformationChannel
    time_days: int
    geo_min: KnowledgeLevel
    route_nav_min: KnowledgeLevel
    market_min: KnowledgeLevel
    political_min: KnowledgeLevel


@dataclass(frozen=True)
class InformationOpportunity:
    opportunity_id: str
    channel: InformationChannel
    origin_node: str
    target_route_id: str
    target_node_id: str
    time_days: int
    geo_min: KnowledgeLevel
    route_nav_min: KnowledgeLevel
    market_min: KnowledgeLevel
    political_min: KnowledgeLevel
    pilot_id: str | None = None


class InformationModel:
    """Gera oportunidades conservadoras a partir da rede documentada."""

    def __init__(self, root: Path | None = None) -> None:
        repository = RepositoryData(root)
        self.root = repository.root
        self.nodes = {
            row["node_id"]: row for row in repository.historical("nodes.csv")
        }
        self.routes = {
            row["route_id"]: row for row in repository.historical("routes.csv")
        }
        self.pilots = {
            row["pilot_id"]: row for row in repository.historical("pilots.csv")
        }
        self.pilot_routes = repository.historical("pilot_routes.csv")
        self.rules: dict[InformationChannel, InformationRule] = {}
        for row in repository.simulation("information_rules.csv"):
            channel = InformationChannel(row["channel"])
            self.rules[channel] = InformationRule(
                channel=channel,
                time_days=int(row["time_days"]),
                geo_min=KnowledgeLevel(int(row["geo_min"])),
                route_nav_min=KnowledgeLevel(int(row["route_nav_min"])),
                market_min=KnowledgeLevel(int(row["market_min"])),
                political_min=KnowledgeLevel(int(row["political_min"])),
            )

    @staticmethod
    def _active(row: dict[str, str], on_date: date) -> bool:
        start = row.get("period_from", "")
        end = row.get("period_to", "")
        if start and on_date.year < int(start):
            return False
        if end and on_date.year > int(end):
            return False
        return True

    def _outgoing_routes(self, node_id: str, on_date: date) -> list[dict[str, str]]:
        return sorted(
            (
                row
                for row in self.routes.values()
                if row["origin_node"] == node_id
                and row.get("route_origin") != "STRATEGIC_AGGREGATE"
                and self._active(row, on_date)
            ),
            key=lambda row: row["route_id"],
        )

    def _generic_interaction_available(self, node_id: str) -> bool:
        node = self.nodes[node_id]
        return (
            node.get("node_type") != "NAVIGATION_POINT"
            and node.get("market_scale") not in {"", "NONE"}
        )

    def _merchant_contact_available(self, node_id: str) -> bool:
        return self.nodes[node_id].get("broker_availability") in {"LOW", "MEDIUM", "HIGH"}

    def _pilot_ids_for_route(
        self, node_id: str, route_id: str, on_date: date
    ) -> tuple[str, ...]:
        available: list[str] = []
        for row in self.pilot_routes:
            pilot_id = row["pilot_id"]
            pilot = self.pilots.get(pilot_id)
            if pilot is None:
                continue
            if row["route_id"] != route_id or row["competence"] != "CONFIRMED":
                continue
            if pilot["available_node"] != node_id:
                continue
            if not self._active(pilot, on_date) or not self._active(row, on_date):
                continue
            available.append(pilot_id)
        return tuple(sorted(available))

    def opportunities(
        self,
        node_id: str,
        on_date: date,
        *,
        channel: InformationChannel | None = None,
        used_ids: tuple[str, ...] = (),
    ) -> tuple[InformationOpportunity, ...]:
        """Retorna oportunidades estruturais, sem consultar estado da Coroa."""
        used = set(used_ids)
        result: list[InformationOpportunity] = []
        routes = self._outgoing_routes(node_id, on_date)

        for route in routes:
            route_id = route["route_id"]
            target = route["destination_node"]

            if channel in (None, InformationChannel.RUMOR) and self._generic_interaction_available(node_id):
                rule = self.rules[InformationChannel.RUMOR]
                key = f"RUMOR:{node_id}:{route_id}"
                if key not in used:
                    result.append(
                        InformationOpportunity(
                            opportunity_id=key,
                            channel=InformationChannel.RUMOR,
                            origin_node=node_id,
                            target_route_id=route_id,
                            target_node_id=target,
                            time_days=rule.time_days,
                            geo_min=rule.geo_min,
                            route_nav_min=rule.route_nav_min,
                            market_min=rule.market_min,
                            political_min=rule.political_min,
                        )
                    )

            if channel in (None, InformationChannel.MERCHANT_CONTACT) and self._merchant_contact_available(node_id):
                rule = self.rules[InformationChannel.MERCHANT_CONTACT]
                key = f"MERCHANT_CONTACT:{node_id}:{route_id}"
                if key not in used:
                    result.append(
                        InformationOpportunity(
                            opportunity_id=key,
                            channel=InformationChannel.MERCHANT_CONTACT,
                            origin_node=node_id,
                            target_route_id=route_id,
                            target_node_id=target,
                            time_days=rule.time_days,
                            geo_min=rule.geo_min,
                            route_nav_min=rule.route_nav_min,
                            market_min=rule.market_min,
                            political_min=rule.political_min,
                        )
                    )

            if channel in (None, InformationChannel.PILOT_CONSULTATION):
                rule = self.rules[InformationChannel.PILOT_CONSULTATION]
                for pilot_id in self._pilot_ids_for_route(node_id, route_id, on_date):
                    key = f"PILOT_CONSULTATION:{pilot_id}:{route_id}"
                    if key in used:
                        continue
                    result.append(
                        InformationOpportunity(
                            opportunity_id=key,
                            channel=InformationChannel.PILOT_CONSULTATION,
                            origin_node=node_id,
                            target_route_id=route_id,
                            target_node_id=target,
                            time_days=rule.time_days,
                            geo_min=rule.geo_min,
                            route_nav_min=rule.route_nav_min,
                            market_min=rule.market_min,
                            political_min=rule.political_min,
                            pilot_id=pilot_id,
                        )
                    )

        return tuple(sorted(result, key=lambda item: item.opportunity_id))

    @staticmethod
    def choose(
        opportunities: tuple[InformationOpportunity, ...],
        *,
        seed: int,
        node_id: str,
        on_date: date,
        channel: InformationChannel,
    ) -> InformationOpportunity | None:
        if not opportunities:
            return None
        rng = random.Random(
            f"information:{seed}:{node_id}:{on_date.isoformat()}:{channel.value}"
        )
        return opportunities[rng.randrange(len(opportunities))]
