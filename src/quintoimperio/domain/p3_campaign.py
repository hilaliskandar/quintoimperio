"""Fachada incremental para campanhas P3 já normalizadas.

A classe reutiliza integralmente ``HistoricalCampaignModel``. Ela só define
estados iniciais das novas expedições e ações específicas sustentadas por
permanências documentadas; rotas, cronologia, logística, risco e persistência
continuam pertencendo aos modelos existentes. Valores de provisões são
parâmetros abstratos de simulação e não alegações históricas.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import date
from pathlib import Path

from quintoimperio.data.loader import RepositoryData

from .campaign import HistoricalCampaignModel
from .port import PortServiceKind, PortServiceResult
from .session import GameSessionState, SessionPortServiceResult
from .stop import ChronologyMode, ExpeditionStop


class P3CampaignModel(HistoricalCampaignModel):
    """Extensão opt-in para as campanhas documentadas a partir de 1500."""

    CABRAL_PREDEPARTURE_START = date(1500, 3, 7)
    CABRAL_DEPARTURE = date(1500, 3, 9)
    CABRAL_EXPEDITION_ID = "EXP_CABRAL_1500"
    CABRAL_DOCUMENTED_PROVISION_ACTIVITIES = frozenset({"WATER", "WOOD", "REFRESHMENTS"})
    CABRAL_ONE_SHOT_PROVISION_NODES = frozenset({"VCR", "MOZ", "MAL"})

    def __init__(self, root: Path | None = None) -> None:
        super().__init__(root)
        repository = RepositoryData(root)
        self.p3_rules = {
            (row["rule_type"], row["key"]): float(row["value"])
            for row in repository.simulation("p3_rules.csv")
        }

    def initial_cabral_state(
        self,
        *,
        provision_days: float = 60.0,
        condition: float = 100.0,
        capital_index: float = 100.0,
        capacity_total: float = 30.0,
    ) -> GameSessionState:
        """Abre a tranche Cabral na partida documental de 09/03/1500."""
        return self.session.initial_state(
            location_node="LIS",
            start_date=self.CABRAL_DEPARTURE,
            provision_days=provision_days,
            condition=condition,
            capital_index=capital_index,
            capacity_total=capacity_total,
            active_expedition_id=self.CABRAL_EXPEDITION_ID,
            chronology_mode=ChronologyMode.GUIDED,
        )

    def initial_cabral_playable_state(
        self,
        *,
        provision_days: float = 60.0,
        condition: float = 100.0,
        capital_index: float = 100.0,
        capacity_total: float = 30.0,
    ) -> GameSessionState:
        """Abre dois dias simulados de preparação antes da partida documental.

        07/03/1500 é uma camada de jogo, não uma alegação histórica sobre o início
        do aprestamento da armada. A partida guiada continua fixada em 09/03/1500
        pela observação da primeira perna, reproduzindo a separação já usada no MVP.
        """
        return self.session.initial_state(
            location_node="LIS",
            start_date=self.CABRAL_PREDEPARTURE_START,
            provision_days=provision_days,
            condition=condition,
            capital_index=capital_index,
            capacity_total=capacity_total,
            active_expedition_id=self.CABRAL_EXPEDITION_ID,
            chronology_mode=ChronologyMode.GUIDED,
        )

    @staticmethod
    def _cabral_action_key(stop: ExpeditionStop, action: str) -> str:
        return f"P3_ACTION:{stop.stop_id}:{action}"

    def _cabral_action_used(
        self, state: GameSessionState, stop: ExpeditionStop, action: str
    ) -> bool:
        return self._cabral_action_key(stop, action) in state.information_history

    def _record_cabral_action(
        self, state: GameSessionState, stop: ExpeditionStop, action: str
    ) -> GameSessionState:
        key = self._cabral_action_key(stop, action)
        if key in state.information_history:
            return state
        return replace(state, information_history=state.information_history + (key,))

    def documented_cabral_stop_can_reprovision(self, state: GameSessionState) -> bool:
        """Expõe apenas a ação material documentada na escala ativa de Cabral."""
        stop = self.session.active_stop(state)
        if not (
            stop is not None
            and stop.expedition_id == self.CABRAL_EXPEDITION_ID
            and stop.node_id == state.vessel.location_node
            and self.CABRAL_DOCUMENTED_PROVISION_ACTIVITIES.intersection(stop.activities)
        ):
            return False
        return not (
            stop.node_id in self.CABRAL_ONE_SHOT_PROVISION_NODES
            and self._cabral_action_used(state, stop, "PROVISIONS")
        )

    def reprovision_at_documented_cabral_stop(
        self, state: GameSessionState
    ) -> SessionPortServiceResult:
        """Projeta aguada/refrescos documentados em autonomia abstrata one-shot.

        O efeito é parametrizado em ``simulation/p3_rules.csv`` e não transforma
        Vera Cruz, Moçambique ou Melinde em serviços genéricos de provisões.
        """
        stop = self.session.active_stop(state)
        blockers: tuple[str, ...] = ()
        if stop is None:
            blockers = ("NO_ACTIVE_EXPEDITION_STOP",)
        elif stop.expedition_id != self.CABRAL_EXPEDITION_ID:
            blockers = ("STOP_NOT_PART_OF_CABRAL_EXPEDITION",)
        elif stop.node_id != state.vessel.location_node:
            blockers = ("VESSEL_NOT_AT_DOCUMENTED_STOP",)
        elif not self.CABRAL_DOCUMENTED_PROVISION_ACTIVITIES.intersection(stop.activities):
            blockers = ("STOP_HAS_NO_DOCUMENTED_PROVISION_ACTIVITY",)
        elif (
            stop.node_id in self.CABRAL_ONE_SHOT_PROVISION_NODES
            and self._cabral_action_used(state, stop, "PROVISIONS")
        ):
            blockers = ("DOCUMENTED_PROVISION_ACTION_ALREADY_USED",)

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

        assert stop is not None
        capacity = self.p3_rules[
            ("DOCUMENTED_STOP_PROVISION_CAPACITY_PER_ACTION", stop.node_id)
        ]
        service_days = int(
            self.p3_rules[("DOCUMENTED_STOP_PROVISION_SERVICE_DAYS", stop.node_id)]
        )
        max_onboard = self.session.port.rules[("PROVISION_MAX_ONBOARD", "DEFAULT")]
        remaining_capacity = max(0.0, max_onboard - state.vessel.provision_days)
        added = min(capacity, remaining_capacity)
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
        if stop.node_id in self.CABRAL_ONE_SHOT_PROVISION_NODES:
            after = self._record_cabral_action(after, stop, "PROVISIONS")
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
