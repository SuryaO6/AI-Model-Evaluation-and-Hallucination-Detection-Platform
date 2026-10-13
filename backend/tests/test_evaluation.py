from fastapi.testclient import TestClient

from app.evaluation.runner import evaluate_answer
from app.main import app


def test_evaluate_answer_classifies_supported_and_unverifiable_claims() -> None:
    result = evaluate_answer(
        "What is the capital of France?",
        "Paris is the capital of France.",
        "The capital of France is Paris. France has 80 million residents.",
    )

    assert result.supported_count == 1
    assert result.unverifiable_count == 1
    assert result.contradicted_count == 0
    assert result.factuality_score == 0.5


def test_evaluate_answer_detects_negation_contradiction() -> None:
    result = evaluate_answer(
        "Is water wet?",
        "Water is wet.",
        "Water is not wet.",
    )

    assert result.contradicted_count == 1
    assert result.claims[0].evidence == "Water is wet."


def test_evaluations_endpoint_returns_json_contract() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/evaluations",
        json={
            "question": "What is the capital of France?",
            "reference_context": "Paris is the capital of France.",
            "answer": "Paris is the capital of France.",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["supported_count"] == 1
    assert body["claims"][0]["status"] == "supported"


def test_evaluations_endpoint_rejects_blank_input() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/evaluations",
        json={"question": "", "reference_context": "context", "answer": "answer"},
    )

    assert response.status_code == 422


def test_evaluations_endpoint_rejects_whitespace_only_input() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/evaluations",
        json={
            "question": "   ",
            "reference_context": "context",
            "answer": "answer",
        },
    )

    assert response.status_code == 422


def test_evaluate_answer_handles_punctuated_negation() -> None:
    result = evaluate_answer(
        "Is water wet?",
        "Water is wet.",
        "Water is not wet.",
    )

    assert result.claims[0].status.value == "contradicted"
