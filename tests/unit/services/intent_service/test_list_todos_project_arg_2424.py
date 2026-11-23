"""Issue 2424: ``list_todos_query`` with the router's ``project`` arg shows that project.

Arch 2026-11-23 (01M84VG8MN), handler only. On ``list_todos_query`` (not its two rail
siblings), a router ``project`` arg that passes 2297's word-set guard is resolved by
2297's ``resolve``: exactly one match shows that project's open todos by 2413's
``show_project_todos`` (2301's render); several, none, no projects or a failed project
read say what 2413's own entry says for that case; no arg, or a refused one, is today's
reply through the unchanged existing call. Nothing is written.

LAYER: the rail entry point ``run_todo_query_workflow`` (what the rail calls for all
three keys), with the project read replaced at one seam (``attach._active_projects``),
the todo service stubbed under the real 2301 render, and ``_handle_execution_intent``
(today's path) a recorded stub. No router call, no model call, no database.
DENOMINATOR: one match (list, stored-name header for an other-case arg and a trailing
"project", no open todos, a failed todo read); several, none, no projects, a failed
project read (each equal to 2413's entry and arming where it arms); a refused arg; no
arg; the two sibling actions with an arg; nothing written in every case; the entry
shape (one entry object, one entry point, for all three keys).
"""

import types
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.exc import OperationalError

from services.domain.models import Intent
from services.intent_service import project_status_todos as pst
from services.intent_service import project_todos_read as ptr
from services.intent_service import todo_project_attach as attach
from services.intent_service import workflow_entries
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.shared_types import IntentCategory

USER = "24240000-0000-4000-8000-000000002424"
SESSION = "s2424"
ASK = "can you show me the tasks in the Launch project?"
TODAY = object()  # today's reply, as the stubbed existing path returns it


def _project(pid, name, created=None):
    return types.SimpleNamespace(id=pid, name=name, created_at=created)


def _todo(tid, text, priority="medium"):
    return types.SimpleNamespace(
        id=tid, text=text, priority=priority, completed=False, status="pending"
    )


def _handlers(by_project=None, fail=None):
    """The real 2301 render with the todo service stubbed; every write an AsyncMock."""
    h = TodoIntentHandlers.__new__(TodoIntentHandlers)
    reads = []

    async def list_todos(**kwargs):
        reads.append(kwargs)
        if fail is not None:
            raise fail
        return (by_project or {}).get(kwargs.get("project_id"), [])

    h.todo_service = MagicMock()
    h.todo_service.list_todos = AsyncMock(side_effect=list_todos)
    h._remember_todo_list_lines = MagicMock()
    h.create_titles_in_project = AsyncMock()
    h.create_titles_without_project = AsyncMock()
    h._reads = reads
    return h


def _assert_nothing_written(svc):
    h = svc.todo_handlers
    for name in ("create_todo", "update_todo", "delete_todo", "complete_todo"):
        getattr(h.todo_service, name).assert_not_called()
    h.create_titles_in_project.assert_not_called()
    h.create_titles_without_project.assert_not_called()


def _service(handlers=None, store=True):
    svc = types.SimpleNamespace(todo_handlers=handlers or _handlers())
    svc._handle_execution_intent = AsyncMock(return_value=TODAY)
    if store:
        svc.workflow_offer_service = MagicMock()
    return svc


def _intent(action="list_todos_query", project="Launch", message=ASK):
    context = {"original_message": message}
    if project is not None:
        context["inversion_args"] = {"project": project}
    return Intent(
        original_message=message,
        category=IntentCategory.QUERY,
        action=action,
        confidence=0.9,
        context=context,
    )


@pytest.fixture
def projects(monkeypatch):
    """The person's active projects by user id: the one seam for the project read."""
    table = {USER: []}

    async def _active(user_id):
        rows = table.get(str(user_id), [])
        if isinstance(rows, Exception):
            raise rows
        return list(rows)

    monkeypatch.setattr(attach, "_active_projects", _active)
    return table


async def _run(intent, svc):
    return await workflow_entries.run_todo_query_workflow(
        SESSION, USER, {"intent": intent, "intent_service": svc}
    )


async def _via_2413(intent, svc):
    return await ptr.run_list_project_todos_workflow(
        SESSION, USER, {"intent": intent, "intent_service": svc}
    )


def _armed(svc):
    calls = svc.workflow_offer_service.set_pending_offer.call_args_list
    return calls[-1].args[1] if calls else None


LAUNCH_TODOS = {"p1": [_todo("a", "book the venue"), _todo("b", "send invites", "high")]}


# -- exactly one match ---------------------------------------------------------------


class TestOneMatch:
    async def test_shows_that_projects_open_todos_and_not_the_full_list(self, projects):
        projects[USER] = [_project("p1", "Launch"), _project("p2", "Website Refresh")]
        svc = _service(_handlers(LAUNCH_TODOS))
        result = await _run(_intent(), svc)
        expected = await svc.todo_handlers.project_status_todos(
            SESSION, attach_principal(), attach.ProjectRef(id="p1", name="Launch")
        )
        assert result.message == expected
        assert result.message.startswith("Open todos in Launch:")
        assert "book the venue" in result.message and "send invites" in result.message
        assert result.success is True
        assert result.requires_clarification is False
        assert result.intent_data == {"category": "query", "action": "list_todos_query"}
        svc._handle_execution_intent.assert_not_called()
        assert [r["project_id"] for r in svc.todo_handlers._reads] == ["p1", "p1"]
        svc.workflow_offer_service.set_pending_offer.assert_not_called()
        _assert_nothing_written(svc)

    @pytest.mark.parametrize(
        "arg,message",
        [
            ("launch", "show me the tasks in the launch project"),
            ("Launch project", ASK),
            ("LAUNCH PROJECT", "show me the tasks in the LAUNCH PROJECT"),
        ],
    )
    async def test_the_header_names_the_stored_project(self, projects, arg, message):
        projects[USER] = [_project("p1", "Launch")]
        svc = _service(_handlers(LAUNCH_TODOS))
        result = await _run(_intent(project=arg, message=message), svc)
        assert result.message.splitlines()[0] == "Open todos in Launch:"
        svc._handle_execution_intent.assert_not_called()
        _assert_nothing_written(svc)

    async def test_the_shown_lines_are_recorded_as_the_last_numbered_list(self, projects):
        projects[USER] = [_project("p1", "Launch")]
        svc = _service(_handlers(LAUNCH_TODOS))
        await _run(_intent(), svc)
        svc.todo_handlers._remember_todo_list_lines.assert_called_once()

    async def test_no_open_todos_says_the_standalone_line(self, projects):
        projects[USER] = [_project("p1", "Launch")]
        svc = _service(_handlers({}))
        result = await _run(_intent(project="launch project"), svc)
        assert result.message == "Launch has no open todos."
        assert result.message == ptr.NO_OPEN_TODOS_STANDALONE_LINE.format(project="Launch")
        svc._handle_execution_intent.assert_not_called()
        _assert_nothing_written(svc)

    @pytest.mark.parametrize("raised", [OperationalError("x", {}, Exception()), OSError("down")])
    async def test_a_failed_todo_read_says_2301s_line(self, projects, raised):
        projects[USER] = [_project("p1", "Launch")]
        svc = _service(_handlers(fail=raised))
        result = await _run(_intent(), svc)
        assert result.message == pst.TODOS_READ_FAILED_LINE
        assert result.message == "I couldn't check its todos just now."
        svc._handle_execution_intent.assert_not_called()
        _assert_nothing_written(svc)


def attach_principal():
    from services.intent.intent_service import _coerce_todo_principal

    return _coerce_todo_principal(USER)


# -- not exactly one: what 2413's own entry says --------------------------------------


class TestAsWithout2413:
    @pytest.mark.parametrize(
        "rows,arms",
        [
            # several: two projects share the name
            ([_project("p1", "Launch"), _project("p2", "launch")], True),
            # none: projects exist, none is called Launch
            ([_project("p3", "Website Refresh"), _project("p4", "Hiring")], True),
            # no projects at all
            ([], False),
        ],
        ids=["several", "none", "no-projects"],
    )
    async def test_equals_2413s_entry_and_arms_where_it_arms(self, projects, rows, arms):
        projects[USER] = rows
        ours, theirs = _service(), _service()
        intent = _intent()
        result = await _run(intent, ours)
        expected = await _via_2413(intent, theirs)
        assert result == expected
        assert _armed(ours) == _armed(theirs)
        assert (_armed(ours) is not None) is arms
        if arms:
            assert result.requires_clarification is True
            assert _armed(ours)["pending_action"]["kind"] == ptr.PROJECT_TODOS_PICK_KIND
            assert _armed(ours)["pending_action"]["pick_ids"] == [r.id for r in rows]
        ours._handle_execution_intent.assert_not_called()
        assert ours.todo_handlers._reads == []
        _assert_nothing_written(ours)

    async def test_several_is_the_listed_question_not_a_cant_find_line(self, projects):
        projects[USER] = [_project("p1", "Launch"), _project("p2", "launch")]
        svc = _service()
        result = await _run(_intent(), svc)
        assert result.message == (
            "Which project's todos do you want? Your projects: Launch, launch. "
            "Tell me the name and I'll show them."
        )
        assert "can't find" not in result.message

    async def test_no_match_is_the_listed_question(self, projects):
        projects[USER] = [_project("p3", "Website Refresh"), _project("p4", "Hiring")]
        result = await _run(_intent(), _service())
        assert result.message == (
            "Which project's todos do you want? Your projects: Website Refresh, Hiring. "
            "Tell me the name and I'll show them."
        )

    async def test_no_projects_is_2413s_line(self, projects):
        result = await _run(_intent(), _service())
        assert result.message == ptr.NO_PROJECTS_LINE

    @pytest.mark.parametrize("raised", [OperationalError("x", {}, Exception()), OSError("down")])
    async def test_a_failed_project_read_equals_2413s_entry(self, projects, raised):
        projects[USER] = raised
        ours, theirs = _service(), _service()
        intent = _intent()
        result = await _run(intent, ours)
        expected = await _via_2413(intent, theirs)
        assert result == expected
        assert result.message == "I couldn't check your projects just now."
        ours.workflow_offer_service.set_pending_offer.assert_not_called()
        ours._handle_execution_intent.assert_not_called()
        _assert_nothing_written(ours)

    async def test_the_armed_question_is_answered_by_2413s_answer_turn(self, projects):
        projects[USER] = [_project("p3", "Website Refresh"), _project("p1", "Launch Plan")]
        svc = _service(_handlers({"p3": [_todo("c", "pick a font")]}))
        await _run(_intent(), svc)
        reply = await ptr.handle_project_todos_pick_turn(
            _armed(svc), "Website Refresh", session_id=SESSION, user_id=USER, intent_service=svc
        )
        assert reply["message"].startswith("Open todos in Website Refresh:")
        _assert_nothing_written(svc)


# -- today's reply ---------------------------------------------------------------------


class TestTodaysReply:
    async def test_no_arg_is_todays_call_exactly_once(self, projects):
        projects[USER] = [_project("p1", "Launch")]
        svc = _service()
        intent = _intent(project=None)
        result = await _run(intent, svc)
        assert result is TODAY
        svc._handle_execution_intent.assert_awaited_once_with(intent, None, SESSION, USER)
        svc.workflow_offer_service.set_pending_offer.assert_not_called()
        assert svc.todo_handlers._reads == []
        _assert_nothing_written(svc)

    @pytest.mark.parametrize("arg", ["", "   ", 7, None])
    async def test_an_empty_or_non_string_arg_is_todays_reply(self, projects, arg):
        projects[USER] = [_project("p1", "Launch")]
        svc = _service()
        intent = _intent()
        intent.context["inversion_args"] = {"project": arg}
        assert await _run(intent, svc) is TODAY
        svc._handle_execution_intent.assert_awaited_once_with(intent, None, SESSION, USER)

    async def test_an_arg_the_guard_refuses_is_todays_reply(self, projects, monkeypatch):
        """The arg names a word the person did not say: no arg. Nothing is read."""
        reads = AsyncMock(side_effect=AssertionError("project read on a refused arg"))
        monkeypatch.setattr(attach, "_active_projects", reads)
        svc = _service()
        intent = _intent(project="Mobile Redesign", message="show me my todos")
        assert await _run(intent, svc) is TODAY
        svc._handle_execution_intent.assert_awaited_once_with(intent, None, SESSION, USER)
        reads.assert_not_called()
        _assert_nothing_written(svc)

    @pytest.mark.parametrize("action", ["list_completed_todos", "next_todo_query"])
    async def test_the_sibling_actions_ignore_the_arg(self, projects, monkeypatch, action):
        reads = AsyncMock(side_effect=AssertionError("project read on a sibling action"))
        monkeypatch.setattr(attach, "_active_projects", reads)
        svc = _service()
        intent = _intent(action=action)
        assert await _run(intent, svc) is TODAY
        svc._handle_execution_intent.assert_awaited_once_with(intent, None, SESSION, USER)
        reads.assert_not_called()
        _assert_nothing_written(svc)

    async def test_no_principal_is_todays_reply(self, projects):
        svc = _service()
        intent = _intent()
        out = await workflow_entries.run_todo_query_workflow(
            SESSION, None, {"intent": intent, "intent_service": svc}
        )
        assert out is TODAY
        svc._handle_execution_intent.assert_awaited_once_with(intent, None, SESSION, None)


# -- the entry shape -------------------------------------------------------------------


class TestEntryShape:
    def test_the_three_keys_keep_one_entry_and_one_entry_point(self):
        from services.intent_service.workflow_dispatcher import get_action_workflows

        workflow_entries.register_default_workflows()
        rail = get_action_workflows()
        entry = rail["list_todos_query"]
        assert rail["list_completed_todos"] is entry
        assert rail["next_todo_query"] is entry
        assert entry.entry_point is workflow_entries.run_todo_query_workflow
        assert rail["create_reminder"].entry_point is workflow_entries.run_todo_query_workflow
        assert entry.router_visible is True
