from prometheus_client import Counter, Histogram

# -----------------------------
# LLM Metrics
# -----------------------------

LLM_REQUESTS_TOTAL = Counter(
    "llm_requests_total",
    "Total number of LLM requests",
    ["provider", "model"]
)

LLM_REQUEST_FAILURES = Counter(
    "llm_request_failures_total",
    "Total number of failed LLM requests",
    ["provider", "model"]
)

LLM_LATENCY_SECONDS = Histogram(
    "llm_latency_seconds",
    "Latency of LLM requests in seconds",
    ["provider", "model"],
    buckets=(0.1, 0.3, 0.5, 1, 1.5, 2, 3, 5, 10)
)

