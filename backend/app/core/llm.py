import os

from app.core.llm_clients.base import LLMClient
from app.core.llm_clients.openai_client import OpenAILLMClient
from app.core.llm_clients.gemini_client import GeminiLLMClient
from app.core.llm_clients.ollama_client import OllamaLLMClient

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "").lower()
LLM_MODEL = os.getenv("LLM_MODEL")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))
OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/chat"
)


def get_llm_client() -> LLMClient:
    if not LLM_PROVIDER:
        raise ValueError("LLM_PROVIDER environment variable is not set")

    if LLM_PROVIDER == "gemini":
        return GeminiLLMClient(
            model_name=LLM_MODEL,
            api_key=LLM_API_KEY,
            temperature=LLM_TEMPERATURE
        )

    if LLM_PROVIDER == "openai":
        return OpenAILLMClient(
            model_name=LLM_MODEL,
            api_key=LLM_API_KEY,
            temperature=LLM_TEMPERATURE
        )

    if LLM_PROVIDER == "ollama":
        return OllamaLLMClient(
            model_name=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            url=OLLAMA_URL
        )

    raise ValueError(f"Unsupported LLM_PROVIDER: {LLM_PROVIDER}")
