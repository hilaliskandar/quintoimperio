"""Regimes de acesso portuário separados de conhecimento e reputação.

A classificação histórica/inferencial do porto vem de ``data/nodes.csv``. A
conversão para estados jogáveis e o custo de tempo da negociação pertencem a
``simulation/access_rules.csv``. A v0.1 não inventa taxas, presentes, contratos
ou probabilidade de sucesso diplomático.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from quintoimperio.data.loader import RepositoryData


class AccessStatus(str, Enum):
    OPEN = "OPEN"
    NEGOTIATION_REQUIRED = "NEGOTIATION_REQUIRED"
    NEGOTIATED = "NEGOTIATED"
    RESTRICTED = "RESTRICTED"
    NONCOMMERCIAL = "NONCOMMERCIAL"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class AccessRule:
    access_regime: str
    initial_status: AccessStatus
    negotiable: bool
    time_days: int


@dataclass(frozen=True)
class AccessView:
    node_id: str
    access_regime: str
    status: AccessStatus
    commercial_access: bool
    negotiable: bool
    time_days: int
    broker_availability: str


class AccessModel:
    """Traduz o regime documentado do nó em um gate institucional conservador."""

    def __init__(self, root: Path | None = None) -> None:
        repository = RepositoryData(root)
        self.root = repository.root
        self.nodes = {
            row["node_id"]: row for row in repository.historical("nodes.csv")
        }
        self.rules: dict[str, AccessRule] = {}
        for row in repository.simulation("access_rules.csv"):
            rule = AccessRule(
                access_regime=row["access_regime"],
                initial_status=AccessStatus(row["initial_status"]),
                negotiable=row["negotiable"] == "TRUE",
                time_days=int(row["time_days"]),
            )
            self.rules[rule.access_regime] = rule

    def initial_status(self, node_id: str) -> AccessStatus:
        regime = self.nodes[node_id].get("access_regime", "")
        rule = self.rules.get(regime)
        return rule.initial_status if rule is not None else AccessStatus.UNKNOWN

    @staticmethod
    def commercial_access(status: AccessStatus) -> bool:
        return status in {AccessStatus.OPEN, AccessStatus.NEGOTIATED}

    def view(self, node_id: str, status: AccessStatus | str) -> AccessView:
        status = AccessStatus(status)
        node = self.nodes[node_id]
        regime = node.get("access_regime", "")
        rule = self.rules.get(regime)
        negotiable = (
            status is AccessStatus.NEGOTIATION_REQUIRED
            and rule is not None
            and rule.negotiable
            and node.get("market_scale", "") not in {"", "NONE"}
        )
        return AccessView(
            node_id=node_id,
            access_regime=regime,
            status=status,
            commercial_access=self.commercial_access(status),
            negotiable=negotiable,
            time_days=rule.time_days if negotiable and rule is not None else 0,
            broker_availability=node.get("broker_availability", "") or "UNKNOWN",
        )

    def negotiate(self, node_id: str, status: AccessStatus | str) -> AccessStatus:
        """Conclui a ação genérica sem sorteio de sucesso na v0.1.

        O resultado significa apenas que o gate abstrato foi satisfeito. Não
        afirma que uma audiência, presente ou acordo histórico específico
        ocorreu.
        """
        view = self.view(node_id, status)
        if not view.negotiable:
            raise ValueError("ACCESS_NEGOTIATION_NOT_AVAILABLE")
        return AccessStatus.NEGOTIATED
