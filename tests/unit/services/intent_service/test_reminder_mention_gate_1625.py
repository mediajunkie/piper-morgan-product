"""Issue #1625: reminder surfacing is relentless — mention ONCE per session.

PM live 8/15 (v53 retest): "Reminders are a bit relentless! maybe they should
be locked to the top of radar but not mentioned in every reply." The #1566
surfacing rider (due reminders ride EVERY floor-bound turn) over-rotated: the
transcript shows the block on four consecutive replies inside one standup
interview, including mid-question.

PM's ruling (binding): Radar pins due reminders at top (the persistent
surface owns persistence — see the radar tests); conversation mentions them
ONCE per session, or again on material change (a genuinely NEW reminder
coming due), then stays quiet. Guard: "once" must NOT become "never" — the
gate keys on reminder IDENTITY, not a boolean.

The gate lives in context_assembler (post-#984-cache, since the cache is
per-user and the mention-set is per-session) with the same lifetime class as
the rail's session memory (verified_inference._SESSION_DECLINES): transient
per-process state, never a persisted preference.
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.intent_service import context_assembler as ca
from services.intent_service.context_assembler import ContextAssembler
from services.process.registry import (
    ProcessCheckResult,
    ProcessRegistry,
    ProcessType,
    get_process_registry,
)

_CATEGORY_GATHERERS = [
    "_gather_identity_context",
    "_gather_trust_context",
    "_gather_insight_pull_context",
    "_gather_memory_context",
    "_gather_temporal_context",
    "_gather_status_priority_context",
]


@pytest.fixture(autouse=True)
def _clean_session_state():
    """Fresh mention-set + process registry per test (both module/class level)."""
    ca._SESSION_REMINDER_MENTIONS.clear()
    ProcessRegistry.reset_instance()
    yield
    ca._SESSION_REMINDER_MENTIONS.clear()
    ProcessRegistry.reset_instance()


def _quiet_gatherers():
    """Patch the category gatherers to empty so tests isolate the reminder
    rail (the real gatherers reach for DB/GitHub). Same shape as the #1566
    suite."""
    patchers = [
        patch.object(ContextAssembler, name, AsyncMock(return_value={}))
        for name in _CATEGORY_GATHERERS
    ]
    patchers.append(
        patch(
            "services.intent_service.context_assembler._current_time_for_user",
            AsyncMock(return_value=None),
        )
    )
    return patchers


def _mock_due(reminders):
    """Patch TodoIntentHandlers so get_due_reminders returns `reminders`."""
    mock_instance = MagicMock()
    mock_instance.get_due_reminders = AsyncMock(return_value=reminders)
    return patch(
        "services.intent_service.todo_handlers.TodoIntentHandlers",
        return_value=mock_instance,
    )


async def _gather(reminders, session_id=None, category="STATUS", user_id=None):
    """One gather_context pass with `reminders` due.

    Fresh user_id per call by default: the #984 reminder cache keys on
    user_id, so a fresh user guarantees the mocked due-list is what the
    rider sees — while the #1625 mention gate keys on session_id, which the
    caller controls. (This is the deliberate seam the gate sits on: cache
    per-user, mention-set per-session.)
    """
    patchers = _quiet_gatherers()
    for p in patchers:
        p.start()
    try:
        with _mock_due(reminders):
            assembler = ContextAssembler()
            return await assembler.gather_context(
                category, user_id=user_id or str(uuid4()), session_id=session_id
            )
    finally:
        for p in patchers:
            p.stop()


class _StubFlow:
    """Minimal GuidedProcess (protocol shape from test_registry.MockGuidedProcess)
    whose activity the test toggles — stands in for the standup interview."""

    def __init__(self, process_type=ProcessType.STANDUP, active=True):
        self._process_type = process_type
        self.active = active

    @property
    def process_type(self):
        return self._process_type

    async def check_active(self, user_id, session_id):
        return self.active

    async def handle_message(self, user_id, session_id, message):
        return ProcessCheckResult.not_handled()

    async def suspend(self, user_id, session_id):
        return None

    async def has_suspended_session(self, user_id):
        return None


# ---------------------------------------------------------------------------
# Once per session, then quiet
# ---------------------------------------------------------------------------


class TestMentionOncePerSession1625:
    @pytest.mark.asyncio
    async def test_first_turn_mentions_then_quiet(self):
        """PM's transcript shape: the same due reminders rode four consecutive
        replies. First turn mentions; every later turn in the session is quiet."""
        session = f"sess-{uuid4()}"
        first = await _gather(["check in with the Lead Developer"], session_id=session)
        assert first.get("due_reminders") == ["check in with the Lead Developer"]
        assert first["reminder_count"] == 1

        for _ in range(3):  # the three follow-up replies PM saw re-nag
            later = await _gather(["check in with the Lead Developer"], session_id=session)
            assert "due_reminders" not in later, (
                "due reminders re-surfaced in the same session — the #1625 "
                "once-per-conversation ruling"
            )
            assert "reminder_count" not in later

    @pytest.mark.asyncio
    async def test_new_reminder_coming_due_is_mentioned_once_more(self):
        """Guard from the issue: 'once' must not become 'never'. A genuinely
        NEW reminder coming due mid-session IS mentioned — and only the new one."""
        session = f"sess-{uuid4()}"
        await _gather(["submit the report"], session_id=session)

        second = await _gather(["submit the report", "call the vendor"], session_id=session)
        assert second.get("due_reminders") == ["call the vendor"], (
            "a NEW reminder coming due mid-session must be mentioned "
            "(identity-keyed set, not a boolean)"
        )
        assert second["reminder_count"] == 1

        third = await _gather(["submit the report", "call the vendor"], session_id=session)
        assert "due_reminders" not in third

    @pytest.mark.asyncio
    async def test_sessions_are_independent(self):
        """The mention-set is per-session: a different conversation still
        gets its one mention."""
        await _gather(["submit the report"], session_id="sess-a-1625")
        other = await _gather(["submit the report"], session_id="sess-b-1625")
        assert other.get("due_reminders") == ["submit the report"]

    @pytest.mark.asyncio
    async def test_no_session_id_preserves_1566_surfacing(self):
        """No session → no per-session gating possible; the #1566 behavior
        (surface on every floor-bound turn) is preserved unchanged."""
        for _ in range(2):
            context = await _gather(["submit the report"], session_id=None)
            assert context.get("due_reminders") == ["submit the report"]

    @pytest.mark.asyncio
    async def test_source_failed_honesty_unaffected(self):
        """#1425: the gate only touches the due-reminder keys; a failed
        lookup still flags source_failed on every turn."""
        session = f"sess-{uuid4()}"
        for _ in range(2):
            context = await _gather(None, session_id=session)
            assert context.get("source_failed") is True

    @pytest.mark.asyncio
    async def test_gate_does_not_mutate_cached_slice(self):
        """The gated dict must be a new dict — the input may be the #984
        cache's shared per-user reference."""
        assembler = ContextAssembler()
        cached = {"due_reminders": ["a", "b"], "reminder_count": 2}
        session = f"sess-{uuid4()}"
        ca._SESSION_REMINDER_MENTIONS[session] = {"a"}
        gated = await assembler._gate_due_reminder_mentions(cached, str(uuid4()), session)
        assert gated["due_reminders"] == ["b"]
        assert cached == {"due_reminders": ["a", "b"], "reminder_count": 2}


# ---------------------------------------------------------------------------
# Never inside an active gathering/interview exchange
# ---------------------------------------------------------------------------


class TestNoReminderBlockMidInterview1625:
    @pytest.mark.asyncio
    async def test_no_block_while_standup_interview_active(self):
        """PM's v53 transcript: the block appeared MID-QUESTION inside a
        standup interview. An active guided flow suppresses the block."""
        flow = _StubFlow(active=True)
        get_process_registry().register(flow)
        session = f"sess-{uuid4()}"
        context = await _gather(["check in with the Lead Developer"], session_id=session)
        assert "due_reminders" not in context, (
            "due-reminder block rendered inside an active standup interview "
            "(#1625 regression: PM saw it mid-question)"
        )
        assert "reminder_count" not in context

    @pytest.mark.asyncio
    async def test_suppressed_turn_does_not_count_as_mentioned(self):
        """Suppression is not a mention: the user was never told, so the
        first turn AFTER the interview ends still mentions the reminders."""
        flow = _StubFlow(active=True)
        get_process_registry().register(flow)
        session = f"sess-{uuid4()}"
        await _gather(["check in with the Lead Developer"], session_id=session)

        flow.active = False  # interview over
        after = await _gather(["check in with the Lead Developer"], session_id=session)
        assert after.get("due_reminders") == ["check in with the Lead Developer"], (
            "reminders suppressed during the interview were marked mentioned — "
            "'once' became 'never'"
        )

    @pytest.mark.asyncio
    async def test_probe_failure_fails_open_to_surfacing(self):
        """The mention gate is a quieting layer — a broken registry probe
        must not break the #1566 surfacing promise."""
        session = f"sess-{uuid4()}"
        with patch.object(
            ProcessRegistry, "any_active", AsyncMock(side_effect=RuntimeError("boom"))
        ):
            context = await _gather(["submit the report"], session_id=session)
        assert context.get("due_reminders") == ["submit the report"]


# ---------------------------------------------------------------------------
# Registry probe
# ---------------------------------------------------------------------------


class TestRegistryAnyActive1625:
    @pytest.mark.asyncio
    async def test_any_active_true_when_a_flow_is_active(self):
        get_process_registry().register(_StubFlow(active=True))
        assert await get_process_registry().any_active("u1", "s1") is True

    @pytest.mark.asyncio
    async def test_any_active_false_when_no_flow_active(self):
        get_process_registry().register(_StubFlow(active=False))
        assert await get_process_registry().any_active("u1", "s1") is False

    @pytest.mark.asyncio
    async def test_any_active_false_on_empty_registry(self):
        assert await get_process_registry().any_active("u1", "s1") is False

    @pytest.mark.asyncio
    async def test_handler_error_counts_as_not_active(self):
        flow = _StubFlow(active=True)
        flow.check_active = AsyncMock(side_effect=RuntimeError("db down"))
        get_process_registry().register(flow)
        assert await get_process_registry().any_active("u1", "s1") is False
