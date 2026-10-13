# Architecture

Evalora is organized as a React + Vite + TypeScript frontend and a Python +
FastAPI backend.

- `frontend/` contains the web application, shared UI, feature pages, and API services.
- `backend/app/api/` exposes versioned HTTP endpoints.
- `backend/app/services/` coordinates application behavior; providers and evaluation
  modules contain model integrations and evaluation metrics.
- `backend/app/database/` contains persistence infrastructure.
- `data/` is reserved for local evaluation datasets and should not contain secrets.

The initial API health check is available at `/api/v1/health`.
