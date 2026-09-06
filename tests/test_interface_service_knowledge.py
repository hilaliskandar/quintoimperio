import os
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

from quintoimperio.domain import PortServiceKind
from prototype.game_service_knowledge import ServiceKnowledgePrototype


class ServiceKnowledgeInterfaceTests(unittest.TestCase):
    def test_lisbon_exposes_documented_service(self):
        app = ServiceKnowledgePrototype()
        self.assertEqual(
            app.service_label(PortServiceKind.PROVISIONS),
            "documentado: HIGH",
        )

    def test_historical_unknown_is_named_as_evidence_indeterminate(self):
        app = ServiceKnowledgePrototype()
        app.state = app.session.initial_state(location_node="SHB")
        self.assertEqual(
            app.service_label(PortServiceKind.PROVISIONS),
            "evidência histórica indeterminada",
        )


if __name__ == "__main__":
    unittest.main()
