"""Relatorio textual do estado de viagem e pilotos v0.1."""

from datetime import date

from quintoimperio.domain import GameClock, KnowledgeLevel, TravelModel, VesselState


if __name__ == "__main__":
    model = TravelModel()
    state = VesselState(
        location_node="MAL",
        clock=GameClock(date(1498, 4, 24)),
        provision_days=40.0,
        condition=100.0,
    )
    blocked = model.plan_voyage(
        state,
        "R_MAL_CAL",
        KnowledgeLevel.RUMORED,
        seed=1498,
    )
    guided = model.plan_voyage(
        state,
        "R_MAL_CAL",
        KnowledgeLevel.RUMORED,
        pilot_id="PIL_MAL_GUJ_1498",
        seed=1498,
    )

    print("Quinto Imperio — viagem e pilotos v0.1")
    print("Provisoes e condicao sao escalas abstratas de simulacao, nao unidades historicas.")
    print("Sem piloto e com conhecimento apenas rumoreado:", blocked.feasible, blocked.blockers)
    print("Com piloto guzerate documentado em Melinde:", guided.feasible, guided.navigation_basis.value)
    print(f"Duracao estimada: {guided.estimated_duration_days:.1f} dias; dias inteiros de jogo: {guided.travel_days}")
    print(f"Chegada simulada: {guided.arrival_date.isoformat()}")
    print(f"Provisoes: {state.provision_days:.1f} -> {guided.provision_days_after:.1f} dias-equivalentes")
    print(f"Condicao: {state.condition:.1f} -> {guided.condition_after:.1f} pontos")
