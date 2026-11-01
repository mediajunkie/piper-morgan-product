"""#2242: the real read of ``users.preferences`` behind ``may_connect_mcp``.

The unit file pins the predicate with a dict-backed reader because the MCP
unit tests' in-memory SQLite cannot hold the ``users`` table. This pins the
default reader on Postgres: a JSON ``true`` lists the account; the string
``"true"``, a missing key and a missing row do not. LAYER: the ORM read on the
dev database; DENOMINATOR: the one list source, three rows.
"""

from __future__ import annotations

import uuid

import pytest

from services.database.models import User
from services.database.session_factory import AsyncSessionFactory
from services.mcp.server.allowlist import MCP_ALLOW_KEY, may_connect_mcp, read_preferences

pytestmark = [pytest.mark.asyncio, pytest.mark.integration]


async def _user(session, prefs):
    uid = uuid.uuid4()
    session.add(
        User(
            id=uid,
            username=f"allow-{uid.hex[:8]}",
            email=f"allow-{uid.hex[:8]}@test.invalid",
            is_alpha=True,
            preferences=prefs,
        )
    )
    await session.commit()
    return uid


@pytest.mark.asyncio
async def test_real_read_lists_only_json_true(db_session):
    listed = await _user(db_session, {MCP_ALLOW_KEY: True})
    stringy = await _user(db_session, {MCP_ALLOW_KEY: "true"})
    plain = await _user(db_session, {"timezone": "UTC"})
    try:
        scope = AsyncSessionFactory.session_scope_fresh
        assert await read_preferences(listed, session_scope=scope) == {MCP_ALLOW_KEY: True}
        assert await read_preferences(uuid.uuid4(), session_scope=scope) is None
        assert await may_connect_mcp(listed, session_scope=scope) is True
        assert await may_connect_mcp(stringy, session_scope=scope) is False
        assert await may_connect_mcp(plain, session_scope=scope) is False
        assert await may_connect_mcp(uuid.uuid4(), session_scope=scope) is False
    finally:
        for uid in (listed, stringy, plain):
            row = await db_session.get(User, uid)
            if row is not None:
                await db_session.delete(row)
        await db_session.commit()
