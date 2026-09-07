"""Continuidade pós-MVP da primeira viagem até os Baixos do Rio Grande.

Esta fachada preserva ``HistoricalCampaignModel`` como baseline Lisboa-Calecute e
ativa explicitamente a subcampanha documental do retorno. Atividades de provisões
registradas em ``expedition_stops.csv`` autorizam apenas uma ação específica da
expedição; elas não convertem ``nodes.csv`` em disponibilidade portuária genérica.
Quantidades e duração da ação são parâmetros de ``simulation/return_rules.csv``.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import date
from pathlib import Path

from quintoimperio.data.loader import RepositoryData

from .campaign import HistoricalCampaignModel
from .port import PortServiceKind, PortServiceResult, ServiceAvailability
from .session import GameSessionState, SessionPortServiceResult
from .stop import ChronologyMode, ExpeditionStop


class ReturnCampaignModel(HistoricalCampaignModel):
    """Fachada opt-in para o retorno documentado de 1498-1499."""

    RETURN_EXPEDITION_ID = "EXP_GAMA_RETURN_1498"
    RETURN_START_NODE = "CAL"
    RETURN_END_NODE = "BRG"
    RETURN_DEPARTURE = date(1498, 8, 30)
    PROVISION_ACTIVITIES = frozenset(
        {"WATER", "FOOD", "FOOD_EXCHANGE", "FISHING", "FOOD_PRESERVATION"}
    )

    def __init__(self, root: Path | None = None) -> None:
        super().__init__(root)
        repository = RepositoryData(root)
        self.return_rules = {
            (row["rule_type"], row["key"]): float(row["value"])
            for row in repository.simulation("return_rules.csv")
        }

    def activate_return(self, state: GameSessionState) -> GameSessionState:
        """Ativa a subcampanha de retorno sem alterar o encerramento do MVP.

        A ativação é explícita. Se o jogador já passou de 30/08/1498, a campanha
        não força uma data histórica retroativa e passa a ``COUNTERFACTUAL``.
        """
        if state.vessel.location_node != self.RETURN_START_NODE:
            raise ValueError("O retorno só pode ser ativado em Calecute")
        if state.active_expedition_id is not None:
            raise ValueError("Já existe uma expedição ativa")

        first_sequence = self.session.expedition.first_sequence(self.RETURN_EXPEDITION_ID)
        chronology = state.chronology_mode
        if state.vessel.clock.current_date > self.RETURN_DEPARTURE:
            chronology = ChronologyMode.COUNTERFACTUAL
        return replace(
            state,
            active_expedition_id=self.RETURN_EXPEDITION_ID,
            expedition_leg_sequence=first_sequence,
            active_stop_id=None,
            chronology_mode=chronology,
        )

    def _stop_has_documented_provisions(self, stop: ExpeditionStop | None) -> bool:
        return bool(stop and self.PROVISION_ACTIVITIES.intersection(stop.activities))

    def _logistics_horizon(
        self,
        state: GameSessionState,
        *,
        current_required: float,
        seed: int = 0,
    ) -> tuple[float, str]:
        """Encerra o horizonte também em permanência documental com provisões.

        Isso não modifica a disponibilidade genérica do nó. O horizonte apenas
        reconhece que, para esta expedição específica, existe uma futura decisão
        de provisões sustentada por `expedition_stops.csv`.
        """
        if state.active_expedition_id != self.RETURN_EXPEDITION_ID:
            return super()._logistics_horizon(
                state,
                current_required=current_required,
                seed=seed,
            )

        leg = self.current_leg(state)
        if leg is None:
            raise ValueError("Nenhuma perna ativa para horizonte logístico")

        expedition_id = state.active_expedition_id
        route = self.session.routes[leg.route_id]
        total = current_required
        end_node = route["destination_node"]
        stop = self.session.stops.for_leg(expedition_id, leg.sequence)
        if self._stop_has_documented_provisions(stop):
            return total, end_node
        availability = self.session.port.availability(end_node, PortServiceKind.PROVISIONS)
        if availability not in {ServiceAvailability.UNKNOWN, ServiceAvailability.NONE}:
            return total, end_node

        for future_leg in self.session.expedition.legs.get(expedition_id, ()):
            if future_leg.sequence <= leg.sequence:
                continue
            required = self._historical_leg_provision_requirement(future_leg, seed=seed)
            if required is None:
                break
            total += required
            future_route = self.session.routes[future_leg.route_id]
            end_node = future_route["destination_node"]
            stop = self.session.stops.for_leg(expedition_id, future_leg.sequence)
            if self._stop_has_documented_provisions(stop):
                break
            availability = self.session.port.availability(
                end_node, PortServiceKind.PROVISIONS
            )
            if availability not in {ServiceAvailability.UNKNOWN, ServiceAvailability.NONE}:
                break
        return total, end_node

    def documented_stop_can_reprovision(self, state: GameSessionState) -> bool:
        stop = self.session.active_stop(state)
        return bool(
            stop is not None
            and stop.expedition_id == self.RETURN_EXPEDITION_ID
            and stop.node_id == state.vessel.location_node
            and self._stop_has_documented_provisions(stop)
        )

    def reprovision_at_documented_stop(
        self, state: GameSessionState, requested_days: float
    ) -> SessionPortServiceResult:
        """Converte ato documental de provisões em efeito abstrato de jogo.

        A autorização histórica vem somente da permanência ativa. A quantidade
        adicionada e o tempo consumido são ``SIMULATION``. O serviço genérico do
        nó permanece inalterado e pode continuar ``UNKNOWN``.
        """
        if requested_days <= 0:
            raise ValueError("requested_days deve ser positivo")

        stop = self.session.active_stop(state)
        if stop is None:
            blockers = ("NO_ACTIVE_EXPEDITION_STOP",)
        elif stop.expedition_id != self.RETURN_EXPEDITION_ID:
            blockers = ("STOP_NOT_PART_OF_RETURN_EXPEDITION",)
        elif stop.node_id != state.vessel.location_node:
            blockers = ("VESSEL_NOT_AT_DOCUMENTED_STOP",)
        elif not self._stop_has_documented_provisions(stop):
            blockers = ("STOP_HAS_NO_DOCUMENTED_PROVISION_ACTIVITY",)
        else:
            blockers = ()

        if blockers:
            port_result = PortServiceResult(
                node_id=state.vessel.location_node,
                service=PortServiceKind.PROVISIONS,
                success=False,
                state_before=state.vessel,
                state_after=state.vessel,
                effect=0.0,
                days_spent=0,
                blockers=blockers,
            )
            return SessionPortServiceResult(
                executed=False,
                reasons=blockers,
                state_before=state,
                state_after=state,
                service_result=port_result,
            )

        capacity = self.return_rules[
            ("DOCUMENTED_STOP_PROVISION_CAPACITY_PER_ACTION", "DEFAULT")
        ]
        service_days = int(
            self.return_rules[("DOCUMENTED_STOP_PROVISION_SERVICE_DAYS", "DEFAULT")]
        )
        max_onboard = self.session.port.rules[("PROVISION_MAX_ONBOARD", "DEFAULT")]
        remaining_capacity = max(0.0, max_onboard - state.vessel.provision_days)
        added = min(requested_days, capacity, remaining_capacity)
        if added <= 0:
            blockers = ("ONBOARD_PROVISION_CAP_REACHED",)
            port_result = PortServiceResult(
                node_id=state.vessel.location_node,
                service=PortServiceKind.PROVISIONS,
                success=False,
                state_before=state.vessel,
                state_after=state.vessel,
                effect=0.0,
                days_spent=0,
                blockers=blockers,
            )
            return SessionPortServiceResult(
                executed=False,
                reasons=blockers,
                state_before=state,
                state_after=state,
                service_result=port_result,
            )

        vessel_after = replace(
            state.vessel,
            clock=state.vessel.clock.advance(service_days),
            provision_days=state.vessel.provision_days + added,
        )
        after = replace(state, vessel=vessel_after)
        port_result = PortServiceResult(
            node_id=state.vessel.location_node,
            service=PortServiceKind.PROVISIONS,
            success=True,
            state_before=state.vessel,
            state_after=vessel_after,
            effect=added,
            days_spent=service_days,
            blockers=(),
        )
        return SessionPortServiceResult(
            executed=True,
            reasons=(),
            state_before=state,
            state_after=after,
            service_result=port_result,
        )
