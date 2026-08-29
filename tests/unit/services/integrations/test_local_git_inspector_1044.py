"""Tests for the local-git inspector + pre-classifier wiring (#1044).

Covers:
- LocalGitInspector returns a structured LocalGitStatus
- Error states (not a git repo) surface via .error field, never raise
- Pre-classifier patterns: "what branch are we on?" routes to
  local_git_status_query (NOT to list_branches_query — the GitHub-remote
  handler — which it would have done before patterns were added).
- Handler exists at the dispatch level
"""

import os
import tempfile
from pathlib import Path

import pytest

from services.integrations.local_git import LocalGitInspector, LocalGitStatus

# Inspector ---------------------------------------------------------------


def test_inspector_returns_local_git_status_for_real_repo() -> None:
    """When run inside a real git repo (this worktree), the inspector
    returns a populated status."""
    status = LocalGitInspector().get_status()
    # We're running inside a git worktree, so error should be None
    assert status.error is None, f"Unexpected error: {status.error}"
    assert status.current_branch is not None
    # Working-tree state should be a bool (we know clean/dirty)
    assert status.is_clean in (True, False)


def test_inspector_error_state_for_non_git_path() -> None:
    """When given a non-git path, returns structured error — does NOT raise."""
    with tempfile.TemporaryDirectory() as tmp:
        # tmp dir is not a git repo
        inspector = LocalGitInspector(repo_path=tmp)
        status = inspector.get_status()
        assert (
            status.error is not None
        ), "Non-git path must surface an error in the status, not raise"
        # When error is set, observation fields are None
        assert status.current_branch is None
        assert status.is_clean is None


def test_inspector_status_dataclass_is_immutable() -> None:
    """LocalGitStatus is a frozen dataclass — bounded observation, no mutation."""
    s = LocalGitStatus(current_branch="main", is_clean=True)
    with pytest.raises(Exception):  # FrozenInstanceError
        s.current_branch = "other"  # type: ignore[misc]


# Pre-classifier ----------------------------------------------------------


def test_what_branch_singular_routes_to_local_git() -> None:
    """The canonical 'what branch are we on?' must route to the local-git
    handler, NOT to the GitHub list_branches handler."""
    from services.intent_service.pre_classifier import PreClassifier

    intent = PreClassifier.pre_classify("what branch are we on?")
    assert intent is not None, "PreClassifier must match this canonical phrase"
    assert intent.action == "local_git_status_query", (
        f"Expected local_git_status_query, got {intent.action}. "
        f"This phrase was historically captured by list_branches_query "
        f"(GitHub-remote); #1044 fixes that."
    )


def test_current_branch_singular_routes_to_local_git() -> None:
    """'What's the current branch?' (singular) routes local; 'current branches'
    (plural) stays GitHub-remote."""
    from services.intent_service.pre_classifier import PreClassifier

    intent = PreClassifier.pre_classify("what's the current branch")
    assert intent is not None
    assert intent.action == "local_git_status_query"


def test_uncommitted_changes_routes_to_local_git() -> None:
    from services.intent_service.pre_classifier import PreClassifier

    intent = PreClassifier.pre_classify("any uncommitted changes?")
    assert intent is not None
    assert intent.action == "local_git_status_query"


def test_git_status_routes_to_local_git() -> None:
    from services.intent_service.pre_classifier import PreClassifier

    intent = PreClassifier.pre_classify("git status")
    assert intent is not None
    assert intent.action == "local_git_status_query"


def test_show_branches_does_not_route_to_local_git() -> None:
    """Regression check: GitHub-remote phrasing ('show branches') must NOT be
    captured by the new local-git patterns. Whether it routes to
    list_branches_query directly or via LLM-classifier fallback is out of
    scope — the regression check here is just that local-git didn't get
    too greedy and grab it."""
    from services.intent_service.pre_classifier import PreClassifier

    for msg in ["show branches", "list branches", "active branches"]:
        intent = PreClassifier.pre_classify(msg)
        action = intent.action if intent else None
        assert (
            action != "local_git_status_query"
        ), f"Local-git patterns are too greedy: captured {msg!r} (→ {action})"


# Dispatch ---------------------------------------------------------------


def test_handler_exists_at_dispatch_level() -> None:
    """Verify the intent_service has the handler attached."""
    from services.intent.intent_service import IntentService

    # The method must exist on the class
    assert hasattr(
        IntentService, "_handle_local_git_status_query"
    ), "_handle_local_git_status_query must be defined on IntentService"


def test_dispatch_table_routes_local_git_action() -> None:
    """The action-dispatch rail must route local_git_status_query.

    #1124: QUERY-category routing moved off _handle_query_intent's elif chain
    onto the action-dispatch rail. The local-git routing now lives in the rail's
    entry-point registration in workflow_entries.py: an entry point built from
    _handle_local_git_status_query is registered against the local_git_status[_query]
    action keys. The invariant (this action routes to that handler) is unchanged —
    only its location moved.
    """
    from pathlib import Path

    src = Path("services/intent_service/workflow_entries.py").read_text()
    assert "local_git_status_query" in src, "Dispatch table must include local_git_status_query"
    assert (
        "_handle_local_git_status_query" in src
    ), "Dispatch table must call _handle_local_git_status_query"
