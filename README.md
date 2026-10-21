# New Hire Ramp-Up Assistant (PoC)

Innovation Day PoC (Transform Mitel). An internal bot answers technical questions from new hires. It pulls from existing docs and resolved tickets and **always cites the source**. As a bonus, it tracks the questions it couldn't answer and turns them into a **"missing docs" list**.

The demo runs on **fictional data**: docs and Jira cards for "Larderly", a made-up company that builds stock and ordering software for restaurants. No real company content is included.

```
docs (.md/.txt) ─┐                         question
                 ├─ chunk ─ embed ─► index ◄── embed ── top-8 excerpts ──► LLM ──► answer + [S#] citations
tickets (.json) ─┘   (local, multilingual)                                  │
                                                              answered=false / 👎
                                                                            ▼
                                                   gaps.db ──► "Missing docs" (similar questions grouped)
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\python -m app.ingest          # builds index/ (first run downloads a ~220 MB embedding model)
copy .env.example .env                        # then put your DeepSeek key in .env
.\.venv\Scripts\python -m app.server          # http://localhost:8000
```

`.env` is git-ignored. Settings can also be set as environment variables, which take precedence over `.env`.

Terminal only: `python -m app.cli "which Node version do I need?"` and `python -m app.cli --gaps`.

## The LLM

Answers are written by DeepSeek (`deepseek-flash`, thinking mode turned off for speed) through its OpenAI-compatible API. DeepSeek is prepaid: if the account has no balance, requests fail with HTTP 402. Use `DEEPSEEK_MODEL` to change the model.

Without a key, or if a DeepSeek call fails, the app runs in **offline mode**: it shows the best excerpts with their sources and decides gaps by similarity only.

## How it works

| Step | Where | Notes |
|---|---|---|
| Ingest | `app/ingest.py` | One chunk per `##`/`###` section of each doc (≤500 chars); one chunk per **resolved** ticket (problem + resolution). Open tickets are skipped. |
| Embedding | `app/store.py` | `paraphrase-multilingual-MiniLM-L12-v2` via fastembed (ONNX, runs locally on CPU). Questions in PT match docs in EN. |
| Vector store | `app/store.py` | numpy matrix + JSON, brute-force cosine. Plenty for thousands of chunks. |
| Answer | `app/llm.py` | DeepSeek returns `{answer, cited_sources, answered, missing_topic}` as JSON; the prompt forbids answering from general knowledge. |
| Gaps | `app/gaps.py` | Every question is logged in SQLite. A gap is when the LLM says it wasn't answered, the similarity is low (offline), or someone gives a 👎. Questions that don't belong in a wiki (social, chit-chat, general knowledge) are judged out of scope by the LLM and kept out of the list. Similar questions are grouped into one topic with a count. |

Other settings (`app/config.py`): `RAMPUP_TOP_K` (8), `RAMPUP_MIN_SCORE` (0.35), `RAMPUP_GAP_CLUSTER_SCORE` (0.7), `RAMPUP_DATA_DIR`.

## Demo script

1. "Which Node version do I need for Counter?" → Node 20, citing ticket WEB-731, and it points out that the setup page still says Node 18: a **stale doc** found automatically.
2. "Meu git clone dá 'Repository not found', o que eu faço?" → answers in Portuguese from an English ticket (IT-1042).
3. "What is Autopilot and why doesn't it work locally?" → combines the glossary, architecture doc and ticket ORD-288.
4. "How do I get kubectl access to staging?" / "How do I get access to the production database?" → no answer; logged as missing docs.
5. Open the **Missing docs** tab → topics ranked by how many people asked, PT and EN grouped together.

## The fictional data

- `data/docs/`: 16 Markdown docs. Each starts with a `#` title, has an `Owner: <name> (<role>) · Also ask: <name> (<role>)` line, and uses `##`/`###` sections. The owners are attached to every chunk of the doc, so when the bot can't fully answer, it suggests who to ask.
  - `general/`: welcome, glossary, team rituals, teams and people (fictional names)
  - `environment/`: dev setup, local stack
  - `codebase/`: repository map and tech stack, backend conventions, frontend conventions
  - `workflow/`: git and code review, branching strategy, life of a ticket, Scrum and ceremonies, CI/CD and releases
  - `architecture/`: system overview, observability and on-call
- `data/tickets/jira-cards.json`: 15 resolved Jira cards and 2 open ones, each with `id`, `title`, `status`, `assignee`, `description`, `resolution`.
- Left out on purpose, so the missing-docs list has something to show: staging kubectl access, production database access, mobile app store releases, expenses and travel.

To use other content, replace the files and run `python -m app.ingest` again.

## Next steps after the PoC

- Connectors: Confluence and Jira APIs instead of files; incremental reindexing.
- Better retrieval: hybrid (BM25 + embedding) and a larger embedding model (`multilingual-e5-large`). The current one only reads ~128 tokens per chunk and handles acronyms poorly.
- Gaps → a "draft this doc" button that drafts the missing page from related tickets.
- Slack/Teams bot using the same `assistant.ask()`.
