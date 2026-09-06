"""Progresso e encerramento da vertical slice Lisboa–Calecute.

A camada M4 não cria quests, recompensas ou fatos históricos. Os marcos são
leituras derivadas do estado já mantido pela sessão: localização, expedição,
conhecimento, relações, acesso e estado comercial. Assim, nenhum marco duplica
as regras dos respectivos modelos de domínio.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .knowledge import KnowledgeLevel
from .session import GameSessionModel, GameSessionState
from .stop import ChronologyMode


@dataclass(frozen=True)
class CampaignMilestone:
    milestone_id: str
    label: str
    completed: bool


@dataclass(frozen=True)
class CampaignProgress:
    milestones: tuple[CampaignMilestone, ...]
    completed: bool
    current_objective: str


@dataclass(frozen=True)
class CampaignSummary:
    completed: bool
    current_date: date
    chronology_mode: ChronologyMode
    location_node: str
    knowledge_nodes: int
    contacted_actor_ids: tuple[str, ...]
    capital_index: float
    capacity_used: float
    capacity_total: float
    cargo: tuple[tuple[str, float], ...]
    counterfactual: bool


class CampaignProgressModel:
    """Projeta objetivos do MVP a partir do estado real da sessão."""

    EXPEDITION_ID = "EXP_GAMA_1497"
    FINAL_NODE = "CAL"
    START_NODE = "LIS"
    START_DATE = date(1497, 7, 8)

    def __init__(self, session: GameSessionModel) -> None:
        self.session = session

    def _fleet_participation(self, state: GameSessionState) -> bool:
        return (
            state.active_expedition_id == self.EXPEDITION_ID
            or state.vessel.location_node != self.START_NODE
            or state.vessel.clock.current_date > self.START_DATE
        )

    def _arrived_calicut(self, state: GameSessionState) -> bool:
        return (
            state.vessel.location_node == self.FINAL_NODE
            and state.active_expedition_id is None
        )

    def _calicut_knowledge(self, state: GameSessionState) -> bool:
        if not self._arrived_calicut(state):
            return False
        knowledge = self.session.node_state(state, self.FINAL_NODE)
        return knowledge.market >= KnowledgeLevel.OPERATIONAL

    def _has_contact(self, state: GameSessionState) -> bool:
        return bool(self.session.contacted_relationships(state))

    def _calicut_access(self, state: GameSessionState) -> bool:
        if not self._arrived_calicut(state):
            return False
        return self.session.access_view(state, self.FINAL_NODE).commercial_access

    @staticmethod
    def _has_commercial_cargo(state: GameSessionState) -> bool:
        # A campanha histórica começa sem carga comercial. No escopo do MVP,
        # carga positiva em Calecute só pode resultar de uma compra explícita;
        # serviços portuários não alteram CommercialState.
        return any(item.quantity > 0 for item in state.commerce.cargo)

    def progress(self, state: GameSessionState) -> CampaignProgress:
        arrived = self._arrived_calicut(state)
        access = self._calicut_access(state)
        traded = arrived and access and self._has_commercial_cargo(state)
        milestones = (
            CampaignMilestone(
                "FLEET_PARTICIPATION",
                "Participar da armada de 1497",
                self._fleet_participation(state),
            ),
            CampaignMilestone(
                "DOCUMENTED_CONTACT",
                "Estabelecer contato com ator documentado",
                self._has_contact(state),
            ),
            CampaignMilestone(
                "ARRIVE_CALICUT",
                "Chegar a Calecute",
                arrived,
            ),
            CampaignMilestone(
                "CALICUT_KNOWLEDGE",
                "Obter conhecimento operacional do mercado de Calecute",
                self._calicut_knowledge(state),
            ),
            CampaignMilestone(
                "CALICUT_ACCESS",
                "Negociar acesso comercial em Calecute",
                access,
            ),
            CampaignMilestone(
                "FIRST_TRADE",
                "Realizar a primeira compra comercial em Calecute",
                traded,
            ),
        )
        completed = arrived and self._calicut_knowledge(state) and access and traded
        current = next(
            (item.label for item in milestones if not item.completed),
            "Campanha concluída em Calecute",
        )
        return CampaignProgress(
            milestones=milestones,
            completed=completed,
            current_objective=current,
        )

    def summary(self, state: GameSessionState) -> CampaignSummary:
        progress = self.progress(state)
        knowledge_nodes = sum(
            1
            for record in state.node_knowledge
            if any(
                level > KnowledgeLevel.UNKNOWN
                for level in (
                    record.state.geo,
                    record.state.nav,
                    record.state.market,
                    record.state.political,
                )
            )
        )
        contacts = tuple(
            sorted(actor.actor_id for actor in self.session.contacted_relationships(state))
        )
        cargo = tuple(
            sorted(
                (item.good_id, item.quantity)
                for item in state.commerce.cargo
                if item.quantity > 0
            )
        )
        return CampaignSummary(
            completed=progress.completed,
            current_date=state.vessel.clock.current_date,
            chronology_mode=state.chronology_mode,
            location_node=state.vessel.location_node,
            knowledge_nodes=knowledge_nodes,
            contacted_actor_ids=contacts,
            capital_index=state.commerce.capital_index,
            capacity_used=self.session.trade.capacity_used(state.commerce),
            capacity_total=state.commerce.capacity_total,
            cargo=cargo,
            counterfactual=state.chronology_mode is ChronologyMode.COUNTERFACTUAL,
        )
