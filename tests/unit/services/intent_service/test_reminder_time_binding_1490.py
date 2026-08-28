"""Issue #1490 (reopened after PM verification 8/8): inverted-order time binding.

PM's verification phrasing — "remind me at 3pm tomorrow to review the PR" —
DROPPED the explicit 3pm and saved the reminder at the 09:00 morning default
(prod row: reminder_date 2026-08-09 09:00; reply copy said "tomorrow morning").

Root cause: parse_reminder_time's bare-"tomorrow" branch fired before any
branch that could see "at 3pm", so the explicit time was silently replaced by
the vague-time default. The prior #1490 fix covered [time-adjacent] "tomorrow
at 3pm" only.

Covers:
- The ordering matrix (parser + slot extraction): "at 3pm tomorrow",
  "tomorrow at 3pm" (must stay green), "at 9:41 today", "today at 9:41",
  "at noon tomorrow", and "tomorrow morning" (vague time — morning default
  IS correct there).
- THE INVARIANT (its own class): a message carrying an explicit clock time
  (am/pm form, HH:MM, noon/midnight) must yield a parsed reminder carrying
  that time — never a silent default. Unbindable explicit times ("at 25:99")
  return (None, honest-echo) and the handler ASKS instead of guessing 9am.
- #1493 companion: the inverted-order path returns an AWARE local datetime
  (same offset discipline as the rest of temporal_utils).

Related-but-out-of-scope: "remind me at 9:41 today to X" ALSO failed to
ROUTE on 8/8 (pre-classifier REMINDER_PATTERNS requires to|about directly
after "remind me") — that is #1517's routing half. These tests pin that the
slot layer (extraction + parsing) handles it once routed.
"""

import re
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from services.intent_service.temporal_utils import parse_reminder_time


def _now_local():
    return datetime.now().astimezone()


def _tomorrow_local():
    return _now_local() + timedelta(days=1)


def _freeze_parser_now(monkeypatch, frozen_naive: datetime) -> None:
    """#1562: freeze temporal_utils' wall clock at a NAIVE local datetime.

    parse_reminder_time reads `datetime.now().astimezone()`; returning a
    naive value from now() lets .astimezone() attach the machine-local
    offset, so tests are deterministic in WALL-CLOCK terms on any host —
    which is exactly the axis the today/past logic runs on (the past-check
    runs on the server clock; see the #1562 today-branch comment).
    """
    import services.intent_service.temporal_utils as tu

    class _FrozenDatetime(datetime):
        @classmethod
        def now(cls, tz=None):  # the parse fns call now() with no tz arg
            return frozen_naive if tz is None else frozen_naive.astimezone(tz)

    monkeypatch.setattr(tu, "datetime", _FrozenDatetime)


# ---------------------------------------------------------------------------
# Parser: ordering matrix
# ---------------------------------------------------------------------------


class TestInvertedOrderTimeParsing1490:
    """parse_reminder_time must bind an explicit clock time to the date word
    regardless of which comes first in the message."""

    def test_pm_verbatim_at_3pm_tomorrow(self):
        """PM's exact failing phrasing (8/8 verification)."""
        dt, label = parse_reminder_time("remind me at 3pm tomorrow to review the PR")
        assert dt is not None
        assert (dt.hour, dt.minute) == (15, 0), (
            f"explicit 3pm dropped — got {dt.hour:02d}:{dt.minute:02d} "
            f"(label {label!r}); 09:00 means the morning default swallowed it"
        )
        assert dt.date() == _tomorrow_local().date()
        assert "3pm" in label
        assert "morning" not in label

    def test_tomorrow_at_3pm_stays_green(self):
        """The already-fixed adjacent ordering must not regress."""
        dt, label = parse_reminder_time("remind me tomorrow at 3pm to review the PR")
        assert dt is not None
        assert (dt.hour, dt.minute) == (15, 0)
        assert dt.date() == _tomorrow_local().date()
        assert label == "tomorrow at 3pm"

    def test_at_941_today(self, monkeypatch):
        # #1562: an explicit "today" binds TODAY — the old "or tomorrow if
        # already past" alternative here was the silent day-roll PM hit live.
        # Frozen before 9:41 so the binding is deterministic.
        _freeze_parser_now(monkeypatch, datetime(2026, 8, 10, 7, 16))
        dt, label = parse_reminder_time("remind me at 9:41 today to check the deploy")
        assert dt is not None
        assert (dt.hour, dt.minute) == (9, 41)
        assert (
            dt.date() == datetime(2026, 8, 10).date()
        ), f"explicit 'today' bound {dt.date()} — never a silent next-day roll (#1562)"
        assert "9:41" in label

    def test_today_at_941(self, monkeypatch):
        _freeze_parser_now(monkeypatch, datetime(2026, 8, 10, 7, 16))
        dt, label = parse_reminder_time("remind me today at 9:41 to check the deploy")
        assert dt is not None
        assert (dt.hour, dt.minute) == (9, 41)
        assert dt.date() == datetime(2026, 8, 10).date()
        assert "9:41" in label

    def test_at_noon_tomorrow(self):
        dt, label = parse_reminder_time("remind me at noon tomorrow to review the PR")
        assert dt is not None
        assert (dt.hour, dt.minute) == (
            12,
            0,
        ), f"explicit noon dropped — got {dt.hour:02d}:{dt.minute:02d} (label {label!r})"
        assert dt.date() == _tomorrow_local().date()
        assert "noon" in label

    def test_tomorrow_morning_vague_default_is_correct(self):
        """'tomorrow morning' carries NO explicit clock time — the 9am
        morning default is the CORRECT behavior there, not a bug."""
        dt, label = parse_reminder_time("remind me tomorrow morning to stretch")
        assert dt is not None
        assert (dt.hour, dt.minute) == (9, 0)
        assert dt.date() == _tomorrow_local().date()
        assert label == "tomorrow morning"


# ---------------------------------------------------------------------------
# Slot extraction: ordering matrix
# ---------------------------------------------------------------------------


class TestInvertedOrderTextExtraction1490:
    """_extract_reminder_text must consume time expressions in time-first
    position and strip them in trailing position, for the same matrix."""

    def setup_method(self):
        from services.intent_service.todo_handlers import TodoIntentHandlers

        self.handlers = TodoIntentHandlers()

    @pytest.mark.parametrize(
        "message,expected",
        [
            # PM's verbatim failing phrasing
            ("remind me at 3pm tomorrow to review the PR", "review the pr"),
            # Adjacent ordering (must stay green)
            ("remind me tomorrow at 3pm to review the PR", "review the pr"),
            # HH:MM + today, both orderings (the #1517-adjacent slot half)
            ("remind me at 9:41 today to check the deploy", "check the deploy"),
            ("remind me today at 9:41 to check the deploy", "check the deploy"),
            # noon, time-first
            ("remind me at noon tomorrow to review the PR", "review the pr"),
            # vague time, time-first (must stay green)
            ("remind me tomorrow morning to stretch", "stretch"),
        ],
    )
    def test_time_first_orderings(self, message, expected):
        assert self.handlers._extract_reminder_text(message) == expected

    @pytest.mark.parametrize(
        "message,expected",
        [
            # Trailing time expressions stripped from the todo text
            ("remind me to review the PR at 3pm tomorrow", "review the pr"),
            ("remind me to check the deploy at 9:41 today", "check the deploy"),
            ("remind me to review the PR at noon tomorrow", "review the pr"),
        ],
    )
    def test_trailing_time_stripped(self, message, expected):
        assert self.handlers._extract_reminder_text(message) == expected


# ---------------------------------------------------------------------------
# THE INVARIANT
# ---------------------------------------------------------------------------


class TestExplicitClockTimeInvariant1490:
    """If the user's message contains an explicit clock time (am/pm form,
    HH:MM, or noon/midnight), the parsed reminder MUST carry that time —
    never a silent default. If the time can't be bound, the parser returns
    (None, honest-echo) and the handler asks instead of guessing 9am."""

    @pytest.mark.parametrize(
        "message,hour,minute",
        [
            ("remind me at 3pm tomorrow to review the PR", 15, 0),
            ("remind me to review the PR at 3pm tomorrow", 15, 0),
            ("remind me tomorrow at 3pm to review the PR", 15, 0),
            ("remind me at 9:41 today to check the deploy", 9, 41),
            ("remind me today at 9:41 to check the deploy", 9, 41),
            ("remind me at noon tomorrow to submit the report", 12, 0),
            ("remind me at midnight tomorrow to run the deploy", 0, 0),
            ("remind me tomorrow at 7:15am to go for a run", 7, 15),
            ("remind me next Monday at 4pm to send the invoice", 16, 0),
            ("remind me next week at 4pm to send the invoice", 16, 0),
            ("remind me at 5pm to send the update", 17, 0),
        ],
    )
    def test_explicit_time_is_always_carried(self, message, hour, minute, monkeypatch):
        # #1562: frozen at 08:00 so the today-form rows are deterministic —
        # explicit "today" + a PAST clock time now honestly asks (None,
        # past-today echo) instead of silently rolling, so running this
        # matrix late in the day must not flip those rows.
        _freeze_parser_now(monkeypatch, datetime(2026, 8, 10, 8, 0))
        dt, label = parse_reminder_time(message)
        assert (
            dt is not None
        ), f"explicit clock time in {message!r} parsed to None (label {label!r})"
        assert (dt.hour, dt.minute) == (hour, minute), (
            f"explicit clock time in {message!r} not carried: expected "
            f"{hour:02d}:{minute:02d}, got {dt.hour:02d}:{dt.minute:02d} "
            f"(label {label!r}) — a silent default violates the #1490 invariant"
        )

    @pytest.mark.parametrize(
        "message,delta",
        [
            # Issue #1542 (invariant deepening): word-form durations are
            # explicit time expressions too. The digit-only "in \d+ hours"
            # let these fall to the tomorrow-9am default (PM live 8/9:
            # "remind me to stretch in two hours" saved for tomorrow 09:00).
            ("remind me to stretch in two hours", timedelta(hours=2)),
            ("remind me in two hours to stretch", timedelta(hours=2)),
            ("remind me in ten minutes to check the oven", timedelta(minutes=10)),
            ("remind me to follow up in three days", timedelta(days=3)),
            ("remind me in twelve hours to take the medication", timedelta(hours=12)),
            ("remind me in one minute to look up", timedelta(minutes=1)),
        ],
    )
    def test_explicit_word_duration_is_always_carried(self, message, delta):
        before = datetime.now().astimezone()
        dt, label = parse_reminder_time(message)
        after = datetime.now().astimezone()
        assert (
            dt is not None
        ), f"explicit word-form duration in {message!r} parsed to None (label {label!r})"
        assert before + delta <= dt <= after + delta, (
            f"explicit word-form duration in {message!r} not carried: expected "
            f"now+{delta}, got {dt} (label {label!r}) — a silent default "
            "violates the #1490 invariant (#1542 deepening)"
        )

    @pytest.mark.parametrize(
        "message,echo",
        [
            # Explicit-but-unbindable times: minute > 59, am/pm hour out of
            # 1-12. Pre-fix these either crashed (ValueError from
            # .replace(hour=25)) or silently fell to a default.
            ("remind me at 25:99 tomorrow to review the PR", "25:99"),
            ("remind me at 13pm tomorrow to review the PR", "13pm"),
        ],
    )
    def test_unbindable_explicit_time_returns_none_with_honest_echo(self, message, echo):
        dt, label = parse_reminder_time(message)
        assert dt is None, (
            f"unbindable explicit time in {message!r} was guessed as {dt!r} — "
            "must return None so the handler can ask"
        )
        assert echo in label, f"label {label!r} must echo the unparsed time"

    @pytest.mark.asyncio
    async def test_handler_asks_on_unbindable_time_never_saves_default(self):
        """Handler honest path: explicit-but-unbindable time -> no todo is
        created, no 'scheduled' claim, the copy echoes the time and asks."""
        from services.domain.models import Intent
        from services.intent_service.todo_handlers import TodoIntentHandlers
        from services.shared_types import IntentCategory

        handlers = TodoIntentHandlers()
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_reminder",
            context={"original_message": "remind me at 25:99 tomorrow to review the PR"},
        )
        with patch.object(
            handlers.todo_service, "create_todo", new_callable=AsyncMock
        ) as mock_create:
            result = await handlers.handle_create_reminder(intent, "session-1", uuid4())

        assert not mock_create.called, (
            "handler saved a reminder despite an unbindable explicit time — "
            "the silent-default path the #1490 invariant forbids"
        )
        assert "25:99" in result, "honest path must echo the time it couldn't parse"
        assert "scheduled" not in result.lower()
        assert "?" in result, "honest path should ask for the time"

    @pytest.mark.asyncio
    async def test_handler_saves_pm_phrasing_at_15_00_not_morning(self):
        """End-to-end for PM's verbatim phrasing: reminder_date carries 15:00
        and the confirmation copy does NOT claim 'tomorrow morning'."""
        from services.domain.models import Intent, Todo
        from services.intent_service.todo_handlers import TodoIntentHandlers
        from services.shared_types import IntentCategory

        handlers = TodoIntentHandlers()
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_reminder",
            context={"original_message": "remind me at 3pm tomorrow to review the PR"},
        )
        mock_todo = Todo(
            id=str(uuid4()),
            text="review the pr",
            priority="medium",
            status="pending",
            completed=False,
        )
        with patch.object(
            handlers.todo_service,
            "create_todo",
            new_callable=AsyncMock,
            return_value=mock_todo,
        ) as mock_create:
            result = await handlers.handle_create_reminder(intent, "session-1", uuid4())

        assert mock_create.called
        saved = mock_create.call_args.kwargs.get("reminder_date")
        assert saved is not None
        assert (saved.hour, saved.minute) == (15, 0), (
            f"saved reminder_date {saved} dropped the explicit 3pm — this is "
            "the exact prod failure (row saved at 09:00)"
        )
        assert mock_create.call_args.kwargs.get("text") == "review the pr"
        assert (
            "morning" not in result.lower()
        ), f"confirmation copy claims a morning default: {result!r}"
        assert "3:00 pm" in result.lower() or "3pm" in result.lower()
        assert not re.search(r"\b(\w+)\s+\1\b", result.lower())


# ---------------------------------------------------------------------------
# #1493 companion: inverted-order path is timezone-aware local
# ---------------------------------------------------------------------------


class TestInvertedOrderTZAware1493:
    """The new inverted-order binding must honor #1493's aware-local rule:
    the returned datetime CARRIES the server-local offset (so timestamptz
    storage is UTC-normalized instead of drifting by the UTC offset)."""

    def test_inverted_order_reminder_is_aware_local(self):
        dt, label = parse_reminder_time("remind me at 3pm tomorrow to review the PR")
        assert dt is not None
        assert dt.tzinfo is not None, (
            "inverted-order path returned a NAIVE datetime — stored to "
            "timestamptz it drifts by the server's UTC offset (#1493)"
        )
        assert dt.utcoffset() == datetime.now().astimezone().utcoffset()
        assert dt.hour == 15  # 3pm server-LOCAL wall clock, per #1493 semantics


# ---------------------------------------------------------------------------
# #1562: "today" is an explicit DAY WORD — never silently becomes tomorrow
# ---------------------------------------------------------------------------


class TestTodayExplicitDayWord1562:
    """#1562 (PM live 8/10, 07:16 PT): "remind me at 9:41am today to check in
    with the Lead Developer" stored TUESDAY (tomorrow) 9:41 UTC.

    Two mechanisms: (a) parse_reminder_time had NO "today" branch — the
    generic clock branch's past-roll (`if dt <= now: dt += 1 day`) silently
    overrode the explicit day word; (b) the past-check runs on the SERVER
    clock (aware-local = UTC on fly), so at 14:16 UTC "9:41am" looked past
    while it was 2.5h in PM's future.

    The never-default rule (#1490 family) extended to day words: an explicit
    "today" NEVER yields a next-day date silently. Either it binds TODAY, or
    (genuinely past on the server clock) the parser returns
    (None, PAST_TODAY_PREFIX + time) and the handler ASKS "did you mean
    tomorrow?". The bare-clock branch (no day word) keeps its roll-forward.
    """

    PM_VERBATIM = "remind me at 9:41am today to check in with the Lead Developer"

    def test_pm_verbatim_binds_today_when_time_is_future(self, monkeypatch):
        """PM's exact phrasing, server wall clock 07:16 — must bind TODAY."""
        _freeze_parser_now(monkeypatch, datetime(2026, 8, 10, 7, 16))
        dt, label = parse_reminder_time(self.PM_VERBATIM)
        assert dt is not None, f"today-form parsed to None (label {label!r})"
        assert (dt.hour, dt.minute) == (9, 41)
        assert dt.date() == datetime(2026, 8, 10).date(), (
            f"explicit 'today' bound {dt.date()} — the silent tomorrow-roll " "PM hit live (#1562)"
        )
        assert label == "today at 9:41am"

    def test_pm_scenario_server_clock_past_asks_never_rolls(self, monkeypatch):
        """Server wall clock 14:16 (fly runs UTC — this is PM's actual live
        scenario: 9:41am read as past on the server while still future for
        PM). Honest ask, never a silent roll to tomorrow."""
        from services.intent_service.temporal_utils import PAST_TODAY_PREFIX

        _freeze_parser_now(monkeypatch, datetime(2026, 8, 10, 14, 16))
        dt, label = parse_reminder_time(self.PM_VERBATIM)
        assert dt is None, (
            f"explicit 'today' + past clock silently bound {dt} — must return "
            "the honest-ask shape (#1562)"
        )
        assert label == f"{PAST_TODAY_PREFIX}9:41am"

    @pytest.mark.parametrize(
        "message",
        [
            PM_VERBATIM,
            "remind me today at 9:41am to check in with the Lead Developer",
            "remind me at 9:41 today to check the deploy",
            "remind me today at 9:41 to check the deploy",
            "remind me at noon today to submit the report",
        ],
    )
    @pytest.mark.parametrize(
        "wall_clock",
        [datetime(2026, 8, 10, 7, 16), datetime(2026, 8, 10, 14, 16)],
    )
    def test_invariant_explicit_today_never_yields_next_day(self, monkeypatch, message, wall_clock):
        """THE #1562 INVARIANT: explicit 'today' never yields a next-day date
        without clarification — whatever the server clock says."""
        from services.intent_service.temporal_utils import PAST_TODAY_PREFIX

        _freeze_parser_now(monkeypatch, wall_clock)
        dt, label = parse_reminder_time(message)
        if dt is not None:
            assert dt.date() == wall_clock.date(), (
                f"{message!r} at server wall clock {wall_clock.time()} bound "
                f"{dt.date()} — explicit 'today' silently became another day"
            )
        else:
            assert label.startswith(PAST_TODAY_PREFIX), (
                f"{message!r} returned None without the past-today ask shape " f"(label {label!r})"
            )

    def test_bare_clock_no_day_word_keeps_roll_forward(self, monkeypatch):
        """No day word -> next-occurrence semantics are unchanged."""
        _freeze_parser_now(monkeypatch, datetime(2026, 8, 10, 14, 16))
        dt, label = parse_reminder_time("remind me at 9:41am to check in")
        assert dt is not None
        assert (dt.hour, dt.minute) == (9, 41)
        assert dt.date() == datetime(2026, 8, 11).date()  # rolled — correct here
        assert label == "at 9:41am"

    def test_bare_today_no_clock_asks_instead_of_tomorrow_default(self, monkeypatch):
        """'remind me today to X' used to fall through to the tomorrow-morning
        default — the same silent day-word override in vague form. Ask."""
        _freeze_parser_now(monkeypatch, datetime(2026, 8, 10, 7, 16))
        dt, label = parse_reminder_time("remind me today to check in with the Lead Developer")
        assert dt is None, (
            f"bare 'today' silently bound {dt} — the tomorrow-9am default "
            "overrides an explicit day word (#1562)"
        )
        assert label == "today"

    def test_todays_possessive_is_not_a_day_word(self, monkeypatch):
        """'today's report' is task text, not a time expression — the
        bare-clock branch (with its roll-forward) still owns this shape."""
        _freeze_parser_now(monkeypatch, datetime(2026, 8, 10, 14, 16))
        dt, label = parse_reminder_time("remind me to send today's report at 5pm")
        assert dt is not None
        assert (dt.hour, dt.minute) == (17, 0)
        assert dt.date() == datetime(2026, 8, 10).date()  # 5pm still future
        assert label == "at 5pm"

    @pytest.mark.asyncio
    async def test_handler_past_today_asks_never_saves(self, monkeypatch):
        """Handler honest path: past 'today' time -> no todo saved, no
        'scheduled' claim; copy echoes the time and asks about tomorrow."""
        from services.domain.models import Intent
        from services.intent_service.todo_handlers import TodoIntentHandlers
        from services.shared_types import IntentCategory

        _freeze_parser_now(monkeypatch, datetime(2026, 8, 10, 14, 16))
        handlers = TodoIntentHandlers()
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_reminder",
            context={"original_message": self.PM_VERBATIM},
        )
        with patch.object(
            handlers.todo_service, "create_todo", new_callable=AsyncMock
        ) as mock_create:
            result = await handlers.handle_create_reminder(intent, "session-1", uuid4())

        assert not mock_create.called, (
            "handler saved a reminder for a past 'today' time — the silent "
            "roll the #1562 invariant forbids"
        )
        assert "9:41am" in result, "ask must echo the time it couldn't bind"
        assert "already passed" in result.lower()
        assert "tomorrow" in result.lower(), "ask should offer tomorrow explicitly"
        assert "?" in result
        assert "scheduled" not in result.lower()
        assert "past-today:" not in result, "marker prefix must never leak to copy"

    @pytest.mark.asyncio
    async def test_handler_saves_pm_verbatim_today_and_copy_has_no_for_at(self, monkeypatch):
        """End-to-end green path: PM's phrasing at 07:16 saves TODAY 9:41 and
        the confirmation never reads '(scheduled for at 9:41am)' — the label
        already carried 'at' and the copy prepended 'for' (#1562 doublet)."""
        from services.domain.models import Intent, Todo
        from services.intent_service.todo_handlers import TodoIntentHandlers
        from services.shared_types import IntentCategory

        _freeze_parser_now(monkeypatch, datetime(2026, 8, 10, 7, 16))
        handlers = TodoIntentHandlers()
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_reminder",
            context={"original_message": self.PM_VERBATIM},
        )
        mock_todo = Todo(
            id=str(uuid4()),
            text="check in with the lead developer",
            priority="medium",
            status="pending",
            completed=False,
        )
        with patch.object(
            handlers.todo_service,
            "create_todo",
            new_callable=AsyncMock,
            return_value=mock_todo,
        ) as mock_create:
            result = await handlers.handle_create_reminder(intent, "session-1", uuid4())

        assert mock_create.called
        saved = mock_create.call_args.kwargs.get("reminder_date")
        assert saved is not None
        assert (saved.hour, saved.minute) == (9, 41)
        assert (
            saved.date() == datetime(2026, 8, 10).date()
        ), f"saved {saved} — 'today' must save TODAY, not tomorrow (#1562)"
        assert "for at " not in result, f"'(scheduled for at ...)' doublet: {result!r}"
        assert "today at 9:41am" in result

    @pytest.mark.asyncio
    async def test_bare_clock_confirmation_has_no_for_at_doublet(self, monkeypatch):
        """The doublet also hit the bare-clock label ('at 5pm') — copy must
        read 'scheduled for 5pm', never 'scheduled for at 5pm'."""
        from services.domain.models import Intent, Todo
        from services.intent_service.todo_handlers import TodoIntentHandlers
        from services.shared_types import IntentCategory

        _freeze_parser_now(monkeypatch, datetime(2026, 8, 10, 8, 0))
        handlers = TodoIntentHandlers()
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_reminder",
            context={"original_message": "remind me at 5pm to send the update"},
        )
        mock_todo = Todo(
            id=str(uuid4()),
            text="send the update",
            priority="medium",
            status="pending",
            completed=False,
        )
        with patch.object(
            handlers.todo_service,
            "create_todo",
            new_callable=AsyncMock,
            return_value=mock_todo,
        ) as mock_create:
            result = await handlers.handle_create_reminder(intent, "session-1", uuid4())

        assert mock_create.called
        assert "for at " not in result, f"'(scheduled for at ...)' doublet: {result!r}"
        assert "scheduled for 5pm" in result
