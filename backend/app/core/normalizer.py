from app.ml.ml_classifier import classify_log_message


def normalize_logs_to_incident(raw_input):
    confirmed_actions = set()
    inferred_actions = []
    non_actions = set()

    environment_context = {
        "mfa_enabled": True,
        "endpoint_monitoring": True,
        "network_segmentation": True
    }

    initial_vector = "unknown"

    for log in raw_input.logs:
        msg = log.message.lower()
        rule_matched = False

        # ---- Rule-based extraction (HIGH confidence) ----
        if "login successful" in msg:
            confirmed_actions.add("login_success")
            rule_matched = True

        if "password authentication" in msg:
            confirmed_actions.add("credential_use")
            initial_vector = "credential_access"
            rule_matched = True

        if "mfa disabled" in msg:
            environment_context["mfa_enabled"] = False
            rule_matched = True

        # ---- ML-assisted extraction (ONLY if rules fail) ----
        if not rule_matched:
            ml_result = classify_log_message(log.message)

            if ml_result:
                action, confidence = ml_result

                inferred_actions.append({
                    "action": action,
                    "confidence": confidence,
                    "source": "ml"
                })

    # ---- Infer non-actions ----
    if "lateral_movement" not in confirmed_actions:
        non_actions.add("no_lateral_movement")

    return {
        "initial_vector": initial_vector,
        "confirmed_actions": list(confirmed_actions),
        "inferred_actions": inferred_actions,
        "non_actions": list(non_actions),
        "environment_context": environment_context,
        "audience_level": raw_input.audience_level
    }
