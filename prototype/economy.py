"""Compatibilidade temporária com o protótipo econômico v0.1.

A implementação de produção foi movida para ``quintoimperio.domain.economy``.
Este arquivo permanece apenas como ponto de entrada textual durante a transição.
"""

from quintoimperio.domain import EconomyModel


if __name__ == "__main__":
    model = EconomyModel()
    print("\n".join(model.report_lines()))
