"""1696 — 'delete my reminders' (bulk plural) reaches an explicit bulk path,
not the which-todo ask.

Found in the 1527 named-target lane: post-1527 routing, an EXPLICIT bulk
delete — 'delete my reminders', the literal phrase in 1527's title —
dispatches the delete_todo rail, names no single target (every word is
command vocabulary), and got the single-item clarification "Which todo
should I remove? Try: 'delete todo [number]'". The user who was MORE
explicit got LESS capability: the ambiguous 'clear my reminders' has the
full #1605 three-variant flow, while the explicit imperative was declined
by that flow's ``_EXPLICIT_VERB_RE`` (correctly — the verb isn't ambiguous)
and then fell to a single-item-only handler.

The fix under test (the issue's candidate direction, chosen from evidence):
a second seam in ``run_delete_todo_workflow``, AFTER the #1605 clear-family
seam declines — ``reminder_clear.maybe_handle_explicit_bulk_delete``. When
the delete_todo turn carries a PLURAL domain noun (reminders / todos /
to-dos / tasks), no todo number, no named target, and no exception clause,
it resolves the bulk target set at offer time and arms the clear-family
flow's ALREADY-#1190-GATED delete leg (``_delete_confirmation_offer`` →
``CLEAR_DELETE_WORKFLOW``) with an explicit-delete question. No verb check:
the delete_todo emission IS the verb evidence (so remove / erase /
get rid of ride the same seam), and no stored-preference copy: the user
said delete, so the ask is the plain confirm, never variant 3's
"You've set 'clear' to mean delete" framing.

Layer honesty (m-43): the e2e classes drive the REAL
``IntentService.process_intent`` with classification stubbed to the
surface-2 ``delete_todo`` emission (the 1527/1666 idiom — the 1527 suite
proves surface 1 no longer intercepts these phrasings). The delete boundary
is EXPLOSIVE until a test arms it: nothing may mutate without a confirmed
yes (#1190).

Boundary pins (#1605 both ways, unregressed):
- ambiguous 'clear my reminders' still gets the three-variant flow FIRST
  (the clear seam keeps first claim; the bulk seam never sees it);
- singular unnamed 'delete my reminder' still gets the which-todo ask
  (no plural, no bulk claim);
- exception clauses stay #1563's lane — never a guessed bulk set.
"""

import datetime as _dt
from types import SimpleNamespace
from uuid import uuid4

import pytest

from services.domain.models import Intent, Todo
from services.intent.intent_service import IntentService
from services.intent_service import reminder_clear as rc
from services.intent_service.classifier import IntentClassifier
from services.intent_service.destructive_confirm import (
    CONFIRM_PENDING_ACTION_WORKFLOW,
)
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import IntentCategory

_USER = "9c1e2d40-1696-4b00-9e00-000000001696"  # valid UUID: survives principal parsing


# ---------------------------------------------------------------------------
# Detection unit pins
# ---------------------------------------------------------------------------


class TestDetectExplicitBulkDeleteAsk:
    @pytest.mark.parametrize(
        "message,noun",
        [
            ("delete my reminders", "reminder"),
            ("delete all my reminders", "reminder"),
            ("remove my reminders", "reminder"),
            ("get rid of my reminders", "reminder"),
            ("erase my reminders", "reminder"),
            ("delete my todos", "todo"),
            ("delete my to-dos", "todo"),
            ("delete all my tasks", "todo"),
        ],
    )
    def test_bulk_plural_shapes_detected(self, message, noun):
        assert rc.detect_explicit_bulk_delete_ask(message) == noun

    @pytest.mark.parametrize(
        "message",
        [
            "delete my reminder",  # singular — which one? stays the honest ask
            "delete the hydrate reminder",  # singular, named
            "delete todo 3",  # numbered (number handled by caller too)
            "delete my reminders except the vendor one",  # #1563's lane
            "delete the alpha project",  # no domain noun
            "",
        ],
    )
    def test_non_bulk_shapes_declined(self, message):
        assert rc.detect_explicit_bulk_delete_ask(message) is None

    def test_reminder_noun_wins_mixed_mention(self):
        # same tiebreak as detect_clear_family_ask (#1569)
        assert rc.detect_explicit_bulk_delete_ask("delete my reminders and todos") == "reminder"


# ---------------------------------------------------------------------------
# End-to-end through the REAL process_intent (1527/1605 idiom)
# ---------------------------------------------------------------------------


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — these turns must resolve deterministically"
        )


@pytest.fixture
def live_service():
    register_default_workflows()  # idempotent; the app does this at startup
    return IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))


def _pending_offers(service):
    return service.workflow_offer_service._pending_offers


def _stub_classification(monkeypatch, service, message, action):
    """Deterministic surface-2 emission (the 1666/#1605 idiom)."""
    intent = Intent(
        category=IntentCategory.EXECUTION,
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
    """Two reminder-dated todos + one plain todo: 'reminders' resolves 2,
    'todos' resolves all 3 — the noun scopes the set (#1569)."""
    when = _dt.datetime(2026, 9, 12, 9, 0, tzinfo=_dt.timezone.utc)
    return [
        Todo(
            id=str(uuid4()),
            text="Review the PR",
            priority="medium",
            status="pending",
            completed=False,
            reminder_date=when,
        ),
        Todo(
            id=str(uuid4()),
            text="Call the vendor",
            priority="medium",
            status="pending",
            completed=False,
            reminder_date=when,
        ),
        Todo(
            id=str(uuid4()),
            text="Draft the retro notes",
            priority="medium",
            status="pending",
            completed=False,
        ),
    ]


@pytest.fixture
def todo_boundary(monkeypatch):
    """TodoManagementService boundary: list deterministic; delete EXPLOSIVE
    until a test arms it — nothing may mutate without a confirmed yes."""
    from services.todo.todo_management_service import TodoManagementService

    state = {"todos": _todos(), "deleted": [], "allow_delete": False}

    async def _list_todos(self, user_id, include_completed=False):
        return list(state["todos"])

    async def _delete(self, todo_id, user_id):
        if not state["allow_delete"]:
            raise AssertionError(
                "todo_service.delete_todo FIRED — a destructive mutation "
                "executed without a confirmed yes (#1190 gate breach)"
            )
        state["deleted"].append(str(todo_id))
        return True

    monkeypatch.setattr(TodoManagementService, "list_todos", _list_todos)
    monkeypatch.setattr(TodoManagementService, "delete_todo", _delete)
    return state


@pytest.fixture
def pref_store(monkeypatch):
    """In-memory users.preferences JSONB behind collaboration_gate's seam
    (needed by the #1605 boundary pin — the clear seam reads the store)."""
    from services.intent_service import collaboration_gate as cg

    store: dict = {}

    async def _load(user_id):
        return dict(store)

    async def _save(user_id, key, value):
        store[key] = value
        return True

    monkeypatch.setattr(cg, "_load_preferences", _load)
    monkeypatch.setattr(cg, "_save_preference", _save)
    return store


class TestBulkConfirmArms:
    pytestmark = pytest.mark.asyncio

    @pytest.mark.parametrize(
        "phrase",
        (
            "delete my reminders",  # the 1696 verbatim phrase (1527's title)
            "delete all my reminders",  # RED pre-1696: matching-"all" miss
            "remove my reminders",
            "get rid of my reminders",
        ),
    )
    async def test_bulk_reminder_delete_arms_the_1190_confirm(
        self, live_service, monkeypatch, todo_boundary, phrase
    ):
        """RED pre-1696: 'Which todo should I remove?' (or, for the 'all'
        form, a named-target miss on the word 'all'). GREEN: the bulk set
        resolves at offer time (2 reminder-dated rows), the clear-family
        flow's #1190-gated delete leg arms, nothing deleted on the ask."""
        sid = f"e2e-1696-{hash(phrase) & 0xFFFF}"
        _stub_classification(monkeypatch, live_service, phrase, "delete_todo")
        result = await live_service.process_intent(message=phrase, session_id=sid, user_id=_USER)
        assert result.message == "Delete these 2 reminders? (yes/no)"
        assert result.intent_data.get("destructive_confirmation_pending") is True
        assert result.intent_data.get("action") == rc.CLEAR_DELETE_WORKFLOW
        stored = _pending_offers(live_service).get(sid)
        assert stored is not None
        assert stored["workflow_type"] == CONFIRM_PENDING_ACTION_WORKFLOW
        assert stored["pending_action"]["kind"] == rc.CLEAR_DELETE_CONFIRMATION_KIND
        assert stored["pending_action"]["action"] == rc.CLEAR_DELETE_WORKFLOW
        assert todo_boundary["deleted"] == []

    async def test_todo_noun_scopes_to_all_active_todos(
        self, live_service, monkeypatch, todo_boundary
    ):
        """'delete my todos' → todo vocabulary, ALL 3 active rows (#1569:
        the noun scopes the set — reminders are the reminder-dated subset)."""
        sid = "e2e-1696-todos"
        _stub_classification(monkeypatch, live_service, "delete my todos", "delete_todo")
        result = await live_service.process_intent(
            message="delete my todos", session_id=sid, user_id=_USER
        )
        assert result.message == "Delete these 3 todos? (yes/no)"
        stored = _pending_offers(live_service).get(sid)
        assert stored["pending_action"]["kind"] == rc.CLEAR_DELETE_CONFIRMATION_KIND
        assert todo_boundary["deleted"] == []

    async def test_yes_deletes_exactly_the_bound_reminder_rows(
        self, live_service, monkeypatch, todo_boundary
    ):
        """The confirmed yes deletes the ids bound at OFFER time — the 2
        reminder-dated rows, never the plain todo."""
        sid = "e2e-1696-yes"
        _stub_classification(monkeypatch, live_service, "delete my reminders", "delete_todo")
        await live_service.process_intent(
            message="delete my reminders", session_id=sid, user_id=_USER
        )
        todo_boundary["allow_delete"] = True
        confirmed = await live_service.process_intent(message="yes", session_id=sid, user_id=_USER)
        reminder_ids = {t.id for t in todo_boundary["todos"] if t.reminder_date is not None}
        assert set(todo_boundary["deleted"]) == reminder_ids
        assert "Deleted 2 reminders" in confirmed.message
        assert "Review the PR" in confirmed.message
        assert "Draft the retro notes" not in confirmed.message

    async def test_no_cancels_honestly_and_nothing_fires(
        self, live_service, monkeypatch, todo_boundary
    ):
        sid = "e2e-1696-no"
        _stub_classification(monkeypatch, live_service, "delete my reminders", "delete_todo")
        await live_service.process_intent(
            message="delete my reminders", session_id=sid, user_id=_USER
        )
        result = await live_service.process_intent(message="no", session_id=sid, user_id=_USER)
        assert "won't delete" in result.message
        assert todo_boundary["deleted"] == []
        assert _pending_offers(live_service).get(sid) is None

    async def test_empty_target_set_answers_honestly_and_arms_nothing(
        self, live_service, monkeypatch, todo_boundary
    ):
        """Zero reminder-dated rows: the Pattern-073 verified-empty copy,
        no confirm armed, nothing touched."""
        todo_boundary["todos"] = [t for t in todo_boundary["todos"] if t.reminder_date is None]
        sid = "e2e-1696-empty"
        _stub_classification(monkeypatch, live_service, "delete my reminders", "delete_todo")
        result = await live_service.process_intent(
            message="delete my reminders", session_id=sid, user_id=_USER
        )
        assert "there are none to delete right now" in result.message
        assert "Nothing has been changed" in result.message
        assert _pending_offers(live_service).get(sid) is None
        assert todo_boundary["deleted"] == []


class TestBoundariesUnregressed:
    pytestmark = pytest.mark.asyncio

    async def test_ambiguous_clear_still_gets_the_1605_flow_first(
        self, live_service, monkeypatch, todo_boundary, pref_store
    ):
        """#1605 keeps FIRST CLAIM: an ambiguous 'clear my reminders' the
        classifier guessed as delete_todo runs the three-variant flow (the
        variant-1 verb question here — no stored default), never the
        explicit bulk confirm."""
        sid = "e2e-1696-clear"
        _stub_classification(monkeypatch, live_service, "clear my reminders", "delete_todo")
        result = await live_service.process_intent(
            message="clear my reminders", session_id=sid, user_id=_USER
        )
        assert result.message == rc.variant_one_question("clear", "reminder")
        stored = _pending_offers(live_service).get(sid)
        assert stored["pending_action"]["kind"] == rc.CLEAR_VERB_QUESTION_KIND
        assert todo_boundary["deleted"] == []

    async def test_singular_unnamed_delete_keeps_the_which_todo_ask(
        self, live_service, monkeypatch, todo_boundary
    ):
        """'delete my reminder' (singular, nothing named): which ONE is the
        honest question — the bulk seam must not claim it."""
        sid = "e2e-1696-singular"
        _stub_classification(monkeypatch, live_service, "delete my reminder", "delete_todo")
        result = await live_service.process_intent(
            message="delete my reminder", session_id=sid, user_id=_USER
        )
        assert "Which todo should I remove?" in result.message
        assert _pending_offers(live_service).get(sid) is None
        assert todo_boundary["deleted"] == []

    async def test_exception_clause_never_gets_a_guessed_bulk_set(
        self, live_service, monkeypatch, todo_boundary
    ):
        """'delete my reminders except …' is #1563's set-complement lane —
        whatever answers, it is never the bulk confirm and never a delete."""
        sid = "e2e-1696-except"
        phrase = "delete my reminders except the vendor one"
        _stub_classification(monkeypatch, live_service, phrase, "delete_todo")
        result = await live_service.process_intent(message=phrase, session_id=sid, user_id=_USER)
        assert result.message != "Delete these 2 reminders? (yes/no)"
        stored = _pending_offers(live_service).get(sid)
        assert stored is None or stored["pending_action"].get("kind") != (
            rc.CLEAR_DELETE_CONFIRMATION_KIND
        )
        assert todo_boundary["deleted"] == []

    async def test_named_target_still_arms_the_title_bound_confirm(
        self, live_service, monkeypatch, todo_boundary
    ):
        """The #1527 named-target leg is untouched: 'delete my vendor
        reminder' resolves by name and arms the #1666 title-bound confirm."""
        sid = "e2e-1696-named"
        phrase = "delete my vendor reminder"
        _stub_classification(monkeypatch, live_service, phrase, "delete_todo")
        result = await live_service.process_intent(message=phrase, session_id=sid, user_id=_USER)
        assert result.message == 'Delete todo: "Call the vendor"? (yes/no)'
        assert todo_boundary["deleted"] == []
