
# Evalora

Evalora is a platform for evaluating AI model responses and detecting
hallucinations. The repository contains a React + Vite + TypeScript frontend
and a FastAPI backend.

## Project structure

- `frontend/` — React, Vite, and TypeScript application
- `backend/` — FastAPI API and evaluation services
- `data/` — local evaluation datasets
- `docs/` — architecture and API documentation

## Getting started

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API health check is available at `http://localhost:8000/api/v1/health`.
