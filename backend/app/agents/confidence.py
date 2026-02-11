def confidence_calibration_agent(state):
    """
    Calibrates confidence based on signal clarity,
    uncertainty, and risk alignment.
    """

    confidence = 0.9  # optimistic starting point

    # -----------------------------
    # Penalize unknowns
    # -----------------------------
    unknown_count = len(state.evidence.unknown)
    confidence -= 0.05 * unknown_count

    # -----------------------------
    # Penalize low recon confidence
    # -----------------------------
    if state.attacker_view.confidence == "low":
        confidence -= 0.1

    # -----------------------------
    # Penalize high-risk ambiguity
    # -----------------------------
    if (
        state.risks.escalation_risk == "high"
        and state.decisions.chosen_path != "opportunistic_wait"
    ):
        confidence -= 0.15

    # -----------------------------
    # Penalize conflicting signals
    # (e.g. aggressive decision + high visibility)
    # -----------------------------
    if (
        state.attacker_view.visibility == "high"
        and state.decisions.chosen_path.startswith("attempt")
    ):
        confidence -= 0.1

    # -----------------------------
    # Small boost for clarity
    # -----------------------------
    if unknown_count == 0:
        confidence += 0.05

    # Clamp confidence
    confidence = max(0.3, min(confidence, 0.95))

    state.narrative.confidence_score = round(confidence, 2)

    # -----------------------------
    # Trace
    # -----------------------------
    state.trace.append({
        "agent": "ConfidenceAgent",
        "summary": f"Confidence calibrated to {state.narrative.confidence_score} based on evidence clarity and risk alignment."
    })

    return state
