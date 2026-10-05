"""#1458 store-level pin (Arch, 2026-10-05): the one STATEFUL store on the MCP read path.

`test_two_caller_behavioural_1458.py` proves identity propagates into each store call, but it
stubs the stores themselves. Two of the three are stateless per call (a direct DB select, a fresh
GitHub adapter keyed by user). `user_context_service` is not: it keeps a process-lifetime cache.
This test runs the REAL `UserContextService.get_user_context` for two users, stubbing only the
loaders beneath the cache, and checks each caller gets its own context on the cache-miss path AND
on the cache-hit path after the other caller has filled the cache.
"""

from __future__ import annotations

from uuid import UUID

import pytest

from services.configuration.piper_config_loader import piper_config_loader
from services.user_context_service import UserContextService

pytestmark = pytest.mark.asyncio

USER_A = UUID("aaaaaaaa-0000-0000-0000-000000000001")
USER_B = UUID("bbbbbbbb-0000-0000-0000-000000000002")


@pytest.fixture
def service(monkeypatch) -> UserContextService:
    svc = UserContextService()  # fresh instance: empty cache, no cross-test leakage

    async def _projects(user_id: UUID) -> list:
        return [f"proj-{str(user_id)[:8]}"]

    async def _prefs(user_id: UUID) -> dict:
        return {}

    monkeypatch.setattr(svc, "_load_projects_from_db", _projects)
    monkeypatch.setattr(svc, "_load_user_preferences_from_db", _prefs)
    monkeypatch.setattr(piper_config_loader, "load_config", lambda *a, **k: {})
    return svc


async def test_each_user_gets_own_context_on_miss_and_on_hit(service) -> None:
    a1 = await service.get_user_context(session_id=f"mcp:{USER_A}", user_id=USER_A)
    b1 = await service.get_user_context(session_id=f"mcp:{USER_B}", user_id=USER_B)
    # Cache-hit path, each after the OTHER user has populated the cache.
    a2 = await service.get_user_context(session_id=f"mcp:{USER_A}", user_id=USER_A)
    b2 = await service.get_user_context(session_id=f"mcp:{USER_B}", user_id=USER_B)

    assert a1.user_id == a2.user_id == USER_A
    assert b1.user_id == b2.user_id == USER_B
    assert a1.projects == a2.projects == ["proj-aaaaaaaa"]
    assert b1.projects == b2.projects == ["proj-bbbbbbbb"]
    # The second reads were genuinely served from the cache, not two misses.
    assert service.cache_hits >= 2
    assert set(service.cache) == {f"user:{USER_A}", f"user:{USER_B}"}


async def test_session_id_cannot_select_another_users_entry(service) -> None:
    """The MCP call sites pass both; the cache key must follow user_id, never session_id."""
    await service.get_user_context(session_id="mcp:shared", user_id=USER_A)
    b = await service.get_user_context(session_id="mcp:shared", user_id=USER_B)

    assert b.user_id == USER_B
    assert b.projects == ["proj-bbbbbbbb"]
