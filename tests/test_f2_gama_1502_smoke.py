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


def test_malabar_reorganization_is_conservative_and_preserves_local_sovereignty():
    model = Gama1502CampaignModel()

    before_cochin = model.malabar_institutional_state("COC", date(1502, 12, 30))
    after_cochin = model.malabar_institutional_state("COC", date(1502, 12, 31))
    before_cannanore = model.malabar_institutional_state("CAN", date(1502, 12, 30))
    after_cannanore = model.malabar_institutional_state("CAN", date(1502, 12, 31))

    assert "COC1502_E01" not in before_cochin.applied_event_ids
    assert "COC1502_E01" in after_cochin.applied_event_ids
    assert after_cochin.institutional_presence == "FACTORY_REORGANIZED"
    assert "Perumpadappu" in after_cochin.sovereignty_note

    assert "CAN1502_E01" not in before_cannanore.applied_event_ids
    assert "CAN1502_E01" in after_cannanore.applied_event_ids
    assert after_cannanore.institutional_presence == "FACTORY_REORGANIZED"
    assert "Kolathunad" in after_cannanore.sovereignty_note


def test_sodre_force_is_documentary_world_event_not_second_active_expedition():
    model = Gama1502CampaignModel()
    state = model.initial_gama_1502_state(provision_days=500.0)
    event = model.sodre_force_remains_event()

    assert state.active_expedition_id == model.EXPEDITION_ID
    assert event.trajectory_id == "SODRE_FORCE"
    assert event.event_type == "FORCE_REMAINS"
    assert event.date_from == date(1503, 1, 1)
    assert event.date_to == date(1503, 3, 31)
