"""Small, dependency-free text processing helpers for evaluation."""

from __future__ import annotations

import re

_WORD_PATTERN = re.compile(r"\b[\w'-]+\b")
_SENTENCE_PATTERN = re.compile(r"(?<=[.!?])\s+|\n+")
_STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "was",
    "were",
    "with",
}


def normalize_text(text: str) -> str:
    """Collapse whitespace and normalize casing for comparisons."""
    return " ".join(text.lower().split())


def split_sentences(text: str) -> list[str]:
    """Return non-empty sentence-like units while preserving original text."""
    return [part.strip() for part in _SENTENCE_PATTERN.split(text) if part.strip()]


def content_tokens(text: str) -> set[str]:
    """Return meaningful lowercase tokens used for lexical evidence matching."""
    return {
        token
        for token in _WORD_PATTERN.findall(normalize_text(text))
        if token not in _STOP_WORDS
    }
