from app.graph.state import CyberNoirState


def decision_simulation_agent(state: CyberNoirState) -> CyberNoirState:
    """
    Simulates attacker decision-making by selecting the
    most rational path given goals, risks, and evidence.

    Opportunistic attacker model:
    - Goals bias behavior
    - Risks gate execution
    - Weak defenses unlock aggression
    """

    goals = state.goals
    risks = state.risks
    evidence = state.evidence

    escalation_risk = risks.escalation_risk
    lateral_risk = risks.lateral_movement_risk
    goal = goals.primary_goal

    rejected_paths = []

    # -----------------------------
    # Decision Logic
    # -----------------------------

    # 🔥 Opportunistic rule:
    # Weak defenses + manageable escalation = try lateral movement
    if escalation_risk in ["low", "medium"] and lateral_risk in ["high", "medium"]:
        chosen_path = "attempt_lateral_movement"

    # Credential harvesting prefers persistence if escalation is risky
    elif goal == "credential_harvesting" and escalation_risk != "low":
        chosen_path = "maintain_access"

    else:
        chosen_path = "opportunistic_wait"

    # -----------------------------
    # Rejected Paths (Explainability)
    # -----------------------------

    if escalation_risk == "high":
        rejected_paths.append({
            "action": "attempt_privilege_escalation",
            "reason": "high_escalation_risk"
        })

    if lateral_risk == "very_high":
        rejected_paths.append({
            "action": "attempt_lateral_movement",
            "reason": "excessive_detection_risk"
        })

    if "data_exfiltration" in evidence.unknown:
        rejected_paths.append({
            "action": "attempt_data_exfiltration",
            "reason": "no_clear_value_and_high_noise"
        })

    # Deduplicate rejections
    unique_rejections = {
        (r["action"], r["reason"]): r for r in rejected_paths
    }

    state.decisions.chosen_path = chosen_path
    state.decisions.rejected_paths = list(unique_rejections.values())

    # -----------------------------
    # Trace (Brick 10)
    # -----------------------------
    state.trace.append({
        "agent": "DecisionAgent",
        "summary": (
            f"Chosen action path: {chosen_path} "
            f"(goal: {goal}, escalation risk: {escalation_risk}, "
            f"lateral risk: {lateral_risk})."
        )
    })

    return state
