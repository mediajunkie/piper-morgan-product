"""Issues 2415 and 2416: a status turn where code has nothing for the floor to say is
answered by code alone (mechanism B).

Arch 2026-11-23 (01M84SB40Q, 01M84SMP0J), CXO's words (01M84S7E7T), PPM's acceptance
(01M84SKC86).

LAYER: ``IntentService._handle_floor_with_context`` end to end, with the gather, the
milestone resolver and the person's projects replaced at one seam each and the todo
service stubbed; the block is built by the real ``status_todos_for_project`` and the
real todo render. ``ConversationalFloor.respond`` is a mock: on a B turn it fails the
test if awaited. No database, no router call, no model call.
DENOMINATOR: the three GitHub kinds, each with a different block form (a list, no
open todos, todos could not be checked, so both could-not-check lines appear once);
the floor runs for five named content keys, a content-empty-is-nothing key with a
value, an unclassified key, GitHub healthy, no GitHub flags, and a named milestone
absent or tied; today's reply for no arg, no match, several matches and a resolved
milestone; the key guard over ``context_assembler.py``; the seam forms.

Existing pins relied on and not duplicated: ``test_project_status_todos_2301.py``
``TestNothingIsAdded`` (no arg, an arg the person did not say, several, none, no
projects, a failed project read, another op, no principal: the block is ""), and
``TestWhereTheBlockGoes.test_the_milestone_branch_returns_first`` (source order).
"""

import ast
import types
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent_service import project_status_todos as pst
from services.intent_service import status_all_code as sac
from services.intent_service import todo_project_attach as attach
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.shared_types import IntentCategory

REPO = Path(__file__).resolve().parents[4]
ASSEMBLER = REPO / "services" / "intent_service" / "context_assembler.py"
USER = "11111111-1111-1111-1111-111111111111"
MESSAGE = "how is the Mobile Redesign project going?"

_FLOOR_RESPOND = "services.intent_service.conversational_floor.ConversationalFloor.respond"
_GATHER = "services.intent_service.context_assembler.ContextAssembler.gather_context"
_PROVENANCE = "services.intent_service.context_assembler.ContextAssembler.get_last_provenance"
_MILESTONE = "services.intent.intent_service.IntentService._try_resolved_milestone_status"

# What a tester's STATUS gather holds today with GitHub never connected: the clock,
# their projects, their todos (taken out because the block follows), and the
# high-priority gatherer's nothing-shape (no repository resolves).
_BASE = {
    "current_time": "10:00 AM",
    "current_date": "Monday, November 23, 2026",
    "projects": [{"name": "Mobile Redesign"}],
    "project_count": 1,
    "pending_todos": [{"text": "book the venue"}],
    "pending_todo_count": 1,
    "high_priority_issues": [],
    "open_issue_count": 0,
    "open_issue_count_capped": False,
    "github_repo_unconfigured": True,
}
NEVER = {**_BASE, "github_connected": False, "github_needs_reconnecting": False}
RECONNECT = {**_BASE, "github_connected": True, "github_needs_reconnecting": True}
COULDNT = {**_BASE, "github_needs_reconnecting": False, "integrations_source_failed": True}
HEALTHY = {**_BASE, "github_connected": True, "github_needs_reconnecting": False}


def _todo(tid, text):
    return types.SimpleNamespace(
        id=tid, text=text, priority="medium", completed=False, status="pending"
    )


def _handlers(todos=None, fail=None):
    h = TodoIntentHandlers.__new__(TodoIntentHandlers)

    async def list_todos(**kwargs):
        if fail is not None:
            raise fail
        return list(todos or [])

    h.todo_service = MagicMock()
    h.todo_service.list_todos = AsyncMock(side_effect=list_todos)
    h._remember_todo_list_lines = MagicMock()
    return h


@pytest.fixture
def service():
    from services.intent.intent_service import IntentService

    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            svc = IntentService()
    svc.workflow_offer_service = MagicMock()
    svc.workflow_offer_service.peek_pending_offer = MagicMock(return_value=None)
    return svc


@pytest.fixture
def stored(monkeypatch):
    table = {"projects": [types.SimpleNamespace(id="p1", name="Mobile Redesign")]}

    async def _active(user_id):
        return list(table["projects"])

    monkeypatch.setattr(attach, "_active_projects", _active)
    return table


async def _turn(
    service,
    gathered,
    *,
    todos=None,
    fail=None,
    args=None,
    milestone=(None, ""),
    floor_allowed,
    session="s2415",
):
    from services.intent_service.conversational_floor import FloorResponse

    if floor_allowed:
        respond = AsyncMock(return_value=FloorResponse(message="FLOOR: status."))
    else:
        respond = AsyncMock(side_effect=AssertionError("the floor was called on a B turn"))
    service.todo_handlers = _handlers(todos, fail)
    ctx = {"original_message": MESSAGE, "user_id": USER}
    ctx["inversion_args"] = {"project": "Mobile Redesign"} if args is None else args
    intent = Intent(
        category=IntentCategory.STATUS,
        action="get_project_status",
        confidence=0.9,
        original_message=MESSAGE,
        context=ctx,
    )
    with (
        patch(_FLOOR_RESPOND, new=respond),
        patch(_GATHER, new=AsyncMock(return_value=dict(gathered))),
        patch(_PROVENANCE, return_value={}),
        patch(_MILESTONE, new=AsyncMock(return_value=milestone)),
    ):
        result = await service._handle_floor_with_context(intent, session, user_id=USER)
    if not floor_allowed:
        respond.assert_not_awaited()
    return result, respond


LIST_BLOCK = "Open todos in Mobile Redesign:\n1. book the venue\n2. draft the brief"

#: The three B replies, whole, as a person reads them (the report prints these).
RENDERED = {
    "never_connected": (
        "I can't give you GitHub status for Mobile Redesign yet: GitHub isn't connected. "
        "You can connect it in Settings → Integrations.\n\n" + LIST_BLOCK
    ),
    "needs_reconnecting": (
        "I can't give you GitHub status for Mobile Redesign right now: GitHub needs "
        "reconnecting. You can do that in Settings → Integrations → GitHub.\n\n"
        "No open todos in it."
    ),
    "could_not_check": (
        "I couldn't check GitHub for Mobile Redesign just now.\n\n"
        "I couldn't check its todos just now."
    ),
}


@pytest.mark.asyncio
class TestTheReplyIsAllCode:
    async def test_never_connected_with_a_list(self, service, stored):
        todos = [_todo("a", "book the venue"), _todo("b", "draft the brief")]
        result, _ = await _turn(service, NEVER, todos=todos, floor_allowed=False)
        assert result.message == RENDERED["never_connected"]
        assert result.intent_data["status_all_code"] == "never_connected"

    async def test_needs_reconnecting_with_no_open_todos(self, service, stored):
        result, _ = await _turn(service, RECONNECT, todos=[], floor_allowed=False)
        assert result.message == RENDERED["needs_reconnecting"]
        assert result.intent_data["status_all_code"] == "needs_reconnecting"

    async def test_could_not_check_keeps_both_could_not_check_lines(self, service, stored):
        result, _ = await _turn(service, COULDNT, fail=OSError("down"), floor_allowed=False)
        assert result.message == RENDERED["could_not_check"]
        assert result.intent_data["status_all_code"] == "could_not_check"

    async def test_could_not_check_comes_before_needs_reconnecting(self, service, stored):
        both = {**RECONNECT, "integrations_source_failed": True}
        result, _ = await _turn(service, both, todos=[], floor_allowed=False)
        assert result.message.startswith("I couldn't check GitHub for Mobile Redesign")

    async def test_the_header_and_the_line_name_the_stored_project(self, service, stored):
        stored["projects"] = [types.SimpleNamespace(id="p1", name="mobile redesign")]
        result, _ = await _turn(service, NEVER, todos=[_todo("a", "x")], floor_allowed=False)
        assert result.message.startswith("I can't give you GitHub status for mobile redesign yet")
        assert "\n\nOpen todos in mobile redesign:\n1. x" in result.message

    async def test_the_result_shape_and_no_floor_instrumentation(self, service, stored):
        from services.intent_service.conversation_context import get_or_create_context

        session = "s2415-shape"
        result, _ = await _turn(service, NEVER, todos=[], floor_allowed=False, session=session)
        assert result.success is True and result.workflow_id is None
        assert result.requires_clarification is False
        data = result.intent_data
        assert data["category"] == "STATUS" and data["action"] == "get_project_status"
        assert data["confidence"] == 0.9 and data["original_message"] == MESSAGE
        assert data["floor_hit"] is False
        assert data["status_all_code"] == "never_connected"
        # As today: the floor's context keys after the todo keys came out.
        assert data["context_keys"] == list(pst.without_todo_keys(NEVER).keys())
        conv = get_or_create_context(session, user_id=USER)
        assert conv.last_response_was_floor is False
        assert not conv.turn_provenance

    async def test_one_log_event_with_the_kind_and_key_names_only(self, service, stored):
        with patch.object(sac, "logger") as log:
            await _turn(service, RECONNECT, todos=[], floor_allowed=False)
        calls = [c for c in log.info.call_args_list if c.args[0] == "status_all_code_reply"]
        assert len(calls) == 1
        kwargs = calls[0].kwargs
        assert kwargs["kind"] == "needs_reconnecting"
        assert kwargs["context_keys"] == sorted(pst.without_todo_keys(RECONNECT).keys())
        assert "Mobile Redesign" not in repr(kwargs)


CONTENT_CASES = {
    "calendar": {"calendar": {"next_meeting": {"title": "Design review", "start": "2pm"}}},
    "due_reminder": {"due_reminders": ["call the venue"], "reminder_count": 1},
    "blocked_items": {"blocked_items": [{"number": 7, "title": "x"}], "blocked_count": 1},
    "milestone": {"active_milestones": [{"title": "Beta"}], "active_milestone_count": 1},
    "recent_activity": {"recent_activity": [{"title": "PR 9"}], "recent_activity_count": 1},
    "high_priority_issue": {"high_priority_issues": [{"number": 3}], "open_issue_count": 1},
    "calendar_read_failed": {"calendar_source_failed": True},
    "unclassified_key": {"zz_a_key_nobody_classified": "anything"},
}


@pytest.mark.asyncio
class TestTheFloorRunsAsToday:
    @pytest.mark.parametrize("extra", CONTENT_CASES.values(), ids=CONTENT_CASES.keys())
    async def test_a_content_or_unclassified_key(self, service, stored, extra):
        result, respond = await _turn(
            service, {**NEVER, **extra}, todos=[_todo("a", "x")], floor_allowed=True
        )
        respond.assert_awaited_once()
        assert result.message == "FLOOR: status.\n\nOpen todos in Mobile Redesign:\n1. x"
        assert result.intent_data["floor_hit"] is True
        assert "status_all_code" not in result.intent_data

    async def test_github_connected_and_healthy(self, service, stored):
        result, respond = await _turn(service, HEALTHY, todos=[], floor_allowed=True)
        respond.assert_awaited_once()
        assert result.message == "FLOOR: status.\n\nNo open todos in it."

    async def test_no_github_flags_because_the_status_gather_did_not_run(self, service, stored):
        bare = {k: v for k, v in NEVER.items() if not k.startswith("github_")}
        result, respond = await _turn(service, bare, todos=[], floor_allowed=True)
        respond.assert_awaited_once()
        assert result.message == "FLOOR: status.\n\nNo open todos in it."

    async def test_a_named_milestone_absent_or_tied(self, service, stored):
        prefix = "I couldn't find a milestone called Beta.\n\n"
        result, respond = await _turn(
            service, NEVER, todos=[], milestone=(None, prefix), floor_allowed=True
        )
        respond.assert_awaited_once()
        assert result.message == f"{prefix}FLOOR: status.\n\nNo open todos in it."


@pytest.mark.asyncio
class TestPathsBDoesNotTouch:
    """With a B-ready context (GitHub never connected, nothing else), the paths that
    show no block keep today's reply: the floor's message alone."""

    async def test_no_project_arg(self, service, stored):
        result, respond = await _turn(service, NEVER, args={}, floor_allowed=True)
        respond.assert_awaited_once()
        assert result.message == "FLOOR: status."

    async def test_no_match(self, service, stored):
        stored["projects"] = [types.SimpleNamespace(id="p1", name="Launch")]
        result, respond = await _turn(service, NEVER, floor_allowed=True)
        respond.assert_awaited_once()
        assert result.message == "FLOOR: status."

    async def test_several_matches(self, service, stored):
        stored["projects"] = [
            types.SimpleNamespace(id="p1", name="Mobile Redesign"),
            types.SimpleNamespace(id="p2", name="mobile redesign"),
        ]
        result, respond = await _turn(service, NEVER, floor_allowed=True)
        respond.assert_awaited_once()
        assert result.message == "FLOOR: status."

    async def test_a_resolved_milestone(self, service, stored):
        from services.intent.intent_service import IntentProcessingResult

        resolved = IntentProcessingResult(success=True, message="MILESTONE.", intent_data={})
        result, respond = await _turn(service, NEVER, milestone=(resolved, ""), floor_allowed=False)
        assert result is resolved
        service.todo_handlers.todo_service.list_todos.assert_not_awaited()


class TestTheUnit:
    def test_empty_inputs_return_none(self):
        intent = types.SimpleNamespace(action="get_project_status", confidence=1.0)
        intent.original_message = MESSAGE
        ctx = pst.without_todo_keys(NEVER)
        assert sac.status_all_code_result(intent, "STATUS", "x", "P", ctx, "") is not None
        assert sac.status_all_code_result(intent, "STATUS", "", "P", ctx, "") is None
        assert sac.status_all_code_result(intent, "STATUS", "x", None, ctx, "") is None
        assert sac.status_all_code_result(intent, "STATUS", "x", "P", ctx, "pre") is None

    def test_the_content_empty_is_nothing_keys_count_when_they_hold_something(self):
        for key, value in (("high_priority_issues", [{}]), ("open_issue_count", 2)):
            ctx = {**pst.without_todo_keys(NEVER), key: value}
            assert sac._content_keys(ctx) == [key]

    def test_a_none_or_false_ordinary_content_value_still_counts(self):
        for value in (None, False, [], {}):
            ctx = {**pst.without_todo_keys(NEVER), "blocked_items": value}
            assert sac._content_keys(ctx) == ["blocked_items"]

    def test_the_lines_use_the_one_settings_sources(self):
        from services.intent_service.capability_answer import needs_reconnecting_sentence
        from services.intent_service.capability_legibility import SETTINGS_INTEGRATIONS

        assert sac.GITHUB_LINES["needs_reconnecting"].endswith(
            needs_reconnecting_sentence(["GitHub"])
        )
        assert sac.GITHUB_LINES["never_connected"].endswith(f"{SETTINGS_INTEGRATIONS}.")


class TestNoSeamForm:
    SEAM_FORMS = (
        "ask me directly",
        "tell me directly",
        "Nothing has been done yet",
        "To do that, say",
    )

    def test_no_reply_template_carries_a_seam_form(self):
        templates = list(sac.GITHUB_LINES.values()) + list(RENDERED.values())
        for text in templates:
            for form in self.SEAM_FORMS:
                assert form not in text, (form, text)

    def test_no_reply_asks_a_question(self):
        for text in sac.GITHUB_LINES.values():
            assert "?" not in text


class TestTheKeyClassification:
    def test_the_two_sets_are_disjoint(self):
        kc = sac.KEY_CLASSIFICATION
        assert not (kc.content & kc.status_or_own_record)

    def test_empty_is_no_content_is_part_of_content(self):
        kc = sac.KEY_CLASSIFICATION
        assert kc.empty_is_no_content <= kc.content


# The STATUS gather's functions in context_assembler.py: gather_context and everything
# _gather_status_priority_context and the reminder rider call.
STATUS_GATHER_FUNCTIONS = (
    "gather_context",
    "_gather_status_priority_context",
    "_gather_calendar_context",
    "_compute_calendar_context",
    "_get_user_context_cached",
    "_compute_user_context",
    "_get_pending_todos_cached",
    "_compute_pending_todos",
    "_gather_reminder_context",
    "_compute_reminder_context",
    "_gate_due_reminder_mentions",
    "_gather_blocked_items_context",
    "_get_blocked_items_cached",
    "_compute_blocked_items",
    "_gather_high_priority_issues_context",
    "_get_high_priority_issues_cached",
    "_compute_high_priority_issues",
    "_gather_active_milestones_context",
    "_get_active_milestones_cached",
    "_compute_active_milestones",
    "_gather_recent_activity_context",
    "_get_recent_activity_cached",
    "_slice_recent_activity",
    "_compute_recent_activity",
)
TRACKED_DICTS = frozenset({"context", "result", "reminder_ctx", "gated", "failed_flags", "out"})


def _str_keys(node):
    return [k.value for k in node.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)]


def _emitted_keys():
    """The literal keys the STATUS gather functions put in the dicts they return.

    WHAT IT SCANS (``ast`` over ``context_assembler.py``, only inside the functions in
    ``STATUS_GATHER_FUNCTIONS``): ``X["key"] = ...`` and ``X["key"] += ...`` where X is
    a name in ``TRACKED_DICTS``; the top-level string keys of a dict literal that is
    returned or assigned to a tracked name; string arguments of
    ``failed_flags.append(...)``; string elements of a tuple passed to
    ``_UserContextReadFailed(...)`` (those become ``context[flag] = True``).

    WHAT IT CANNOT SEE: keys built at run time (``context[flag]``, the comprehension in
    ``_gather_recent_activity_context``'s ``out.update``: their names are the literals
    scanned above, but a new run-time source of names would be missed); keys added
    outside this file (``first_contact.gather_first_contact_demo``,
    ``intent_service``'s ``guided_flow_escape``: classified by hand); a gatherer that
    is newly called but not added to ``STATUS_GATHER_FUNCTIONS``; nested dicts (the
    values under ``calendar`` or ``priorities``, which are not floor keys). A key the
    classification does not know still counts as content at run time, so a miss here
    keeps today's behaviour rather than skipping the floor."""
    tree = ast.parse(ASSEMBLER.read_text(encoding="utf-8"))
    functions = {
        node.name: node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    missing = [name for name in STATUS_GATHER_FUNCTIONS if name not in functions]
    assert missing == [], f"renamed or removed gatherers: {missing}"
    keys = {}
    for name in STATUS_GATHER_FUNCTIONS:
        for node in ast.walk(functions[name]):
            found = []
            targets = []
            if isinstance(node, ast.Assign):
                targets = node.targets
            elif isinstance(node, (ast.AnnAssign, ast.AugAssign)):
                targets = [node.target]
            for target in targets:
                if (
                    isinstance(target, ast.Subscript)
                    and isinstance(target.value, ast.Name)
                    and target.value.id in TRACKED_DICTS
                    and isinstance(target.slice, ast.Constant)
                    and isinstance(target.slice.value, str)
                ):
                    found.append(target.slice.value)
                if (
                    isinstance(target, ast.Name)
                    and target.id in TRACKED_DICTS
                    and isinstance(getattr(node, "value", None), ast.Dict)
                ):
                    found.extend(_str_keys(node.value))
            if isinstance(node, ast.Return) and isinstance(node.value, ast.Dict):
                found.extend(_str_keys(node.value))
            if isinstance(node, ast.Call):
                func = node.func
                if (
                    isinstance(func, ast.Attribute)
                    and func.attr == "append"
                    and isinstance(func.value, ast.Name)
                    and func.value.id == "failed_flags"
                ):
                    found.extend(
                        a.value
                        for a in node.args
                        if isinstance(a, ast.Constant) and isinstance(a.value, str)
                    )
                if isinstance(func, ast.Name) and func.id == "_UserContextReadFailed":
                    for arg in node.args:
                        if isinstance(arg, ast.Tuple):
                            found.extend(
                                e.value
                                for e in arg.elts
                                if isinstance(e, ast.Constant) and isinstance(e.value, str)
                            )
            for key in found:
                keys.setdefault(key, name)
    return keys


class TestTheKeyGuard:
    def test_the_scan_sees_the_keys_it_guards(self):
        keys = _emitted_keys()
        for known in (
            "current_time",
            "github_connected",
            "github_needs_reconnecting",
            "integrations_source_failed",
            "calendar",
            "blocked_items",
            "active_milestones",
            "recent_activity",
            "high_priority_issues",
            "github_repo_unconfigured",
            "projects_source_failed",
            "github_activity_source_failed",
            "due_reminders",
            "pending_todos_in_reminders",
        ):
            assert known in keys, known

    def test_every_key_a_status_gatherer_emits_is_classified(self):
        kc = sac.KEY_CLASSIFICATION
        known = kc.content | kc.status_or_own_record
        unclassified = {k: fn for k, fn in _emitted_keys().items() if k not in known}
        assert unclassified == {}, (
            "classify each key in status_all_code.KEY_CLASSIFICATION (content unless "
            f"it is a GitHub status flag or the person's own record): {unclassified}"
        )

    def test_the_hand_classified_keys_from_other_modules_are_listed(self):
        content = sac.KEY_CLASSIFICATION.content
        for key in ("first_contact_demo", "first_contact_source_failed", "guided_flow_escape"):
            assert key in content
        first_contact = (REPO / "services" / "intent_service" / "first_contact.py").read_text()
        assert '"first_contact_demo"' in first_contact
        assert '"first_contact_source_failed"' in first_contact
