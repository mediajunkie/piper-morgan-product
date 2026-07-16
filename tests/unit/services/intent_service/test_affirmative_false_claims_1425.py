"""#1425 (F2) — status/agenda handlers must not assert emptiness when the source FAILED.

The false-claim family: a swallowed source error rendered as "there is nothing"
(about the user's own work) instead of "I couldn't check." The fix distinguishes
source-FAILED from source-EMPTY and degrades honestly (ADR-060 / #1331 / #1414 model).

This file grows one class per handler as #1425 is fixed. Handler 1
(_get_priority_metadata → _format_detailed_priorities) landed first.
"""

from services.intent_service.canonical_handlers import CanonicalHandlers


class TestPriorityMetadataSourceFailed:
    """_get_priority_metadata swallow → _format_detailed_priorities render."""

    def _render(self, priority_metadata):
        return CanonicalHandlers()._format_detailed_priorities(
            priorities=["Ship the beta"],  # non-empty so we reach the metadata branch
            user_context=type("U", (), {"organization": None})(),
            priority_metadata=priority_metadata,
        )

    def test_source_failed_renders_honest_not_false_empty(self):
        """The load-bearing assertion: on source failure, be honest — never claim
        'no high-priority issues found' (which would be false while P0/P1s exist)."""
        out = self._render({"has_github": True, "high_priority_issues": [], "source_failed": True})
        assert "couldn't check" in out.lower()
        assert "No high-priority" not in out  # the false-claim must NOT appear

    def test_genuine_empty_still_says_none_found(self):
        """A real empty (source OK, no P0/P1s) keeps the honest 'none found' claim."""
        out = self._render({"has_github": True, "high_priority_issues": []})
        assert "No high-priority" in out
        assert "couldn't check" not in out.lower()

    def test_populated_still_lists_issues(self):
        """The happy path is unchanged — real issues still render."""
        out = self._render({
            "has_github": True,
            "high_priority_issues": [{"number": 107, "title": "Fix login", "labels": ["P0"]}],
        })
        assert "#107" in out
        assert "couldn't check" not in out.lower()
        assert "No high-priority" not in out
