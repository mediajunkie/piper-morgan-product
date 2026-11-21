"""#2297: a todo created with a router-named project is attached to that project.

Arch 11-06 11:13 (A): the router's ``project`` arg is resolved against the person's
own active projects. One match writes the todo with the project's id; several ask
an armed numbered pick and write nothing until a number is given. Never a fuzzy
attach, never a created project. CXO 11-06 11:14: the confirm words.

Arch 11-20 (mail 01M7XBJ38R): the match is a LOOKUP. Exact, ignoring case; only if
that matches nothing, one trailing word ``project`` is removed and the exact match
runs again; a single match is used and every other case asks. CXO 11-20 (mail
01M7XAV6XH): the four attach lines for no match, more than five projects, no
projects, and a failed read. Arch's split (01M7X8HRFP): handler only, with the
router's catalog and request byte-identical to main, pinned below by sha256.

LAYER: the resolver, the handler, the rail adapter and the ask builder through
their own functions, with the todo service and the project read replaced at their
one seam each. Nothing here calls a router or a database.
DENOMINATOR: no arg (unchanged), one, the lookup's four ruled cases, none (ask,
name answer, re-ask), more than five, no projects (ask, yes), a failed read, several
(ask, answer, re-ask, decline paths that this module owns), the confirmed yes/no
with a bound id, the registry rows, the router request pin.
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
        assert "I can't find a project" in result.message
        assert "px" not in str(svc.workflow_offer_service.set_pending_offer.call_args)


LAUNCH_MSG = "add a task to my Launch project: book the venue"
LAUNCH_ARGS = {"text": "book the venue", "project": "Launch project"}


class TestLookup:
    """Arch 11-20 (01M7XBJ38R): his four tests, then the edges of the rule."""

    async def test_launch_project_with_a_stored_launch_attaches_to_launch(self, projects):
        # PPM's acceptance row.
        projects[USER] = [_project("p1", "Launch"), _project("p2", "Other")]
        svc = _service()
        result = await _run(_intent(LAUNCH_MSG, LAUNCH_ARGS), svc)
        assert svc.todo_handlers._calls[0]["project_id"] == "p1"
        # CXO 11-20 (01M7XC6TNR): the confirm names the STORED project.
        assert result.message == "I've added 'book the venue' to Launch."

    async def test_with_both_stored_the_exact_match_wins(self, projects):
        projects[USER] = [_project("p1", "Launch"), _project("p2", "Launch project")]
        svc = _service()
        result = await _run(_intent(LAUNCH_MSG, LAUNCH_ARGS), svc)
        assert [c["project_id"] for c in svc.todo_handlers._calls] == ["p2"]
        assert result.message == "I've added 'book the venue' to Launch project."

    async def test_launch_and_launch_in_another_case_both_stored_asks(self, projects):
        projects[USER] = [_project("p1", "Launch"), _project("p2", "launch")]
        svc = _service()
        result = await _run(_intent(LAUNCH_MSG, LAUNCH_ARGS), svc)
        assert svc.todo_handlers._calls == []
        assert result.requires_clarification is True
        assert result.message.endswith(
            "Which one should I add 'book the venue' to? Say the number."
        )
        payload = svc.workflow_offer_service.set_pending_offer.call_args.args[1]["pending_action"]
        assert payload["pick_ids"] == ["p1", "p2"] and payload["answer"] == attach.ANSWER_NUMBER

    @pytest.mark.parametrize(
        "typed",
        [
            "Launch projects",  # a plural is another word
            "Launch plan",  # no other trailing word is removed
            "Launch project plan",  # `project` is not the last word
            "the Launch project",  # nothing is removed from the front
            "Launch project project",  # ONE trailing word: "Launch project" is not stored
            "Launchproject",  # a whole word only
        ],
    )
    async def test_no_other_suffix_is_stripped(self, projects, typed):
        projects[USER] = [_project("p1", "Launch")]
        msg = f"add a task to {typed}: book the venue"
        svc = _service()
        result = await _run(_intent(msg, {"text": "book the venue", "project": typed}), svc)
        assert svc.todo_handlers._calls == []
        assert result.message.startswith(f'I can\'t find a project called "{typed}"')

    def test_the_one_word_removed(self):
        assert attach.without_trailing_project("Launch project") == "Launch"
        assert attach.without_trailing_project("Launch  PROJECT") == "Launch"
        assert attach.without_trailing_project("Launch project project") == "Launch project"
        assert attach.without_trailing_project("project") is None
        assert attach.without_trailing_project("Launch") is None

    def test_a_project_named_project_is_an_exact_match(self):
        refs = attach.lookup([_project("p1", "Project")], "project")
        assert [r.id for r in refs] == ["p1"]

    def test_the_second_step_runs_only_when_the_first_matched_nothing(self):
        stored = [_project("p1", "Launch"), _project("p2", "Launch Project")]
        assert [r.id for r in attach.lookup(stored, "launch project")] == ["p2"]
        assert [r.id for r in attach.lookup(stored, "Launch")] == ["p1"]


class TestAListNameIsNotAProject:
    """PPM's row (11-20): 'add renew passport to my personal list' attaches to no
    project. Main's router sends no ``project`` for that phrase (arm B screen, row
    D2: `(none)` 6 of 6 on main), and this unit leaves the router's request
    unchanged. If a ``project`` ever did arrive for a list name, it is looked up
    like any other name and never guessed into a project."""

    LIST_MSG = "add renew passport to my personal list"

    async def test_with_no_project_arg_it_is_a_plain_todo(self, monkeypatch):
        monkeypatch.setattr(attach, "_active_projects", AsyncMock(side_effect=AssertionError))
        svc = _service()
        await _run(_intent(self.LIST_MSG, {"text": "renew passport"}), svc)
        assert [c["text"] for c in svc.todo_handlers._calls] == ["renew passport"]
        assert "project_id" not in svc.todo_handlers._calls[0]

    async def test_a_list_name_sent_as_a_project_attaches_to_nothing(self, projects):
        projects[USER] = [_project("p1", "Personal finance"), _project("p2", "Launch")]
        svc = _service()
        result = await _run(
            _intent(self.LIST_MSG, {"text": "renew passport", "project": "personal"}), svc
        )
        assert svc.todo_handlers._calls == []
        assert result.message.startswith('I can\'t find a project called "personal"')


NOT_FOUND = (
    "I can't find a project called \"Mobile Redesign\", so I haven't added the todo yet. "
    "Your projects: Mobile Redesign v2, Launch. Which one did you mean?"
)


class TestNoMatch:
    """CXO 11-20 (01M7XAV6XH): the question names what exists and says nothing
    was written. It is armed, with every project and the titles bound."""

    async def test_writes_nothing_and_asks_cxos_question(self, projects):
        projects[USER] = [_project("p1", "Mobile Redesign v2"), _project("p2", "Launch")]
        svc = _service()
        result = await _run(_intent(args={"text": TITLE, "project": "Mobile Redesign"}), svc)
        assert svc.todo_handlers._calls == []
        assert result.message == NOT_FOUND
        assert result.requires_clarification is True
        assert result.intent_data["project_not_found"] is True
        assert result.intent_data[attach.PICK_PENDING_FLAG] is True
        session, record = svc.workflow_offer_service.set_pending_offer.call_args.args
        payload = record["pending_action"]
        assert session == "s1" and record["question"] == NOT_FOUND
        assert payload["kind"] == attach.TODO_PROJECT_PICK_KIND
        assert payload["answer"] == attach.ANSWER_NAME
        assert payload["pick_ids"] == ["p1", "p2"]
        assert payload["titles"] == [TITLE] and payload["user_id"] == USER

    async def test_more_than_five_lists_five_and_binds_all(self, projects):
        names = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta"]
        projects[USER] = [_project(f"p{i}", n) for i, n in enumerate(names)]
        svc = _service()
        result = await _run(_intent(args={"text": TITLE, "project": "Mobile Redesign"}), svc)
        assert result.message == (
            "I can't find a project called \"Mobile Redesign\", so I haven't added the todo yet. "
            "Your projects: Alpha, Beta, Gamma, Delta, Epsilon …and 2 more. "
            "Tell me the name and I'll check."
        )
        payload = svc.workflow_offer_service.set_pending_offer.call_args.args[1]["pending_action"]
        assert payload["pick_names"] == names  # a name past the fifth still answers

    async def test_exactly_five_are_all_listed_with_the_question(self, projects):
        projects[USER] = [_project(f"p{i}", n) for i, n in enumerate("ABCDE")]
        svc = _service()
        result = await _run(_intent(args={"text": TITLE, "project": "Mobile Redesign"}), svc)
        assert result.message.endswith("Your projects: A, B, C, D, E. Which one did you mean?")

    async def test_no_store_asks_no_question_and_writes_nothing(self, projects):
        projects[USER] = [_project("p1", "Launch")]
        svc = _service(store=False)
        result = await _run(_intent(args={"text": TITLE, "project": "Mobile Redesign"}), svc)
        assert svc.todo_handlers._calls == []
        assert result.message == (
            "I can't find a project called \"Mobile Redesign\", so I haven't added the todo yet."
        )
        assert "?" not in result.message and result.requires_clarification is not True

    def _pending(self, names=("Mobile Redesign v2", "Launch"), user=USER):
        refs = [attach.ProjectRef(id=f"p{i + 1}", name=n) for i, n in enumerate(names)]
        return attach.build_not_found_offer(user, "Mobile Redesign", refs, [TITLE], "medium", MSG)

    @pytest.mark.parametrize(
        "answer", ["Launch", "launch", "Launch.", '"Launch"', "Launch project"]
    )
    async def test_a_listed_name_writes_the_bound_title_into_it(self, projects, answer):
        projects[USER] = [_project("p1", "Mobile Redesign v2"), _project("p2", "Launch")]
        svc = _service()
        turn = await attach.handle_todo_project_pick_turn(self._pending(), answer, "s1", USER, svc)
        assert [c["project_id"] for c in svc.todo_handlers._calls] == ["p2"]
        assert svc.todo_handlers._calls[0]["text"] == TITLE
        assert turn["message"] == "I've added 'interview five current users' to Launch."

    @pytest.mark.parametrize(
        "answer", ["the Launch one", "Launc", "Mobile Redesign", "2", "show my projects", "no"]
    )
    async def test_anything_else_is_not_an_answer_and_writes_nothing(self, projects, answer):
        projects[USER] = [_project("p1", "Mobile Redesign v2"), _project("p2", "Launch")]
        svc = _service()
        turn = await attach.handle_todo_project_pick_turn(self._pending(), answer, "s1", USER, svc)
        assert turn is None and svc.todo_handlers._calls == []

    async def test_a_name_two_bound_projects_share_asks_the_numbered_pick(self, projects):
        projects[USER] = [_project("p1", "Launch"), _project("p2", "launch")]
        svc = _service()
        pending = self._pending(names=("Launch", "launch"))
        turn = await attach.handle_todo_project_pick_turn(pending, "Launch", "s1", USER, svc)
        assert svc.todo_handlers._calls == []
        assert turn["requires_clarification"] is True
        assert turn["message"] == (
            "I found more than one project with that name: 1. Launch 2. launch. "
            "Which one should I add 'interview five current users' to? Say the number."
        )
        record = svc.workflow_offer_service.set_pending_offer.call_args.args[1]
        assert record["pending_action"]["answer"] == attach.ANSWER_NUMBER
        assert record["pending_action"]["pick_ids"] == ["p1", "p2"]

    async def test_a_project_gone_since_the_ask_writes_nothing(self, projects):
        projects[USER] = [_project("p1", "Mobile Redesign v2")]
        svc = _service()
        turn = await attach.handle_todo_project_pick_turn(
            self._pending(), "Launch", "s1", USER, svc
        )
        assert svc.todo_handlers._calls == [] and turn["message"] == attach.PROJECT_GONE_LINE

    async def test_another_principal_cannot_answer(self, projects):
        projects[USER] = [_project("p2", "Launch")]
        svc = _service()
        turn = await attach.handle_todo_project_pick_turn(
            self._pending(), "Launch", "s1", OTHER, svc
        )
        assert svc.todo_handlers._calls == []
        assert turn["message"] == attach.PRINCIPAL_MISMATCH_LINE

    async def test_a_bare_yes_reasks_the_same_question(self):
        svc = _service()
        pending = self._pending()
        out = await attach.run_clarify_todo_project_pick_workflow(
            "s1", USER, {"pending_action": pending["pending_action"], "intent_service": svc}
        )
        assert out["message"] == pending["question"] == NOT_FOUND
        record = svc.workflow_offer_service.set_pending_offer.call_args.args[1]
        assert record["question"] == NOT_FOUND
        assert record["pending_action"]["answer"] == attach.ANSWER_NAME


NO_PROJECTS = (
    "I can't find a project called \"Mobile Redesign\", and I don't see any projects on your "
    "account, so I haven't added the todo yet. Want it added without a project?"
)


class TestNoProjects:
    """CXO 11-20: the list read succeeded and was empty."""

    async def test_writes_nothing_and_asks_cxos_question(self, projects):
        svc = _service()
        result = await _run(_intent(args={"text": TITLE, "project": "Mobile Redesign"}), svc)
        assert svc.todo_handlers._calls == []
        assert result.message == NO_PROJECTS
        assert result.requires_clarification is True
        assert result.intent_data["action"] == attach.TODO_NO_PROJECT_WORKFLOW
        record = svc.workflow_offer_service.set_pending_offer.call_args.args[1]
        assert record["workflow_type"] == attach.TODO_NO_PROJECT_WORKFLOW
        assert record["question"] == NO_PROJECTS
        assert record["decline_message"] == attach.PICK_DECLINE_LINE
        payload = record["pending_action"]
        assert payload["kind"] == attach.TODO_NO_PROJECT_KIND
        assert payload["titles"] == [TITLE] and payload["user_id"] == USER

    async def test_no_store_asks_no_question(self, projects):
        svc = _service(store=False)
        result = await _run(_intent(args={"text": TITLE, "project": "Mobile Redesign"}), svc)
        assert svc.todo_handlers._calls == []
        assert result.message == NO_PROJECTS.replace(" Want it added without a project?", "")

    def _payload(self, titles=(TITLE,), user=USER):
        record = attach.build_no_projects_offer(user, "Mobile Redesign", list(titles), "high", MSG)
        return record["pending_action"]

    async def test_yes_writes_the_bound_title_with_no_project(self):
        svc = _service()
        out = await attach.run_create_todo_without_project_workflow(
            "s1", USER, {"pending_action": self._payload(), "intent_service": svc}
        )
        call = svc.todo_handlers._calls[0]
        assert call["text"] == TITLE and call["priority"] == "high"
        assert "project_id" not in call
        assert TITLE in out["message"] and "Mobile Redesign" not in out["message"]
        assert out["requires_clarification"] is False

    async def test_yes_writes_every_bound_title(self):
        svc = _service()
        out = await attach.run_create_todo_without_project_workflow(
            "s1", USER, {"pending_action": self._payload(("a b", "c d")), "intent_service": svc}
        )
        assert [c["text"] for c in svc.todo_handlers._calls] == ["a b", "c d"]
        assert all("project_id" not in c for c in svc.todo_handlers._calls)
        assert "'a b' and 'c d'" in out["message"]

    async def test_another_principals_yes_writes_nothing(self):
        svc = _service()
        out = await attach.run_create_todo_without_project_workflow(
            "s1", OTHER, {"pending_action": self._payload(), "intent_service": svc}
        )
        assert svc.todo_handlers._calls == []
        assert out["message"] == attach.PRINCIPAL_MISMATCH_LINE

    async def test_a_foreign_payload_writes_nothing(self):
        svc = _service()
        out = await attach.run_create_todo_without_project_workflow(
            "s1", USER, {"pending_action": {"kind": "something_else"}, "intent_service": svc}
        )
        assert out is None and svc.todo_handlers._calls == []


class TestLookupFailed:
    """CXO 11-20: the read failed, so neither "can't find" nor "no projects" is known."""

    @pytest.mark.parametrize("error", [OSError("down"), None])
    async def test_writes_nothing_and_says_only_what_is_known(self, monkeypatch, error):
        from sqlalchemy.exc import OperationalError

        raised = error or OperationalError("select", {}, Exception("down"))
        monkeypatch.setattr(attach, "_active_projects", AsyncMock(side_effect=raised))
        svc = _service()
        result = await _run(_intent(args={"text": TITLE, "project": "Mobile Redesign"}), svc)
        assert svc.todo_handlers._calls == []
        assert result.message == (
            "I couldn't check your projects just now, so I haven't added the todo. "
            "Try again in a moment."
        )
        assert "can't find" not in result.message and "no projects" not in result.message.lower()
        svc.workflow_offer_service.set_pending_offer.assert_not_called()

    async def test_the_write_ask_leaves_a_failed_read_to_the_op(self, monkeypatch):
        monkeypatch.setattr(attach, "_active_projects", AsyncMock(side_effect=OSError("down")))
        intent = _intent(args={"text": TITLE, "project": "Mobile Redesign"})
        ask = await create_todo_write_ask(
            WriteAskRequest(intent=intent, message=MSG, intent_service=_service(), principal=USER)
        )
        assert ask.passthrough is True and "write_ask_bound" not in intent.context


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

    def test_the_without_a_project_yes_is_offer_only_and_writes(self):
        from services.intent_service.workflow_dispatcher import (
            EffectClass,
            get_action_workflows,
            get_registered_workflows,
        )

        workflow_entries.register_default_workflows()
        landing = get_registered_workflows()[attach.TODO_NO_PROJECT_WORKFLOW]
        assert landing.effect == EffectClass.WRITE
        assert landing.action_triggered is False
        assert attach.TODO_NO_PROJECT_WORKFLOW not in get_action_workflows()

    def test_the_router_request_is_mains_by_sha256(self):
        """Arch 11-20 (01M7X8HRFP): not a rule-7 change IF the catalog and the
        router's request are unchanged. The request below is the router's system
        prompt and its whole user prompt (the catalog is inside it) for one
        phrase, hashed at main `a537dae663` before this change. A different hash
        means the router's input moved: that is a rule-7 change and needs its
        screen. This constant moves only in the commit that lands a screened
        change, never to make this test pass."""
        import hashlib

        from services.intent_service.inversion_router import (
            _SYSTEM_PROMPT,
            build_routing_prompt,
            derive_routing_grammar,
        )

        workflow_entries.register_default_workflows()
        grammar = derive_routing_grammar()
        names = {op.name for op in grammar.operations}
        assert attach.TODO_PROJECT_PICK_WORKFLOW not in names
        assert attach.TODO_NO_PROJECT_WORKFLOW not in names
        prompt = build_routing_prompt(LAUNCH_MSG, grammar, None)
        request = _SYSTEM_PROMPT + "\x00" + prompt
        assert hashlib.sha256(request.encode("utf-8")).hexdigest() == (
            "0cbc4772d8cf2831a692c6239801a788034853fec897f9099aedb0c93b7a84ac"
        )

    def test_create_todos_router_description_is_unchanged(self):
        """Rule 7: the handler side lands with ZERO router-prompt delta. A wording
        that names the project arg is a separate, screened change."""
        from services.intent_service.workflow_dispatcher import get_registered_workflows

        workflow_entries.register_default_workflows()
        assert get_registered_workflows()["create_todo"].description == (
            "Create-todo via action dispatch (#1685)"
        )
