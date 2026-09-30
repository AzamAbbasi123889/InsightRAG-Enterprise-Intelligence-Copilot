# Architecture Notes

## Retrieval

The starter implementation combines two lexical signals:

- TF-IDF cosine similarity for phrase-level relevance
- BM25 for keyword/exact-term relevance

These are normalized and fused with a weighted score. This gives a realistic baseline before introducing a hosted vector database or learned reranker.

## Routing

The router classifies requests into document, SQL, hybrid, or hybrid-graph flows. In a production implementation, replace the rule-based router with a small intent classifier or structured-output LLM router and retain deterministic guardrails.

## Security considerations

For a real deployment, add authentication, per-document authorization, tenant isolation, audit logs, prompt-injection defenses, SQL allow-lists, sensitive-data redaction, and source-level access controls.

## Scaling path

1. Move retrieval to Qdrant/Pinecone.
2. Add OpenSearch for BM25.
3. Introduce cross-encoder reranking.
4. Add Redis caching.
5. Add async ingestion with Celery or a queue.
6. Add OpenTelemetry traces and Prometheus metrics.
7. Add evaluation gates to CI/CD.
