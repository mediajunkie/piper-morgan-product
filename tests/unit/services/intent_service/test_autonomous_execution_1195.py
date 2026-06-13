"""#1195 AutonomousExecutor wire — flag gating + the real read-only safety envelope.

These tests use the REAL AutonomousExecutor + ActionClassifier (only the
dispatch rail is stubbed), so they verify the actual safety boundary rather
than a mock of it: only SAFE (read-only) action_types at confidence >= 0.9
auto-execute; mutating / destructive / low-confidence patterns never do.

The minimal wire is read-only by construction (see
IntentService._maybe_autoexecute_automation_patterns docstring). Mutating
auto-execution + rollback UX is the fleshing-out increment (#1209); the
user-facing proactive surface is #1174.
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.intent.intent_service import IntentService


def _svc():
    svc = IntentService.__new__(IntentService)
    svc.logger = MagicMock()
    return svc


def _pattern(action_type, confidence, pid="p1"):
    return {
        "pattern_id": pid,
        "confidence": confidence,
        "pattern_data": {"action_type": action_type, "context": {}},
    }


def _fresh_executor():
    """Real AutonomousExecutor with a deterministically-not-stopped emergency
    stop (the stop is a process singleton; pin it so test order can't leak)."""
    from services.automation.autonomous_executor import AutonomousExecutor

    ex = AutonomousExecutor()
    ex.emergency_stop.is_stopped = MagicMock(return_value=False)
    return ex


class TestFlagGating:
    @pytest.mark.asyncio
    async def test_flag_off_is_noop(self, monkeypatch):
        monkeypatch.setenv("AUTONOMOUS_EXECUTION_ENABLED", "false")
        with patch(
            "services.automation.autonomous_executor.get_autonomous_executor"
        ) as gae:
            out = await _svc()._maybe_autoexecute_automation_patterns(
                [_pattern("list_issues_query", 0.95)], "s1", str(uuid4())
            )
        assert out == []
        gae.assert_not_called()  # never even constructs the executor

    @pytest.mark.asyncio
    async def test_no_user_id_is_noop(self, monkeypatch):
        monkeypatch.setenv("AUTONOMOUS_EXECUTION_ENABLED", "true")
        out = await _svc()._maybe_autoexecute_automation_patterns(
            [_pattern("list_issues_query", 0.95)], "s1", None
        )
        assert out == []

    @pytest.mark.asyncio
    async def test_empty_patterns_is_noop(self, monkeypatch):
        monkeypatch.setenv("AUTONOMOUS_EXECUTION_ENABLED", "true")
        out = await _svc()._maybe_autoexecute_automation_patterns([], "s1", str(uuid4()))
        assert out == []


class TestRealSafetyEnvelope:
    """Flag ON, real executor + classifier, dispatch stubbed."""

    @pytest.fixture(autouse=True)
    def _enable(self, monkeypatch):
        monkeypatch.setenv("AUTONOMOUS_EXECUTION_ENABLED", "true")

    async def _run(self, patterns):
        executor = _fresh_executor()
        dispatch = AsyncMock(return_value={"ok": True, "stub": "read result"})
        with patch(
            "services.automation.autonomous_executor.get_autonomous_executor",
            return_value=executor,
        ), patch(
            "services.intent_service.workflow_dispatcher.dispatch_workflow", dispatch
        ):
            out = await _svc()._maybe_autoexecute_automation_patterns(
                patterns, "s1", str(uuid4())
            )
        return out, dispatch

    @pytest.mark.asyncio
    async def test_safe_readonly_high_confidence_executes(self):
        out, dispatch = await self._run([_pattern("list_issues_query", 0.95)])
        assert len(out) == 1
        assert out[0]["action_type"] == "list_issues_query"
        assert out[0]["auto_executed"] is True
        dispatch.assert_awaited_once()  # the read actually ran through the rail
        # dispatched the predicted action type
        assert dispatch.await_args.kwargs["workflow_type"] == "list_issues_query"

    @pytest.mark.asyncio
    async def test_mutating_action_does_not_execute(self):
        # "create" => REQUIRES_CONFIRMATION => execute_with_safety refuses
        out, dispatch = await self._run([_pattern("create_github_issue", 0.99)])
        assert out == []
        dispatch.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_destructive_action_never_executes(self):
        out, dispatch = await self._run([_pattern("delete_repository", 0.99)])
        assert out == []
        dispatch.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_low_confidence_safe_action_does_not_execute(self):
        # SAFE but below the 0.9 threshold
        out, dispatch = await self._run([_pattern("list_issues_query", 0.7)])
        assert out == []
        dispatch.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_emergency_stop_blocks_even_safe_action(self):
        executor = _fresh_executor()
        executor.emergency_stop.is_stopped = MagicMock(return_value=True)
        dispatch = AsyncMock(return_value={"ok": True})
        with patch(
            "services.automation.autonomous_executor.get_autonomous_executor",
            return_value=executor,
        ), patch(
            "services.intent_service.workflow_dispatcher.dispatch_workflow", dispatch
        ):
            out = await _svc()._maybe_autoexecute_automation_patterns(
                [_pattern("list_issues_query", 0.95)], "s1", str(uuid4())
            )
        assert out == []
        dispatch.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_mutating_query_suffix_blocked_by_allowlist(self):
        """#1210 defense — now defense-in-depth (BOTH gates block).
        comment_issue_query / close_issue_query / reopen_issue_query MUTATE despite
        the '_query' suffix. The read-only allow-list (outer gate) blocks them; as
        of the #1210 fix the classifier (inner gate) ALSO correctly refuses them —
        it matches the mutating verb as an exact token, no longer fooled into SAFE
        by the 'query' substring."""
        from services.automation.action_classifier import ActionClassifier

        clf = ActionClassifier()
        # #1210 FIX: the classifier now CORRECTLY refuses these (was: wrongly SAFE,
        # which is what made the outer allow-list load-bearing). Inner gate restored.
        assert clf.is_safe_for_auto_execution("comment_issue_query", 0.99) is False
        assert clf.is_safe_for_auto_execution("close_issue_query", 0.99) is False
        assert clf.is_safe_for_auto_execution("reopen_issue_query", 0.99) is False

        out, dispatch = await self._run(
            [
                _pattern("comment_issue_query", 0.99, "mut1"),
                _pattern("close_issue_query", 0.99, "mut2"),
                _pattern("reopen_issue_query", 0.99, "mut3"),
            ]
        )
        assert out == []  # allow-list blocked all three
        dispatch.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_mixed_batch_only_allowlisted_reads_execute(self):
        out, dispatch = await self._run(
            [
                _pattern("list_issues_query", 0.95, "safe1"),
                _pattern("create_github_issue", 0.99, "mut1"),
                _pattern("comment_issue_query", 0.99, "mut2"),  # mutating — blocked by both gates (#1210)
                _pattern("delete_thing", 0.99, "des1"),
                _pattern("list_prs_query", 0.93, "safe2"),
            ]
        )
        executed_types = {e["action_type"] for e in out}
        assert executed_types == {"list_issues_query", "list_prs_query"}
        assert dispatch.await_count == 2

    @pytest.mark.asyncio
    async def test_pattern_without_action_type_skipped(self):
        out, dispatch = await self._run([{"pattern_id": "x", "confidence": 0.95, "pattern_data": {}}])
        assert out == []
        dispatch.assert_not_awaited()
