"""#2301: "what's in my <project>?" lists that project's open todos.

Arch 11-06 13:34: a project-scoped todo read reached through its own catalog line
(``list_project_todos``). The router names the project (``project`` arg); code
resolves it against the person's own active projects by exact name, as #2297 does,
and never guesses. CXO 11-06 11:14: ``Mobile Redesign has 2 open todos. Here they
are:`` then the main list's own lines; ``Mobile Redesign has no todos yet.``

LAYER: the rail adapter and the handler through their own functions, with the todo
service and the project read replaced at one seam each. No router, no database.
DENOMINATOR: one match (several, one, no todos), no arg, no match, several matches
(ask, number, re-ask), the main list's header unchanged, the registry rows.
"""

import types
from unittest.mock import AsyncMock, MagicMock

import pytest

from services.consciousness.todo_consciousness import format_todo_list_grouped
from services.domain.models import Intent
from services.intent_service import todo_project_attach as attach
from services.intent_service import workflow_entries
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.shared_types import IntentCategory

USER = "11111111-1111-1111-1111-111111111111"
MSG = "what's in my Mobile Redesign project?"


def _todo(tid, text, priority="medium"):
    return types.SimpleNamespace(
        id=tid, text=text, priority=priority, completed=False, status="pending"
    )


def _project(pid, name):
    return types.SimpleNamespace(id=pid, name=name)


def _service(by_project=None, store=True):
    h = TodoIntentHandlers.__new__(TodoIntentHandlers)
    calls = []

    async def list_todos(**kwargs):
        calls.append(kwargs)
        return list((by_project or {}).get(kwargs.get("project_id"), []))

    h.todo_service = MagicMock()
    h.todo_service.list_todos = AsyncMock(side_effect=list_todos)
    h._remember_todo_list_lines = MagicMock()
    h._calls = calls
    svc = types.SimpleNamespace(todo_handlers=h)
    if store:
        svc.workflow_offer_service = MagicMock()
    return svc


def _intent(args=None, message=MSG):
    ctx = {"original_message": message}
    if args is not None:
        ctx["inversion_args"] = args
    return Intent(
        original_message=message,
        category=IntentCategory.QUERY,
        action="list_project_todos",
        confidence=0.95,
        context=ctx,
    )


@pytest.fixture
def projects(monkeypatch):
    table = {USER: []}

    async def _active(user_id):
        return list(table.get(str(user_id), []))

    monkeypatch.setattr(attach, "_active_projects", _active)
    return table


async def _run(intent, svc):
    return await workflow_entries.run_list_project_todos_workflow(
        "s1", USER, {"intent": intent, "intent_service": svc}
    )


class TestOneProject:
    async def test_lists_that_projects_open_todos_under_cxos_header(self, projects):
        projects[USER] = [_project("p1", "Mobile Redesign"), _project("p2", "Other")]
        svc = _service(
            {
                "p1": [
                    _todo("a", "interview five current users"),
                    _todo("b", "audit the current navigation", "high"),
                ],
                "p2": [_todo("z", "not this one")],
            }
        )
        result = await _run(_intent({"project": "mobile redesign"}), svc)
        assert result.message == (
            "Mobile Redesign has 2 open todos. Here they are:\n"
            "1. interview five current users\n"
            "2. audit the current navigation (high)"
        )
        call = svc.todo_handlers._calls[0]
        assert call["project_id"] == "p1" and call["include_completed"] is False
        # The shown lines are recorded, so "complete the first one" binds to them.
        shown = svc.todo_handlers._remember_todo_list_lines.call_args.args[2]
        assert [t.id for t in shown] == ["a", "b"]

    async def test_one_line_reads_here_it_is_and_repeats_group(self, projects):
        projects[USER] = [_project("p1", "Launch")]
        svc = _service({"p1": [_todo("a", "review prs"), _todo("b", "review prs")]})
        result = await _run(_intent({"project": "Launch"}, "what's in Launch?"), svc)
        assert result.message == "Launch has 2 open todos. Here it is:\n1. review prs (×2)"

    async def test_a_capped_list_says_so_with_the_headers_noun(self, projects):
        """CXO 11-14: "todos", as the header says; never "tasks" in the same reply."""
        projects[USER] = [_project("p1", "Mobile Redesign")]
        svc = _service({})

        class _Page(list):
            capped = True

        svc.todo_handlers.todo_service.list_todos = AsyncMock(
            return_value=_Page([_todo("a", "one"), _todo("b", "two")])
        )
        result = await _run(_intent({"project": "Mobile Redesign"}), svc)
        assert result.message.endswith("\n\nShowing the first 2 todos in Mobile Redesign.")
        assert "tasks" not in result.message

    async def test_a_project_with_no_todos_says_so(self, projects):
        projects[USER] = [_project("p1", "Mobile Redesign")]
        svc = _service({})
        result = await _run(_intent({"project": "Mobile Redesign"}), svc)
        assert result.message == "Mobile Redesign has no todos yet."
        svc.todo_handlers._remember_todo_list_lines.assert_not_called()


class TestNothingToList:
    async def test_no_project_arg_is_a_statement_and_reads_nothing(self, monkeypatch):
        monkeypatch.setattr(attach, "_active_projects", AsyncMock(side_effect=AssertionError))
        svc = _service({})
        result = await _run(_intent({}), svc)
        assert result.message == attach.READ_NO_NAME_LINE
        assert "?" not in result.message  # a statement: nothing is armed
        assert svc.todo_handlers._calls == []
        svc.workflow_offer_service.set_pending_offer.assert_not_called()

    async def test_no_match_says_so_without_the_create_words(self, projects):
        projects[USER] = [_project("p1", "Mobile Redesign v2")]
        svc = _service({"p1": [_todo("a", "x")]})
        result = await _run(_intent({"project": "Mobile Redesign"}), svc)
        assert result.message == (
            'I couldn\'t find a project called "Mobile Redesign". '
            'Check the name, or say "show my projects".'
        )
        assert "added" not in result.message
        assert svc.todo_handlers._calls == []


class TestWordGuard:
    async def test_a_project_the_person_did_not_say_is_no_project(self, monkeypatch):
        """The same reader as create (Arch 11-14 ruling 1): a model-written name is
        never resolved and never shown."""
        monkeypatch.setattr(attach, "_active_projects", AsyncMock(side_effect=AssertionError))
        svc = _service({})
        result = await _run(_intent({"project": "Launch Plan"}, "what's in my project?"), svc)
        assert result.message == attach.READ_NO_NAME_LINE
        assert "Launch" not in result.message


class TestSeveralProjects:
    async def test_asks_the_armed_pick_and_a_number_shows_that_project(self, projects):
        projects[USER] = [_project("p1", "Mobile Redesign"), _project("p2", "mobile redesign")]
        svc = _service({"p2": [_todo("a", "interview five current users")]})
        result = await _run(_intent({"project": "Mobile Redesign"}), svc)
        assert result.message == (
            "I found more than one project with that name: 1. Mobile Redesign "
            "2. mobile redesign. Which one do you mean? Say the number."
        )
        assert svc.todo_handlers._calls == []
        record = svc.workflow_offer_service.set_pending_offer.call_args.args[1]
        payload = record["pending_action"]
        assert payload["kind"] == attach.TODO_PROJECT_PICK_KIND
        assert payload["purpose"] == attach.PURPOSE_READ
        assert payload["pick_ids"] == ["p1", "p2"] and payload["titles"] == []

        turn = await attach.handle_todo_project_pick_turn(record, "2", "s1", USER, svc)
        assert turn["message"] == (
            "mobile redesign has 1 open todo. Here it is:\n1. interview five current users"
        )
        assert turn["intent_data"]["action"] == "list_project_todos"
        assert svc.todo_handlers._calls[0]["project_id"] == "p2"

    async def test_bare_yes_reasks_with_the_read_question(self):
        svc = _service({})
        record = attach.build_pick_offer(
            USER,
            [attach.ProjectRef("p1", "A"), attach.ProjectRef("p2", "a")],
            [],
            "medium",
            MSG,
            purpose=attach.PURPOSE_READ,
        )
        out = await attach.run_clarify_todo_project_pick_workflow(
            "s1", USER, {"pending_action": record["pending_action"], "intent_service": svc}
        )
        assert out["message"].endswith("Which one do you mean? Say the number.")
        rearmed = svc.workflow_offer_service.set_pending_offer.call_args.args[1]
        assert rearmed["pending_action"]["purpose"] == attach.PURPOSE_READ
        assert rearmed["decline_message"] == attach.READ_PICK_DECLINE_LINE


class TestPurposesNeverCross:
    async def test_a_read_record_with_titles_injected_still_only_reads(self, projects):
        """Arch 11-14: one pick record, two purposes. A read pick never writes."""
        projects[USER] = [_project("p1", "A"), _project("p2", "a")]
        svc = _service({"p1": [_todo("t", "existing")]})
        svc.todo_handlers.todo_service.create_todo = AsyncMock(side_effect=AssertionError)
        svc.todo_handlers.create_titles_in_project = AsyncMock(side_effect=AssertionError)
        record = attach.build_pick_offer(
            USER,
            [attach.ProjectRef("p1", "A"), attach.ProjectRef("p2", "a")],
            ["injected title"],
            "medium",
            MSG,
            purpose=attach.PURPOSE_READ,
        )
        turn = await attach.handle_todo_project_pick_turn(record, "1", "s1", USER, svc)
        assert turn["message"] == "A has 1 open todo. Here it is:\n1. existing"
        assert "injected title" not in record["question"]

    async def test_no_store_for_a_read_pick_says_what_is_true(self, projects):
        projects[USER] = [_project("p1", "A"), _project("p2", "a")]
        svc = _service({}, store=False)
        result = await _run(_intent({"project": "A"}, "what's in A?"), svc)
        assert result.message == (
            "I found more than one project with that name, so I haven't listed anything."
        )
        assert svc.todo_handlers._calls == []

    def test_the_read_decline_says_what_will_not_happen(self):
        record = attach.build_pick_offer(
            USER, [attach.ProjectRef("p1", "A")], [], "medium", MSG, purpose=attach.PURPOSE_READ
        )
        assert record["decline_message"] == "Okay, I won't list anything."


class TestCreatedDateIsTheStoredDate:
    def test_the_label_is_the_rows_own_date_as_stored(self):
        import datetime as dt

        row = types.SimpleNamespace(
            id="p1",
            name="Launch",
            created_at=dt.datetime(2026, 11, 4, 3, 0, tzinfo=dt.timezone.utc),
        )
        assert attach.exact_matches([row], "launch")[0].created == "4 Nov"


class TestMainListUnchanged:
    def test_the_main_lists_header_is_what_it_was(self):
        todos = [_todo("a", "one"), _todo("b", "two")]
        assert format_todo_list_grouped(todos).splitlines()[0] == (
            "You have 2 open todos. Here they are:"
        )


class TestRegistry:
    def test_the_entry_reads_flips_with_the_todo_list_and_has_its_own_line(self):
        from services.intent_service.action_registry import ACTION_REGISTRY, ActionDisposition
        from services.intent_service.router_catalog_order import CATALOG_ORDER_LEDGER
        from services.intent_service.workflow_dispatcher import (
            EffectClass,
            get_action_workflows,
        )

        workflow_entries.register_default_workflows()
        entry = get_action_workflows()["list_project_todos"]
        assert entry.effect is EffectClass.READ
        assert entry.flip_group == "read_status"
        assert entry.description == (
            "List the open todos in ONE project the person names (\"what's in my Mobile "
            "Redesign project?\"); put that project's name in args as project, in their "
            "words. For all todos use list_todos_query; for how a project is going use "
            "get_project_status. (#2301)"
        )
        assert ACTION_REGISTRY[("QUERY", "list_project_todos")] is ActionDisposition.WORKFLOW
        # Append-only ledger: a new op goes at the END and moves no other line.
        assert CATALOG_ORDER_LEDGER[-1] == "list_project_todos"
