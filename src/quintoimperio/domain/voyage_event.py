"""Eventos marítimos genéricos de simulação para viagens não fixadas pela evidência.

Nenhum evento deste módulo é tratado como incidente histórico documentado. As
regras vivem em ``simulation/voyage_event_rules.csv`` e só podem acrescentar
tempo e perda abstrata de condição na v0.1.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import date
from enum import Enum
from pathlib import Path

from quintoimperio.data.loader import RepositoryData


class VoyageEventType(str, Enum):
    CALM_DELAY = "CALM_DELAY"
    ROUGH_WEATHER = "ROUGH_WEATHER"
    MINOR_RIGGING_DAMAGE = "MINOR_RIGGING_DAMAGE"
    JUNE_JULY_DISRUPTION = "JUNE_JULY_DISRUPTION"


@dataclass(frozen=True)
class VoyageEvent:
    event_id: str
    event_type: VoyageEventType
    route_id: str
    departure_date: date
    extra_days: int
    condition_loss: float
    simulation_only: bool = True


@dataclass(frozen=True)
class VoyageEventRule:
    event_id: str
    event_type: VoyageEventType
    route_type: str
    monsoon_dependence: tuple[str, ...]
    months: tuple[int, ...]
    probability: float
    extra_days_min: int
    extra_days_max: int
    condition_loss_min: float
    condition_loss_max: float


class VoyageEventModel:
    """Seleciona no máximo um evento por viagem de forma determinística."""

    def __init__(self, root: Path | None = None) -> None:
        repository = RepositoryData(root)
        self.root = repository.root
        self.routes = {
            row["route_id"]: row for row in repository.historical("routes.csv")
        }
        self.rules: tuple[VoyageEventRule, ...] = tuple(
            VoyageEventRule(
                event_id=row["event_id"],
                event_type=VoyageEventType(row["event_type"]),
                route_type=row["route_type"],
                monsoon_dependence=tuple(
                    value for value in row["monsoon_dependence"].split("|") if value
                ),
                months=tuple(int(value) for value in row["months"].split("|") if value),
                probability=float(row["probability"]),
                extra_days_min=int(row["extra_days_min"]),
                extra_days_max=int(row["extra_days_max"]),
                condition_loss_min=float(row["condition_loss_min"]),
                condition_loss_max=float(row["condition_loss_max"]),
            )
            for row in repository.simulation("voyage_event_rules.csv")
        )

    @staticmethod
    def _matches_value(rule_values: tuple[str, ...], actual: str) -> bool:
        return not rule_values or "ANY" in rule_values or actual in rule_values

    def applicable_rules(self, route_id: str, departure: date) -> tuple[VoyageEventRule, ...]:
        route = self.routes[route_id]
        route_type = route.get("route_type", "") or "ANY"
        monsoon = route.get("monsoon_dependence", "") or "NONE"
        result: list[VoyageEventRule] = []
        for rule in self.rules:
            if rule.route_type not in {"ANY", route_type}:
                continue
            if not self._matches_value(rule.monsoon_dependence, monsoon):
                continue
            if rule.months and departure.month not in rule.months:
                continue
            result.append(rule)
        return tuple(result)

    def select(self, route_id: str, departure: date, *, seed: int = 0) -> tuple[VoyageEvent, ...]:
        rules = self.applicable_rules(route_id, departure)
        if not rules:
            return ()

        rng = random.Random(f"voyage-event:{seed}:{route_id}:{departure.isoformat()}")
        roll = rng.random()
        cumulative = 0.0
        selected: VoyageEventRule | None = None
        for rule in rules:
            cumulative += rule.probability
            if roll < cumulative:
                selected = rule
                break
        if selected is None:
            return ()

        extra_days = rng.randint(selected.extra_days_min, selected.extra_days_max)
        if selected.condition_loss_min == selected.condition_loss_max:
            condition_loss = selected.condition_loss_min
        else:
            condition_loss = rng.uniform(
                selected.condition_loss_min, selected.condition_loss_max
            )
        return (
            VoyageEvent(
                event_id=selected.event_id,
                event_type=selected.event_type,
                route_id=route_id,
                departure_date=departure,
                extra_days=extra_days,
                condition_loss=condition_loss,
            ),
        )
