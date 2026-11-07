"""ADR-083 (PROPOSED; Arch 11-06 16:21: wording (i), D1a, D3a). Built on a branch for the
screen's arm C; it reaches main only after the screen passes and xian's veto window closes.

D1: one fact, the last numbered list's kind and line count, nothing else. D1a: one field
in the live session snapshot. D3a: it renders only when the list was shown in the turn
right before this message. Absent, the snapshot (and so the router call) is byte-identical
to main's."""

from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from services.intent_service.conversation_context import (
    NumberedList,
    get_or_create_context,
)
from services.intent_service.session_snapshot import SessionSnapshot, serialize_for_prompt
from services.intent_service.snapshot_assembly import _last_list_fact, _list_kind


def _ctx(sid, turns_ago_list_shown, n_turns=2, kind="active todos", lines=7):
    ctx = get_or_create_context(sid, "u-adr083")
    ctx.turns.clear()
    # Relative to now: the context prunes turns past its age window (max_age_minutes).
    base = datetime.now() - timedelta(minutes=n_turns + 1)
    for i in range(n_turns):
        turn = ctx.add_turn(message=f"m{i}")
        turn.timestamp = base + timedelta(minutes=i)
    shown = base + timedelta(minutes=n_turns - 1 - turns_ago_list_shown, seconds=30)
    ctx.last_numbered_list = NumberedList(
        kind=kind,
        ids=[str(uuid4()) for _ in range(lines)],
        texts=[f"t{i}" for i in range(lines)],
        shown_at=shown,
    )
    return ctx


def test_wording_i_is_the_bare_fact():
    snap = SessionSnapshot(last_list_kind="todos", last_list_lines=7)
    assert serialize_for_prompt(snap) == "LAST LIST SHOWN: 7 numbered todos"


def test_absent_is_byte_identical():
    """Arm C's absent half: no list fact, no line; the empty snapshot still renders ""."""
    assert serialize_for_prompt(SessionSnapshot()) == ""
    assert serialize_for_prompt(SessionSnapshot(last_list_kind="todos")) == ""


@pytest.mark.parametrize(
    "kind,expected",
    [
        ("active todos", "todos"),
        ("active to-dos", "todos"),
        ("reminders", "reminders"),
        ("due reminders", "reminders"),
        ("issues", None),
    ],
)
def test_kind_is_normalized(kind, expected):
    assert _list_kind(kind) == expected


def test_shown_in_the_previous_turn_renders():
    _ctx("s-adr083-a", turns_ago_list_shown=1)
    assert _last_list_fact("s-adr083-a", "u-adr083", set()) == ("todos", 7)


def test_shown_two_turns_ago_expires():
    """D3a: any reply in between (a topic switch, an unrelated answer) drops it."""
    _ctx("s-adr083-b", turns_ago_list_shown=2, n_turns=3)
    assert _last_list_fact("s-adr083-b", "u-adr083", set()) == (None, None)


def test_no_previous_turn_renders_nothing():
    _ctx("s-adr083-c", turns_ago_list_shown=0, n_turns=1)
    assert _last_list_fact("s-adr083-c", "u-adr083", set()) == (None, None)


def test_a_kind_outside_the_todo_family_renders_nothing():
    _ctx("s-adr083-d", turns_ago_list_shown=1, kind="issues")
    assert _last_list_fact("s-adr083-d", "u-adr083", set()) == (None, None)


def test_no_session_renders_nothing():
    assert _last_list_fact(None, "u-adr083", set()) == (None, None)
