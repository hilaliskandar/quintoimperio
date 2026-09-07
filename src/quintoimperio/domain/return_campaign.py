"""Continuidade pós-MVP da primeira viagem até os Baixos do Rio Grande.

Esta fachada preserva ``HistoricalCampaignModel`` como baseline Lisboa-Calecute e
ativa explicitamente a subcampanha documental do retorno. Atividades materiais
registradas em ``expedition_stops.csv`` autorizam apenas ações específicas da
expedição; elas não convertem ``nodes.csv`` em disponibilidade portuária genérica.
Quantidades e durações das ações são parâmetros de ``simulation/return_rules.csv``.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import date
from math import ceil
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
        {
            "WATER",
            "FOOD",
            "FOOD_EXCHANGE",
            "FISH_EXCHANGE",
            "FISHING",
            "FOOD_PRESERVATION",
        }
    )
    REPAIR_ACTIVITIES = frozenset({"CARENING", "MAST_REPAIR"})
    ONE_SHOT_PROVISION_NODES = frozenset({"SMI"})
    ONE_SHOT_REPAIR_NODES = frozenset({"ANJ"})

    def __init__(self, root: Path | None = None) -> None:
        super().__init__(root)
        repository = RepositoryData(root)
        self.return_rules = {
            (row["rule_type"], row["key"]): float(row["value"])
            for row in repository.simulation("return_rules.csv")
        }

    def _return_rule(self, rule_type: str, node_id: str) -> float:
        """Resolve regra específica do nó com fallback explícito para DEFAULT."""
        return self.return_rules.get(
            (rule_type, node_id),
            self.return_rules[(rule_type, "DEFAULT")],
        )

    @staticmethod
    def _action_key(stop: ExpeditionStop, action: str) -> str:
        return f"RETURN_ACTION:{stop.stop_id}:{action}"

    def _action_used(self, state: GameSessionState, stop: ExpeditionStop, action: str) -> bool:
        return self._action_key(stop, action) in state.information_history

    def _record_action(
        self, state: GameSessionState, stop: ExpeditionStop, action: str
    ) -> GameSessionState:
        key = self._action_key(stop, action)
        if key in state.information_history:
            return state
        return replace(state, information_history=state.information_history + (key,))

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

    def _stop_has_documented_repair(self, stop: ExpeditionStop | None) -> bool:
        return bool(stop and self.REPAIR_ACTIVITIES.intersection(stop.activities))

    def _logistics_horizon(
        self,
        state: GameSessionState,
        *,
        current_required: float,
        seed: int = 0,
    ) -> tuple[float, str]:
        """Encerra o horizonte também em permanência documental com provisões."""
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
        if not (
            stop is not None
            and stop.expedition_id == self.RETURN_EXPEDITION_ID
            and stop.node_id == state.vessel.location_node
            and self._stop_has_documented_provisions(stop)
        ):
            return False
        return not (
            stop.node_id in self.ONE_SHOT_PROVISION_NODES
            and self._action_used(state, stop, "PROVISIONS")
        )

    def documented_stop_can_repair(self, state: GameSessionState) -> bool:
        stop = self.session.active_stop(state)
        if not (
            stop is not None
            and stop.expedition_id == self.RETURN_EXPEDITION_ID
            and stop.node_id == state.vessel.location_node
            and self._stop_has_documented_repair(stop)
        ):
            return False
        return not (
            stop.node_id in self.ONE_SHOT_REPAIR_NODES
            and self._action_used(state, stop, "REPAIR")
        )

    def _specific_stop_blockers(
        self,
        state: GameSessionState,
        *,
        require_provisions: bool = False,
        require_repair: bool = False,
    ) -> tuple[str, ...]:
        stop = self.session.active_stop(state)
        if stop is None:
            return ("NO_ACTIVE_EXPEDITION_STOP",)
        if stop.expedition_id != self.RETURN_EXPEDITION_ID:
            return ("STOP_NOT_PART_OF_RETURN_EXPEDITION",)
        if stop.node_id != state.vessel.location_node:
            return ("VESSEL_NOT_AT_DOCUMENTED_STOP",)
        if require_provisions and not self._stop_has_documented_provisions(stop):
            return ("STOP_HAS_NO_DOCUMENTED_PROVISION_ACTIVITY",)
        if require_repair and not self._stop_has_documented_repair(stop):
            return ("STOP_HAS_NO_DOCUMENTED_REPAIR_ACTIVITY",)
        if (
            require_provisions
            and stop.node_id in self.ONE_SHOT_PROVISION_NODES
            and self._action_used(state, stop, "PROVISIONS")
        ):
            return ("DOCUMENTED_PROVISION_ACTION_ALREADY_USED",)
        if (
            require_repair
            and stop.node_id in self.ONE_SHOT_REPAIR_NODES
            and self._action_used(state, stop, "REPAIR")
        ):
            return ("DOCUMENTED_REPAIR_ACTION_ALREADY_USED",)
        return ()

    def reprovision_at_documented_stop(
        self, state: GameSessionState, requested_days: float
    ) -> SessionPortServiceResult:
        """Converte ato documental de provisões em efeito abstrato de jogo."""
        if requested_days <= 0:
            raise ValueError("requested_days deve ser positivo")

        blockers = self._specific_stop_blockers(state, require_provisions=True)
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
            return SessionPortServiceResult(False, blockers, state, state, port_result)

        stop = self.session.active_stop(state)
        if stop is None:
            raise RuntimeError("Ação documental sem permanência ativa")
        capacity = self._return_rule(
            "DOCUMENTED_STOP_PROVISION_CAPACITY_PER_ACTION",
            state.vessel.location_node,
        )
        service_days = int(
            self._return_rule(
                "DOCUMENTED_STOP_PROVISION_SERVICE_DAYS",
                state.vessel.location_node,
            )
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
            return SessionPortServiceResult(False, blockers, state, state, port_result)

        vessel_after = replace(
            state.vessel,
            clock=state.vessel.clock.advance(service_days),
            provision_days=state.vessel.provision_days + added,
        )
        after = replace(state, vessel=vessel_after)
        if stop.node_id in self.ONE_SHOT_PROVISION_NODES:
            after = self._record_action(after, stop, "PROVISIONS")
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
        return SessionPortServiceResult(True, (), state, after, port_result)

    def repair_at_documented_stop(
        self, state: GameSessionState, requested_points: float
    ) -> SessionPortServiceResult:
        """Projeta carena/reparo documentado em restauração abstrata de condição."""
        if requested_points <= 0:
            raise ValueError("requested_points deve ser positivo")

        blockers = self._specific_stop_blockers(state, require_repair=True)
        if blockers:
            port_result = PortServiceResult(
                node_id=state.vessel.location_node,
                service=PortServiceKind.REPAIR,
                success=False,
                state_before=state.vessel,
                state_after=state.vessel,
                effect=0.0,
                days_spent=0,
                blockers=blockers,
            )
            return SessionPortServiceResult(False, blockers, state, state, port_result)

        stop = self.session.active_stop(state)
        if stop is None:
            raise RuntimeError("Ação documental sem permanência ativa")
        missing = max(0.0, 100.0 - state.vessel.condition)
        if missing <= 0:
            blockers = ("VESSEL_ALREADY_FULL_CONDITION",)
            port_result = PortServiceResult(
                node_id=state.vessel.location_node,
                service=PortServiceKind.REPAIR,
                success=False,
                state_before=state.vessel,
                state_after=state.vessel,
                effect=0.0,
                days_spent=0,
                blockers=blockers,
            )
            return SessionPortServiceResult(False, blockers, state, state, port_result)

        rate = self._return_rule(
            "DOCUMENTED_STOP_REPAIR_POINTS_PER_DAY",
            state.vessel.location_node,
        )
        max_days = int(
            self._return_rule(
                "DOCUMENTED_STOP_REPAIR_MAX_DAYS_PER_ACTION",
                state.vessel.location_node,
            )
        )
        restored = min(requested_points, missing, rate * max_days)
        service_days = max(1, ceil(restored / rate))
        vessel_after = replace(
            state.vessel,
            clock=state.vessel.clock.advance(service_days),
            condition=min(100.0, state.vessel.condition + restored),
        )
        after = replace(state, vessel=vessel_after)
        if stop.node_id in self.ONE_SHOT_REPAIR_NODES:
            after = self._record_action(after, stop, "REPAIR")
        port_result = PortServiceResult(
            node_id=state.vessel.location_node,
            service=PortServiceKind.REPAIR,
            success=True,
            state_before=state.vessel,
            state_after=vessel_after,
            effect=restored,
            days_spent=service_days,
            blockers=(),
        )
        return SessionPortServiceResult(True, (), state, after, port_result)
