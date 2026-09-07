from datetime import date

from quintoimperio.domain.joao_nova_campaign import JoaoNovaCampaignModel
from quintoimperio.domain.stop import ChronologyMode


def test_joao_nova_commercial_sequence_reaches_cannanore_without_invented_observations():
    model = JoaoNovaCampaignModel()
    state = model.initial_joao_nova_state(provision_days=500.0)

    while state.active_expedition_id == model.EXPEDITION_ID:
        plan = model.plan_current_leg(state, seed=1501)
        if model.WARNING_REQUIRED_BLOCKER in plan.blockers:
            assert state.vessel.location_node == "SBR"
            state = model.acquire_malabar_warning(state)
            plan = model.plan_current_leg(state, seed=1501)
        assert plan.feasible, (state.vessel.location_node, state.vessel.clock.current_date, plan.blockers)
        state = model.execute_voyage(state, plan)

    assert state.vessel.location_node == "CAN"
    assert model.joao_nova_has_malabar_warning(state)
    assert state.chronology_mode is ChronologyMode.GUIDED
    assert state.vessel.clock.current_date <= date(1501, 12, 30), state.vessel.clock.current_date

    commercial_arrival = state.vessel.clock.current_date
    wait = model.wait_until_cannanore_blockade(state)
    assert wait.executed
    assert wait.days_waited == (date(1501, 12, 30) - commercial_arrival).days
    state = wait.state_after
    assert state.vessel.location_node == "CAN"
    assert state.vessel.clock.current_date == date(1501, 12, 30)
    assert state.chronology_mode is ChronologyMode.GUIDED

    event = model.cannanore_blockade_event()
    assert event.event_type == "NAVAL_BLOCKADE_BEGINS"
    assert event.date_from == date(1501, 12, 30)
    assert event.date_to == date(1501, 12, 30)
