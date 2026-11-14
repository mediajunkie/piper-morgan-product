"""#2297: a todo created with a router-named project is attached to that project.

Arch 11-06 11:13 (A): the router's ``project`` arg is resolved against the person's
own active projects by exact name, case-insensitively. One match writes the todo
with the project's id; none writes nothing and says so; several ask an armed
numbered pick and write nothing until a number is given. Never a fuzzy attach,
never a created project. CXO 11-06 11:14: the words.

LAYER: the resolver, the handler, the rail adapter and the ask builder through
their own functions, with the todo service and the project read replaced at their
one seam each. Nothing here calls a router or a database.
DENOMINATOR: no arg (unchanged), one, none, several (ask, answer, re-ask, decline
paths that this module owns), the confirmed yes/no with a bound id, the registry row.
"""

import types
from unittest.mock import AsyncMock, MagicMock

import pytest

from services.domain.models import Intent
from services.intent_service import todo_project_attach as attach
from services.intent_service import workflow_entries
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.intent_service.write_confirm_words import (
    WriteAskRequest,
    bind_write_values,
    create_todo_write_ask,
)
from services.shared_types import IntentCategory

USER = "11111111-1111-1111-1111-111111111111"
OTHER = "22222222-2222-2222-2222-222222222222"
MSG = "add a task to Mobile Redesign: interview five current users"
TITLE = "interview five current users"


def _project(pid, name):
    return types.SimpleNamespace(id=pid, name=name)


def _handlers():
    h = TodoIntentHandlers.__new__(TodoIntentHandlers)
    calls = []

    async def create_todo(**kwargs):
        calls.append(kwargs)
        return types.SimpleNamespace(
            id=f"t-{len(calls)}",
            text=kwargs["text"],
            priority=kwargs.get("priority", "medium"),
            completed=False,
        )

    h.todo_service = MagicMock()
    h.todo_service.create_todo = AsyncMock(side_effect=create_todo)
    h._calls = calls
    return h


def _intent(message=MSG, args=None):
    ctx = {"original_message": message}
    if args is not None:
        ctx["inversion_args"] = args
    return Intent(
        original_message=message,
        category=IntentCategory.EXECUTION,
        action="create_todo",
        confidence=0.95,
        context=ctx,
    )


def _service(handlers=None, store=True):
    svc = types.SimpleNamespace(todo_handlers=handlers or _handlers())
    if store:
        svc.workflow_offer_service = MagicMock()
    return svc


@pytest.fixture
def projects(monkeypatch):
    """The person's active projects, by user id. The one seam for the project read."""
    table = {USER: []}

    async def _active(user_id):
        return list(table.get(str(user_id), []))

    monkeypatch.setattr(attach, "_active_projects", _active)
    return table


async def _run(intent, svc, user=USER, session="s1"):
    return await workflow_entries.run_create_todo_workflow(
        session, user, {"intent": intent, "intent_service": svc}
    )


class TestRouterArg:
    def test_reads_the_project_arg_whitespace_collapsed(self):
        assert attach.router_project_name(_intent(args={"project": " Mobile  Redesign "})) == (
            "Mobile Redesign"
        )

    @pytest.mark.parametrize("args", [None, {}, {"project": ""}, {"project": 7}, {"text": "x"}])
    def test_no_usable_arg_is_none(self, args):
        assert attach.router_project_name(_intent(args=args)) is None

    def test_exact_whole_name_any_case_only(self):
        ps = [_project("p1", "Mobile Redesign"), _project("p2", "Mobile Redesign v2")]
        assert [m.id for m in attach.exact_matches(ps, "mobile redesign")] == ["p1"]
        assert attach.exact_matches(ps, "Mobile") == []
        assert attach.exact_matches(ps, "Redesign") == []


class TestWordGuard:
    """Arch 11-14 ruling 1: the arg is the person's only when every word of it is
    in their message. Otherwise it is no arg, and create_todo is today's."""

    async def test_an_arg_with_a_word_not_said_makes_the_plain_todo(self, monkeypatch):
        monkeypatch.setattr(attach, "_active_projects", AsyncMock(side_effect=AssertionError))
        msg = "add a todo: interview five current users"
        svc = _service()
        result = await _run(_intent(msg, {"text": TITLE, "project": "Mobile Redesign"}), svc)
        assert "project_id" not in svc.todo_handlers._calls[0]
        assert svc.todo_handlers._calls[0]["text"] == TITLE
        assert result.message.startswith("I've added that to your list.")
        assert "Mobile Redesign" not in result.message

    def test_one_missing_word_is_enough(self):
        intent = _intent("add to Mobile: x", {"project": "Mobile Redesign"})
        assert attach.router_project_name(intent) is None

    def test_all_words_said_in_any_case_and_punctuation_passes(self):
        intent = _intent("add 'x' to the MOBILE redesign, please", {"project": "Mobile Redesign"})
        assert attach.router_project_name(intent) == "Mobile Redesign"

    async def test_the_ask_for_a_guarded_out_arg_is_the_plain_question(self, monkeypatch):
        monkeypatch.setattr(attach, "_active_projects", AsyncMock(side_effect=AssertionError))
        intent = _intent("also add: buy oat milk", {"text": "buy oat milk", "project": "Home"})
        ask = await create_todo_write_ask(
            WriteAskRequest(
                intent=intent,
                message=intent.original_message,
                intent_service=_service(),
                principal=USER,
            )
        )
        assert ask.words.question == 'Add "buy oat milk" to your todos? (yes/no)'


class TestPickShowsWhatItWrites:
    """Arch 11-14 ruling 2, CXO's words: the number is the consent only because the
    question shows each bound title exactly as stored, on the re-ask too."""

    def _matches(self):
        import datetime as dt

        return attach.exact_matches(
            [
                types.SimpleNamespace(id="p1", name="Launch", created_at=dt.datetime(2026, 11, 3)),
                types.SimpleNamespace(id="p2", name="launch", created_at=dt.datetime(2026, 11, 9)),
            ],
            "Launch",
        )

    @pytest.mark.parametrize(
        "titles,shown",
        [
            (["interview five current users"], "'interview five current users'"),
            (["draft brief", "book venue"], "'draft brief' and 'book venue'"),
            (["a", "b", "c"], "'a', 'b' and 'c'"),
        ],
    )
    async def test_question_and_reask_carry_every_stored_title(self, titles, shown):
        record = attach.build_pick_offer(USER, self._matches(), titles, "medium", "m")
        assert record["question"] == (
            "I found more than one project with that name: 1. Launch (created 3 Nov) "
            f"2. launch (created 9 Nov). Which one should I add {shown} to? Say the number."
        )
        for title in record["pending_action"]["titles"]:
            assert f"'{title}'" in record["question"]
        svc = _service()
        out = await attach.run_clarify_todo_project_pick_workflow(
            "s1", USER, {"pending_action": record["pending_action"], "intent_service": svc}
        )
        assert out["message"] == record["question"]

    def test_a_row_with_no_created_date_shows_the_name_alone(self):
        ref = attach.exact_matches([_project("p1", "Launch")], "launch")[0]
        assert ref.label == "Launch"


class TestPriorityClause:
    """CXO 11-14: a stored non-default priority is said; the default says nothing."""

    async def test_high_priority_is_said(self, projects):
        projects[USER] = [_project("p1", "Mobile Redesign")]
        svc = _service()
        svc.todo_handlers._extract_priority = lambda _m: "high"
        result = await _run(_intent(args={"text": TITLE, "project": "Mobile Redesign"}), svc)
        assert result.message == (
            "I've added 'interview five current users' to Mobile Redesign, at high priority."
        )

    def test_default_priority_says_nothing(self):
        assert attach.render_attached(["x"], "P", priority="medium") == "I've added 'x' to P."


class TestNoArgIsUnchanged:
    async def test_plain_create_passes_no_project_and_reads_no_projects(self, monkeypatch):
        monkeypatch.setattr(attach, "_active_projects", AsyncMock(side_effect=AssertionError))
        svc = _service()
        result = await _run(_intent("add todo: buy oat milk", {"text": "buy oat milk"}), svc)
        assert svc.todo_handlers._calls == [
            {
                "user_id": svc.todo_handlers._calls[0]["user_id"],
                "text": "buy oat milk",
                "priority": "medium",
            }
        ]
        assert "project_id" not in svc.todo_handlers._calls[0]
        assert result.message.startswith("I've added that to your list.")


class TestOneMatch:
    async def test_writes_with_the_project_id_and_says_so(self, projects):
        projects[USER] = [_project("p1", "Mobile Redesign"), _project("p2", "Other")]
        svc = _service()
        result = await _run(_intent(args={"text": TITLE, "project": "mobile redesign"}), svc)
        assert svc.todo_handlers._calls[0]["project_id"] == "p1"
        assert svc.todo_handlers._calls[0]["text"] == TITLE
        # CXO's line, with the STORED name, not the typed casing.
        assert result.message == "I've added 'interview five current users' to Mobile Redesign."

    async def test_several_titles_all_go_to_the_project(self, projects):
        projects[USER] = [_project("p1", "Launch")]
        msg = "add to Launch: draft brief, book venue"
        svc = _service()
        result = await _run(
            _intent(msg, {"items": ["draft brief", "book venue"], "project": "Launch"}), svc
        )
        assert [c["project_id"] for c in svc.todo_handlers._calls] == ["p1", "p1"]
        assert result.message == "I've added 2 todos to Launch: 'draft brief' and 'book venue'."

    async def test_another_persons_project_of_that_name_is_not_a_match(self, projects):
        projects[OTHER] = [_project("px", "Mobile Redesign")]
        svc = _service()
        result = await _run(_intent(args={"text": TITLE, "project": "Mobile Redesign"}), svc)
        assert svc.todo_handlers._calls == []
        assert "couldn't find a project" in result.message


class TestNoMatch:
    async def test_writes_nothing_and_says_cxos_line(self, projects):
        projects[USER] = [_project("p1", "Mobile Redesign v2")]
        svc = _service()
        result = await _run(_intent(args={"text": TITLE, "project": "Mobile Redesign"}), svc)
        assert svc.todo_handlers._calls == []
        assert result.message == (
            "I couldn't find a project called \"Mobile Redesign\", so I haven't added anything. "
            'Check the name, or say "show my projects".'
        )
        svc.workflow_offer_service.set_pending_offer.assert_not_called()


class TestProjectReadFails:
    async def test_a_failed_project_read_writes_nothing_and_says_so(self, monkeypatch):
        """The lookup runs BEFORE the write, so the outcome is known: nothing added.
        Never a plain todo the person didn't ask for."""
        monkeypatch.setattr(attach, "_active_projects", AsyncMock(side_effect=OSError("down")))
        svc = _service()
        result = await _run(_intent(args={"text": TITLE, "project": "Mobile Redesign"}), svc)
        assert svc.todo_handlers._calls == []
        assert result.message == attach.RESOLVE_FAILED_LINE
        assert "haven't added anything" in result.message


class TestSeveralMatches:
    async def test_asks_an_armed_pick_and_writes_nothing(self, projects):
        projects[USER] = [_project("p1", "Mobile Redesign"), _project("p2", "mobile redesign")]
        svc = _service()
        result = await _run(_intent(args={"text": TITLE, "project": "Mobile Redesign"}), svc)
        assert svc.todo_handlers._calls == []
        assert result.message == (
            "I found more than one project with that name: 1. Mobile Redesign "
            "2. mobile redesign. Which one should I add 'interview five current users' to? "
            "Say the number."
        )
        assert result.requires_clarification is True
        assert result.intent_data[attach.PICK_PENDING_FLAG] is True
        session, record = svc.workflow_offer_service.set_pending_offer.call_args.args
        payload = record["pending_action"]
        assert session == "s1"
        assert record["question"] == result.message
        assert payload["kind"] == attach.TODO_PROJECT_PICK_KIND
        assert payload["pick_ids"] == ["p1", "p2"]
        assert payload["titles"] == [TITLE]
        assert payload["user_id"] == USER

    async def test_no_store_asks_no_question_and_writes_nothing(self, projects):
        projects[USER] = [_project("p1", "A"), _project("p2", "a")]
        svc = _service(store=False)
        result = await _run(_intent("add to A: x y", {"text": "x y", "project": "A"}), svc)
        assert svc.todo_handlers._calls == []
        assert result.message == (
            "I found more than one project with that name, so I haven't added anything."
        )

    def _pending(self, titles=(TITLE,), user=USER):
        return attach.build_pick_offer(
            user,
            [
                attach.ProjectRef("p1", "Mobile Redesign"),
                attach.ProjectRef("p2", "mobile redesign"),
            ],
            list(titles),
            "medium",
            MSG,
        )

    async def test_a_number_writes_the_bound_title_into_the_bound_project(self, projects):
        projects[USER] = [_project("p1", "Mobile Redesign"), _project("p2", "mobile redesign")]
        svc = _service()
        turn = await attach.handle_todo_project_pick_turn(self._pending(), "2", "s1", USER, svc)
        assert svc.todo_handlers._calls[0]["project_id"] == "p2"
        assert svc.todo_handlers._calls[0]["text"] == TITLE
        assert turn["message"] == "I've added 'interview five current users' to mobile redesign."

    async def test_another_principal_writes_nothing(self, projects):
        projects[OTHER] = [_project("p1", "Mobile Redesign")]
        svc = _service()
        turn = await attach.handle_todo_project_pick_turn(self._pending(), "1", "s1", OTHER, svc)
        assert svc.todo_handlers._calls == []
        assert turn["message"] == attach.PRINCIPAL_MISMATCH_LINE

    async def test_a_project_gone_since_the_ask_writes_nothing(self, projects):
        projects[USER] = [_project("p1", "Mobile Redesign")]  # p2 archived since
        svc = _service()
        turn = await attach.handle_todo_project_pick_turn(self._pending(), "2", "s1", USER, svc)
        assert svc.todo_handlers._calls == []
        assert turn["message"] == attach.PROJECT_GONE_LINE

    @pytest.mark.parametrize(
        "message", ["", "7", "show my projects please now", "what's the weather"]
    )
    async def test_anything_but_a_listed_number_falls_through(self, projects, message):
        projects[USER] = [_project("p1", "Mobile Redesign"), _project("p2", "mobile redesign")]
        svc = _service()
        turn = await attach.handle_todo_project_pick_turn(self._pending(), message, "s1", USER, svc)
        assert turn is None
        assert svc.todo_handlers._calls == []

    async def test_a_foreign_record_is_not_ours(self):
        record = {"pending_action": {"kind": "project_archive_pick_question"}}
        assert (
            await attach.handle_todo_project_pick_turn(record, "1", "s1", USER, _service()) is None
        )

    async def test_bare_yes_reasks_and_rearms_the_same_bound_list(self):
        svc = _service()
        payload = self._pending()["pending_action"]
        out = await attach.run_clarify_todo_project_pick_workflow(
            "s1", USER, {"pending_action": payload, "intent_service": svc}
        )
        assert out["message"].startswith("I found more than one project with that name: 1. Mobile")
        record = svc.workflow_offer_service.set_pending_offer.call_args.args[1]
        assert record["pending_action"]["pick_ids"] == ["p1", "p2"]
        assert record["pending_action"]["titles"] == [TITLE]
        assert svc.todo_handlers._calls == []


class TestWriteAsk:
    def _request(self, intent, svc=None):
        return WriteAskRequest(
            intent=intent, message=MSG, intent_service=svc or _service(), principal=USER
        )

    async def test_one_match_names_the_project_and_binds_its_id(self, projects):
        projects[USER] = [_project("p1", "Mobile Redesign")]
        intent = _intent(args={"text": TITLE, "project": "mobile redesign"})
        ask = await create_todo_write_ask(self._request(intent))
        assert ask.words.question == (
            'Add "interview five current users" to Mobile Redesign? (yes/no)'
        )
        bound = intent.context["write_ask_bound"]
        assert bound == {
            "op": "create_todo",
            "text": TITLE,
            "project_id": "p1",
            "project_name": "Mobile Redesign",
        }

    @pytest.mark.parametrize("names", [[], ["Mobile Redesign", "mobile redesign"]])
    async def test_none_or_several_is_left_to_the_op(self, projects, names):
        projects[USER] = [_project(f"p{i}", n) for i, n in enumerate(names)]
        intent = _intent(args={"text": TITLE, "project": "Mobile Redesign"})
        ask = await create_todo_write_ask(self._request(intent))
        assert ask.passthrough is True and ask.words is None and ask.reply is None
        assert "write_ask_bound" not in intent.context

    async def test_no_project_arg_keeps_the_plain_question(self, monkeypatch):
        monkeypatch.setattr(attach, "_active_projects", AsyncMock(side_effect=AssertionError))
        intent = _intent("also add: buy oat milk", {"text": "buy oat milk"})
        ask = await create_todo_write_ask(self._request(intent))
        assert ask.words.question == 'Add "buy oat milk" to your todos? (yes/no)'


class TestConfirmedYes:
    async def test_writes_the_bound_title_into_the_bound_id_without_resolving_a_name(
        self, projects
    ):
        # The name now matches TWO projects; the id bound at ask time still decides.
        projects[USER] = [_project("p1", "Mobile Redesign"), _project("p2", "mobile redesign")]
        intent = _intent(args={"text": "something else", "project": "Mobile Redesign"})
        bind_write_values(
            intent, "create_todo", text=TITLE, project_id="p2", project_name="mobile redesign"
        )
        svc = _service()
        result = await _run(intent, svc)
        assert svc.todo_handlers._calls[0]["project_id"] == "p2"
        assert svc.todo_handlers._calls[0]["text"] == TITLE
        assert result.message == "I've added 'interview five current users' to mobile redesign."
        svc.workflow_offer_service.set_pending_offer.assert_not_called()

    async def test_a_bound_project_gone_since_the_ask_writes_nothing(self, projects):
        intent = _intent(args={"text": TITLE, "project": "Mobile Redesign"})
        bind_write_values(intent, "create_todo", text=TITLE, project_id="p9", project_name="X")
        svc = _service()
        result = await _run(intent, svc)
        assert svc.todo_handlers._calls == []
        assert result.message == attach.PROJECT_GONE_LINE


class TestRegistry:
    def test_the_reask_landing_is_offer_only_and_reads(self):
        from services.intent_service.workflow_dispatcher import (
            EffectClass,
            get_action_workflows,
            get_registered_workflows,
        )

        workflow_entries.register_default_workflows()
        landing = get_registered_workflows()[attach.TODO_PROJECT_PICK_WORKFLOW]
        assert landing.effect == EffectClass.READ
        assert landing.action_triggered is False
        assert attach.TODO_PROJECT_PICK_WORKFLOW not in get_action_workflows()

    def test_create_todos_router_description_is_unchanged(self):
        """Rule 7: the handler side lands with ZERO router-prompt delta. A wording
        that names the project arg is a separate, screened change."""
        from services.intent_service.workflow_dispatcher import get_registered_workflows

        workflow_entries.register_default_workflows()
        assert get_registered_workflows()["create_todo"].description == (
            "Create-todo via action dispatch (#1685)"
        )
