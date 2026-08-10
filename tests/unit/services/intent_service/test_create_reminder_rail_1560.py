"""#1560 — create_reminder is reachable via the #1124 action-dispatch rail,
not elif-only (the structural half of the #1517 capability-gaslighting
incident).

Before this fix create_reminder's ONLY dispatch was the legacy
`elif mapped_action == "create_reminder"` inside `_handle_execution_intent`
(intent_service.py), which is reached only when the classifier emits category
EXECUTION. A correct create_reminder emission under any OTHER category
(TEMPORAL, GUIDANCE, ...) fell past every dispatch surface to the floor —
which then improvised a capability denial (#1517). The rail check in
process_intent (`intent.action in get_action_workflows()`) runs BEFORE
category routing and never consults intent.category, so a rail entry makes
dispatch category-independent by construction.

The entry reuses `run_todo_query_workflow` — the existing execution-side
adapter that delegates to `_handle_execution_intent(intent, None, session_id,
user_id)` — so the rail reaches the SAME handler chain the elif fronts
(ActionMapper -> todo_handlers.handle_create_reminder); no duplicated logic.

Layer honesty (m-43): these are registration/wiring tests plus a
dispatch-layer test against a stub IntentService. They do not drive the full
process_intent pipeline or a live classifier.
"""

import pytest

from services.domain.models import Intent
from services.shared_types import EffectClass, IntentCategory
from services.intent_service.workflow_dispatcher import (
    dispatch_workflow,
    get_action_workflows,
    wired_chat_actions,
)
from services.intent_service.workflow_entries import register_default_workflows

# The ActionMapper raw-emission aliases that map to create_reminder (#284/#1426);
# all three must hit the rail so a non-EXECUTION emission of any of them
# dispatches instead of flooring.
_ALIASES = ["create_reminder", "set_reminder", "add_reminder"]


class TestCreateReminderRailRegistration:
    def test_all_aliases_dispatch_via_the_rail(self):
        register_default_workflows()
        keys = get_action_workflows().keys()
        for alias in _ALIASES:
            assert alias in keys, (
                f"{alias!r} must be rail-dispatchable — elif-only dispatch is "
                f"category-dependent (#1560 / #1517 structural gap)"
            )

    def test_aliases_share_one_entry_point(self):
        register_default_workflows()
        wf = get_action_workflows()
        entries = {id(wf[a]) for a in _ALIASES}
        assert len(entries) == 1, "all create_reminder aliases must share one entry"

    def test_entry_declares_write_effect(self):
        # handle_create_reminder persists a reminder row via
        # todo_service.create_todo — a DB WRITE (recoverable, not DESTRUCTIVE).
        register_default_workflows()
        entry = get_action_workflows()["create_reminder"]
        assert entry.effect == EffectClass.WRITE
        assert entry.action_triggered is True


class TestCreateReminderCategoryIndependence:
    """The rail dispatches by intent.action alone; category must not matter."""

    class _StubIntentService:
        """Records what the rail entry point invokes — proving the entry
        reaches _handle_execution_intent (the same handler chain the legacy
        elif fronts) without duplicating handler logic."""

        def __init__(self):
            self.calls = []

        async def _handle_execution_intent(self, intent, workflow, session_id, user_id=None):
            self.calls.append((intent, workflow, session_id, user_id))
            return "SENTINEL_RESULT"

    @pytest.mark.asyncio
    @pytest.mark.parametrize("category", [IntentCategory.TEMPORAL, IntentCategory.GUIDANCE])
    async def test_wrong_category_emission_still_reaches_execution_handler(self, category):
        register_default_workflows()
        stub = self._StubIntentService()
        intent = Intent(
            category=category,  # the #1517 shape: right action, wrong category
            action="create_reminder",
            context={"original_message": "remind me at 3pm tomorrow to review the PR"},
        )
        # Precondition of the fix: the rail key exists regardless of category.
        assert intent.action in get_action_workflows()

        result = await dispatch_workflow(
            workflow_type=intent.action,
            session_id="session-1560",
            user_id="user-1560",
            context={"intent": intent, "workflow_id": None, "intent_service": stub},
        )

        assert result == "SENTINEL_RESULT"
        assert len(stub.calls) == 1
        called_intent, workflow, session_id, user_id = stub.calls[0]
        assert called_intent is intent
        assert workflow is None  # #883/#1094: no pre-created workflow
        assert session_id == "session-1560"
        assert user_id == "user-1560"


class TestCapabilityManifestUnaffected:
    """#1517 guard: the rail entry must not double-count create_reminder in
    wired_chat_actions() — it now appears on BOTH derivation surfaces (rail +
    ActionMapper targets) and the set-union must dedup it to one."""

    def test_create_reminder_listed_exactly_once(self):
        wired = wired_chat_actions()
        assert wired.count("create_reminder") == 1
