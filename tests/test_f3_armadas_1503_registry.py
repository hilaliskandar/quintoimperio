import pytest

from quintoimperio.domain import ExpeditionModel


EXPEDITIONS_1503 = (
    "EXP_AFONSO_ALBUQUERQUE_1503",
    "EXP_FRANCISCO_ALBUQUERQUE_1503",
    "EXP_SALDANHA_1503",
)


def test_1503_armadas_are_distinct_documentary_expeditions():
    model = ExpeditionModel()

    leaders = {
        expedition_id: model.expeditions[expedition_id]["leader"]
        for expedition_id in EXPEDITIONS_1503
    }

    assert leaders == {
        "EXP_AFONSO_ALBUQUERQUE_1503": "Afonso de Albuquerque",
        "EXP_FRANCISCO_ALBUQUERQUE_1503": "Francisco de Albuquerque",
        "EXP_SALDANHA_1503": "António de Saldanha",
    }
    assert all(
        model.expeditions[expedition_id]["source_id"] == "EVE_ARMADAS_MANUEL"
        for expedition_id in EXPEDITIONS_1503
    )


def test_1503_registry_entries_have_no_playable_legs_yet():
    model = ExpeditionModel()

    for expedition_id in EXPEDITIONS_1503:
        assert model.legs.get(expedition_id, ()) == ()
        with pytest.raises(KeyError, match="Expedicao sem pernas"):
            model.first_sequence(expedition_id)
