"""Application service for answer evaluations."""

from app.evaluation.runner import evaluate_answer
from app.schemas.evaluation import EvaluationRequest, EvaluationResult


def run_evaluation(request: EvaluationRequest) -> EvaluationResult:
    return evaluate_answer(
        question=request.question,
        reference_context=request.reference_context,
        answer=request.answer,
    )
