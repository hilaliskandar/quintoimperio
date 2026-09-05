"""Inspeção textual dos serviços portuários mínimos v0.1."""

from datetime import date

from quintoimperio.domain import (
    GameClock,
    PortServiceKind,
    PortServiceModel,
    VesselState,
)


if __name__ == "__main__":
    model = PortServiceModel()

    print("Quinto Império — serviços portuários v0.1")
    print("Capacidades, duração e condição são escalas de simulação, não medidas históricas.")
    print()

    for node_id in ("LIS", "CEU", "MAL", "CGH"):
        provision = model.quote(node_id, PortServiceKind.PROVISIONS)
        repair = model.quote(node_id, PortServiceKind.REPAIR)
        print(
            f"{node_id}: provisões={provision.availability.value} "
            f"reparo={repair.availability.value}"
        )

    state = VesselState(
        location_node="LIS",
        clock=GameClock(date(1497, 7, 1)),
        provision_days=20.0,
        condition=70.0,
    )
    provisioned = model.reprovision(state, "LIS", requested_days=30.0)
    repaired = model.repair(provisioned.state_after, "LIS", requested_points=20.0)

    print()
    print(
        f"Lisboa/reabastecimento: +{provisioned.effect:.1f} dias-equivalentes; "
        f"data={provisioned.state_after.clock.current_date.isoformat()}"
    )
    print(
        f"Lisboa/reparo: +{repaired.effect:.1f} pontos abstratos; "
        f"data={repaired.state_after.clock.current_date.isoformat()}"
    )

    malindi_state = VesselState(
        location_node="MAL",
        clock=GameClock(date(1498, 4, 16)),
        provision_days=25.0,
        condition=80.0,
    )
    unknown = model.reprovision(malindi_state, "MAL", requested_days=10.0)
    print(
        "Melinde/reabastecimento com evidência atual:",
        unknown.success,
        unknown.blockers,
    )
