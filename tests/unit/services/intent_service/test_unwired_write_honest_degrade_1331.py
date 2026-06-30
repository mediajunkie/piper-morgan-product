"""Tests for #1331 — honest-degrade unwired WRITE intents (no confabulation).

The bug (#1331, verified in UAT): a user asks Piper to perform a WRITE in chat
("add a milestone to my default repo"). The LLM classifier recognizes the action
(`create_milestone`, a free-form action — there is no CREATE verb) but NO handler
or WorkflowEntry exists, so the action falls through to the conversational floor
(the LLM), which CONFABULATES a success message ("Milestone created ✓") with full
details — while NO GitHub write ever happens. That is a trust-property violation.

The fix (honest-degrade FLOOR, NOT real writes — #1322 Q3 owns real writes): for
each recognized-but-unwired WRITE action, register an action-triggered
WorkflowEntry that routes to `_handle_unwired_write`, which returns a brief honest
decline ("I can't create milestones from chat yet …") and performs NO write and
fabricates NO success. The action-dispatch rail (ADR-059 / #1124) intercepts the
action BEFORE it can reach the floor — so the confabulation path is cut off.

These tests assert, per covered action:
- The action is registered as an action-triggered workflow (so the rail picks it
  up, not the floor).
- Dispatching the action invokes `_handle_unwired_write` and returns its result.
- The handler's message DECLINES honestly (says it can't do it *yet*) and does
  NOT contain a fabricated success marker ("created", "✓", "done", "added").
- No write is attempted (the handler constructs no GitHub router/connector/service
  and calls nothing that could mutate state — verified structurally: the handler
  takes only (intent, workflow_id) and returns a static decline).

NO new `elif intent.action` branch is added — `TestPreFloorDispatchSiteRatchet`
(tests/test_architecture_enforcement.py) enforces MAX_DISPATCH_SITES == 0.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.intent_service.unwired_writes import UNWIRED_WRITE_ACTIONS
from services.shared_types import IntentCategory

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def intent_service():
    """IntentService with heavy deps patched out (mirrors cohort tests)."""
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService()


# Substrings that would indicate a CONFABULATED write-success — the exact failure
# mode of #1331. A correct honest-degrade message must contain NONE of these.
_FABRICATED_SUCCESS_MARKERS = ["✓", "✅", "created", "added", "done!", "successfully", "i've created", "i have created"]

# Substrings that indicate an HONEST decline (the message must contain at least one).
_HONEST_DECLINE_MARKERS = ["can't", "cannot", "can not", "not yet", "yet"]


# ---------------------------------------------------------------------------
# Coverage set — the actions we cover (at minimum create_milestone, per #1331)
# ---------------------------------------------------------------------------


class TestUnwiredWriteActionSet:
    """The covered-action set includes create_milestone (the confirmed bug) and the
    create-write siblings that are likewise classifier-recognized but unwired."""

    def test_create_milestone_is_covered(self):
        assert "create_milestone" in UNWIRED_WRITE_ACTIONS

    def test_create_write_siblings_covered(self):
        # All GitHub-object create writes with no handler (confirmed: no
        # _handle_create_* method, not in ActionMapper).
        for action in [
            "create_milestone",
            "create_release",
            "create_label",
            "create_branch",
        ]:
            assert action in UNWIRED_WRITE_ACTIONS, f"{action} not covered"

    def test_wired_writes_not_in_set(self):
        """Actions that DO have real handlers must NOT be hijacked by honest-degrade
        (create_issue/update_issue error honestly; generate_report is ANALYSIS-wired)."""
        for wired in ["create_issue", "create_ticket", "update_issue", "generate_report"]:
            assert wired not in UNWIRED_WRITE_ACTIONS, (
                f"{wired} is WIRED — must not be honest-degraded (it has a real handler)"
            )


# ---------------------------------------------------------------------------
# Handler test — the honest-degrade handler declines, never confabulates
# ---------------------------------------------------------------------------


class TestUnwiredWriteHandler:
    """_handle_unwired_write returns an honest decline with NO fabricated success
    and attempts NO write."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("action", sorted(UNWIRED_WRITE_ACTIONS))
    async def test_declines_honestly_no_confabulation(self, intent_service, action):
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action=action,
            context={"original_message": f"please {action.replace('_', ' ')} on my default repo"},
        )

        result = await intent_service._handle_unwired_write(intent, "wf-1")

        assert isinstance(result, IntentProcessingResult)
        assert result.success is True  # graceful, not a 422/error to the user
        msg_lower = result.message.lower()

        # Honest: says it can't do this yet.
        assert any(m in msg_lower for m in _HONEST_DECLINE_MARKERS), (
            f"{action}: message does not honestly decline: {result.message!r}"
        )
        # NOT confabulated: no fake success markers.
        for marker in _FABRICATED_SUCCESS_MARKERS:
            assert marker not in msg_lower, (
                f"{action}: message contains fabricated-success marker {marker!r}: "
                f"{result.message!r}"
            )
        # intent_data records the unwired-write disposition (analytics + audit).
        assert result.intent_data.get("action") == action
        assert result.intent_data.get("unwired_write") is True

    @pytest.mark.asyncio
    async def test_create_milestone_points_to_alternative(self, intent_service):
        """The decline should point the user to the GitHub alternative (per #1331
        tone guidance: brief, honest, point to the alternative)."""
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_milestone",
            context={"original_message": "add a milestone to my default repo"},
        )
        result = await intent_service._handle_unwired_write(intent, "wf-1")
        assert "github" in result.message.lower(), (
            f"decline should point to GitHub alternative: {result.message!r}"
        )

    @pytest.mark.asyncio
    async def test_handler_attempts_no_github_write(self, intent_service):
        """The honest-degrade handler must construct NO GitHub router/connector — it
        performs no write. (Structural guard: patch the router and assert never built.)"""
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_milestone",
            context={"original_message": "add a milestone to my default repo"},
        )
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            result = await intent_service._handle_unwired_write(intent, "wf-1")
        MockRouter.assert_not_called()
        assert result.success is True


# ---------------------------------------------------------------------------
# Dispatch routing — the action-dispatch rail intercepts BEFORE the floor
# ---------------------------------------------------------------------------


class TestUnwiredWriteDispatch:
    """Each covered action is an action-triggered workflow that dispatches to
    _handle_unwired_write via the rail (no hand-coded elif branch)."""

    @pytest.mark.parametrize("action", sorted(UNWIRED_WRITE_ACTIONS))
    def test_registered_as_action_triggered_workflow(self, action):
        from services.intent_service.workflow_dispatcher import WORKFLOW_REGISTRY
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()  # idempotent
        assert action in WORKFLOW_REGISTRY, f"{action} not registered"
        assert WORKFLOW_REGISTRY[action].action_triggered is True, (
            f"{action} not action_triggered — rail won't intercept it; floor will confabulate"
        )

    def test_all_covered_actions_in_action_workflows(self):
        """get_action_workflows() (what the rail checks) contains every covered action,
        so `if intent.action in get_action_workflows()` cuts the floor path."""
        from services.intent_service.workflow_dispatcher import get_action_workflows
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()
        action_workflows = get_action_workflows()
        for action in UNWIRED_WRITE_ACTIONS:
            assert action in action_workflows, f"{action} not on the action-dispatch rail"

    @pytest.mark.asyncio
    async def test_dispatch_invokes_handler(self):
        """dispatch_workflow('create_milestone', ...) calls _handle_unwired_write with
        (intent, workflow_id) and returns its result."""
        from services.intent_service.workflow_dispatcher import dispatch_workflow
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()

        fake_result = IntentProcessingResult(success=True, message="ok", intent_data={})
        mock_service = MagicMock()
        mock_service._handle_unwired_write = AsyncMock(return_value=fake_result)

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_milestone",
            context={"original_message": "add a milestone to my default repo"},
        )

        result = await dispatch_workflow(
            workflow_type="create_milestone",
            session_id="sess-1",
            user_id="user-123",
            context={
                "intent": intent,
                "workflow_id": "wf-1",
                "intent_service": mock_service,
            },
        )

        assert result is fake_result
        mock_service._handle_unwired_write.assert_awaited_once()
        call_args = mock_service._handle_unwired_write.call_args.args
        assert call_args[0] is intent
        assert call_args[1] == "wf-1"


# ---------------------------------------------------------------------------
# End-to-end-ish: the rail short-circuits the floor for an unwired write
# ---------------------------------------------------------------------------


class TestUnwiredWriteShortCircuitsFloor:
    """The crux of #1331: when the classifier yields an unwired write action, the
    rail returns the honest decline and the conversational floor is NEVER invoked
    (so it can't confabulate)."""

    @pytest.mark.asyncio
    async def test_floor_not_reached_for_unwired_write(self, intent_service):
        """Drive _process_intent_internal with a classifier that yields create_milestone
        and assert: (a) the honest decline comes back, (b) ConversationalFloor.respond is
        never called (the rail intercepts before the floor can confabulate).

        user_id is None so the DB-coupled early stages (formality/trust/resume — all
        guarded by `if user_id`) are skipped, keeping this a hermetic unit test that
        exercises the real classify → rail → honest-degrade path.
        """
        from services.intent_service.pre_classifier import MultiIntentResult
        from services.intent_service.workflow_entries import register_default_workflows

        # Make sure the rail is populated.
        register_default_workflows()

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_milestone",
            confidence=0.95,
            context={"original_message": "add a milestone to my default repo"},
            original_message="add a milestone to my default repo",
        )

        # Stub the classification seam: classify_multiple → a single-intent result
        # whose primary_intent is our unwired write. (Single intent, not multi → the
        # `else` branch in _process_intent_internal picks primary_intent directly.)
        intent_service.intent_classifier = MagicMock()
        intent_service.intent_classifier.classify_multiple = AsyncMock(
            return_value=MultiIntentResult(intents=[intent], is_multi_intent=False)
        )
        # Guided-process check runs regardless of user_id — stub it to "no active
        # process" so we reach classification + the rail.
        intent_service._check_active_guided_process = AsyncMock(return_value=(None, None))

        with patch(
            "services.intent_service.conversational_floor.ConversationalFloor.respond",
            new=AsyncMock(),
        ) as mock_floor_respond, patch.object(
            intent_service, "_apply_soft_offer", side_effect=lambda result, *a, **k: result
        ):
            result = await intent_service._process_intent_internal(
                message="add a milestone to my default repo",
                session_id="sess-1",
                user_id=None,
            )

        # The floor must NOT have run — the rail intercepted the unwired write.
        mock_floor_respond.assert_not_called()
        # And the answer is the honest decline (no fabricated success).
        assert result is not None
        msg_lower = (result.message or "").lower()
        assert any(m in msg_lower for m in _HONEST_DECLINE_MARKERS), result.message
        for marker in _FABRICATED_SUCCESS_MARKERS:
            assert marker not in msg_lower, f"confabulation leaked: {result.message!r}"
