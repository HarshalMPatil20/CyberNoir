from sqlalchemy import Column, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class IncidentHistory(Base):
    __tablename__ = "incident_history"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=datetime.utcnow)

    mode = Column(String)  # analyze | replay | ingest

    input_data = Column(JSON)
    decision = Column(String)
    confidence = Column(Float)
    trace = Column(JSON)
