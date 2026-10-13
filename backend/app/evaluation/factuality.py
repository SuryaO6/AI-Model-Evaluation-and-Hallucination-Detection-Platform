"""Claim extraction and reference-grounded factuality classification."""

from __future__ import annotations

from app.evaluation.evidence import find_evidence
from app.schemas.evaluation import ClaimResult, ClaimStatus
from app.utils.text_processing import split_sentences


def classify_claims(answer: str, reference_context: str) -> list[ClaimResult]:
    """Extract answer sentences and classify them against reference evidence."""
    claims: list[ClaimResult] = []
    for claim in split_sentences(answer):
        evidence, overlap, has_negation_mismatch = find_evidence(
            claim, reference_context
        )
        if evidence is None:
            status = ClaimStatus.UNVERIFIABLE
            confidence = 0.35
        elif has_negation_mismatch:
            status = ClaimStatus.CONTRADICTED
            confidence = min(1.0, 0.65 + overlap * 0.35)
        else:
            status = ClaimStatus.SUPPORTED
            confidence = min(1.0, 0.55 + overlap * 0.45)

        claims.append(
            ClaimResult(
                claim=claim,
                status=status,
                confidence=round(confidence, 3),
                evidence=evidence,
            )
        )
    return claims
