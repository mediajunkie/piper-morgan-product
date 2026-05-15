"""Unit tests for the topic-extractor and preview helpers (Issue #1021).

Covers the module-level helpers in services.database.repositories that
back the DBUserHistoryRepository ConversationSummary projection:
- _extract_topics_heuristic — heuristic intents+entities aggregation
- _build_preview — single-line truncation of first user message
"""

from dataclasses import dataclass, field
from typing import List, Optional

import pytest

from services.database.repositories import (
    _build_preview,
    _extract_topics_heuristic,
)


@dataclass
class _FakeTurn:
    """Minimal duck-typed stand-in for ConversationTurnDB / domain.ConversationTurn."""

    intent: Optional[str] = None
    entities: List = field(default_factory=list)


class TestExtractTopicsHeuristic:
    def test_empty_turns_returns_empty(self):
        assert _extract_topics_heuristic([]) == []

    def test_extracts_intent(self):
        turns = [_FakeTurn(intent="roadmap_planning")]
        assert _extract_topics_heuristic(turns) == ["roadmap planning"]

    def test_strips_generic_intents(self):
        turns = [
            _FakeTurn(intent="general_query"),
            _FakeTurn(intent="greeting"),
            _FakeTurn(intent="small_talk"),
        ]
        assert _extract_topics_heuristic(turns) == []

    def test_extracts_string_entities(self):
        turns = [_FakeTurn(entities=["Project Alpha", "Q1 roadmap"])]
        assert _extract_topics_heuristic(turns) == ["project alpha", "q1 roadmap"]

    def test_dedupes_case_insensitive(self):
        turns = [
            _FakeTurn(entities=["Roadmap"]),
            _FakeTurn(entities=["roadmap", "ROADMAP"]),
        ]
        assert _extract_topics_heuristic(turns) == ["roadmap"]

    def test_caps_at_max_topics(self):
        turns = [_FakeTurn(entities=[f"topic-{i}" for i in range(20)])]
        result = _extract_topics_heuristic(turns, max_topics=3)
        assert len(result) == 3
        assert result == ["topic-0", "topic-1", "topic-2"]

    def test_combines_intent_and_entities(self):
        turns = [
            _FakeTurn(intent="onboarding_flow", entities=["new user", "trial"]),
        ]
        result = _extract_topics_heuristic(turns)
        assert "onboarding flow" in result
        assert "new user" in result
        assert "trial" in result

    def test_tolerates_dict_entities(self):
        turns = [_FakeTurn(entities=[{"name": "Acme Corp"}, {"value": "renewal"}])]
        assert _extract_topics_heuristic(turns) == ["acme corp", "renewal"]

    def test_ignores_malformed_entities(self):
        turns = [_FakeTurn(entities=[None, 42, {"unrelated": "key"}, ""])]
        assert _extract_topics_heuristic(turns) == []


class TestBuildPreview:
    def test_empty_message_returns_empty_string(self):
        assert _build_preview("") == ""
        assert _build_preview(None) == ""

    def test_short_message_passes_through(self):
        assert _build_preview("Hello, what's on my calendar?") == "Hello, what's on my calendar?"

    def test_strips_newlines(self):
        result = _build_preview("Line one\nLine two\r\nLine three")
        assert "\n" not in result
        assert "\r" not in result

    def test_truncates_long_message_with_ellipsis(self):
        long_msg = "a " * 300
        result = _build_preview(long_msg, max_len=50)
        assert len(result) <= 50
        assert result.endswith("…")

    def test_default_max_len_is_280(self):
        msg = "x" * 500
        result = _build_preview(msg)
        assert len(result) <= 280
