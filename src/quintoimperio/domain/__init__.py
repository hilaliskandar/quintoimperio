"""Regras de dominio independentes da interface grafica."""

from .calendar import GameClock, MonsoonPhase, monsoon_phase
from .economy import EconomyModel
from .knowledge import KnowledgeLevel, KnowledgeModel, KnowledgeState
from .navigation import NavigationModel, great_circle_nm
from .travel import NavigationBasis, TravelModel, VesselState, VoyagePlan

__all__ = [
    "EconomyModel",
    "GameClock",
    "KnowledgeLevel",
    "KnowledgeModel",
    "KnowledgeState",
    "MonsoonPhase",
    "NavigationBasis",
    "NavigationModel",
    "TravelModel",
    "VesselState",
    "VoyagePlan",
    "great_circle_nm",
    "monsoon_phase",
]
