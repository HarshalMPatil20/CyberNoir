import time
from typing import List, Dict

import requests

from app.core.logger import get_logger
from app.core.metrics import (
    LLM_REQUESTS_TOTAL,
    LLM_REQUEST_FAILURES,
    LLM_LATENCY_SECONDS
)
from app.core.llm_clients.base import LLMClient

logger = get_logger("LLM.Ollama")


class OllamaLLMClient(LLMClient):
    def __init__(self, model_name: str, temperature: float, url: str):
        logger.info("Initializing Ollama LLM client")

        self.provider = "ollama"
        self.model_name = model_name
        self.temperature = temperature
        self.url = url

    def generate(self, messages: List[Dict[str, str]]) -> str:
        LLM_REQUESTS_TOTAL.labels(
            provider=self.provider,
            model=self.model_name
        ).inc()

        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False,
            "options": {"temperature": self.temperature}
        }

        start = time.time()

        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()

            latency = time.time() - start

            LLM_LATENCY_SECONDS.labels(
                provider=self.provider,
                model=self.model_name
            ).observe(latency)

            logger.info(f"Ollama response in {latency:.2f}s")
            return response.json()["message"]["content"]

        except Exception as e:
            LLM_REQUEST_FAILURES.labels(
                provider=self.provider,
                model=self.model_name
            ).inc()

            logger.exception("Ollama request failed")
            raise RuntimeError(str(e))
