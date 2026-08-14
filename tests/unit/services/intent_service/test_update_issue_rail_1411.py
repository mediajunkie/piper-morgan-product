"""#1411 — update_issue is reachable via the rail, not elif-only (mode-4 fix).

_handle_update_issue is fully implemented but was dispatched only via the
`mapped_action` elif (surface 4) — registry/rail/prompt-invisible, so it depended
on the LLM emitting the right action and was invisible to the #1283 ratchet. This
registers it on the rail + ACTION_REGISTRY, and (migration completion) RETIRES the
legacy elif branch in `_handle_execution_intent`: the rail is the single dispatch
surface for update_issue. B3 Stage-0 referent resolution (classifier.py
`_resolve_issue_referent`) emits `update_issue` directly and rides the same rail
key — covered by the reachability tests below.

Why there is NO CHAT_POINTERS ledger row for update_issue: the #1433 ledger is
exact-match against DERIVED product surfaces (ui.py page routes + connectable
integrations + decline-copy capabilities) — both missing AND stale rows fail the
ratchet, and update_issue is none of those surfaces, so a row would fail as
stale. A POINTER utterance also could not resolve deterministically: update
phrasings need the LLM classifier (or session-relative B3 ledger state the
static resolver deliberately doesn't model), which fails at authoring time.
Reachability enforcement for update_issue lives here + the registry-outward
lint (test_routing_vocabulary_1283) instead.
"""

import re
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from services.intent_service.action_registry import ACTION_REGISTRY
from services.intent_service.workflow_dispatcher import (
    dispatch_workflow,
    get_action_workflows,
)
from services.intent_service.workflow_entries import register_default_workflows

_ALIASES = ["update_issue", "modify_issue", "update_ticket", "update_github_issue"]

_INTENT_SERVICE_PY = Path(__file__).parents[4] / "services" / "intent" / "intent_service.py"


class TestUpdateIssueReachability:
    def test_registry_carries_update_issue_canonical(self):
        canon = {action for (_cat, action) in ACTION_REGISTRY}
        assert "update_issue" in canon

    def test_all_aliases_dispatch_via_the_rail(self):
        register_default_workflows()
        keys = get_action_workflows().keys()
        for alias in _ALIASES:
            assert alias in keys, f"{alias!r} must be rail-dispatchable (mode-4 fix)"

    def test_aliases_share_one_entry_point(self):
        """All four raw names the classifier can emit resolve to the same handler."""
        register_default_workflows()
        wf = get_action_workflows()
        entries = {id(wf[a]) for a in _ALIASES}
        assert len(entries) == 1, "all update_issue aliases must share one entry"


class TestUpdateIssueElifRetired:
    """Migration completion: the rail is the ONLY dispatch surface for
    update_issue — the legacy `elif mapped_action in ["update_issue", ...]`
    branch in `_handle_execution_intent` is removed, not kept as a backstop.

    Rationale: the elif was reachable only when rail dispatch returned None,
    which for a registered key means the handler RAISED (dispatch_workflow
    catches and returns None) — so the "backstop" was really a silent RETRY of
    a failed GitHub WRITE (double-mutation hazard). Post-removal, that edge
    falls to the #1333 honest-decline else-branch instead.
    """

    def _elif_tokens(self) -> set:
        """Same derivation as TestForwardGuardExecutionCohort / the #1433
        ratchet's _elif_tokens: the tokens _handle_execution_intent branches on."""
        src = _INTENT_SERVICE_PY.read_text()
        tokens = set(re.findall(r'mapped_action\s*==\s*"([a-z_]+)"', src))
        for group in re.findall(r"mapped_action\s+in\s+\[([^\]]+)\]", src):
            tokens |= set(re.findall(r'"([a-z_]+)"', group))
        return tokens

    def test_update_issue_is_not_elif_dispatched(self):
        tokens = self._elif_tokens()
        leftovers = {"update_issue", "update_ticket"} & tokens
        assert not leftovers, (
            f"update_issue must dispatch via the rail ONLY; legacy elif tokens "
            f"remain in _handle_execution_intent: {sorted(leftovers)} (#1411)"
        )


class TestUpdateIssueRailDispatch:
    """Behavioral: the rail entry actually invokes _handle_update_issue with the
    handler's (intent, workflow_id, session_id, user_id) shape — not just key
    membership. session_id threaded since the #1411 clarify-first ask (2026-08-13):
    the unmapped-status-value ask binds via the session-keyed #846 offer store."""

    @pytest.mark.asyncio
    async def test_rail_dispatch_invokes_handler(self):
        register_default_workflows()
        expected = object()
        svc = SimpleNamespace(_handle_update_issue=AsyncMock(return_value=expected))
        intent = SimpleNamespace(action="update_issue")
        result = await dispatch_workflow(
            workflow_type="update_issue",
            session_id="s-1",
            user_id="u-1",
            context={"intent": intent, "workflow_id": "wf-1", "intent_service": svc},
        )
        svc._handle_update_issue.assert_awaited_once_with(intent, "wf-1", "s-1", "u-1")
        assert result is expected

    @pytest.mark.asyncio
    async def test_alias_dispatch_reaches_same_handler(self):
        """A classifier paraphrase alias (modify_issue) rides the same entry."""
        register_default_workflows()
        svc = SimpleNamespace(_handle_update_issue=AsyncMock(return_value=object()))
        intent = SimpleNamespace(action="modify_issue")
        await dispatch_workflow(
            workflow_type="modify_issue",
            session_id="s-1",
            user_id="u-1",
            context={"intent": intent, "workflow_id": "wf-2", "intent_service": svc},
        )
        svc._handle_update_issue.assert_awaited_once_with(intent, "wf-2", "s-1", "u-1")
