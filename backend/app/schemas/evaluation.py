"""Request and response schemas for answer evaluation."""

from enum import Enum

from pydantic import BaseModel, Field, field_validator


class ClaimStatus(str, Enum):
    SUPPORTED = "supported"
    CONTRADICTED = "contradicted"
    UNVERIFIABLE = "unverifiable"


class EvaluationRequest(BaseModel):
    question: str = Field(min_length=1)
    reference_context: str = Field(min_length=1)
    answer: str = Field(min_length=1)

    @field_validator("question", "reference_context", "answer")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value


class ClaimResult(BaseModel):
    claim: str
    status: ClaimStatus
    confidence: float = Field(ge=0.0, le=1.0)
    evidence: str | None = None


class EvaluationResult(BaseModel):
    question: str
    overall_score: float = Field(ge=0.0, le=1.0)
    factuality_score: float = Field(ge=0.0, le=1.0)
    claim_count: int = Field(ge=0)
    supported_count: int = Field(ge=0)
    contradicted_count: int = Field(ge=0)
    unverifiable_count: int = Field(ge=0)
    claims: list[ClaimResult]
