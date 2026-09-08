from quintoimperio.domain.gama_1502_campaign import Gama1502CampaignModel
from quintoimperio.domain.persistence import CampaignPersistence
from quintoimperio.domain.stop import ChronologyMode


def test_gama_1502_progress_survives_roundtrip_without_parallel_fleet_state():
    model = Gama1502CampaignModel()
    persistence = CampaignPersistence()
    state = model.initial_gama_1502_state(provision_days=500.0)

    first = model.plan_current_leg(state, seed=1502)
    assert first.feasible, first.blockers
    at_sofala = model.execute_voyage(state, first)

    restored = persistence.loads(persistence.dumps(at_sofala, seed=1502))

    assert restored.seed == 1502
    assert restored.state.vessel.location_node == "SOF"
    assert restored.state.vessel.clock.current_date == at_sofala.vessel.clock.current_date
    assert restored.state.active_expedition_id == model.EXPEDITION_ID
    assert restored.state.expedition_leg_sequence == 2
    assert restored.state.chronology_mode is ChronologyMode.GUIDED

    next_plan = model.plan_current_leg(restored.state, seed=1502)
    assert next_plan.route_id == "R_SOF_KIL"
    assert next_plan.feasible, next_plan.blockers

    # A permanência histórica de Sodré continua fora do estado ativo do jogador.
    event = model.sodre_force_remains_event()
    assert event.trajectory_id == "SODRE_FORCE"
    assert restored.state.active_expedition_id != "EXP_SODRE_1503"
