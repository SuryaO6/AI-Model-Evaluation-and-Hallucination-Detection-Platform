"""Evaluation endpoints."""

from fastapi import APIRouter

from app.schemas.evaluation import EvaluationRequest, EvaluationResult
from app.services.evaluation_service import run_evaluation

router = APIRouter(prefix="/evaluations", tags=["evaluations"])


@router.post("", response_model=EvaluationResult)
def create_evaluation(request: EvaluationRequest) -> EvaluationResult:
    return run_evaluation(request)
