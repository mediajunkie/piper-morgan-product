"""#2324 gap A and "tomorrow" (CXO 11-07 20:02, Arch 20:03).

Gap A: every render of an open milestone with open issues whose due date is past
in the person's local date says so: ``Due 2026-10-29 (overdue by 9 days).`` No
local date (timezone unknown) adds nothing; it is never guessed from the server.

Tomorrow: the templated time reply carries both days every time:
``Today is …. Tomorrow is Sunday, November 8.``
"""

from __future__ import annotations

from datetime import date, datetime
from unittest.mock import AsyncMock, MagicMock, patch
from zoneinfo import ZoneInfo

import pytest

from services.intent_service import milestone_render as mr

BETA = {
    "title": "Beta launch",
    "state": "open",
    "due_on": "2026-10-29T00:00:00Z",
    "open_issues": 4,
    "closed_issues": 0,
}
NOV_7 = date(2026, 11, 7)


def test_cxo_words_verbatim_on_the_one_milestone_render():
    assert mr.render_one_milestone(BETA, date(2026, 11, 7)) == (
        "**Beta launch**: 0 of 4 issues closed, 4 still open. Due 2026-10-29 (overdue by 9 days)."
    )


def test_one_day_is_singular():
    assert "(overdue by 1 day)." in mr.render_one_milestone(BETA, date(2026, 10, 30))


@pytest.mark.parametrize("today", [date(2026, 10, 29), date(2026, 10, 1)])
def test_due_today_or_later_adds_nothing(today):
    assert mr.render_one_milestone(BETA, today).endswith("Due 2026-10-29.")


def test_no_local_date_adds_nothing():
    assert mr.render_one_milestone(BETA, None).endswith("Due 2026-10-29.")
    assert mr.render_one_milestone(BETA).endswith("Due 2026-10-29.")


def test_no_open_issues_adds_nothing():
    m = {**BETA, "open_issues": 0, "closed_issues": 3}
    assert mr.render_one_milestone(m, NOV_7).endswith("Due 2026-10-29.")
    assert mr.overdue_note({**BETA, "open_issues": 0, "closed_issues": 0}, NOV_7) == ""


def test_closed_or_undated_adds_nothing():
    assert mr.overdue_note({**BETA, "state": "closed"}, NOV_7) == ""
    assert mr.overdue_note({**BETA, "due_on": None}, NOV_7) == ""
    assert mr.overdue_note({**BETA, "due_on": "not-a-date"}, NOV_7) == ""


@pytest.mark.asyncio
async def test_the_milestone_list_carries_the_note_from_the_persons_date():
    from services.domain.models import Intent, IntentCategory
    from services.intent.intent_service import IntentService

    svc = IntentService()
    intent = Intent(
        category=IntentCategory.QUERY,
        action="list_milestones_query",
        confidence=0.9,
        original_message="what milestones do I have?",
    )
    router = AsyncMock()
    router.list_milestones_via_mcp = AsyncMock(
        return_value=[BETA, {**BETA, "title": "Later", "due_on": "2026-12-01T00:00:00Z"}]
    )
    router._resolve_default_repo = AsyncMock(return_value=None)
    with (
        patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ),
        patch(
            "services.intent_service.context_assembler._user_local_today",
            AsyncMock(return_value=NOV_7),
        ),
        patch.object(
            IntentService,
            "_resolve_milestone_in_read",
            AsyncMock(return_value=MagicMock(outcome="none", index=None)),
        ),
    ):
        result = await svc._handle_list_milestones_query(intent, workflow_id="wf-1")
    assert "- **Beta launch** — Due 2026-10-29 (overdue by 9 days). (4 open issues)" in (
        result.message
    )
    assert "- **Later** — Due 2026-12-01. (4 open issues)" in result.message


def _temporal_intent():
    from services.domain.models import Intent
    from services.shared_types import IntentCategory

    return Intent(
        original_message="what day is it tomorrow?",
        category=IntentCategory.TEMPORAL,
        action="provide_current_time_with_calendar",
        confidence=0.9,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "now, today_words, tomorrow_words",
    [
        (
            datetime(2026, 11, 7, 19, 37, tzinfo=ZoneInfo("America/Los_Angeles")),
            "Today is Saturday, November 07, 2026 at 7:37 PM PST.",
            "Tomorrow is Sunday, November 8.",
        ),
        (
            datetime(2026, 10, 31, 23, 50, tzinfo=ZoneInfo("America/Los_Angeles")),
            "Today is Saturday, October 31, 2026 at 11:50 PM PDT.",
            "Tomorrow is Sunday, November 1.",
        ),
    ],
)
async def test_every_time_reply_says_tomorrow(now, today_words, tomorrow_words):
    from services.intent_service.canonical_handlers import CanonicalHandlers

    router = MagicMock()
    router.get_temporal_summary = AsyncMock(return_value={})
    with (
        patch(
            "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
            return_value=router,
        ),
        patch(
            "services.intent_service.canonical_handlers.user_timezone_name",
            AsyncMock(return_value="America/Los_Angeles"),
        ),
        patch("services.intent_service.canonical_handlers.now_in_zone", return_value=now),
    ):
        result = await CanonicalHandlers()._handle_temporal_query(
            _temporal_intent(), "session-1", user_id="11111111-2222-3333-4444-555555555555"
        )
    assert f"{today_words} {tomorrow_words}" in result["message"]
