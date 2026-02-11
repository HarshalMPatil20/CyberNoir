import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from typing import List, Dict

import google.generativeai as genai

from app.core.logger import get_logger
from app.core.metrics import (
    LLM_REQUESTS_TOTAL,
    LLM_REQUEST_FAILURES,
    LLM_LATENCY_SECONDS
)
from app.core.llm_clients.base import LLMClient

logger = get_logger("LLM.Gemini")


class GeminiLLMClient(LLMClient):
    def __init__(self, model_name: str, api_key: str, temperature: float):
        if not api_key:
            raise ValueError("LLM_API_KEY must be set for Gemini")

        logger.info("Initializing Gemini LLM client")
        logger.info(f"Model: {model_name}")

        genai.configure(api_key=api_key)

        self.provider = "gemini"
        self.model_name = model_name
        self.temperature = temperature

        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config={"temperature": temperature}
        )

    def generate(self, messages: List[Dict[str, str]]) -> str:
        LLM_REQUESTS_TOTAL.labels(
            provider=self.provider,
            model=self.model_name
        ).inc()

        prompt = "\n\n".join(
            f"{m['role'].upper()}: {m['content']}"
            for m in messages
        )

        logger.info("Sending request to Gemini")
        start = time.time()

        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(
                    self.model.generate_content,
                    prompt
                )
                response = future.result(timeout=10)

            latency = time.time() - start

            LLM_LATENCY_SECONDS.labels(
                provider=self.provider,
                model=self.model_name
            ).observe(latency)

            logger.info(f"Gemini response in {latency:.2f}s")
            return response.text

        except TimeoutError:
            LLM_REQUEST_FAILURES.labels(
                provider=self.provider,
                model=self.model_name
            ).inc()

            logger.error("Gemini request timed out")
            raise RuntimeError("Gemini LLM request timed out")

        except Exception as e:
            LLM_REQUEST_FAILURES.labels(
                provider=self.provider,
                model=self.model_name
            ).inc()

            logger.exception("Gemini request failed")
            raise RuntimeError(str(e))
