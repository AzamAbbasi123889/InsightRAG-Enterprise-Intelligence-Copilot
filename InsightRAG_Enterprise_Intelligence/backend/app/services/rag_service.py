from __future__ import annotations
from pathlib import Path
import re
from dataclasses import dataclass
from typing import Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi

BASE_DIR = Path(__file__).resolve().parents[2]
DOC_DIR = BASE_DIR / "data" / "docs"

@dataclass
class Chunk:
    id: str
    title: str
    text: str

class HybridRAG:
    def __init__(self):
        self.chunks = self._load_chunks()
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.matrix = None
        self.bm25 = None
        self._fit()

    def _load_chunks(self):
        chunks = []
        for path in sorted(DOC_DIR.rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
            for i, para in enumerate(paragraphs):
                if len(para) < 30:
                    continue
                chunks.append(Chunk(f"{path.stem}-{i}", path.stem.replace("_", " ").title(), para))
        return chunks

    @staticmethod
    def _tokens(text: str):
        return re.findall(r"[a-zA-Z0-9]+", text.lower())

    def _fit(self):
        texts = [c.text for c in self.chunks]
        if not texts:
            return
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2))
        self.matrix = self.vectorizer.fit_transform(texts)
        self.bm25 = BM25Okapi([self._tokens(t) for t in texts])

    def search(self, query: str, top_k: int = 5):
        if not self.chunks:
            return []
        tfidf_scores = cosine_similarity(self.vectorizer.transform([query]), self.matrix).ravel()
        bm25_scores = np.array(self.bm25.get_scores(self._tokens(query)))
        def norm(x):
            if np.max(x) == np.min(x):
                return np.zeros_like(x)
            return (x - np.min(x)) / (np.max(x) - np.min(x))
        scores = 0.55 * norm(tfidf_scores) + 0.45 * norm(bm25_scores)
        order = np.argsort(scores)[::-1][:top_k]
        return [
            {"id": self.chunks[i].id, "title": self.chunks[i].title,
             "snippet": self.chunks[i].text[:500], "score": float(scores[i]),
             "source_type": "document"}
            for i in order
        ]
