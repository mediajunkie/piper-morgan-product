"""#1333 — DERIVED honest-decline for unwired EXECUTION actions (no confabulation).

Arch ruling 2026-06-30: the unwired-decline must be DERIVED, not a hand-maintained
list. An EXECUTION action that reaches `_handle_execution_intent`'s else-branch has
NO registered handler (not in the rail's `get_action_workflows` AND not mapped by
ActionMapper) — it is unwired by construction. It must deterministically honest-decline
and must NEVER route to the conversational floor (which confabulates "done ✓" — the
#1331 trust-breaker).

The KEY property vs the old hand-coded `unwired_writes` list: an action the list never
enumerated (the drift gap Arch flagged — "miss one → confabulation") now declines too,
because the trigger is "reached the else-branch," not "is on the list."
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.shared_types import IntentCategory

pytestmark = pytest.mark.asyncio

_FABRICATED_SUCCESS = ["✓", "✅", "created", "added", "done!", "successfully", "i've", "i have created"]
_HONEST_DECLINE = ["can't", "cannot", "can not", "not yet", "yet"]


@pytest.fixture
def intent_service():
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService()


async def test_novel_unwired_action_declines_not_confabulates_1333(intent_service):
    """An unwired EXECUTION action the old list NEVER enumerated (the drift gap) now
    honest-declines via the derived else-branch — no confabulated success."""
    # 'archive_repository' is not in the former UNWIRED_WRITE_ACTIONS list, has no
    # ActionMapper mapping, and no handler → reaches the else-branch.
    intent = Intent(
        category=IntentCategory.EXECUTION,
        action="archive_repository",
        context={"original_message": "archive my repo please"},
    )

    result = await intent_service._handle_execution_intent(
        intent, workflow=None, session_id="s-1", user_id="u-1"
    )

    assert isinstance(result, IntentProcessingResult)
    assert result.success is True  # honest decline, not a 422 error
    msg = result.message.lower()
    assert any(m in msg for m in _HONEST_DECLINE), f"not an honest decline: {result.message!r}"
    assert not any(m in msg for m in _FABRICATED_SUCCESS), f"confabulated success: {result.message!r}"
    assert result.intent_data.get("unwired_action") is True
    assert result.workflow_id is None  # no handler ran


async def test_unwired_execution_never_routes_to_floor_1333(intent_service):
    """The else-branch must NOT invoke the conversational floor for an unwired action
    (the floor is the confabulation vector). Patch it and assert it's never constructed."""
    intent = Intent(
        category=IntentCategory.EXECUTION,
        action="archive_repository",
        context={"original_message": "archive my repo please"},
    )

    with patch(
        "services.intent_service.conversational_floor.ConversationalFloor"
    ) as floor_cls:
        result = await intent_service._handle_execution_intent(
            intent, workflow=None, session_id="s-1", user_id="u-1"
        )

    floor_cls.assert_not_called()
    assert result.success is True
    assert result.intent_data.get("unwired_action") is True


async def test_create_milestone_declines_via_derived_branch_1333(intent_service):
    """The original #1331 case (create_milestone) honest-declines — curated copy."""
    intent = Intent(
        category=IntentCategory.EXECUTION,
        action="create_milestone",
        context={"original_message": "add a milestone to my default repo"},
    )

    result = await intent_service._handle_execution_intent(
        intent, workflow=None, session_id="s-1", user_id="u-1"
    )

    msg = result.message.lower()
    assert "milestone" in msg
    assert any(m in msg for m in _HONEST_DECLINE)
    assert not any(m in msg for m in _FABRICATED_SUCCESS)
