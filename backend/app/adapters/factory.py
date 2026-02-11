from app.adapters.splunk_adapter import SplunkAdapter
from app.adapters.elastic_adapter import ElasticAdapter


def get_siem_adapter(siem_type: str):
    if siem_type == "splunk":
        return SplunkAdapter()
    elif siem_type == "elastic":
        return ElasticAdapter()
    else:
        raise ValueError("Unsupported SIEM type")
