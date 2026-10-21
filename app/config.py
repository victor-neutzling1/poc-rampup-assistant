import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
# Keys and settings can live in a .env file at the project root (git-ignored). Variables already set in the shell win.
load_dotenv(ROOT / ".env")
DATA_DIR = Path(os.getenv("RAMPUP_DATA_DIR", ROOT / "data"))
INDEX_DIR = ROOT / "index"
MODEL_CACHE = ROOT / ".models"
GAPS_DB = ROOT / "gaps.db"

# Multilingual so a question in Portuguese still matches English docs.
EMBED_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-flash")

TOP_K = int(os.getenv("RAMPUP_TOP_K", "8"))  # broad questions ("tell me about project X") need several sections
# Below this cosine similarity the best match is considered "not really about this".
# Only decides gaps in offline mode; with DeepSeek, the model judges whether the excerpts answer the question
# (the small embedding model's scores are too noisy, especially across languages, to be the only signal).
MIN_SCORE = float(os.getenv("RAMPUP_MIN_SCORE", "0.35"))
# Gap questions at least this similar to each other are grouped as one missing topic.
GAP_CLUSTER_SCORE = float(os.getenv("RAMPUP_GAP_CLUSTER_SCORE", "0.7"))


def llm_enabled() -> bool:
    return bool(DEEPSEEK_API_KEY)
