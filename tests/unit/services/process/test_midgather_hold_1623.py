"""#1623 — an ACTIVE gathering flow must HOLD its turns (PM live 2026-08-15).

PM's baseline transcript (v52), the flow-claiming family's THIRD face
(#1529 fixed hijack-INTO; #1617 releases COMPLETED tails; this is
mid-gathering theft):

- Interview: "What are you planning to work on?" → PM's plans answer →
  **"I can't do that from chat yet"** — the files-family canned denial
  claimed an interview ANSWER.
- Interview: "Blockers?" → PM: "just my own availability" →
  **"Today is Saturday, August 15…"** — the temporal surface ate the
  blocker answer.

MEASURED DIAGNOSIS (the suspect pool exonerated, the real thief found):

Every content-dependent surface at or above the guided-process claim was
measured against PM's verbatim turns and passes them through untouched —
`collaboration_gate.detect_mode_declaration` (the #1510 surface that runs
deliberately ABOVE the claim), the #846 pending-offer pop, the #852
contextual-offer continuation, the #1529 escape tiers
(exit/refusal/off_intent), and the #899 off-topic detector. With a fresh
clock, the real `process_intent` + live registry + adapter HOLDS both turns
(captured, no LLM touched).

The thief was `StandupProcessAdapter.check_active`'s LAZY 15-minute timeout
(#888): with no background reaper, it fires inside the processing of the
user's next turn — which mid-gathering is by construction the ANSWER to the
open question. >15 min of think-time between question and answer silently
auto-suspended the flow mid-turn and dropped the answer through to the LLM
classifier, where the files-family denial (turn 1) and the temporal surface
(turn 2) claimed it. Reproduced end-to-end: a 16-minute-stale clock stole
both turns; a fresh clock stole neither.

THE FIX: the timeout auto-suspend is gated to the completion tail
(REFINING/FINALIZING). Mid-gathering, the flow holds its turns regardless
of think-time; the deliberate exits remain the #888/#1529 escape tiers,
#899 off-topic, and the #1510 mode-declaration surface (which escapes the
turn WITHOUT touching the flow — the open question stays open).
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest

from services.process.escape import check_escape
from services.process.off_topic import detect_off_topic
from services.process.registry import ProcessRegistry, ProcessType
from services.shared_types import StandupConversationState

# PM's verbatim stolen turns (baseline transcript 2026-08-15, v52).
PM_PLANS_ANSWER = (
    "continue testing with Lead Developer. If time allows, discuss FTUX "
    "with CXO and BYOC MCP plugin architecture with PA"
)
PM_BLOCKERS_ANSWER = "just my own availability"

_USER = "3f7b8a52-1623-4b00-9e00-000000001623"
_SESSION = "sess-1623"

STALE = timedelta(minutes=16)  # past the #888 15-minute timeout


def _fake_components():
    from services.standup.conversation_handler import StandupConversationHandler
    from tests.unit.services.standup._fake_conversation_manager import (
        FakeStandupConversationManager,
    )

    manager = FakeStandupConversationManager()
    handler = StandupConversationHandler(conversation_manager=manager)
    return manager, handler


async def _conversation(manager, state, stale=True, session_id=_SESSION, user_id=_USER):
    conv = await manager.create_conversation(session_id=session_id, user_id=user_id)
    conv.state = state
    if stale:
        conv.updated_at = datetime.now(timezone.utc) - STALE
    return conv


# ---------------------------------------------------------------------------
# Unit: the suspect pool is exonerated on PM's verbatim turns
# ---------------------------------------------------------------------------


class TestSuspectPoolExoneration:
    """The measured diagnosis, pinned: no content-dependent surface at or
    above the claim fires on PM's answers — they are flow material."""

    @pytest.mark.parametrize("turn", [PM_PLANS_ANSWER, PM_BLOCKERS_ANSWER])
    def test_escape_tiers_pass_the_answers(self, turn):
        assert check_escape(turn, ProcessType.STANDUP, in_completion_tail=False) is None

    @pytest.mark.parametrize("turn", [PM_PLANS_ANSWER, PM_BLOCKERS_ANSWER])
    def test_off_topic_passes_the_answers(self, turn):
        assert detect_off_topic(turn, ProcessType.STANDUP).is_off_topic is False

    @pytest.mark.parametrize("turn", [PM_PLANS_ANSWER, PM_BLOCKERS_ANSWER])
    def test_mode_declaration_passes_the_answers(self, turn):
        from services.intent_service.collaboration_gate import detect_mode_declaration

        assert detect_mode_declaration(turn) is None


# ---------------------------------------------------------------------------
# Unit: adapter — mid-gathering holds through the clock; the tail still times out
# ---------------------------------------------------------------------------


class TestAdapterTimeoutGating:
    pytestmark = pytest.mark.asyncio

    async def _adapter(self):
        from services.process.adapters import StandupProcessAdapter

        manager, handler = _fake_components()
        adapter = StandupProcessAdapter()
        adapter._manager, adapter._handler = manager, handler
        return adapter, manager

    @pytest.mark.parametrize(
        "state",
        [
            StandupConversationState.GATHERING_YESTERDAY,
            StandupConversationState.GATHERING_TODAY,
            StandupConversationState.GATHERING_BLOCKERS,
        ],
    )
    async def test_stale_mid_gathering_stays_active(self, state):
        """The lazy timeout no longer ejects a mid-gathering flow: the open
        question binds its answer no matter how long the user thought."""
        adapter, manager = await self._adapter()
        conv = await _conversation(manager, state, stale=True)
        assert await adapter.check_active(_USER, _SESSION) is True
        assert conv.state == state  # not silently suspended

    @pytest.mark.parametrize(
        "state",
        [
            StandupConversationState.REFINING,
            StandupConversationState.FINALIZING,
        ],
    )
    async def test_stale_tail_still_times_out(self, state):
        """#888's timeout survives where it belongs: a DELIVERED flow going
        idle stops claiming the session."""
        adapter, manager = await self._adapter()
        conv = await _conversation(manager, state, stale=True)
        assert await adapter.check_active(_USER, _SESSION) is False
        assert conv.state == StandupConversationState.SUSPENDED

    async def test_fresh_tail_is_still_active(self):
        adapter, manager = await self._adapter()
        await _conversation(manager, StandupConversationState.REFINING, stale=False)
        assert await adapter.check_active(_USER, _SESSION) is True


# ---------------------------------------------------------------------------
# End-to-end: PM's exact stolen turns through the REAL process_intent
# ---------------------------------------------------------------------------


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM (forbidden:
    a held mid-gathering answer must never reach classification — that fall-
    through is exactly how the files denial and the temporal surface stole
    PM's answers live)."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — the gathering flow must hold this turn"
        )


@pytest.fixture
def mem_prefs(monkeypatch):
    store: dict = {_USER: {}}

    async def _load(user_id):
        return dict(store.get(str(user_id), {}))

    async def _save(user_id, key, value):
        if str(user_id) not in store:
            return False
        store[str(user_id)][key] = value
        return True

    from services.intent_service import collaboration_gate

    monkeypatch.setattr(collaboration_gate, "_load_preferences", _load)
    monkeypatch.setattr(collaboration_gate, "_save_preference", _save)
    return store


@pytest.fixture
async def live_service(mem_prefs):
    """Real IntentService + real ProcessRegistry + real StandupProcessAdapter
    over the in-memory manager. Conversation state is set per-test."""
    from services.intent.intent_service import IntentService
    from services.intent_service.classifier import IntentClassifier
    from services.intent_service.workflow_entries import register_default_workflows
    from services.process.adapters import StandupProcessAdapter

    register_default_workflows()
    manager, handler = _fake_components()

    adapter = StandupProcessAdapter()
    adapter._manager, adapter._handler = manager, handler

    ProcessRegistry.reset_instance()
    ProcessRegistry.get_instance().register(adapter)

    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            clf = IntentClassifier(llm_service=_ExplosiveLLM())
            service = IntentService(intent_classifier=clf)

    yield service, manager

    ProcessRegistry.reset_instance()


class TestPmStolenTurnsNowHeld:
    """The house pattern: PM's verbatim turns as e2e regression, with the
    STALE clock that reproduced the live theft pre-fix."""

    pytestmark = pytest.mark.asyncio

    async def test_pm_plans_answer_reaches_the_open_question(self, live_service):
        service, manager = live_service
        conv = await _conversation(manager, StandupConversationState.GATHERING_TODAY, stale=True)

        result = await service.process_intent(
            message=PM_PLANS_ANSWER, session_id=_SESSION, user_id=_USER
        )

        # The answer was captured against the open question…
        captured = [item.display for item in conv.partial_capture.today]
        assert PM_PLANS_ANSWER in captured
        # …the interview advanced to blockers…
        assert conv.state == StandupConversationState.GATHERING_BLOCKERS
        assert "blockers" in result.message.lower()
        # …and no canned denial stole the turn (the live theft copy).
        assert "can't do that from chat" not in result.message

    async def test_pm_blockers_answer_reaches_the_open_question(self, live_service):
        service, manager = live_service
        conv = await _conversation(manager, StandupConversationState.GATHERING_BLOCKERS, stale=True)

        result = await service.process_intent(
            message=PM_BLOCKERS_ANSWER, session_id=_SESSION, user_id=_USER
        )

        captured = [item.display for item in conv.partial_capture.blockers]
        assert PM_BLOCKERS_ANSWER in captured
        # Blockers is the final gathering part — the standup renders.
        assert conv.state in (
            StandupConversationState.REFINING,
            StandupConversationState.COMPLETE,
        )
        assert "just my own availability" in result.message
        # Not the temporal surface's live steal.
        assert "great day for deep work" not in result.message.lower()

    async def test_full_interview_with_slow_answers(self, live_service):
        """The whole 3-part interview with EVERY answer past the old timeout:
        nothing is stolen at any step."""
        service, manager = live_service
        conv = await _conversation(
            manager, StandupConversationState.GATHERING_YESTERDAY, stale=True
        )

        r1 = await service.process_intent(
            message="shipped the v53 cut", session_id=_SESSION, user_id=_USER
        )
        assert conv.state == StandupConversationState.GATHERING_TODAY

        conv.updated_at = datetime.now(timezone.utc) - STALE
        r2 = await service.process_intent(
            message=PM_PLANS_ANSWER, session_id=_SESSION, user_id=_USER
        )
        assert conv.state == StandupConversationState.GATHERING_BLOCKERS

        conv.updated_at = datetime.now(timezone.utc) - STALE
        r3 = await service.process_intent(
            message=PM_BLOCKERS_ANSWER, session_id=_SESSION, user_id=_USER
        )
        assert [i.display for i in conv.partial_capture.yesterday] == ["shipped the v53 cut"]
        assert PM_PLANS_ANSWER in [i.display for i in conv.partial_capture.today]
        assert PM_BLOCKERS_ANSWER in [i.display for i in conv.partial_capture.blockers]


class TestDeliberateEscapesSurviveTheHold:
    """The hard part named by the issue: holding mid-gathering turns must NOT
    break the deliberate exits — even with a stale clock."""

    pytestmark = pytest.mark.asyncio

    async def test_universal_escape_still_exits(self, live_service):
        service, manager = live_service
        conv = await _conversation(manager, StandupConversationState.GATHERING_TODAY, stale=True)
        result = await service.process_intent(message="cancel", session_id=_SESSION, user_id=_USER)
        assert conv.state == StandupConversationState.SUSPENDED
        assert "paused" in result.message.lower()

    async def test_1529_flow_exit_still_ends_the_flow(self, live_service):
        service, manager = live_service
        conv = await _conversation(manager, StandupConversationState.GATHERING_TODAY, stale=True)
        result = await service.process_intent(
            message="end standup", session_id=_SESSION, user_id=_USER
        )
        assert conv.state == StandupConversationState.ABANDONED
        assert "ended the standup" in result.message.lower()

    async def test_1529_off_intent_still_pauses_mid_gathering(self, live_service):
        """'remind me to …' is a cross-domain ACTION per the #1529 seam rules
        — it still escapes the hold (pause + normal processing answers). The
        assertion stops at the pause: what answers the residual is the
        below-claim stack's business, not this seam's."""
        service, manager = live_service
        conv = await _conversation(manager, StandupConversationState.GATHERING_TODAY, stale=True)
        try:
            await service.process_intent(
                message="remind me to review the cut tomorrow",
                session_id=_SESSION,
                user_id=_USER,
            )
        except Exception:
            pass  # downstream surfaces may need more than this harness wires
        assert conv.state == StandupConversationState.SUSPENDED

    async def test_899_off_topic_still_pauses_mid_gathering(self, live_service):
        service, manager = live_service
        conv = await _conversation(manager, StandupConversationState.GATHERING_TODAY, stale=True)
        # NOTE: "what's the weather today?" would NOT pause — the word
        # "today" matches a standup on-topic pattern (pre-existing #899
        # conservatism, unchanged here). "what time is it" is a clean
        # generic non-sequitur.
        try:
            await service.process_intent(
                message="what time is it", session_id=_SESSION, user_id=_USER
            )
        except Exception:
            pass  # the residual answer may consult surfaces this harness doesn't wire
        assert conv.state == StandupConversationState.SUSPENDED

    async def test_1510_mode_declaration_still_escapes_flow_untouched(self, live_service):
        """The #1510 surface stays deliberately ABOVE the claim (the #1617
        rationale: a durative meta-instruction about HOW Piper works is
        vanishingly unlikely as interview material, and its detector demands
        the durative marker). Crucially it never touches the flow — the open
        question stays open for the next turn."""
        service, manager = live_service
        conv = await _conversation(manager, StandupConversationState.GATHERING_TODAY, stale=True)
        result = await service.process_intent(
            message="do things directly from now on", session_id=_SESSION, user_id=_USER
        )
        assert result.intent_data.get("action") == "set_working_mode"
        assert conv.state == StandupConversationState.GATHERING_TODAY

        # And the very next turn still answers the held question.
        result2 = await service.process_intent(
            message=PM_PLANS_ANSWER, session_id=_SESSION, user_id=_USER
        )
        assert PM_PLANS_ANSWER in [i.display for i in conv.partial_capture.today]
