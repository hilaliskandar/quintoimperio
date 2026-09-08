from datetime import date

from quintoimperio.domain.gama_1502_campaign import Gama1502CampaignModel
from quintoimperio.domain.stop import ChronologyMode


def test_gama_1502_minimal_sequence_reaches_cannanore_without_invented_observations():
    model = Gama1502CampaignModel()
    state = model.initial_gama_1502_state(provision_days=500.0)

    route_ids = []
    while state.active_expedition_id == model.EXPEDITION_ID:
        plan = model.plan_current_leg(state, seed=1502)
        assert plan.feasible, (
            state.vessel.location_node,
            state.vessel.clock.current_date,
            plan.blockers,
        )
        route_ids.append(plan.route_id)
        state = model.execute_voyage(state, plan)

    assert route_ids == [
        "R_LIS_SOF_GAMA1502",
        "R_SOF_KIL",
        "R_KIL_CAN_GAMA1502",
    ]
    assert state.vessel.location_node == "CAN"
    assert state.chronology_mode is ChronologyMode.GUIDED
    assert state.vessel.clock.current_date.year == 1502

    observations = model.session.travel.navigation.observations
    gama_1502_routes = set(route_ids)
    assert not any(row["route_id"] in gama_1502_routes for row in observations)


def test_gama_1502_departure_is_exact_but_does_not_force_later_daily_dates():
    model = Gama1502CampaignModel()
    state = model.initial_gama_1502_state(provision_days=500.0)
    assert state.vessel.clock.current_date == date(1502, 2, 1)

    plan = model.plan_current_leg(state, seed=1502)
    assert plan.route_id == "R_LIS_SOF_GAMA1502"
    assert not plan.events_suppressed_by_observation
    assert not plan.timing_events_suppressed_by_observation


def test_sodre_force_is_documentary_world_event_not_second_active_expedition():
    model = Gama1502CampaignModel()
    state = model.initial_gama_1502_state(provision_days=500.0)
    event = model.sodre_force_remains_event()

    assert state.active_expedition_id == model.EXPEDITION_ID
    assert event.trajectory_id == "SODRE_FORCE"
    assert event.event_type == "FORCE_REMAINS"
    assert event.date_from == date(1503, 1, 1)
    assert event.date_to == date(1503, 3, 31)
