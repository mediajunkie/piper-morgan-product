"""#2140 / #2143 — "what changed" is fail-closed per read and names the window it read.

Arch (2026-10-23 06:28, on #2140): each of the three reads (activity log, tasks,
projects) records ok-with-rows, ok-empty or failed. CXO's empty line only when
all three read ok and all three are empty; a failed read is named in CXO's
failed-read line, with any rows the others found still listed; all three
failed is ``success=False``. The owner is computed once before any read, and
no principal is not readable. #2143: "past hour" reads an hour, not 0 days.

No LLM and no database: ``AsyncSessionFactory.session_scope`` is stubbed per
read, in the handler's read order (activity log, tasks, projects).
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.shared_types import IntentCategory

# #2265: the window words are rendered from the bounds, so the pins compute them the
# same way, in the patched zone (a fixed non-UTC zone, so a UTC mix-up near midnight
# would print the wrong day and fail here).
_ZONE = "America/Los_Angeles"
_TZ_PATCH = "services.intent.intent_service.user_timezone_name"


def _since_yesterday_words():
    from zoneinfo import ZoneInfo

    start = datetime.now(ZoneInfo(_ZONE)) - timedelta(days=1)
    return f"since the start of yesterday, {start:%A}, {start:%B} {start.day}"


YD = _since_yesterday_words()


@pytest.fixture(autouse=True)
def _fixed_zone():
    with patch(_TZ_PATCH, new=AsyncMock(return_value=_ZONE)):
        yield


_SCOPE = "services.intent.intent_service.AsyncSessionFactory.session_scope"
_USER = "3f7b8a52-2140-4b00-9e00-000000002140"
# #2258 (CXO 2026-11-03 07:3x): the empty reply names no "activity log" (no such page)
# and claims only what the census audits (Slack, GitHub), never "anything".
NOTHING_NEW = (
    "I don't see anything new in your Piper tasks or projects {window}. Piper hasn't "
    "posted to Slack or written to GitHub for you in that time. I haven't looked at "
    "anything done in GitHub outside Piper."
)
# CXO 10-23 09:27, verbatim shapes.
FAILED_ALL = (
    "I couldn't read your Piper tasks or projects, or what Piper did for you, just now, so I "
    f"can't say what changed {YD}. Try again in a moment; if it keeps failing, tell us."
)
FAILED_BESIDE_ROWS = (
    "I couldn't read your Piper {source} just now, so the list above doesn't include it. "
    "Try again in a moment; if it keeps failing, tell us."
)
# #2258 (CXO 2026-11-03 08:2x): tasks failed; projects and the actions read empty.
NOTHING_NEW_TASKS_FAILED = (
    f"I don't see anything new in your Piper projects {YD}, and Piper hasn't posted "
    "to Slack or written to GitHub for you in that time. I couldn't read your Piper tasks just "
    "now, so I can't say what changed there. Try again in a moment; if it keeps failing, tell us."
)


@pytest.fixture
def intent_service():
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService()


def _intent(message="what changed since yesterday", user_id=_USER):
    ctx = {"original_message": message}
    if user_id:
        ctx["user_id"] = user_id
    return Intent(category=IntentCategory.QUERY, action="changes_query", context=ctx)


def _todo(text, minutes_ago):
    t = MagicMock()
    t.text = text
    t.priority = "medium"
    t.created_at = datetime.now(timezone.utc) - timedelta(minutes=minutes_ago)
    t.updated_at = t.created_at
    t.completed_at = None
    return t


def _project(name, minutes_ago):
    p = MagicMock()
    p.name = name
    p.created_at = datetime.now(timezone.utc) - timedelta(minutes=minutes_ago)
    p.updated_at = p.created_at
    return p


class _Session:
    def __init__(self, rows):
        self.rows = rows
        self.statements = []

    async def execute(self, stmt):
        self.statements.append(stmt)
        result = MagicMock()
        result.scalars.return_value.all.return_value = self.rows
        # #2258: the audit read is a grouped select read with .all()
        result.all.return_value = self.rows
        return result


def _scopes(*reads):
    """One session_scope per read; a read is a row list or an Exception."""
    made = []

    def factory():
        spec = reads[len(made)]
        made.append(spec)
        cm = MagicMock()
        if isinstance(spec, Exception):
            cm.__aenter__ = AsyncMock(side_effect=spec)
        else:
            cm.__aenter__ = AsyncMock(return_value=_Session(spec))
        cm.__aexit__ = AsyncMock(return_value=None)
        return cm

    return factory, made


async def _run(intent_service, intent, *reads):
    factory, made = _scopes(*reads)
    with patch(_SCOPE, side_effect=factory):
        result = await intent_service._handle_changes_query(intent, "wf", "session-not-a-user")
    return result, made


@pytest.mark.asyncio
async def test_all_three_ok_and_empty_is_cxos_nothing_new_line(intent_service):
    result, made = await _run(intent_service, _intent(), [], [], [])
    assert len(made) == 3
    assert result.success is True
    assert result.message == NOTHING_NEW.format(window=YD)


@pytest.mark.asyncio
async def test_the_first_read_failing_does_not_empty_the_other_two(intent_service):
    """The owner used to be assigned inside the first read: its failure made the
    other two raise NameError into a false "no activity"."""
    result, made = await _run(
        intent_service,
        _intent(),
        RuntimeError("audit session failed"),
        [_todo("Review the launch notes", 30)],
        [],
    )
    assert len(made) == 3
    assert result.success is True
    # #2258 (CXO 08:0x): the actions read failed, so the opener claims no "what Piper
    # did for you" and the failed line names that source in the person's terms.
    assert result.message.startswith(
        f"Here's what changed in your Piper tasks and projects {YD}. "
        "I haven't looked at anything done in GitHub outside Piper."
    )
    assert "Review the launch notes" in result.message
    assert result.message.endswith(
        "I couldn't read what Piper did for you just now, so the list above doesn't include "
        "it. Try again in a moment; if it keeps failing, tell us."
    )
    assert "activity log" not in result.message
    assert result.intent_data["failed_sources"] == ["activity log"]


@pytest.mark.asyncio
async def test_a_failed_read_with_the_others_empty_is_not_nothing_new(intent_service):
    result, _ = await _run(intent_service, _intent(), [], RuntimeError("todo read"), [])
    assert result.message == NOTHING_NEW_TASKS_FAILED
    assert "activity log" not in result.message


@pytest.mark.asyncio
async def test_one_read_failing_while_another_has_rows_lists_rows_and_names_the_failure(
    intent_service,
):
    result, _ = await _run(
        intent_service, _intent(), [], RuntimeError("todo read"), [_project("Atlas", 20)]
    )
    assert result.success is True
    assert "Atlas" in result.message
    assert result.message.startswith(
        f"Here's what changed in your Piper projects {YD}, and what Piper did for "
        "you. I haven't looked at anything done in GitHub outside Piper."
    )
    assert "activity log" not in result.message
    assert result.message.endswith(FAILED_BESIDE_ROWS.format(source="tasks"))


@pytest.mark.asyncio
async def test_every_read_failing_is_success_false(intent_service):
    boom = RuntimeError("db down")
    result, _ = await _run(intent_service, _intent(), boom, boom, boom)
    assert result.success is False
    assert result.message == FAILED_ALL


@pytest.mark.asyncio
async def test_no_principal_is_a_failed_read_and_reads_nothing(intent_service):
    """The session-id fallback matched no owner row: a false empty."""
    result, made = await _run(intent_service, _intent(user_id=None))
    assert made == []
    assert result.success is False
    assert result.message == FAILED_ALL
    assert result.intent_data["reason"] == "no_principal"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "message, window",
    [
        ("what changed in the past week?", "in the past week"),
        ("what changed in the last 3 days?", "in the past 3 days"),
        ("what changed in the past month?", "in the past month"),
    ],
)
async def test_the_words_name_the_window_read(intent_service, message, window):
    result, _ = await _run(intent_service, _intent(message), [], [], [])
    assert result.message == NOTHING_NEW.format(window=window)


def _bound_since(stmt):
    """The datetime the statement's where clause compares created_at against."""
    params = stmt.compile().params
    stamps = [v for v in params.values() if isinstance(v, datetime)]
    assert stamps, params
    return min(stamps)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "message, hours, window",
    [
        ("what changed in the past hour?", 1, "in the past hour"),
        ("what changed in the last 3 hours?", 3, "in the past 3 hours"),
    ],
)
async def test_2143_an_hour_window_is_a_real_window(intent_service, message, hours, window):
    sessions = []

    def factory():
        s = _Session([_todo("Draft the agenda", 10)] if len(sessions) == 1 else [])
        sessions.append(s)
        cm = MagicMock()
        cm.__aenter__ = AsyncMock(return_value=s)
        cm.__aexit__ = AsyncMock(return_value=None)
        return cm

    before = datetime.now(timezone.utc)
    with patch(_SCOPE, side_effect=factory):
        result = await intent_service._handle_changes_query(_intent(message), "wf", "s")

    since = _bound_since(sessions[1].statements[0])
    expected = before - timedelta(hours=hours)
    assert abs((since - expected).total_seconds()) < 5, (since, expected)
    assert result.intent_data["time_window_hours"] == hours
    assert result.message.startswith(
        f"Here's what changed in your Piper tasks and projects {window}, and what Piper did "
        "for you. I haven't looked at anything done in GitHub outside Piper."
    )
    assert "Draft the agenda" in result.message


# #2265 (Arch 2026-11-03 18:52; CXO's words 19:00): a "yesterday" ask reads from the
# person's LOCAL start of yesterday, and the words are rendered from that bound. The
# clock is fixed in a no-DST zone nine hours ahead of UTC, so a UTC mix-up would name
# the wrong day (Monday) and a rolling 24 hours would start at the wrong instant.
class TestYesterdayIsTheLocalStartOfYesterday:
    NOW = datetime(2026, 11, 3, 20, 30, tzinfo=timezone.utc)  # 2026-11-04 05:30 in Tokyo

    @pytest.mark.asyncio
    async def test_the_bound_is_local_midnight_and_the_words_name_that_day(self, intent_service):
        with patch(_TZ_PATCH, new=AsyncMock(return_value="Asia/Tokyo")):
            since, words = await intent_service._changes_window(
                "what did we accomplish yesterday?", _USER, self.NOW
            )
        assert since == datetime(2026, 11, 2, 15, 0, tzinfo=timezone.utc)  # 11-03 00:00 JST
        assert words == "since the start of yesterday, Tuesday, November 3"

    @pytest.mark.asyncio
    async def test_the_zone_is_the_accounts_not_utc(self, intent_service):
        with patch(_TZ_PATCH, new=AsyncMock(return_value="UTC")) as tz:
            since, words = await intent_service._changes_window("since yesterday", _USER, self.NOW)
        tz.assert_awaited_once_with(_USER)
        assert since == datetime(2026, 11, 2, 0, 0, tzinfo=timezone.utc)
        assert words == "since the start of yesterday, Monday, November 2"

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "message, hours, words",
        [
            ("what changed in the past day?", 24, "in the past 24 hours"),
            ("what changed in the last 3 hours?", 3, "in the past 3 hours"),
            ("what changed in the past week?", 24 * 7, "in the past week"),
        ],
    )
    async def test_a_rolling_ask_says_its_span_and_never_reads_the_zone(
        self, intent_service, message, hours, words
    ):
        with patch(_TZ_PATCH, new=AsyncMock(return_value="Asia/Tokyo")) as tz:
            since, got = await intent_service._changes_window(message, _USER, self.NOW)
        tz.assert_not_awaited()
        assert since == self.NOW - timedelta(hours=hours)
        assert got == words

    @pytest.mark.asyncio
    async def test_the_served_reply_carries_the_same_words_as_the_bound(self, intent_service):
        """End to end through the handler: the nothing-new line names the day the
        read started from, in the patched zone, never a separate label."""
        result, made = await _run(
            intent_service, _intent("what did we accomplish yesterday?"), [], [], []
        )
        assert len(made) == 3
        assert result.message == NOTHING_NEW.format(window=YD)
        assert 24 <= result.intent_data["time_window_hours"] <= 48
