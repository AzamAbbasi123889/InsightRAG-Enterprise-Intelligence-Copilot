# API

## GET /health

Returns service status and whether an LLM key is configured.

## POST /api/query

Request:

```json
{"question":"Why did Europe revenue decline in Q3?","top_k":5}
```

Response contains:

- `intent`
- `answer`
- `sources`
- `latency_ms`
- `metrics`

## GET /api/metrics

Returns dashboard starter metrics and evaluation notes.
