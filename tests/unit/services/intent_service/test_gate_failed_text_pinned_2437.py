"""Issue 2437: every action's after-check reply from ``_github_gate_failed``, pinned.

The table below was generated from the code on origin/main BEFORE issue 2437 changed
``_github_gate_failed`` (the close and reopen stale lines now come from one constant per
verb, shared with the close/reopen gate). Every action's text must stay byte-identical.
Each row is (action, verb the call site passes, reason, the exact message).
"""

import re
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from services.integrations.github.read_failed import GitHubReadFailed
from services.intent_service.not_performed import (
    NotPerformed,
    was_not_performed,
    was_said_instead,
)
from services.mcp.consumer.connector import DegradationReason

REPO_ROOT = Path(__file__).resolve().parents[4]

GATE_FAILED_BEFORE = [
    (
        "shipped_this_week",
        "show you what shipped",
        "STALE_TOKEN",
        "Your GitHub connection isn't working anymore. Reconnect it in Settings → Integrations, and I can show you what shipped.",
    ),
    (
        "shipped_this_week",
        "show you what shipped",
        "UNREACHABLE",
        "I couldn't check your GitHub connection just now, so I can't show you what shipped yet. Try again in a moment; if it keeps failing, tell us.",
    ),
    (
        "stale_prs",
        "list your stale PRs",
        "STALE_TOKEN",
        "Your GitHub connection isn't working anymore. Reconnect it in Settings → Integrations, and I can list your stale PRs.",
    ),
    (
        "stale_prs",
        "list your stale PRs",
        "UNREACHABLE",
        "I couldn't check your GitHub connection just now, so I can't list your stale PRs yet. Try again in a moment; if it keeps failing, tell us.",
    ),
    (
        "review_issue",
        "show you that issue's details",
        "STALE_TOKEN",
        "Your GitHub connection isn't working anymore. Reconnect it in Settings → Integrations, and I can show you that issue's details.",
    ),
    (
        "review_issue",
        "show you that issue's details",
        "UNREACHABLE",
        "I couldn't check your GitHub connection just now, so I can't show you that issue's details yet. Try again in a moment; if it keeps failing, tell us.",
    ),
    (
        "close_issue",
        "close that issue",
        "STALE_TOKEN",
        "Your GitHub connection isn't working anymore. Reconnect it in Settings → Integrations, and I can close that issue.",
    ),
    (
        "close_issue",
        "close that issue",
        "UNREACHABLE",
        "I couldn't check your GitHub connection just now, so I can't close that issue yet. Nothing was changed. Try again in a moment; if it keeps failing, tell us.",
    ),
    (
        "reopen_issue",
        "reopen that issue",
        "STALE_TOKEN",
        "Your GitHub connection isn't working anymore. Reconnect it in Settings → Integrations, and I can reopen that issue.",
    ),
    (
        "reopen_issue",
        "reopen that issue",
        "UNREACHABLE",
        "I couldn't check your GitHub connection just now, so I can't reopen that issue yet. Nothing was changed. Try again in a moment; if it keeps failing, tell us.",
    ),
    (
        "comment_issue",
        "comment on that issue",
        "STALE_TOKEN",
        "Your GitHub connection isn't working anymore. Reconnect it in Settings → Integrations, and I can comment on that issue.",
    ),
    (
        "comment_issue",
        "comment on that issue",
        "UNREACHABLE",
        "I couldn't check your GitHub connection just now, so I can't comment on that issue yet. Nothing was changed. Try again in a moment; if it keeps failing, tell us.",
    ),
    (
        "list_prs",
        "list your pull requests",
        "STALE_TOKEN",
        "Your GitHub connection isn't working anymore. Reconnect it in Settings → Integrations, and I can list your pull requests.",
    ),
    (
        "list_prs",
        "list your pull requests",
        "UNREACHABLE",
        "I couldn't check your GitHub connection just now, so I can't list your pull requests yet. Try again in a moment; if it keeps failing, tell us.",
    ),
    (
        "create_issue",
        "create that issue",
        "STALE_TOKEN",
        "Your GitHub connection isn't working anymore. Reconnect it in Settings → Integrations, and I can create that issue. Nothing was added. If you meant a todo, say \"add a todo: …\" and I'll add it.",
    ),
    (
        "create_issue",
        "create that issue",
        "UNREACHABLE",
        "I couldn't check your GitHub connection just now, so I can't create that issue yet. Nothing was changed. Try again in a moment; if it keeps failing, tell us. If you meant a todo, say \"add a todo: …\" and I'll add it.",
    ),
    (
        "update_issue",
        "update that issue",
        "STALE_TOKEN",
        "Your GitHub connection isn't working anymore. Reconnect it in Settings → Integrations, and I can update that issue.",
    ),
    (
        "update_issue",
        "update that issue",
        "UNREACHABLE",
        "I couldn't check your GitHub connection just now, so I can't update that issue yet. Nothing was changed. Try again in a moment; if it keeps failing, tell us.",
    ),
]


def _svc():
    from services.intent.intent_service import IntentService

    svc = IntentService.__new__(IntentService)
    svc.logger = MagicMock()
    return svc


@pytest.mark.parametrize("action,verb,reason,message", GATE_FAILED_BEFORE)
def test_every_action_says_what_it_said_before(action, verb, reason, message):
    rf = GitHubReadFailed("x", DegradationReason[reason], detail=reason.lower())
    out = _svc()._github_gate_failed(rf, action, verb)
    assert out.message == message
    assert out.success is False
    assert out.intent_data["action"] == action
    assert out.intent_data["context"]["read_failed"] == DegradationReason[reason].value


def test_the_table_covers_every_call_site():
    """Each (action, verb) pair the service passes is in the table, with both reasons."""
    src = (REPO_ROOT / "services/intent/intent_service.py").read_text()
    sites = set(
        re.findall(r'self\._github_gate_failed\(\s*_gate_failed,\s*"(\w+)",\s*"([^"]+)"', src)
    )
    pinned = {(a, v) for a, v, _r, _m in GATE_FAILED_BEFORE}
    assert sites == pinned
    for pair in pinned:
        reasons = {r for a, v, r, _m in GATE_FAILED_BEFORE if (a, v) == pair}
        assert reasons == {"STALE_TOKEN", "UNREACHABLE"}


@pytest.mark.parametrize("action,verb,reason,message", GATE_FAILED_BEFORE)
def test_every_action_is_marked_degraded_not_said_instead(action, verb, reason, message):
    """Issue 2437 (Arch 09:06): a degrade under 2188. The learning handler skips it; it
    was already success=False, so it is not said-instead."""
    rf = GitHubReadFailed("x", DegradationReason[reason], detail=reason.lower())
    out = _svc()._github_gate_failed(rf, action, verb)
    assert out.intent_data["not_performed"] == NotPerformed.DEGRADED
    assert was_not_performed(out)
    assert not was_said_instead(out)
