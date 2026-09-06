"""Persistência JSON versionada da campanha do MVP.

O formato registra somente estado pertencente ao domínio e a seed usada pela
sessão. Estado efêmero da interface, como seleção visual, histórico curto ou
modal de confirmação, não participa do save.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from .access import AccessStatus
from .calendar import GameClock
from .knowledge import KnowledgeLevel, KnowledgeState
from .port import PortServiceKind, ServiceAvailability
from .relationship import RelationshipStatus
from .service_knowledge import (
    ServiceAwareSessionState,
    ServiceKnowledgeRecord,
    ServiceKnowledgeStatus,
)
from .session import (
    AccessRecord,
    GameSessionState,
    NodeKnowledgeRecord,
    RelationshipRecord,
    RouteKnowledgeRecord,
)
from .stop import ChronologyMode
from .trade import CargoHolding, CommercialState
from .travel import VesselState
from .voyage_event import VoyageEvent, VoyageEventType


SAVE_SCHEMA_VERSION = 2
SUPPORTED_SCHEMA_VERSIONS = (1, 2)


@dataclass(frozen=True)
class CampaignSave:
    schema_version: int
    seed: int
    state: GameSessionState


class CampaignPersistence:
    """Converte ``GameSessionState`` para JSON e migra saves v1 sem inferir fatos."""

    schema_version = SAVE_SCHEMA_VERSION

    @staticmethod
    def _event_to_dict(event: VoyageEvent) -> dict[str, Any]:
        return {
            "event_id": event.event_id,
            "event_type": event.event_type.value,
            "route_id": event.route_id,
            "departure_date": event.departure_date.isoformat(),
            "extra_days": event.extra_days,
            "condition_loss": event.condition_loss,
            "simulation_only": event.simulation_only,
        }

    def to_dict(self, state: GameSessionState, *, seed: int) -> dict[str, Any]:
        service_records = tuple(getattr(state, "service_knowledge_records", ()))
        return {
            "schema_version": self.schema_version,
            "seed": int(seed),
            "state": {
                "vessel": {
                    "location_node": state.vessel.location_node,
                    "current_date": state.vessel.clock.current_date.isoformat(),
                    "provision_days": state.vessel.provision_days,
                    "condition": state.vessel.condition,
                },
                "commerce": {
                    "capital_index": state.commerce.capital_index,
                    "capacity_total": state.commerce.capacity_total,
                    "cargo": [
                        {"good_id": item.good_id, "quantity": item.quantity}
                        for item in state.commerce.cargo
                    ],
                },
                "node_knowledge": [
                    {
                        "node_id": record.node_id,
                        "geo": int(record.state.geo),
                        "nav": int(record.state.nav),
                        "market": int(record.state.market),
                        "political": int(record.state.political),
                    }
                    for record in state.node_knowledge
                ],
                "route_knowledge": [
                    {"route_id": record.route_id, "nav": int(record.nav)}
                    for record in state.route_knowledge
                ],
                "access_records": [
                    {"node_id": record.node_id, "status": record.status.value}
                    for record in state.access_records
                ],
                "relationship_records": [
                    {"actor_id": record.actor_id, "status": int(record.status)}
                    for record in state.relationship_records
                ],
                "service_knowledge_records": [
                    {
                        "node_id": record.node_id,
                        "service": record.service.value,
                        "status": record.status.value,
                        "revealed_availability": (
                            None
                            if record.revealed_availability is None
                            else record.revealed_availability.value
                        ),
                    }
                    for record in service_records
                ],
                "active_expedition_id": state.active_expedition_id,
                "expedition_leg_sequence": state.expedition_leg_sequence,
                "chronology_mode": state.chronology_mode.value,
                "active_stop_id": state.active_stop_id,
                "information_history": list(state.information_history),
                "voyage_event_history": [
                    self._event_to_dict(event) for event in state.voyage_event_history
                ],
            },
        }

    @staticmethod
    def _require_mapping(payload: Any, name: str) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise ValueError(f"Campo {name} deve ser um objeto JSON")
        return payload

    def from_dict(self, payload: dict[str, Any]) -> CampaignSave:
        data = self._require_mapping(payload, "save")
        version = data.get("schema_version")
        if version not in SUPPORTED_SCHEMA_VERSIONS:
            raise ValueError(
                f"Versão de save não suportada: {version!r}; esperadas {SUPPORTED_SCHEMA_VERSIONS}"
            )
        if "seed" not in data:
            raise ValueError("Save sem seed")
        raw = self._require_mapping(data.get("state"), "state")
        vessel_raw = self._require_mapping(raw.get("vessel"), "state.vessel")
        commerce_raw = self._require_mapping(raw.get("commerce"), "state.commerce")

        vessel = VesselState(
            location_node=str(vessel_raw["location_node"]),
            clock=GameClock(date.fromisoformat(str(vessel_raw["current_date"]))),
            provision_days=float(vessel_raw["provision_days"]),
            condition=float(vessel_raw["condition"]),
        )
        commerce = CommercialState(
            capital_index=float(commerce_raw["capital_index"]),
            capacity_total=float(commerce_raw["capacity_total"]),
            cargo=tuple(
                CargoHolding(good_id=str(item["good_id"]), quantity=float(item["quantity"]))
                for item in commerce_raw.get("cargo", [])
            ),
        )
        node_knowledge = tuple(
            NodeKnowledgeRecord(
                node_id=str(item["node_id"]),
                state=KnowledgeState(
                    geo=KnowledgeLevel(int(item["geo"])),
                    nav=KnowledgeLevel(int(item["nav"])),
                    market=KnowledgeLevel(int(item["market"])),
                    political=KnowledgeLevel(int(item["political"])),
                ),
            )
            for item in raw.get("node_knowledge", [])
        )
        route_knowledge = tuple(
            RouteKnowledgeRecord(route_id=str(item["route_id"]), nav=KnowledgeLevel(int(item["nav"])))
            for item in raw.get("route_knowledge", [])
        )
        access_records = tuple(
            AccessRecord(node_id=str(item["node_id"]), status=AccessStatus(str(item["status"])))
            for item in raw.get("access_records", [])
        )
        relationship_records = tuple(
            RelationshipRecord(
                actor_id=str(item["actor_id"]),
                status=RelationshipStatus(int(item["status"])),
            )
            for item in raw.get("relationship_records", [])
        )
        service_knowledge_records = tuple(
            ServiceKnowledgeRecord(
                node_id=str(item["node_id"]),
                service=PortServiceKind(str(item["service"])),
                status=ServiceKnowledgeStatus(str(item["status"])),
                revealed_availability=(
                    None
                    if item.get("revealed_availability") is None
                    else ServiceAvailability(str(item["revealed_availability"]))
                ),
            )
            for item in raw.get("service_knowledge_records", [])
        )
        events = tuple(
            VoyageEvent(
                event_id=str(item["event_id"]),
                event_type=VoyageEventType(str(item["event_type"])),
                route_id=str(item["route_id"]),
                departure_date=date.fromisoformat(str(item["departure_date"])),
                extra_days=int(item["extra_days"]),
                condition_loss=float(item["condition_loss"]),
                simulation_only=bool(item.get("simulation_only", True)),
            )
            for item in raw.get("voyage_event_history", [])
        )
        state = ServiceAwareSessionState(
            vessel=vessel,
            commerce=commerce,
            node_knowledge=node_knowledge,
            route_knowledge=route_knowledge,
            access_records=access_records,
            relationship_records=relationship_records,
            active_expedition_id=raw.get("active_expedition_id"),
            expedition_leg_sequence=(
                None
                if raw.get("expedition_leg_sequence") is None
                else int(raw["expedition_leg_sequence"])
            ),
            chronology_mode=ChronologyMode(str(raw["chronology_mode"])),
            active_stop_id=raw.get("active_stop_id"),
            information_history=tuple(str(value) for value in raw.get("information_history", [])),
            voyage_event_history=events,
            service_knowledge_records=service_knowledge_records,
        )
        return CampaignSave(schema_version=int(version), seed=int(data["seed"]), state=state)

    def dumps(self, state: GameSessionState, *, seed: int) -> str:
        return json.dumps(
            self.to_dict(state, seed=seed),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ) + "\n"

    def loads(self, text: str) -> CampaignSave:
        try:
            payload = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Save JSON inválido: {exc.msg}") from exc
        return self.from_dict(payload)

    def save_file(self, path: str | Path, state: GameSessionState, *, seed: int) -> Path:
        target = Path(path)
        target.write_text(self.dumps(state, seed=seed), encoding="utf-8")
        return target

    def load_file(self, path: str | Path) -> CampaignSave:
        return self.loads(Path(path).read_text(encoding="utf-8"))
