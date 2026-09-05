#!/usr/bin/env python3
"""Inspeção humana do primeiro ciclo de compra e venda."""

from quintoimperio.domain import CommercialState, TradeModel


def main() -> None:
    model = TradeModel()
    state = CommercialState(capital_index=100.0, capacity_total=30.0)

    print("Quinto Império — comércio v0.1")
    print("Capital, quantidade, capacidade e preços são índices abstratos de simulação.")
    print()

    buy = model.buy(state, "CAL", "PEPPER", 2.0, year=1498, seed=1498)
    print("Compra CAL/PEPPER:", buy.executed, buy.reasons)
    if buy.quote:
        print(f"  índice unitário de compra: {buy.quote.unit_price_index:.2f}")
    print(f"  capital: {state.capital_index:.2f} -> {buy.state_after.capital_index:.2f}")
    print(f"  pimenta: {state.quantity_of('PEPPER'):.2f} -> {buy.state_after.quantity_of('PEPPER'):.2f}")
    print(f"  capacidade usada: {model.capacity_used(buy.state_after):.2f}/{buy.state_after.capacity_total:.2f}")
    print()

    sell = model.sell(buy.state_after, "ADE", "PEPPER", 2.0, year=1498, seed=1498)
    print("Venda ADE/PEPPER:", sell.executed, sell.reasons)
    if sell.quote:
        print(f"  índice unitário de venda: {sell.quote.unit_price_index:.2f}")
    print(f"  capital: {buy.state_after.capital_index:.2f} -> {sell.state_after.capital_index:.2f}")
    print(f"  pimenta restante: {sell.state_after.quantity_of('PEPPER'):.2f}")


if __name__ == "__main__":
    main()
