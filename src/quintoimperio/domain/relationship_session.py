"""Consequências relacionais mínimas para a vertical slice do MVP.

A camada estende ``GameSessionModel`` sem criar reputação global, confiança
numérica ou efeitos econômicos automáticos. O único efeito relacional v0.2 é
local e explicitamente parametrizado: contato com autoridade documentada pode
ser requisito para atribuir ao personagem um piloto cuja provisão pela própria
autoridade é documentada.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path

from quintoimperio.data.loader import RepositoryData

from .relationship import HistoricalActor, RelationshipStatus
from .session import GameSessionModel, GameSessionState


@dataclass(frozen=True)
class SessionRelationshipResult:
    executed: bool
    reasons: tuple[str, ...]
    days_spent: int
    actor: HistoricalActor | None
    state_before: GameSessionState
    state_after: GameSessionState


class RelationshipSessionModel(GameSessionModel):
    """Sessão com uma ação relacional explícita e efeitos locais mínimos."""

    def __init__(self, root: Path | None = None) -> None:
        super().__init__(root)
        repository = RepositoryData(self.root)
        self.relationship_rules = {
            (row["rule_type"], row["key"]): row["value"]
            for row in repository.simulation("relationship_rules.csv")
        }

    def contact_authority(self, state: GameSessionState) -> SessionRelationshipResult:
        """Estabelece contato com autoridade normalizada sem conceder outros efeitos.

        O custo temporal é um parâmetro de simulação. A ação não negocia acesso,
        não altera conhecimento, mercado, capital, carga, provisões, condição ou
        qualquer preço.
        """
        node_id = state.vessel.location_node
        on_date = state.vessel.clock.current_date
        authority = self.relationship.actor_for_role(node_id, on_date, "AUTHORITY")
        if authority is None:
            return SessionRelationshipResult(
                executed=False,
                reasons=("NO_DOCUMENTED_AUTHORITY_ACTOR",),
                days_spent=0,
                actor=None,
                state_before=state,
                state_after=state,
            )

        if self.relationship_status(state, authority.actor_id) is RelationshipStatus.CONTACTED:
            return SessionRelationshipResult(
                executed=False,
                reasons=("AUTHORITY_ALREADY_CONTACTED",),
                days_spent=0,
                actor=authority,
                state_before=state,
                state_after=state,
            )

        days = int(self.relationship_rules[("CONTACT_TIME_DAYS", "AUTHORITY")])
        after = self._replace_relationship(
            state,
            authority.actor_id,
            RelationshipStatus.CONTACTED,
        )
        if days:
            after = self._replace_vessel(
                after,
                replace(after.vessel, clock=after.vessel.clock.advance(days)),
            )
        return SessionRelationshipResult(
            executed=True,
            reasons=(),
            days_spent=days,
            actor=authority,
            state_before=state,
            state_after=after,
        )

    def pilot_available_to_player(
        self,
        state: GameSessionState,
        pilot_id: str,
        route_id: str,
    ) -> bool:
        """Distingue disponibilidade histórica do piloto de atribuição ao personagem."""
        origin = state.vessel.location_node
        on_date = state.vessel.clock.current_date
        if not self.travel.pilot_can_guide(pilot_id, route_id, on_date, origin):
            return False

        required_actor = self.relationship_rules.get(
            ("PILOT_REQUIRES_ACTOR_CONTACT", pilot_id)
        )
        if required_actor is None:
            return True
        return (
            self.relationship_status(state, required_actor)
            is RelationshipStatus.CONTACTED
        )

    def recommended_pilot_id(
        self,
        state: GameSessionState,
        route_id: str,
    ) -> str | None:
        for pilot_id in sorted(self.travel.pilots):
            if self.pilot_available_to_player(state, pilot_id, route_id):
                return pilot_id
        return None
