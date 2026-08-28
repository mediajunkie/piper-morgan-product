"""
#1004 Fix B — tests for SemanticBoundaryDetector (Layer 2).

Covers:
- Pydantic schema (model_config extra='forbid', confidence range, category enum)
- Threshold tier classification (BLOCK ≥0.85 / AMBIGUOUS 0.6–0.85 / PASS <0.6)
- Refusal-to-classify fallback (LLM exception, JSON parse error, schema error)
- Cache hit/miss
- Code-fence stripping in LLM output

LLM client is fully mocked. No network, no API keys required.

Per #1004 contract v1.0 §"SemanticDetectorOutput", §"Threshold tiers",
§"Refusal-to-classify behavior", §"Cache contract (MVP)".
"""

import json
from typing import Any, Optional
from unittest.mock import AsyncMock

import pytest
from pydantic import ValidationError

from services.ethics.semantic_boundary_detector import (
    AMBIGUOUS_THRESHOLD,
    BLOCK_THRESHOLD,
    REFUSAL_FALLBACK,
    SemanticBoundaryDetector,
    SemanticDetectorOutput,
    _LRUCache,
    classify_decision,
)

# ---------------------------------------------------------------------------
# Mock LLM client
# ---------------------------------------------------------------------------


class _FakeLLMClient:
    """Records calls and returns canned responses."""

    def __init__(self, response: Optional[str] = None, raise_on_call: Optional[Exception] = None):
        self.response = response
        self.raise_on_call = raise_on_call
        self.calls: list[dict[str, Any]] = []

    async def complete(self, **kwargs):
        self.calls.append(kwargs)
        if self.raise_on_call:
            raise self.raise_on_call
        return self.response


def _make_detector(response: Optional[str] = None, raise_on_call: Optional[Exception] = None):
    return SemanticBoundaryDetector(
        llm_client=_FakeLLMClient(response=response, raise_on_call=raise_on_call)
    )


# ---------------------------------------------------------------------------
# Schema tests
# ---------------------------------------------------------------------------


def test_schema_accepts_well_formed_payload():
    out = SemanticDetectorOutput(
        violation_detected=True,
        category="harassment",
        confidence=0.9,
        reasoning="Request targets a named colleague's standing.",
        redirect_hint="redirect toward workflow process",
    )
    assert out.violation_detected is True
    assert out.category == "harassment"
    assert out.confidence == 0.9


def test_schema_rejects_extra_fields():
    """model_config extra='forbid' catches prompt drift."""
    with pytest.raises(ValidationError):
        SemanticDetectorOutput(
            violation_detected=False,
            category="none",
            confidence=0.0,
            reasoning="ok",
            redirect_hint=None,
            severity="block",  # not in schema
        )


def test_schema_rejects_invalid_category():
    with pytest.raises(ValidationError):
        SemanticDetectorOutput(
            violation_detected=False,
            category="not_a_category",
            confidence=0.0,
            reasoning="ok",
            redirect_hint=None,
        )


def test_schema_rejects_out_of_range_confidence():
    with pytest.raises(ValidationError):
        SemanticDetectorOutput(
            violation_detected=False,
            category="none",
            confidence=1.5,
            reasoning="ok",
            redirect_hint=None,
        )
    with pytest.raises(ValidationError):
        SemanticDetectorOutput(
            violation_detected=False,
            category="none",
            confidence=-0.1,
            reasoning="ok",
            redirect_hint=None,
        )


def test_schema_caps_reasoning_length():
    too_long = "x" * 501
    with pytest.raises(ValidationError):
        SemanticDetectorOutput(
            violation_detected=False,
            category="none",
            confidence=0.0,
            reasoning=too_long,
            redirect_hint=None,
        )


# ---------------------------------------------------------------------------
# Threshold-tier tests
# ---------------------------------------------------------------------------


def test_classify_decision_block_at_threshold():
    assert classify_decision(BLOCK_THRESHOLD) == "block"
    assert classify_decision(0.95) == "block"
    assert classify_decision(1.0) == "block"


def test_classify_decision_ambiguous_band():
    assert classify_decision(AMBIGUOUS_THRESHOLD) == "ambiguous"
    assert classify_decision(0.7) == "ambiguous"
    # Just below block threshold
    assert classify_decision(BLOCK_THRESHOLD - 0.001) == "ambiguous"


def test_classify_decision_pass_band():
    assert classify_decision(0.0) == "pass"
    assert classify_decision(0.5) == "pass"
    assert classify_decision(AMBIGUOUS_THRESHOLD - 0.001) == "pass"


# ---------------------------------------------------------------------------
# detect() — happy path
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_detect_parses_clean_json_response():
    payload = json.dumps(
        {
            "violation_detected": True,
            "category": "harassment",
            "confidence": 0.92,
            "reasoning": "Request targets a named colleague.",
            "redirect_hint": "redirect toward workflow process",
        }
    )
    detector = _make_detector(response=payload)
    out = await detector.detect("any message")
    assert out.violation_detected is True
    assert out.category == "harassment"
    assert out.confidence == 0.92


@pytest.mark.asyncio
async def test_detect_strips_code_fence_wrapping():
    """Some providers wrap JSON in ```json fences despite the prompt."""
    payload = (
        "```json\n"
        + json.dumps(
            {
                "violation_detected": False,
                "category": "none",
                "confidence": 0.95,
                "reasoning": "Legitimate PM request.",
                "redirect_hint": None,
            }
        )
        + "\n```"
    )
    detector = _make_detector(response=payload)
    out = await detector.detect("any message")
    assert out.violation_detected is False
    assert out.category == "none"


@pytest.mark.asyncio
async def test_detect_passes_message_as_prompt_and_uses_system_prompt():
    payload = json.dumps(
        {
            "violation_detected": False,
            "category": "none",
            "confidence": 0.9,
            "reasoning": "ok",
            "redirect_hint": None,
        }
    )
    fake = _FakeLLMClient(response=payload)
    detector = SemanticBoundaryDetector(llm_client=fake)
    await detector.detect("user content here")
    assert len(fake.calls) == 1
    call = fake.calls[0]
    assert call["task_type"] == "boundary_detection"
    assert call["prompt"] == "user content here"
    assert "boundary-detection classifier" in call["system"]


# ---------------------------------------------------------------------------
# detect() — refusal-to-classify fallback
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_detect_returns_fallback_on_llm_exception():
    detector = _make_detector(raise_on_call=RuntimeError("provider down"))
    out = await detector.detect("any message")
    assert out == REFUSAL_FALLBACK
    assert out.violation_detected is False
    assert out.category == "none"
    assert out.confidence == 0.0


@pytest.mark.asyncio
async def test_detect_returns_fallback_on_json_parse_error():
    detector = _make_detector(response="not json at all { broken")
    out = await detector.detect("any message")
    assert out == REFUSAL_FALLBACK


@pytest.mark.asyncio
async def test_detect_returns_fallback_on_schema_violation():
    """LLM produces JSON but schema doesn't match."""
    bad_payload = json.dumps(
        {
            "violation_detected": True,
            "category": "made_up_category",
            "confidence": 0.9,
            "reasoning": "x",
        }
    )
    detector = _make_detector(response=bad_payload)
    out = await detector.detect("any message")
    assert out == REFUSAL_FALLBACK


@pytest.mark.asyncio
async def test_detect_returns_fallback_on_extra_field():
    """model_config extra='forbid' triggers fallback on prompt drift."""
    bad_payload = json.dumps(
        {
            "violation_detected": False,
            "category": "none",
            "confidence": 0.0,
            "reasoning": "ok",
            "redirect_hint": None,
            "severity": "block",  # drift
        }
    )
    detector = _make_detector(response=bad_payload)
    out = await detector.detect("any message")
    assert out == REFUSAL_FALLBACK


@pytest.mark.asyncio
async def test_detect_returns_fallback_on_empty_response():
    detector = _make_detector(response="")
    out = await detector.detect("any message")
    assert out == REFUSAL_FALLBACK


# ---------------------------------------------------------------------------
# Cache tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_detect_caches_result():
    payload = json.dumps(
        {
            "violation_detected": False,
            "category": "none",
            "confidence": 0.9,
            "reasoning": "ok",
            "redirect_hint": None,
        }
    )
    fake = _FakeLLMClient(response=payload)
    detector = SemanticBoundaryDetector(llm_client=fake)

    # First call — LLM invoked
    await detector.detect("same message")
    assert len(fake.calls) == 1

    # Second call with same message — served from cache
    await detector.detect("same message")
    assert len(fake.calls) == 1

    # Different message — LLM invoked again
    await detector.detect("different message")
    assert len(fake.calls) == 2


@pytest.mark.asyncio
async def test_cache_lookup_does_not_mutate_lru_order():
    payload = json.dumps(
        {
            "violation_detected": False,
            "category": "none",
            "confidence": 0.9,
            "reasoning": "ok",
            "redirect_hint": None,
        }
    )
    detector = SemanticBoundaryDetector(llm_client=_FakeLLMClient(response=payload))
    assert detector.cache_lookup("foo") is False
    await detector.detect("foo")
    assert detector.cache_lookup("foo") is True


def test_lru_cache_evicts_oldest_when_full():
    cache = _LRUCache(max_entries=2)
    a = SemanticDetectorOutput(
        violation_detected=False, category="none", confidence=0.0, reasoning="a"
    )
    b = SemanticDetectorOutput(
        violation_detected=False, category="none", confidence=0.0, reasoning="b"
    )
    c = SemanticDetectorOutput(
        violation_detected=False, category="none", confidence=0.0, reasoning="c"
    )
    cache.put(1, a)
    cache.put(2, b)
    assert len(cache) == 2
    cache.put(3, c)  # evicts 1 (oldest)
    assert len(cache) == 2
    assert cache.get(1) is None
    assert cache.get(2) is b
    assert cache.get(3) is c


def test_lru_cache_get_promotes_to_most_recent():
    cache = _LRUCache(max_entries=2)
    a = SemanticDetectorOutput(
        violation_detected=False, category="none", confidence=0.0, reasoning="a"
    )
    b = SemanticDetectorOutput(
        violation_detected=False, category="none", confidence=0.0, reasoning="b"
    )
    c = SemanticDetectorOutput(
        violation_detected=False, category="none", confidence=0.0, reasoning="c"
    )
    cache.put(1, a)
    cache.put(2, b)
    # Touch 1 — should be most-recent now
    cache.get(1)
    cache.put(3, c)  # evicts 2 (now oldest), not 1
    assert cache.get(1) is a
    assert cache.get(2) is None
    assert cache.get(3) is c
