import unittest

from quintoimperio.domain import (
    CampaignPersistence,
    HistoricalCampaignModel,
    PortServiceKind,
    ServiceAvailability,
    ServiceKnowledgeStatus,
)


class ServiceKnowledgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = HistoricalCampaignModel()

    def test_current_port_observation_reveals_documented_evidence(self):
        state = self.model.initial_state(location_node="LIS")
        provisions = self.model.service_view(state, PortServiceKind.PROVISIONS)
        self.assertEqual(provisions.knowledge_status, ServiceKnowledgeStatus.DOCUMENTED)
        self.assertEqual(provisions.revealed_availability, ServiceAvailability.HIGH)
        self.assertTrue(provisions.historical_documented)
        self.assertTrue(provisions.actionable)

    def test_unvisited_port_remains_unassessed_for_player(self):
        state = self.model.initial_state(location_node="LIS")
        future = self.model.service_view(
            state,
            PortServiceKind.PROVISIONS,
            node_id="SBR",
        )
        self.assertEqual(future.knowledge_status, ServiceKnowledgeStatus.UNASSESSED)
        self.assertIsNone(future.revealed_availability)
        self.assertFalse(future.actionable)

    def test_historical_unknown_is_indeterminate_not_unavailable(self):
        state = self.model.initial_state(location_node="SHB", provision_days=20.0)
        view = self.model.service_view(state, PortServiceKind.PROVISIONS)
        self.assertEqual(
            self.model.port.availability("SHB", PortServiceKind.PROVISIONS),
            ServiceAvailability.UNKNOWN,
        )
        self.assertEqual(
            view.knowledge_status,
            ServiceKnowledgeStatus.EVIDENCE_INDETERMINATE,
        )
        self.assertIsNone(view.revealed_availability)
        self.assertFalse(view.historical_documented)
        self.assertFalse(view.actionable)

        result = self.model.reprovision(state, 30.0)
        self.assertFalse(result.executed)
        self.assertEqual(
            result.reasons,
            ("HISTORICAL_SERVICE_EVIDENCE_INDETERMINATE",),
        )
        self.assertEqual(state.vessel.provision_days, 20.0)

    def test_documented_none_remains_distinct_from_indeterminate(self):
        state = self.model.initial_state(location_node="CGH")
        view = self.model.service_view(state, PortServiceKind.PROVISIONS)
        self.assertEqual(view.knowledge_status, ServiceKnowledgeStatus.DOCUMENTED)
        self.assertEqual(view.revealed_availability, ServiceAvailability.NONE)
        result = self.model.reprovision(state, 10.0)
        self.assertEqual(result.reasons, ("SERVICE_UNAVAILABLE",))

    def test_arrival_observes_destination_without_rewriting_evidence(self):
        state = self.model.initial_state(active_expedition_id="EXP_GAMA_1497")
        plan = self.model.plan_current_leg(state, seed=1498)
        self.assertTrue(plan.feasible)
        destination = plan.destination_node
        before = self.model.service_view(
            state,
            PortServiceKind.PROVISIONS,
            node_id=destination,
        )
        self.assertEqual(before.knowledge_status, ServiceKnowledgeStatus.UNASSESSED)
        after = self.model.execute_voyage(state, plan)
        observed = self.model.service_view(after, PortServiceKind.PROVISIONS)
        self.assertNotEqual(observed.knowledge_status, ServiceKnowledgeStatus.UNASSESSED)
        self.assertEqual(
            self.model.port.availability(destination, PortServiceKind.PROVISIONS),
            self.model.port.quote(destination, PortServiceKind.PROVISIONS).availability,
        )

    def test_persistence_round_trip_preserves_service_knowledge(self):
        persistence = CampaignPersistence()
        state = self.model.initial_state(location_node="SHB")
        loaded = persistence.loads(persistence.dumps(state, seed=77))
        self.assertEqual(loaded.state, state)
        self.assertEqual(
            self.model.service_view(loaded.state, PortServiceKind.PROVISIONS).knowledge_status,
            ServiceKnowledgeStatus.EVIDENCE_INDETERMINATE,
        )

    def test_schema_v1_migrates_without_inventing_service_knowledge(self):
        persistence = CampaignPersistence()
        state = self.model.initial_state(location_node="LIS")
        payload = persistence.to_dict(state, seed=1)
        payload["schema_version"] = 1
        payload["state"].pop("service_knowledge_records")
        loaded = persistence.from_dict(payload)
        self.assertEqual(loaded.schema_version, 1)
        self.assertEqual(getattr(loaded.state, "service_knowledge_records"), ())
        view = self.model.service_view(loaded.state, PortServiceKind.PROVISIONS)
        self.assertEqual(view.knowledge_status, ServiceKnowledgeStatus.UNASSESSED)


if __name__ == "__main__":
    unittest.main()
