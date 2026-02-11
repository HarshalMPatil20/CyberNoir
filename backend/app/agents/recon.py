from app.graph.state import CyberNoirState


def recon_reasoning_agent(state: CyberNoirState) -> CyberNoirState:
    """
    Determines what the attacker could realistically see
    and how confident they might feel based on evidence
    and environmental controls.
    """

    evidence = state.evidence
    env = state.incident.environment_context

    # ---- Visibility reasoning ----
    # Start conservative
    visibility_score = 0

    # Successful credential use increases visibility
    if "credential_use" in evidence.confirmed:
        visibility_score += 1

    if "login_success" in evidence.confirmed:
        visibility_score += 1

    # Strong segmentation reduces visibility
    if env.get("network_segmentation"):
        visibility_score -= 1

    # Clamp visibility
    if visibility_score <= 0:
        visibility = "low"
    elif visibility_score == 1:
        visibility = "medium"
    else:
        visibility = "high"

    # ---- Confidence reasoning ----
    confidence_score = 0

    # No detection = more confidence
    if env.get("endpoint_monitoring") and len(evidence.confirmed) <= 2:
        confidence_score += 1

    # MFA lowers confidence
    if env.get("mfa_enabled"):
        confidence_score -= 1

    # Explicit absence of alerts increases confidence
    if "no_privilege_escalation" in evidence.absent:
        confidence_score += 1

    # Clamp confidence
    if confidence_score <= 0:
        confidence = "low"
    elif confidence_score == 1:
        confidence = "medium"
    else:
        confidence = "high"

    # Write to state
    state.attacker_view.visibility = visibility
    state.attacker_view.confidence = confidence
    state.trace.append({
        "agent": "ReconAgent",
        "summary": (
            f"Attacker visibility assessed as {state.attacker_view.visibility} "
            f"with confidence {state.attacker_view.confidence}."
        )
    })

    return state
