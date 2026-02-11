from app.db.session import SessionLocal
from app.db.models import IncidentHistory


def serialize_trace(trace):
    """
    Converts TraceEntry objects into JSON-serializable dicts.
    """
    serialized = []

    for entry in trace:
        # If already a dict, keep it
        if isinstance(entry, dict):
            serialized.append(entry)
        else:
            serialized.append({
                "agent": getattr(entry, "agent", "unknown"),
                "summary": getattr(entry, "summary", "")
            })

    return serialized


def save_incident_history(
    *,
    mode: str,
    input_data: dict,
    decision: str,
    confidence: float,
    trace: list
):
    db = SessionLocal()
    try:
        record = IncidentHistory(
            mode=mode,
            input_data=input_data,
            decision=decision,
            confidence=confidence,
            trace=serialize_trace(trace)  # ✅ FIX HERE
        )
        db.add(record)
        db.commit()
    finally:
        db.close()
