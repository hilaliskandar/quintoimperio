import unittest

from prototype.game import PlayablePrototype
from quintoimperio.domain import InformationChannel


class InterfaceRelationshipTests(unittest.TestCase):
    def test_unestablished_actors_are_not_visible(self):
        app = PlayablePrototype("TECHNICAL")
        self.assertEqual(app.visible_relationships(), ())

    def test_merchant_contact_reveals_only_contacted_merchant_community(self):
        app = PlayablePrototype("TECHNICAL")
        app.acquire_information(InformationChannel.MERCHANT_CONTACT)
        visible = app.visible_relationships()
        self.assertEqual(
            [actor.actor_id for actor in visible],
            ["ACT_CAL_MUSLIM_MERCHANTS"],
        )
        self.assertNotIn(
            "ACT_CAL_SAMUDRI_AUTH",
            [actor.actor_id for actor in visible],
        )


if __name__ == "__main__":
    unittest.main()
