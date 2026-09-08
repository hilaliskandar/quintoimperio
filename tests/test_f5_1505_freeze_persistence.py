from datetime import date

from quintoimperio.domain import NodeStateEventModel
from quintoimperio.domain.persistence import CampaignPersistence
from quintoimperio.domain.session import GameSessionModel
from quintoimperio.domain.stop import ChronologyMode


def _world_projection(model: NodeStateEventModel, on_date: date):
    return {
        node: model.effective_state(node, on_date)
        for node in ("KIL", "SOF", "ANJ", "CAN", "COC", "MOM")
    }


def test_freeze_context_survives_save_load_without_inventing_playable_almeida_campaign():
    freeze_date = date(1505, 12, 31)
    session = GameSessionModel()
    persistence = CampaignPersistence()

    # Almeida não possui pernas executáveis; o save representa o contexto temporal
    # do jogador sem fabricar uma campanha ativa apenas para persistir o mundo.
    state = session.initial_state(
        location_node="COC",
        start_date=freeze_date,
        provision_days=60.0,
        condition=100.0,
        active_expedition_id=None,
        chronology_mode=ChronologyMode.COUNTERFACTUAL,
    )

    restored = persistence.loads(persistence.dumps(state, seed=1505))

    assert restored.seed == 1505
    assert restored.state.vessel.location_node == "COC"
    assert restored.state.vessel.clock.current_date == freeze_date
    assert restored.state.active_expedition_id is None
    assert restored.state.expedition_leg_sequence is None
    assert restored.state.chronology_mode is ChronologyMode.COUNTERFACTUAL

    # O estado histórico objetivo é derivado de data + dados documentais, não
    # duplicado dentro do save. A projeção antes/depois do round-trip é idêntica.
    nodes = NodeStateEventModel()
    before = _world_projection(nodes, state.vessel.clock.current_date)
    after = _world_projection(NodeStateEventModel(), restored.state.vessel.clock.current_date)
    assert before == after

    assert before["CAN"].fortification_state == "PORTUGUESE_FORT"
    assert before["COC"].garrison_state == "PORTUGUESE_GARRISON"
    assert before["MOM"].fortification_state != "PORTUGUESE_FORT"
