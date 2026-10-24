"""#2151 FLOOR-ABSENT, memory (gather 6 of 7).

A failed conversation-history read left ``persistent_memory`` absent, the same as a
user with no prior conversations, so the floor could greet someone as new. These pins
run the real UserHistoryService over DBUserHistoryRepository and fail the read at the
repository's ``get_conversations``.
"""

from contextlib import asynccontextmanager
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.intent_service.context_assembler import ContextAssembler

UID = "00000000-0000-0000-0000-000000002151"


@asynccontextmanager
async def _fake_session_scope():
    yield MagicMock()


async def _gather(get_conversations):
    with (
        patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope",
            new=_fake_session_scope,
        ),
        patch(
            "services.database.repositories.DBUserHistoryRepository.get_conversations",
            new=get_conversations,
        ),
    ):
        return await ContextAssembler()._gather_memory_context(UID, None)


@pytest.mark.asyncio
async def test_a_failed_history_read_arms_the_flag():
    out = await _gather(AsyncMock(side_effect=TimeoutError("fake db timeout")))
    assert out == {"memory_source_failed": True}


@pytest.mark.asyncio
async def test_no_prior_conversations_is_a_verified_empty():
    out = await _gather(AsyncMock(return_value=([], 0)))
    assert out == {}


@pytest.mark.asyncio
async def test_history_read_renders_without_the_flag():
    conv = MagicMock()
    conv.topics = ["roadmap"]
    conv.last_activity = datetime.now(timezone.utc)
    conv.is_private = False
    with patch(
        "services.memory.user_history.UserHistoryService.get_history",
        new=AsyncMock(return_value=MagicMock(conversations=[conv], total_count=1)),
    ):
        out = await _gather(AsyncMock(return_value=([conv], 1)))
    assert out["persistent_memory"]["has_history"] is True
    assert "memory_source_failed" not in out
