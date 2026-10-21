"""Web UI + JSON API.

Usage: python -m app.server   (then open http://localhost:8000)
"""
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from . import assistant, config, gaps

app = FastAPI(title="New Hire Ramp-Up Assistant")
STATIC = Path(__file__).parent / "static"


class AskRequest(BaseModel):
    question: str


class FeedbackRequest(BaseModel):
    id: int
    feedback: str  # "up" | "down"


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/api/status")
def status():
    return {"llm": config.llm_enabled(), "model": config.DEEPSEEK_MODEL, "chunks": len(assistant.store().chunks)}


@app.post("/api/ask")
def ask(req: AskRequest):
    if not req.question.strip():
        raise HTTPException(400, "Empty question")
    return assistant.ask(req.question.strip())


@app.post("/api/feedback")
def feedback(req: FeedbackRequest):
    if req.feedback not in {"up", "down"}:
        raise HTTPException(400, "feedback must be 'up' or 'down'")
    gaps.record_feedback(req.id, req.feedback)
    return {"ok": True}


@app.get("/api/gaps")
def gap_list():
    return {"stats": gaps.stats(), "gaps": gaps.gap_report()}


if __name__ == "__main__":
    import logging
    import uvicorn
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    if not config.llm_enabled():
        logging.warning("DEEPSEEK_API_KEY not set - running in offline mode (excerpts only, no LLM answers)")
    else:
        logging.info("Answering with DeepSeek (%s)", config.DEEPSEEK_MODEL)
    assistant.store()  # fail fast if the index is missing, and warm up the embedding model
    uvicorn.run(app, host="127.0.0.1", port=8000)
