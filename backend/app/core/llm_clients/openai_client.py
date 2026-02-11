import time
from typing import List, Dict

from openai import OpenAI

from app.core.logger import get_logger
from app.core.metrics import (
    LLM_REQUESTS_TOTAL,
    LLM_REQUEST_FAILURES,
    LLM_LATENCY_SECONDS
)
from app.core.llm_clients.base import LLMClient

logger = get_logger("LLM.OpenAI")


class OpenAILLMClient(LLMClient):
    def __init__(self, model_name: str, api_key: str, temperature: float):
        if not api_key:
            raise ValueError("LLM_API_KEY must be set for OpenAI")

        logger.info("Initializing OpenAI LLM client")

        self.provider = "openai"
        self.model_name = model_name
        self.temperature = temperature
        self.client = OpenAI(api_key=api_key)

    def generate(self, messages: List[Dict[str, str]]) -> str:
        LLM_REQUESTS_TOTAL.labels(
            provider=self.provider,
            model=self.model_name
        ).inc()

        start = time.time()

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature
            )

            latency = time.time() - start

            LLM_LATENCY_SECONDS.labels(
                provider=self.provider,
                model=self.model_name
            ).observe(latency)

            logger.info(f"OpenAI response in {latency:.2f}s")
            return response.choices[0].message.content

        except Exception as e:
            LLM_REQUEST_FAILURES.labels(
                provider=self.provider,
                model=self.model_name
            ).inc()

            logger.exception("OpenAI request failed")
            raise RuntimeError(str(e))
