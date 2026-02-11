DEFENSIVE_ACTION_MAP = {
    "maintain_access": "Force password reset, rotate credentials, and enable MFA.",
    "attempt_privilege_escalation": "Audit privileged accounts and review recent permission changes.",
    "attempt_lateral_movement": "Isolate affected host and monitor east-west traffic.",
    "attempt_data_exfiltration": "Inspect outbound traffic and enforce DLP policies.",
    "opportunistic_wait": "Increase monitoring and review authentication logs."
}


def get_recommended_action(decision: str) -> str:
    return DEFENSIVE_ACTION_MAP.get(
        decision,
        "Review logs manually and escalate for analyst investigation."
    )