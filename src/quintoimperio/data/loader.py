"""Utilitários mínimos de carregamento da base versionada do projeto."""

from __future__ import annotations

import csv
from pathlib import Path


def discover_project_root(start: Path | None = None) -> Path:
    """Localiza a raiz do checkout a partir de um caminho do pacote.

    A v0.1 assume execução a partir de um checkout do repositório. Empacotamento
    dos CSVs como recursos da distribuição será tratado quando houver build do
    primeiro executável.
    """
    current = (start or Path(__file__)).resolve()
    candidates = [current.parent, *current.parents]
    for candidate in candidates:
        if (candidate / "data" / "nodes.csv").exists() and (
            candidate / "simulation" / "rules.csv"
        ).exists():
            return candidate
    raise FileNotFoundError("Não foi possível localizar a raiz do projeto Quinto Império.")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class RepositoryData:
    """Acesso somente-leitura aos CSVs do checkout."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = Path(root) if root else discover_project_root()

    def historical(self, filename: str) -> list[dict[str, str]]:
        return read_csv(self.root / "data" / filename)

    def simulation(self, filename: str) -> list[dict[str, str]]:
        return read_csv(self.root / "simulation" / filename)
