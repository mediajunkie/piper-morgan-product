"""#1423 slice 1 — silent-death un-swallow: failures must SURFACE, not vanish.

Each test forces the underlying error at a formerly-swallowed site and asserts
the failure now surfaces the way the call site's contract honestly supports:

- top-level intent handlers (standup / list_issues / set_default_repo /
  get_default_repo) return an HONEST error result — success=False with
  error/error_type populated — instead of the old success=True "degraded" lie;
- fire-and-forget persistence paths (_save_conversation_turn,
  hydrate_turns_from_db, _check_active_guided_process, slot-filling
  registration) still never block the turn, but now emit an error/warning log
  record where before there was either a bare ``pass`` or an info-starved
  warning;
- the todo handlers' broad catches were NARROWED to expected DB-layer errors
  (SQLAlchemyError/OSError): infra failures still get the friendly message,
  while code bugs now PROPAGATE to the route's degradation boundary instead of
  masquerading as "a temporary issue";
- the integration-setup guidance says honestly that it could not check
  connection status instead of silently omitting it.

History this guards against: the standup generator's empty sections and the
#1465 inverted learning signal were both this pattern — a broad except-continue
converting a broken feature into a plausible default.
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from sqlalchemy.exc import OperationalError

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.shared_types import IntentCategory

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def intent_service():
    """IntentService with heavy deps patched out (mirrors cohort handler tests)."""
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService()


def _query_intent(action: str, message: str, user_id: str = "user-123") -> Intent:
    return Intent(
        category=IntentCategory.QUERY,
        action=action,
        context={"original_message": message, "user_id": user_id},
    )


# ---------------------------------------------------------------------------
# 1. Standup query handler — honest error result, no success=True lie
# ---------------------------------------------------------------------------


class TestStandupQueryHonestError:
    @pytest.mark.asyncio
    async def test_standup_failure_returns_success_false_with_error(self, intent_service):
        intent = _query_intent("show_standup", "give me my standup")
        with patch(
            "services.standup.assembler.build_user_standup_summary",
            side_effect=RuntimeError("assembler exploded"),
        ):
            result = await intent_service._handle_standup_query(intent, "wf-1", user_id="user-123")
        assert isinstance(result, IntentProcessingResult)
        assert (
            result.success is False
        ), "standup generation failure must not report success=True 'degraded'"
        assert result.error is not None and "assembler exploded" in result.error
        assert result.error_type == "standup_generation_error"
        # Message is still conversational, not a stack trace.
        assert "standup" in result.message.lower()


# ---------------------------------------------------------------------------
# 2-4. GitHub-surface handlers — honest error results
# ---------------------------------------------------------------------------


class TestGitHubHandlersHonestError:
    @pytest.mark.asyncio
    async def test_list_issues_failure_is_success_false(self, intent_service):
        intent = _query_intent("list_issues_query", "how many open issues?")
        with patch(
            "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter",
            side_effect=RuntimeError("adapter down"),
        ):
            result = await intent_service._handle_list_issues_query(intent, "wf-1")
        assert result.success is False
        assert result.error_type == "list_issues_error"
        assert "adapter down" in (result.error or "")

    @pytest.mark.asyncio
    async def test_set_default_repo_failed_write_is_success_false(self, intent_service):
        """A FAILED WRITE must never report success=True (worst of the lies)."""
        intent = _query_intent(
            "set_default_repo", "set my default repo to mediajunkie/piper-morgan-product"
        )
        with patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope",
            side_effect=RuntimeError("db down"),
        ):
            result = await intent_service._handle_set_default_repo(intent, "wf-1")
        assert result.success is False
        assert result.error_type == "set_default_repo_error"
        assert "db down" in (result.error or "")

    @pytest.mark.asyncio
    async def test_get_default_repo_failure_is_success_false(self, intent_service):
        intent = _query_intent("get_default_repo", "what is my default repo?")
        with patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope",
            side_effect=RuntimeError("db down"),
        ):
            result = await intent_service._handle_get_default_repo(intent, "wf-1")
        assert result.success is False
        assert result.error_type == "get_default_repo_error"


# ---------------------------------------------------------------------------
# 5-6. Todo handlers — narrowed catch: infra degrades, bugs propagate
# ---------------------------------------------------------------------------


def _db_error() -> OperationalError:
    return OperationalError("SELECT 1", {}, Exception("connection refused"))


class TestTodoHandlersNarrowedCatch:
    @pytest.fixture
    def handlers(self):
        from services.intent_service.todo_handlers import TodoIntentHandlers

        h = TodoIntentHandlers()
        h.todo_service = MagicMock()
        return h

    def _intent(self, message: str) -> Intent:
        return Intent(
            category=IntentCategory.EXECUTION,
            action="create_todo",
            context={"original_message": message},
        )

    @pytest.mark.asyncio
    async def test_create_todo_db_failure_gets_friendly_message(self, handlers):
        handlers.todo_service.create_todo = AsyncMock(side_effect=_db_error())
        msg = await handlers.handle_create_todo(
            self._intent("add todo: test the ratchet"), "sess-1", user_id=uuid4()
        )
        assert "had trouble saving" in msg

    @pytest.mark.asyncio
    async def test_create_todo_code_bug_propagates(self, handlers):
        """An unexpected error (a CODE bug) must no longer vanish into
        'it may be a temporary issue' — it propagates to the route boundary."""
        handlers.todo_service.create_todo = AsyncMock(
            side_effect=AttributeError("'NoneType' object has no attribute 'id'")
        )
        with pytest.raises(AttributeError):
            await handlers.handle_create_todo(
                self._intent("add todo: test the ratchet"), "sess-1", user_id=uuid4()
            )

    @pytest.mark.asyncio
    async def test_list_todos_db_failure_gets_friendly_message(self, handlers):
        handlers.todo_service.list_todos = AsyncMock(side_effect=_db_error())
        msg = await handlers.handle_list_todos(
            self._intent("show my todos"), "sess-1", user_id=uuid4()
        )
        assert "had trouble loading" in msg

    @pytest.mark.asyncio
    async def test_list_todos_code_bug_propagates(self, handlers):
        handlers.todo_service.list_todos = AsyncMock(side_effect=TypeError("bad arg"))
        with pytest.raises(TypeError):
            await handlers.handle_list_todos(
                self._intent("show my todos"), "sess-1", user_id=uuid4()
            )


# ---------------------------------------------------------------------------
# 7. Turn hydration — still best-effort, but the failure is now LOGGED
# ---------------------------------------------------------------------------


class TestHydrationFailureIsLogged:
    @pytest.mark.asyncio
    async def test_hydrate_failure_logs_warning(self):
        from services.intent_service import conversation_context as cc
        from services.intent_service.conversation_context import (
            clear_context,
            get_or_create_context,
            hydrate_turns_from_db,
        )

        sid, uid = str(uuid4()), str(uuid4())
        ctx = get_or_create_context(sid, user_id=uid)
        manager = MagicMock()
        manager.get_recent_turns = AsyncMock(side_effect=RuntimeError("db down"))
        mock_logger = MagicMock()
        with patch.object(cc, "logger", mock_logger):
            assert await hydrate_turns_from_db(ctx, manager, sid) is False
        assert (
            mock_logger.warning.called
        ), "hydration failure was a ZERO-telemetry swallow — it must log now"
        clear_context(sid, uid)


# ---------------------------------------------------------------------------
# 8. _save_conversation_turn — persistence loss logs at ERROR with traceback
# ---------------------------------------------------------------------------


class TestSaveTurnFailureIsError:
    @pytest.mark.asyncio
    async def test_save_failure_logs_error(self, intent_service):
        intent_service.conversation_manager = MagicMock()
        intent_service.conversation_manager.save_conversation_turn = AsyncMock(
            side_effect=RuntimeError("db down")
        )
        mock_logger = MagicMock()
        intent_service.logger = mock_logger
        # Must not raise (response delivery wins) …
        await intent_service._save_conversation_turn("sess-1", "hi", "hello")
        # … but must log at ERROR (was warning), with exc_info.
        assert mock_logger.error.called
        _, kwargs = mock_logger.error.call_args
        assert kwargs.get("exc_info") is True


# ---------------------------------------------------------------------------
# 9. Guided-process check — fallback preserved, failure logs at ERROR
# ---------------------------------------------------------------------------


class TestGuidedProcessCheckFailureIsError:
    @pytest.mark.asyncio
    async def test_registry_failure_logs_error_and_falls_through(self, intent_service):
        mock_logger = MagicMock()
        intent_service.logger = mock_logger
        with patch(
            "services.intent.intent_service.get_process_registry",
            side_effect=RuntimeError("registry gone"),
        ):
            result, prefix = await intent_service._check_active_guided_process(
                "user-123", "sess-1", "yes, three blockers"
            )
        assert result is None and prefix is None  # designed fallback preserved
        assert mock_logger.error.called, "dropping a user out of a guided flow must be ops-visible"


# ---------------------------------------------------------------------------
# 10. Integration-setup guidance — honest about a failed status check
# ---------------------------------------------------------------------------


class TestIntegrationGuidanceHonestStatus:
    @pytest.mark.asyncio
    async def test_status_check_failure_is_named_in_message(self):
        from unittest.mock import AsyncMock

        from services.intent_service.canonical_handlers import CanonicalHandlers

        handlers = CanonicalHandlers()
        # #1547: the status source is the canonical IntegrationStatusService now;
        # the honesty contract is unchanged — a failed check is NAMED, not silent.
        with patch(
            "services.integrations.integration_status_service." "IntegrationStatusService.get_all",
            new=AsyncMock(side_effect=RuntimeError("status source down")),
        ):
            response = await handlers._format_integration_setup_guidance(user_id="u1")
        assert "couldn't check your current connection status" in response["message"]


# ---------------------------------------------------------------------------
# 11. Slot-filling registration — init survives, but the loss is logged
# ---------------------------------------------------------------------------


class TestSlotFillingRegistrationFailureIsLogged:
    def test_init_survives_and_logs(self):
        mock_logger = MagicMock()
        with (
            patch("services.intent.intent_service.LearningHandler"),
            patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"),
            patch(
                "services.intent.intent_service.get_process_registry",
                side_effect=RuntimeError("registry gone"),
            ),
            patch(
                "services.intent.intent_service.structlog.get_logger",
                return_value=mock_logger,
            ),
        ):
            service = IntentService()  # must not raise
        assert service is not None
        assert mock_logger.error.called, "silent slot-filling loss must be visible in logs"
