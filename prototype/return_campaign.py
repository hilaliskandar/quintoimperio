#!/usr/bin/env python3
"""Smoke reproduzível do retorno documental Calecute -> Baixos do Rio Grande."""

from datetime import date

from quintoimperio.domain.return_campaign import ReturnCampaignModel
from quintoimperio.domain.stop import ChronologyMode


def main() -> None:
    model = ReturnCampaignModel()
    state = model.session.initial_state(
        location_node="CAL",
        start_date=date(1498, 5, 22),
        provision_days=120.0,
        active_expedition_id=None,
        chronology_mode=ChronologyMode.GUIDED,
    )
    state = model.activate_return(state)
    completed = []

    while state.active_expedition_id == model.RETURN_EXPEDITION_ID:
        if model.documented_stop_can_reprovision(state):
            result = model.reprovision_at_documented_stop(state, 120.0)
            if result.executed:
                state = result.state_after

        departure = model.guided_departure_date(state)
        if departure is not None and state.vessel.clock.current_date < departure:
            waited = model.wait_for_guided_departure(state)
            if not waited.executed:
                raise RuntimeError(waited.reasons)
            state = waited.state_after

        leg = model.current_leg(state)
        if leg is None:
            raise RuntimeError("Retorno ativo sem perna corrente")
        plan = model.plan_current_leg(state, seed=1499)
        if not plan.feasible:
            raise RuntimeError(
                f"Perna bloqueada {leg.route_id}: {plan.blockers}; "
                f"provisoes={state.vessel.provision_days:.2f}"
            )
        completed.append(leg.route_id)
        state = model.execute_voyage(state, plan)

    expected = [
        "R_CAL_ANJ",
        "R_ANJ_MAL",
        "R_MAL_BSR",
        "R_BSR_SBR",
        "R_SBR_CGH_RET",
        "R_CGH_BRG",
    ]
    if completed != expected:
        raise RuntimeError(f"Sequencia inesperada: {completed}")
    if state.vessel.location_node != "BRG":
        raise RuntimeError(f"Destino final inesperado: {state.vessel.location_node}")
    if state.vessel.clock.current_date != date(1499, 4, 25):
        raise RuntimeError(f"Data final inesperada: {state.vessel.clock.current_date}")
    if state.chronology_mode is not ChronologyMode.GUIDED:
        raise RuntimeError(f"Cronologia final inesperada: {state.chronology_mode}")

    print("Quinto Imperio — smoke P1-func")
    print("Rotas:", " -> ".join(completed))
    print("Destino:", state.vessel.location_node)
    print("Data:", state.vessel.clock.current_date.isoformat())
    print("Cronologia:", state.chronology_mode.value)
    print("OK")


if __name__ == "__main__":
    main()
