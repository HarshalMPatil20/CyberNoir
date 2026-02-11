from fastapi import APIRouter
from app.db.session import SessionLocal
from app.db.models import IncidentHistory

router = APIRouter(prefix="/history", tags=["History"])


@router.get("/")
def list_incidents(limit: int = 20):
    db = SessionLocal()
    try:
        records = (
            db.query(IncidentHistory)
            .order_by(IncidentHistory.timestamp.desc())
            .limit(limit)
            .all()
        )
        return records
    finally:
        db.close()
