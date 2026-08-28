"""#1617 — the standup interview's completion tail must RELEASE (PM live
2026-08-13 3:29–3:30 PM).

PM's transcript, immediately after a successful interview ("Anything else?"):

- T1 ``do things directly from now on`` → handled by the mode surface — an
  off-tail turn ESCAPED, because collaboration_gate's deterministic
  declaration detector runs ABOVE the guided-process claim in process_intent.
- T2 ``change the status of issue #108 to Done`` → *"Great! Here's your final
  standup"* — the REFINING acceptance substring matched the word "Done" and
  the flow re-rendered its summary AT an issue command.
- T3 same command → *"Your standup is ready! Have a great day!"* — the
  FINALIZING tail claimed the turn while ignoring its content entirely.
  Only the THIRD try reached the issue rail.

The fix generalizes what let T1 out — a deterministic full-confidence
cross-domain detector examining the turn before the flow consumes it —
through the EXISTING #1529 escape seam (services/process/escape.py +
registry), never a second implementation:

1. After the final summary is confirmed, the flow COMPLETES directly —
   the FINALIZING tail turn (whose answer was never read) is gone.
2. In any completion-tail state, the off_intent tier additionally consults
   the #1411 Stage-0 explicit-issue-update detector (delegated, not copied);
   an off-tail turn RELEASES the flow (terminal COMPLETE — its work stands,
   no resume nag) and normal processing answers the turn.
3. PM's exact three turns are the regression, driven through the REAL
   ``process_intent`` with an explosive LLM (T2/T3 resolve at Stage 0).
"""

from unittest.mock import AsyncMock, patch

import pytest

from services.process.escape import (
    check_escape,
    format_release_prefix,
)
from services.process.registry import (
    ProcessCheckResult,
    ProcessRegistry,
    ProcessType,
)
from services.shared_types import StandupConversationState

# PM's verbatim transcript turns (2026-08-13 3:29–3:30 PM).
PM_T1_MODE_FLIP = "do things directly from now on"
PM_T2_ISSUE_COMMAND = "change the status of issue #108 to Done"
PM_T3_ISSUE_COMMAND = "change the status of issue #108 to Done"

_USER = "3f7b8a52-1617-4b00-9e00-000000001617"
_SESSION = "sess-1617"


# ---------------------------------------------------------------------------
# Unit: tail-aware escape detection
# ---------------------------------------------------------------------------


class TestTailEscapeDetection:
    def test_pm_issue_command_is_off_intent_in_the_tail(self):
        signal = check_escape(PM_T2_ISSUE_COMMAND, ProcessType.STANDUP, in_completion_tail=True)
        assert signal is not None
        assert signal.kind == "off_intent"
        assert "explicit_issue_update:#108" in signal.matched

    def test_pm_issue_command_stays_flow_material_mid_gathering(self):
        """Tail-only on purpose: mid-gathering, 'I need to change the status
        of issue #108 to Done' is a legitimate standup answer. The default
        (in_completion_tail=False) must not widen #1529's off-intent set."""
        assert check_escape(PM_T2_ISSUE_COMMAND, ProcessType.STANDUP) is None

    def test_existing_off_intent_shapes_unchanged_in_tail(self):
        signal = check_escape("restore CoVa", ProcessType.STANDUP, in_completion_tail=True)
        assert signal is not None
        assert signal.kind == "off_intent"

    def test_ordinary_tail_answers_still_reach_the_flow(self):
        """A genuine tail response is NOT claimed by the release path."""
        assert check_escape("looks good", ProcessType.STANDUP, in_completion_tail=True) is None


# ---------------------------------------------------------------------------
# Unit: the final confirmation completes the flow (no claiming tail turn)
# ---------------------------------------------------------------------------


def _fake_components():
    from services.standup.conversation_handler import StandupConversationHandler
    from tests.unit.services.standup._fake_conversation_manager import (
        FakeStandupConversationManager,
    )

    manager = FakeStandupConversationManager()
    handler = StandupConversationHandler(conversation_manager=manager)
    return manager, handler


async def _refining_conversation(manager, session_id=_SESSION, user_id=_USER):
    conv = await manager.create_conversation(session_id=session_id, user_id=user_id)
    conv.state = StandupConversationState.REFINING
    conv.current_standup = "*Yesterday:*\n* things"
    return conv


class TestFinalConfirmationReleases:
    pytestmark = pytest.mark.asyncio

    async def test_acceptance_completes_directly_no_finalizing_tail(self):
        """'Looks good' → COMPLETE in one turn. The old FINALIZING tail
        ('share this or save your preferences?') claimed a turn whose answer
        _handle_finalizing never read — it is gone."""
        manager, handler = _fake_components()
        conv = await _refining_conversation(manager)
        response = await handler.handle_turn(conv, "Looks good")
        assert response.state == StandupConversationState.COMPLETE
        assert "Here's your final standup" in response.message
        assert "save your preferences" not in response.message
        assert response.requires_input is False
        assert conv.state == StandupConversationState.COMPLETE

    async def test_completed_flow_is_not_active_for_the_registry(self):
        """COMPLETE is terminal: the adapter's check_active goes False, so
        the flow claims nothing further — the release half of AC 1."""
        from services.process.adapters import StandupProcessAdapter

        manager, handler = _fake_components()
        conv = await _refining_conversation(manager)
        await handler.handle_turn(conv, "Looks good")

        adapter = StandupProcessAdapter()
        adapter._manager, adapter._handler = manager, handler
        assert await adapter.check_active(_USER, _SESSION) is False

    async def test_legacy_finalizing_state_still_terminates(self):
        """An in-flight FINALIZING session (deployed pre-fix) still completes
        on its next turn — no orphaned state."""
        manager, handler = _fake_components()
        conv = await _refining_conversation(manager)
        conv.state = StandupConversationState.FINALIZING
        response = await handler.handle_turn(conv, "Just copy it")
        assert response.state == StandupConversationState.COMPLETE


# ---------------------------------------------------------------------------
# Unit: adapter tail-awareness + release
# ---------------------------------------------------------------------------


class TestStandupAdapterTailAndRelease:
    pytestmark = pytest.mark.asyncio

    async def _adapter(self):
        from services.process.adapters import StandupProcessAdapter

        manager, handler = _fake_components()
        adapter = StandupProcessAdapter()
        adapter._manager, adapter._handler = manager, handler
        return adapter, manager

    async def test_refining_and_finalizing_are_tail_states(self):
        adapter, manager = await self._adapter()
        conv = await _refining_conversation(manager)
        assert await adapter.in_completion_tail(_USER, _SESSION) is True
        conv.state = StandupConversationState.FINALIZING
        assert await adapter.in_completion_tail(_USER, _SESSION) is True

    async def test_gathering_states_are_not_tail(self):
        adapter, manager = await self._adapter()
        conv = await _refining_conversation(manager)
        conv.state = StandupConversationState.GATHERING_TODAY
        assert await adapter.in_completion_tail(_USER, _SESSION) is False

    async def test_release_lands_terminal_complete(self):
        """The delivered standup's honest terminal state is COMPLETE (the
        work happened), not ABANDONED — and terminal means no resume offer."""
        adapter, manager = await self._adapter()
        conv = await _refining_conversation(manager)
        await adapter.release(_USER, _SESSION)
        assert conv.state == StandupConversationState.COMPLETE
        assert await adapter.check_active(_USER, _SESSION) is False
        assert await adapter.has_suspended_session(_USER) is None


# ---------------------------------------------------------------------------
# Registry seam: off-intent in the tail releases; mid-flow still suspends
# ---------------------------------------------------------------------------


class FakeTailProcess:
    """Minimal GuidedProcess in a completion tail, recording lifecycle calls."""

    def __init__(self, in_tail=True, with_release=True):
        self._in_tail = in_tail
        self.handled_messages = []
        self.suspend_called = False
        self.close_called = False
        self.release_called = False
        if not with_release:
            self.release = None  # type: ignore[assignment]

    @property
    def process_type(self):
        return ProcessType.STANDUP

    async def check_active(self, user_id, session_id):
        return True

    async def in_completion_tail(self, user_id, session_id):
        return self._in_tail

    async def handle_message(self, user_id, session_id, message):
        self.handled_messages.append(message)
        return ProcessCheckResult.handled_by(
            process_type=ProcessType.STANDUP,
            response_message="captured as answer",
            intent_data={"category": "execution", "action": "turn", "confidence": 1.0},
        )

    async def suspend(self, user_id, session_id):
        self.suspend_called = True

    async def has_suspended_session(self, user_id):
        return None

    async def close(self, user_id, session_id):
        self.close_called = True

    async def release(self, user_id, session_id):
        self.release_called = True


class TestRegistrySeamTailRelease:
    pytestmark = pytest.mark.asyncio

    async def _run(self, fake, message=PM_T2_ISSUE_COMMAND):
        registry = ProcessRegistry()
        registry.register(fake)
        return await registry.check_active_processes(_USER, _SESSION, message)

    async def test_tail_off_intent_releases_and_falls_through(self):
        """AC 2: the off-tail turn is NOT consumed — the flow releases
        (terminal, via release(), never suspend) and normal processing
        answers, with the honest release prefix attached."""
        fake = FakeTailProcess()
        result = await self._run(fake)
        assert result.handled is False  # normal processing answers the command
        assert result.escaped is True
        assert result.response_message == format_release_prefix(ProcessType.STANDUP)
        assert fake.release_called is True
        assert fake.suspend_called is False
        assert fake.handled_messages == []  # never transcribed

    async def test_release_falls_back_to_close_when_absent(self):
        fake = FakeTailProcess(with_release=False)
        result = await self._run(fake)
        assert result.handled is False
        assert fake.close_called is True

    async def test_mid_flow_issue_command_still_reaches_the_flow(self):
        """Not in the tail → the #1529 posture is unchanged: the issue-shaped
        sentence stays flow material (a standup answer may name one)."""
        fake = FakeTailProcess(in_tail=False)
        result = await self._run(fake)
        assert result.handled is True
        assert fake.handled_messages == [PM_T2_ISSUE_COMMAND]
        assert fake.release_called is False

    async def test_handler_without_tail_protocol_keeps_old_behavior(self):
        """Duck-typing safety: a GuidedProcess that never heard of #1617
        behaves exactly as before (the registry treats an absent checker as
        mid-flow, and mid-flow doesn't claim the issue-shaped sentence)."""
        fake = FakeTailProcess()
        fake.in_completion_tail = None  # type: ignore[assignment]
        result = await self._run(fake)
        assert result.handled is True
        assert fake.handled_messages == [PM_T2_ISSUE_COMMAND]
        assert fake.release_called is False
        assert fake.suspend_called is False


# ---------------------------------------------------------------------------
# End-to-end: PM's exact three turns through the REAL process_intent
# ---------------------------------------------------------------------------


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM (forbidden:
    T2/T3 resolve at Stage 0; T1 at the declaration surface)."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — PM's three turns must resolve deterministically"
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
async def live_setup(mem_prefs):
    """Real IntentService + real ProcessRegistry + real StandupProcessAdapter
    wired to the in-memory conversation manager, conversation parked in the
    REFINING tail exactly as PM's session was at 'Anything else?'."""
    from services.intent.intent_service import IntentProcessingResult, IntentService
    from services.intent_service.classifier import IntentClassifier
    from services.intent_service.workflow_entries import register_default_workflows
    from services.process.adapters import StandupProcessAdapter

    register_default_workflows()
    manager, handler = _fake_components()
    conv = await _refining_conversation(manager)

    adapter = StandupProcessAdapter()
    adapter._manager, adapter._handler = manager, handler

    ProcessRegistry.reset_instance()
    ProcessRegistry.get_instance().register(adapter)

    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            clf = IntentClassifier(llm_service=_ExplosiveLLM())
            service = IntentService(intent_classifier=clf)

    recorder = AsyncMock(
        return_value=IntentProcessingResult(
            success=True, message="routed to update_issue", intent_data={}
        )
    )
    service._handle_update_issue = recorder

    yield service, conv, recorder

    ProcessRegistry.reset_instance()


class TestPmExactThreeTurns:
    pytestmark = pytest.mark.asyncio

    async def test_pm_transcript_replay(self, live_setup):
        service, conv, recorder = live_setup

        # T1 — the mode flip escapes the tail (as it did live) and the flow
        # is untouched: the declaration surface sits above the process claim.
        r1 = await service.process_intent(
            message=PM_T1_MODE_FLIP, session_id=_SESSION, user_id=_USER
        )
        assert r1.intent_data.get("action") == "set_working_mode"
        assert conv.state == StandupConversationState.REFINING
        recorder.assert_not_awaited()

        # T2 — the issue command RELEASES the flow and reaches the issue rail
        # on the FIRST try (live it took three). The release is honest in the
        # copy, and the flow is terminally complete.
        r2 = await service.process_intent(
            message=PM_T2_ISSUE_COMMAND, session_id=_SESSION, user_id=_USER
        )
        assert recorder.await_count == 1
        assert "Here's your final standup" not in r2.message  # the live swallow
        assert format_release_prefix(ProcessType.STANDUP) in r2.message
        assert "routed to update_issue" in r2.message
        assert conv.state == StandupConversationState.COMPLETE

        # T3 — the flow is gone; the command processes normally, unprefixed.
        r3 = await service.process_intent(
            message=PM_T3_ISSUE_COMMAND, session_id=_SESSION, user_id=_USER
        )
        assert recorder.await_count == 2
        assert "Your standup is ready" not in r3.message  # the live swallow
        assert format_release_prefix(ProcessType.STANDUP) not in r3.message
