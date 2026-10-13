"""Reference evidence matching for factual claims."""

from __future__ import annotations

from app.utils.text_processing import content_tokens, split_sentences

_NEGATION_WORDS = {"not", "no", "never", "cannot", "can't", "without", "none"}


def find_evidence(
    claim: str, reference_context: str
) -> tuple[str | None, float, bool]:
    """Find the strongest reference sentence and detect simple negation conflicts."""
    claim_tokens = content_tokens(claim)
    if not claim_tokens:
        return None, 0.0, False

    best_sentence: str | None = None
    best_overlap = 0.0
    for sentence in split_sentences(reference_context):
        evidence_tokens = content_tokens(sentence)
        overlap = len(claim_tokens & evidence_tokens) / len(claim_tokens)
        if overlap > best_overlap:
            best_sentence = sentence
            best_overlap = overlap

    if best_overlap < 0.5 or best_sentence is None:
        return None, best_overlap, False

    claim_is_negated = bool(_NEGATION_WORDS & content_tokens(claim))
    evidence_is_negated = bool(_NEGATION_WORDS & content_tokens(best_sentence))
    return best_sentence, best_overlap, claim_is_negated != evidence_is_negated
