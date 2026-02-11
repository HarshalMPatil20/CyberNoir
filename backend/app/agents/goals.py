from app.graph.state import CyberNoirState


def goal_inference_agent(state: CyberNoirState) -> CyberNoirState:
    """
    Infers attacker goals based on confirmed behavior,
    avoided actions, and attacker confidence.
    """

    evidence = state.evidence
    attacker_view = state.attacker_view
    initial_vector = state.incident.initial_vector

    primary_goal = None
    excluded_goals = []

    # ---- Goal inference logic ----

    # Case 1: Phishing + credentials, no escalation
    if (
        initial_vector == "phishing"
        and "credential_use" in evidence.confirmed
        and "privilege_escalation" in evidence.unknown
        and attacker_view.confidence in ["low", "medium"]
    ):
        primary_goal = "credential_harvesting"
        excluded_goals.extend([
            "ransomware",
            "full_system_compromise",
            "data_exfiltration"
        ])

    # Case 2: Login success but no lateral movement
    if (
        "login_success" in evidence.confirmed
        and "lateral_movement" in evidence.unknown
    ):
        excluded_goals.append("network_wide_compromise")

    # Case 3: Explicit absence of data exfiltration
    if "no_data_exfiltration" in evidence.absent:
        excluded_goals.append("data_theft")

    # Fallback if nothing strongly inferred
    if primary_goal is None:
        primary_goal = "opportunistic_access"
        excluded_goals.append("high_risk_operations")

    # Deduplicate excluded goals
    excluded_goals = list(set(excluded_goals))

    # Write to state
    state.goals.primary_goal = primary_goal
    state.goals.excluded_goals = excluded_goals
    state.trace.append({
        "agent": "GoalAgent",
        "summary": f"Inferred primary attacker goal: {state.goals.primary_goal}."
    })

    return state
