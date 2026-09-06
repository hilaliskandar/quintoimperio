"""Estado epistêmico do jogador sobre serviços portuários.

A disponibilidade histórica continua pertencendo a ``PortServiceModel``. Esta
camada registra apenas o que o personagem já pode distinguir sobre essa
evidência e nunca converte campo histórico vazio em disponibilidade simulada.

A partir da v0.3, esta é também a fronteira jogável que impede antecipação do
evento marítimo: o plano exibido ao jogador é convertido novamente ao cenário-
base e a contingência é resolvida somente na execução.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from pathlib import Path

from quintoimperio.data.loader import RepositoryData

from .port import PortServiceKind, PortServiceQuote, ServiceAvailability
from .relationship_session import RelationshipSessionModel
from .session import GameSessionState, SessionPortServiceResult


class ServiceKnowledgeStatus(str, Enum):
    UNASSESSED = "UNASSESSED"
    DOCUMENTED = "DOCUMENTED"
    EVIDENCE_INDETERMINATE = "EVIDENCE_INDETERMINATE"


@dataclass(frozen=True)
class ServiceKnowledgeRecord:
    node_id: str
    service: PortServiceKind
    status: ServiceKnowledgeStatus
    revealed_availability: ServiceAvailability | None = None


@dataclass(frozen=True)
class ServiceKnowledgeView:
    node_id: str
    service: PortServiceKind
    knowledge_status: ServiceKnowledgeStatus
    revealed_availability: ServiceAvailability | None
    historical_documented: bool
    actionable: bool
    capacity_or_rate: float | None
    unit: str | None


@dataclass(frozen=True)
class ServiceAwareSessionState(GameSessionState):
    service_knowledge_records: tuple[ServiceKnowledgeRecord, ...] = ()


class ServiceKnowledgeSessionModel(RelationshipSessionModel):
    """Sessão que separa observação do jogador da evidência histórica bruta."""

    def __init__(self, root: Path | None = None) -> None:
        super().__init__(root)
        repository = RepositoryData(self.root)
        self.service_knowledge_rules = {
            (row["rule_type"], row["key"]): int(row["value"])
            for row in repository.simulation("service_knowledge_rules.csv")
        }

    @staticmethod
    def _records(state: GameSessionState) -> tuple[ServiceKnowledgeRecord, ...]:
        return tuple(getattr(state, "service_knowledge_records", ()))

    def service_knowledge_status(
        self,
        state: GameSessionState,
        node_id: str,
        service: PortServiceKind,
    ) -> ServiceKnowledgeRecord:
        for record in self._records(state):
            if record.node_id == node_id and record.service is service:
                return record
        return ServiceKnowledgeRecord(
            node_id=node_id,
            service=service,
            status=ServiceKnowledgeStatus.UNASSESSED,
        )

    @staticmethod
    def _as_service_state(state: GameSessionState) -> ServiceAwareSessionState:
        if isinstance(state, ServiceAwareSessionState):
            return state
        return ServiceAwareSessionState(
            vessel=state.vessel,
            commerce=state.commerce,
            node_knowledge=state.node_knowledge,
            route_knowledge=state.route_knowledge,
            access_records=state.access_records,
            relationship_records=state.relationship_records,
            active_expedition_id=state.active_expedition_id,
            expedition_leg_sequence=state.expedition_leg_sequence,
            chronology_mode=state.chronology_mode,
            active_stop_id=state.active_stop_id,
            information_history=state.information_history,
            voyage_event_history=state.voyage_event_history,
            service_knowledge_records=(),
        )

    def _replace_service_knowledge(
        self,
        state: GameSessionState,
        record: ServiceKnowledgeRecord,
    ) -> ServiceAwareSessionState:
        service_state = self._as_service_state(state)
        records = [
            item
            for item in service_state.service_knowledge_records
            if not (item.node_id == record.node_id and item.service is record.service)
        ]
        records.append(record)
        records.sort(key=lambda item: (item.node_id, item.service.value))
        return replace(service_state, service_knowledge_records=tuple(records))

    def observe_port_services(
        self,
        state: GameSessionState,
        node_id: str | None = None,
    ) -> ServiceAwareSessionState:
        """Registra somente o estado da evidência disponível no porto visitado."""
        target = node_id or state.vessel.location_node
        after = self._as_service_state(state)
        for service in PortServiceKind:
            quote = self.port.quote(target, service)
            if quote.availability is ServiceAvailability.UNKNOWN:
                record = ServiceKnowledgeRecord(
                    node_id=target,
                    service=service,
                    status=ServiceKnowledgeStatus.EVIDENCE_INDETERMINATE,
                    revealed_availability=None,
                )
            else:
                record = ServiceKnowledgeRecord(
                    node_id=target,
                    service=service,
                    status=ServiceKnowledgeStatus.DOCUMENTED,
                    revealed_availability=quote.availability,
                )
            after = self._replace_service_knowledge(after, record)
        return after

    def initial_state(self, **kwargs) -> ServiceAwareSessionState:
        base = super().initial_state(**kwargs)
        state = self._as_service_state(base)
        return self.observe_port_services(state, state.vessel.location_node)

    def service_view(
        self,
        state: GameSessionState,
        service: PortServiceKind,
        *,
        node_id: str | None = None,
    ) -> ServiceKnowledgeView:
        target = node_id or state.vessel.location_node
        record = self.service_knowledge_status(state, target, service)
        quote = self.port.quote(target, service)
        if record.status is ServiceKnowledgeStatus.UNASSESSED:
            return ServiceKnowledgeView(
                node_id=target,
                service=service,
                knowledge_status=record.status,
                revealed_availability=None,
                historical_documented=quote.documented,
                actionable=False,
                capacity_or_rate=None,
                unit=None,
            )
        if record.status is ServiceKnowledgeStatus.EVIDENCE_INDETERMINATE:
            return ServiceKnowledgeView(
                node_id=target,
                service=service,
                knowledge_status=record.status,
                revealed_availability=None,
                historical_documented=False,
                actionable=False,
                capacity_or_rate=None,
                unit=None,
            )
        return ServiceKnowledgeView(
            node_id=target,
            service=service,
            knowledge_status=record.status,
            revealed_availability=record.revealed_availability,
            historical_documented=True,
            actionable=quote.actionable,
            capacity_or_rate=quote.capacity_or_rate,
            unit=quote.unit,
        )

    @staticmethod
    def _translate_indeterminate(
        state: GameSessionState,
        result: SessionPortServiceResult,
    ) -> SessionPortServiceResult:
        if "SERVICE_AVAILABILITY_UNKNOWN" not in result.reasons:
            return result
        reasons = tuple(
            "HISTORICAL_SERVICE_EVIDENCE_INDETERMINATE"
            if reason == "SERVICE_AVAILABILITY_UNKNOWN"
            else reason
            for reason in result.reasons
        )
        service_result = replace(result.service_result, blockers=reasons)
        return SessionPortServiceResult(
            executed=False,
            reasons=reasons,
            state_before=state,
            state_after=state,
            service_result=service_result,
        )

    def reprovision(
        self, state: GameSessionState, requested_days: float
    ) -> SessionPortServiceResult:
        result = super().reprovision(state, requested_days)
        return self._translate_indeterminate(state, result)

    def repair(
        self, state: GameSessionState, requested_points: float
    ) -> SessionPortServiceResult:
        result = super().repair(state, requested_points)
        return self._translate_indeterminate(state, result)

    def plan_voyage(self, state: GameSessionState, route_id: str, **kwargs):
        """Expõe somente o cenário-base; o evento específico permanece oculto."""
        resolved_preview = super().plan_voyage(state, route_id, **kwargs)
        return self.travel.defer_plan(state.vessel, resolved_preview)

    def execute_voyage(self, state: GameSessionState, plan):
        """Resolve o evento na confirmação e só então delega a execução da sessão."""
        resolved = self.travel.resolve_voyage(state.vessel, plan)
        after = super().execute_voyage(state, resolved)
        return self.observe_port_services(after, after.vessel.location_node)
