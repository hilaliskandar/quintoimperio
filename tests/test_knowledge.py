import unittest

from quintoimperio.domain import KnowledgeLevel, KnowledgeModel


class KnowledgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = KnowledgeModel()

    def test_lisbon_player_starts_with_high_knowledge(self):
        state = self.model.initial_for_node("LIS", "PLAYER")
        self.assertEqual(state.geo, KnowledgeLevel.CONFIRMED)
        self.assertGreaterEqual(state.nav, KnowledgeLevel.OPERATIONAL)

    def test_calicut_player_starts_with_indirect_not_operational_knowledge(self):
        state = self.model.initial_for_node("CAL", "PLAYER")
        self.assertEqual(state.geo, KnowledgeLevel.PARTIAL)
        self.assertEqual(state.nav, KnowledgeLevel.RUMORED)
        self.assertEqual(state.market, KnowledgeLevel.RUMORED)

    def test_malindi_player_can_start_unknown_while_crown_state_is_separate(self):
        player = self.model.initial_for_node("MAL", "PLAYER")
        crown = self.model.initial_for_node("MAL", "CROWN")
        self.assertEqual(player.geo, KnowledgeLevel.UNKNOWN)
        self.assertEqual(crown.geo, KnowledgeLevel.UNKNOWN)

    def test_calicut_crown_has_strategic_information_distinct_from_player(self):
        player = self.model.initial_for_node("CAL", "PLAYER")
        crown = self.model.initial_for_node("CAL", "CROWN")
        self.assertGreaterEqual(crown.market, player.market)
        self.assertEqual(crown.market, KnowledgeLevel.PARTIAL)
        self.assertEqual(crown.nav, KnowledgeLevel.RUMORED)

    def test_dimensions_improve_independently(self):
        initial = self.model.initial_for_node("CAL", "PLAYER")
        improved = initial.improve("nav", 2)
        self.assertEqual(improved.nav, KnowledgeLevel.OPERATIONAL)
        self.assertEqual(improved.market, initial.market)
        self.assertEqual(improved.geo, initial.geo)

    def test_knowledge_is_capped(self):
        state = self.model.initial_for_node("LIS", "PLAYER")
        improved = state.improve("geo", 20)
        self.assertEqual(improved.geo, KnowledgeLevel.CONFIRMED)


if __name__ == "__main__":
    unittest.main()
