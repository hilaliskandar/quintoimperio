"""Mitigacao experimental de contingencias severas de provisoes.

A reserva segregada e um parametro de simulacao. Ela nao representa servico
portuario historico, nao aumenta o estoque embarcado e so afeta perdas do tipo
MAJOR_PROVISION_LOSS. O custo em capital e um trade-off abstrato de preparacao.
"""
from __future__ import annotations

from dataclasses import dataclass, replace

from .session import GameSessionState
from .travel import VoyagePlan
from .voyage_event import VoyageEvent, VoyageEventType

MAX_SECURED_RESERVE_DAYS = 20.0
SECURED_RESERVE_COST_PER_DAY = 0.25


@dataclass(frozen=True)
class SecuredReserveResult:
    secured_days: float
    capital_cost: float
    mitigated_days: float
    raw_event_provision_delta: float
    effective_event_provision_delta: float


def mitigate_events(
    events: tuple[VoyageEvent, ...], secured_days: float
) -> tuple[tuple[VoyageEvent, ...], float, float, float]:
    """Aplica a reserva apenas a MAJOR_PROVISION_LOSS.

    Retorna eventos efetivos, dias mitigados, delta bruto e delta efetivo.
    """
    remaining = max(0.0, float(secured_days))
    mitigated = 0.0
    raw_total = sum(event.provision_delta for event in events)
    adjusted: list[VoyageEvent] = []
    for event in events:
        if (
            event.event_type is VoyageEventType.MAJOR_PROVISION_LOSS
            and event.provision_delta < 0
            and remaining > 0
        ):
            shield = min(remaining, -event.provision_delta)
            remaining -= shield
            mitigated += shield
            event = replace(event, provision_delta=event.provision_delta + shield)
        adjusted.append(event)
    effective_total = sum(event.provision_delta for event in adjusted)
    return tuple(adjusted), mitigated, raw_total, effective_total


def secure_provision_reserve_for_voyage(
    session,
    state: GameSessionState,
    plan: VoyagePlan,
    secured_days: float,
) -> tuple[GameSessionState, VoyagePlan, SecuredReserveResult]:
    """Paga o preparo e resolve a contingencia sem antecipar o evento ao jogador."""
    secured = float(secured_days)
    if secured < 0 or secured > MAX_SECURED_RESERVE_DAYS:
        raise ValueError("secured_days deve permanecer entre 0 e 20")
    if secured > state.vessel.provision_days:
        raise ValueError("reserva protegida nao pode exceder provisoes embarcadas")
    cost = secured * SECURED_RESERVE_COST_PER_DAY
    if cost > state.commerce.capital_index:
        raise ValueError("capital insuficiente para preparar reserva segregada")

    prepared_state = replace(
        state,
        commerce=replace(
            state.commerce,
            capital_index=state.commerce.capital_index - cost,
        ),
    )
    resolved = session.travel.resolve_voyage(state.vessel, plan)
    events, mitigated, raw_delta, effective_delta = mitigate_events(
        resolved.events, secured
    )
    if mitigated:
        provision_after = max(
            0.0,
            state.vessel.provision_days
            - resolved.provision_days_required
            + effective_delta,
        )
        resolved = replace(
            resolved,
            events=events,
            event_provision_delta=effective_delta,
            provision_days_after=provision_after,
        )
    result = SecuredReserveResult(
        secured_days=secured,
        capital_cost=cost,
        mitigated_days=mitigated,
        raw_event_provision_delta=raw_delta,
        effective_event_provision_delta=effective_delta,
    )
    return prepared_state, resolved, result
