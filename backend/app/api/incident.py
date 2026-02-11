from fastapi import APIRouter
from app.schemas.incident import IncidentRequest, IncidentResponse
from app.schemas.incident import ReplayRequest
from app.graph.state import IncidentInput, CyberNoirState
from app.core.replay import replay_incident
from app.graph.cybernoir_graph import run_cybernoir
from app.core.history import save_incident_history

router = APIRouter(prefix="/incident", tags=["CyberNoir Analysis"])


@router.post("/analyze", response_model=IncidentResponse)
def analyze_incident(payload: IncidentRequest):

    # Convert API payload → graph state
    initial_state = CyberNoirState(
        incident=IncidentInput(
            initial_vector=payload.initial_vector,
            confirmed_actions=payload.confirmed_actions,
            non_actions=payload.non_actions,
            environment_context=payload.environment_context.dict(),
            audience_level=payload.audience_level
        )
    )

    # Run agentic system
    final_state = run_cybernoir(initial_state)

    save_incident_history(
        mode="analyze",
        input_data=payload.model_dump(),
        decision=final_state.decisions.chosen_path,
        confidence=final_state.narrative.confidence_score,
        trace=final_state.trace
    )

    # Return customer-facing response
    return IncidentResponse(
        attacker_narrative=final_state.narrative.attacker_narrative,
        decision_summary=[final_state.decisions.chosen_path],
        confidence=final_state.narrative.confidence_score,
        trace=final_state.trace
    )





@router.post("/incident/replay")
def replay_incident_api(payload: ReplayRequest):

    # 🔹 Convert request → IncidentInput
    base_incident = IncidentInput(
        **payload.base_incident.model_dump()
    )

    # 🔹 Run base scenario
    base_state = run_cybernoir(
        CyberNoirState(incident=base_incident)
    )

    # 🔹 Replay from CLEAN incident (NOT base_state)
    replayed_state = replay_incident(
        base_incident,
        payload
    )

    save_incident_history(
        mode="replay",
        input_data=payload.model_dump(),
        decision=replayed_state.decisions.chosen_path,
        confidence=replayed_state.narrative.confidence_score,
        trace=replayed_state.trace
    )

    return {
        "base_decision": base_state.decisions.chosen_path,
        "replay_decision": replayed_state.decisions.chosen_path,
        "base_confidence": base_state.narrative.confidence_score,
        "replay_confidence": replayed_state.narrative.confidence_score,
        "replay_trace": replayed_state.trace,
        "replay_narrative": replayed_state.narrative.attacker_narrative,
    }
