from datetime import date

from quintoimperio.domain import GameSessionModel, NodeStateEventModel
from quintoimperio.domain.persistence import CampaignPersistence


def test_cochin_1504_inherits_end_1503_state_without_sovereignty_change():
    node_states = NodeStateEventModel()

    state = node_states.effective_state("COC", date(1504, 1, 1))

    assert state.institutional_presence == "FACTORY_RESTORED"
    assert state.fortification_state == "PORTUGUESE_FORT"
    assert state.garrison_state == "PORTUGUESE_GARRISON"
    assert state.access_state == "NEGOTIATED"
    assert state.relationship_state == "FAVORABLE"
    assert "COC1503_E02" in state.applied_event_ids
    assert "COC1503_E03" in state.applied_event_ids
    assert "COC1503_E04" in state.applied_event_ids
    assert "soberania local" in state.sovereignty_note.lower()


def test_cochin_1504_inherited_state_is_stable_across_save_load():
    session = GameSessionModel()
    node_states = NodeStateEventModel()
    persistence = CampaignPersistence()

    state = session.initial_state(
        location_node="COC",
        start_date=date(1504, 6, 30),
        provision_days=60.0,
    )

    before = node_states.effective_state(
        state.vessel.location_node,
        state.vessel.clock.current_date,
    )
    restored = persistence.loads(persistence.dumps(state, seed=1504))
    after = node_states.effective_state(
        restored.state.vessel.location_node,
        restored.state.vessel.clock.current_date,
    )

    assert restored.seed == 1504
    assert restored.state.vessel.location_node == "COC"
    assert restored.state.vessel.clock.current_date == date(1504, 6, 30)
    assert before == after
    assert after.institutional_presence == "FACTORY_RESTORED"
    assert after.fortification_state == "PORTUGUESE_FORT"
    assert after.garrison_state == "PORTUGUESE_GARRISON"
    assert "soberania local" in after.sovereignty_note.lower()
