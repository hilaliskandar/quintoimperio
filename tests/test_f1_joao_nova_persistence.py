from datetime import date

from quintoimperio.domain.joao_nova_campaign import JoaoNovaCampaignModel
from quintoimperio.domain.persistence import CampaignPersistence
from quintoimperio.domain.stop import ChronologyMode


def test_joao_nova_warning_and_expedition_progress_survive_roundtrip():
    model = JoaoNovaCampaignModel()
    persistence = CampaignPersistence()
    state = model.initial_joao_nova_state(provision_days=180.0)

    first = model.plan_current_leg(state, seed=1501)
    at_sao_bras = model.execute_voyage(state, first)
    informed = model.acquire_malabar_warning(at_sao_bras)

    text = persistence.dumps(informed, seed=1501)
    restored = persistence.loads(text)

    assert restored.seed == 1501
    assert restored.state.vessel.location_node == "SBR"
    assert restored.state.vessel.clock.current_date == informed.vessel.clock.current_date
    assert restored.state.active_expedition_id == model.EXPEDITION_ID
    assert restored.state.expedition_leg_sequence == 2
    assert restored.state.chronology_mode is ChronologyMode.GUIDED
    assert model.MALABAR_WARNING_KEY in restored.state.information_history

    released = model.plan_current_leg(restored.state, seed=1501)
    assert model.WARNING_REQUIRED_BLOCKER not in released.blockers


def test_cannanore_blockade_marker_roundtrip_preserves_date_and_guided_mode():
    model = JoaoNovaCampaignModel()
    persistence = CampaignPersistence()
    state = model.initial_joao_nova_state(provision_days=500.0)

    while state.active_expedition_id == model.EXPEDITION_ID:
        plan = model.plan_current_leg(state, seed=1501)
        if model.WARNING_REQUIRED_BLOCKER in plan.blockers:
            state = model.acquire_malabar_warning(state)
            plan = model.plan_current_leg(state, seed=1501)
        assert plan.feasible, plan.blockers
        state = model.execute_voyage(state, plan)

    wait = model.wait_until_cannanore_blockade(state)
    assert wait.executed
    state = wait.state_after
    assert state.vessel.clock.current_date == date(1501, 12, 30)

    restored = persistence.loads(persistence.dumps(state, seed=1501))
    assert restored.state.vessel.location_node == "CAN"
    assert restored.state.vessel.clock.current_date == date(1501, 12, 30)
    assert restored.state.chronology_mode is ChronologyMode.GUIDED
    assert model.MALABAR_WARNING_KEY in restored.state.information_history
