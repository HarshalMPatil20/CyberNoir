from app.adapters.base import SIEMAdapter


class SplunkAdapter(SIEMAdapter):
    """
    Converts Splunk search results into CyberNoir format.
    """

    def convert(self, raw_data):
        confirmed_actions = []
        non_actions = []
        environment_context = {
            "mfa_enabled": True,
            "endpoint_monitoring": True,
            "network_segmentation": True
        }

        initial_vector = "unknown"

        events = raw_data.get("events", [])

        for event in events:
            message = event.get("message", "").lower()

            if "login successful" in message:
                confirmed_actions.append("login_success")

            if "password authentication" in message:
                confirmed_actions.append("credential_use")
                initial_vector = "credential_access"

            if "mfa disabled" in message:
                environment_context["mfa_enabled"] = False

        if "lateral_movement" not in confirmed_actions:
            non_actions.append("no_lateral_movement")

        return {
            "initial_vector": initial_vector,
            "confirmed_actions": confirmed_actions,
            "non_actions": non_actions,
            "environment_context": environment_context
        }
