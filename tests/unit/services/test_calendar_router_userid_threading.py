"""
Issue #849: Tests for user_id threading through CalendarIntegrationRouter instantiation sites.

Category A: Verifies that user_id is correctly propagated from callers
through to CalendarIntegrationRouter for user-scoped keychain authentication.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.conversation.conversation_handler import ConversationHandler
from services.domain.models import Intent
from services.shared_types import IntentCategory


class TestCalendarRouterUserIdPropagation:
    """Issue #849: Verify CalendarIntegrationRouter receives user_id from all call sites."""

    def test_router_stores_user_id(self):
        """CalendarIntegrationRouter stores user_id when provided."""
        from services.integrations.calendar.calendar_integration_router import (
            CalendarIntegrationRouter,
        )

        router = CalendarIntegrationRouter(user_id="test_user_123")
        assert router._user_id == "test_user_123"

    def test_router_defaults_to_none(self):
        """CalendarIntegrationRouter defaults user_id to None."""
        from services.integrations.calendar.calendar_integration_router import (
            CalendarIntegrationRouter,
        )

        router = CalendarIntegrationRouter()
        assert router._user_id is None

    def test_factory_function_passes_user_id(self):
        """create_calendar_integration passes user_id to router."""
        from services.integrations.calendar.calendar_integration_router import (
            create_calendar_integration,
        )

        router = create_calendar_integration(user_id="factory_user")
        assert router._user_id == "factory_user"

    def test_factory_function_defaults_to_none(self):
        """create_calendar_integration defaults user_id to None."""
        from services.integrations.calendar.calendar_integration_router import (
            create_calendar_integration,
        )

        router = create_calendar_integration()
        assert router._user_id is None


class TestGetCalendarSummaryUserIdThreading:
    """Issue #849 Site A1: _get_calendar_summary threads user_id to CalendarIntegrationRouter."""

    @pytest.fixture
    def handler(self):
        return ConversationHandler()

    @pytest.mark.asyncio
    async def test_get_calendar_summary_passes_user_id(self, handler):
        """_get_calendar_summary creates CalendarIntegrationRouter with user_id."""
        # CalendarIntegrationRouter is imported lazily inside _get_calendar_summary,
        # so we patch at the source module path.
        with patch(
            "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter"
        ) as MockRouter:
            mock_instance = AsyncMock()
            mock_instance.get_temporal_summary = AsyncMock(return_value={"events": []})
            MockRouter.return_value = mock_instance

            await handler._get_calendar_summary(user_id="test_user")

            MockRouter.assert_called_once_with(user_id="test_user")

    @pytest.mark.asyncio
    async def test_get_calendar_summary_passes_none_by_default(self, handler):
        """_get_calendar_summary passes None when no user_id provided."""
        with patch(
            "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter"
        ) as MockRouter:
            mock_instance = AsyncMock()
            mock_instance.get_temporal_summary = AsyncMock(return_value={"events": []})
            MockRouter.return_value = mock_instance

            await handler._get_calendar_summary()

            MockRouter.assert_called_once_with(user_id=None)

    @pytest.mark.asyncio
    async def test_respond_to_greeting_threads_user_id_to_calendar(self, handler):
        """_respond_to_greeting passes user_id from intent.context to _get_calendar_summary."""
        intent = Intent(
            category=IntentCategory.CONVERSATION,
            action="greeting",
            context={"user_id": "greeting_user_123"},
        )

        with patch.object(handler, "_get_calendar_summary", new_callable=AsyncMock) as mock_cal:
            mock_cal.return_value = None
            with patch.object(
                handler, "_check_portfolio_onboarding", new_callable=AsyncMock
            ) as mock_onboard:
                mock_onboard.return_value = None

                await handler._respond_to_greeting(intent, "session_1", user_id="greeting_user_123")

                # user_id is extracted from intent.context in _respond_to_greeting,
                # which matches the explicit parameter passed
                mock_cal.assert_called_once_with(user_id="greeting_user_123")


class TestHandleAttentionQueryUserIdThreading:
    """Issue #849 Site A2: _handle_attention_query threads user_id to CalendarIntegrationRouter."""

    @pytest.mark.asyncio
    async def test_attention_query_passes_user_id_to_router(self):
        """_handle_attention_query creates CalendarIntegrationRouter with user_id."""
        from services.intent.intent_service import IntentService

        intent_service = IntentService.__new__(IntentService)
        intent_service.logger = MagicMock()

        intent = Intent(
            category=IntentCategory.QUERY,
            action="attention_query",
            context={"original_message": "what needs attention"},
        )

        # Patch at source module since CalendarIntegrationRouter is lazily imported
        with patch(
            "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter"
        ) as MockRouter:
            mock_instance = AsyncMock()
            mock_instance.authenticate = AsyncMock(return_value=False)
            MockRouter.return_value = mock_instance

            # Mock the DB access parts
            with patch("services.intent.intent_service.AsyncSessionFactory") as MockDB:
                mock_session = AsyncMock()
                mock_result = AsyncMock()
                mock_result.scalars.return_value.all.return_value = []
                mock_session.execute = AsyncMock(return_value=mock_result)

                mock_cm = AsyncMock()
                mock_cm.__aenter__ = AsyncMock(return_value=mock_session)
                mock_cm.__aexit__ = AsyncMock(return_value=None)
                MockDB.session_scope.return_value = mock_cm

                result = await intent_service._handle_attention_query(
                    intent, "workflow_1", "session_1", user_id="attention_user_456"
                )

                MockRouter.assert_called_with(user_id="attention_user_456")


class TestGetCalendarContextUserIdThreading:
    """Issue #849 Site A3: _get_calendar_context threads user_id to CalendarIntegrationRouter."""

    @pytest.mark.asyncio
    async def test_get_calendar_context_passes_user_id(self):
        """_get_calendar_context creates CalendarIntegrationRouter with user_id."""
        from services.intent_service.canonical_handlers import CanonicalHandlers

        handlers = CanonicalHandlers.__new__(CanonicalHandlers)

        # Issue #847 changed _get_calendar_context to use CalendarConfigService
        # instead of get_plugin_registry, so we mock the config service path.
        # CalendarConfigService is lazily imported, so patch at the source module.
        with patch(
            "services.integrations.calendar.config_service.CalendarConfigService"
        ) as MockConfigService:
            mock_config_instance = MagicMock()
            mock_config_instance.is_configured.return_value = True
            MockConfigService.return_value = mock_config_instance

            # Patch at source module since CalendarIntegrationRouter is lazily imported
            with patch(
                "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter"
            ) as MockRouter:
                mock_instance = AsyncMock()
                mock_instance.get_next_meeting = AsyncMock(return_value=None)
                mock_instance.get_free_time_blocks = AsyncMock(return_value=[])
                MockRouter.return_value = mock_instance

                await handlers._get_calendar_context(user_id="context_user_789")

                MockRouter.assert_called_once_with(user_id="context_user_789")

    @pytest.mark.asyncio
    async def test_handle_agenda_query_threads_user_id_to_calendar_context(self):
        """_handle_agenda_query passes user_id to _get_calendar_context."""
        from services.intent_service.canonical_handlers import CanonicalHandlers

        handlers = CanonicalHandlers.__new__(CanonicalHandlers)

        intent = Intent(
            category=IntentCategory.TEMPORAL,
            action="agenda_query",
            context={"original_message": "what is on the agenda"},
        )

        with patch.object(
            handlers, "_get_calendar_context", new_callable=AsyncMock
        ) as mock_cal_ctx:
            mock_cal_ctx.return_value = None
            with patch.object(handlers, "_get_todays_todos", new_callable=AsyncMock) as mock_todos:
                mock_todos.return_value = []
                with patch(
                    "services.intent_service.canonical_handlers.piper_config_loader"
                ) as mock_config:
                    mock_config.load_standup_config.return_value = {
                        "timing": {"timezone": "US/Pacific"}
                    }
                    with patch(
                        "services.intent_service.canonical_handlers.user_context_service"
                    ) as mock_user_ctx:
                        mock_user_ctx.get_user_context = AsyncMock(return_value=None)

                        await handlers._handle_agenda_query(
                            intent, "session_1", user_id="agenda_user_101"
                        )

                        mock_cal_ctx.assert_called_once_with(user_id="agenda_user_101")

    @pytest.mark.asyncio
    async def test_handle_guidance_query_threads_user_id_to_calendar_context(self):
        """_handle_guidance_query passes user_id to _get_calendar_context.

        We verify this by inspecting the source code for the call pattern,
        since the guidance query has deep internal flow that makes full mocking
        fragile. The actual _get_calendar_context threading is tested above.
        """
        import inspect

        from services.intent_service.canonical_handlers import CanonicalHandlers

        # Verify _handle_guidance_query accepts user_id parameter
        sig = inspect.signature(CanonicalHandlers._handle_guidance_query)
        assert "user_id" in sig.parameters, "_handle_guidance_query must accept user_id"

        # Verify user_id has default None (backward compatible)
        user_id_param = sig.parameters["user_id"]
        assert user_id_param.default is None, "user_id must default to None"

        # Verify the source contains the call to _get_calendar_context with user_id
        source = inspect.getsource(CanonicalHandlers._handle_guidance_query)
        assert (
            "_get_calendar_context(user_id=user_id)" in source
        ), "_handle_guidance_query must call _get_calendar_context(user_id=user_id)"


class TestHandleConversationQueryUserIdThreading:
    """Issue #849 Site A1 (canonical): _handle_conversation_query threads user_id."""

    @pytest.mark.asyncio
    async def test_handle_conversation_query_passes_user_id_to_respond(self):
        """_handle_conversation_query passes user_id to ConversationHandler.respond."""
        from services.intent_service.canonical_handlers import CanonicalHandlers

        handlers = CanonicalHandlers.__new__(CanonicalHandlers)

        intent = Intent(
            category=IntentCategory.CONVERSATION,
            action="greeting",
            context={"user_id": "conv_user_303"},
        )

        with patch("services.intent_service.canonical_handlers.ConversationHandler") as MockHandler:
            mock_instance = AsyncMock()
            mock_instance.respond = AsyncMock(
                return_value={
                    "message": "Hello!",
                    "intent": {"category": "conversation", "action": "greeting"},
                    "workflow_id": None,
                }
            )
            MockHandler.return_value = mock_instance

            await handlers._handle_conversation_query(intent, "session_1", user_id="conv_user_303")

            mock_instance.respond.assert_called_once_with(
                intent, "session_1", user_id="conv_user_303"
            )
