"""#2188 (Arch 2026-11-04 13:43 and 14:06; CXO 13:46): ``success`` means the requested
operation ran. The five chat GitHub degrade sites and the not-found write path answer
``success=False`` with the text unchanged and a typed not-performed marker; history
saves what was shown whatever the flag; the learning handler skips a marked result and
still records an unmarked failure; the bubble has no branch on the flag.
"""

import re
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.intent_service.conversation_context import clear_context
from services.intent_service.not_performed import (
    NOT_PERFORMED_KEY,
    NotPerformed,
    mark_not_performed,
    was_not_performed,
)
from services.mcp.consumer.connector import DegradationReason, DegradationResponse
from services.mcp.consumer.github_adapter import (
    GitHubIssuesResult,
    GitHubRepoScopedResult,
    github_degrade_reply,
)
from services.shared_types import IntentCategory

REPO = Path(__file__).resolve().parents[4]
_ADAPTER = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter"
_NATIVE = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"


@pytest.fixture
def svc():
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService()


def _intent(action, message):
    return Intent(
        category=IntentCategory.QUERY,
        action=action,
        confidence=0.9,
        context={"original_message": message, "user_id": str(uuid4())},
    )


def _degrade(reason=DegradationReason.UNREACHABLE):
    return DegradationResponse(
        reason=reason, user_message="GitHub's MCP server is unreachable right now."
    )


class TestTheMarker:
    def test_mark_and_read(self):
        data = mark_not_performed({"category": "query"}, NotPerformed.DEGRADED)
        assert data == {"category": "query", NOT_PERFORMED_KEY: "degraded"}
        r = IntentProcessingResult(success=False, message="x", intent_data=data)
        assert was_not_performed(r) is True

    def test_unmarked_and_garbage_read_false(self):
        assert (
            was_not_performed(IntentProcessingResult(success=False, message="x", intent_data={}))
            is False
        )
        assert (
            was_not_performed(
                IntentProcessingResult(
                    success=False, message="x", intent_data={NOT_PERFORMED_KEY: "outage"}
                )
            )
            is False
        )
        assert was_not_performed(MagicMock(intent_data=None)) is False

    def test_unknown_kind_is_refused(self):
        with pytest.raises(ValueError):
            mark_not_performed({}, "timed out")


class TestTheFiveChatSitesAnswerFalse:
    """One pin per site: ``success is False``, the reply is the helper's text, the marker is set."""

    @pytest.mark.asyncio
    async def test_stale_prs(self, svc):
        d = _degrade()
        with patch(
            f"{_ADAPTER}.list_open_prs",
            new=AsyncMock(return_value=GitHubIssuesResult(degradation=d)),
        ):
            with patch(_NATIVE) as native:
                res = await svc._handle_stale_prs(_intent("stale_prs", "stale prs"), "wf")
        assert res.success is False
        assert res.message == github_degrade_reply(d)
        assert res.intent_data[NOT_PERFORMED_KEY] == NotPerformed.DEGRADED
        native.assert_not_called()

    @pytest.mark.asyncio
    async def test_list_issues(self, svc):
        d = _degrade(DegradationReason.STALE_TOKEN)
        with patch(
            f"{_ADAPTER}.list_open_issues",
            new=AsyncMock(return_value=GitHubIssuesResult(degradation=d)),
        ):
            with patch(_NATIVE) as native:
                res = await svc._handle_list_issues_query(
                    _intent("list_issues_query", "how many open issues"), "wf"
                )
        assert res.success is False
        assert res.message == github_degrade_reply(d)
        assert res.intent_data[NOT_PERFORMED_KEY] == NotPerformed.DEGRADED
        native.assert_not_called()

    @pytest.mark.asyncio
    async def test_list_prs(self, svc):
        d = _degrade()
        with patch(
            f"{_ADAPTER}.list_open_prs",
            new=AsyncMock(return_value=GitHubIssuesResult(degradation=d)),
        ):
            with patch(_NATIVE) as native:
                res = await svc._handle_list_prs_query(
                    _intent("list_prs_query", "show my prs"), "wf"
                )
        assert res.success is False
        assert res.message == github_degrade_reply(d)
        assert res.intent_data[NOT_PERFORMED_KEY] == NotPerformed.DEGRADED
        native.assert_not_called()

    @pytest.mark.asyncio
    async def test_list_releases(self, svc):
        d = _degrade()
        with patch(
            f"{_ADAPTER}.list_releases_connector",
            new=AsyncMock(return_value=GitHubRepoScopedResult(degradation=d)),
        ):
            with patch(_NATIVE) as native:
                res = await svc._handle_list_releases_query(
                    _intent("list_releases_query", "recent releases"), "wf"
                )
        assert res.success is False
        assert res.message == github_degrade_reply(d)
        assert res.intent_data[NOT_PERFORMED_KEY] == NotPerformed.DEGRADED
        native.assert_not_called()

    @pytest.mark.asyncio
    async def test_list_branches(self, svc):
        d = _degrade()
        with patch(
            f"{_ADAPTER}.list_branches_connector",
            new=AsyncMock(return_value=GitHubRepoScopedResult(degradation=d)),
        ):
            with patch(_NATIVE) as native:
                res = await svc._handle_list_branches_query(
                    _intent("list_branches_query", "active branches"), "wf"
                )
        assert res.success is False
        assert res.message == github_degrade_reply(d)
        assert res.intent_data[NOT_PERFORMED_KEY] == NotPerformed.DEGRADED
        native.assert_not_called()

    def test_every_degrade_site_carries_the_marker(self):
        """The five ``github_degrade_reply`` sites each open with the marker and False."""
        src = (REPO / "services/intent/intent_service.py").read_text()
        sites = re.findall(
            r"success=(\w+),[^\n]*\n\s*message=github_degrade_reply\(connector_result\.degradation\),\n"
            r"\s*intent_data=\{\n\s*([A-Z_]+): NotPerformed\.DEGRADED,",
            src,
        )
        assert sites == [("False", "NOT_PERFORMED_KEY")] * 5


class TestHistorySavesWhatWasShown:
    """Arch (1): any turn with a message is saved, whatever ``success``; empty still is not."""

    def _svc(self, success, message):
        s = IntentService.__new__(IntentService)
        s.logger = MagicMock()
        internal = MagicMock()
        internal.success = success
        internal.message = message
        internal.intent_data = {
            "category": "query",
            "action": "list_issues_query",
            NOT_PERFORMED_KEY: "degraded",
        }
        s._process_intent_internal = AsyncMock(return_value=internal)
        s._observe_action_verb = MagicMock()
        s._record_session_activity = AsyncMock()
        s.conversation_manager = MagicMock()
        s.conversation_manager.save_conversation_turn = AsyncMock()
        return s

    @pytest.mark.asyncio
    async def test_a_false_degrade_reply_with_a_message_is_saved(self):
        sid, uid = f"s2188-{uuid4()}", str(uuid4())
        clear_context(sid, uid)
        s = self._svc(
            False,
            "Your GitHub connection needs re-authorizing. Reconnect GitHub in Settings, under Integrations.",
        )
        await IntentService.process_intent(
            s, message="show open issues", session_id=sid, user_id=uid
        )
        save = s.conversation_manager.save_conversation_turn
        save.assert_awaited_once()
        assert save.await_args.kwargs["assistant_response"].startswith(
            "Your GitHub connection needs re-authorizing."
        )
        assert save.await_args.kwargs["intent"] == "query:list_issues_query"
        clear_context(sid, uid)

    @pytest.mark.asyncio
    async def test_an_empty_reply_is_still_not_saved(self):
        sid, uid = f"s2188-{uuid4()}", str(uuid4())
        clear_context(sid, uid)
        s = self._svc(False, "")
        await IntentService.process_intent(
            s, message="show open issues", session_id=sid, user_id=uid
        )
        s.conversation_manager.save_conversation_turn.assert_not_awaited()
        clear_context(sid, uid)


class TestLearningSkipsOnTheMarker:
    """Arch (2): a marked result records nothing; an unmarked failure records False."""

    def _svc(self):
        s = IntentService.__new__(IntentService)
        s.logger = MagicMock()
        s.learning_handler = MagicMock()
        s.learning_handler.record_outcome = AsyncMock(return_value=True)
        return s

    @pytest.mark.asyncio
    async def test_a_marked_degrade_records_nothing(self):
        s = self._svc()
        r = IntentProcessingResult(
            success=False, message="x", intent_data={NOT_PERFORMED_KEY: NotPerformed.DEGRADED}
        )
        with patch("services.intent.intent_service.AsyncSessionFactory") as f:
            await s._record_learning_outcome(r, uuid4(), uuid4())
        s.learning_handler.record_outcome.assert_not_awaited()
        f.session_scope.assert_not_called()

    @pytest.mark.asyncio
    async def test_a_marked_not_found_records_nothing(self):
        s = self._svc()
        r = IntentProcessingResult(
            success=False, message="x", intent_data={NOT_PERFORMED_KEY: NotPerformed.NOT_FOUND}
        )
        with patch("services.intent.intent_service.AsyncSessionFactory"):
            await s._record_learning_outcome(r, uuid4(), uuid4())
        s.learning_handler.record_outcome.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_an_unmarked_failure_records_false(self):
        s = self._svc()
        r = IntentProcessingResult(success=False, message="x", intent_data={"category": "query"})
        with patch("services.intent.intent_service.AsyncSessionFactory") as f:
            f.session_scope.return_value.__aenter__ = AsyncMock(return_value="db")
            f.session_scope.return_value.__aexit__ = AsyncMock(return_value=False)
            await s._record_learning_outcome(r, "p1", "u1")
        s.learning_handler.record_outcome.assert_awaited_once()
        assert s.learning_handler.record_outcome.await_args.kwargs["success"] is False

    @pytest.mark.asyncio
    async def test_a_success_still_records_true(self):
        s = self._svc()
        r = IntentProcessingResult(success=True, message="x", intent_data={"category": "query"})
        with patch("services.intent.intent_service.AsyncSessionFactory") as f:
            f.session_scope.return_value.__aenter__ = AsyncMock(return_value="db")
            f.session_scope.return_value.__aexit__ = AsyncMock(return_value=False)
            await s._record_learning_outcome(r, "p1", "u1")
        assert s.learning_handler.record_outcome.await_args.kwargs["success"] is True

    @pytest.mark.asyncio
    async def test_no_pattern_records_nothing(self):
        s = self._svc()
        r = IntentProcessingResult(success=True, message="x", intent_data={})
        await s._record_learning_outcome(r, None, "u1")
        s.learning_handler.record_outcome.assert_not_awaited()

    def test_the_service_has_one_record_site_and_it_is_the_method(self):
        src = (REPO / "services/intent/intent_service.py").read_text()
        assert src.count("self.learning_handler.record_outcome(") == 1
        assert "await self._record_learning_outcome(result, pattern_id, learning_user_id)" in src


class TestTheBubbleHasNoBranchOnTheFlag:
    """CXO 13:46: a ``success=False`` reply renders in the ordinary bubble. The route
    puts no ``success`` in the body and answers 200, and the chat script reads no
    body-level flag, so there is no visual change (Arch's and CXO's expectation)."""

    def test_the_route_body_carries_no_success_key(self):
        src = (REPO / "web/api/routes/intent.py").read_text()
        i = src.index('"message": result.message,')
        body = src[i : src.index("return response", i)]
        assert '"success"' not in body and "result.success" not in body

    def test_chat_js_reads_no_reply_level_success(self):
        src = (REPO / "web/static/js/chat.js").read_text()
        reads = [m for m in re.findall(r"(\w+)\.success\b", src) if m != "ToastMessages"]
        assert reads == ["permissionResult"]
