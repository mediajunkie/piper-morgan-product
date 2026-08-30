"""#1666 [MVP] — delete_todo onto the rail, #1190-gated (consent-gate coverage gap).

Arch's finding (during the #1663 investigation): delete_todo had NO
WorkflowEntry, so it never reached the #1124 rail check or
``consent_gate``/the CONFIRM branch — it fell to the legacy elif chain and
DELETED IMMEDIATELY with no confirm, while #1663's own worked example
implicitly assumed its DESTRUCTIVE tier was enforced somewhere.

The fix under test: delete_todo + its ActionMapper alias family
(remove_todo / cancel_todo) registered ``effect=EffectClass.DESTRUCTIVE``,
``outwardness=PRIVATE``, ``action_triggered=True`` (the close_issue shape);
the legacy elif REMOVED in the same commit; the #1190 gate arms via the
ASYNC delete-todo builder (positional target → the honest ask needs the
owner-scoped list read), binding the REAL todo text into the question
('Delete todo N: "text"? (yes/no)' — the user confirms WHAT, not just
WHICH) and the resolved row into the intent (the confirmed yes deletes
exactly the row named in the ask, never a positional re-resolve).

Boundary with #1605, pinned BOTH directions:
- ambiguous clear-family shapes classified delete_todo pass through the
  gate untouched → the rail entry point's ``maybe_handle_clear_family``
  seam keeps first claim (three-variant flow, its own #1190-gated delete);
- explicit imperatives ("delete todo 3") are None to
  ``detect_clear_family_ask`` → this gate owns them.

Layer honesty (m-43): the end-to-end classes drive the REAL
``IntentService.process_intent`` (the #1190/#1605 test idiom), mocked ONLY
at the LLM boundary (explosive — classification stubbed deterministically
per turn; answer turns must resolve at the pending-offer seam, which runs
before classification) and the TodoManagementService boundary (explosive
delete until a test arms it — nothing may mutate unconfirmed).
"""

import datetime as _dt
from types import SimpleNamespace
from uuid import uuid4

import pytest

from services.domain.models import Intent, Todo
from services.intent.intent_service import IntentProcessingError, IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.destructive_confirm import (
    CONFIRM_PENDING_ACTION_WORKFLOW,
    DESTRUCTIVE_CONFIRM_KIND,
    RESOLVED_TODO_CONTEXT_KEY,
    TodoDeleteGate,
    build_todo_delete_confirmation,
    is_delete_todo_action,
)
from services.intent_service.reminder_clear import variant_one_question
from services.intent_service.workflow_dispatcher import get_action_workflows
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import EffectClass, IntentCategory, Outwardness

_USER = "3f7b8a52-1666-4b00-9e00-000000001666"  # valid UUID: survives principal parsing

DELETE_TODO_ALIASES = ("delete_todo", "remove_todo", "cancel_todo")

# PM's exact #1650 aside, verbatim — the one-label-two-objects shape that
# fired an armed delete off the greedy accept row pre-#1650. The delete-todo
# confirm rides the same carrier, so the same strict detector must protect it.
PM_ASIDE = (
    "please note that I'll need to figure out later why you thought I "
    "wanted you to delete a project."
)


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — #1666 turns must resolve " "deterministically"
        )


@pytest.fixture
def live_service():
    clf = IntentClassifier(llm_service=_ExplosiveLLM())
    return IntentService(intent_classifier=clf)


def _pending_offers(service):
    return service.workflow_offer_service._pending_offers


def _stub_classification(monkeypatch, service, message, action, category=IntentCategory.EXECUTION):
    """Deterministic classification for turn 1 (the #1605 idiom)."""
    intent = Intent(
        category=category,
        action=action,
        original_message=message,
        confidence=0.95,
        context={"original_message": message},
    )

    async def _classify_multiple(msg, context=None, user_id=None, session_id=None):
        return SimpleNamespace(
            intents=[intent],
            is_multi_intent=False,
            has_greeting=False,
            has_substantive_intent=True,
            primary_intent=intent,
            secondary_intents=[],
        )

    monkeypatch.setattr(service.intent_classifier, "classify_multiple", _classify_multiple)
    return intent


def _todos():
    return [
        Todo(
            id=str(uuid4()),
            text="Review the PR",
            priority="medium",
            status="pending",
            completed=False,
            reminder_date=_dt.datetime(2026, 8, 19, 9, 0, tzinfo=_dt.timezone.utc),
        ),
        Todo(
            id=str(uuid4()),
            text="Call the vendor",
            priority="medium",
            status="pending",
            completed=False,
            reminder_date=_dt.datetime(2026, 8, 19, 10, 0, tzinfo=_dt.timezone.utc),
        ),
    ]


@pytest.fixture
def todo_boundary(monkeypatch):
    """TodoManagementService boundary: list deterministic; delete EXPLOSIVE
    until a test arms it (the #1605 idiom — nothing may mutate unconfirmed)."""
    from services.todo.todo_management_service import TodoManagementService

    state = {"todos": _todos(), "deleted": [], "allow_delete": False}

    async def _list_todos(self, user_id, include_completed=False):
        return list(state["todos"])

    async def _delete(self, todo_id, user_id):
        if not state["allow_delete"]:
            raise AssertionError(
                "todo_service.delete_todo FIRED — a destructive mutation "
                "executed without a confirmed yes (#1666 gate breach)"
            )
        state["deleted"].append(str(todo_id))
        state["todos"] = [t for t in state["todos"] if t.id != str(todo_id)]
        return True

    monkeypatch.setattr(TodoManagementService, "list_todos", _list_todos)
    monkeypatch.setattr(TodoManagementService, "delete_todo", _delete)
    return state


# ---------------------------------------------------------------------------
# 1. Registry: the enum flips (RED while delete_todo was rail-invisible)
# ---------------------------------------------------------------------------


class TestDeleteTodoRailEntries:
    def test_family_registered_destructive_private_action_triggered(self):
        register_default_workflows()
        wf = get_action_workflows()
        for alias in DELETE_TODO_ALIASES:
            assert alias in wf, f"{alias} missing from the action rail (#1666)"
            entry = wf[alias]
            assert (
                entry.effect == EffectClass.DESTRUCTIVE
            ), f"{alias} must be DESTRUCTIVE — deletion is unrecoverable (#1666)"
            assert entry.outwardness == Outwardness.PRIVATE
            assert entry.action_triggered is True

    def test_family_derives_needs_confirm(self):
        """The #1190 gate keys off needs_confirm — derived, never re-derived
        from names."""
        register_default_workflows()
        wf = get_action_workflows()
        for alias in DELETE_TODO_ALIASES:
            assert wf[alias].needs_confirm is True
            assert wf[alias].destructive_hint is True
            assert wf[alias].needs_consent is True  # destructive ⊂ write

    def test_aliases_share_one_entry(self):
        register_default_workflows()
        wf = get_action_workflows()
        assert wf["remove_todo"] is wf["delete_todo"]
        assert wf["cancel_todo"] is wf["delete_todo"]

    def test_family_predicate_matches_registration(self):
        for alias in DELETE_TODO_ALIASES:
            assert is_delete_todo_action(alias)
        assert not is_delete_todo_action("close_issue")
        assert not is_delete_todo_action("complete_todo")
        assert not is_delete_todo_action(None)

    def test_legacy_elif_removed(self):
        """Migration completion (#1411 precedent): the ungated elif branch is
        GONE — the rail is the single dispatch surface for delete_todo."""
        with open("services/intent/intent_service.py", encoding="utf-8") as fh:
            src = fh.read()
        assert 'mapped_action == "delete_todo"' not in src, (
            "the legacy delete_todo elif is back — it dispatches an ungated "
            "immediate delete (#1666's whole finding)"
        )


# ---------------------------------------------------------------------------
# 2. The async confirm builder (unit)
# ---------------------------------------------------------------------------


class _BuilderHandlers:
    """Minimal todo_handlers stand-in for builder unit tests: the real
    _extract_todo_id regex behavior via the real class method, list via stub."""

    def __init__(self, todos=None, raise_on_list=False):
        from services.intent_service.todo_handlers import TodoIntentHandlers

        self._extract = TodoIntentHandlers._extract_todo_id
        self._todos = todos if todos is not None else _todos()
        self._raise = raise_on_list
        outer = self

        class _Svc:
            async def list_todos(self, user_id, include_completed=False):
                if outer._raise:
                    raise RuntimeError("db down")
                return list(outer._todos)

        self.todo_service = _Svc()

    def _extract_todo_id(self, message):
        return self._extract(self, message)


def _delete_intent(message, action="delete_todo"):
    return Intent(
        category=IntentCategory.EXECUTION,
        action=action,
        original_message=message,
        confidence=0.95,
        context={"original_message": message},
    )


class TestConfirmBuilder:
    pytestmark = pytest.mark.asyncio

    async def test_resolved_target_binds_title_and_row(self):
        handlers = _BuilderHandlers()
        intent = _delete_intent("delete todo 1")
        gate = await build_todo_delete_confirmation(intent, handlers, _USER)
        assert gate.offer is not None and not gate.passthrough
        assert gate.offer.question == 'Delete todo 1: "Review the PR"? (yes/no)'
        record = gate.offer.offer
        assert record["workflow_type"] == CONFIRM_PENDING_ACTION_WORKFLOW
        # #1665 invariant: the stored ask IS the said ask, byte-for-byte.
        assert record["question"] == gate.offer.question
        pa = record["pending_action"]
        assert pa["kind"] == DESTRUCTIVE_CONFIRM_KIND
        assert pa["action"] == "delete_todo"
        assert pa["intent"] is intent
        assert pa["summary"] == 'delete todo 1: "Review the PR"'
        assert "won't delete todo 1" in record["decline_message"]
        assert "Nothing has been changed" in record["decline_message"]
        # WHAT-binding: the resolved row rides the intent for the yes turn.
        resolved = intent.context[RESOLVED_TODO_CONTEXT_KEY]
        assert resolved["text"] == "Review the PR"
        assert resolved["todo_id"] == handlers._todos[0].id

    async def test_never_a_number_only_confirm(self):
        """#1666 AC: the user confirms WHAT, not just WHICH — every armed
        question carries the todo's text."""
        handlers = _BuilderHandlers()
        gate = await build_todo_delete_confirmation(
            _delete_intent("delete todo 2"), handlers, _USER
        )
        assert '"Call the vendor"' in gate.offer.question

    async def test_clear_family_shape_passes_through(self):
        """Boundary direction 1: the #1605 seam keeps first claim — the gate
        never steals an ambiguous clear-family shape, even one carrying a
        number the extractor could read."""
        handlers = _BuilderHandlers()
        for message in ("clear my reminders", "clear todo 1", "reset my todos"):
            gate = await build_todo_delete_confirmation(_delete_intent(message), handlers, _USER)
            assert gate.passthrough and gate.offer is None, message

    async def test_no_number_no_named_target_passes_through(self):
        """No number AND nothing named — the handler's which-todo ask is the
        honest turn (the #1527 named-target leg claims only turns that
        actually name a target)."""
        handlers = _BuilderHandlers()
        for message in ("delete it", "delete my reminders"):
            gate = await build_todo_delete_confirmation(_delete_intent(message), handlers, _USER)
            assert gate.passthrough and gate.offer is None, message

    async def test_named_target_without_match_is_honest_didnt_find(self):
        """#1527 named-target leg (was a passthrough pre-1527-scope-close):
        'delete the meeting todo' NAMES a target; against a list with no
        match the gate answers honestly in todo/reminder vocabulary —
        nothing armed, nothing deleted, never a project lookup."""
        handlers = _BuilderHandlers()
        gate = await build_todo_delete_confirmation(
            _delete_intent("delete the meeting todo"), handlers, _USER
        )
        assert gate.clarification is not None
        assert gate.offer is None and not gate.passthrough
        assert "couldn't find a todo or reminder" in gate.clarification
        assert "project" not in gate.clarification.lower()

    async def test_out_of_range_passes_through(self):
        handlers = _BuilderHandlers()
        gate = await build_todo_delete_confirmation(
            _delete_intent("delete todo 9"), handlers, _USER
        )
        assert gate.passthrough and gate.offer is None

    async def test_no_principal_passes_through(self):
        handlers = _BuilderHandlers()
        gate = await build_todo_delete_confirmation(_delete_intent("delete todo 1"), handlers, None)
        assert gate.passthrough and gate.offer is None

    async def test_lookup_failure_is_honest_noop_never_passthrough(self):
        """The one leg that is neither confirm nor passthrough: if the gate
        can't see the list, it neither arms a number-only confirm (AC) nor
        passes a possibly-deleting turn through unverified (the module's
        safe default: an unconfirmed destructive write must never fire)."""
        handlers = _BuilderHandlers(raise_on_list=True)
        gate = await build_todo_delete_confirmation(
            _delete_intent("delete todo 1"), handlers, _USER
        )
        assert gate.error_message is not None
        assert gate.offer is None and not gate.passthrough
        assert "haven't deleted anything" in gate.error_message


# ---------------------------------------------------------------------------
# 3. End-to-end through the REAL process_intent
# ---------------------------------------------------------------------------


class TestEndToEndConfirmFlow:
    pytestmark = pytest.mark.asyncio

    async def test_delete_todo_asks_title_bound_confirm_first(
        self, live_service, monkeypatch, todo_boundary
    ):
        """RED pre-#1666: 'delete todo 1' deleted immediately (the explosive
        delete boundary would have blown). GREEN: the classified turn arms
        the #1190 confirm — title bound, ask stored verbatim (#1665),
        nothing deleted."""
        sid = "e2e-1666-ask"
        _stub_classification(monkeypatch, live_service, "delete todo 1", "delete_todo")
        result = await live_service.process_intent(
            message="delete todo 1", session_id=sid, user_id=_USER
        )
        assert result.message == 'Delete todo 1: "Review the PR"? (yes/no)'
        assert result.intent_data.get("destructive_confirmation_pending") is True
        assert result.requires_clarification is True
        stored = _pending_offers(live_service).get(sid)
        assert stored is not None
        assert stored["pending_action"]["kind"] == DESTRUCTIVE_CONFIRM_KIND
        # #1665: the stored ask is the exact string said this turn.
        assert stored["question"] == result.message
        assert todo_boundary["deleted"] == []

    async def test_crisp_yes_deletes_the_confirmed_row(
        self, live_service, monkeypatch, todo_boundary
    ):
        """The #1650 strict detector applies via the confirm carrier
        automatically; the deletion targets the row bound at ask time."""
        sid = "e2e-1666-yes"
        first_id = todo_boundary["todos"][0].id
        _stub_classification(monkeypatch, live_service, "delete todo 1", "delete_todo")
        await live_service.process_intent(message="delete todo 1", session_id=sid, user_id=_USER)
        todo_boundary["allow_delete"] = True
        result = await live_service.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert todo_boundary["deleted"] == [first_id]
        assert "Review the PR" in result.message
        assert _pending_offers(live_service).get(sid) is None

    async def test_confirmed_yes_deletes_what_was_asked_not_position_n(
        self, live_service, monkeypatch, todo_boundary
    ):
        """WHAT-binding under list shift: a new todo lands at position 1
        between the ask and the yes — the delete still takes the row the
        user confirmed, never the new occupant of position 1."""
        sid = "e2e-1666-shift"
        confirmed_id = todo_boundary["todos"][0].id
        _stub_classification(monkeypatch, live_service, "delete todo 1", "delete_todo")
        await live_service.process_intent(message="delete todo 1", session_id=sid, user_id=_USER)
        interloper = Todo(
            id=str(uuid4()),
            text="Brand new urgent thing",
            priority="high",
            status="pending",
            completed=False,
        )
        todo_boundary["todos"].insert(0, interloper)
        todo_boundary["allow_delete"] = True
        result = await live_service.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert todo_boundary["deleted"] == [confirmed_id]
        assert interloper.id not in todo_boundary["deleted"]
        assert "Review the PR" in result.message

    @pytest.mark.parametrize("negative", ["no", "no thanks", "cancel"])
    async def test_decline_deletes_nothing(
        self, live_service, monkeypatch, todo_boundary, negative
    ):
        sid = f"e2e-1666-no-{negative.replace(' ', '-')}"
        _stub_classification(monkeypatch, live_service, "delete todo 1", "delete_todo")
        await live_service.process_intent(message="delete todo 1", session_id=sid, user_id=_USER)
        result = await live_service.process_intent(message=negative, session_id=sid, user_id=_USER)
        assert 'won\'t delete todo 1: "Review the PR"' in result.message
        assert "Nothing has been changed" in result.message
        assert todo_boundary["deleted"] == []
        assert _pending_offers(live_service).get(sid) is None

    async def test_pm_aside_never_fires_the_armed_delete(
        self, live_service, monkeypatch, todo_boundary
    ):
        """The #1650 tests' aside idiom: PM's exact one-label-two-objects
        aside against the armed delete confirm — neither accept nor decline
        claims it; the pop cancelled the action (nothing can fire it later)
        and the turn falls to normal processing (here the explosive LLM
        boundary, proving no offer seam claimed it)."""
        sid = "e2e-1666-aside"
        _stub_classification(monkeypatch, live_service, "delete todo 1", "delete_todo")
        await live_service.process_intent(message="delete todo 1", session_id=sid, user_id=_USER)

        async def _explosive_classify(msg, context=None, user_id=None, session_id=None):
            raise AssertionError("LLM boundary touched — aside fell to classification")

        monkeypatch.setattr(
            live_service.intent_classifier, "classify_multiple", _explosive_classify
        )
        try:
            result = await live_service.process_intent(
                message=PM_ASIDE, session_id=sid, user_id=_USER
            )
            # However the turn resolves downstream, never the decline copy —
            # declining is not what PM said either.
            assert "won't delete todo 1" not in result.message
        except IntentProcessingError as exc:
            assert "LLM boundary touched" in str(exc) or "INTENT_CLASSIFICATION_FAILED" in str(
                exc
            ), str(exc)
        assert todo_boundary["deleted"] == []  # nothing fired
        assert _pending_offers(live_service).get(sid) is None  # popped

    async def test_alias_remove_todo_rides_the_same_gate(
        self, live_service, monkeypatch, todo_boundary
    ):
        sid = "e2e-1666-alias"
        second_id = todo_boundary["todos"][1].id
        _stub_classification(monkeypatch, live_service, "remove todo 2", "remove_todo")
        result = await live_service.process_intent(
            message="remove todo 2", session_id=sid, user_id=_USER
        )
        assert result.message == 'Delete todo 2: "Call the vendor"? (yes/no)'
        assert todo_boundary["deleted"] == []
        todo_boundary["allow_delete"] = True
        await live_service.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert todo_boundary["deleted"] == [second_id]

    async def test_category_independence(self, live_service, monkeypatch, todo_boundary):
        """The rail dispatches by action BEFORE category routing (#1560
        rationale) — a delete_todo emission under a non-EXECUTION category
        still gets the gate, not the floor."""
        sid = "e2e-1666-category"
        _stub_classification(
            monkeypatch,
            live_service,
            "delete todo 1",
            "delete_todo",
            category=IntentCategory.QUERY,
        )
        result = await live_service.process_intent(
            message="delete todo 1", session_id=sid, user_id=_USER
        )
        assert result.message == 'Delete todo 1: "Review the PR"? (yes/no)'
        assert todo_boundary["deleted"] == []


class TestEndToEndReadOnlyLegs:
    pytestmark = pytest.mark.asyncio

    async def test_no_referent_gets_clarification_not_confirm(
        self, live_service, monkeypatch, todo_boundary
    ):
        """No number and no named target ('delete it') — the handler's
        which-todo ask. (Named-but-unmatched targets now get the #1527
        didn't-find leg instead — pinned in test_delete_todo_named_target_1527.)"""
        sid = "e2e-1666-nonum"
        _stub_classification(monkeypatch, live_service, "delete it", "delete_todo")
        result = await live_service.process_intent(
            message="delete it", session_id=sid, user_id=_USER
        )
        assert "Which todo should I remove?" in result.message
        assert _pending_offers(live_service).get(sid) is None
        assert todo_boundary["deleted"] == []

    async def test_out_of_range_gets_honest_miss_not_confirm(
        self, live_service, monkeypatch, todo_boundary
    ):
        sid = "e2e-1666-range"
        _stub_classification(monkeypatch, live_service, "delete todo 9", "delete_todo")
        result = await live_service.process_intent(
            message="delete todo 9", session_id=sid, user_id=_USER
        )
        assert "couldn't find todo #9" in result.message
        assert _pending_offers(live_service).get(sid) is None
        assert todo_boundary["deleted"] == []

    async def test_lookup_failure_is_honest_noop_turn(
        self, live_service, monkeypatch, todo_boundary
    ):
        from services.todo.todo_management_service import TodoManagementService

        async def _boom(self, user_id, include_completed=False):
            raise RuntimeError("db down")

        monkeypatch.setattr(TodoManagementService, "list_todos", _boom)
        sid = "e2e-1666-lookup"
        _stub_classification(monkeypatch, live_service, "delete todo 1", "delete_todo")
        result = await live_service.process_intent(
            message="delete todo 1", session_id=sid, user_id=_USER
        )
        assert result.success is False
        assert "haven't deleted anything" in result.message
        assert _pending_offers(live_service).get(sid) is None
        assert todo_boundary["deleted"] == []


class TestClearFamilyBoundaryBothWays:
    """The #1605 ↔ #1666 seam, pinned from the #1666 side (the 1605 suite
    pins its own side: explicit deletes get the #1190 confirm there)."""

    pytestmark = pytest.mark.asyncio

    async def test_ambiguous_clear_shape_gets_variant_one_not_delete_confirm(
        self, live_service, monkeypatch, todo_boundary
    ):
        """Direction 1: 'clear my reminders' classified delete_todo — the
        rail entry's clear-family seam runs the three-variant flow; the new
        gate never steals the shape with a 'Delete todo N' confirm."""
        sid = "e2e-1666-clear"
        _stub_classification(monkeypatch, live_service, "clear my reminders", "delete_todo")
        result = await live_service.process_intent(
            message="clear my reminders", session_id=sid, user_id=_USER
        )
        assert result.message == variant_one_question()
        assert "Delete todo" not in result.message
        assert todo_boundary["deleted"] == []

    async def test_explicit_delete_never_gets_variant_one(
        self, live_service, monkeypatch, todo_boundary
    ):
        """Direction 2: the imperative is this gate's — the clear flow's
        _EXPLICIT_VERB_RE guarantees it never claims 'delete todo 1'."""
        sid = "e2e-1666-imperative"
        _stub_classification(monkeypatch, live_service, "delete todo 1", "delete_todo")
        result = await live_service.process_intent(
            message="delete todo 1", session_id=sid, user_id=_USER
        )
        assert variant_one_question() not in result.message
        assert result.message.startswith("Delete todo 1")
