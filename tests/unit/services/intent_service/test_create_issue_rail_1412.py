"""#1412 — create_issue is reachable via the rail, not elif-only (mode-4 fix).

The live primary beta write path. Same gap #1411 fixed for update_issue: fully
implemented (_handle_create_issue) but dispatched only via the mapped_action elif
(surface 4) — registry/rail/prompt-invisible, LLM-emission-dependent, ratchet-blind.
Migrated onto the rail + ACTION_REGISTRY (elif kept as an additive backstop).
"""

from services.intent_service.action_registry import ACTION_REGISTRY, ACTION_TO_VERB, Verb
from services.intent_service.workflow_dispatcher import get_action_workflows
from services.intent_service.workflow_entries import register_default_workflows

_ALIASES = [
    "create_issue",
    "create_github_issue",
    "create_item",
    "create_ticket",
    "make_github_issue",
    "new_github_issue",
]


class TestCreateIssueReachability:
    def test_registry_carries_create_issue_canonical(self):
        canon = {action for (_cat, action) in ACTION_REGISTRY}
        assert "create_issue" in canon

    def test_create_issue_maps_to_a_verb(self):
        assert ACTION_TO_VERB.get("create_issue") is Verb.CREATE

    def test_all_aliases_dispatch_via_the_rail(self):
        register_default_workflows()
        keys = get_action_workflows().keys()
        for alias in _ALIASES:
            assert alias in keys, f"{alias!r} must be rail-dispatchable (mode-4 fix)"

    def test_aliases_share_one_entry_point(self):
        register_default_workflows()
        wf = get_action_workflows()
        entries = {id(wf[a]) for a in _ALIASES}
        assert len(entries) == 1, "all create_issue aliases must share one entry"
