"""1654 (v70 regression) — bare "remind me" through the REAL classifier path.

PM live 2026-09-08 ~05:15 (v70):

    PM:     remind me
    Piper:  What would you like me to remind you about, and when?  [+ due list]
    PM:     make coffee
    Piper:  Ha — I wish. That one's outside what I can do from here.

The merged what-and-when question is NOT a literal string anywhere in the
repo — the conversational FLOOR composed it. Live routing trace (real
classifier, 3/3 runs pre-fix): bare "remind me" → pre_classify None →
LLM emitted {"category": "unknown", "action": "clarification_needed",
"confidence": 0.6} → the vague-conversion returned CONVERSATION/
clarification_needed → CONVERSATION is floor-routed → the floor asked a
clarify question WITHOUT arming a carrier (the #1648 breach: carriers own
clarify questions). PM's bare answer then orphaned into the routing chain
as a literal request — the exact #1654 class, at a site the armed
two-question chain never won.

The fix under test: the winning site loses the turn to the path that arms.
One classifier-prompt example ("remind me" → execution/create_reminder;
corpus row deposited per the 8/29 policy in the same commit) routes the
turn to the rail-registered create_reminder entry → handle_create_reminder
→ _extract_reminder_text returns None → the #1654 no-task clarify ARMS the
reminder_task_question carrier. The answer binds at the offer seam and
chains into the #1648 time question — the full two-question recovery, which
test_task_clarify_1654.py already pins from its deterministically-claimed
entry ("set a reminder: …"); THIS file pins the LLM-lane entry that failed
live.

Live emission after the prompt change (captured verbatim, 3/3 runs
2026-09-08): execution/create_reminder, confidence 0.7 — and the
vague-conversion does not fire (action not in the vague set; ambiguity
notes live in reasoning, not intent.context).

Layer honesty (m-43): real ``process_intent`` → ``classify_multiple`` →
pre-classifier → JSON-parse → rail → consent gate → handler chain. The LLM
boundary alone is pinned, and it permits EXACTLY ONE classification draw —
any later consultation means an answer turn escaped the offer seam, which
is the orphan shape itself, so it explodes. TodoManagementService is
mocked at the seam (binding/chaining under test, not persistence).
"""

import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.todo_handlers import (
    _TIME_ASK,
    REMINDER_TASK_QUESTION_KIND,
    REMINDER_TIME_QUESTION_KIND,
)
from services.intent_service.workflow_entries import register_default_workflows

GATE = "services.intent_service.collaboration_gate"

_USER = "3f7b8a52-1654-4b00-9e00-000000000070"  # valid UUID: survives principal parsing

_PM_TURN_1 = "remind me"
_PM_TURN_2 = "make coffee"

# The live classifier's response for _PM_TURN_1 with the taught example,
# captured verbatim 2026-09-08 (identical across 3/3 runs).
_LIVE_EMISSION = {
    "category": "execution",
    "action": "create_reminder",
    "confidence": 0.7,
    "reasoning": (
        "The query 'remind me' suggests an intent to set a reminder, which "
        "falls under execution actions."
    ),
    "helpful_knowledge_domains": ["task_management", "time_management"],
    "ambiguity_notes": ["missing: specific detail about what to remind"],
    "knowledge_used": [],
}


class _OneDrawLLM:
    """The LLM boundary: the pinned live emission for the FIRST
    classification draw; explosive afterwards — a second consultation means
    an answer turn escaped the offer seam (the orphan shape this issue is)."""

    def __init__(self):
        self.calls = 0

    async def complete(self, task_type=None, **kwargs):
        if task_type != "intent_classification":
            raise AssertionError(
                f"LLM boundary touched for task_type={task_type!r} — only the "
                "turn-1 classification draw may consult the LLM"
            )
        self.calls += 1
        if self.calls > 1:
            raise AssertionError(
                "LLM consulted a second time — an answer turn escaped the "
                "offer seam and re-entered the routing chain (the #1654 orphan)"
            )
        return json.dumps(_LIVE_EMISSION)

    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name}) beyond complete()")


def _svc():
    register_default_workflows()  # idempotent; the app does this at startup
    llm = _OneDrawLLM()
    return IntentService(intent_classifier=IntentClassifier(llm_service=llm)), llm


def _mock_todo_service(svc):
    mock = MagicMock()
    mock.create_todo = AsyncMock(return_value=SimpleNamespace(id=uuid4(), text="whatever"))
    mock.list_todos = AsyncMock(return_value=[])
    svc.todo_handlers.todo_service = mock
    return mock


def _pending_offers(service):
    return service.workflow_offer_service._pending_offers


async def _turn(svc, message, sid):
    with patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})):
        return await svc.process_intent(message=message, session_id=sid, user_id=_USER)


class TestBareRemindMeArmsTheCarrier:
    pytestmark = pytest.mark.asyncio

    async def test_turn_1_asks_the_armed_task_question_not_a_floor_merge(self):
        """The clarify question that answers bare 'remind me' is the CARRIER's
        question — armed, stored byte-for-byte (#1665), never a floor-composed
        merged ask with nothing listening."""
        svc, llm = _svc()
        _mock_todo_service(svc)
        r1 = await _turn(svc, _PM_TURN_1, "e2e-1654-bare-arm")
        assert llm.calls == 1  # the real path drew the LLM once
        assert "I didn't catch what you'd like to be reminded about" in r1.message
        stored = next(iter(_pending_offers(svc).values()))
        assert stored["pending_action"]["kind"] == REMINDER_TASK_QUESTION_KIND
        assert stored["question"] == r1.message  # the said ask IS the stored ask
        assert r1.intent_data.get("reminder_task_question_pending") is True
        assert r1.requires_clarification is True

    async def test_turn_2_make_coffee_binds_as_the_task_never_a_literal_request(self):
        """PM's exact answer. Pre-fix it was classified as a literal request
        to make coffee ('outside what I can do from here'). It must bind at
        the offer seam — the explosive second draw proves it never re-entered
        the routing chain — and chain into the #1648 time question."""
        svc, _ = _svc()
        mock = _mock_todo_service(svc)
        sid = "e2e-1654-bare-bind"
        await _turn(svc, _PM_TURN_1, sid)

        r2 = await _turn(svc, _PM_TURN_2, sid)
        mock.create_todo.assert_not_awaited()  # no time yet — nothing saved
        assert "**make coffee**" in r2.message
        assert _TIME_ASK in r2.message
        assert "outside what I can do" not in r2.message
        stored = next(iter(_pending_offers(svc).values()))
        assert stored["pending_action"]["kind"] == REMINDER_TIME_QUESTION_KIND
        assert stored["pending_action"]["task_text"] == "make coffee"
        assert r2.intent_data.get("reminder_task_bound") is True

    async def test_full_recovery_saves_the_reminder(self):
        """PM's whole intended exchange, recovered: remind me → what → make
        coffee → when → at 6am tomorrow → REAL save."""
        svc, _ = _svc()
        mock = _mock_todo_service(svc)
        sid = "e2e-1654-bare-save"
        await _turn(svc, _PM_TURN_1, sid)
        await _turn(svc, _PM_TURN_2, sid)

        r3 = await _turn(svc, "at 6am tomorrow", sid)
        mock.create_todo.assert_awaited_once()
        kwargs = mock.create_todo.await_args.kwargs
        assert kwargs["text"] == "make coffee"
        assert kwargs["reminder_date"] is not None
        assert (kwargs["reminder_date"].hour, kwargs["reminder_date"].minute) == (6, 0)
        assert "Reminder saved" in r3.message
        assert _pending_offers(svc) == {}


class TestPromptTeachesTheReminderLane:
    def test_prompt_carries_the_bare_remind_me_example(self):
        """The routing half of this fix is ONE taught example (corpus row
        deposited in the same commit, per the 8/29 policy). Silently dropping
        it would regress the live draw back to clarification_needed → floor —
        this pin makes that removal loud."""
        from services.intent_service.prompts import INTENT_CLASSIFICATION_PROMPT

        assert '"remind me"' in INTENT_CLASSIFICATION_PROMPT
        idx = INTENT_CLASSIFICATION_PROMPT.index('"remind me"')
        taught_line = INTENT_CLASSIFICATION_PROMPT[idx : idx + 200]
        assert '"create_reminder"' in taught_line
        assert '"execution"' in taught_line
