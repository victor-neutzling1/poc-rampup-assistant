"""Load docs (Markdown/text) and resolved tickets (JSON), chunk them, embed, and save the index.

Usage: python -m app.ingest
"""
import json
import re

from . import config
from .store import Chunk, VectorStore

MAX_CHARS = 500  # the embedding model only reads ~128 tokens, so keep chunks around that size
SKIP_SECTIONS = {"table of contents", "contents", "revision history"}  # navigation/boilerplate, only adds noise
INVISIBLE = dict.fromkeys(map(ord, "​‌‍﻿ "), None)  # Confluence copy-paste leftovers


def split_long(text: str) -> list[str]:
    if len(text) <= MAX_CHARS:
        return [text]
    parts, current = [], ""
    for para in re.split(r"\n\s*\n", text):
        if current and len(current) + len(para) > MAX_CHARS:
            parts.append(current.strip())
            current = ""
        current += para + "\n\n"
    if current.strip():
        parts.append(current.strip())
    return parts


def title_from_filename(rel_path: str) -> str:
    stem = rel_path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    return re.sub(r"[-_]+", " ", stem).strip().capitalize()


def looks_like_heading(line: str, next_line: str) -> bool:
    """Plain text pasted from Confluence loses the heading markup; recover it heuristically:
    a short, unindented line that doesn't end like a sentence, followed by a blank line."""
    if not line or line[0].isspace() or next_line.strip():
        return False
    s = line.strip().rstrip(":")
    return (0 < len(s) <= 70 and len(s.split()) <= 9 and s[0].isalnum()
            and not s.endswith((".", ",", ";", "?", "!", ")")) and not line.startswith(("git ", "http"))
            and not re.search(r"[=\\%$<>{}|]|://", s))  # commands, paths, URLs


def split_sections(lines: list[str]) -> list[tuple[str, str]]:
    """[(heading, body)] using Markdown `##`/`###` headings, or recovered headings for plain pasted text."""
    markdown = any(re.match(r"#{2,3} ", l) for l in lines)
    sections, heading, body = [], "Overview", []
    in_code = False
    for i, line in enumerate(lines):
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if line.lstrip().startswith("```"):
            in_code = not in_code
        if in_code or line.lstrip().startswith("```"):
            body.append(line)  # never treat a line inside a code block as a heading
            continue
        if markdown:
            is_heading = bool(re.match(r"#{2,3} ", line))
            text = line.lstrip("#").strip()
        else:
            is_heading = looks_like_heading(line, nxt)
            text = line.strip().rstrip(":")
        if is_heading:
            sections.append((heading, "\n".join(body).strip()))
            heading, body = text, []
        else:
            body.append(line)
    sections.append((heading, "\n".join(body).strip()))
    return [(h, b) for h, b in sections if b and h.lower() not in SKIP_SECTIONS]


def chunk_document(rel_path: str, text: str) -> list[Chunk]:
    """One chunk per section (long sections split by paragraphs), cited as 'Doc title › Section'."""
    lines = text.translate(INVISIBLE).splitlines()
    first = next((i for i, l in enumerate(lines) if l.strip()), None)
    # Only a `# ` on the first non-empty line is the title; later ones are usually shell comments in code samples.
    if first is not None and lines[first].startswith("# "):
        doc_title, lines = lines[first][2:].strip(), lines[first + 1:]
    else:
        doc_title = title_from_filename(rel_path)
    # An "Owner: ... · Also ask: ..." line near the top is attached to every chunk, so whichever section is
    # retrieved, the LLM knows who to point people to.
    owner_idx = next((i for i, l in enumerate(lines[:10]) if l.startswith("Owner:")), None)
    contacts = ""
    if owner_idx is not None:
        contacts = lines[owner_idx].replace("Owner:", "", 1).replace("· Also ask:", ";").strip()
        lines = lines[:owner_idx] + lines[owner_idx + 1:]
    # Quote lines above the first heading are page banners (e.g. "> Fictional content..."), not content worth indexing.
    first_heading = next((i for i, l in enumerate(lines) if re.match(r"#{2,3} ", l)), len(lines))
    lines = [l for i, l in enumerate(lines) if i >= first_heading or not l.startswith(">")]
    chunks = []
    for s, (heading, body) in enumerate(split_sections(lines)):
        for n, part in enumerate(split_long(body)):
            chunks.append(Chunk(
                id=f"{rel_path}#{s}-{n}",
                source_type="doc",
                title=f"{doc_title} › {heading}",
                location=rel_path,
                text=part,
                contacts=contacts,
            ))
    return chunks


def load_docs() -> list[Chunk]:
    docs_dir = config.DATA_DIR / "docs"
    chunks = []
    for path in sorted(docs_dir.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(config.DATA_DIR).as_posix()
        if path.suffix.lower() not in {".md", ".txt"}:
            print(f"  skipped (not .md/.txt): {rel}")
            continue
        chunks += chunk_document(rel, path.read_text(encoding="utf-8"))
    return chunks


def load_tickets() -> list[Chunk]:
    """Each resolved ticket becomes one chunk: problem + resolution is exactly the Q&A pair we want."""
    chunks = []
    for path in sorted((config.DATA_DIR / "tickets").glob("*.json")):
        for t in json.loads(path.read_text(encoding="utf-8")):
            if t.get("status", "resolved").lower() not in {"resolved", "closed", "done"}:
                continue
            chunks.append(Chunk(
                id=t["id"],
                source_type="ticket",
                title=f"{t['id']}: {t['title']}",
                location=t["id"],
                text=f"Problem: {t['description']}\nResolution: {t['resolution']}",
                contacts=t.get("assignee", ""),
            ))
    return chunks


def main() -> None:
    chunks = load_docs() + load_tickets()
    if not chunks:
        raise SystemExit(f"No docs or tickets found under {config.DATA_DIR}")
    print(f"Embedding {len(chunks)} chunks "
          f"({sum(c.source_type == 'doc' for c in chunks)} doc sections, "
          f"{sum(c.source_type == 'ticket' for c in chunks)} tickets)...")
    VectorStore.build(chunks).save()
    print(f"Index saved to {config.INDEX_DIR}")


if __name__ == "__main__":
    main()
