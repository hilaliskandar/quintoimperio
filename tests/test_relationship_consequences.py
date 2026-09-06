import unittest
from datetime import date

from quintoimperio.domain import (
    AccessStatus,
    ChronologyMode,
    HistoricalCampaignModel,
    NavigationBasis,
    RelationshipSessionModel,
    RelationshipStatus,
)


class RelationshipConsequenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = RelationshipSessionModel()
        cls.campaign = HistoricalCampaignModel()

    def test_contact_authority_changes_only_relationship_and_clock(self):
        state = self.session.initial_state(
            location_node="MAL",
            start_date=date(1498, 4, 14),
            provision_days=80.0,
            condition=87.0,
            capital_index=73.0,
            capacity_total=30.0,
        )
        access_before = self.session.access_status(state, "MAL")
        commerce_before = state.commerce
        node_knowledge_before = state.node_knowledge
        route_knowledge_before = state.route_knowledge
        provisions_before = state.vessel.provision_days
        condition_before = state.vessel.condition
        history_before = state.information_history
        events_before = state.voyage_event_history

        result = self.session.contact_authority(state)
        self.assertTrue(result.executed)
        self.assertEqual(result.days_spent, 1)
        self.assertIsNotNone(result.actor)
        self.assertEqual(result.actor.actor_id, "ACT_MAL_RULER_1498")

        after = result.state_after
        self.assertEqual(
            self.session.relationship_status(after, "ACT_MAL_RULER_1498"),
            RelationshipStatus.CONTACTED,
        )
        self.assertEqual(after.vessel.clock.current_date, date(1498, 4, 15))
        self.assertEqual(after.vessel.provision_days, provisions_before)
        self.assertEqual(after.vessel.condition, condition_before)
        self.assertEqual(after.commerce, commerce_before)
        self.assertEqual(after.node_knowledge, node_knowledge_before)
        self.assertEqual(after.route_knowledge, route_knowledge_before)
        self.assertEqual(after.information_history, history_before)
        self.assertEqual(after.voyage_event_history, events_before)
        self.assertEqual(self.session.access_status(after, "MAL"), access_before)
        self.assertEqual(access_before, AccessStatus.NEGOTIATION_REQUIRED)

    def test_contact_is_unavailable_without_documented_authority(self):
        state = self.session.initial_state(
            location_node="ADE",
            start_date=date(1498, 5, 22),
        )
        result = self.session.contact_authority(state)
        self.assertFalse(result.executed)
        self.assertIn("NO_DOCUMENTED_AUTHORITY_ACTOR", result.reasons)
        self.assertIsNone(result.actor)
        self.assertEqual(result.state_after, state)

    def test_repeated_contact_is_idempotent(self):
        state = self.session.initial_state(
            location_node="MAL",
            start_date=date(1498, 4, 14),
        )
        first = self.session.contact_authority(state)
        self.assertTrue(first.executed)
        second = self.session.contact_authority(first.state_after)
        self.assertFalse(second.executed)
        self.assertIn("AUTHORITY_ALREADY_CONTACTED", second.reasons)
        self.assertEqual(second.state_after, first.state_after)

    def test_malindi_pilot_is_historically_available_but_not_personally_assigned_before_contact(self):
        state = self.campaign.initial_state(
            location_node="MAL",
            start_date=date(1498, 4, 14),
            provision_days=120.0,
            active_expedition_id="EXP_GAMA_1497",
            expedition_leg_sequence=10,
            chronology_mode=ChronologyMode.GUIDED,
        )
        self.assertTrue(
            self.campaign.travel.pilot_can_guide(
                "PIL_MAL_GUJ_1498",
                "R_MAL_CAL",
                state.vessel.clock.current_date,
                "MAL",
            )
        )
        self.assertIsNone(
            self.campaign.recommended_pilot_id(state, "R_MAL_CAL")
        )

        contacted = self.campaign.contact_authority(state)
        self.assertTrue(contacted.executed)
        state = contacted.state_after
        self.assertEqual(
            self.campaign.recommended_pilot_id(state, "R_MAL_CAL"),
            "PIL_MAL_GUJ_1498",
        )

        waited = self.campaign.wait_for_guided_departure(state)
        self.assertTrue(waited.executed)
        self.assertEqual(waited.state_after.vessel.clock.current_date, date(1498, 4, 24))
        plan = self.campaign.plan_current_leg(waited.state_after, seed=1498)
        self.assertTrue(plan.feasible)
        self.assertEqual(plan.pilot_id, "PIL_MAL_GUJ_1498")
        self.assertEqual(plan.navigation_basis, NavigationBasis.PILOT)

    def test_contacted_remains_the_only_added_relational_state_needed_for_mvp_gate(self):
        self.assertEqual(
            set(RelationshipStatus),
            {RelationshipStatus.UNESTABLISHED, RelationshipStatus.CONTACTED},
        )


if __name__ == "__main__":
    unittest.main()
