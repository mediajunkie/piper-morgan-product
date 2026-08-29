"""
Issue #1529: universal guided-process escape (FLOW-ESCAPE) — failing-first
tests from PM's 2026-08-08 T6 transcript.

The live failure: a standup interview claimed PM's session. Five explicit
commands — including the verbatim "i am not doing the standup right now.
restore CoVa" — were transcribed INTO the standup as answers, and "end
standup" was misrouted to a todo-complete response. The #888 escape hatch
recognized six exact words only; #899's off-topic layer declared anything
containing the word "standup" ON-topic, so refusals naming the flow were
the most reliably swallowed messages of all.

Contract under test (services/process/escape.py + registry wiring):
- exit phrases ("end standup", "stop the standup", "not now") are consumed
  at the seam, deterministically, BEFORE the flow handler or any classifier
  sees them; the flow is CLOSED (terminal — no resume nag).
- refusal shapes ("i am not doing the standup right now") close the flow;
  residual content ("restore CoVa") falls through to normal intent
  processing with an honest exit prefix.
- clear cross-domain actions ("restore CoVa" alone) pause the flow and fall
  through (Option A UX, #899).
- genuine flow answers are untouched.
"""

import pytest

from services.process.escape import (
    check_escape,
    detect_flow_exit,
    format_exit_message,
    format_refusal_prefix,
)
from services.process.registry import (
    GuidedProcess,
    ProcessCheckResult,
    ProcessRegistry,
    ProcessType,
)

# PM's verbatim transcript lines (2026-08-08 T6)
PM_REFUSAL_WITH_COMMAND = "i am not doing the standup right now. restore CoVa"
PM_END_STANDUP = "end standup"


# ---------------------------------------------------------------------------
# Unit: detection
# ---------------------------------------------------------------------------


class TestFlowExitDetection:
    """Full-message exit commands aimed at the flow."""

    @pytest.mark.parametrize(
        "message",
        [
            PM_END_STANDUP,
            "End standup",
            "end the standup",
            "End the standup now.",
            "stop the standup",
            "cancel standup",
            "quit the standup please",
            "exit standup",
            "end this",
            "stop this process",
            "not now",
            "nevermind",
            "forget it",
        ],
    )
    def test_exit_phrases_detected(self, message):
        assert detect_flow_exit(message, ProcessType.STANDUP) is True

    @pytest.mark.parametrize(
        "message",
        [
            "worked on the standup feature yesterday",  # names standup as WORK, not command
            "yesterday I finished the parser",
            "no blockers",
            "yes",
            "",
        ],
    )
    def test_non_exit_messages_not_detected(self, message):
        assert detect_flow_exit(message, ProcessType.STANDUP) is False

    def test_exit_is_classified_as_exit_kind(self):
        signal = check_escape(PM_END_STANDUP, ProcessType.STANDUP)
        assert signal is not None
        assert signal.kind == "exit"


class TestRefusalDetection:
    """Refusal clauses naming the flow — with and without residual content."""

    def test_pm_verbatim_refusal_with_command(self):
        """The transcript line: refusal + the user's actual request."""
        signal = check_escape(PM_REFUSAL_WITH_COMMAND, ProcessType.STANDUP)
        assert signal is not None
        assert signal.kind == "refusal"
        assert signal.residual == "restore CoVa"

    def test_refusal_without_residual(self):
        signal = check_escape("i am not doing the standup right now", ProcessType.STANDUP)
        assert signal is not None
        assert signal.kind == "refusal"
        assert signal.residual is None

    @pytest.mark.parametrize(
        "message",
        [
            "I don't want to do the standup",
            "let's not do the standup today",
            "no standup",
            "I'm not doing this right now",  # generic pronoun, full message
        ],
    )
    def test_refusal_variants(self, message):
        signal = check_escape(message, ProcessType.STANDUP)
        assert signal is not None, f"{message!r} should be a refusal"
        assert signal.kind == "refusal"

    def test_exit_clause_in_longer_message_is_refusal_with_residual(self):
        signal = check_escape("stop the standup and restore CoVa", ProcessType.STANDUP)
        assert signal is not None
        assert signal.kind == "refusal"
        assert signal.residual == "restore CoVa"

    @pytest.mark.parametrize(
        "message",
        [
            # Generic-pronoun refusal shapes must NOT fire clause-level:
            # a real standup answer about some other piece of work.
            "I'm not going to do that refactor today",
            "I'm not doing the migration today, blocked on reviews",
            # Ordinary answers
            "worked on the 1529 fix yesterday, mostly tests",
            "finished the parser and started on the docs",
        ],
    )
    def test_genuine_answers_are_not_refusals(self, message):
        signal = check_escape(message, ProcessType.STANDUP)
        assert signal is None, f"{message!r} must reach the flow handler, got {signal}"


class TestOffIntentDetection:
    """Clear cross-domain actions the flow can't use."""

    @pytest.mark.parametrize(
        "message",
        [
            "restore CoVa",
            "restore the CoVa project",
            "unarchive CoVa",
            "remind me to check the deploy",
            "create an issue for the login bug",
        ],
    )
    def test_cross_actions_detected(self, message):
        signal = check_escape(message, ProcessType.STANDUP)
        assert signal is not None, f"{message!r} should be off-intent"
        assert signal.kind == "off_intent"

    def test_skip_left_to_888_escape_commands(self):
        """'skip' is #888 registry territory (and a legit per-part standup
        skip); the escape module must not claim it."""
        assert check_escape("skip", ProcessType.STANDUP) is None


# ---------------------------------------------------------------------------
# Integration: the registry seam
# ---------------------------------------------------------------------------


class FakeGuidedProcess:
    """Minimal GuidedProcess implementation that records what reached it."""

    def __init__(self, process_type=ProcessType.STANDUP, active=True, with_close=True):
        self._type = process_type
        self._active = active
        self.handled_messages = []
        self.suspend_called = False
        self.close_called = False
        if not with_close:
            # Remove close from THIS instance's lookup path
            self.close = None  # type: ignore[assignment]

    @property
    def process_type(self):
        return self._type

    async def check_active(self, user_id, session_id):
        return self._active

    async def handle_message(self, user_id, session_id, message):
        self.handled_messages.append(message)
        return ProcessCheckResult.handled_by(
            process_type=self._type,
            response_message="captured as answer",
            intent_data={"category": "execution", "action": "turn", "confidence": 1.0},
        )

    async def suspend(self, user_id, session_id):
        self.suspend_called = True

    async def has_suspended_session(self, user_id):
        return None

    async def close(self, user_id, session_id):
        self.close_called = True


@pytest.fixture
def registry_with_active_standup():
    registry = ProcessRegistry()
    fake = FakeGuidedProcess()
    registry.register(fake)
    return registry, fake


class TestRegistrySeamEscape:
    """The seam contract: escapes consumed before the flow handler."""

    @pytest.mark.asyncio
    async def test_end_standup_never_reaches_flow_handler(self, registry_with_active_standup):
        """PM verbatim: 'end standup' mid-flow → deterministic exit; the flow
        never transcribes it, no classifier ever sees it."""
        registry, fake = registry_with_active_standup

        result = await registry.check_active_processes("user-1", "sess-1", PM_END_STANDUP)

        assert result.handled is True
        assert result.escaped is True
        assert fake.handled_messages == []  # never transcribed
        assert fake.close_called is True  # closed, not suspended (no resume nag)
        assert result.response_message == format_exit_message(ProcessType.STANDUP)

    @pytest.mark.asyncio
    async def test_pm_refusal_exits_and_falls_through_to_answer(self, registry_with_active_standup):
        """PM verbatim: refusal + 'restore CoVa' → flow closed, turn falls
        through (handled=False) so intent processing answers the request,
        with the honest exit prefix attached."""
        registry, fake = registry_with_active_standup

        result = await registry.check_active_processes("user-1", "sess-1", PM_REFUSAL_WITH_COMMAND)

        assert result.handled is False  # normal processing answers "restore CoVa"
        assert result.escaped is True
        assert result.response_message == format_refusal_prefix(ProcessType.STANDUP)
        assert fake.close_called is True
        assert fake.handled_messages == []  # NOT composed into the standup

    @pytest.mark.asyncio
    async def test_refusal_without_residual_claims_turn(self, registry_with_active_standup):
        registry, fake = registry_with_active_standup

        result = await registry.check_active_processes(
            "user-1", "sess-1", "i am not doing the standup right now"
        )

        assert result.handled is True
        assert result.escaped is True
        assert fake.close_called is True
        assert fake.handled_messages == []

    @pytest.mark.asyncio
    async def test_off_intent_pauses_and_falls_through(self, registry_with_active_standup):
        """'restore CoVa' alone mid-flow → pause (resumable) + answer."""
        registry, fake = registry_with_active_standup

        result = await registry.check_active_processes("user-1", "sess-1", "restore CoVa")

        assert result.handled is False
        assert result.escaped is True
        assert fake.suspend_called is True  # paused, not closed — resumable
        assert fake.close_called is False
        assert fake.handled_messages == []

    @pytest.mark.asyncio
    async def test_genuine_answer_still_reaches_flow(self, registry_with_active_standup):
        registry, fake = registry_with_active_standup

        message = "worked on the 1529 fix yesterday, mostly tests"
        result = await registry.check_active_processes("user-1", "sess-1", message)

        assert result.handled is True
        assert result.escaped is False
        assert fake.handled_messages == [message]

    @pytest.mark.asyncio
    async def test_888_exact_escape_commands_still_suspend(self, registry_with_active_standup):
        """Regression: the pre-existing #888 hatch is unchanged — exact
        'cancel' suspends (resumable), does not close."""
        registry, fake = registry_with_active_standup

        result = await registry.check_active_processes("user-1", "sess-1", "cancel")

        assert result.handled is True
        assert result.escaped is True
        assert fake.suspend_called is True
        assert fake.close_called is False

    @pytest.mark.asyncio
    async def test_close_falls_back_to_suspend_when_handler_lacks_close(self):
        """Handlers without close() (e.g. slot-filling) still get cleanly
        stopped via suspend()."""
        registry = ProcessRegistry()
        fake = FakeGuidedProcess(with_close=False)
        registry.register(fake)

        result = await registry.check_active_processes("user-1", "sess-1", "end standup")

        assert result.handled is True
        assert result.escaped is True
        assert fake.suspend_called is True


class TestStandupAdapterClose:
    """StandupProcessAdapter.close() → ABANDONED (terminal, no resume offer)."""

    @pytest.mark.asyncio
    async def test_close_transitions_to_abandoned(self):
        from unittest.mock import patch

        from services.process.adapters import StandupProcessAdapter
        from services.shared_types import StandupConversationState
        from tests.unit.services.standup._fake_conversation_manager import (
            FakeStandupConversationManager,
        )

        manager = FakeStandupConversationManager()
        conv = await manager.create_conversation("sess-1", "user-1")
        await manager.transition_state(conv.id, StandupConversationState.GATHERING_YESTERDAY)

        adapter = StandupProcessAdapter()
        with patch.object(adapter, "_get_components", return_value=(manager, None)):
            await adapter.close("user-1", "sess-1")

        closed = await manager.get_conversation(conv.id)
        assert closed.state == StandupConversationState.ABANDONED

    def test_fake_satisfies_protocol(self):
        assert isinstance(FakeGuidedProcess(), GuidedProcess)
