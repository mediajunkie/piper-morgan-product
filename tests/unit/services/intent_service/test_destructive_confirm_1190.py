"""#1190 [MVP] — multi-turn confirmation gate for destructive issue mutations.

PM ruling (decisions.log 2026-08-10 ~10:55): close_issue / reopen_issue are
DESTRUCTIVE — the point is BLAST-RADIUS protection (a closed Beta Blocker
disappears from every board/query that filters on open state, and the 2026-07
auto-close incident closed a live Beta Blocker from a commit message).
Recoverability ("reversible via reopen") was the old WRITE rationale and is
explicitly retired by the ruling.

These are the FIRST DESTRUCTIVE rail entries — the tier goes from
tests-only (synthetic entries in test_workflow_dispatcher.py) to live.
"""

import pytest

from services.intent_service.workflow_dispatcher import get_action_workflows
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import EffectClass

CLOSE_ALIASES = ("close_issue", "close_issue_query")
REOPEN_ALIASES = ("reopen_issue", "reopen_issue_query")


class TestDestructiveEnumFlips1190:
    """Part 1: the enum flips. RED while close/reopen are still WRITE."""

    def test_close_issue_entries_are_destructive(self):
        register_default_workflows()
        wf = get_action_workflows()
        for alias in CLOSE_ALIASES:
            assert wf[alias].effect == EffectClass.DESTRUCTIVE, (
                f"{alias} must be DESTRUCTIVE (PM ruling 2026-08-10: "
                "blast-radius protection, not recoverability)"
            )

    def test_reopen_issue_entries_are_destructive(self):
        register_default_workflows()
        wf = get_action_workflows()
        for alias in REOPEN_ALIASES:
            assert wf[alias].effect == EffectClass.DESTRUCTIVE, (
                f"{alias} must be DESTRUCTIVE (PM ruling 2026-08-10)"
            )

    def test_destructive_entries_derive_needs_confirm(self):
        """The #1190 gate keys off needs_confirm — the flip must make the
        derived predicate true (never a re-derivation from names)."""
        register_default_workflows()
        wf = get_action_workflows()
        for alias in CLOSE_ALIASES + REOPEN_ALIASES:
            assert wf[alias].needs_confirm is True
            assert wf[alias].destructive_hint is True
            assert wf[alias].needs_consent is True  # destructive ⊂ write

    def test_destructive_tier_scope_with_denominator(self):
        """m-44: state the denominator. Exactly the close/reopen pair (2
        entries, 4 alias keys) is DESTRUCTIVE on the action rail today — this
        is the honest update of the previous zero-DESTRUCTIVE registry state,
        not a deletion of it. If a new action legitimately joins the tier,
        update this set in the same commit that flips its entry."""
        register_default_workflows()
        wf = get_action_workflows()
        destructive_keys = {
            key for key, entry in wf.items() if entry.effect == EffectClass.DESTRUCTIVE
        }
        assert destructive_keys == set(CLOSE_ALIASES) | set(REOPEN_ALIASES), (
            f"Destructive rail keys drifted: {sorted(destructive_keys)}. "
            "PM ruled exactly close/reopen destructive on 2026-08-10; a new "
            "destructive entry needs its own ruling + this set updated."
        )
