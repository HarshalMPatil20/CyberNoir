from app.adapters.base import SIEMAdapter


class ElasticAdapter(SIEMAdapter):
    """
    Converts Elastic / Elasticsearch alerts into CyberNoir format.
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

        hits = raw_data.get("hits", {}).get("hits", [])

        for hit in hits:
            source = hit.get("_source", {})
            event_type = source.get("event", {}).get("action", "").lower()

            if event_type == "user_login":
                confirmed_actions.append("login_success")

            if source.get("authentication", {}).get("method") == "password":
                confirmed_actions.append("credential_use")
                initial_vector = "credential_access"

            if source.get("mfa", {}).get("enabled") is False:
                environment_context["mfa_enabled"] = False

        if "lateral_movement" not in confirmed_actions:
            non_actions.append("no_lateral_movement")

        return {
            "initial_vector": initial_vector,
            "confirmed_actions": confirmed_actions,
            "non_actions": non_actions,
            "environment_context": environment_context
        }
