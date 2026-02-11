"""
ML-assisted log classification.
This module is OPTIONAL and only used when rule-based
normalization fails to extract signals.
"""

from typing import Optional, Tuple


def classify_log_message(message: str) -> Optional[Tuple[str, float]]:
    """
    Attempts to infer an action from a log message.
    Returns (action, confidence) or None.
    """

    msg = message.lower()

    # ---- Simulated ML behavior (placeholder) ----
    # Replace with real model later
    if "unusual location" in msg or "new ip" in msg:
        return "credential_use", 0.82

    if "multiple failed logins" in msg:
        return "brute_force_attempt", 0.78

    return None
