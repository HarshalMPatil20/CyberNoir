from abc import ABC, abstractmethod
from typing import Dict, Any


class SIEMAdapter(ABC):
    """
    Base interface for all SIEM adapters.
    Converts SIEM-specific data into CyberNoir facts.
    """

    @abstractmethod
    def convert(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
