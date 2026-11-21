"""#2301, handler-only: a status ask that names one project shows its open todos.

Arch 2026-11-20 (01M7Y2ZP7C, corrected by 01M7Y3JVMS) and CXO (01M7Y2W1YE,
01M7Y3EYRS), after two ``list_project_todos`` catalog wordings failed rule 7. No
catalog text changes: the read hangs off ``get_project_status`` and the router's
own ``project`` arg.

LAYER: ``status_todos_block`` and the handler method through their own functions,
with the todo service and the project read replaced at one seam each; the call
site's order read from source. No router call, no floor call, no database.
DENOMINATOR: no arg, one match (todos, none, capped, a failed todo read), several,
no match, no projects, a failed project read, another op, no principal; the header
names the stored project; the main list's header unchanged; the block's place
after the floor and after the milestone branch; the request pin and the grammar.
"""

import hashlib
import types
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.exc import OperationalError

from services.consciousness.todo_consciousness import format_todo_list_grouped
from services.domain.models import Intent
from services.intent_service import project_status_todos as pst
from services.intent_service import todo_project_attach as attach
from services.intent_service import workflow_entries
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.shared_types import IntentCategory

REPO = Path(__file__).resolve().parents[4]
USER = "11111111-1111-1111-1111-111111111111"
T4 = "what's in my Mobile Redesign project?"
T6 = "what's left to do in Mobile Redesign"
N3 = "how is the Mobile Redesign project going?"


def _todo(tid, text, priority="medium"):
    return types.SimpleNamespace(
        id=tid, text=text, priority=priority, completed=False, status="pending"
    )


def _project(pid, name):
    return types.SimpleNamespace(id=pid, name=name)


def _handlers(by_project=None, fail=None):
    h = TodoIntentHandlers.__new__(TodoIntentHandlers)
    calls = []

    async def list_todos(**kwargs):
        calls.append(kwargs)
        if fail is not None:
            raise fail
        return (by_project or {}).get(kwargs.get("project_id"), [])

    h.todo_service = MagicMock()
    h.todo_service.list_todos = AsyncMock(side_effect=list_todos)
    h._remember_todo_list_lines = MagicMock()
    h._calls = calls
    return h


def _intent(message=T6, args=None, action="get_project_status"):
    ctx = {"original_message": message}
    if args is not None:
        ctx["inversion_args"] = args
    return Intent(
        original_message=message,
        category=IntentCategory.STATUS,
        action=action,
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


async def _block(intent, handlers, user=USER):
    return await pst.status_todos_block(intent, "s1", user, handlers)


class TestOneProject:
    @pytest.mark.parametrize("message", [T4, T6, N3])
    async def test_every_named_project_status_ask_gets_the_block(self, projects, message):
        # Arch's condition 4: code cannot tell T4 from N3, so all of them get it.
        projects[USER] = [_project("p1", "Mobile Redesign"), _project("p2", "Launch")]
        h = _handlers({"p1": [_todo("a", "book the venue"), _todo("b", "draft the brief", "high")]})
        block = await _block(_intent(message, {"project": "Mobile Redesign"}), h)
        assert block == (
            "Open todos in Mobile Redesign:\n1. book the venue\n2. draft the brief (high)"
        )
        assert h._calls == [
            {"user_id": h._calls[0]["user_id"], "include_completed": False, "project_id": "p1"}
        ]

    async def test_the_shown_lines_are_recorded_as_the_last_numbered_list(self, projects):
        projects[USER] = [_project("p1", "Mobile Redesign")]
        todos = [_todo("a", "x"), _todo("b", "y")]
        h = _handlers({"p1": todos})
        await _block(_intent(args={"project": "Mobile Redesign"}), h)
        session, _user, recorded = h._remember_todo_list_lines.call_args.args
        assert session == "s1" and list(recorded) == todos

    async def test_the_header_names_the_stored_project(self, projects):
        # CXO: "Launch project" typed against a stored "Launch" shows what matched.
        projects[USER] = [_project("p1", "Launch")]
        h = _handlers({"p1": [_todo("a", "x")]})
        message = "what's in my launch project?"
        block = await _block(_intent(message, {"project": "launch project"}), h)
        assert block.startswith("Open todos in Launch:\n1. x")

    async def test_repeats_group_as_the_main_list_groups_them(self, projects):
        projects[USER] = [_project("p1", "Mobile Redesign")]
        h = _handlers({"p1": [_todo("a", "review prs"), _todo("b", "review prs")]})
        block = await _block(_intent(args={"project": "Mobile Redesign"}), h)
        assert block == "Open todos in Mobile Redesign:\n1. review prs (×2)"

    async def test_no_open_todos_says_so(self, projects):
        projects[USER] = [_project("p1", "Mobile Redesign")]
        h = _handlers({})
        assert await _block(_intent(args={"project": "Mobile Redesign"}), h) == (
            "No open todos in it."
        )
        h._remember_todo_list_lines.assert_not_called()

    async def test_a_capped_list_says_so(self, projects):
        class _Page(list):
            capped = True

        projects[USER] = [_project("p1", "Mobile Redesign")]
        h = _handlers({"p1": _Page([_todo("a", "x"), _todo("b", "y")])})
        block = await _block(_intent(args={"project": "Mobile Redesign"}), h)
        assert block.endswith("\n\nShowing the first 2 todos in Mobile Redesign.")

    @pytest.mark.parametrize(
        "error", [OSError("down"), OperationalError("select", {}, Exception())]
    )
    async def test_a_failed_todo_read_says_cxos_line_and_no_partial_list(self, projects, error):
        projects[USER] = [_project("p1", "Mobile Redesign")]
        h = _handlers(fail=error)
        block = await _block(_intent(args={"project": "Mobile Redesign"}), h)
        assert block == "I couldn't check its todos just now."
        h._remember_todo_list_lines.assert_not_called()


class TestNothingIsAdded:
    """Arch's condition 2: today's reply, no block and no question."""

    async def test_no_project_arg_reads_nothing(self, monkeypatch):
        # T4 carries no arg 2 of 6 on main; code never reads the name from words.
        monkeypatch.setattr(attach, "_active_projects", AsyncMock(side_effect=AssertionError))
        h = _handlers({})
        assert await _block(_intent(T4, {}), h) == ""
        assert await _block(_intent(T4), h) == ""
        assert h._calls == []

    async def test_an_arg_the_person_did_not_say_is_no_arg(self, monkeypatch):
        monkeypatch.setattr(attach, "_active_projects", AsyncMock(side_effect=AssertionError))
        h = _handlers({})
        assert await _block(_intent("how is it going?", {"project": "Launch"}), h) == ""

    @pytest.mark.parametrize(
        "stored",
        [
            ["Mobile Redesign", "mobile redesign"],  # several
            ["Mobile Redesign v2"],  # no match
            [],  # no projects
        ],
    )
    async def test_several_none_or_no_projects(self, projects, stored):
        projects[USER] = [_project(f"p{i}", n) for i, n in enumerate(stored)]
        h = _handlers({"p0": [_todo("a", "x")]})
        block = await _block(_intent(args={"project": "Mobile Redesign"}), h)
        assert block == "" and h._calls == []

    async def test_a_failed_project_read(self, monkeypatch):
        monkeypatch.setattr(attach, "_active_projects", AsyncMock(side_effect=OSError("down")))
        h = _handlers({})
        assert await _block(_intent(args={"project": "Mobile Redesign"}), h) == ""
        assert h._calls == []

    async def test_another_op_or_no_principal(self, projects):
        projects[USER] = [_project("p1", "Mobile Redesign")]
        h = _handlers({"p1": [_todo("a", "x")]})
        other = _intent(args={"project": "Mobile Redesign"}, action="analyze_blockers")
        assert await _block(other, h) == ""
        assert await _block(_intent(args={"project": "Mobile Redesign"}), h, user=None) == ""
        assert h._calls == []

    def test_no_line_of_this_unit_asks_a_question(self):
        for line in (
            pst.OPEN_TODOS_HEADER,
            pst.NO_OPEN_TODOS_LINE,
            pst.TODOS_READ_FAILED_LINE,
            pst.CAP_LINE,
        ):
            assert "?" not in line


class TestTheBlockCannotFailTheStatusReply:
    """Arch 11-20 (01M7Y4QVSY): an error outside the two expected ones must not
    escape; the floor's reply has already been given."""

    async def test_an_unexpected_error_in_the_project_read_adds_nothing(self, monkeypatch):
        monkeypatch.setattr(attach, "_active_projects", AsyncMock(side_effect=RuntimeError("x")))
        h = _handlers({})
        assert await _block(_intent(args={"project": "Mobile Redesign"}), h) == ""
        assert h._calls == []

    async def test_an_unexpected_error_in_the_todo_read_says_cxos_line(self, projects):
        projects[USER] = [_project("p1", "Mobile Redesign")]
        h = _handlers(fail=RuntimeError("x"))
        block = await _block(_intent(args={"project": "Mobile Redesign"}), h)
        assert block == "I couldn't check its todos just now."
        h._remember_todo_list_lines.assert_not_called()

    async def test_an_unexpected_error_in_the_render_says_cxos_line(self, projects, monkeypatch):
        projects[USER] = [_project("p1", "Mobile Redesign")]
        h = _handlers({"p1": [_todo("a", "x")]})
        h._remember_todo_list_lines = MagicMock(side_effect=TypeError("renamed field"))
        block = await _block(_intent(args={"project": "Mobile Redesign"}), h)
        assert block == "I couldn't check its todos just now."

    def test_the_status_reply_stands_with_the_right_tail(self):
        """The call site joins the block to the floor's message and has no path
        that drops ``response.message``."""
        source = (REPO / "services" / "intent" / "intent_service.py").read_text()
        start = source.index("_todos_block = await status_todos_block(")
        tail = source[start : source.index("return IntentProcessingResult(", start)]
        assert "_status_message = _milestone_prefix + response.message" in tail
        assert "raise" not in tail


class TestTheMainListIsUnchanged:
    def test_its_header_is_what_it_was(self):
        todos = [_todo("a", "x"), _todo("b", "y")]
        assert format_todo_list_grouped(todos).splitlines()[0] == (
            "You have 2 open todos. Here they are:"
        )


class TestWhereTheBlockGoes:
    SOURCE = (REPO / "services" / "intent" / "intent_service.py").read_text()

    def test_code_adds_it_after_the_floor_replied(self):
        """Condition 3: the floor never receives the list. The block is built
        after ``floor.respond`` returned and joined to its message by code."""
        respond = self.SOURCE.index("response = await floor.respond(floor_ctx)")
        block = self.SOURCE.index("_todos_block = await status_todos_block(")
        joined = self.SOURCE.index('_status_message = f"{_status_message}\\n\\n{_todos_block}"')
        assert respond < block < joined
        assert self.SOURCE.count("status_todos_block(") == 1

    def test_the_milestone_branch_returns_first(self):
        """Condition 5: a resolved #2197 milestone returns before this branch."""
        milestone = self.SOURCE.index(
            "return _resolved_result", self.SOURCE.index("#2250: the milestone resolved")
        )
        block = self.SOURCE.index("_todos_block = await status_todos_block(")
        assert milestone < block

    def test_the_floor_module_knows_nothing_of_it(self):
        floor = (REPO / "services" / "intent_service" / "conversational_floor.py").read_text()
        assembler = (REPO / "services" / "intent_service" / "context_assembler.py").read_text()
        for source in (floor, assembler):
            assert "project_status_todos" not in source and "Open todos in" not in source


class TestNoCatalogChange:
    def test_the_router_request_is_mains_and_the_read_op_is_absent(self):
        """Condition 6 and the pin: nothing from the parked candidate's catalog
        side landed. The hash is main's at `a537dae663`, the one 2297 pins."""
        from services.intent_service.action_registry import ACTION_EXAMPLES, ACTION_REGISTRY
        from services.intent_service.inversion_router import (
            _SYSTEM_PROMPT,
            build_routing_prompt,
            derive_routing_grammar,
        )
        from services.intent_service.router_catalog_order import CATALOG_ORDER_LEDGER
        from services.intent_service.workflow_dispatcher import get_registered_workflows

        workflow_entries.register_default_workflows()
        grammar = derive_routing_grammar()
        assert "list_project_todos" not in grammar.names()
        assert "list_project_todos" not in get_registered_workflows()
        assert "list_project_todos" not in CATALOG_ORDER_LEDGER
        assert not [k for k in ACTION_REGISTRY if k[1] == "list_project_todos"]
        assert not [k for k in ACTION_EXAMPLES if k[1] == "list_project_todos"]
        prompt = build_routing_prompt(
            "add a task to my Launch project: book the venue", grammar, None
        )
        request = _SYSTEM_PROMPT + "\x00" + prompt
        assert hashlib.sha256(request.encode("utf-8")).hexdigest() == (
            "0cbc4772d8cf2831a692c6239801a788034853fec897f9099aedb0c93b7a84ac"
        )

    def test_get_project_status_is_registered_as_it_was(self):
        from services.intent_service.inversion_router import derive_routing_grammar

        workflow_entries.register_default_workflows()
        assert "get_project_status" in derive_routing_grammar().names()
