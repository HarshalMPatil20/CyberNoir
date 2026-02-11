from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.api import incident

from app.db.session import init_db

init_db()

app = FastAPI(
    title="CyberNoir",
    description="Every attack has a motive.",
    version="0.1.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {
        "message": "CyberNoir API is running. Visit /docs for API documentation."
    }

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(incident.router)

from app.api.ingest import router as ingest_router

app.include_router(ingest_router)

from app.api.history import router as history_router

app.include_router(history_router)


