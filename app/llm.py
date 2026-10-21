"""Answer a question from retrieved excerpts with DeepSeek, always citing sources."""
import json
import re
from functools import lru_cache

import openai
from pydantic import BaseModel, ValidationError

from . import config
from .store import Chunk

SYSTEM = """You are the New Hire Ramp-Up Assistant, a friendly colleague who helps engineers who just joined the company.
You answer ONLY from the internal docs and resolved Jira tickets given to you in <source> tags. Each source has an id
(S1, S2, ...) and may list contacts: the people who own that doc or resolved that ticket.

How to write the answer:
- Write naturally, like a helpful teammate. Refer to "the docs", the doc's name or the ticket ID. Never mention
  "sources", "excerpts" or "the information provided", and never talk about how you work.
- Cite every claim with its source id in brackets right after it, e.g. "Autopilot lives in orders-service [S1]."
  Cite each source separately: [S1][S3], not [S1, S3]. Never invent sources.
- Never use general knowledge about how companies usually do things to fill gaps - a wrong internal answer is worse
  than none.
- Be concise and practical: steps, commands, who to contact. Use short paragraphs or bullet lists.
- Reply in the same language as the question.

When the docs don't fully answer the question:
- Share what the docs do say, cited as usual.
- Do NOT list, describe or summarize what the docs don't cover (no "the docs don't explain X, Y or Z", no "neither
  explains..."). Instead end with a short closing like: "I couldn't find a complete answer in the docs, so for the
  full picture I'd ask Jonas Weber (Tech Lead, Orders) or Lucía Fernández (Product Manager, Orders)."
- Pick those people from the contacts or names in the sources most related to the question. Only suggest people who
  appear in the sources; if none fit, suggest asking in #eng-help.
- Set answered=false and missing_topic to a short title for the documentation page that should exist (e.g. "Autopilot
  project overview"). These are only used internally, never mention them in the answer.
- If the docs say nothing relevant at all, say so in one sentence and suggest who to ask, the same way.

Questions that don't belong in a company wiki:
- Set in_scope=false for social or personal questions (where people go for drinks, favourite lunch spots, who is fun to
  work with), opinions, chit-chat, jokes, general knowledge, or generic programming questions not specific to this
  company. Answer briefly and kindly that it's outside what you can help with, and leave missing_topic empty.
- Anything about the company's setup, tools, access, codebase, processes, people or policies (including HR and admin
  topics like expenses or time off) is in scope.

Respond with a single JSON object and nothing else, in exactly this shape:
{"answer": "<markdown answer with [S#] citations>", "cited_sources": ["S1"], "answered": true, "in_scope": true, "missing_topic": ""}"""


class Answer(BaseModel):
    answer: str            # Markdown answer with [S#] citations
    cited_sources: list[str]
    answered: bool         # True only if the sources fully answer the question
    missing_topic: str     # Title of the missing doc when answered is false, else empty
    in_scope: bool = True  # False for questions that don't belong in a wiki (social, chit-chat, general knowledge)


@lru_cache(maxsize=1)
def client() -> openai.OpenAI:
    # DeepSeek's API is OpenAI-compatible, so we use the OpenAI SDK pointed at DeepSeek.
    return openai.OpenAI(api_key=config.DEEPSEEK_API_KEY, base_url=config.DEEPSEEK_BASE_URL)


def format_sources(hits: list[tuple[Chunk, float]]) -> str:
    return "\n\n".join(
        f'<source id="S{i}" type="{c.source_type}" title="{c.title}"'
        + (f' contacts="{c.contacts}"' if c.contacts else "")
        + f">\n{c.text}\n</source>"
        for i, (c, _) in enumerate(hits, 1)
    )


def answer_with_deepseek(question: str, hits: list[tuple[Chunk, float]]) -> Answer:
    response = client().chat.completions.create(
        model=config.DEEPSEEK_MODEL,
        max_tokens=4000,
        response_format={"type": "json_object"},  # JSON mode has no schema parameter; the shape is in SYSTEM
        # Thinking mode is on by default; for answering from given excerpts it only adds latency.
        extra_body={"thinking": {"type": "disabled"}},
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"<sources>\n{format_sources(hits)}\n</sources>\n\nQuestion: {question}"},
        ],
    )
    content = (response.choices[0].message.content or "").strip()
    try:
        return Answer.model_validate(json.loads(content))
    except (json.JSONDecodeError, ValidationError):
        # If the model ignored the format, still show what it wrote, but don't count it as answered.
        return Answer(answer=content or "I couldn't produce an answer for this question.",
                      cited_sources=re.findall(r"S\d+", content), answered=False, missing_topic="")


def answer_offline(hits: list[tuple[Chunk, float]], good_match: bool) -> Answer:
    """No LLM available: just surface the best excerpts so the retrieval + citation + gap flow still works."""
    if not good_match:
        return Answer(answer="I couldn't find anything in the docs or tickets that covers this.",
                      cited_sources=[], answered=False, missing_topic="")
    top = [(i, c) for i, (c, s) in enumerate(hits, 1) if s >= config.MIN_SCORE][:3]
    body = "\n\n".join(f"**{c.title}** [S{i}]\n\n{c.text}" for i, c in top)
    return Answer(answer=f"_No LLM configured - showing the most relevant excerpts:_\n\n{body}",
                  cited_sources=[f"S{i}" for i, _ in top], answered=True, missing_topic="")
