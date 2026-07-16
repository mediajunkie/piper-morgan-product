"""#1411 — update_issue is reachable via the rail, not elif-only (mode-4 fix).

_handle_update_issue is fully implemented but was dispatched only via the
`mapped_action` elif (surface 4) — registry/rail/prompt-invisible, so it depended
on the LLM emitting the right action and was invisible to the #1283 ratchet. This
registers it on the rail + ACTION_REGISTRY (the elif stays as an additive backstop).
"""

from services.intent_service.action_registry import ACTION_REGISTRY
from services.intent_service.workflow_dispatcher import get_action_workflows
from services.intent_service.workflow_entries import register_default_workflows

_ALIASES = ["update_issue", "modify_issue", "update_ticket", "update_github_issue"]


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
