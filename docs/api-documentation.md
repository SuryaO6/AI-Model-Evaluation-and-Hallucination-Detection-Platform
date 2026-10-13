# API documentation

The FastAPI application in `backend/` serves the API under the `/api/v1` prefix.

## Health check

`GET /api/v1/health`

Returns `{"status": "ok"}` when the API is running.

Interactive OpenAPI documentation is available at `/docs` when the server is
running.

## Evaluate an answer

`POST /api/v1/evaluations`

Request:

```json
{
  "question": "What is the capital of France?",
  "reference_context": "Paris is the capital of France.",
  "answer": "The capital of France is Paris."
}
```

The response contains each extracted claim and its status:
`supported`, `contradicted`, or `unverifiable`.

```json
{
  "question": "What is the capital of France?",
  "overall_score": 1.0,
  "factuality_score": 1.0,
  "claim_count": 1,
  "supported_count": 1,
  "contradicted_count": 0,
  "unverifiable_count": 0,
  "claims": [
    {
      "claim": "The capital of France is Paris.",
      "status": "supported",
      "confidence": 0.9,
      "evidence": "Paris is the capital of France."
    }
  ]
}
```
