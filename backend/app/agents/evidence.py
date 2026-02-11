from app.graph.state import CyberNoirState


def evidence_context_agent(state: CyberNoirState) -> CyberNoirState:
    """
    Aggregates confirmed, inferred, and unknown attacker actions.

    Rules:
    - Confirmed actions are trusted ground truth
    - ML-inferred actions are accepted only if confidence is high
    - Low-confidence inferences increase uncertainty
    """

    confirmed = []
    unknown = []

    # -----------------------------
    # Confirmed actions (hard facts)
    # -----------------------------
    for action in state.incident.confirmed_actions:
        confirmed.append(action)

    # -----------------------------
    # ML-assisted inferred actions
    # -----------------------------
    for inferred in getattr(state.incident, "inferred_actions", []) or []:
        action = inferred.action
        confidence = inferred.confidence

        if confidence >= 0.8:
            confirmed.append(action)
            state.trace.append({
                "agent": "EvidenceAgent",
                "summary": (
                    f"Accepted ML-inferred action '{action}' "
                    f"with confidence {confidence}."
                )
            })
        else:
            unknown.append(action)
            state.trace.append({
                "agent": "EvidenceAgent",
                "summary": (
                    f"Marked ML-inferred action '{action}' as uncertain "
                    f"(confidence {confidence})."
                )
            })

    # -----------------------------
    # Explicit non-actions
    # -----------------------------
    for non_action in state.incident.non_actions:
        unknown.append(non_action)

    # -----------------------------
    # Update state
    # -----------------------------
    state.evidence.confirmed = list(set(confirmed))
    state.evidence.unknown = list(set(unknown))

    # -----------------------------
    # Final trace summary
    # -----------------------------
    state.trace.append({
        "agent": "EvidenceAgent",
        "summary": (
            f"Confirmed actions: {state.evidence.confirmed}. "
            f"Uncertain/absent actions: {state.evidence.unknown}."
        )
    })

    return state
