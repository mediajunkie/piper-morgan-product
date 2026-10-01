"""#1521: "what reminders do I have?" reaches the reminder LIST lane.

Before: no surface claimed the reminder-QUERY shape. The pre-classifier
returned None (probed 2026-08-08 — REMINDER_PATTERNS only cover CREATION
phrasings: "remind me to…", "set a reminder…"), so the utterance fell to the
LLM classifier, which misrouted it to the temporal/calendar lane — a signed-in
"what reminders do I have?" answered "Today is Saturday… (No meetings – great
day for deep work!)" while the stored reminder (todo_items.reminder_date, the
#1491 fetch path) was never consulted.

Now surface 1 claims the obvious query shapes deterministically →
QUERY/list_reminders_query → action rail → _handle_list_reminders_query →
TodoIntentHandlers.handle_list_reminders (owner-scoped, aware-UTC per
#1493/#1429).

Coverage shape mirrors #1471 (test_integration_connect_preclassifier_1417):
positive rows, the BLOCKER guard (creation phrasings stay create_reminder —
never over-claimed into the query lane), and regression rows (temporal + todo
routing unchanged).
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from services.domain.models import Intent, Todo
from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory
from tests.unit.services.intent_service._inversion_pin_helper import (
    assert_inversion_routes,
)


def _classify(msg: str):
    return PreClassifier.pre_classify(msg)


# ---------------------------------------------------------------------------
# Positive: obvious reminder-query shapes route deterministically (#1521)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "message",
    [
        "what reminders do I have?",
        "What reminders do I have",
        "list my reminders",
        "show my reminders",
        "show me my reminders",
        "what are my reminders?",
        "do I have any reminders?",
        "check my reminders",
        "view my reminders",
    ],
)
@pytest.mark.asyncio
async def test_reminder_query_routes_to_list_reminders(message, monkeypatch):
    """#1595 Phase 3 (2026-09-27): REMINDER_QUERY_PATTERNS' literals were
    deleted (scripts/inversion_phase3_deleted_patterns.json) — surface 1 no
    longer claims these phrases. Two-part pin: (a) surface 1 declines (the
    honest new fact — this phrase falls through to the Inversion, not to an
    unproven LLM guess), and (b) the Inversion routes it to
    list_reminders_query, deterministically (a stubbed router, no LLM)."""
    intent = _classify(message)
    assert intent is None, (
        f"REMINDER_QUERY_PATTERNS is deleted — pre-classifier should no "
        f"longer claim {message!r} (got {intent!r})"
    )
    routed = await assert_inversion_routes(
        monkeypatch,
        message,
        live_categories="read_status,create_reminder",
        expected_action="list_reminders_query",
    )
    assert routed.category == IntentCategory.QUERY


def test_multi_intent_path_no_longer_claims_reminder_query_1521():
    """#1595 Phase 3: the multi-intent path's claim of the reminder-query
    shape moved from a deterministic regex list (now empty) to the
    Inversion — see test_reminder_query_routes_to_list_reminders above for
    the routing half. This pin now records the honest new fact: surface 1's
    multi-intent path claims NOTHING for this phrase (never a phantom
    misclaim onto a sibling list)."""
    result = PreClassifier.detect_multiple_intents("what reminders do I have?")
    assert result.intents == [], f"multi-intent path resolved {result.intents} (#1595 Phase 3)"


@pytest.mark.asyncio
async def test_greeting_paired_reminder_query_keeps_both_parts(monkeypatch):
    """#1595 Phase 3: the greeting half still claims deterministically at
    surface 1; the reminder half no longer does (REMINDER_QUERY_PATTERNS
    deleted) — proven separately via the Inversion (isolating just the
    reminder phrase, per assert_inversion_routes's docstring: the stubbed
    router doesn't care about the surrounding greeting text). TEMPORAL must
    still never phantom-claim the reminder half — that guarantee is
    independent of REMINDER_QUERY_PATTERNS (TEMPORAL_PATTERNS never claimed
    reminder-query shapes) and still holds."""
    result = PreClassifier.detect_multiple_intents("hi piper, what reminders do I have?")
    actions = {i.action for i in result.intents}
    assert "list_reminders_query" not in actions, (
        "REMINDER_QUERY_PATTERNS is deleted — surface 1 should no longer " "claim the reminder half"
    )
    assert IntentCategory.TEMPORAL not in {i.category for i in result.intents}
    await assert_inversion_routes(
        monkeypatch,
        "what reminders do I have?",
        live_categories="read_status,create_reminder",
        expected_action="list_reminders_query",
    )


# ---------------------------------------------------------------------------
# Blocker guard (the load-bearing one): creation phrasings are NEVER
# over-claimed into the query lane — "remind me…" stays create_reminder.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "message",
    [
        "remind me to review PRs tomorrow",
        "remind me about the standup meeting",
        "set a reminder to check the build",
        "create a reminder to call Sam",
        "don't let me forget to send the memo",
        "I need to remember to call the vendor",
    ],
)
@pytest.mark.asyncio
async def test_creation_phrasings_stay_create_reminder(message, monkeypatch):
    """#1595 Phase 3: REMINDER_PATTERNS is deleted too, so surface 1 no
    longer claims these creation phrasings either — but the #1521 blocker
    guard's actual point (creation never gets hijacked into the QUERY
    listing lane) still needs proving. Two-part pin: (a) surface 1 declines
    for BOTH lanes (never claims list_reminders_query — the hijack this
    guard exists to prevent — and no longer claims create_reminder either,
    the honest new fact), and (b) the Inversion routes it to
    create_reminder, not the query lane."""
    intent = _classify(message)
    assert intent is None, (
        f"REMINDER_PATTERNS is deleted — pre-classifier should no longer "
        f"claim {message!r} (got {intent!r})"
    )
    routed = await assert_inversion_routes(
        monkeypatch,
        message,
        live_categories="read_status,create_reminder",
        expected_action="create_reminder",
    )
    assert (
        routed.action != "list_reminders_query"
    ), f"creation phrasing hijacked into the query lane: {message!r} (#1521 blocker guard)"


@pytest.mark.parametrize(
    "message",
    [
        "delete my reminders",
        "clear my reminders",
        "remove my reminders",
        "cancel my reminders",
    ],
)
def test_write_verb_phrasings_never_claim_query_lane(message):
    intent = _classify(message)
    if intent is not None:
        assert (
            intent.action != "list_reminders_query"
        ), f"write ask hijacked into reminder listing: {message!r}"


def test_multi_path_never_claims_creation_phrasing():
    result = PreClassifier.detect_multiple_intents("remind me to review PRs tomorrow")
    assert "list_reminders_query" not in {i.action for i in result.intents}


# ---------------------------------------------------------------------------
# Regression: temporal + todo routing unchanged
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "message,expected_action",
    [
        # #1595 Phase 3 fourth deletion (2026-10-01): TEMPORAL_PATTERNS is
        # now `[]` (tombstoned) — none of these three claim at surface 1 any
        # more. Converted to the decline+inversion-routes idiom (surface 1
        # declines, the stubbed Inversion still dispatches each to its
        # correct destination), not deleted — same idiom as this suite's own
        # test_todo_listing_unchanged below.
        ("what time is it", "get_current_time"),
        ("my appointments", "week_calendar"),
        ("show my calendar", "week_calendar"),
    ],
)
async def test_temporal_queries_unchanged(message, expected_action, monkeypatch):
    assert _classify(message) is None, f"surface 1 still claims: {message}"
    await assert_inversion_routes(
        monkeypatch,
        message,
        live_categories="read_temporal",
        expected_action=expected_action,
    )


@pytest.mark.asyncio
async def test_todo_listing_unchanged(monkeypatch):
    """#1595 Phase 3 (second deletion, 2026-09-27): TODO_QUERY_PATTERNS'
    literals were also deleted (scripts/inversion_phase3_deleted_patterns.json)
    — surface 1 no longer claims "show my todos" either. Same two-part pin
    as the reminder-query conversion above: (a) surface 1 declines, (b) the
    Inversion routes it to list_todos_query, deterministically."""
    intent = _classify("show my todos")
    assert intent is None, (
        f"TODO_QUERY_PATTERNS is deleted — pre-classifier should no longer "
        f"claim 'show my todos' (got {intent!r})"
    )
    routed = await assert_inversion_routes(
        monkeypatch,
        "show my todos",
        live_categories="read_status,create_reminder",
        expected_action="list_todos_query",
    )
    assert routed.category == IntentCategory.QUERY


# ---------------------------------------------------------------------------
# Rail + registry wiring (#1124 discipline: rail entry, no new elif)
# ---------------------------------------------------------------------------


def test_list_reminders_query_is_rail_registered():
    from services.intent_service.workflow_dispatcher import get_action_workflows
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()
    rail = get_action_workflows()
    for key in ("list_reminders_query", "list_reminders", "show_reminders", "get_reminders"):
        assert key in rail, f"rail key missing: {key} (#1521)"


def test_list_reminders_query_is_registry_canonical():
    from services.intent_service.action_registry import (
        ACTION_EXAMPLES,
        ACTION_REGISTRY,
        ACTION_TO_VERB,
        ActionDisposition,
        Verb,
    )

    assert ACTION_REGISTRY.get(("QUERY", "list_reminders_query")) is ActionDisposition.WORKFLOW
    assert ("QUERY", "list_reminders_query") in ACTION_EXAMPLES
    assert ACTION_TO_VERB.get("list_reminders_query") is Verb.LIST


def test_chat_pointer_pins_the_utterance_forever():
    """#1521 regression requirement (mirrors #1471's pin): the natural phrasing
    is a POINTER row, so the #1433 ratchet re-verifies deterministic resolution
    on every build."""
    from services.intent_service.chat_pointers import CHAT_POINTERS, POINTER

    pins = [
        row
        for row in CHAT_POINTERS.values()
        if isinstance(row, POINTER) and row.utterance == "what reminders do I have?"
    ]
    assert pins, "no CHAT_POINTERS row pins 'what reminders do I have?' (#1521)"
    assert pins[0].expects == ("query", "list_reminders_query")


# ---------------------------------------------------------------------------
# Handler: handle_list_reminders reads the stored reminders (owner-scoped,
# aware-UTC per #1493/#1429 — naive rows must not raise, they are assumed UTC)
# ---------------------------------------------------------------------------


def _todo(text, reminder_date=None, completed=False):
    return Todo(
        text=text,
        priority="medium",
        status="completed" if completed else "pending",
        completed=completed,
        reminder_date=reminder_date,
    )


@pytest.fixture
def todo_handlers():
    from services.intent_service.todo_handlers import TodoIntentHandlers

    return TodoIntentHandlers()


def _intent(message):
    return Intent(
        category=IntentCategory.QUERY,
        action="list_reminders_query",
        confidence=1.0,
        original_message=message,
        context={"original_message": message},
    )


@pytest.mark.asyncio
async def test_handle_list_reminders_lists_only_reminder_todos(todo_handlers):
    user_id = uuid4()
    now = datetime.now(timezone.utc)
    todos = [
        _todo("overdue thing", reminder_date=now - timedelta(hours=2)),
        _todo("upcoming thing", reminder_date=now + timedelta(days=1)),
        _todo("plain todo with no reminder"),
    ]
    with patch.object(
        todo_handlers.todo_service, "list_todos", new_callable=AsyncMock, return_value=todos
    ) as mock_list:
        result = await todo_handlers.handle_list_reminders(
            _intent("what reminders do I have?"), "session-1", user_id
        )
    # Owner-scoped read (#1493): the query runs as THIS user, nobody else.
    assert mock_list.call_args.kwargs.get("user_id") == user_id
    assert "overdue thing" in result
    assert "upcoming thing" in result
    assert "plain todo with no reminder" not in result


@pytest.mark.asyncio
async def test_handle_list_reminders_naive_rows_assumed_utc(todo_handlers):
    """#1491/#1429 guard shape: a tz-naive reminder_date (SQLite-style) must
    not raise TypeError against the aware now() — it is assumed UTC."""
    user_id = uuid4()
    naive_past = datetime.utcnow() - timedelta(hours=3)
    todos = [_todo("naive-row reminder", reminder_date=naive_past)]
    with patch.object(
        todo_handlers.todo_service, "list_todos", new_callable=AsyncMock, return_value=todos
    ):
        result = await todo_handlers.handle_list_reminders(
            _intent("what reminders do I have?"), "session-1", user_id
        )
    assert "naive-row reminder" in result


@pytest.mark.asyncio
async def test_handle_list_reminders_empty_is_honest(todo_handlers):
    """Pattern-073 discipline: say what was actually queried — no categorical
    'nothing scheduled', and no calendar/current-time impersonation."""
    with patch.object(
        todo_handlers.todo_service, "list_todos", new_callable=AsyncMock, return_value=[]
    ):
        result = await todo_handlers.handle_list_reminders(
            _intent("what reminders do I have?"), "session-1", uuid4()
        )
    assert "reminder" in result.lower()
    assert "great day for deep work" not in result.lower()


@pytest.mark.asyncio
async def test_handle_list_reminders_failure_is_honest(todo_handlers):
    """Source failure reads as trouble-loading, never as 'no reminders' (#1425)."""
    with patch.object(
        todo_handlers.todo_service,
        "list_todos",
        new_callable=AsyncMock,
        side_effect=RuntimeError("db down"),
    ):
        result = await todo_handlers.handle_list_reminders(
            _intent("what reminders do I have?"), "session-1", uuid4()
        )
    assert "trouble" in result.lower()
    assert "don't have any" not in result.lower()
