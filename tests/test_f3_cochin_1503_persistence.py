from datetime import date

from quintoimperio.domain import GameSessionModel, NodeStateEventModel
from quintoimperio.domain.persistence import CampaignPersistence


def test_cochin_historical_state_is_stable_across_save_load_by_session_date():
    session = GameSessionModel()
    node_states = NodeStateEventModel()
    persistence = CampaignPersistence()

    state = session.initial_state(
        location_node="COC",
        start_date=date(1503, 9, 30),
        provision_days=60.0,
    )

    before = node_states.effective_state(
        state.vessel.location_node,
        state.vessel.clock.current_date,
    )
    restored = persistence.loads(persistence.dumps(state, seed=1503))
    after = node_states.effective_state(
        restored.state.vessel.location_node,
        restored.state.vessel.clock.current_date,
    )

    assert restored.seed == 1503
    assert restored.state.vessel.location_node == "COC"
    assert restored.state.vessel.clock.current_date == date(1503, 9, 30)
    assert before == after
    assert after.institutional_presence == "FACTORY_RESTORED"
    assert after.fortification_state == "PORTUGUESE_FORT"
    assert after.garrison_state == "NONE"
    assert "COC1503_E02" in after.applied_event_ids
    assert "COC1503_E03" in after.applied_event_ids


def test_cochin_end_1503_garrison_is_date_derived_not_parallel_save_state():
    session = GameSessionModel()
    node_states = NodeStateEventModel()
    persistence = CampaignPersistence()

    state = session.initial_state(
        location_node="COC",
        start_date=date(1503, 12, 31),
        provision_days=60.0,
    )
    restored = persistence.loads(persistence.dumps(state, seed=15031))
    world = node_states.effective_state(
        restored.state.vessel.location_node,
        restored.state.vessel.clock.current_date,
    )

    assert world.fortification_state == "PORTUGUESE_FORT"
    assert world.garrison_state == "PORTUGUESE_GARRISON"
    assert "COC1503_E04" in world.applied_event_ids
    assert "soberania local" in world.sovereignty_note.lower()
