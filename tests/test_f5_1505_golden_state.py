import unittest
from datetime import date

from quintoimperio.domain import ExpeditionEventModel, NodeStateEventModel


class F5GoldenStateTests(unittest.TestCase):
    FREEZE_DATE = date(1505, 12, 31)

    def setUp(self):
        self.nodes = NodeStateEventModel()
        self.events = ExpeditionEventModel()

    def test_persistent_world_state_at_1505_freeze(self):
        kil = self.nodes.effective_state("KIL", self.FREEZE_DATE)
        sof = self.nodes.effective_state("SOF", self.FREEZE_DATE)
        anj = self.nodes.effective_state("ANJ", self.FREEZE_DATE)
        can = self.nodes.effective_state("CAN", self.FREEZE_DATE)
        coc = self.nodes.effective_state("COC", self.FREEZE_DATE)
        mom = self.nodes.effective_state("MOM", self.FREEZE_DATE)

        self.assertEqual((kil.fortification_state, kil.garrison_state), ("PORTUGUESE_FORT", "PORTUGUESE_GARRISON"))
        self.assertEqual((sof.fortification_state, sof.garrison_state), ("PORTUGUESE_FORT", "PORTUGUESE_GARRISON"))
        self.assertEqual((anj.fortification_state, anj.garrison_state), ("PORTUGUESE_FORT", "PORTUGUESE_GARRISON"))
        self.assertEqual((can.fortification_state, can.garrison_state), ("PORTUGUESE_FORT", "PORTUGUESE_GARRISON"))
        self.assertEqual((coc.fortification_state, coc.garrison_state), ("PORTUGUESE_FORT", "PORTUGUESE_GARRISON"))

        self.assertNotEqual(mom.fortification_state, "PORTUGUESE_FORT")
        self.assertNotEqual(mom.garrison_state, "PORTUGUESE_GARRISON")

        self.assertIn("KIL1505_E01", kil.applied_event_ids)
        self.assertIn("SOF1505_E02", sof.applied_event_ids)
        self.assertIn("ANJ1505_E01", anj.applied_event_ids)
        self.assertIn("CAN1505_E01", can.applied_event_ids)
        self.assertIn("COC1503_E04", coc.applied_event_ids)

    def test_local_sovereignty_is_not_replaced_by_portuguese_fortification(self):
        states = {
            node: self.nodes.effective_state(node, self.FREEZE_DATE)
            for node in ("KIL", "SOF", "ANJ", "CAN", "COC")
        }

        self.assertIn("não", states["KIL"].sovereignty_note.lower())
        self.assertIn("não", states["SOF"].sovereignty_note.lower())
        self.assertIn("não", states["ANJ"].sovereignty_note.lower())
        self.assertIn("Kolathunad", states["CAN"].sovereignty_note)
        self.assertIn("local", states["COC"].sovereignty_note.lower())

    def test_almeida_institutional_sequence_is_available_by_freeze(self):
        available = self.events.available_by("EXP_ALMEIDA_1505", self.FREEZE_DATE)
        self.assertEqual(
            [event.event_id for event in available],
            ["ALM1505_E01", "ALM1505_E02", "ALM1505_E03", "ALM1505_E04", "ALM1505_E05"],
        )
        self.assertEqual(available[-1].destination_node, "COC")
        self.assertEqual(available[-1].date_from, date(1505, 12, 16))

    def test_freeze_queries_are_deterministic(self):
        first = {
            node: self.nodes.effective_state(node, self.FREEZE_DATE)
            for node in ("KIL", "SOF", "ANJ", "CAN", "COC", "MOM")
        }
        second_model = NodeStateEventModel()
        second = {
            node: second_model.effective_state(node, self.FREEZE_DATE)
            for node in ("KIL", "SOF", "ANJ", "CAN", "COC", "MOM")
        }
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
