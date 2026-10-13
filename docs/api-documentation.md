# API documentation

The FastAPI application in `backend/` serves the API under the `/api/v1` prefix.

## Health check

`GET /api/v1/health`

Returns `{"status": "ok"}` when the API is running.

Interactive OpenAPI documentation is available at `/docs` when the server is
running.
