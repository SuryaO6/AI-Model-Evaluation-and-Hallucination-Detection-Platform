"""Public orchestration entry point for answer evaluation."""

from app.evaluation.factuality import classify_claims
from app.evaluation.scoring import build_result
from app.schemas.evaluation import EvaluationResult


def evaluate_answer(
    question: str, reference_context: str, answer: str
) -> EvaluationResult:
    """Evaluate answer claims against trusted reference context."""
    claims = classify_claims(answer, reference_context)
    return build_result(question, claims)
