from dataclasses import replace
from datetime import date

from quintoimperio.domain.calendar import GameClock
from quintoimperio.domain.joao_nova_campaign import JoaoNovaCampaignModel
from quintoimperio.domain.stop import ChronologyMode
from quintoimperio.domain.travel import NavigationBasis


def test_joao_nova_departs_without_cabral_malabar_warning():
    model = JoaoNovaCampaignModel()
    state = model.initial_joao_nova_state()

    assert state.vessel.location_node == "LIS"
    assert state.vessel.clock.current_date == date(1501, 3, 5)
    assert state.active_expedition_id == model.EXPEDITION_ID
    assert not model.joao_nova_has_malabar_warning(state)
    assert not model.can_acquire_malabar_warning(state)


def test_warning_is_acquired_only_at_sao_bras_inside_documented_window_and_is_one_shot():
    model = JoaoNovaCampaignModel()
    initial = model.initial_joao_nova_state()
    event = model.malabar_warning_event()

    assert event.origin_node == "SBR"
    assert event.destination_node == "SBR"
    assert event.event_type == "INFORMATION_ACQUISITION"
    assert event.date_from == date(1501, 5, 1)
    assert event.date_to == date(1501, 8, 31)

    at_sao_bras = replace(
        initial,
        vessel=replace(
            initial.vessel,
            location_node="SBR",
            clock=GameClock(event.date_to),
        ),
    )
    assert model.can_acquire_malabar_warning(at_sao_bras)

    informed = model.acquire_malabar_warning(at_sao_bras)
    assert model.joao_nova_has_malabar_warning(informed)
    assert informed.information_history.count(model.MALABAR_WARNING_KEY) == 1
    assert not model.can_acquire_malabar_warning(informed)

    repeated = model.acquire_malabar_warning(informed)
    assert repeated == informed


def test_first_leg_without_daily_observation_uses_simulated_timing_and_stays_guided():
    model = JoaoNovaCampaignModel()
    state = model.initial_joao_nova_state(provision_days=180.0)

    assert model.guided_departure_date(state) is None
    plan = model.plan_current_leg(state, seed=1501)

    assert plan.feasible, plan.blockers
    assert plan.route_id == "R_LIS_SBR_NOVA"
    assert plan.navigation_basis is NavigationBasis.FLEET_COMMAND
    assert not plan.timing_events_suppressed_by_observation
    assert not plan.events_suppressed_by_observation
    assert plan.departure_date == date(1501, 3, 5)
    assert plan.travel_days >= 1

    after = model.execute_voyage(state, plan)
    assert after.vessel.location_node == "SBR"
    assert after.chronology_mode is ChronologyMode.GUIDED
    assert after.active_expedition_id == model.EXPEDITION_ID
    assert after.expedition_leg_sequence == 2


def test_simulated_arrival_at_sao_bras_falls_inside_documented_warning_window():
    model = JoaoNovaCampaignModel()
    state = model.initial_joao_nova_state(provision_days=180.0)
    plan = model.plan_current_leg(state, seed=1501)
    after = model.execute_voyage(state, plan)
    event = model.malabar_warning_event()

    assert event.date_from <= after.vessel.clock.current_date <= event.date_to, (
        after.vessel.clock.current_date,
        event.date_from,
        event.date_to,
    )
    assert model.can_acquire_malabar_warning(after)


def test_sao_bras_warning_is_required_before_historical_route_continues():
    model = JoaoNovaCampaignModel()
    state = model.initial_joao_nova_state(provision_days=180.0)
    first = model.plan_current_leg(state, seed=1501)
    at_sao_bras = model.execute_voyage(state, first)

    blocked = model.plan_current_leg(at_sao_bras, seed=1501)
    assert blocked.route_id == "R_SBR_KIL_NOVA"
    assert not blocked.feasible
    assert model.WARNING_REQUIRED_BLOCKER in blocked.blockers

    informed = model.acquire_malabar_warning(at_sao_bras)
    released = model.plan_current_leg(informed, seed=1501)
    assert model.WARNING_REQUIRED_BLOCKER not in released.blockers
    assert released.navigation_basis is NavigationBasis.FLEET_COMMAND


def test_joao_nova_route_order_avoids_calicut():
    model = JoaoNovaCampaignModel()
    legs = model.session.expedition.legs[model.EXPEDITION_ID]
    route_ids = [leg.route_id for leg in legs]

    assert route_ids == [
        "R_LIS_SBR_NOVA",
        "R_SBR_KIL_NOVA",
        "R_KIL_MAL_NOVA",
        "R_MAL_ANJ_NOVA",
        "R_ANJ_CAN_NOVA",
        "R_CAN_COC_NOVA",
        "R_COC_CAN_NOVA",
    ]
    destinations = [model.session.routes[route_id]["destination_node"] for route_id in route_ids]
    assert destinations == ["SBR", "KIL", "MAL", "ANJ", "CAN", "COC", "CAN"]
    assert "CAL" not in destinations
