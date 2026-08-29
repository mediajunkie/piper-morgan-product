"""1527 — narrow the pre-classifier's greedy delete-claims so reminder/todo-noun
deletes stop misrouting to the project lane.

PM live 2026-08-29 (v64, flip ON): THREE misroutes in one exchange —
'delete the reminder to hydrate' answered with "couldn't find a project
called 'the reminder to hydrate'", then Piper ITSELF taught "drop me a quick
line like 'delete my hydrate reminder'" and that EXACT phrase misrouted to
the project lane, twice. Mechanism: surface 1's PORTFOLIO delete patterns
(``\\bdelete\\s+…(.+)`` and siblings) claimed every delete+noun turn with a
greedy capture, so no later surface — including the flipped router — ever
saw the message.

The fix under test is NARROWING ONLY: the delete-family PORTFOLIO patterns
(delete / remove / get rid of) decline via a negative lookahead
(``REMINDER_TODO_NOUN_GUARD``) whenever the delete-target noun phrase
carries reminder/todo vocabulary (reminder(s), todo(s), to-do(s), task(s)).
A guarded miss is a fall-through to the LLM lane — whose delete_todo
emission dispatches the 1666 DESTRUCTIVE rail family — never a reroute:
no new pre-classifier claim is added anywhere. Companion narrowing, exposed
by the fix: REMINDER_QUERY_BLOCKERS gains the phrasal destructive verb
"get rid of" so the reminder LIST lane cannot claim the destructive ask the
portfolio lane just released.

Layer honesty (m-43), per test class:
- The Surface-1 classes call ``PreClassifier.pre_classify`` AND
  ``PreClassifier.detect_multiple_intents`` directly — BOTH pattern entry
  surfaces, since PORTFOLIO_PATTERNS is consulted by each. This is the
  actual fix pin: re-widening the pattern fails here first.
- The end-to-end class drives the REAL ``IntentService.process_intent``
  with classification stubbed to the surface-2 ``delete_todo`` emission
  (the 1666 idiom). The stub is justified by the Surface-1 classes: they
  prove the pre-classifier no longer intercepts these phrasings, so
  surface 2 is what actually sees them; its expected emission for an
  explicit reminder/todo delete is the delete_todo family. The e2e pins
  the routed DESTINATION: the todo delete rail — an honest todo-family
  turn, never a project lookup — and that the 1666 title-bound confirm
  still arms unregressed.
"""

import datetime as _dt
from types import SimpleNamespace
from uuid import uuid4

import pytest

from services.domain.models import Intent, Todo
from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.destructive_confirm import DESTRUCTIVE_CONFIRM_KIND
from services.intent_service.pre_classifier import PreClassifier
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import IntentCategory

_USER = "3f7b8a52-1527-4b00-9e00-000000001527"  # valid UUID: survives principal parsing

# PM's exact phrasings from the 2026-08-29 live round (v64), plus the issue's
# original plural. 'delete my hydrate reminder' is the phrase Piper itself
# taught and then denied — twice.
PM_PHRASES = (
    "delete the reminder to hydrate",
    "delete my hydrate reminder",
    "delete my reminders",
)

# The same misroute through the sibling delete-family verbs and the todo
# vocabulary — every word the guard names.
VOCAB_PHRASES = (
    "remove my hydrate reminder",
    "get rid of my reminders",
    "delete the todo about standup",
    "delete my to-do about standup",
    "delete the task about standup",
)

# Legitimate project-lane deletes: the guard must not touch these.
PROJECT_PHRASES = (
    "delete the alpha project",
    "delete my project alpha",
    "remove the old project",
    "get rid of the alpha project",
)


def _single(phrase):
    return PreClassifier.pre_classify(phrase)


def _multi(phrase):
    return PreClassifier.detect_multiple_intents(phrase).intents


# ---------------------------------------------------------------------------
# 1. Surface 1 declines the reminder/todo-noun deletes (the fix pin)
# ---------------------------------------------------------------------------


class TestSurfaceOneDeclinesReminderTodoDeletes:
    @pytest.mark.parametrize("phrase", PM_PHRASES + VOCAB_PHRASES)
    def test_single_intent_path_falls_through(self, phrase):
        """RED pre-1527: PORTFOLIO/manage_portfolio at confidence 1.0.
        GREEN: no surface-1 claim at all — the turn reaches the LLM lane."""
        assert _single(phrase) is None

    @pytest.mark.parametrize("phrase", PM_PHRASES + VOCAB_PHRASES)
    def test_multi_intent_path_falls_through(self, phrase):
        """detect_multiple_intents consults the same PORTFOLIO_PATTERNS via
        its own pattern-group loop — both entry surfaces must decline."""
        assert _multi(phrase) == []


# ---------------------------------------------------------------------------
# 2. No over-narrowing: the project lane keeps its legitimate claims
# ---------------------------------------------------------------------------


class TestProjectLaneUnaffected:
    @pytest.mark.parametrize("phrase", PROJECT_PHRASES)
    def test_project_deletes_still_claim_single(self, phrase):
        intent = _single(phrase)
        assert intent is not None
        assert intent.category == IntentCategory.PORTFOLIO
        assert intent.action == "manage_portfolio"

    @pytest.mark.parametrize("phrase", PROJECT_PHRASES)
    def test_project_deletes_still_claim_multi(self, phrase):
        intents = _multi(phrase)
        assert [(i.category, i.action) for i in intents] == [
            (IntentCategory.PORTFOLIO, "manage_portfolio")
        ]

    def test_archive_family_untouched(self):
        """The guard rides the DELETE-family patterns only."""
        intent = _single("archive my project alpha")
        assert intent is not None
        assert intent.action == "manage_portfolio"


# ---------------------------------------------------------------------------
# 3. The reminder LIST lane: reads keep claiming, the released destructive
#    ask does not leak into it
# ---------------------------------------------------------------------------


class TestReminderListLaneBoundary:
    @pytest.mark.parametrize(
        "phrase",
        ("what reminders do i have", "show my reminders", "check my reminders"),
    )
    def test_list_reads_still_claim(self, phrase):
        intent = _single(phrase)
        assert intent is not None
        assert intent.action == "list_reminders_query"

    def test_get_rid_of_never_lands_in_the_list_lane(self):
        """Exposed by the 1527 narrowing: with the portfolio claim gone,
        'get rid of my reminders' reached REMINDER_QUERY_PATTERNS and the
        destructive-verb blocker missed the phrasal form. A destructive ask
        must never be answered with a list."""
        assert _single("get rid of my reminders") is None
        assert _multi("get rid of my reminders") == []


# ---------------------------------------------------------------------------
# 4. End-to-end: the routed destination is the todo delete family
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


@pytest.fixture
def todo_boundary(monkeypatch):
    """TodoManagementService boundary: list deterministic (PM's hydrate
    reminder is row 1); delete EXPLOSIVE — nothing in these tests confirms,
    so nothing may mutate."""
    from services.todo.todo_management_service import TodoManagementService

    state = {
        "todos": [
            Todo(
                id=str(uuid4()),
                text="hydrate",
                priority="medium",
                status="pending",
                completed=False,
                reminder_date=_dt.datetime(2026, 8, 29, 9, 0, tzinfo=_dt.timezone.utc),
            ),
        ],
        "deleted": [],
    }

    async def _list_todos(self, user_id, include_completed=False):
        return list(state["todos"])

    async def _delete(self, todo_id, user_id):
        raise AssertionError(
            "todo_service.delete_todo FIRED — a destructive mutation "
            "executed without a confirmed yes"
        )

    monkeypatch.setattr(TodoManagementService, "list_todos", _list_todos)
    monkeypatch.setattr(TodoManagementService, "delete_todo", _delete)
    return state


class TestEndToEndRoutedDestination:
    pytestmark = pytest.mark.asyncio

    @pytest.mark.parametrize("phrase", PM_PHRASES)
    async def test_pm_phrasings_land_in_the_todo_family_not_a_project_lookup(
        self, live_service, monkeypatch, todo_boundary, phrase
    ):
        """RED pre-1527 (behaviorally): surface 1 claimed the turn as
        PORTFOLIO/manage_portfolio and the canonical handler answered
        "I couldn't find a project called '…'". GREEN: the turn dispatches
        the delete_todo rail — the no-number leg answers with the todo
        family's own clarification, deletes nothing, and never mentions a
        project."""
        _stub_classification(monkeypatch, live_service, phrase, "delete_todo")
        result = await live_service.process_intent(
            message=phrase, session_id=f"e2e-1527-{hash(phrase) & 0xFFFF}", user_id=_USER
        )
        # never the project lane's copy:
        assert "couldn't find a project" not in result.message.lower()
        assert "project" not in result.message.lower()
        # the todo delete family's own no-number clarification:
        assert "Which todo should I remove?" in result.message
        assert result.intent_data.get("action") == "delete_todo"
        assert todo_boundary["deleted"] == []

    async def test_numbered_delete_still_arms_the_title_bound_confirm(
        self, live_service, monkeypatch, todo_boundary
    ):
        """The 1666 DESTRUCTIVE confirm flow is the correct destination and
        must still arm — title bound to the REAL row ('hydrate'), nothing
        deleted on the ask turn."""
        sid = "e2e-1527-confirm"
        _stub_classification(monkeypatch, live_service, "delete todo 1", "delete_todo")
        result = await live_service.process_intent(
            message="delete todo 1", session_id=sid, user_id=_USER
        )
        assert result.message == 'Delete todo 1: "hydrate"? (yes/no)'
        assert result.intent_data.get("destructive_confirmation_pending") is True
        stored = live_service.workflow_offer_service._pending_offers.get(sid)
        assert stored is not None
        assert stored["pending_action"]["kind"] == DESTRUCTIVE_CONFIRM_KIND
        assert todo_boundary["deleted"] == []
