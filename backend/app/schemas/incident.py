from pydantic import BaseModel
from typing import List, Dict, Optional, Any

from app.graph.state import TraceEntry


class EnvironmentContext(BaseModel):
    mfa_enabled: bool
    endpoint_monitoring: bool
    network_segmentation: bool


class IncidentRequest(BaseModel):
    initial_vector: str
    confirmed_actions: List[str]
    non_actions: List[str]
    environment_context: EnvironmentContext
    audience_level: str  # "technical" | "non_technical"
    explanation_mode: str = "fast"  # "fast" | "deep"


class IncidentResponse(BaseModel):
    attacker_narrative: str
    decision_summary: List[str]
    confidence: float
    trace: List[TraceEntry]

class ReplayRequest(BaseModel):
    base_incident: IncidentRequest

    # What-if overrides
    override_environment: Optional[Dict[str, Any]] = None
    override_confirmed_actions: Optional[list[str]] = None
    override_non_actions: Optional[list[str]] = None

