from typing import Any, Literal
from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    question: str = Field(min_length=3, max_length=3000)
    top_k: int = Field(default=5, ge=1, le=15)

class Source(BaseModel):
    id: str
    title: str
    snippet: str
    score: float
    source_type: Literal["document", "sql", "graph"]

class QueryResponse(BaseModel):
    question: str
    intent: str
    answer: str
    sources: list[Source]
    latency_ms: float
    metrics: dict[str, Any]
