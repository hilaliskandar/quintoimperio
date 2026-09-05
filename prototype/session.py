#!/usr/bin/env python3
"""Inspeção do primeiro loop integrado sem interface gráfica final."""

from datetime import date

from quintoimperio.domain import (
    AccessStatus,
    GameSessionModel,
    KnowledgeLevel,
    KnowledgeState,
)


def expedition_command_demo(model: GameSessionModel) -> None:
    print("A) Participação institucional: armada de Vasco da Gama, Lisboa -> São Thiago")
    state = model.initial_state(
        active_expedition_id="EXP_GAMA_1497",
        provision_days=90.0,
    )
    before = model.route_nav(state, "R_LIS_STG")
    print("  conhecimento pessoal da rota antes:", before.name)
    print(
        "  expedição ativa:",
        state.active_expedition_id,
        "perna",
        state.expedition_leg_sequence,
    )
    plan = model.plan_voyage(state, "R_LIS_STG", seed=1497)
    print("  viagem autorizada:", plan.feasible, plan.navigation_basis.value if plan.navigation_basis else None)
    print("  duração histórica observada:", plan.travel_days, "dias")
    print("  conhecimento pessoal continua:", model.route_nav(state, "R_LIS_STG").name)
    if plan.feasible:
        arrived = model.execute_voyage(state, plan)
        print("  chegada:", arrived.vessel.location_node, arrived.vessel.clock.current_date)
        print("  conhecimento após percorrer a rota:", model.route_nav(arrived, "R_LIS_STG").name)
        print("  próxima perna institucional:", arrived.expedition_leg_sequence)
    aggregate = model.plan_voyage(state, "R_LIS_CGH", seed=1497)
    print("  Lisboa->Cabo agregado executável:", aggregate.feasible, aggregate.blockers)
    print()


def historical_learning_demo(model: GameSessionModel) -> None:
    print("B) Aprendizagem histórica de rota e acesso: Melinde -> Calecute, 1498")
    state = model.initial_state(
        location_node="MAL",
        start_date=date(1498, 4, 24),
        provision_days=50.0,
    )
    without_pilot = model.plan_voyage(state, "R_MAL_CAL", seed=1498)
    print("  sem piloto:", without_pilot.feasible, without_pilot.blockers)
    plan = model.plan_voyage(
        state,
        "R_MAL_CAL",
        pilot_id="PIL_MAL_GUJ_1498",
        seed=1498,
    )
    print("  com piloto documentado:", plan.feasible, plan.navigation_basis.value)
    arrived = model.execute_voyage(state, plan)
    print("  chegada:", arrived.vessel.location_node, arrived.vessel.clock.current_date)
    print("  conhecimento da rota:", model.route_nav(arrived, "R_MAL_CAL").name)
    print("  conhecimento do mercado de Calecute:", model.node_state(arrived, "CAL").market.name)
    access = model.access_view(arrived)
    print("  acesso institucional:", access.status.value, "negociável=", access.negotiable)
    print("  mercado acionável antes da negociação:", model.market_view(arrived, seed=1498).actionable)
    negotiated = model.negotiate_access(arrived)
    print("  negociação genérica:", negotiated.executed, "dias=", negotiated.days_spent)
    print("  mercado acionável depois:", model.market_view(negotiated.state_after, seed=1498).actionable)
    print()


def integration_demo(model: GameSessionModel) -> None:
    print("C) Cenário técnico de integração: Calecute -> Aden")
    print("   NÃO representa o estado histórico inicial do personagem.")
    state = model.initial_state(
        location_node="CAL",
        start_date=date(1498, 5, 22),
        provision_days=200.0,
        capital_index=100.0,
        capacity_total=30.0,
    )
    cal = model.node_state(state, "CAL")
    state = model.scenario_set_node_knowledge(
        state,
        "CAL",
        KnowledgeState(
            geo=cal.geo,
            nav=cal.nav,
            market=KnowledgeLevel.OPERATIONAL,
            political=cal.political,
        ),
    )
    state = model.scenario_set_route_knowledge(
        state, "R_CAL_ADE", KnowledgeLevel.OPERATIONAL
    )
    state = model.scenario_set_access(state, "CAL", AccessStatus.NEGOTIATED)

    market = model.market_view(state, seed=1498)
    print("  mercado CAL operacional e com acesso:", market.actionable)
    print("  bens visíveis:", ", ".join(entry.good_id for entry in market.entries))

    bought = model.buy(state, "PEPPER", 2.0, seed=1498)
    print("  compra de pimenta:", bought.executed, bought.reasons)
    state = bought.state_after
    print(
        f"  capital={state.commerce.capital_index:.2f}; "
        f"pimenta={state.commerce.quantity_of('PEPPER'):.2f}"
    )

    plan = model.plan_voyage(state, "R_CAL_ADE", seed=1498)
    print(
        f"  viagem CAL->ADE: {plan.feasible}; {plan.travel_days} dias; "
        f"chegada={plan.arrival_date}"
    )
    state = model.execute_voyage(state, plan)
    print("  acesso ADE na chegada:", model.access_view(state).status.value)
    print("  mercado ADE acionável antes de negociar:", model.market_view(state, seed=1498).actionable)
    access = model.negotiate_access(state)
    state = access.state_after
    print("  negociação ADE:", access.executed, "dias=", access.days_spent)

    sold = model.sell(state, "PEPPER", 2.0, seed=1498)
    state = sold.state_after
    print("  venda de pimenta:", sold.executed, sold.reasons)
    print(
        f"  capital final={state.commerce.capital_index:.2f}; "
        f"pimenta={state.commerce.quantity_of('PEPPER'):.2f}"
    )


def main() -> None:
    print("Quinto Império — sessão integrada v0.1")
    print("Todos os valores econômicos, de capacidade e tempos genéricos abaixo são simulação.")
    print()
    model = GameSessionModel()
    expedition_command_demo(model)
    historical_learning_demo(model)
    integration_demo(model)


if __name__ == "__main__":
    main()
