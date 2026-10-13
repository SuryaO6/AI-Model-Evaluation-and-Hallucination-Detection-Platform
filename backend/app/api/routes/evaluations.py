"""Evaluation endpoints."""

from datetime import datetime, timezone
from os import getenv
from time import perf_counter
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv

from app.providers import gemini, grok
from app.evaluation.runner import evaluate_answer
from app.schemas.evaluation import (
    EvaluationRequest,
    EvaluationResult,
    FrontendEvaluationResult,
    ModelEvaluationRequest,
    ModelEvaluationResponse,
)
from app.services.evaluation_service import run_evaluation

load_dotenv()

router = APIRouter(prefix="/evaluations", tags=["evaluations"])


@router.post("", response_model=EvaluationResult)
def create_evaluation(request: EvaluationRequest) -> EvaluationResult:
    return run_evaluation(request)


@router.post("/run", response_model=FrontendEvaluationResult)
def run_model_evaluation(
    request: ModelEvaluationRequest,
) -> FrontendEvaluationResult:
    responses: list[ModelEvaluationResponse] = []
    generators = {
        "gemini": (gemini.generate, getenv("GEMINI_API_KEY")),
        "grok": (grok.generate, getenv("GROK_API_KEY")),
    }

    for model in request.models:
        generator = generators.get(model)
        if generator is None or not generator[1]:
            raise HTTPException(
                status_code=400,
                detail=f"Model '{model}' is not configured on the backend",
            )
        started = perf_counter()
        try:
            text = generator[0](request.prompt, request.context, generator[1])
        except Exception as exc:
            raise HTTPException(
                status_code=502,
                detail=f"{model} provider failed: {exc}",
            ) from exc

        evaluation = evaluate_answer(
            question=request.prompt,
            reference_context=request.context or "",
            answer=text,
        )
        factuality = evaluation.factuality_score if request.context else 0.5
        evidence_coverage = (
            evaluation.supported_count / evaluation.claim_count
            if request.context and evaluation.claim_count
            else 0.5
        )
        quality_score = 0.75 if text else 0.0
        overall = round(
            (
                quality_score
                + factuality
                + quality_score
                + quality_score
                + evidence_coverage
            )
            / 5,
            3,
        )
        hallucinations = [
            {
                "id": f"{model}-claim-{index}",
                "snippet": claim.claim,
                "severity": (
                    "high"
                    if claim.status.value == "contradicted"
                    else "medium"
                ),
                "explanation": (
                    "The claim could not be verified against the supplied context."
                ),
            }
            for index, claim in enumerate(evaluation.claims)
            if claim.status.value != "supported"
        ]
        responses.append(
            ModelEvaluationResponse(
                modelId=model,
                text=text,
                latencyMs=round((perf_counter() - started) * 1000),
                tokenCount=len(text.split()),
                scores={
                    "relevance": quality_score,
                    "factuality": factuality,
                    "coherence": quality_score,
                    "completeness": quality_score,
                    "evidenceCoverage": evidence_coverage,
                    "overall": overall,
                },
                hallucinations=hallucinations,
            )
        )

    now = datetime.now(timezone.utc).isoformat()
    return FrontendEvaluationResult(
        id=f"eval-{uuid4()}",
        prompt=request.prompt,
        context=request.context,
        models=request.models,
        criteria=request.criteria,
        responses=responses,
        status="completed",
        createdAt=now,
        completedAt=now,
    )
