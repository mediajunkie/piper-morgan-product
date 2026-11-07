"""ADR-083 D5 (PROPOSED; Arch 11-06 17:29, 17:52): a second router call only on CLARIFY
with a list in scope, accepted only as the list family's op with positions. Branch only,
for the screen."""

import asyncio
from types import SimpleNamespace

import pytest

from services.intent_service import list_consult as lc
from services.intent_service.session_snapshot import SessionSnapshot, serialize_for_prompt

_SNAP = SessionSnapshot(last_list_kind="todos", last_list_lines=7)


class _State:
    def __init__(self, state_block):
        self.state_block = state_block


_CLARIFY = SimpleNamespace(outcome="clarify", operation=None, args={})


def _op(operation, targets, outcome="operation"):
    return SimpleNamespace(outcome=outcome, operation=operation, args={"targets": targets})


@pytest.mark.parametrize("token", ["1", "7", "2-4", "first", "last", "Last"])
def test_positions(token):
    assert lc.is_position(token, 7)


@pytest.mark.parametrize("token", ["all", "0", "8", "3-9", "4-2", "review prs", "", None, 2])
def test_not_positions(token):
    assert not lc.is_position(token, 7)


def test_accepts_only_the_family_op_with_positions():
    assert lc.accepts(_op("delete_todo", ["1", "2"]), "todos", 7)
    assert lc.accepts(_op("complete_todo", ["last"]), "todos", 7)
    assert not lc.accepts(_op("complete_todo", ["all"]), "todos", 7)  # Arch 17:52
    assert not lc.accepts(_op("list_projects", ["1"]), "todos", 7)
    assert not lc.accepts(_op("delete_todo", []), "todos", 7)
    assert not lc.accepts(_op("delete_todo", ["1"]), "issues", 7)
    assert not lc.accepts(_CLARIFY, "todos", 7)


def test_the_main_calls_block_never_carries_the_list_fact():
    assert serialize_for_prompt(lc.without_list_fact(_SNAP)) == ""
    assert serialize_for_prompt(_SNAP) == "LAST LIST SHOWN: 7 numbered todos"


def _route(answer, seen):
    async def route(message, session_state, **kw):
        seen.append(session_state.state_block if session_state else None)
        if isinstance(answer, BaseException):
            raise answer
        if answer == "slow":
            await asyncio.sleep(5)
        return answer

    return route


def _consult(decision, snapshot, route):
    return asyncio.run(
        lc.consult_on_clarify(
            "delete the first two",
            decision,
            snapshot,
            route=route,
            router_snapshot=_State,
            llm_service=None,
            grammar=None,
            user_id="u",
        )
    )


def test_clarify_with_a_list_asks_once_with_the_slot_and_accepts():
    seen = []
    second = _op("delete_todo", ["1", "2"])
    assert _consult(_CLARIFY, _SNAP, _route(second, seen)) is second
    assert seen == ["LAST LIST SHOWN: 7 numbered todos"]


def test_an_all_target_keeps_the_clarify():
    assert _consult(_CLARIFY, _SNAP, _route(_op("complete_todo", ["all"]), [])) is _CLARIFY


def test_a_non_clarify_decision_is_never_reconsulted():
    seen = []
    first = _op("list_projects", [])
    assert _consult(first, _SNAP, _route(_op("delete_todo", ["1"]), seen)) is first
    assert seen == []


def test_no_list_in_scope_is_never_reconsulted():
    seen = []
    assert (
        _consult(_CLARIFY, SessionSnapshot(), _route(_op("delete_todo", ["1"]), seen)) is _CLARIFY
    )
    assert seen == []


def test_a_failed_second_call_keeps_the_clarify():
    assert _consult(_CLARIFY, _SNAP, _route(RuntimeError("boom"), [])) is _CLARIFY


def test_a_slow_second_call_times_out_to_the_clarify(monkeypatch):
    from services.intent_service import todo_handlers

    monkeypatch.setattr(todo_handlers, "SELECTOR_CEILING_S", 0.05)
    assert _consult(_CLARIFY, _SNAP, _route("slow", [])) is _CLARIFY
