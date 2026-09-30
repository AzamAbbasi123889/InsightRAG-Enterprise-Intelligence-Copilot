# InsightRAG — Enterprise Intelligence Copilot

A portfolio-ready, production-oriented RAG platform that combines **document retrieval, SQL analytics, hybrid search, evidence citations, optional GraphRAG, evaluation, and observability**.

## What this project demonstrates

- Hybrid retrieval: TF-IDF/semantic embeddings + BM25-style keyword matching
- Query routing across documents and structured business data
- SQL analytics over customer, product, revenue, and support-ticket data
- Evidence-backed answers with source citations
- Optional Neo4j knowledge-graph expansion
- Optional OpenAI-compatible LLMs (Groq/OpenAI-compatible endpoints)
- RAG evaluation scripts for retrieval hit-rate and answer groundedness checks
- React dashboard for analysts and hiring managers to explore the system
- Docker Compose for PostgreSQL, Neo4j, backend, and frontend
- Clean service-oriented Python/FastAPI architecture

## Business scenario

The demo simulates a SaaS company. Users can ask questions such as:

> Why did Europe revenue decline in Q3, and which products contributed most?

> What is the refund policy for enterprise customers?

> Which products have high support volume but declining renewals?

> Summarize the risks mentioned in the latest annual report.

The system decides whether a question needs documents, SQL, or a hybrid response.

## Architecture

```text
                         ┌─────────────────┐
                         │   React UI      │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ FastAPI API     │
                         │ Query Router    │
                         └───────┬─────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              ▼                  ▼                  ▼
       ┌────────────┐      ┌────────────┐     ┌────────────┐
       │ Hybrid RAG │      │ SQL Agent  │     │ GraphRAG   │
       │ Vector+BM25│      │ PostgreSQL │     │ Neo4j      │
       └─────┬──────┘      └─────┬──────┘     └─────┬──────┘
             └────────────────────┼──────────────────┘
                                  ▼
                         ┌─────────────────┐
                         │ Evidence Fusion │
                         │ + LLM Generator │
                         └────────┬────────┘
                                  ▼
                         Answer + Citations
                                  │
                                  ▼
                        Evaluation / Metrics
```

## Project structure

```text
InsightRAG_Enterprise_Intelligence/
├── backend/
│   ├── app/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── schemas.py
│   │   └── services/
│   │       ├── graph_service.py
│   │       ├── llm_service.py
│   │       ├── query_router.py
│   │       ├── rag_service.py
│   │       └── sql_service.py
│   ├── data/
│   │   ├── docs/
│   │   ├── seed.sql
│   │   └── eval_questions.json
│   ├── scripts/
│   │   ├── ingest.py
│   │   └── evaluate.py
│   ├── tests/
│   │   └── test_api.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
├── docs/
│   ├── architecture.md
│   └── api.md
├── .env.example
├── docker-compose.yml
└── LICENSE
```

## Run locally — fastest path

### 1. Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python scripts/ingest.py
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

The backend has a deterministic fallback mode, so the demo works without an LLM API key. To enable generated answers, copy `.env.example` to `.env` and set an OpenAI-compatible provider.

## Docker

```bash
docker compose up --build
```

Services:

- Frontend: `http://localhost:5173`
- API: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- PostgreSQL: `localhost:5432`
- Neo4j browser: `http://localhost:7474`

## LLM configuration

The backend supports an OpenAI-compatible endpoint. Example for Groq:

```env
LLM_API_KEY=your_key
LLM_BASE_URL=https://api.groq.com/openai/v1
LLM_MODEL=llama-3.3-70b-versatile
```

You can also point the same interface to another OpenAI-compatible provider.

## Example API call

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question":"Why did Europe revenue decline in Q3, and which products contributed most?"}'
```

## Interview talking points

1. **Why hybrid retrieval?** Keyword search is strong for exact product names, policy terms and identifiers; semantic retrieval is strong for paraphrased questions.
2. **Why query routing?** Not every question should be sent through vector search. Business metrics belong in SQL and relationship-heavy questions can benefit from a graph.
3. **How is hallucination reduced?** The generator is given only retrieved evidence and the API returns source citations.
4. **How do you evaluate RAG?** The evaluation script measures retrieval hit rate against a labeled question set; production systems should add faithfulness, answer relevance and latency/cost monitoring.
5. **How would you scale it?** Replace in-memory indexes with Qdrant/Pinecone, add async workers, use PostgreSQL read replicas, add Redis caching, and stream generation.

## Next-level extensions

- Add Qdrant or Pinecone as the vector store
- Add Elasticsearch/OpenSearch for BM25 retrieval
- Add a learned cross-encoder reranker
- Add LangGraph for multi-step agents
- Add OpenTelemetry + Prometheus/Grafana
- Add role-based access controls and document-level permissions
- Add PII redaction before indexing
- Add prompt-injection and data-exfiltration tests
- Add a human feedback loop for retrieval quality
