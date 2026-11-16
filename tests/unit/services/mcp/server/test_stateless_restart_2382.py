"""#2382: the first connector read after the MCP server gets a new process is served.

The SDK's default (stateful streamable HTTP) keeps each client's ``Mcp-Session-Id`` in
process memory. A client that initialized against the old process sends that id to the
new one, which doesn't know it. Arch's ruling (2026-11-15): run stateless, since this
server keeps no per-session state.

LAYER: raw JSON-RPC over HTTP against the real ASGI app (bearer auth, rate limit, path
gate), in process. Two app instances stand for the old and the new process. Not a
deployed server, and not the Claude connector itself.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from contextlib import asynccontextmanager

import httpx
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from services.database.models import MCPAccessToken
from services.database.session_factory import AsyncSessionFactory
from services.mcp.server import allowlist as _allowlist
from services.mcp.server.app import MCPPathGate, build_mcp_server
from services.mcp.server.rate_limit import MCPRateLimitMiddleware
from services.mcp.server.resources import PROFILE_URI
from services.user_context_service import UserContext, user_context_service

BASE = "http://127.0.0.1:8765"
USER = uuid.UUID("5a1e0000-0000-4000-8000-000000002382")
RAW_TOKEN = "mcp_restartCase2382"
ACCEPT = "application/json, text/event-stream"


@pytest.fixture(autouse=True)
def _listed(monkeypatch):
    async def _prefs(_user_id, **_kwargs):
        return {_allowlist.MCP_ALLOW_KEY: True}

    monkeypatch.setattr(_allowlist, "read_preferences", _prefs)


@pytest_asyncio.fixture
async def token(monkeypatch):
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )
    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @asynccontextmanager
    async def _scope():
        session = factory()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async with engine.begin() as conn:
        await conn.run_sync(lambda c: MCPAccessToken.__table__.create(c, checkfirst=True))
    async with factory() as session:
        session.add(
            MCPAccessToken(
                id=uuid.uuid4(),
                user_id=USER,
                token_hash=hashlib.sha256(RAW_TOKEN.encode()).hexdigest(),
                label="2382",
            )
        )
        await session.commit()
    monkeypatch.setattr(AsyncSessionFactory, "session_scope", _scope)
    yield RAW_TOKEN
    await engine.dispose()


@asynccontextmanager
async def _process(stateless=None):
    """One server process: a freshly built app with its session manager running."""
    mcp = build_mcp_server()
    if stateless is not None:
        mcp.settings.stateless_http = stateless
    inner = mcp.streamable_http_app()
    path = mcp.settings.streamable_http_path
    app = MCPPathGate(MCPRateLimitMiddleware(inner, mcp_path=path), mcp_path=path)
    async with mcp.session_manager.run():
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url=BASE, timeout=30.0
        ) as client:
            yield client, path


def _rpc(method, request_id, params=None):
    body = {"jsonrpc": "2.0", "id": request_id, "method": method}
    if params is not None:
        body["params"] = params
    return body


def _result(response):
    """The JSON-RPC message of a reply, whether sent as JSON or as one SSE event."""
    if response.headers.get("content-type", "").startswith("text/event-stream"):
        data = [ln[5:].strip() for ln in response.text.splitlines() if ln.startswith("data:")]
        return json.loads(data[-1])
    return response.json()


async def _initialize(client, path, bearer):
    return await client.post(
        path,
        headers={"Authorization": f"Bearer {bearer}", "Accept": ACCEPT},
        json=_rpc(
            "initialize",
            1,
            {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "restart-case", "version": "0"},
            },
        ),
    )


async def _list_tools(client, path, bearer, session_id):
    headers = {"Authorization": f"Bearer {bearer}", "Accept": ACCEPT}
    if session_id:
        headers["mcp-session-id"] = session_id
    return await client.post(path, headers=headers, json=_rpc("tools/list", 2))


async def _read_profile(client, path, bearer, session_id):
    headers = {"Authorization": f"Bearer {bearer}", "Accept": ACCEPT}
    if session_id:
        headers["mcp-session-id"] = session_id
    return await client.post(
        path, headers=headers, json=_rpc("resources/read", 3, {"uri": PROFILE_URI})
    )


def test_the_server_is_built_stateless():
    assert build_mcp_server().settings.stateless_http is True


async def test_a_read_on_a_new_process_serves_with_the_old_process_s_session(token):
    # The old process: the client initializes and keeps whatever session id it is given.
    async with _process() as (old, path):
        first = await _initialize(old, path, token)
        assert first.status_code == 200, first.text
        held = first.headers.get("mcp-session-id")

    # The new process has never seen that client. Its next request is a plain read,
    # carrying the session id it holds (or one from before, if none was issued).
    async with _process() as (new, path):
        reply = await _list_tools(new, path, token, held or "session-from-the-old-process")
        assert reply.status_code == 200, reply.text
        tools = _result(reply)["result"]["tools"]
        assert tools, "the read was answered with no tools"


async def test_a_resource_read_on_a_new_process_serves_the_callers_own_data(token, monkeypatch):
    """Arch's acceptance row: initialize against one instance, read a RESOURCE against
    a fresh one with the same bearer. The bearer alone names the caller."""
    asked_for = []

    async def _profile(session_id=None, user_id=None):
        asked_for.append(user_id)
        return UserContext(
            user_id=user_id,
            organization="Org-2382",
            projects=["proj-2382"],
            priorities=[],
            projects_source="config",
        )

    monkeypatch.setattr(user_context_service, "get_user_context", _profile)

    async with _process() as (old, path):
        first = await _initialize(old, path, token)
        assert first.status_code == 200, first.text
        held = first.headers.get("mcp-session-id")

    async with _process() as (new, path):
        reply = await _read_profile(new, path, token, held or "session-from-the-old-process")
        assert reply.status_code == 200, reply.text
        message = _result(reply)
        assert "error" not in message, message
        text = message["result"]["contents"][0]["text"]
        assert "proj-2382" in text
    assert asked_for == [USER]


async def test_a_stateless_server_issues_no_session_id(token):
    async with _process() as (client, path):
        first = await _initialize(client, path, token)
        assert first.status_code == 200
        assert first.headers.get("mcp-session-id") is None


async def test_the_same_read_is_refused_by_a_stateful_server(token):
    """The contrast that shows the test above can fail: with the SDK's default, a new
    process refuses a session id it never issued. This is the defect as served."""
    async with _process(stateless=False) as (old, path):
        first = await _initialize(old, path, token)
        held = first.headers.get("mcp-session-id")
        assert first.status_code == 200 and held

    async with _process(stateless=False) as (new, path):
        reply = await _list_tools(new, path, token, held)
        assert reply.status_code in (400, 404), reply.text


async def test_the_bearer_is_still_required_on_a_stateless_read(token):
    async with _process() as (client, path):
        reply = await client.post(path, headers={"Accept": ACCEPT}, json=_rpc("tools/list", 2))
        assert reply.status_code == 401
        wrong = await _list_tools(client, path, "mcp_notARealToken", None)
        assert wrong.status_code == 401
