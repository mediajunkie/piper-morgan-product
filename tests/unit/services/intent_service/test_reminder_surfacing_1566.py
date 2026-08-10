"""Issue #1566: due reminders must surface on EVERY floor-bound turn.

PM live 8/10: four due-now reminders and 15 minutes of STATUS / EXECUTION /
TEMPORAL turns with ZERO surfacing. Two distinct breaks in the promise chain
("I'll surface this ... once it's due"):

1. context_assembler.gather_context gathered reminder context ONLY for
   `category == "CONVERSATION"` (#903's greeting design) — every other
   floor-bound category never fetched due reminders at all.
2. conversational_floor._format_domain_context never rendered
   due_reminders / reminder_count / source_failed AT ALL — even a
   CONVERSATION turn dropped the gathered keys on the floor's doorstep.

Fix: reminder context rides every gather_context call (cached TTL-30s per
#984, so the marginal cost is a dict merge), and the floor renders a due-line
for any category. #1425 honesty preserved: a failed lookup renders as
"couldn't check", never as "nothing due".
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.intent_service.context_assembler import ContextAssembler
from services.intent_service.conversational_floor import ConversationalFloor

# Every category branch gather_context dispatches on, plus UNKNOWN (the #960
# else-branch). CONVERSATION is the pre-#1566 behavior that must not regress.
FLOOR_CATEGORIES = [
    "CONVERSATION",
    "STATUS",
    "PRIORITY",
    "TEMPORAL",
    "MEMORY",
    "IDENTITY",
    "DISCOVERY",
    "TRUST",
    "UNKNOWN",
]

_CATEGORY_GATHERERS = [
    "_gather_identity_context",
    "_gather_trust_context",
    "_gather_insight_pull_context",
    "_gather_memory_context",
    "_gather_temporal_context",
    "_gather_status_priority_context",
]


def _quiet_gatherers():
    """Patch the category gatherers to empty so tests isolate the reminder
    rail (the real gatherers reach for DB/GitHub)."""
    patchers = [
        patch.object(ContextAssembler, name, AsyncMock(return_value={}))
        for name in _CATEGORY_GATHERERS
    ]
    patchers.append(
        patch(
            "services.intent_service.context_assembler._current_time_for_user",
            AsyncMock(return_value=None),
        )
    )
    return patchers


def _mock_due(reminders):
    """Patch TodoIntentHandlers so get_due_reminders returns `reminders`."""
    mock_instance = MagicMock()
    mock_instance.get_due_reminders = AsyncMock(return_value=reminders)
    return patch(
        "services.intent_service.todo_handlers.TodoIntentHandlers",
        return_value=mock_instance,
    )


async def _gather(category, reminders):
    patchers = _quiet_gatherers()
    for p in patchers:
        p.start()
    try:
        with _mock_due(reminders):
            assembler = ContextAssembler()
            # Fresh user_id per call -> no cross-test cache hits (#984 keys by user)
            return await assembler.gather_context(category, user_id=str(uuid4()))
    finally:
        for p in patchers:
            p.stop()


# ---------------------------------------------------------------------------
# Assembler: reminder context rides every floor-bound category
# ---------------------------------------------------------------------------


class TestReminderContextRidesEveryCategory1566:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("category", FLOOR_CATEGORIES)
    async def test_due_reminders_present_for_category(self, category):
        """PM's live gap: STATUS/TEMPORAL/etc turns never gathered reminders."""
        context = await _gather(category, ["check in with the Lead Developer"])
        assert context.get("due_reminders") == ["check in with the Lead Developer"], (
            f"due reminders missing from {category} context — the #1566 "
            f"CONVERSATION-only gate (context keys: {list(context.keys())})"
        )
        assert context["reminder_count"] == 1

    @pytest.mark.asyncio
    @pytest.mark.parametrize("category", ["STATUS", "TEMPORAL", "CONVERSATION"])
    async def test_source_failed_flag_rides_every_category(self, category):
        """#1425 honesty: a failed lookup (None sentinel) flags source_failed
        on every category, never a silent nothing."""
        context = await _gather(category, None)
        assert context.get("source_failed") is True, (
            f"failed reminder lookup left no source_failed flag on {category}"
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("category", ["STATUS", "CONVERSATION"])
    async def test_no_due_reminders_adds_nothing(self, category):
        context = await _gather(category, [])
        assert "due_reminders" not in context
        assert "source_failed" not in context

    @pytest.mark.asyncio
    async def test_category_gatherer_failure_does_not_kill_reminders(self):
        """The reminder rail sits OUTSIDE the category dispatch's try — a
        broken STATUS gatherer must not take due reminders down with it."""
        patchers = _quiet_gatherers()
        for p in patchers:
            p.start()
        try:
            with patch.object(
                ContextAssembler,
                "_gather_status_priority_context",
                AsyncMock(side_effect=RuntimeError("github down")),
            ), _mock_due(["submit the report"]):
                assembler = ContextAssembler()
                context = await assembler.gather_context("STATUS", user_id=str(uuid4()))
        finally:
            for p in patchers:
                p.stop()
        assert context.get("due_reminders") == ["submit the report"]


# ---------------------------------------------------------------------------
# Floor renderer: due_reminders / source_failed actually render
# ---------------------------------------------------------------------------


class TestFloorRendersDueReminders1566:
    def _render(self, domain_context):
        return ConversationalFloor()._format_domain_context(domain_context)

    def test_due_reminders_render_as_due_line(self):
        """Pre-#1566 the floor had NO handling for due_reminders — the
        gathered keys were silently dropped from the prompt."""
        out = self._render(
            {"due_reminders": ["check in with the Lead Developer"], "reminder_count": 1}
        )
        assert "check in with the Lead Developer" in out, (
            "due reminder text missing from the floor's context block"
        )
        assert "DUE REMINDER" in out

    def test_due_reminders_render_alongside_status_keys(self):
        """Any-category rendering: the due-line rides with e.g. STATUS data."""
        out = self._render(
            {
                "pending_todos": [{"text": "review the PR"}],
                "due_reminders": ["submit the report", "call the vendor"],
                "reminder_count": 2,
            }
        )
        assert "submit the report" in out
        assert "call the vendor" in out
        assert "review the PR" in out

    def test_source_failed_renders_honest_couldnt_check(self):
        """#1425: lookup failure renders as couldn't-check, never dropped."""
        out = self._render({"source_failed": True})
        assert "Reminder check FAILED" in out
        assert "couldn't check" in out or "could not verify" in out

    def test_reminder_count_beyond_display_cap_is_stated(self):
        """m-44: the denominator rides with a truncated list."""
        rems = [f"reminder {i}" for i in range(7)]
        out = self._render({"due_reminders": rems, "reminder_count": 7})
        assert "7" in out
        assert "more" in out

    def test_empty_context_still_renders_empty(self):
        assert self._render({}) == ""
