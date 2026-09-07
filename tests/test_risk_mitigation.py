import unittest
from dataclasses import replace
from datetime import date

from quintoimperio.domain.risk_mitigation import (
    MAX_SECURED_RESERVE_DAYS,
    SECURED_RESERVE_COST_PER_DAY,
    mitigate_events,
    secure_provision_reserve_for_voyage,
)
from quintoimperio.domain import HistoricalCampaignModel
from quintoimperio.domain.voyage_event import VoyageEvent, VoyageEventType


class SecuredReserveTests(unittest.TestCase):
    def test_mitigates_only_major_provision_loss(self):
        major = VoyageEvent(
            event_id="X", event_type=VoyageEventType.MAJOR_PROVISION_LOSS,
            route_id="R", departure_date=date(1497, 1, 1), extra_days=0,
            condition_loss=0.0, provision_delta=-24.0, observed_timing_safe=True,
        )
        minor = replace(major, event_id="Y", event_type=VoyageEventType.PROVISION_SPOILAGE, provision_delta=-6.0)
        events, mitigated, raw, effective = mitigate_events((major, minor), 20.0)
        self.assertAlmostEqual(mitigated, 20.0)
        self.assertAlmostEqual(raw, -30.0)
        self.assertAlmostEqual(effective, -10.0)
        self.assertAlmostEqual(events[0].provision_delta, -4.0)
        self.assertAlmostEqual(events[1].provision_delta, -6.0)

    def test_zero_reserve_preserves_event(self):
        event = VoyageEvent(
            event_id="X", event_type=VoyageEventType.MAJOR_PROVISION_LOSS,
            route_id="R", departure_date=date(1497, 1, 1), extra_days=0,
            condition_loss=0.0, provision_delta=-18.0, observed_timing_safe=True,
        )
        events, mitigated, raw, effective = mitigate_events((event,), 0.0)
        self.assertEqual(events, (event,))
        self.assertEqual(mitigated, 0.0)
        self.assertEqual(raw, effective)

    def test_preparation_costs_capital_without_adding_provisions(self):
        model = HistoricalCampaignModel()
        state = model.initial_playable_state()
        wait = model.wait_for_guided_departure(state)
        state = wait.state_after
        plan = model.plan_current_leg(state, seed=1)
        before_provisions = state.vessel.provision_days
        before_capital = state.commerce.capital_index
        prepared, resolved, result = secure_provision_reserve_for_voyage(
            model.session, state, plan, 10.0
        )
        self.assertAlmostEqual(prepared.vessel.provision_days, before_provisions)
        self.assertAlmostEqual(
            prepared.commerce.capital_index,
            before_capital - 10.0 * SECURED_RESERVE_COST_PER_DAY,
        )
        self.assertTrue(resolved.events_resolved)
        self.assertEqual(result.secured_days, 10.0)

    def test_reserve_bounds(self):
        model = HistoricalCampaignModel()
        state = model.initial_playable_state()
        wait = model.wait_for_guided_departure(state)
        state = wait.state_after
        plan = model.plan_current_leg(state, seed=1)
        with self.assertRaises(ValueError):
            secure_provision_reserve_for_voyage(
                model.session, state, plan, MAX_SECURED_RESERVE_DAYS + 1
            )


if __name__ == "__main__":
    unittest.main()
