from time import perf_counter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.schemas import QueryRequest, QueryResponse, Source
from app.services.query_router import route_query
from app.services.rag_service import HybridRAG
from app.services.sql_service import answer_sql
from app.services.graph_service import GraphService
from app.services.llm_service import LLMService

app = FastAPI(title="InsightRAG Enterprise Intelligence API", version="1.0.0")
origins = [x.strip() for x in settings.cors_origins.split(",") if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

rag = HybridRAG()
llm = LLMService()
graph = GraphService()

@app.get("/health")
def health():
    return {"status":"ok", "documents":len(rag.chunks), "llm_enabled":llm.enabled}

@app.post("/api/query", response_model=QueryResponse)
def query(payload: QueryRequest):
    start = perf_counter()
    intent = route_query(payload.question)
    sources = []
    evidence = []
    sql_rows = []

    if intent in {"document", "hybrid", "hybrid_graph"}:
        evidence = rag.search(payload.question, payload.top_k)
        sources.extend(evidence)

    if intent in {"sql", "hybrid", "hybrid_graph"}:
        sql_rows, sql_text = answer_sql(payload.question)
        for i, row in enumerate(sql_rows[:10]):
            sources.append({
                "id": f"sql-{i+1}",
                "title": "PostgreSQL analytics",
                "snippet": sql_text + " " + ", ".join(f"{k}={v}" for k,v in row.items()),
                "score": 1.0,
                "source_type": "sql"
            })

    if intent == "hybrid_graph":
        graph_rows = graph.query(payload.question)
        for i, row in enumerate(graph_rows[:5]):
            sources.append({"id":f"graph-{i+1}", "title":"Neo4j graph result", "snippet":str(row), "score":1.0, "source_type":"graph"})

    answer = llm.generate(payload.question, evidence, sql_rows)
    latency = (perf_counter() - start) * 1000
    metrics = {
        "retrieved_documents": len(evidence),
        "sql_rows": len(sql_rows),
        "intent": intent,
        "llm_mode": "model" if llm.enabled else "fallback",
        "citation_count": len(sources),
    }
    return QueryResponse(question=payload.question, intent=intent, answer=answer,
                         sources=[Source(**s) for s in sources], latency_ms=round(latency, 2), metrics=metrics)

@app.get("/api/metrics")
def metrics():
    return {
        "retrieval_precision_estimate": 0.89,
        "context_recall_estimate": 0.84,
        "faithfulness_estimate": 0.93,
        "answer_relevance_estimate": 0.91,
        "avg_latency_ms_demo": 420,
        "note": "Starter dashboard values; run backend/scripts/evaluate.py for dataset-based retrieval evaluation."
    }
