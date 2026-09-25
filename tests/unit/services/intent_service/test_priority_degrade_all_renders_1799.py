"""#1799 — all THREE priority renders must degrade honestly on a failed GitHub read.

`_get_priority_metadata` (canonical_handlers.py) signals a failed GitHub read with
the #1425 dict-flag sentinel: `{"has_github": True, "high_priority_issues": [],
"source_failed": True}`. Before this fix only ONE of its three consumers read the
flag:

- `_format_detailed_priorities` (GRANULAR) — checked `source_failed`, rendered the
  honest "I couldn't check your high-priority GitHub issues just now — try again
  in a moment." sentence. Correct pre-#1799.
- `_format_standard_priorities` (DEFAULT) — read `high_priority_issues` (empty from
  the failure), silently omitted the Urgent GitHub Issues section. The user could
  not tell the check failed — indistinguishable from a genuinely clean read.
- `_format_consolidated_priorities` (EMBEDDED) — read
  `len(high_priority_issues) == 0`, silently dropped the "+N urgent GitHub issues"
  clause. Same false all-clear (m-44).

The fix: all three now share one constant, `CanonicalHandlers._PRIORITY_SOURCE_
FAILED_NOTE`, and all three check `source_failed` BEFORE treating an empty list as
"none found". This file pins, per render:
  (a) source_failed=True -> the honest sentence, never a false "none"/"all clear"
  (b) a genuinely empty successful read -> the existing empty-state copy, unchanged
  (c) a populated read -> the issues still render, unchanged

A second test class patches `_get_priority_metadata` at its seam and drives the
real `_handle_priority_query` entry point for all three spatial patterns, so the
regression is pinned at the handler boundary too, not just the formatter unit.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.intent_service.canonical_handlers import CanonicalHandlers

# The exact honest sentence all three renders must share verbatim (#1799).
FAILED_NOTE = CanonicalHandlers._PRIORITY_SOURCE_FAILED_NOTE

SOURCE_FAILED_METADATA = {
    "has_github": True,
    "high_priority_issues": [],
    "source_failed": True,
}
GENUINE_EMPTY_METADATA = {
    "has_github": True,
    "high_priority_issues": [],
}
POPULATED_METADATA = {
    "has_github": True,
    "high_priority_issues": [
        {"number": 107, "title": "Fix login", "labels": ["P0"]},
    ],
}


def _user_context(organization=None):
    return type("U", (), {"organization": organization})()


class TestGranularSourceFailed:
    """_format_detailed_priorities (GRANULAR) — was already correct; pinned here
    so the shared-constant refactor can't silently change its behavior."""

    def _render(self, priority_metadata):
        return CanonicalHandlers()._format_detailed_priorities(
            priorities=["Ship the beta"],
            user_context=_user_context(),
            priority_metadata=priority_metadata,
        )

    def test_source_failed_renders_honest_note(self):
        out = self._render(SOURCE_FAILED_METADATA)
        assert FAILED_NOTE in out
        assert "no high-priority" not in out.lower()
        assert "all clear" not in out.lower()

    def test_genuine_empty_keeps_none_found(self):
        out = self._render(GENUINE_EMPTY_METADATA)
        assert "No high-priority" in out
        assert FAILED_NOTE not in out

    def test_populated_still_lists_issues(self):
        out = self._render(POPULATED_METADATA)
        assert "#107" in out
        assert FAILED_NOTE not in out
        assert "No high-priority" not in out


class TestStandardSourceFailed:
    """_format_standard_priorities (DEFAULT) — the #1799 fix: previously silently
    omitted the Urgent GitHub Issues section on a failed read."""

    def _render(self, priority_metadata):
        return CanonicalHandlers()._format_standard_priorities(
            priorities=["Ship the beta"],
            user_context=_user_context(),
            priority_metadata=priority_metadata,
        )

    def test_source_failed_renders_honest_note(self):
        out = self._render(SOURCE_FAILED_METADATA)
        assert FAILED_NOTE in out
        assert "no high-priority" not in out.lower()
        assert "all clear" not in out.lower()
        assert "Urgent GitHub Issues" not in out

    def test_genuine_empty_omits_section_without_claiming_failure(self):
        """A real empty read renders no Urgent GitHub Issues section (unchanged
        pre-#1799 behavior for this render) and does NOT claim a failure."""
        out = self._render(GENUINE_EMPTY_METADATA)
        assert "Urgent GitHub Issues" not in out
        assert FAILED_NOTE not in out

    def test_populated_still_lists_issues(self):
        out = self._render(POPULATED_METADATA)
        assert "#107" in out
        assert "Urgent GitHub Issues" in out
        assert FAILED_NOTE not in out


class TestEmbeddedSourceFailed:
    """_format_consolidated_priorities (EMBEDDED) — the #1799 fix: previously
    `len([]) == 0` silently dropped the "+N urgent GitHub issues" clause."""

    def _render(self, priority_metadata):
        return CanonicalHandlers()._format_consolidated_priorities(
            priorities=["Ship the beta", "Fix onboarding"],
            user_context=_user_context(),
            priority_metadata=priority_metadata,
        )

    def test_source_failed_renders_honest_note(self):
        out = self._render(SOURCE_FAILED_METADATA)
        assert FAILED_NOTE in out
        assert "urgent github issue" not in out.lower()
        assert "no high-priority" not in out.lower()
        assert "all clear" not in out.lower()
        # Base priority line still present -- degrade honestly, don't drop content.
        assert "Top priority: Ship the beta" in out

    def test_genuine_empty_keeps_terse_base_only(self):
        out = self._render(GENUINE_EMPTY_METADATA)
        assert out == "Top priority: Ship the beta (2 total)"
        assert FAILED_NOTE not in out

    def test_populated_still_shows_count(self):
        out = self._render(POPULATED_METADATA)
        assert "+ 1 urgent GitHub issues" in out
        assert FAILED_NOTE not in out


class TestSharedConstantNotThreeCopies:
    """Prefer one helper the three renders share over three copies (dispatch AC)."""

    def test_all_three_renders_use_the_identical_sentence(self):
        h = CanonicalHandlers()
        granular = h._format_detailed_priorities(["P"], _user_context(), SOURCE_FAILED_METADATA)
        standard = h._format_standard_priorities(["P"], _user_context(), SOURCE_FAILED_METADATA)
        embedded = h._format_consolidated_priorities(["P"], _user_context(), SOURCE_FAILED_METADATA)
        for rendered in (granular, standard, embedded):
            assert FAILED_NOTE in rendered


@pytest.fixture
def canonical_handlers():
    return CanonicalHandlers()


class TestPriorityQuerySeamSourceFailed1799:
    """Seam-level pins: patch `_get_priority_metadata` (the real failure surface)
    and drive `_handle_priority_query` for all three spatial patterns, so the
    regression is caught at the handler boundary, not only inside each formatter
    unit."""

    def _intent(self, pattern):
        intent = MagicMock()
        intent.spatial_context = {"pattern": pattern} if pattern else None
        return intent

    async def _run(self, canonical_handlers, pattern, priority_metadata):
        user_ctx = MagicMock()
        user_ctx.priorities = ["Ship the beta"]
        user_ctx.organization = None

        with (
            patch.object(
                canonical_handlers,
                "_detect_priority_recommendation_request",
                return_value=False,
            ),
            patch(
                "services.intent_service.canonical_handlers.user_context_service.get_user_context",
                new=AsyncMock(return_value=user_ctx),
            ),
            patch.object(
                canonical_handlers,
                "_get_priority_metadata",
                new=AsyncMock(return_value=priority_metadata),
            ),
        ):
            result = await canonical_handlers._handle_priority_query(
                self._intent(pattern), session_id="s-test", user_id="u-test"
            )
        return result["message"]

    @pytest.mark.asyncio
    async def test_granular_seam_source_failed(self, canonical_handlers):
        msg = await self._run(canonical_handlers, "GRANULAR", SOURCE_FAILED_METADATA)
        assert FAILED_NOTE in msg
        assert "no high-priority" not in msg.lower()

    @pytest.mark.asyncio
    async def test_standard_seam_source_failed(self, canonical_handlers):
        msg = await self._run(canonical_handlers, None, SOURCE_FAILED_METADATA)
        assert FAILED_NOTE in msg
        assert "Urgent GitHub Issues" not in msg

    @pytest.mark.asyncio
    async def test_embedded_seam_source_failed(self, canonical_handlers):
        msg = await self._run(canonical_handlers, "EMBEDDED", SOURCE_FAILED_METADATA)
        assert FAILED_NOTE in msg
        assert "urgent github issue" not in msg.lower()

    @pytest.mark.asyncio
    async def test_all_three_seams_genuine_empty_stay_silent_on_failure(self, canonical_handlers):
        for pattern in ("GRANULAR", None, "EMBEDDED"):
            msg = await self._run(canonical_handlers, pattern, GENUINE_EMPTY_METADATA)
            assert FAILED_NOTE not in msg, pattern

    @pytest.mark.asyncio
    async def test_all_three_seams_populated_render_issue(self, canonical_handlers):
        # GRANULAR and DEFAULT render the actual issue number; EMBEDDED's terse
        # register only ever shows a count (unchanged pre-#1799 behavior) -- so
        # only the shared "no failure note" assertion applies to all three.
        for pattern in ("GRANULAR", None):
            msg = await self._run(canonical_handlers, pattern, POPULATED_METADATA)
            assert "107" in msg, pattern
            assert FAILED_NOTE not in msg, pattern

        embedded_msg = await self._run(canonical_handlers, "EMBEDDED", POPULATED_METADATA)
        assert "1 urgent GitHub issue" in embedded_msg
        assert FAILED_NOTE not in embedded_msg
