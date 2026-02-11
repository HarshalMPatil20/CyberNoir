from app.graph.state import CyberNoirState


def risk_evaluation_agent(state):
    env = state.incident.environment_context or {}

    mfa_enabled = env.get("mfa_enabled", True)
    endpoint_monitoring = env.get("endpoint_monitoring", True)
    network_segmentation = env.get("network_segmentation", True)

    visibility = state.attacker_view.visibility

    # -----------------------------
    # Base escalation risk
    # -----------------------------
    if not mfa_enabled and not endpoint_monitoring:
        escalation_risk = "low"
    elif not mfa_enabled or not endpoint_monitoring:
        escalation_risk = "medium"
    else:
        escalation_risk = "high"

    # Visibility bumps risk by ONE level (not to max)
    if visibility == "high":
        if escalation_risk == "low":
            escalation_risk = "medium"
        elif escalation_risk == "medium":
            escalation_risk = "high"

    state.risks.escalation_risk = escalation_risk

    # -----------------------------
    # Base lateral movement risk
    # -----------------------------
    if not network_segmentation:
        lateral_risk = "medium"
    else:
        lateral_risk = "very_high"

    if visibility == "high" and lateral_risk == "medium":
        lateral_risk = "high"

    state.risks.lateral_movement_risk = lateral_risk

    # -----------------------------
    # Trace
    # -----------------------------
    summary_parts = []

    if not mfa_enabled:
        summary_parts.append("MFA disabled")
    if not endpoint_monitoring:
        summary_parts.append("weak endpoint monitoring")
    if not network_segmentation:
        summary_parts.append("no network segmentation")
    if visibility == "high":
        summary_parts.append("high attacker visibility")

    env_summary = ", ".join(summary_parts)

    state.trace.append({
        "agent": "RiskAgent",
        "summary": (
            f"Escalation risk assessed as {escalation_risk} and "
            f"lateral movement risk as {lateral_risk} due to {env_summary}."
        )
    })

    return state
