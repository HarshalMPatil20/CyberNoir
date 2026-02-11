from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class IncidentInput(BaseModel):
    initial_vector: str
    confirmed_actions: List[str]
    non_actions: List[str]
    environment_context: Dict[str, bool]
    audience_level: str
    environment_context: Dict[str, bool] = Field(default_factory=dict)


class EvidenceState(BaseModel):
    confirmed: List[str] = []
    absent: List[str] = []
    unknown: List[str] = []


class AttackerViewState(BaseModel):
    visibility: Optional[str] = None        # "low" | "medium" | "high"
    confidence: Optional[str] = None        # "low" | "medium" | "high"


class GoalInferenceState(BaseModel):
    primary_goal: Optional[str] = None
    excluded_goals: List[str] = []


class RiskAssessmentState(BaseModel):
    escalation_risk: Optional[str] = None   # "low" | "medium" | "high"
    lateral_movement_risk: Optional[str] = None
    detection_strength: Optional[str] = None


class DecisionState(BaseModel):
    chosen_path: Optional[str] = None
    rejected_paths: List[Dict[str, str]] = []


class NarrativeState(BaseModel):
    attacker_narrative: Optional[str] = None
    confidence_score: Optional[float] = None


class TraceEntry(BaseModel):
    agent: str
    summary: str

class InferredAction(BaseModel):
    action: str
    confidence: float
    source: str = "ml"


class CyberNoirState(BaseModel):
    # Input
    incident: IncidentInput

    # Agent-owned sections
    evidence: EvidenceState = EvidenceState()
    attacker_view: AttackerViewState = AttackerViewState()
    goals: GoalInferenceState = GoalInferenceState()
    risks: RiskAssessmentState = RiskAssessmentState()
    decisions: DecisionState = DecisionState()
    narrative: NarrativeState = NarrativeState()
    trace: List[TraceEntry] = Field(default_factory=list)
    inferred_actions: Optional[List[InferredAction]] = []


