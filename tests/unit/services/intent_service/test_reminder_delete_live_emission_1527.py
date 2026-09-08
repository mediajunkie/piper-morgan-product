"""1527 (v70 regression) — PM's exact phrasing through the REAL classifier path.

PM live 2026-09-08 ~05:15 (v70): "delete my hydrate reminder" → "I can't do
that from chat yet — that capability is still on the way." — the GENERIC
unwired-write decline (unwired_writes.GENERIC_UNWIRED_WRITE_DECLINE), a FALSE
claim about our own capability: the v67 named-target delete rail was live and
confirm-gated the whole time.

Why the previous pin missed it (test_delete_todo_named_target_1527.py): its
e2e classes stubbed classify_multiple with the surface-2 ``delete_todo``
emission — but the LIVE classifier never emits ``delete_todo`` for this
phrasing. Captured verbatim from the real LLM (3/3 runs, 2026-09-08):

    {"category": "execution", "verb": "delete", "source_type": "reminder",
     "action": "delete_reminder", "confidence": 0.95, ...}

``delete_reminder`` was not a rail key, not an ActionMapper key, and
``(Verb.DELETE, *)`` had no shim cell — so the emission fell past the rail to
``_handle_execution_intent``'s else-branch and the generic decline. A
routing-gap at root, presenting to PM as fabricated absence.

The fix under test (registry-level, no classifier-prompt change):
- ``_VERB_SOURCE_TO_ACTION`` gains todo-domain DELETE cells
  ((DELETE, reminder/todo/task) → delete_todo) so the observed verb-carrying
  emission canonicalizes at the parse boundary;
- the rail + ActionMapper + ``_DELETE_TODO_FAMILY`` gain the reminder-noun
  raw-emission aliases (delete_reminder/remove_reminder/cancel_reminder) so a
  verb-LESS free-form emission dispatches too (defense in depth — the same
  two-leg discipline as the create family's add_reminder, #1426).

Layer honesty (m-43): these tests drive the REAL ``IntentService.process_intent``
with the REAL ``classify_multiple`` → ``classify`` → pre-classifier →
``_classify_with_reasoning`` JSON-parse → verb shim → rail chain. The ONLY
mocked seam is the LLM boundary itself (``llm.complete``), which returns the
live trace's emission verbatim; any other LLM consultation is explosive. The
TodoManagementService boundary is explosive-until-armed (nothing mutates
unconfirmed).
"""

import datetime as _dt
import json
from uuid import uuid4

import pytest

from services.domain.models import Todo
from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.unwired_writes import GENERIC_UNWIRED_WRITE_DECLINE
from services.intent_service.workflow_entries import register_default_workflows

_USER = "3f7b8a52-1527-4b00-9e00-000000000070"  # valid UUID: survives principal parsing

_PM_PHRASE = "delete my hydrate reminder"

# The live classifier's response for _PM_PHRASE, captured verbatim 2026-09-08
# (identical action/category across 3/3 runs; confidence 0.9-0.95).
_LIVE_EMISSION = {
    "category": "execution",
    "verb": "delete",
    "source_type": "reminder",
    "action": "delete_reminder",
    "confidence": 0.95,
    "reasoning": (
        "The query is a direct request to perform an action, specifically to "
        "delete a reminder, which aligns with the EXECUTION category."
    ),
    "helpful_knowledge_domains": ["task_management", "reminder_systems"],
    "ambiguity_notes": [],
    "knowledge_used": [],
}


class _PinnedEmissionLLM:
    """The LLM boundary: returns the pinned live emission for the intent-
    classification call; ANY other consultation (floor, entity extraction,
    a second classification…) is explosive — these turns must resolve
    deterministically past the one classification draw."""

    def __init__(self, emission: dict):
        self._payload = json.dumps(emission)
        self.classification_calls = 0

    async def complete(self, task_type=None, **kwargs):
        if task_type != "intent_classification":
            raise AssertionError(
                f"LLM boundary touched for task_type={task_type!r} — only the "
                "classification draw may consult the LLM on these turns"
            )
        self.classification_calls += 1
        return self._payload

    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name}) beyond complete()")


def _todo(text):
    return Todo(
        id=str(uuid4()),
        text=text,
        priority="medium",
        status="pending",
        completed=False,
        reminder_date=_dt.datetime(2026, 9, 8, 6, 0, tzinfo=_dt.timezone.utc),
    )


def _service_with(emission: dict):
    register_default_workflows()  # idempotent; the app does this at startup
    llm = _PinnedEmissionLLM(emission)
    return IntentService(intent_classifier=IntentClassifier(llm_service=llm)), llm


@pytest.fixture
def todo_boundary(monkeypatch):
    """TodoManagementService boundary: list deterministic (PM's hydrate
    reminder is row 1); delete EXPLOSIVE until a test arms it."""
    from services.todo.todo_management_service import TodoManagementService

    state = {
        "todos": [_todo("hydrate"), _todo("Review the PR")],
        "deleted": [],
        "allow_delete": False,
    }

    async def _list_todos(self, user_id, include_completed=False):
        return list(state["todos"])

    async def _delete(self, todo_id, user_id):
        if not state["allow_delete"]:
            raise AssertionError(
                "todo_service.delete_todo FIRED — a destructive mutation "
                "executed without a confirmed yes"
            )
        state["deleted"].append(str(todo_id))
        state["todos"] = [t for t in state["todos"] if t.id != str(todo_id)]
        return True

    monkeypatch.setattr(TodoManagementService, "list_todos", _list_todos)
    monkeypatch.setattr(TodoManagementService, "delete_todo", _delete)
    return state


class TestLiveEmissionReachesTheBuiltPath:
    pytestmark = pytest.mark.asyncio

    async def test_pm_exact_phrase_with_live_emission_arms_title_bound_confirm(self, todo_boundary):
        """The v70 transcript, replayed with the fix: PM's exact phrasing,
        the live classifier emission verbatim → the title-bound DESTRUCTIVE
        confirm — never the capability decline."""
        service, llm = _service_with(_LIVE_EMISSION)
        result = await service.process_intent(
            message=_PM_PHRASE, session_id="e2e-live-emission", user_id=_USER
        )
        assert llm.classification_calls == 1  # the real path drew the LLM once
        assert result.message == 'Delete todo: "hydrate"? (yes/no)'
        assert result.intent_data.get("destructive_confirmation_pending") is True
        assert todo_boundary["deleted"] == []

    async def test_pm_exact_phrase_never_gets_the_generic_decline(self, todo_boundary):
        """The regression pinned at the copy level: the false 'still on the
        way' claim must never answer this turn again."""
        service, _ = _service_with(_LIVE_EMISSION)
        result = await service.process_intent(
            message=_PM_PHRASE, session_id="e2e-live-no-decline", user_id=_USER
        )
        assert result.message != GENERIC_UNWIRED_WRITE_DECLINE
        assert "can't do that from chat" not in result.message
        assert "still on the way" not in result.message
        assert result.intent_data.get("unwired_action") is None

    async def test_confirmed_yes_deletes_the_bound_row(self, todo_boundary):
        """End of the lane: confirm → yes → exactly the named row deleted."""
        service, _ = _service_with(_LIVE_EMISSION)
        sid = "e2e-live-yes"
        hydrate_id = todo_boundary["todos"][0].id
        result = await service.process_intent(message=_PM_PHRASE, session_id=sid, user_id=_USER)
        assert result.message == 'Delete todo: "hydrate"? (yes/no)'
        todo_boundary["allow_delete"] = True
        result = await service.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert todo_boundary["deleted"] == [hydrate_id]
        assert "hydrate" in result.message

    async def test_verbless_free_form_emission_dispatches_via_rail_alias(self, todo_boundary):
        """Defense-in-depth leg: the same free-form action WITHOUT the
        canonical verb (shim never fires) still reaches the rail through the
        delete_reminder alias key — the two legs fail independently."""
        emission = dict(_LIVE_EMISSION, verb=None, source_type=None)
        service, _ = _service_with(emission)
        result = await service.process_intent(
            message=_PM_PHRASE, session_id="e2e-live-verbless", user_id=_USER
        )
        assert result.message == 'Delete todo: "hydrate"? (yes/no)'
        assert result.intent_data.get("destructive_confirmation_pending") is True
        assert todo_boundary["deleted"] == []


# ---------------------------------------------------------------------------
# PM's 07:09-07:10 live probe round (2026-09-08, real account, v70) — three
# phrasings that halved the hypothesis space: both delete-verb forms hit the
# identical generic decline; the complete-verb form worked perfectly. Raw
# emissions captured verbatim from the live classifier (2/2 runs each):
#
#   "delete the hydrate reminder"  -> verb=delete   action=delete_reminder
#   "remove my hydrate reminder"   -> verb=delete   action=remove_reminder
#   "complete my hydrate reminder" -> verb=complete action=complete_reminder
#
# NONE of the three raw actions is an ActionMapper key. Completion worked
# live because the verb shim ALREADY carried (COMPLETE, None) ->
# complete_todo — the DELETE verb had no cell at all. That asymmetry, not
# mapper complete-family aliases, is why one verb family routed and the
# other fell to the false capability decline.
# ---------------------------------------------------------------------------

_PROBE_DELETE_THE = dict(
    _LIVE_EMISSION,
    action="delete_reminder",
    confidence=0.9,
    reasoning=(
        "The user explicitly requests to delete a specific reminder, which "
        "is an action-oriented task."
    ),
)
_PROBE_REMOVE_MY = dict(
    _LIVE_EMISSION,
    action="remove_reminder",
    confidence=0.9,
    reasoning=(
        "The user is requesting to remove a specific reminder, which is an " "action to perform."
    ),
)
_PROBE_COMPLETE_MY = dict(
    _LIVE_EMISSION,
    verb="complete",
    action="complete_reminder",
    confidence=0.9,
    reasoning=(
        "The user is requesting to complete a specific task related to a "
        "reminder, indicating an action to be executed."
    ),
    ambiguity_notes=["missing: specific detail about the reminder"],
)


class TestPmProbeRoundPhrasings:
    pytestmark = pytest.mark.asyncio

    @pytest.mark.parametrize(
        ("phrase", "emission"),
        [
            ("delete the hydrate reminder", _PROBE_DELETE_THE),
            ("remove my hydrate reminder", _PROBE_REMOVE_MY),
        ],
        ids=["delete-the", "remove-my"],
    )
    async def test_both_delete_probe_phrasings_arm_the_confirm(
        self, todo_boundary, phrase, emission
    ):
        """PM's two failing probe phrasings, each with its own verbatim live
        emission: both must arm the title-bound confirm, never the decline."""
        service, _ = _service_with(emission)
        result = await service.process_intent(
            message=phrase, session_id=f"e2e-probe-{emission['action']}", user_id=_USER
        )
        assert result.message == 'Delete todo: "hydrate"? (yes/no)'
        assert result.intent_data.get("destructive_confirmation_pending") is True
        assert "still on the way" not in result.message
        assert todo_boundary["deleted"] == []

    async def test_complete_probe_phrasing_still_completes_no_confirm(self, todo_boundary):
        """The control that worked live ('Nice - I've marked hydrate as
        done') — pinned so the COMPLETE shim cell that carried it can't
        silently regress, and so the delete fix demonstrably didn't drag
        completion into the DESTRUCTIVE confirm tier (WRITE-class stays
        no-confirm)."""
        from services.todo.todo_management_service import TodoManagementService

        completed = []

        async def _complete(self, todo_id, user_id):
            row = next(t for t in todo_boundary["todos"] if t.id == str(todo_id))
            completed.append(row.text)
            row.completed = True
            return row

        import unittest.mock as _mock

        with _mock.patch.object(TodoManagementService, "complete_todo", _complete):
            service, _ = _service_with(_PROBE_COMPLETE_MY)
            result = await service.process_intent(
                message="complete my hydrate reminder",
                session_id="e2e-probe-complete",
                user_id=_USER,
            )
        assert completed == ["hydrate"]
        assert "hydrate" in result.message
        assert "(yes/no)" not in result.message  # WRITE-class: no confirm gate
        assert result.intent_data.get("destructive_confirmation_pending") is None
        assert todo_boundary["deleted"] == []
