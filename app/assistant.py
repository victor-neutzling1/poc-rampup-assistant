"""retrieve -> answer -> log gap. Shared by the web server and the CLI."""
import logging
from functools import lru_cache

import openai

from . import config, gaps
from .llm import answer_offline, answer_with_deepseek
from .store import VectorStore

log = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def store() -> VectorStore:
    return VectorStore.load()


def ask(question: str) -> dict:
    hits = store().search(question)
    top_chunk, top_score = hits[0]
    good_match = top_score >= config.MIN_SCORE

    mode = "deepseek" if config.llm_enabled() else "offline"
    if mode == "deepseek":
        try:
            result = answer_with_deepseek(question, hits)
        except openai.AuthenticationError:
            log.error("Invalid DEEPSEEK_API_KEY - falling back to offline mode")
            mode = "offline"
        except (openai.RateLimitError, openai.APIStatusError, openai.APIConnectionError) as e:
            log.error("DeepSeek call failed (%s) - falling back to offline mode", e)
            mode = "offline"
    if mode == "offline":
        result = answer_offline(hits, good_match)

    gap_reason = None
    if not result.answered:
        if not result.in_scope:
            gap_reason = gaps.OUT_OF_SCOPE  # logged, but kept out of the missing-docs list
        else:
            gap_reason = "low_similarity" if mode == "offline" else "llm_not_answered"

    qid = gaps.log_question(question, top_score, top_chunk.title, result.answered, gap_reason, result.missing_topic)

    cited = set(result.cited_sources)
    return {
        "id": qid,
        "mode": mode,
        "answer": result.answer,
        "answered": result.answered,
        "gap": gap_reason not in (None, gaps.OUT_OF_SCOPE),
        "missing_topic": result.missing_topic,
        "sources": [
            {"ref": f"S{i}", "title": c.title, "type": c.source_type, "location": c.location,
             "score": round(s, 3), "cited": f"S{i}" in cited, "text": c.text}
            for i, (c, s) in enumerate(hits, 1)
        ],
    }
