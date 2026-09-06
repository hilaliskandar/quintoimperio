"""Eventos marítimos genéricos de simulação v0.4.

Nenhum evento deste módulo é tratado como incidente histórico documentado. As
regras vivem em ``simulation/voyage_event_rules.csv``. A camada admite efeitos
positivos e negativos sobre provisões e condição, preservando a
reprodutibilidade por seed. Em pernas com timing histórico observado, apenas
regras explicitamente marcadas como ``observed_timing_safe`` podem ocorrer.
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
    PROVISION_SPOILAGE = "PROVISION_SPOILAGE"
    EFFICIENT_RATIONING = "EFFICIENT_RATIONING"
    MAJOR_PROVISION_LOSS = "MAJOR_PROVISION_LOSS"
    STRUCTURAL_STRAIN = "STRUCTURAL_STRAIN"


@dataclass(frozen=True)
class VoyageEvent:
    event_id: str
    event_type: VoyageEventType
    route_id: str
    departure_date: date
    extra_days: int
    condition_loss: float
    provision_delta: float = 0.0
    observed_timing_safe: bool = False
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
    provision_delta_min: float
    provision_delta_max: float
    observed_timing_safe: bool


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
                provision_delta_min=float(row.get("provision_delta_min", "0") or 0),
                provision_delta_max=float(row.get("provision_delta_max", "0") or 0),
                observed_timing_safe=(row.get("observed_timing_safe", "").upper() == "TRUE"),
            )
            for row in repository.simulation("voyage_event_rules.csv")
        )

    @staticmethod
    def _matches_value(rule_values: tuple[str, ...], actual: str) -> bool:
        return not rule_values or "ANY" in rule_values or actual in rule_values

    def applicable_rules(
        self,
        route_id: str,
        departure: date,
        *,
        timing_safe_only: bool = False,
    ) -> tuple[VoyageEventRule, ...]:
        route = self.routes[route_id]
        route_type = route.get("route_type", "") or "ANY"
        monsoon = route.get("monsoon_dependence", "") or "NONE"
        result: list[VoyageEventRule] = []
        for rule in self.rules:
            if timing_safe_only and not rule.observed_timing_safe:
                continue
            if rule.route_type not in {"ANY", route_type}:
                continue
            if not self._matches_value(rule.monsoon_dependence, monsoon):
                continue
            if rule.months and departure.month not in rule.months:
                continue
            result.append(rule)
        return tuple(result)

    def select(
        self,
        route_id: str,
        departure: date,
        *,
        seed: int = 0,
        timing_safe_only: bool = False,
    ) -> tuple[VoyageEvent, ...]:
        rules = self.applicable_rules(
            route_id,
            departure,
            timing_safe_only=timing_safe_only,
        )
        if not rules:
            return ()

        # O prefixo v02 é mantido deliberadamente para preservar a sequência
        # pseudoaleatória já usada nas ondas anteriores. Novas regras são
        # anexadas à cauda da distribuição, em vez de reembaralhar seeds antigas.
        rng = random.Random(
            f"voyage-event:v02:{seed}:{route_id}:{departure.isoformat()}:{int(timing_safe_only)}"
        )
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
        if selected.provision_delta_min == selected.provision_delta_max:
            provision_delta = selected.provision_delta_min
        else:
            provision_delta = rng.uniform(
                selected.provision_delta_min, selected.provision_delta_max
            )
        return (
            VoyageEvent(
                event_id=selected.event_id,
                event_type=selected.event_type,
                route_id=route_id,
                departure_date=departure,
                extra_days=extra_days,
                condition_loss=condition_loss,
                provision_delta=provision_delta,
                observed_timing_safe=selected.observed_timing_safe,
            ),
        )
