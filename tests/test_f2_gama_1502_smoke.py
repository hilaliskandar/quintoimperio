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
    assert event.date_from == date(1503, 2, 23)
    assert event.date_to == date(1503, 2, 28)


def test_calcoen_witness_anchors_malabar_sequence_without_general_combat():
    model = Gama1502CampaignModel()
    events = {
        event.event_id: event
        for event in model.expedition_events.preferred_for_expedition(model.EXPEDITION_ID)
    }

    can_to_cal = events["GAMA1502_E04"]
    cal_to_coc = events["GAMA1502_E05"]
    cochin_audience = events["GAMA1502_E06"]
    cochin_departure = events["GAMA1503_E07"]
    calicut_engagement = events["GAMA1503_E08"]
    return_preparation = events["GAMA1503_E09"]

    assert can_to_cal.date_from == date(1502, 10, 27)
    assert can_to_cal.origin_node == "CAN"
    assert can_to_cal.destination_node == "CAL"
    assert can_to_cal.event_type == "FLEET_DEPARTURE"

    assert cal_to_coc.date_from == date(1502, 11, 2)
    assert cal_to_coc.origin_node == "CAL"
    assert cal_to_coc.destination_node == "COC"

    assert cochin_audience.date_from == date(1502, 11, 28)
    assert cochin_audience.event_type == "ROYAL_NEGOTIATION"

    assert cochin_departure.date_from == date(1503, 1, 3)
    assert cochin_departure.origin_node == "COC"

    assert calicut_engagement.date_from == date(1503, 2, 12)
    assert calicut_engagement.event_type == "NAVAL_ENGAGEMENT"

    assert return_preparation.date_from == date(1503, 2, 13)
    assert return_preparation.origin_node == "CAL"
    assert return_preparation.destination_node == "CAN"

    assert all("CALCOEN_1504" in event.source_id for event in (
        can_to_cal,
        cal_to_coc,
        cochin_audience,
        cochin_departure,
        calicut_engagement,
        return_preparation,
    ))


def test_return_split_is_range_not_invented_exact_departure():
    model = Gama1502CampaignModel()
    events = {
        event.event_id: event
        for event in model.expedition_events.preferred_for_expedition(model.EXPEDITION_ID)
    }

    resident = events["GAMA1502_E03"]
    departure = events["GAMA1503_E10"]

    assert resident.date_from == date(1503, 2, 23)
    assert resident.date_to == date(1503, 2, 28)
    assert resident.date_precision == "RANGE"

    assert departure.event_type == "RETURN_FLEET_DEPARTS"
    assert departure.origin_node == "CAN"
    assert departure.destination_node == "LIS"
    assert departure.date_from == date(1503, 2, 23)
    assert departure.date_to == date(1503, 2, 28)
    assert departure.date_precision == "RANGE"

    # O retorno fica documental: F2 não cria rota executável CAN→LIS.
    assert not any(
        leg.origin_node == "CAN" and leg.destination_node == "LIS"
        for leg in model.expeditions.legs
        if leg.expedition_id == model.EXPEDITION_ID
    )
