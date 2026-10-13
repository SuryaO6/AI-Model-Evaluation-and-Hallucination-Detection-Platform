"""Aggregate claim classifications into an evaluation score."""

from collections import Counter

from app.schemas.evaluation import ClaimResult, ClaimStatus, EvaluationResult


def build_result(question: str, claims: list[ClaimResult]) -> EvaluationResult:
    counts = Counter(claim.status for claim in claims)
    claim_count = len(claims)
    factuality_score = (
        counts[ClaimStatus.SUPPORTED] / claim_count if claim_count else 0.0
    )
    return EvaluationResult(
        question=question,
        overall_score=round(factuality_score, 3),
        factuality_score=round(factuality_score, 3),
        claim_count=claim_count,
        supported_count=counts[ClaimStatus.SUPPORTED],
        contradicted_count=counts[ClaimStatus.CONTRADICTED],
        unverifiable_count=counts[ClaimStatus.UNVERIFIABLE],
        claims=claims,
    )
