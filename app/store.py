"""Tiny vector store: a normalized numpy matrix + a JSON list of chunks, brute-force cosine search."""
import json
from dataclasses import dataclass, asdict
from functools import lru_cache

import numpy as np
from fastembed import TextEmbedding

from . import config


@dataclass
class Chunk:
    id: str
    source_type: str  # "doc" | "ticket"
    title: str        # human-readable citation, e.g. "dev-environment.md › VPN"
    location: str     # file path or ticket id
    text: str
    contacts: str = ""  # who to ask about this: the doc's owners or the ticket's assignee


@lru_cache(maxsize=1)
def embedder() -> TextEmbedding:
    return TextEmbedding(config.EMBED_MODEL, cache_dir=str(config.MODEL_CACHE))


def embed(texts: list[str]) -> np.ndarray:
    vecs = np.array(list(embedder().embed(texts)), dtype=np.float32)
    return vecs / np.linalg.norm(vecs, axis=1, keepdims=True)


class VectorStore:
    def __init__(self, chunks: list[Chunk], vectors: np.ndarray):
        self.chunks = chunks
        self.vectors = vectors

    @classmethod
    def build(cls, chunks: list[Chunk]) -> "VectorStore":
        # Title is embedded with the body so section names help retrieval.
        return cls(chunks, embed([f"{c.title}\n{c.text}" for c in chunks]))

    def save(self) -> None:
        config.INDEX_DIR.mkdir(exist_ok=True)
        np.save(config.INDEX_DIR / "vectors.npy", self.vectors)
        (config.INDEX_DIR / "chunks.json").write_text(
            json.dumps([asdict(c) for c in self.chunks], ensure_ascii=False, indent=1), encoding="utf-8"
        )

    @classmethod
    def load(cls) -> "VectorStore":
        chunks_file = config.INDEX_DIR / "chunks.json"
        if not chunks_file.exists():
            raise FileNotFoundError("Index not found - run `python -m app.ingest` first.")
        chunks = [Chunk(**c) for c in json.loads(chunks_file.read_text(encoding="utf-8"))]
        return cls(chunks, np.load(config.INDEX_DIR / "vectors.npy"))

    def search(self, query: str, k: int = config.TOP_K) -> list[tuple[Chunk, float]]:
        scores = self.vectors @ embed([query])[0]
        top = np.argsort(-scores)[:k]
        return [(self.chunks[i], float(scores[i])) for i in top]
