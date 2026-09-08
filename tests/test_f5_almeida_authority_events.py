import unittest
from datetime import date

from quintoimperio.domain import ExpeditionEventModel


class F5AlmeidaAuthorityEventTests(unittest.TestCase):
    def setUp(self):
        self.model = ExpeditionEventModel()
        self.events = self.model.for_expedition("EXP_ALMEIDA_1505")

    def test_authority_sequence_preserves_legal_command_and_indian_activation(self):
        by_id = {event.event_id: event for event in self.events}

        self.assertEqual(
            [event.event_id for event in self.events],
            ["ALM1505_E01", "ALM1505_E02", "ALM1505_E03", "ALM1505_E04", "ALM1505_E05"],
        )
        self.assertEqual(by_id["ALM1505_E01"].date_from, date(1505, 2, 27))
        self.assertEqual(by_id["ALM1505_E01"].event_type, "ROYAL_APPOINTMENT")
        self.assertEqual(by_id["ALM1505_E02"].date_from, date(1505, 3, 3))
        self.assertEqual(by_id["ALM1505_E02"].event_type, "ROYAL_REGIMENT_ISSUED")
        self.assertEqual(by_id["ALM1505_E03"].date_from, date(1505, 3, 25))
        self.assertEqual(by_id["ALM1505_E03"].origin_node, "LIS")
        self.assertIsNone(by_id["ALM1505_E03"].destination_node)

        activation = by_id["ALM1505_E04"]
        self.assertEqual(activation.date_precision, "RANGE")
        self.assertEqual(activation.date_from, date(1505, 10, 1))
        self.assertEqual(activation.date_to, date(1505, 10, 31))
        self.assertEqual(activation.origin_node, "CAN")
        self.assertEqual(activation.destination_node, "CAN")

        cochin = by_id["ALM1505_E05"]
        self.assertEqual(cochin.date_precision, "EXACT")
        self.assertEqual(cochin.date_from, date(1505, 12, 16))
        self.assertEqual(cochin.destination_node, "COC")

    def test_conservative_availability_does_not_activate_viceroyal_event_early(self):
        september = {event.event_id for event in self.model.available_by("EXP_ALMEIDA_1505", date(1505, 9, 30))}
        october_30 = {event.event_id for event in self.model.available_by("EXP_ALMEIDA_1505", date(1505, 10, 30))}
        october_31 = {event.event_id for event in self.model.available_by("EXP_ALMEIDA_1505", date(1505, 10, 31))}
        december_15 = {event.event_id for event in self.model.available_by("EXP_ALMEIDA_1505", date(1505, 12, 15))}
        december_16 = {event.event_id for event in self.model.available_by("EXP_ALMEIDA_1505", date(1505, 12, 16))}

        self.assertNotIn("ALM1505_E04", september)
        self.assertNotIn("ALM1505_E04", october_30)
        self.assertIn("ALM1505_E04", october_31)
        self.assertNotIn("ALM1505_E05", december_15)
        self.assertIn("ALM1505_E05", december_16)

    def test_appointment_does_not_claim_viceroyal_authority_in_india(self):
        appointment = next(event for event in self.events if event.event_id == "ALM1505_E01")
        activation = next(event for event in self.events if event.event_id == "ALM1505_E04")

        self.assertNotEqual(appointment.event_type, activation.event_type)
        self.assertIsNone(appointment.origin_node)
        self.assertIsNone(appointment.destination_node)
        self.assertGreater(activation.date_from, appointment.date_from)


if __name__ == "__main__":
    unittest.main()
