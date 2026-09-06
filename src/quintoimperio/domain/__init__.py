"""Regras de dominio independentes da interface grafica."""

from .access import AccessModel, AccessRule, AccessStatus, AccessView
from .calendar import GameClock, MonsoonPhase, monsoon_phase
from .campaign import HistoricalCampaignModel
from .campaign_progress import (
    CampaignMilestone,
    CampaignProgress,
    CampaignProgressModel,
    CampaignSummary,
)
from .economy import EconomyModel
from .expedition import ExpeditionLeg, ExpeditionModel
from .fleet import (
    ConsumableRates,
    EvidenceClass,
    FleetModel,
    FleetState,
    PhysicalVessel,
    ProvisionLoad,
)
from .information import (
    InformationChannel,
    InformationModel,
    InformationOpportunity,
    InformationRule,
)
from .knowledge import KnowledgeLevel, KnowledgeModel, KnowledgeState
from .navigation import NavigationModel, great_circle_nm
from .persistence import CampaignPersistence, CampaignSave, SAVE_SCHEMA_VERSION
from .port import (
    PortServiceKind,
    PortServiceModel,
    PortServiceQuote,
    PortServiceResult,
    ServiceAvailability,
)
from .relationship import HistoricalActor, NodeActor, RelationshipModel, RelationshipStatus
from .relationship_session import RelationshipSessionModel, SessionRelationshipResult
from .route_knowledge import RouteKnowledgeModel
from .service_knowledge import (
    ServiceAwareSessionState,
    ServiceKnowledgeRecord,
    ServiceKnowledgeSessionModel,
    ServiceKnowledgeStatus,
    ServiceKnowledgeView,
)
from .session import (
    AccessRecord,
    GameSessionModel,
    GameSessionState,
    MarketEntry,
    MarketView,
    NodeKnowledgeRecord,
    RelationshipRecord,
    RouteKnowledgeRecord,
    SessionAccessResult,
    SessionInformationResult,
    SessionPortServiceResult,
    SessionTradeResult,
    SessionWaitResult,
)
from .stop import ChronologyMode, ExpeditionStop, ExpeditionStopModel
from .trade import CargoHolding, CommercialState, TradeModel, TradeQuote, TradeResult, TradeSide
from .travel import NavigationBasis, TravelModel, VesselState, VoyagePlan
from .voyage_event import VoyageEvent, VoyageEventModel, VoyageEventRule, VoyageEventType
from .world_map import MapEdge, MapExtent, MapPoint, WorldMapModel

__all__ = [
    "AccessModel",
    "AccessRecord",
    "AccessRule",
    "AccessStatus",
    "AccessView",
    "CampaignMilestone",
    "CampaignPersistence",
    "CampaignProgress",
    "CampaignProgressModel",
    "CampaignSave",
    "CampaignSummary",
    "CargoHolding",
    "ChronologyMode",
    "CommercialState",
    "ConsumableRates",
    "EconomyModel",
    "EvidenceClass",
    "ExpeditionLeg",
    "ExpeditionModel",
    "ExpeditionStop",
    "ExpeditionStopModel",
    "FleetModel",
    "FleetState",
    "GameClock",
    "GameSessionModel",
    "GameSessionState",
    "HistoricalActor",
    "HistoricalCampaignModel",
    "InformationChannel",
    "InformationModel",
    "InformationOpportunity",
    "InformationRule",
    "KnowledgeLevel",
    "KnowledgeModel",
    "KnowledgeState",
    "MapEdge",
    "MapExtent",
    "MapPoint",
    "MarketEntry",
    "MarketView",
    "MonsoonPhase",
    "NavigationBasis",
    "NavigationModel",
    "NodeActor",
    "NodeKnowledgeRecord",
    "PhysicalVessel",
    "PortServiceKind",
    "PortServiceModel",
    "PortServiceQuote",
    "PortServiceResult",
    "ProvisionLoad",
    "RelationshipModel",
    "RelationshipRecord",
    "RelationshipSessionModel",
    "RelationshipStatus",
    "RouteKnowledgeModel",
    "RouteKnowledgeRecord",
    "SAVE_SCHEMA_VERSION",
    "ServiceAvailability",
    "ServiceAwareSessionState",
    "ServiceKnowledgeRecord",
    "ServiceKnowledgeSessionModel",
    "ServiceKnowledgeStatus",
    "ServiceKnowledgeView",
    "SessionAccessResult",
    "SessionInformationResult",
    "SessionPortServiceResult",
    "SessionRelationshipResult",
    "SessionTradeResult",
    "SessionWaitResult",
    "TradeModel",
    "TradeQuote",
    "TradeResult",
    "TradeSide",
    "TravelModel",
    "VesselState",
    "VoyageEvent",
    "VoyageEventModel",
    "VoyageEventRule",
    "VoyageEventType",
    "VoyagePlan",
    "WorldMapModel",
    "great_circle_nm",
    "monsoon_phase",
]
