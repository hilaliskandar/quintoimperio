from dataclasses import replace
from datetime import date

from quintoimperio.domain.calendar import GameClock
from quintoimperio.domain.joao_nova_campaign import JoaoNovaCampaignModel


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
