"""#1331/#1333 — unwired WRITE honest-decline COPY (no confabulation).

History: #1331 fixed the confabulation trust-breaker (an unwired write like
`create_milestone` reached the conversational floor, which confabulated "created ✓"
without writing). The first fix was a hand-maintained `UNWIRED_WRITE_ACTIONS` list
fanned onto the action-dispatch rail. #1333 (Arch-ruled 2026-06-30) replaced that
LIST with a DERIVED rule: any unwired EXECUTION action reaches
`_handle_execution_intent`'s else-branch and deterministically honest-declines —
no list, no registration, no `_handle_unwired_write` rail handler.

So the *behavioral* coverage (an unwired action declines, never confabulates, never
hits the floor — including a novel action the list never had) now lives in
`test_unwired_execution_derived_decline_1333.py`. THIS file covers what survives:
the curated decline-COPY map (`unwired_writes.UNWIRED_WRITE_DECLINES` /
`get_unwired_write_decline`) — the *copy*, not the *trigger*.
"""

import pytest

from services.intent_service.unwired_writes import (
    GENERIC_UNWIRED_WRITE_DECLINE,
    UNWIRED_WRITE_DECLINES,
    get_unwired_write_decline,
)

# Substrings that would indicate a CONFABULATED write-success (the #1331 failure mode).
_FABRICATED_SUCCESS_MARKERS = [
    "✓", "✅", "created", "added", "done!", "successfully", "i've created", "i have created",
]
# Substrings that indicate an HONEST decline.
_HONEST_DECLINE_MARKERS = ["can't", "cannot", "can not", "not yet", "yet"]


class TestCuratedDeclineCopy:
    """The curated per-action copy declines honestly and never confabulates success."""

    def test_create_milestone_has_curated_copy(self):
        # The confirmed #1331 case keeps its specific, nicer wording.
        assert "create_milestone" in UNWIRED_WRITE_DECLINES
        msg = get_unwired_write_decline("create_milestone").lower()
        assert "milestone" in msg
        assert "github" in msg  # points to the alternative (#1331 tone)

    @pytest.mark.parametrize("action", sorted(UNWIRED_WRITE_DECLINES.keys()))
    def test_curated_copy_declines_without_confabulation(self, action):
        msg = get_unwired_write_decline(action).lower()
        assert any(m in msg for m in _HONEST_DECLINE_MARKERS), (
            f"{action}: not an honest decline: {msg!r}"
        )
        for marker in _FABRICATED_SUCCESS_MARKERS:
            assert marker not in msg, f"{action}: confabulated-success marker {marker!r}: {msg!r}"

    def test_unknown_action_falls_back_to_generic_honest_decline(self):
        """A novel/unlisted action (the drift gap) still gets an honest, non-confabulating
        decline via the generic fallback — so 'not on the list' never means 'confabulate'."""
        msg = get_unwired_write_decline("archive_repository")
        assert msg == GENERIC_UNWIRED_WRITE_DECLINE
        low = msg.lower()
        assert any(m in low for m in _HONEST_DECLINE_MARKERS)
        for marker in _FABRICATED_SUCCESS_MARKERS:
            assert marker not in low

    def test_wired_writes_have_no_unwired_copy(self):
        """Actions with real handlers must NOT be in the curated unwired-copy map
        (they behave honestly via their handlers; they're not unwired)."""
        for wired in ["create_issue", "create_ticket", "update_issue", "generate_report"]:
            assert wired not in UNWIRED_WRITE_DECLINES, (
                f"{wired} is WIRED — must not have unwired-decline copy"
            )
