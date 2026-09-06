import unittest
from datetime import date

from quintoimperio.domain import RelationshipSessionModel


class RelationshipRuleValidationTests(unittest.TestCase):
    def _malindi_state(self, model):
        return model.initial_state(
            location_node="MAL",
            start_date=date(1498, 4, 24),
            provision_days=120.0,
        )

    def test_empty_required_actor_rule_is_rejected_with_context(self):
        model = RelationshipSessionModel()
        model.relationship_rules = dict(model.relationship_rules)
        model.relationship_rules[("PILOT_REQUIRES_ACTOR_CONTACT", "PIL_MAL_GUJ_1498")] = ""
        with self.assertRaisesRegex(
            ValueError,
            "PILOT_REQUIRES_ACTOR_CONTACT/PIL_MAL_GUJ_1498.*relationship_rules.csv",
        ):
            model.pilot_available_to_player(
                self._malindi_state(model),
                "PIL_MAL_GUJ_1498",
                "R_MAL_CAL",
            )

    def test_unknown_required_actor_rule_is_rejected_with_context(self):
        model = RelationshipSessionModel()
        model.relationship_rules = dict(model.relationship_rules)
        model.relationship_rules[("PILOT_REQUIRES_ACTOR_CONTACT", "PIL_MAL_GUJ_1498")] = "ACT_DOES_NOT_EXIST"
        with self.assertRaisesRegex(
            KeyError,
            "PILOT_REQUIRES_ACTOR_CONTACT/PIL_MAL_GUJ_1498.*ator inexistente",
        ):
            model.pilot_available_to_player(
                self._malindi_state(model),
                "PIL_MAL_GUJ_1498",
                "R_MAL_CAL",
            )


if __name__ == "__main__":
    unittest.main()
