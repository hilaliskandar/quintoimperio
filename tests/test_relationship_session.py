import unittest
from datetime import date

from quintoimperio.domain import (
    GameSessionModel,
    InformationChannel,
    RelationshipStatus,
)


class RelationshipSessionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = GameSessionModel()

    def calicut_state(self):
        return self.model.initial_state(
            location_node="CAL",
            start_date=date(1498, 5, 22),
            provision_days=100.0,
        )

    def test_relationships_start_unestablished_and_hidden_from_contact_view(self):
        state = self.calicut_state()
        self.assertEqual(
            self.model.relationship_status(state, "ACT_CAL_SAMUDRI_AUTH"),
            RelationshipStatus.UNESTABLISHED,
        )
        self.assertEqual(
            self.model.relationship_status(state, "ACT_CAL_MUSLIM_MERCHANTS"),
            RelationshipStatus.UNESTABLISHED,
        )
        self.assertEqual(self.model.contacted_relationships(state), ())

    def test_access_negotiation_contacts_only_documented_authority(self):
        state = self.calicut_state()
        result = self.model.negotiate_access(state)
        self.assertTrue(result.executed)
        after = result.state_after
        self.assertEqual(
            self.model.relationship_status(after, "ACT_CAL_SAMUDRI_AUTH"),
            RelationshipStatus.CONTACTED,
        )
        self.assertEqual(
            self.model.relationship_status(after, "ACT_CAL_MUSLIM_MERCHANTS"),
            RelationshipStatus.UNESTABLISHED,
        )
        contacted = self.model.contacted_relationships(after)
        self.assertEqual([actor.actor_id for actor in contacted], ["ACT_CAL_SAMUDRI_AUTH"])

    def test_merchant_contact_contacts_documented_merchant_community(self):
        state = self.calicut_state()
        result = self.model.acquire_information(
            state, InformationChannel.MERCHANT_CONTACT, seed=1498
        )
        self.assertTrue(result.executed)
        after = result.state_after
        self.assertEqual(
            self.model.relationship_status(after, "ACT_CAL_MUSLIM_MERCHANTS"),
            RelationshipStatus.CONTACTED,
        )
        self.assertEqual(
            self.model.relationship_status(after, "ACT_CAL_SAMUDRI_AUTH"),
            RelationshipStatus.UNESTABLISHED,
        )

    def test_non_merchant_information_does_not_create_merchant_contact(self):
        state = self.calicut_state()
        result = self.model.acquire_information(
            state, InformationChannel.RUMOR, seed=1498
        )
        self.assertTrue(result.executed)
        self.assertEqual(
            self.model.relationship_status(
                result.state_after, "ACT_CAL_MUSLIM_MERCHANTS"
            ),
            RelationshipStatus.UNESTABLISHED,
        )

    def test_unmapped_port_does_not_invent_relationship(self):
        state = self.model.initial_state(
            location_node="ADE",
            start_date=date(1498, 6, 1),
            provision_days=100.0,
        )
        before = state.relationship_records
        result = self.model.negotiate_access(state)
        self.assertTrue(result.executed)
        self.assertEqual(result.state_after.relationship_records, before)


if __name__ == "__main__":
    unittest.main()
