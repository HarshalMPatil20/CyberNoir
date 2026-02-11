from app.graph.state import CyberNoirState, IncidentInput
from app.graph.cybernoir_graph import run_cybernoir


def sanitize_environment_context(env: dict) -> dict:
    if not isinstance(env, dict):
        return {}
    return {k: v for k, v in env.items() if isinstance(v, bool)}


def replay_incident(base_incident: IncidentInput, replay_request):

    incident_data = base_incident.model_dump()

    # -----------------------------
    # Sanitize environment context
    # -----------------------------
    incident_data["environment_context"] = sanitize_environment_context(
        incident_data.get("environment_context", {})
    )

    # -----------------------------
    # Apply overrides (SAFE)
    # -----------------------------
    if replay_request.override_environment:
        incident_data["environment_context"].update(
            sanitize_environment_context(
                replay_request.override_environment
            )
        )

    if replay_request.override_confirmed_actions is not None:
        incident_data["confirmed_actions"] = (
            replay_request.override_confirmed_actions
        )

    if replay_request.override_non_actions is not None:
        incident_data["non_actions"] = (
            replay_request.override_non_actions
        )

    # -----------------------------
    # Build fresh state
    # -----------------------------
    replay_state = CyberNoirState(
        incident=IncidentInput(**incident_data)
    )

    return run_cybernoir(replay_state)
