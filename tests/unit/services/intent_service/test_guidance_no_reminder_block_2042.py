"""#2042 aside (CXO 2026-11-02 18:59; Arch 19:3x): a GUIDANCE turn's floor context
carries no due-reminder block, and the gather is never run on that path.

The GUIDANCE assembler used to merge ``ContextAssembler._gather_reminder_context``
directly (#1566), bypassing the #2233 ride gate and the #1625 mention gate, which is how
an unasked reminder aside reached a guidance turn on alpha (PA's Ba1/B1 replays). Keyed
on the route the classifier chose, never on wording (ADR-080). Nothing is marked
surfaced on a guidance turn, so the conversation's one mention moves to the next op in
``DUE_REMINDER_LINE_OPS`` (PPM's condition). The enforcement pin
``TestReminderGatherHasOneFloorCaller`` holds the seam at the source level; this pins
the behaviour.
"""

from unittest.mock import AsyncMock, patch

import pytest

from services.domain.models import Intent
from services.shared_types import IntentCategory
from tests.unit.services.intent_service.test_milestone_pick_2209 import (  # noqa: F401
    service,
)

_REMINDER_KEYS = ("due_reminders", "reminder_count", "due_reminder_ages")


@pytest.mark.asyncio
async def test_guidance_context_runs_no_reminder_gather_and_carries_no_block(service):
    intent = Intent(
        category=IntentCategory.GUIDANCE,
        action="get_contextual_guidance",
        context={"original_message": "Help me break down the search feature"},
    )
    gather = AsyncMock(return_value={"due_reminders": ["review PRs"], "reminder_count": 1})
    with patch(
        "services.intent_service.context_assembler.ContextAssembler._gather_reminder_context",
        new=gather,
    ):
        ctx = await service._assemble_guidance_context(intent, "s2042-g1", "u-2042")
    gather.assert_not_awaited()
    for key in _REMINDER_KEYS:
        assert key not in ctx, f"{key} reached a GUIDANCE turn's context"
    assert "current_time" in ctx  # the rest of the guidance context is intact


@pytest.mark.asyncio
async def test_guidance_turn_marks_nothing_surfaced(service):
    """Nothing is spent on a guidance turn: the session's surfaced set (the once-per-
    conversation store the DUE_REMINDER_LINE_OPS line reads) stays empty, so the next
    eligible op's line still carries the one mention (PPM's condition)."""
    from services.intent_service.conversation_context import get_or_create_context

    intent = Intent(
        category=IntentCategory.GUIDANCE,
        action="get_contextual_guidance",
        context={"original_message": "What should I focus on learning first?"},
    )
    sid, uid = "s2042-g2", "u-2042"
    assert not get_or_create_context(sid, user_id=uid).surfaced_reminder_ids
    await service._assemble_guidance_context(intent, sid, uid)
    assert not get_or_create_context(sid, user_id=uid).surfaced_reminder_ids
