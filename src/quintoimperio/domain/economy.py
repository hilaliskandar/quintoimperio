"""Núcleo econômico relativo do Quinto Império.

O módulo consome evidência estruturada em ``data/`` e parâmetros de
balanceamento em ``simulation/``. Os índices calculados aqui não são preços,
fretes, alíquotas ou probabilidades históricas.
"""

from __future__ import annotations

import random
from pathlib import Path
from typing import Iterable

from quintoimperio.data.loader import RepositoryData


def _number(value: str | None, default: float = 0.0) -> float:
    if value is None or value == "":
        return default
    return float(value)


def _active(row: dict[str, str], year: int) -> bool:
    start = row.get("period_from", "")
    end = row.get("period_to", "")
    if start and year < int(start):
        return False
    if end and year > int(end):
        return False
    return True


class EconomyModel:
    """Modelo ordinal orientado por dados e independente da interface."""

    def __init__(self, root: Path | None = None) -> None:
        repository = RepositoryData(root)
        self.root = repository.root

        self.nodes = {
            row["node_id"]: row for row in repository.historical("nodes.csv")
        }
        self.node_goods = repository.historical("node_goods.csv")
        self.routes = {
            row["route_id"]: row for row in repository.historical("routes.csv")
        }
        self.route_goods = repository.historical("route_goods.csv")
        self.goods = {
            row["good_id"]: row for row in repository.simulation("goods_params.csv")
        }

        self.rules: dict[str, dict[str, dict[str, str]]] = {}
        for row in repository.simulation("rules.csv"):
            self.rules.setdefault(row["rule_type"], {})[row["key"]] = row

    def _rule(self, rule_type: str, key: str) -> dict[str, str]:
        try:
            return self.rules[rule_type][key]
        except KeyError as exc:
            raise KeyError(f"Regra ausente: {rule_type}/{key}") from exc

    def node_good(
        self, node_id: str, good_id: str, year: int = 1498
    ) -> dict[str, str] | None:
        candidates = [
            row
            for row in self.node_goods
            if row["node_id"] == node_id
            and row["good_id"] == good_id
            and _active(row, year)
        ]
        if not candidates:
            return None
        return sorted(candidates, key=lambda r: int(r.get("period_from") or 0))[-1]

    def availability_score(self, node_id: str, good_id: str, year: int = 1498) -> float:
        """Índice ordinal de disponibilidade comercial, não quantidade histórica."""
        row = self.node_good(node_id, good_id, year)
        if row is None:
            return 0.0

        role = self._rule("TRADE_ROLE", row["trade_role"])
        supply = _number(role.get("supply_index"))
        access = self._rule("ACCESS_REGIME", row["access_regime"])
        friction = _number(access.get("cost_index"))
        if friction >= 99:
            return 0.0
        restriction = 0.75 if row.get("restricted") == "TRUE" else 1.0
        return supply * restriction / (1.0 + friction)

    def volatility(self, node_id: str, good_id: str, year: int = 1498) -> float:
        """Volatilidade-base do estoque derivada da origem do fluxo."""
        row = self.node_good(node_id, good_id, year)
        if row is None:
            return 0.0
        rule = self._rule("SOURCE_TYPE", row.get("source_type") or "UNKNOWN")
        return _number(rule.get("volatility"))

    def exchange_power(self, good_id: str) -> float:
        """Capacidade relativa do bem de funcionar como meio de troca."""
        return _number(self.goods[good_id]["exchange_index"])

    def market_quote(
        self, node_id: str, good_id: str, year: int = 1498, seed: int = 0
    ) -> dict[str, float] | None:
        """Produz um índice relativo de mercado com choque determinístico."""
        row = self.node_good(node_id, good_id, year)
        if row is None:
            return None

        role_rule = self._rule("TRADE_ROLE", row["trade_role"])
        source_rule = self._rule("SOURCE_TYPE", row.get("source_type") or "UNKNOWN")
        access_rule = self._rule("ACCESS_REGIME", row["access_regime"])

        supply = _number(role_rule.get("supply_index"), 2.0)
        demand = _number(role_rule.get("demand_index"), 2.0)
        volatility = _number(source_rule.get("volatility"), 0.25)
        access_cost = _number(access_rule.get("cost_index"), 0.2)
        base_value = _number(self.goods[good_id]["base_value_index"], 1.0)

        rng = random.Random(f"{seed}:{year}:{node_id}:{good_id}")
        shock = rng.uniform(-volatility, volatility)
        stock_index = max(0.10, supply * (1.0 + shock))
        scarcity = (demand + 1.0) / (stock_index + 1.0)
        price_index = base_value * scarcity * (1.0 + access_cost)

        return {
            "supply_index": supply,
            "demand_index": demand,
            "volatility": volatility,
            "stock_index": stock_index,
            "access_cost_index": access_cost,
            "base_value_index": base_value,
            "price_index": price_index,
        }

    def route_supports_good(
        self, route_id: str, good_id: str, year: int = 1498
    ) -> bool:
        return any(
            row["route_id"] == route_id
            and row["good_id"] == good_id
            and _active(row, year)
            for row in self.route_goods
        )

    def goods_on_route(self, route_id: str, year: int = 1498) -> list[dict[str, str]]:
        return [
            row
            for row in self.route_goods
            if row["route_id"] == route_id and _active(row, year)
        ]

    def route_cost(
        self, route_id: str, good_id: str, year: int = 1498, seed: int = 0
    ) -> dict[str, float]:
        """Calcula componentes de custo em índices sem unidade monetária."""
        route = self.routes[route_id]
        good = self.goods[good_id]
        destination = self.nodes[route["destination_node"]]

        route_base = _number(
            self._rule("ROUTE_TYPE", route["route_type"]).get("cost_index"), 1.0
        )
        monsoon = _number(
            self._rule("MONSOON_DEPENDENCE", route["monsoon_dependence"]).get(
                "cost_index"
            )
        )
        access = _number(
            self._rule("ACCESS_REGIME", destination["access_regime"]).get(
                "cost_index"
            )
        )
        bulk = _number(good["bulk_index"], 3.0)
        value = _number(good["base_value_index"], 2.0)

        freight = route_base * bulk
        provisions = route_base * (1.0 + monsoon)
        taxation_access = access * value
        intermediation = (
            0.50 if destination["access_regime"] == "FOREIGN_NEGOTIATED" else 0.15
        )

        rng = random.Random(f"route:{seed}:{year}:{route_id}:{good_id}")
        operational_shock = rng.uniform(0.95, 1.05)
        total = (
            freight + provisions + taxation_access + intermediation
        ) * operational_shock

        return {
            "freight_index": freight,
            "provisions_index": provisions,
            "taxation_access_index": taxation_access,
            "intermediation_index": intermediation,
            "operational_shock": operational_shock,
            "total_cost_index": total,
        }

    def report_lines(self, year: int = 1498, seed: int = 1498) -> Iterable[str]:
        """Resumo textual para inspeção humana da calibração v0.1."""
        yield "Quinto Império — protótipo econômico relativo"
        yield "Índices de simulação; não representam preços históricos."
        yield ""

        for node_id, good_id in [
            ("CAL", "PEPPER"),
            ("MOZ", "PEPPER"),
            ("ELM", "GOLD"),
            ("CAM", "TEXTILE_IND"),
            ("MLK", "CLOVE"),
        ]:
            quote = self.market_quote(node_id, good_id, year=year, seed=seed)
            if quote is None:
                continue
            yield (
                f"{node_id}/{good_id}: disponibilidade="
                f"{self.availability_score(node_id, good_id, year):.2f}; "
                f"estoque={quote['stock_index']:.2f}; "
                f"índice-preço={quote['price_index']:.2f}; "
                f"volatilidade={quote['volatility']:.2f}"
            )

        yield ""
        route_cost = self.route_cost("R_CAM_MLK", "TEXTILE_IND", year=year, seed=seed)
        yield (
            "R_CAM_MLK/TEXTILE_IND: custo total relativo="
            f"{route_cost['total_cost_index']:.2f}"
        )
