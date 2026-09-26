"""Phase C unit 2 — the three owner-scoped MCP resources (#1462).

Pins the build plan's unit 2 acceptance points and Arch's slice doc's "never silently
empty" contract, proven through a real MCP client round trip — not a direct call into
the resource functions:

(a) `resources/list` returns exactly the three URIs (`piper://me/profile`,
    `piper://me/colleague-model`, `piper://me/github/issues`) and nothing else.
(b) each resource, read with user A's token, returns A's data and never B's — the three
    read surfaces (user-context, the #1510 preference store, the GitHub connector) are
    mocked per-user and the user_id each stub receives is asserted to equal the token's
    own owner, not just "some" plausible value.
(c) a profile read failure (the user-context read raises) -> a structured honest-empty
    payload (`available: false`), and the MCP *protocol* layer still returns 200/success —
    the failure is caught inside the resource, never surfaced as a JSON-RPC error.
(d) colleague-model with nothing verified -> the honest-empty shape (`verified: []`,
    a `note` field), not an exception and not a fabricated entry.
(e) the GitHub resource: unbound -> `{"available": false, "reason": "connect_required",
    "connector": "github"}`; bound -> issues plus `count`/`capped_at`.
(f) the server's advertised capabilities are still resources-only (re-asserted here,
    now WITH resources actually registered, complementing unit 0's zero-resources
    version of the same check).

LAYER (m-43): every read/write test goes through a real MCP client
(`mcp.client.streamable_http` + `ClientSession`) over an in-process ASGI transport built
by `services.mcp.server.app.build_asgi_app()` — the same client-side protocol surface a
real tester's client speaks, exercising unit 1's real bearer-auth machinery end to end,
not a direct call into a resource function. Token seeding/session-scope fixture and the
real-client helper are the same idiom `test_identity_unit1.py` established.

DENOMINATOR: unit 2's three resources only. Identity boundary correctness (401s,
revocation, expiry, two-caller isolation at the AUTH layer) is `test_identity_unit1.py`'s
scope, not re-proven here — this file assumes a valid bearer resolves correctly (unit 1,
already pinned) and tests what each RESOURCE does once identity is resolved.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from contextlib import asynccontextmanager
from typing import Any

import httpx
import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

import sse_starlette.sse as _sse_starlette_sse  # noqa: E402
from mcp.client.session import ClientSession  # noqa: E402
from mcp.client.streamable_http import streamable_http_client  # noqa: E402
from pydantic import AnyUrl  # noqa: E402
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool  # noqa: E402

from services.database.models import MCPAccessToken  # noqa: E402
from services.database.session_factory import AsyncSessionFactory  # noqa: E402
from services.mcp.consumer.connector import (  # noqa: E402
    DegradationReason,
    DegradationResponse,
)
from services.mcp.consumer.github_adapter import (  # noqa: E402
    GitHubIssuesResult,
    GitHubMCPSpatialAdapter,
)
from services.mcp.server.app import MCPPathGate, build_mcp_server  # noqa: E402
from services.mcp.server.resources import (  # noqa: E402
    COLLEAGUE_MODEL_URI,
    GITHUB_ISSUES_PAGE_CAP,
    GITHUB_ISSUES_URI,
    PROFILE_URI,
)
from services.user_context_service import UserContext, user_context_service  # noqa: E402

# NOTE: no module-wide `pytestmark = pytest.mark.asyncio` — `asyncio_mode = auto`
# (pytest.ini) already runs every `async def test_*` as an asyncio test; a blanket
# pytestmark here would also tag this file's one SYNC test
# (TestCapabilitiesStillResourcesOnly's capability check) with an asyncio marker it
# doesn't need, which pytest-asyncio warns about.

MCP_PATH = "/mcp"
LOCAL_BASE_URL = "http://localhost:8080"

USER_A = uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
USER_B = uuid.UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")


@pytest.fixture(autouse=True)
def _reset_sse_starlette_loop_singleton():
    """Same fresh-per-test singleton reset as test_identity_unit1.py — see that file's
    module docstring for why this is load-bearing when several tests in one file reach
    a real `initialize` response."""
    _sse_starlette_sse.AppStatus.should_exit = False
    _sse_starlette_sse.AppStatus.should_exit_event = None
    yield


def _hash(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@pytest_asyncio.fixture
async def token_store():
    """Same in-memory-SQLite token store as test_identity_unit1.py."""
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

    yield factory, _scope

    await engine.dispose()


async def _seed_token(factory, *, user_id: uuid.UUID, raw_token: str, label: str = "test") -> None:
    async with factory() as session:
        session.add(
            MCPAccessToken(
                id=uuid.uuid4(),
                user_id=user_id,
                token_hash=_hash(raw_token),
                label=label,
            )
        )
        await session.commit()


@asynccontextmanager
async def _session(asgi_app, raw_token: str):
    headers = {"Authorization": f"Bearer {raw_token}"}
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=asgi_app),
        base_url=LOCAL_BASE_URL,
        headers=headers,
        timeout=httpx.Timeout(30.0),
    ) as http_client:
        async with streamable_http_client(
            f"{LOCAL_BASE_URL}{MCP_PATH}", http_client=http_client
        ) as (read_stream, write_stream, _get_session_id):
            async with ClientSession(read_stream, write_stream) as client_session:
                await client_session.initialize()
                yield client_session


async def _read_json(asgi_app, raw_token: str, uri: str) -> dict[str, Any]:
    async with _session(asgi_app, raw_token) as session:
        result = await session.read_resource(AnyUrl(uri))
        text = result.contents[0].text  # type: ignore[union-attr]
    return json.loads(text)


# ---- fixtures shared across tests: seed both users ----
#
# NOTE: unlike test_identity_unit1.py's (a)-(d) tests (which use the synchronous
# Starlette TestClient, whose context-manager entry runs the ASGI lifespan and starts
# the streamable-HTTP session manager for free), a real multi-request MCP client
# session (`streamable_http_client` + `ClientSession`) needs the session manager's task
# group running explicitly — `httpx.ASGITransport` never sends ASGI lifespan events.
# Built by hand here (mirroring `build_asgi_app()`'s own construction) rather than
# calling `build_asgi_app()` so each test can enter `mcp.session_manager.run()` itself,
# the same pattern `test_identity_unit1.py`'s `TestTwoCallerIsolation` already
# established.


@pytest_asyncio.fixture
async def app_with_users(monkeypatch, token_store):
    factory, scope = token_store
    raw_a, raw_b = "mcp_userAtoken", "mcp_userBtoken"
    await _seed_token(factory, user_id=USER_A, raw_token=raw_a, label="A")
    await _seed_token(factory, user_id=USER_B, raw_token=raw_b, label="B")
    monkeypatch.setattr(AsyncSessionFactory, "session_scope", scope)

    mcp = build_mcp_server()
    inner_app = mcp.streamable_http_app()
    gated_app = MCPPathGate(inner_app, mcp_path=mcp.settings.streamable_http_path)
    yield mcp, gated_app, raw_a, raw_b


class TestResourcesList:
    async def test_lists_exactly_the_three_uris(self, app_with_users) -> None:
        mcp, asgi_app, raw_a, _raw_b = app_with_users
        async with mcp.session_manager.run():
            async with _session(asgi_app, raw_a) as session:
                result = await session.list_resources()

        uris = {str(r.uri) for r in result.resources}
        assert uris == {PROFILE_URI, COLLEAGUE_MODEL_URI, GITHUB_ISSUES_URI}
        assert len(result.resources) == 3


class TestProfileOwnerScoping:
    async def test_each_users_token_reads_only_their_own_profile(
        self, monkeypatch, app_with_users
    ) -> None:
        mcp, asgi_app, raw_a, raw_b = app_with_users
        seen_user_ids: list[uuid.UUID | None] = []

        async def _stub(session_id=None, user_id=None):
            seen_user_ids.append(user_id)
            if user_id == USER_A:
                return UserContext(
                    user_id=user_id,
                    organization="Org A",
                    projects=["project-a"],
                    priorities=["priority-a"],
                    projects_source="database",
                )
            return UserContext(
                user_id=user_id,
                organization="Org B",
                projects=["project-b"],
                priorities=["priority-b"],
                projects_source="config",
            )

        monkeypatch.setattr(user_context_service, "get_user_context", _stub)

        async with mcp.session_manager.run():
            payload_a = await _read_json(asgi_app, raw_a, PROFILE_URI)
            payload_b = await _read_json(asgi_app, raw_b, PROFILE_URI)

        assert payload_a == {
            "available": True,
            "organization": "Org A",
            "projects": ["project-a"],
            "projects_source": "database",
            "priorities": ["priority-a"],
        }
        assert payload_b["organization"] == "Org B"
        assert payload_a["organization"] != payload_b["organization"]
        # The user_id passed into the read matches the TOKEN's own owner — not a default,
        # not the other caller's id.
        assert seen_user_ids == [USER_A, USER_B]

    async def test_profile_read_failure_is_honest_empty_not_an_exception(
        self, monkeypatch, app_with_users
    ) -> None:
        """(c) The MCP protocol layer still succeeds (200/resource content returned);
        the failure is caught INSIDE the resource and surfaced as a structured payload."""
        mcp, asgi_app, raw_a, _raw_b = app_with_users

        async def _boom(session_id=None, user_id=None):
            raise RuntimeError("db unreachable")

        monkeypatch.setattr(user_context_service, "get_user_context", _boom)

        async with mcp.session_manager.run():
            payload = await _read_json(asgi_app, raw_a, PROFILE_URI)

        assert payload == {"available": False, "reason": "profile_read_failed"}


class TestColleagueModelOwnerScoping:
    async def test_each_users_token_reads_only_their_own_verified_inferences(
        self, monkeypatch, app_with_users
    ) -> None:
        mcp, asgi_app, raw_a, raw_b = app_with_users
        seen_user_ids: list[str] = []

        prefs_by_user = {
            str(USER_A): {
                "verified_inferences": {
                    "reminder_clear_verb:done": {
                        "value": "complete",
                        "source": "user_verified",
                        "confidence_at_verification": 0.9,
                        "verified_at": "2026-09-01T00:00:00+00:00",
                    }
                }
            },
            str(USER_B): {},  # nothing confirmed for B
        }

        async def _stub_load_preferences(user_id):
            seen_user_ids.append(str(user_id))
            return prefs_by_user.get(str(user_id), {})

        async def _stub_get_user_context(session_id=None, user_id=None):
            return UserContext(user_id=user_id, priorities=["priority-for-" + str(user_id)])

        import services.intent_service.collaboration_gate as collaboration_gate

        monkeypatch.setattr(collaboration_gate, "_load_preferences", _stub_load_preferences)
        monkeypatch.setattr(user_context_service, "get_user_context", _stub_get_user_context)

        async with mcp.session_manager.run():
            payload_a = await _read_json(asgi_app, raw_a, COLLEAGUE_MODEL_URI)
            payload_b = await _read_json(asgi_app, raw_b, COLLEAGUE_MODEL_URI)

        assert payload_a["verified"] == [
            {
                "key": "reminder_clear_verb:done",
                "value": "complete",
                "verified_at": "2026-09-01T00:00:00+00:00",
            }
        ]
        assert "note" not in payload_a
        assert payload_a["priorities"] == ["priority-for-" + str(USER_A)]

        # (d) nothing confirmed for B -> the honest-empty shape.
        assert payload_b["verified"] == []
        assert payload_b["note"] == "nothing confirmed yet"

        assert seen_user_ids == [str(USER_A), str(USER_B)]


class TestGithubIssuesResource:
    async def test_unbound_user_gets_connect_required_payload(
        self, monkeypatch, app_with_users
    ) -> None:
        mcp, asgi_app, raw_a, _raw_b = app_with_users

        async def _stub_unbound(self, user_id, *, limit=50, repository=None):
            return GitHubIssuesResult(
                degradation=DegradationResponse(
                    reason=DegradationReason.CONNECT_REQUIRED,
                    user_message="Connect GitHub to continue.",
                    action_hint="/api/v1/settings/integrations/github/connect",
                )
            )

        monkeypatch.setattr(GitHubMCPSpatialAdapter, "list_open_issues", _stub_unbound)

        async with mcp.session_manager.run():
            payload = await _read_json(asgi_app, raw_a, GITHUB_ISSUES_URI)

        assert payload == {
            "available": False,
            "connector": "github",
            "reason": "connect_required",
            "message": "Connect GitHub to continue.",
        }

    async def test_bound_user_gets_issues_with_count_and_cap(
        self, monkeypatch, app_with_users
    ) -> None:
        mcp, asgi_app, raw_a, raw_b = app_with_users
        issues_by_user = {
            str(USER_A): [{"number": 1, "title": "A's issue"}],
            str(USER_B): [{"number": 2, "title": "B's issue"}, {"number": 3, "title": "B's other"}],
        }
        seen_user_ids: list[str] = []

        async def _stub_bound(self, user_id, *, limit=50, repository=None):
            seen_user_ids.append(str(user_id))
            items = issues_by_user[str(user_id)]
            return GitHubIssuesResult(issues=items, total=len(items))

        monkeypatch.setattr(GitHubMCPSpatialAdapter, "list_open_issues", _stub_bound)

        async with mcp.session_manager.run():
            payload_a = await _read_json(asgi_app, raw_a, GITHUB_ISSUES_URI)
            payload_b = await _read_json(asgi_app, raw_b, GITHUB_ISSUES_URI)

        assert payload_a == {
            "available": True,
            "issues": [{"number": 1, "title": "A's issue"}],
            "count": 1,
            "capped_at": GITHUB_ISSUES_PAGE_CAP,
        }
        assert payload_b["count"] == 2
        assert payload_a["issues"] != payload_b["issues"]
        assert seen_user_ids == [str(USER_A), str(USER_B)]


class TestCapabilitiesStillResourcesOnly:
    """Complements unit 0's zero-resources version of this same check — now with unit 2's
    three resources actually registered, the capability SET (resources vs. tools/prompts)
    must still show resources-only; only the resource COUNT changes."""

    def test_advertised_capabilities_have_resources_not_tools_or_prompts(self) -> None:
        server = build_mcp_server()
        init_options = server._mcp_server.create_initialization_options()
        caps = init_options.capabilities

        assert caps.resources is not None
        assert caps.tools is None
        assert caps.prompts is None

    async def test_three_resources_are_registered(self) -> None:
        server = build_mcp_server()
        resources = await server.list_resources()

        assert {str(r.uri) for r in resources} == {
            PROFILE_URI,
            COLLEAGUE_MODEL_URI,
            GITHUB_ISSUES_URI,
        }
