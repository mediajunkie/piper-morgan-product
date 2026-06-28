"""#1317 inc.2 slice D — persist_github_connection orchestration.

On a successful OAuth callback: store the user's grant (encrypted #358 store) + mark the
#1229 binding BOUND with the self-hosted server ref. Binding holds no token (D3); the
grant store is mocked (DI) — #358 already tests encryption.
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.connectors.binding_repository import ConnectorBindingRepository  # noqa: E402
from services.database.models import ConnectorBinding  # noqa: E402
from services.mcp.consumer.connector import ConnectorStatusState  # noqa: E402
from services.mcp.consumer.github_oauth_handler import persist_github_connection  # noqa: E402

pytestmark = pytest.mark.asyncio

_ALPHA = "11111111-1111-1111-1111-111111111111"


@pytest_asyncio.fixture
async def maker():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: ConnectorBinding.__table__.create(c, checkfirst=True))
    yield async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    await engine.dispose()


class TestPersistGitHubConnection:
    async def test_stores_grant_and_marks_binding_bound(self, maker):
        grant = AsyncMock()
        async with maker() as s:
            await persist_github_connection(
                s, _ALPHA, "gho_tok", grant_store=grant, server_ref="http://srv/mcp"
            )
            await s.commit()

        # grant stored under (user, "github") with the token
        grant.store.assert_awaited_once()
        args, _ = grant.store.call_args
        assert args[1] == _ALPHA and args[2] == "github" and args[3] == "gho_tok"

        # binding now BOUND + records the server ref (no token on the row — D3)
        async with maker() as s:
            b = await ConnectorBindingRepository(s).get(_ALPHA, "github")
        assert b is not None
        assert b.status == ConnectorStatusState.BOUND.value
        assert b.mcp_server_ref == "http://srv/mcp"
