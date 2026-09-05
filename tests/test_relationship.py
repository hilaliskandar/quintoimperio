import unittest
from datetime import date

from quintoimperio.domain import RelationshipModel, RelationshipStatus


class RelationshipModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = RelationshipModel()

    def test_v01_statuses_are_categorical_not_numeric_reputation(self):
        self.assertEqual(RelationshipStatus.UNESTABLISHED.value, 0)
        self.assertEqual(RelationshipStatus.CONTACTED.value, 1)
        self.assertEqual(len(RelationshipStatus), 2)

    def test_calicut_has_documented_authority_and_merchant_community(self):
        on_date = date(1498, 5, 21)
        authority = self.model.actor_for_role("CAL", on_date, "AUTHORITY")
        merchants = self.model.actor_for_role("CAL", on_date, "MERCHANT_COMMUNITY")
        self.assertIsNotNone(authority)
        self.assertIsNotNone(merchants)
        assert authority is not None and merchants is not None
        self.assertEqual(authority.actor_id, "ACT_CAL_SAMUDRI_AUTH")
        self.assertEqual(merchants.actor_id, "ACT_CAL_MUSLIM_MERCHANTS")
        self.assertNotEqual(authority.actor_id, merchants.actor_id)

    def test_malindi_1498_has_documented_local_authority(self):
        authority = self.model.actor_for_role(
            "MAL", date(1498, 4, 16), "AUTHORITY"
        )
        self.assertIsNotNone(authority)
        assert authority is not None
        self.assertEqual(authority.actor_id, "ACT_MAL_RULER_1498")

    def test_malindi_actor_is_not_silently_extended_beyond_documented_period(self):
        self.assertIsNone(
            self.model.actor_for_role("MAL", date(1499, 4, 16), "AUTHORITY")
        )

    def test_no_generic_actor_is_invented_for_unmapped_port(self):
        self.assertEqual(self.model.actors_at("ADE", date(1498, 6, 1)), ())
        self.assertIsNone(
            self.model.actor_for_role("ADE", date(1498, 6, 1), "AUTHORITY")
        )


if __name__ == "__main__":
    unittest.main()
