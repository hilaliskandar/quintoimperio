"""Estado comercial abstrato e operações de compra/venda.

Capital, quantidade, capacidade e preços são índices de simulação. O módulo não
pretende reproduzir moedas, pesos, volumes ou margens históricas. Restrições
específicas registradas em ``node_goods.csv`` não são anuladas por acesso
portuário genérico.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from quintoimperio.data.loader import RepositoryData

from .economy import EconomyModel


class TradeSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


@dataclass(frozen=True)
class CargoHolding:
    good_id: str
    quantity: float


@dataclass(frozen=True)
class CommercialState:
    capital_index: float
    capacity_total: float
    cargo: tuple[CargoHolding, ...] = ()

    def quantity_of(self, good_id: str) -> float:
        return sum(item.quantity for item in self.cargo if item.good_id == good_id)


@dataclass(frozen=True)
class TradeQuote:
    node_id: str
    good_id: str
    side: TradeSide
    unit_price_index: float
    bulk_per_unit: float
    market_price_index: float


@dataclass(frozen=True)
class TradeResult:
    executed: bool
    reasons: tuple[str, ...]
    state_before: CommercialState
    state_after: CommercialState
    quote: TradeQuote | None
    quantity: float
    total_value_index: float


class TradeModel:
    """Opera sobre mercados documentados e cotações relativas do protótipo."""

    def __init__(self, root: Path | None = None) -> None:
        repository = RepositoryData(root)
        self.root = repository.root
        self.economy = EconomyModel(self.root)
        self.rules = {
            (row["rule_type"], row["key"]): float(row["value"])
            for row in repository.simulation("trade_rules.csv")
        }

    def _rule(self, rule_type: str, key: str) -> float:
        try:
            return self.rules[(rule_type, key)]
        except KeyError as exc:
            raise KeyError(f"Regra comercial ausente: {rule_type}/{key}") from exc

    def bulk_per_unit(self, good_id: str) -> float:
        return float(self.economy.goods[good_id]["bulk_index"])

    def capacity_used(self, state: CommercialState) -> float:
        return sum(self.bulk_per_unit(item.good_id) * item.quantity for item in state.cargo)

    def capacity_free(self, state: CommercialState) -> float:
        return max(0.0, state.capacity_total - self.capacity_used(state))

    def good_restricted(self, node_id: str, good_id: str, year: int) -> bool:
        row = self.economy.node_good(node_id, good_id, year)
        return row is not None and row.get("restricted") == "TRUE"

    def quote(
        self,
        node_id: str,
        good_id: str,
        side: TradeSide | str,
        *,
        year: int = 1498,
        seed: int = 0,
    ) -> TradeQuote | None:
        side = TradeSide(side)
        market = self.economy.market_quote(node_id, good_id, year=year, seed=seed)
        if market is None:
            return None

        price = market["price_index"]
        multiplier = self._rule(
            "MARKET", "BUY_MULTIPLIER" if side is TradeSide.BUY else "SELL_MULTIPLIER"
        )
        return TradeQuote(
            node_id=node_id,
            good_id=good_id,
            side=side,
            unit_price_index=price * multiplier,
            bulk_per_unit=self.bulk_per_unit(good_id),
            market_price_index=price,
        )

    @staticmethod
    def _replace_quantity(
        state: CommercialState, good_id: str, new_quantity: float, new_capital: float
    ) -> CommercialState:
        cargo = [item for item in state.cargo if item.good_id != good_id]
        if new_quantity > 1e-12:
            cargo.append(CargoHolding(good_id=good_id, quantity=new_quantity))
        cargo.sort(key=lambda item: item.good_id)
        return CommercialState(
            capital_index=new_capital,
            capacity_total=state.capacity_total,
            cargo=tuple(cargo),
        )

    def buy(
        self,
        state: CommercialState,
        node_id: str,
        good_id: str,
        quantity: float,
        *,
        year: int = 1498,
        seed: int = 0,
    ) -> TradeResult:
        reasons: list[str] = []
        if quantity <= 0:
            reasons.append("QUANTITY_MUST_BE_POSITIVE")

        quote = self.quote(node_id, good_id, TradeSide.BUY, year=year, seed=seed)
        if quote is None:
            reasons.append("GOOD_NOT_DOCUMENTED_IN_MARKET")
        elif self.good_restricted(node_id, good_id, year):
            reasons.append("GOOD_RESTRICTED_BY_HISTORICAL_ACCESS_REGIME")

        if quote is not None and quantity > 0:
            required_capacity = quote.bulk_per_unit * quantity
            total = quote.unit_price_index * quantity
            if required_capacity > self.capacity_free(state) + 1e-12:
                reasons.append("INSUFFICIENT_CARGO_CAPACITY")
            if total > state.capital_index + 1e-12:
                reasons.append("INSUFFICIENT_CAPITAL")
        else:
            total = 0.0

        if reasons:
            return TradeResult(
                executed=False,
                reasons=tuple(reasons),
                state_before=state,
                state_after=state,
                quote=quote,
                quantity=quantity,
                total_value_index=total,
            )

        assert quote is not None
        current = state.quantity_of(good_id)
        after = self._replace_quantity(
            state,
            good_id,
            current + quantity,
            state.capital_index - total,
        )
        return TradeResult(
            executed=True,
            reasons=(),
            state_before=state,
            state_after=after,
            quote=quote,
            quantity=quantity,
            total_value_index=total,
        )

    def sell(
        self,
        state: CommercialState,
        node_id: str,
        good_id: str,
        quantity: float,
        *,
        year: int = 1498,
        seed: int = 0,
    ) -> TradeResult:
        reasons: list[str] = []
        if quantity <= 0:
            reasons.append("QUANTITY_MUST_BE_POSITIVE")

        quote = self.quote(node_id, good_id, TradeSide.SELL, year=year, seed=seed)
        if quote is None:
            reasons.append("GOOD_NOT_DOCUMENTED_IN_MARKET")
        elif self.good_restricted(node_id, good_id, year):
            reasons.append("GOOD_RESTRICTED_BY_HISTORICAL_ACCESS_REGIME")

        current = state.quantity_of(good_id)
        if quantity > current + 1e-12:
            reasons.append("INSUFFICIENT_INVENTORY")

        total = quote.unit_price_index * quantity if quote is not None and quantity > 0 else 0.0
        if reasons:
            return TradeResult(
                executed=False,
                reasons=tuple(reasons),
                state_before=state,
                state_after=state,
                quote=quote,
                quantity=quantity,
                total_value_index=total,
            )

        assert quote is not None
        after = self._replace_quantity(
            state,
            good_id,
            current - quantity,
            state.capital_index + total,
        )
        return TradeResult(
            executed=True,
            reasons=(),
            state_before=state,
            state_after=after,
            quote=quote,
            quantity=quantity,
            total_value_index=total,
        )
