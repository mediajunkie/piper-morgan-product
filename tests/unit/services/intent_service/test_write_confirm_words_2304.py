"""#2304 (CXO 11-06 11:28; Arch 11-06 11:38): every write's yes/no names the thing it
would change, from that op's own args, and never shows an op name.

- Per op: the filled question (CXO's table), and the "not sure" statement with
  nothing armed when the args can't name the thing.
- add_project with no name: CXO's name question, armed on the #2080 name carrier
  (consent_owed), never a yes that runs an add with no name.
- The sweep: every consent-needing rail key with empty args says the statement
  (complete: its own no-target statement), never its op words.
- The #2219 seam's entry-identity ``elif`` is gone; complete still asks
  'Mark "x" as done? (yes/no)' through its entry's ``write_ask``.
- Driven through the REAL ``process_intent`` with only the LLM boundary pinned
  (the #2219 harness).
"""

import inspect
from types import SimpleNamespace

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service.add_project_clarify import ADD_PROJECT_NAME_QUESTION_KIND
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.intent_service.workflow_dispatcher import get_action_workflows
from services.intent_service.workflow_entries import register_default_workflows
from services.intent_service.write_confirm_words import (
    ADD_PROJECT_NAME_QUESTION,
    NOT_SURE_STATEMENT,
    WriteAskRequest,
    resolve_write_ask,
)
from services.shared_types import IntentCategory
from tests.unit.services.intent_service.test_floor_category_write_2219 import (  # noqa: F401
    _USER,
    _service,
    _wrote,
    boundary,
)


class _Offers:
    def __init__(self):
        self.armed = []

    def set_pending_offer(self, session_id, offer, user_id=None):
        self.armed.append((session_id, offer, user_id))


def _intent(action, message="", **context):
    return Intent(
        category=IntentCategory.EXECUTION,
        action=action,
        confidence=0.9,
        original_message=message,
        context={"original_message": message, **context},
    )


def _service_stub(offers=None):
    handlers = TodoIntentHandlers.__new__(TodoIntentHandlers)  # extractors only; no DB
    return SimpleNamespace(todo_handlers=handlers, workflow_offer_service=offers or _Offers())


async def _ask(action, message="", *, session_id=None, service=None, **context):
    register_default_workflows()
    return await resolve_write_ask(
        get_action_workflows()[action],
        WriteAskRequest(
            intent=_intent(action, message, **context),
            message=message,
            intent_service=service if service is not None else _service_stub(),
            session_id=session_id,
            user_id=_USER if session_id else None,
        ),
    )


# ── the filled questions, one per op that its args can name ──


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "action,message,context,question,summary",
    [
        (
            "create_todo",
            "add todo: buy milk",
            {},
            'Add "buy milk" to your todos? (yes/no)',
            'add "buy milk" to your todos',
        ),
        (
            "create_todo",
            "add a todo to water the plants",
            {"inversion_args": {"text": "water the plants"}},
            'Add "water the plants" to your todos? (yes/no)',
            'add "water the plants" to your todos',
        ),
        (
            "create_reminder",
            "remind me to call mom tomorrow at 3pm",
            {},
            'Set a reminder "call mom" for tomorrow at 3pm? (yes/no)',
            'set a reminder "call mom" for tomorrow at 3pm',
        ),
        (
            "archive_project",
            "I would like to archive project Bar",
            {},
            'Archive the project "Bar"? (yes/no)',
            'archive the project "Bar"',
        ),
        (
            "restore_project",
            "restore project Bar",
            {},
            'Restore the project "Bar"? (yes/no)',
            'restore the project "Bar"',
        ),
        (
            "add_project",
            "add a project called Klatch",
            {},
            'Add a project called "Klatch"? (yes/no)',
            'add a project called "Klatch"',
        ),
        (
            "create_issue",
            'create an issue titled "Login bug" in acme/web',
            {},
            'Create an issue titled "Login bug" in acme/web? (yes/no)',
            'create an issue titled "Login bug" in acme/web',
        ),
        (
            "create_issue",
            "file it",
            {"title": "Login bug", "repository": "acme/web"},
            'Create an issue titled "Login bug" in acme/web? (yes/no)',
            'create an issue titled "Login bug" in acme/web',
        ),
        (
            "update_issue",
            "the title of issue #108 ought to say Q3 roadmap",
            {"repository": "acme/roadmap", "title": "Q3 roadmap"},
            "Change the title of issue #108 in acme/roadmap? (yes/no)",
            "change the title of issue #108 in acme/roadmap",
        ),
        (
            "update_issue",
            "relabel it",
            {"issue_number": 7, "repo": "acme/web", "labels": ["bug"], "state": "closed"},
            "Change the state and the labels of issue #7 in acme/web? (yes/no)",
            "change the state and the labels of issue #7 in acme/web",
        ),
    ],
)
async def test_each_op_asks_its_own_question_with_the_thing_named(
    action, message, context, question, summary
):
    ask = await _ask(action, message, **context)
    assert ask.reply is None
    assert ask.words.question == question
    assert ask.words.summary == summary


# ── the rows the args can't fill: CXO's statement, nothing armed ──


# CXO 11-06 (2304 rulings): the ops that can never name the thing say how to go ahead.
_SAY_IT = "I'm not sure exactly what you want changed, so I haven't done anything. "
_DIRECT_LINES = {
    "update_document": _SAY_IT
    + "Say it as a direct request that names the document and the change.",
    "set_default_repo": _SAY_IT
    + 'Say it as a direct request, like "set my default repo to owner/name".',
    "set_timezone": _SAY_IT
    + 'Say it as a direct request, like "set my timezone to America/Los_Angeles".',
    # link_repo: CXO dropped its example (served-judged 7ffd460640); it names the thing
    # when its parse resolves (#2308, test_link_repo_held_ask_2308.py), else the plain line.
    # comment_issue: CXO's example dropped (no routed row of that shape); the plain line.
    "comment_issue": NOT_SURE_STATEMENT,
}


@pytest.fixture(autouse=True)
def _no_stored_preferences(monkeypatch):
    """#955's set aliases read the person's stored keys (never the words); none here."""
    import services.intent_service.preference_change as pc

    async def _none(user_id):
        return {}

    monkeypatch.setattr(pc, "_stored_clear_keys", _none)


def _expected_statement(action):
    register_default_workflows()
    entry = get_action_workflows()[action]
    from services.intent_service import preference_change as pc

    if pc.CHANGE_BY_ACTION.get(action) in (pc.CHANGE_DONE, pc.CHANGE_DELETE):
        # #955 (Arch 07:18 (iii)): set-directly never creates a preference; with none
        # stored the ask is CXO's line 4 for that verb (Arch 13:21), nothing armed.
        return pc.NOTHING_TO_CHANGE_TEMPLATE.format(verb=pc.VERB_BY_ACTION.get(action, "clear"))
    for op, line in _DIRECT_LINES.items():
        if entry is get_action_workflows()[op]:
            return line
    return NOT_SURE_STATEMENT


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "action,message,context",
    [
        # handler finds the document with an LLM call: nothing to read before yes
        ("update_document", 'update the document "Q3 Plan" with the new date', {}),
        # handler finds the comment text with an LLM call
        ("comment_issue", 'comment "looks good" on issue #5 in acme/web', {}),
        # #2308: link_repo with neither an owner/name nor a project named
        ("link_repo", "link it up", {}),
        # handlers parse their targets inline (no reusable resolver, no new regex)
        ("set_default_repo", "set my default repo to acme/web", {}),
        ("set_timezone", "set my timezone to Europe/Helsinki", {}),
        # no time said: CXO's row falls to the statement
        ("create_reminder", "remind me to call mom", {}),
        # several titles: no CXO row for a multi-add
        (
            "create_todo",
            "add todos: draft brief, book venue",
            {"inversion_args": {"items": ["draft brief", "book venue"]}},
        ),
        # the args don't say what changes
        ("update_issue", "update issue #108", {"repository": "acme/roadmap"}),
        # a repo the handler would only find by lookup is not named
        ("create_issue", 'create an issue titled "Login bug"', {}),
        ("archive_project", "archive", {}),
    ],
)
async def test_unnameable_rows_say_not_sure_and_arm_nothing(action, message, context):
    offers = _Offers()
    ask = await _ask(action, message, session_id="s-2304", service=_service_stub(offers), **context)
    assert ask.words is None
    assert ask.reply == _expected_statement(action)
    assert ask.armed is False
    assert offers.armed == []


@pytest.mark.asyncio
async def test_add_project_with_no_name_asks_cxos_name_question_on_the_name_carrier():
    offers = _Offers()
    ask = await _ask(
        "add_project",
        "I'd like to start a new project",
        session_id="s-2304-add",
        service=_service_stub(offers),
    )
    assert ask.words is None  # no "Add a project called …?" yes/no exists to say yes to
    assert ask.reply == ADD_PROJECT_NAME_QUESTION
    assert ask.reply == (
        'What should I call the project? Say its name, for example "add project Mobile Redesign".'
    )
    assert ask.armed is True
    [(sid, offer, user)] = offers.armed
    assert sid == "s-2304-add" and user == _USER
    assert offer["pending_action"]["kind"] == ADD_PROJECT_NAME_QUESTION_KIND
    assert offer["pending_action"]["consent_owed"] is True
    assert offer["question"] == ADD_PROJECT_NAME_QUESTION
    assert offer["workflow_type"] != "confirm_pending_action"


@pytest.mark.asyncio
async def test_add_project_with_no_name_and_no_session_arms_nothing():
    ask = await _ask("add_project", "I'd like to start a new project")
    assert ask.reply == NOT_SURE_STATEMENT
    assert ask.armed is False


# ── the sweep: no consent-needing rail key ever shows its op words ──


def _consent_keys():
    register_default_workflows()
    return sorted(k for k, e in get_action_workflows().items() if e.needs_consent)


def test_the_sweep_covers_every_consent_needing_rail_key():
    keys = _consent_keys()
    assert len(keys) >= 40, keys  # 13 WRITE + 4 DESTRUCTIVE entries with their aliases
    for op in ("create_todo", "update_document_query", "comment_issue", "complete_todo"):
        assert op in keys


class _NoTodos:
    async def list_todos(self, user_id, include_completed=False):
        from services.domain.models import Todo

        return [Todo(id="t1", text="water plants", priority="medium", status="pending")]


@pytest.mark.asyncio
@pytest.mark.parametrize("action", _consent_keys())
async def test_empty_args_never_show_the_op_name(action):
    service = _service_stub()
    service.todo_handlers.todo_service = _NoTodos()
    ask = await resolve_write_ask(
        get_action_workflows()[action],
        WriteAskRequest(
            intent=_intent(action), message="", intent_service=service, principal=_USER
        ),
    )
    said = " ".join(x for x in (ask.reply, ask.words and ask.words.question) if x)
    # #2321: CXO's by-name floor quotes a phrasing for the person to type ("complete
    # todo call mom"); that example is not the op name leaking, so it is set aside.
    said = said.replace('Ask me by name, like "complete todo call mom".', "")
    assert action not in said
    assert action.replace("_", " ") not in said.lower()
    assert ask.words is None
    if get_action_workflows()[action] is get_action_workflows()["complete_todo"]:
        # #2321 (CXO 11-07 14:30): the no-list reply; no session here, so nothing is
        # armed and it ends on the by-name statement.
        assert ask.reply.startswith("I haven't shown you a numbered list yet.")
        assert ask.reply.endswith('Ask me by name, like "complete todo call mom".')
    else:
        assert ask.reply == _expected_statement(action)
    assert ask.armed is False


# ── the seam's elif is gone; complete asks through its entry ──


def test_the_2219_elif_is_deleted_and_complete_rides_its_entry():
    source = inspect.getsource(IntentService._dispatch_action_rail)
    assert "elif _floor_write" not in source
    assert "build_floor_write_complete_ask" not in source
    register_default_workflows()
    from services.intent_service.floor_write_ask import complete_todo_write_ask

    assert get_action_workflows()["complete_todo"].write_ask is complete_todo_write_ask
    assert get_action_workflows()["mark_done"].write_ask is complete_todo_write_ask


# ── through the REAL process_intent, only the LLM boundary pinned ──


@pytest.mark.asyncio
async def test_e2e_a_marked_named_create_asks_cxos_question_and_yes_adds_it_once(boundary):
    service = _service(action="create_todo")
    sid = "e2e-2304-create"
    result = await service.process_intent(
        message="I keep meaning to add todo: buy milk", session_id=sid, user_id=_USER
    )
    assert result.message.endswith('Add "buy milk" to your todos? (yes/no)')
    assert "create todo" not in result.message.lower()
    assert _wrote(boundary) == []
    await service.process_intent(message="yes", session_id=sid, user_id=_USER)
    assert boundary["created"] == ["buy milk"]


@pytest.mark.asyncio
async def test_e2e_a_named_create_declined_says_the_thing(boundary):
    service = _service(action="create_todo")
    sid = "e2e-2304-create-no"
    await service.process_intent(
        message="I keep meaning to add todo: buy milk", session_id=sid, user_id=_USER
    )
    declined = await service.process_intent(message="no", session_id=sid, user_id=_USER)
    assert (
        declined.message
        == 'Okay — I won\'t add "buy milk" to your todos. Nothing has been changed.'
    )
    assert _wrote(boundary) == []


@pytest.mark.asyncio
async def test_e2e_a_marked_add_project_with_no_name_asks_the_name_and_arms_no_yes(boundary):
    service = _service(action="add_project")
    sid = "e2e-2304-add"
    result = await service.process_intent(
        message="I keep thinking about a new project", session_id=sid, user_id=_USER
    )
    assert result.message == ADD_PROJECT_NAME_QUESTION
    pending = service.workflow_offer_service.peek_pending_offer(sid, _USER)
    assert pending is not None
    assert pending["pending_action"]["kind"] == ADD_PROJECT_NAME_QUESTION_KIND
    assert pending["workflow_type"] != "confirm_pending_action"


@pytest.mark.asyncio
async def test_e2e_a_marked_write_the_args_cant_name_says_not_sure_and_yes_does_nothing(
    boundary,
):
    service = _service(action="set_timezone")
    sid = "e2e-2304-tz"
    result = await service.process_intent(
        message="I keep meaning to set my timezone to Europe/Helsinki",
        session_id=sid,
        user_id=_USER,
    )
    assert result.message == _DIRECT_LINES["set_timezone"]
    assert service.workflow_offer_service.peek_pending_offer(sid, _USER) is None


@pytest.mark.asyncio
async def test_e2e_complete_still_asks_mark_as_done_after_the_elif(boundary):
    result = await _service().process_intent(
        message="mark high task as done", session_id="e2e-2304-complete", user_id=_USER
    )
    assert result.message == 'Mark "high task" as done? (yes/no)'
    assert _wrote(boundary) == []
