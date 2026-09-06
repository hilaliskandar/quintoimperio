import tempfile
import unittest
from dataclasses import replace
from datetime import date
from pathlib import Path

from quintoimperio.domain import (
    CampaignPersistence,
    CargoHolding,
    ChronologyMode,
    HistoricalCampaignModel,
    RelationshipRecord,
    RelationshipStatus,
    SAVE_SCHEMA_VERSION,
    VoyageEvent,
    VoyageEventType,
)


class CampaignPersistenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = HistoricalCampaignModel()
        cls.persistence = CampaignPersistence()

    def _nontrivial_state(self):
        state = self.model.initial_state(active_expedition_id="EXP_GAMA_1497")
        plan = self.model.plan_current_leg(state, seed=1498)
        self.assertTrue(plan.feasible)
        state = self.model.execute_voyage(state, plan)

        commerce = replace(
            state.commerce,
            capital_index=81.25,
            cargo=(CargoHolding("PEPPER", 2.0),),
        )
        relationships = list(state.relationship_records)
        if relationships:
            first = relationships[0]
            relationships[0] = RelationshipRecord(
                actor_id=first.actor_id,
                status=RelationshipStatus.CONTACTED,
            )
        event = VoyageEvent(
            event_id="TEST_SAVE_EVENT",
            event_type=VoyageEventType.ROUGH_WEATHER,
            route_id="R_LIS_STG",
            departure_date=date(1497, 7, 8),
            extra_days=2,
            condition_loss=3.5,
            simulation_only=True,
        )
        return replace(
            state,
            commerce=commerce,
            relationship_records=tuple(relationships),
            information_history=("TEST_INFO",),
            voyage_event_history=(event,),
            chronology_mode=ChronologyMode.COUNTERFACTUAL,
        )

    def test_round_trip_preserves_complete_session_state(self):
        state = self._nontrivial_state()
        text = self.persistence.dumps(state, seed=1498)
        loaded = self.persistence.loads(text)
        self.assertEqual(loaded.schema_version, SAVE_SCHEMA_VERSION)
        self.assertEqual(loaded.seed, 1498)
        self.assertEqual(loaded.state, state)
        self.assertEqual(loaded.state.active_stop_id, state.active_stop_id)
        self.assertEqual(loaded.state.information_history, ("TEST_INFO",))
        self.assertEqual(len(loaded.state.voyage_event_history), 1)

    def test_file_round_trip(self):
        state = self._nontrivial_state()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "slot.json"
            self.persistence.save_file(path, state, seed=77)
            loaded = self.persistence.load_file(path)
        self.assertEqual(loaded.seed, 77)
        self.assertEqual(loaded.state, state)

    def test_unknown_schema_is_rejected(self):
        state = self.model.initial_state(active_expedition_id="EXP_GAMA_1497")
        payload = self.persistence.to_dict(state, seed=1498)
        payload["schema_version"] = SAVE_SCHEMA_VERSION + 1
        with self.assertRaisesRegex(ValueError, "Versão de save não suportada"):
            self.persistence.from_dict(payload)

    def test_same_seed_and_loaded_state_preserve_next_plan(self):
        state = self.model.initial_state(active_expedition_id="EXP_GAMA_1497")
        before = self.model.plan_current_leg(state, seed=1498)
        loaded = self.persistence.loads(
            self.persistence.dumps(state, seed=1498)
        )
        after = self.model.plan_current_leg(loaded.state, seed=loaded.seed)
        self.assertEqual(after, before)


if __name__ == "__main__":
    unittest.main()
