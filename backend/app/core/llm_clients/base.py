from typing import List, Dict


class LLMClient:
    """
    Abstract base class for all LLM clients.
    """

    def generate(self, messages: List[Dict[str, str]]) -> str:
        raise NotImplementedError
