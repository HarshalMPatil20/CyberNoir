from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class RawLog(BaseModel):
    source: str                # e.g. auth, firewall, edr
    message: str               # raw log message
    severity: Optional[str] = None
    metadata: Dict[str, Any] = {}


class RawIncidentInput(BaseModel):
    logs: List[RawLog]
    evidences: Optional[List[str]] = []
    audience_level: str = "technical"
