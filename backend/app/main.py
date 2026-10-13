from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.evaluations import router as evaluations_router
from app.api.routes.health import router as health_router

app = FastAPI(
    title="Evalora API",
    description="API for AI model evaluation and hallucination detection.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(evaluations_router, prefix="/api/v1")
