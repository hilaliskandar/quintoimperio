"""Navegação v0.1: distância geodésica, calibração e duração relativa."""

from __future__ import annotations

import math
import random
from datetime import date
from pathlib import Path
from statistics import mean

from quintoimperio.data.loader import RepositoryData


EARTH_RADIUS_NM = 3440.065


def great_circle_nm(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distância ortodrômica em milhas náuticas entre duas âncoras cartográficas."""
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return EARTH_RADIUS_NM * c


def _parse_date(value: str) -> date:
    return date.fromisoformat(value)


class NavigationModel:
    """Primeiro modelo determinístico de navegação, independente da interface.

    As distâncias são geodésicas calculadas a partir das âncoras modernas em
    ``nodes.csv``. Elas não são distâncias históricas efetivamente navegadas.
    A taxa diária de referência é calibrada pela travessia Melinde–Calecute de
    1498 e não deve ser interpretada como velocidade histórica universal.
    """

    def __init__(self, root: Path | None = None) -> None:
        repository = RepositoryData(root)
        self.root = repository.root
        self.nodes = {
            row["node_id"]: row for row in repository.historical("nodes.csv")
        }
        self.routes = {
            row["route_id"]: row for row in repository.historical("routes.csv")
        }
        self.observations = repository.historical("voyage_observations.csv")

        self.navigation_rules: dict[tuple[str, str], str] = {}
        for row in repository.simulation("navigation_rules.csv"):
            self.navigation_rules[(row["rule_type"], row["key"])] = row["value"]

    def route_geodesic_nm(self, route_id: str) -> float | None:
        route = self.routes[route_id]
        origin = self.nodes[route["origin_node"]]
        destination = self.nodes[route["destination_node"]]

        coordinates = (
            origin.get("latitude"),
            origin.get("longitude"),
            destination.get("latitude"),
            destination.get("longitude"),
        )
        if any(value in (None, "") for value in coordinates):
            return None

        return great_circle_nm(
            float(origin["latitude"]),
            float(origin["longitude"]),
            float(destination["latitude"]),
            float(destination["longitude"]),
        )

    def observed_days(self, route_id: str) -> list[int]:
        days: list[int] = []
        for row in self.observations:
            if row["route_id"] != route_id:
                continue
            if row.get("observed_days"):
                days.append(int(row["observed_days"]))
            else:
                days.append(
                    (_parse_date(row["arrival_date"]) - _parse_date(row["departure_date"])).days
                )
        return days

    @property
    def reference_route_id(self) -> str:
        for (rule_type, key), value in self.navigation_rules.items():
            if rule_type == "REFERENCE_ROUTE" and value == "1":
                return key
        raise KeyError("Nenhuma REFERENCE_ROUTE foi definida em navigation_rules.csv")

    @property
    def reference_daily_nm(self) -> float:
        route_id = self.reference_route_id
        distance = self.route_geodesic_nm(route_id)
        observations = self.observed_days(route_id)
        if distance is None or not observations:
            raise ValueError("A rota de referência não possui distância e observações suficientes.")
        return distance / mean(observations)

    def seasonal_multiplier(self, route_id: str, departure: date) -> float:
        dependency = self.routes[route_id]["monsoon_dependence"] or "NONE"
        if departure.month in (6, 7):
            key = ("JUNE_JULY_MULTIPLIER", dependency)
        else:
            key = ("OTHER_MONTH_MULTIPLIER", dependency)
        try:
            return float(self.navigation_rules[key])
        except KeyError as exc:
            raise KeyError(f"Regra de navegação ausente para {key[0]}/{key[1]}") from exc

    def estimate_duration_days(
        self, route_id: str, departure: date, seed: int = 0
    ) -> float | None:
        """Duração estimada em dias para comparação interna do protótipo.

        A v0.1 usa distância geodésica, taxa de progresso calibrada e uma
        penalidade sazonal conservadora. Não infere automaticamente que uma
        direção específica é favorecida pela monção: isso exigirá evidência
        regional por rota.
        """
        distance = self.route_geodesic_nm(route_id)
        if distance is None:
            return None

        base_days = distance / self.reference_daily_nm
        seasonal = self.seasonal_multiplier(route_id, departure)
        noise_fraction = float(
            self.navigation_rules[("DURATION_NOISE_FRACTION", "DEFAULT")]
        )
        rng = random.Random(f"navigation:{seed}:{route_id}:{departure.isoformat()}")
        noise = rng.uniform(1.0 - noise_fraction, 1.0 + noise_fraction)
        return base_days * seasonal * noise
