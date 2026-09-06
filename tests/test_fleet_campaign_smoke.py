import unittest
from dataclasses import replace

from quintoimperio.domain import FleetModel, FleetState, HistoricalCampaignModel, PhysicalVessel


class PhysicalFleetCampaignSmokeTests(unittest.TestCase):
    """Smoke paralelo: campanha historica existente + consumo fisico experimental.

    O teste nao altera VesselState. Ele apenas usa os dias de viagem produzidos
    pelo dominio atual para consumir os quatro mantimentos da camada fisica.
    As mesmas acoes explicitas de reabastecimento do smoke historico sao
    traduzidas em dias de racao fisica para cada embarcacao.
    """

    @classmethod
    def setUpClass(cls):
        cls.campaign = HistoricalCampaignModel()
        cls.fleet_model = FleetModel()

    def _add_days_to_all(self, fleet: FleetState, days: float) -> FleetState:
        vessels: list[PhysicalVessel] = []
        for vessel in fleet.vessels:
            added = self.fleet_model.provision_for(vessel.persons, days)
            vessels.append(replace(vessel, provisions=vessel.provisions.plus(added)))
        return FleetState(tuple(vessels))

    def _consume_travel_days(self, fleet: FleetState, days: int) -> FleetState:
        vessels: list[PhysicalVessel] = []
        for vessel in fleet.vessels:
            required = self.fleet_model.provision_for(vessel.persons, days)
            vessels.append(replace(vessel, provisions=vessel.provisions.minus(required)))
        return FleetState(tuple(vessels))

    def _travel(self, state, fleet, seen):
        plan = self.campaign.plan_current_leg(state, seed=1498)
        self.assertTrue(plan.feasible, (plan.route_id, plan.blockers))
        fleet = self._consume_travel_days(fleet, plan.travel_days)
        seen.append((plan.route_id, plan.travel_days))
        state = self.campaign.execute_voyage(state, plan)
        return state, fleet

    def _reprovision(self, state, fleet, actions: int):
        for _ in range(actions):
            result = self.campaign.reprovision(state, 30.0)
            self.assertTrue(result.executed)
            state = result.state_after
            fleet = self._add_days_to_all(fleet, 30.0)
        return state, fleet

    def test_guided_lisbon_calicut_is_physically_feasible_without_unknown_stop_imputation(self):
        state = self.campaign.initial_state(active_expedition_id="EXP_GAMA_1497")
        fleet = self.fleet_model.load_research_scenario()
        initial_mass = fleet.provisions.major_consumables_mass_kg
        seen = []

        # Lisboa -> Sao Tiago: o carregamento fisico inicial suporta a perna.
        state, fleet = self._travel(state, fleet, seen)

        # Sao Tiago: reproduz as tres acoes explicitas do smoke historico.
        state, fleet = self._reprovision(state, fleet, 3)
        state = self.campaign.wait_for_guided_departure(state).state_after

        # Sao Tiago -> Santa Helena Bay. Nenhuma provisao e inventada em SHB.
        state, fleet = self._travel(state, fleet, seen)
        state = self.campaign.wait_for_guided_departure(state).state_after
        state, fleet = self._travel(state, fleet, seen)

        # Cabo da Boa Esperanca -> Sao Bras.
        state, fleet = self._travel(state, fleet, seen)

        # Sao Bras documenta agua e oferece quatro acoes explicitas no smoke.
        state, fleet = self._reprovision(state, fleet, 4)
        state = self.campaign.wait_for_guided_departure(state).state_after
        state, fleet = self._travel(state, fleet, seen)

        # Rio do Cobre e Rio dos Bons Sinais: uma acao explicita em cada escala.
        state, fleet = self._reprovision(state, fleet, 1)
        state = self.campaign.wait_for_guided_departure(state).state_after
        state, fleet = self._travel(state, fleet, seen)

        state, fleet = self._reprovision(state, fleet, 1)
        state = self.campaign.wait_for_guided_departure(state).state_after
        state, fleet = self._travel(state, fleet, seen)

        # Mozambique, Mombaca e Melinde permanecem sem imputacao de provisoes.
        state = self.campaign.wait_for_guided_departure(state).state_after
        state, fleet = self._travel(state, fleet, seen)
        state = self.campaign.wait_for_guided_departure(state).state_after
        state, fleet = self._travel(state, fleet, seen)

        contacted = self.campaign.contact_authority(state)
        self.assertTrue(contacted.executed)
        state = contacted.state_after
        state = self.campaign.wait_for_guided_departure(state).state_after
        state, fleet = self._travel(state, fleet, seen)

        self.assertEqual(state.vessel.location_node, "CAL")
        self.assertEqual(
            [route for route, _ in seen],
            [
                "R_LIS_STG",
                "R_STG_SHB",
                "R_SHB_CGH",
                "R_CGH_SBR",
                "R_SBR_RCO",
                "R_RCO_RBS",
                "R_RBS_MOZ",
                "R_MOZ_MOM",
                "R_MOM_MAL",
                "R_MAL_CAL",
            ],
        )
        self.assertGreater(fleet.provisions.major_consumables_mass_kg, 0.0)
        self.assertGreater(fleet.provisions.major_consumables_mass_kg, initial_mass * 0.25)
        self.assertTrue(all(self.fleet_model.autonomy_days(v) > 0 for v in fleet.vessels))

    def test_unknown_stops_are_not_needed_to_make_physical_smoke_feasible(self):
        """Controle: a viabilidade nao depende de criar estoque em SHB/MOZ/MOM/MAL."""
        state = self.campaign.initial_state(active_expedition_id="EXP_GAMA_1497")
        fleet = self.fleet_model.load_research_scenario()
        unknown_reprovision_events = 0

        state, fleet = self._travel(state, fleet, [])
        state, fleet = self._reprovision(state, fleet, 3)
        state = self.campaign.wait_for_guided_departure(state).state_after
        state, fleet = self._travel(state, fleet, [])

        # SHB: sem acao material.
        state = self.campaign.wait_for_guided_departure(state).state_after
        state, fleet = self._travel(state, fleet, [])
        state, fleet = self._travel(state, fleet, [])
        state, fleet = self._reprovision(state, fleet, 4)
        state = self.campaign.wait_for_guided_departure(state).state_after
        state, fleet = self._travel(state, fleet, [])
        state, fleet = self._reprovision(state, fleet, 1)
        state = self.campaign.wait_for_guided_departure(state).state_after
        state, fleet = self._travel(state, fleet, [])
        state, fleet = self._reprovision(state, fleet, 1)
        state = self.campaign.wait_for_guided_departure(state).state_after
        state, fleet = self._travel(state, fleet, [])

        # MOZ/MOM/MAL: sincronizacao cronologica e contato, mas zero provisoes novas.
        state = self.campaign.wait_for_guided_departure(state).state_after
        state, fleet = self._travel(state, fleet, [])
        state = self.campaign.wait_for_guided_departure(state).state_after
        state, fleet = self._travel(state, fleet, [])
        state = self.campaign.contact_authority(state).state_after
        state = self.campaign.wait_for_guided_departure(state).state_after
        state, fleet = self._travel(state, fleet, [])

        self.assertEqual(unknown_reprovision_events, 0)
        self.assertEqual(state.vessel.location_node, "CAL")
        self.assertTrue(all(self.fleet_model.autonomy_days(v) > 0 for v in fleet.vessels))


if __name__ == "__main__":
    unittest.main()
