"""Tests for LLMClient.complete() output-filter wrap (Issue #1017 Phase 2.2).

Scope: verify the regenerate-on-violation flow and audit-decorator wiring.
Mocks `_complete_raw` to avoid real LLM calls; uses a real OutputFilter
instance (with mock BoundaryEnforcer where needed) so the filter logic
itself is exercised end-to-end with the decorator.
"""

from __future__ import annotations

from dataclasses import dataclass
from unittest.mock import AsyncMock, patch

import pytest

from services.ethics.output_filter import (
    Action,
    CANNED_VIOLATION_RESPONSE,
    OutputFilter,
    REDACTED_TOKEN,
    Severity,
)


@dataclass
class _MockBoundaryDecision:
    is_violation: bool = False
    violation_type: str = ""


class _MockBoundaryEnforcer:
    """Mock that returns predetermined violation states across calls.

    Set `will_flag_sequence` to a list of bools; each call to
    enforce_boundaries pops the next one. Lets tests script first-call-fails
    then retry-passes (or vice-versa).
    """

    def __init__(self, will_flag_sequence: list[bool] | None = None):
        self._sequence = list(will_flag_sequence or [])
        self.calls = 0

    async def enforce_boundaries(self, message, context=None, session_id=None):
        self.calls += 1
        flag = self._sequence.pop(0) if self._sequence else False
        return _MockBoundaryDecision(is_violation=flag, violation_type="harassment")


def _build_client_with_filter(boundary_enforcer=None, raw_responses: list[str] | None = None):
    """Build an LLMClient with a real OutputFilter + a mocked _complete_raw.

    The `raw_responses` list scripts what `_complete_raw` returns on
    successive calls — first call gets index 0, retry gets index 1, etc.
    """
    from services.llm.clients import LLMClient

    output_filter = OutputFilter(boundary_enforcer=boundary_enforcer)

    # Don't actually run client init (no real API keys in test); patch it out.
    with patch.object(LLMClient, "_init_clients", lambda self: None):
        client = LLMClient(output_filter=output_filter)

    responses = list(raw_responses or [])

    # AsyncMock with side_effect=list returns successive items per call.
    client._complete_raw = AsyncMock(side_effect=responses if responses else [""])
    return client


# ============================================================================
# Backward-compat: no filter injected → existing behavior
# ============================================================================


class TestBackwardCompatibility:
    @pytest.mark.asyncio
    async def test_no_filter_returns_raw_response(self):
        from services.llm.clients import LLMClient

        with patch.object(LLMClient, "_init_clients", lambda self: None):
            client = LLMClient()  # no output_filter
        client._complete_raw = AsyncMock(return_value="Raw LLM response")

        result = await client.complete(task_type="conversation", prompt="hi")

        assert result == "Raw LLM response"
        client._complete_raw.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_no_filter_no_pii_redaction(self):
        """When output_filter is None, even PII passes through unredacted
        (the existing behavior before #1017 — backward compat)."""
        from services.llm.clients import LLMClient

        with patch.object(LLMClient, "_init_clients", lambda self: None):
            client = LLMClient()
        client._complete_raw = AsyncMock(return_value="Email is alice@example.com here.")

        result = await client.complete(task_type="conversation", prompt="hi")

        assert "alice@example.com" in result
        assert REDACTED_TOKEN not in result


# ============================================================================
# With filter: clean content passes through
# ============================================================================


class TestWithFilterClean:
    @pytest.mark.asyncio
    async def test_clean_content_passes_through(self):
        client = _build_client_with_filter(raw_responses=["The roadmap looks healthy."])

        result = await client.complete(task_type="conversation", prompt="hi")

        assert result == "The roadmap looks healthy."

    @pytest.mark.asyncio
    async def test_internal_task_type_skips_filter(self):
        """intent_classification stays internal-profile; PII NOT redacted
        because internal profile = log-only, no transform."""
        client = _build_client_with_filter(
            raw_responses=['{"action": "create_issue", "email": "alice@example.com"}']
        )

        result = await client.complete(task_type="intent_classification", prompt="hi")

        assert "alice@example.com" in result  # internal profile passes through
        assert REDACTED_TOKEN not in result


# ============================================================================
# With filter: PII / secret redaction
# ============================================================================


class TestWithFilterRedaction:
    @pytest.mark.asyncio
    async def test_pii_redacted_in_place(self):
        client = _build_client_with_filter(raw_responses=["Reach me at alice@example.com please."])

        result = await client.complete(task_type="conversation", prompt="hi")

        assert "alice@example.com" not in result
        assert REDACTED_TOKEN in result

    @pytest.mark.asyncio
    async def test_secret_redacted(self):
        client = _build_client_with_filter(
            raw_responses=["Token: ghp_AAAAAABBBBBBCCCCCCDDDDDDEEEEEEFFFFFF"]
        )

        result = await client.complete(task_type="conversation", prompt="hi")

        assert "ghp_AAAAAABBBBBBCCCCCCDDDDDDEEEEEEFFFFFF" not in result
        assert REDACTED_TOKEN in result


# ============================================================================
# Regenerate-on-violation flow
# ============================================================================


class TestRegenerateOnViolation:
    @pytest.mark.asyncio
    async def test_first_violates_retry_passes(self):
        """First LLM response triggers boundary violation; retry produces
        clean content; user sees the retry (not canned)."""
        enforcer = _MockBoundaryEnforcer(will_flag_sequence=[True, False])
        client = _build_client_with_filter(
            boundary_enforcer=enforcer,
            raw_responses=[
                "Bad first response (mock-flagged).",
                "Clean retry response.",
            ],
        )

        result = await client.complete(task_type="conversation", prompt="hi")

        assert result == "Clean retry response."
        assert enforcer.calls == 2  # one per attempt
        assert client._complete_raw.await_count == 2

    @pytest.mark.asyncio
    async def test_first_violates_retry_also_violates_returns_canned(self):
        """Both attempts violate; user sees the canned response."""
        enforcer = _MockBoundaryEnforcer(will_flag_sequence=[True, True])
        client = _build_client_with_filter(
            boundary_enforcer=enforcer,
            raw_responses=[
                "Bad first response.",
                "Bad retry response.",
            ],
        )

        result = await client.complete(task_type="conversation", prompt="hi")

        assert result == CANNED_VIOLATION_RESPONSE
        assert enforcer.calls == 2
        assert client._complete_raw.await_count == 2

    @pytest.mark.asyncio
    async def test_regenerate_disabled_returns_canned_immediately(self):
        """With regenerate_on_violation=False, no retry; canned on first violation."""
        enforcer = _MockBoundaryEnforcer(will_flag_sequence=[True])
        client = _build_client_with_filter(
            boundary_enforcer=enforcer,
            raw_responses=["Bad first response."],
        )

        result = await client.complete(
            task_type="conversation",
            prompt="hi",
            regenerate_on_violation=False,
        )

        assert result == CANNED_VIOLATION_RESPONSE
        assert enforcer.calls == 1
        assert client._complete_raw.await_count == 1

    @pytest.mark.asyncio
    async def test_no_violation_no_retry(self):
        """Clean first response → no retry needed."""
        enforcer = _MockBoundaryEnforcer(will_flag_sequence=[False])
        client = _build_client_with_filter(
            boundary_enforcer=enforcer,
            raw_responses=["Clean first response."],
        )

        result = await client.complete(task_type="conversation", prompt="hi")

        assert result == "Clean first response."
        assert enforcer.calls == 1
        assert client._complete_raw.await_count == 1


# ============================================================================
# User/session context propagation
# ============================================================================


class TestContextPropagation:
    @pytest.mark.asyncio
    async def test_user_id_and_session_id_passed_to_filter(self):
        """user_id + session_id flow through to OutputFilter for audit."""
        client = _build_client_with_filter(raw_responses=["Clean content."])

        # Spy on the filter's filter() method.
        original_filter = client._output_filter.filter
        seen_kwargs = {}

        async def spy_filter(**kwargs):
            seen_kwargs.update(kwargs)
            return await original_filter(**kwargs)

        client._output_filter.filter = spy_filter

        await client.complete(
            task_type="conversation",
            prompt="hi",
            user_id="user-1",
            session_id="sess-1",
        )

        assert seen_kwargs.get("user_id") == "user-1"
        assert seen_kwargs.get("session_id") == "sess-1"
        assert seen_kwargs.get("task_type") == "conversation"
