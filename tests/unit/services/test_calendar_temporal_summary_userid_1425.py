"""``get_temporal_summary`` must carry the principal like its siblings do.

``CalendarIntegrationRouter.get_todays_events`` resolves
``user_id or self._user_id``; ``get_temporal_summary`` passed ``user_id``
straight through, so the greeting path — which constructs the router WITH a
user and then calls ``get_temporal_summary()`` with no argument — reached the
adapter as ``user_id=None``. The adapter's ``_get_user_timezone(None)`` then
skips the preference lookup entirely and returns the hardcoded
``America/Los_Angeles`` fallback, so the day-boundary window belonged to no
particular user.

This is the plumbing half only. Deciding what a user's timezone IS, everywhere,
is #1572 and is deliberately out of scope here.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.integrations.calendar.calendar_integration_router import (
    CalendarIntegrationRouter,
)


@pytest.mark.asyncio
async def test_temporal_summary_falls_back_to_instance_user_id():
    router = CalendarIntegrationRouter(user_id="user-abc")
    router.spatial_calendar = MagicMock()
    router.spatial_calendar.get_temporal_summary = AsyncMock(return_value={})
    router.use_spatial = True

    await router.get_temporal_summary()

    router.spatial_calendar.get_temporal_summary.assert_awaited_once_with(user_id="user-abc")


@pytest.mark.asyncio
async def test_explicit_user_id_still_wins():
    router = CalendarIntegrationRouter(user_id="user-abc")
    router.spatial_calendar = MagicMock()
    router.spatial_calendar.get_temporal_summary = AsyncMock(return_value={})
    router.use_spatial = True

    await router.get_temporal_summary(user_id="user-explicit")

    router.spatial_calendar.get_temporal_summary.assert_awaited_once_with(
        user_id="user-explicit"
    )


@pytest.mark.asyncio
async def test_greeting_path_threads_the_principal():
    """The conversation handler's own call site — the one that dropped it."""
    from services.conversation.conversation_handler import ConversationHandler

    handler = ConversationHandler()
    fake_router = MagicMock()
    fake_router.authenticate = AsyncMock(return_value=True)
    fake_router.get_temporal_summary = AsyncMock(return_value={"success": True})

    with patch(
        "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
        return_value=fake_router,
    ):
        await handler._get_calendar_summary(user_id="user-abc")

    fake_router.get_temporal_summary.assert_awaited_once_with(user_id="user-abc")
