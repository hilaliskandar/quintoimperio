import unittest

from quintoimperio.domain import PortServiceKind, PortServiceModel


class PortServiceDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = PortServiceModel()

    def test_all_node_service_fields_use_supported_categories(self):
        for node_id in self.model.nodes:
            for service in PortServiceKind:
                with self.subTest(node_id=node_id, service=service.value):
                    self.model.availability(node_id, service)

    def test_required_simulation_rules_are_present_and_positive(self):
        required = {
            ("PROVISION_CAPACITY_PER_VISIT", "LOW"),
            ("PROVISION_CAPACITY_PER_VISIT", "MEDIUM"),
            ("PROVISION_CAPACITY_PER_VISIT", "HIGH"),
            ("PROVISION_MAX_ONBOARD", "DEFAULT"),
            ("PROVISION_SERVICE_DAYS", "DEFAULT"),
            ("REPAIR_POINTS_PER_DAY", "LOW"),
            ("REPAIR_POINTS_PER_DAY", "MEDIUM"),
            ("REPAIR_POINTS_PER_DAY", "HIGH"),
            ("REPAIR_MAX_DAYS_PER_ACTION", "DEFAULT"),
        }
        self.assertTrue(required.issubset(self.model.rules))
        for key in required:
            self.assertGreater(self.model.rules[key], 0.0)


if __name__ == "__main__":
    unittest.main()
