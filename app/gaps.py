"""Question log in SQLite. Questions without a good answer (or with a thumbs-down) become the 'missing docs' list."""
import sqlite3
from datetime import datetime, timezone

import numpy as np

from . import config
from .store import embed

SCHEMA = """
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    question TEXT NOT NULL,
    top_score REAL NOT NULL,
    top_source TEXT,
    answered INTEGER NOT NULL,
    gap_reason TEXT,          -- low_similarity | llm_not_answered | thumbs_down | out_of_scope | NULL
    missing_topic TEXT,
    feedback TEXT             -- up | down | NULL
)"""

# Unanswered questions that don't belong in a wiki (social, chit-chat, general knowledge). Logged, but not a doc gap.
OUT_OF_SCOPE = "out_of_scope"
IS_GAP = f"gap_reason IS NOT NULL AND gap_reason != '{OUT_OF_SCOPE}'"


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(config.GAPS_DB)
    conn.row_factory = sqlite3.Row
    conn.execute(SCHEMA)
    return conn


def log_question(question: str, top_score: float, top_source: str | None, answered: bool,
                 gap_reason: str | None, missing_topic: str) -> int:
    with _conn() as conn:
        cur = conn.execute(
            "INSERT INTO questions (ts, question, top_score, top_source, answered, gap_reason, missing_topic)"
            " VALUES (?, ?, ?, ?, ?, ?, ?)",
            (datetime.now(timezone.utc).isoformat(timespec="seconds"), question, top_score, top_source,
             int(answered), gap_reason, missing_topic or None),
        )
        return cur.lastrowid


def record_feedback(question_id: int, feedback: str) -> None:
    with _conn() as conn:
        conn.execute(
            "UPDATE questions SET feedback = ?,"
            " gap_reason = CASE WHEN ? = 'down' THEN COALESCE(gap_reason, 'thumbs_down') ELSE gap_reason END"
            " WHERE id = ?",
            (feedback, feedback, question_id),
        )


def stats() -> dict:
    with _conn() as conn:
        row = conn.execute(
            f"SELECT COUNT(*) total, SUM({IS_GAP}) gaps FROM questions WHERE gap_reason IS NOT '{OUT_OF_SCOPE}'"
        ).fetchone()
    total, gaps = row["total"] or 0, row["gaps"] or 0
    return {"total": total, "gaps": gaps, "answered_rate": round(1 - gaps / total, 2) if total else None}


def gap_report() -> list[dict]:
    """Group similar unanswered questions so 5 people asking the same thing show up as one topic with count 5."""
    with _conn() as conn:
        rows = [dict(r) for r in conn.execute(
            f"SELECT * FROM questions WHERE {IS_GAP} ORDER BY ts DESC")]
    if not rows:
        return []

    vecs = embed([r["question"] for r in rows])
    clusters: list[dict] = []
    for i, (row, vec) in enumerate(zip(rows, vecs)):
        best = max(clusters, key=lambda c: float(c["centroid"] @ vec), default=None)
        if best is not None and float(best["centroid"] @ vec) >= config.GAP_CLUSTER_SCORE:
            best["items"].append(row)
            best["idx"].append(i)
            centroid = vecs[best["idx"]].mean(axis=0)
            best["centroid"] = centroid / np.linalg.norm(centroid)
        else:
            clusters.append({"items": [row], "idx": [i], "centroid": vec})

    report = []
    for c in clusters:
        items = c["items"]
        topics = [i["missing_topic"] for i in items if i["missing_topic"]]
        report.append({
            "topic": topics[0] if topics else items[-1]["question"],
            "count": len(items),
            "last_asked": items[0]["ts"],
            "reasons": sorted({i["gap_reason"] for i in items}),
            "closest_existing_source": max(items, key=lambda i: i["top_score"])["top_source"],
            "questions": [i["question"] for i in items],
        })
    return sorted(report, key=lambda r: (r["count"], r["last_asked"]), reverse=True)
