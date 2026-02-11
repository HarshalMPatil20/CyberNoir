from fastapi import APIRouter
from app.schemas.raw_input import RawIncidentInput
from app.core.normalizer import normalize_logs_to_incident
from app.graph.cybernoir_graph import run_cybernoir
from app.graph.state import IncidentInput, CyberNoirState
from app.adapters.factory import get_siem_adapter
from app.core.history import save_incident_history

router = APIRouter(prefix="/ingest", tags=["Ingestion"])


@router.post("/logs")
def ingest_raw_logs(payload: RawIncidentInput):
    """
    Accepts raw logs and evidences, converts them into
    CyberNoir analyze format, and runs analysis.
    """

    normalized_incident = normalize_logs_to_incident(payload)

    incident = IncidentInput(**normalized_incident)
    state = CyberNoirState(incident=incident)

    final_state = run_cybernoir(state)

    save_incident_history(
        mode="ingest",
        input_data=normalized_incident,
        decision=final_state.decisions.chosen_path,
        confidence=final_state.narrative.confidence_score,
        trace=final_state.trace
    )

    return {
        "normalized_incident": normalized_incident,
        "analysis": {
            "decision": final_state.decisions.chosen_path,
            "confidence": final_state.narrative.confidence_score,
            "narrative": final_state.narrative.attacker_narrative,
            "trace": final_state.trace
        }
    }

@router.post("/siem/{siem_type}")
def ingest_siem_data(siem_type: str, payload: dict):
    adapter = get_siem_adapter(siem_type)

    normalized = adapter.convert(payload)
    normalized["audience_level"] = "technical"

    incident = IncidentInput(**normalized)
    state = CyberNoirState(incident=incident)

    final_state = run_cybernoir(state)

    save_incident_history(
        mode=f"siem:{siem_type}",
        input_data=normalized,
        decision=final_state.decisions.chosen_path,
        confidence=final_state.narrative.confidence_score,
        trace=final_state.trace
    )

    return {
        "normalized_incident": normalized,
        "decision": final_state.decisions.chosen_path,
        "confidence": final_state.narrative.confidence_score,
        "trace": final_state.trace
    }