import unittest
from datetime import date

from quintoimperio.domain.campaign_progress import CampaignProgressModel
from quintoimperio.domain import (
    ChronologyMode,
    HistoricalCampaignModel,
    KnowledgeLevel,
    KnowledgeState,
)


class CampaignProgressTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.campaign = HistoricalCampaignModel()
        cls.progress = CampaignProgressModel(cls.campaign.session)

    def _calicut_state(self, chronology=ChronologyMode.GUIDED):
        state = self.campaign.initial_state(
            location_node="CAL",
            start_date=date(1498, 5, 21),
            chronology_mode=chronology,
        )
        state = self.campaign.scenario_set_node_knowledge(
            state,
            "CAL",
            KnowledgeState(
                geo=KnowledgeLevel.OPERATIONAL,
                nav=KnowledgeLevel.PARTIAL,
                market=KnowledgeLevel.OPERATIONAL,
                political=KnowledgeLevel.PARTIAL,
            ),
        )
        return state

    def test_arrival_alone_does_not_finish_campaign(self):
        state = self._calicut_state()
        progress = self.progress.progress(state)
        self.assertFalse(progress.completed)
        self.assertEqual(progress.current_objective, "Estabelecer contato com ator documentado")
        completed = {item.milestone_id: item.completed for item in progress.milestones}
        self.assertTrue(completed["ARRIVE_CALICUT"])
        self.assertTrue(completed["CALICUT_KNOWLEDGE"])
        self.assertFalse(completed["CALICUT_ACCESS"])
        self.assertFalse(completed["FIRST_TRADE"])

    def test_access_without_trade_does_not_finish_campaign(self):
        state = self._calicut_state()
        access = self.campaign.negotiate_access(state)
        self.assertTrue(access.executed)
        progress = self.progress.progress(access.state_after)
        self.assertFalse(progress.completed)
        self.assertEqual(progress.current_objective, "Realizar a primeira compra comercial em Calecute")

    def test_first_calicut_purchase_finishes_campaign(self):
        state = self._calicut_state()
        state = self.campaign.negotiate_access(state).state_after
        trade = self.campaign.buy(state, "PEPPER", 2.0, seed=1498)
        self.assertTrue(trade.executed, trade.reasons)
        state = trade.state_after

        progress = self.progress.progress(state)
        self.assertTrue(progress.completed)
        self.assertEqual(progress.current_objective, "Campanha concluída em Calecute")

        summary = self.progress.summary(state)
        self.assertTrue(summary.completed)
        self.assertEqual(summary.location_node, "CAL")
        self.assertEqual(summary.chronology_mode, ChronologyMode.GUIDED)
        self.assertFalse(summary.counterfactual)
        self.assertGreater(summary.capacity_used, 0)
        self.assertIn(("PEPPER", 2.0), summary.cargo)
        self.assertTrue(summary.contacted_actor_ids)

    def test_counterfactual_completion_is_explicit_in_summary(self):
        state = self._calicut_state(ChronologyMode.COUNTERFACTUAL)
        state = self.campaign.negotiate_access(state).state_after
        state = self.campaign.buy(state, "PEPPER", 1.0, seed=1498).state_after
        summary = self.progress.summary(state)
        self.assertTrue(summary.completed)
        self.assertTrue(summary.counterfactual)
        self.assertEqual(summary.chronology_mode, ChronologyMode.COUNTERFACTUAL)


if __name__ == "__main__":
    unittest.main()
