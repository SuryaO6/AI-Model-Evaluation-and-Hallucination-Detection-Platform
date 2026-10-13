from fastapi import FastAPI

from app.api.routes.health import router as health_router

app = FastAPI(
    title="Evalora API",
    description="API for AI model evaluation and hallucination detection.",
    version="0.1.0",
)

app.include_router(health_router, prefix="/api/v1")
