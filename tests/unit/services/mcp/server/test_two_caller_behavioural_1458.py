"""#1458 — behavioural proof: two real callers, interleaved, see only their own data
across all three MCP resources AND the composite tool.

This is the test Arch's rescoped ruling (2026-10-05) asked for directly: "two tokens for
two real users, interleaved requests across all three resources (and the tool), each
sees only its own data. That's the test that would catch a regression nobody traces by
hand next time." It is deliberately a different LAYER (m-43) from
``test_identity_enforcement_1458.py`` (static/AST, build-time contract) and from
``test_resources_unit2.py`` (per-resource, sequential A-then-B) — THIS file is the one
that would actually fail if a future change ever let one caller's request observe
another caller's in-flight state.

TRACE NOTES (#1458 deliverable 3 — written findings, not asserted by this file's tests,
since they are source-level traces rather than runtime behaviour; see the #1458 PR report
for the exact commands run):

- ``user_context_service.get_user_context`` — already traced clean by Arch (2026-10-05
  ruling): process-local dict cache keyed ``user:{user_id}`` (``services/user_context_
  service.py``, cache_key line), one entry per caller.
- ``collaboration_gate._load_preferences`` (the #1510 verified-inference store this
  file's colleague-model stub exercises) — traced here: reads ``users.preferences`` via
  ``select(User.preferences).where(User.id == str(user_id))`` (``services/intent_
  service/collaboration_gate.py:317-327``) — a single-row, user_id-filtered DB query,
  no process-local cache at all. Clean by construction, not by luck.
- ``GitHubMCPSpatialAdapter().list_open_issues`` — traced here: ``resources.py``
  instantiates a FRESH ``GitHubMCPSpatialAdapter()`` on every call (resources.py:171),
  so the instance's own dicts (``_issue_to_position`` etc., used by ``resolve()``, never
  by ``list_open_issues``) can't carry state between callers even in principle. The read
  itself (``_search_via_connector`` -> ``github_adapter.py:698-728``) looks up the
  caller's OWN ``ConnectorBindingRepository`` row and ``ConnectorGrantStore`` grant by
  ``user_id`` (``github_adapter.py:1044``, keyed ``binding.owner_id``) on every call — no
  cache, no shared dict, nothing keyed any other way.
- Redis: none of the three reads above touch Redis. ``grep -rniI "redis"
  services/mcp/ services/intent_service/collaboration_gate.py services/intent_service/
  verified_inference.py services/user_context_service.py`` has exactly ONE hit in that
  whole surface — a comment in ``services/mcp/consumer/github_oauth_handler.py`` ("Redis/
  DB later") describing unbuilt future work, in the OAuth-CONNECT flow, which none of
  the three reads or the composite tool ever calls. Denominator: every module these three
  reads import, transitively, down to ``AsyncSessionFactory``/``ConnectorBindingRepository``/
  ``ConnectorGrantStore``/``MCPClient``/``server_ref_resolver`` — none of those import
  ``redis`` either (checked directly, zero hits).

LAYER: real MCP client (``mcp.client.streamable_http`` + ``ClientSession``) over an
in-process ASGI transport, round-tripping ``initialize`` + ``resources/read`` /
``tools/call`` — the same client-side protocol surface a real tester's client speaks.
The app under test is built the same way ``services.mcp.server.app.build_asgi_app()``
builds it (bearer auth -> :class:`~services.mcp.server.rate_limit.MCPRateLimitMiddleware`
-> :class:`~services.mcp.server.app.MCPPathGate`) — constructed inline here rather than
via a literal ``build_asgi_app()`` call ONLY because this test needs ``mcp.session_
manager.run()`` directly (``httpx.ASGITransport`` never sends ASGI lifespan events, so
the session manager needs to be entered by hand — the same reason ``test_resources_
unit2.py`` already builds this way instead of calling ``build_asgi_app()``). The
structural-equivalence test below pins that this inline construction is not a stand-in
that could silently drift from the real factory.

DENOMINATOR: the three resources + the one composite tool, two identities, interleaved.
Not: concurrent/simultaneous requests (asyncio task concurrency) — this proves SEQUENTIAL
interleaving (A, B, B, A, ...) never leaks, which is what a contextvar-reset bug would
actually produce; true simultaneous-request isolation is a separate, harder claim this
file does not make.
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
from services.mcp.consumer.github_adapter import (  # noqa: E402
    GitHubIssuesResult,
    GitHubMCPSpatialAdapter,
)
from services.mcp.server.app import MCPPathGate, build_asgi_app, build_mcp_server  # noqa: E402
from services.mcp.server.rate_limit import MCPRateLimitMiddleware  # noqa: E402
from services.mcp.server.resources import (  # noqa: E402
    COLLEAGUE_MODEL_URI,
    GITHUB_ISSUES_URI,
    PROFILE_URI,
    WHAT_PIPER_KNOWS_TOOL,
)
from services.user_context_service import UserContext, user_context_service  # noqa: E402

MCP_PATH = "/mcp"
LOCAL_BASE_URL = "http://localhost:8080"

USER_A = uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
USER_B = uuid.UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")


@pytest.fixture(autouse=True)
def _reset_sse_starlette_loop_singleton():
    """Same fresh-per-test singleton reset as test_identity_unit1.py / test_resources_unit2.py."""
    _sse_starlette_sse.AppStatus.should_exit = False
    _sse_starlette_sse.AppStatus.should_exit_event = None
    yield


def _hash(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@pytest_asyncio.fixture
async def token_store():
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
                id=uuid.uuid4(), user_id=user_id, token_hash=_hash(raw_token), label=label
            )
        )
        await session.commit()


@asynccontextmanager
async def _client_session(asgi_app, raw_token: str):
    """A fresh real MCP client session for ONE round of calls — opened and
    torn down per use, so each call in the interleaving below is a genuinely
    separate request/session, not one long-lived connection that happens to
    carry the right identity throughout."""
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
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                yield session


async def _read_resource(asgi_app, raw_token: str, uri: str) -> dict[str, Any]:
    async with _client_session(asgi_app, raw_token) as session:
        result = await session.read_resource(AnyUrl(uri))
        text = result.contents[0].text  # type: ignore[union-attr]
    return json.loads(text)


async def _call_tool(asgi_app, raw_token: str, name: str) -> dict[str, Any]:
    async with _client_session(asgi_app, raw_token) as session:
        result = await session.call_tool(name, {})
        assert not result.isError, f"tool call {name!r} returned isError: {result.content}"
        text = result.content[0].text  # type: ignore[union-attr]
    return json.loads(text)


@pytest_asyncio.fixture
async def app_with_users(monkeypatch, token_store):
    """Built the same way ``build_asgi_app()`` builds it (see module docstring
    for why this is inline rather than a literal call): bearer auth ->
    :class:`MCPRateLimitMiddleware` -> :class:`MCPPathGate`."""
    factory, scope = token_store
    raw_a, raw_b = "mcp_behaviouralUserA", "mcp_behaviouralUserB"
    await _seed_token(factory, user_id=USER_A, raw_token=raw_a, label="A")
    await _seed_token(factory, user_id=USER_B, raw_token=raw_b, label="B")
    monkeypatch.setattr(AsyncSessionFactory, "session_scope", scope)

    mcp = build_mcp_server()
    inner_app = mcp.streamable_http_app()
    mcp_path = mcp.settings.streamable_http_path
    rate_limited = MCPRateLimitMiddleware(inner_app, mcp_path=mcp_path)
    gated_app = MCPPathGate(rate_limited, mcp_path=mcp_path)
    yield mcp, gated_app, raw_a, raw_b


class TestInlineConstructionMatchesTheRealFactory:
    """Structural pin: the hand-built app above is not a stand-in that could
    silently drift from what ``build_asgi_app()`` actually ships."""

    def test_build_asgi_app_returns_the_same_middleware_chain_shape(self) -> None:
        app = build_asgi_app()
        assert isinstance(app, MCPPathGate)
        assert isinstance(app._app, MCPRateLimitMiddleware)


class TestTwoCallersInterleavedAcrossAllThreeResourcesAndTheTool:
    """The load-bearing proof. Per-user data is monkeypatched into the three
    underlying stores, keyed by the user_id EACH call actually receives (not
    by call order), and the calls are deliberately interleaved
    (A, B, B, A, A, B, B, A) rather than grouped per-caller."""

    async def test_each_caller_sees_only_its_own_data_under_interleaving(
        self, monkeypatch, app_with_users
    ) -> None:
        mcp, asgi_app, raw_a, raw_b = app_with_users

        profile_by_user = {
            USER_A: UserContext(
                user_id=USER_A,
                organization="Org-A",
                projects=["proj-A"],
                priorities=["priority-A"],
                projects_source="database",
            ),
            USER_B: UserContext(
                user_id=USER_B,
                organization="Org-B",
                projects=["proj-B"],
                priorities=["priority-B"],
                projects_source="config",
            ),
        }
        colleague_prefs_by_user = {
            str(USER_A): {
                "verified_inferences": {
                    "pref_a": {
                        "value": "A-only-value",
                        "verified_at": "2026-09-01T00:00:00+00:00",
                    }
                }
            },
            str(USER_B): {
                "verified_inferences": {
                    "pref_b": {
                        "value": "B-only-value",
                        "verified_at": "2026-09-02T00:00:00+00:00",
                    }
                }
            },
        }
        issues_by_user = {
            str(USER_A): [{"number": 101, "title": "A's issue"}],
            str(USER_B): [
                {"number": 202, "title": "B's issue"},
                {"number": 203, "title": "B's other"},
            ],
        }

        profile_calls: list[uuid.UUID] = []
        colleague_calls: list[str] = []
        github_calls: list[str] = []

        async def _stub_get_user_context(session_id=None, user_id=None):
            profile_calls.append(user_id)
            return profile_by_user[user_id]

        async def _stub_load_preferences(user_id):
            colleague_calls.append(str(user_id))
            return colleague_prefs_by_user[str(user_id)]

        async def _stub_list_open_issues(self, user_id, *, limit=50, repository=None):
            github_calls.append(str(user_id))
            items = issues_by_user[str(user_id)]
            return GitHubIssuesResult(issues=items, total=len(items))

        import services.intent_service.collaboration_gate as collaboration_gate

        monkeypatch.setattr(user_context_service, "get_user_context", _stub_get_user_context)
        monkeypatch.setattr(collaboration_gate, "_load_preferences", _stub_load_preferences)
        monkeypatch.setattr(GitHubMCPSpatialAdapter, "list_open_issues", _stub_list_open_issues)

        results: dict[str, dict[str, Any]] = {}

        async with mcp.session_manager.run():
            # Deliberately interleaved, not grouped per caller.
            results["A.profile.1"] = await _read_resource(asgi_app, raw_a, PROFILE_URI)
            results["B.profile.1"] = await _read_resource(asgi_app, raw_b, PROFILE_URI)
            results["B.colleague"] = await _read_resource(asgi_app, raw_b, COLLEAGUE_MODEL_URI)
            results["A.colleague"] = await _read_resource(asgi_app, raw_a, COLLEAGUE_MODEL_URI)
            results["A.github"] = await _read_resource(asgi_app, raw_a, GITHUB_ISSUES_URI)
            results["B.github"] = await _read_resource(asgi_app, raw_b, GITHUB_ISSUES_URI)
            results["B.tool"] = await _call_tool(asgi_app, raw_b, WHAT_PIPER_KNOWS_TOOL)
            results["A.tool"] = await _call_tool(asgi_app, raw_a, WHAT_PIPER_KNOWS_TOOL)
            # Re-read A's profile LAST, after every B call, to catch any
            # staleness/leakage from the intervening requests.
            results["A.profile.2"] = await _read_resource(asgi_app, raw_a, PROFILE_URI)

        print("\n#1458 two-caller interleaved behavioural proof:")
        for label, payload in results.items():
            print(f"  {label}: {payload}")

        # ---- profile ----
        assert results["A.profile.1"]["organization"] == "Org-A"
        assert results["A.profile.2"]["organization"] == "Org-A"
        assert results["B.profile.1"]["organization"] == "Org-B"
        assert results["A.profile.1"] != results["B.profile.1"]

        # ---- colleague-model ----
        assert results["A.colleague"]["verified"] == [
            {"key": "pref_a", "value": "A-only-value", "verified_at": "2026-09-01T00:00:00+00:00"}
        ]
        assert results["B.colleague"]["verified"] == [
            {"key": "pref_b", "value": "B-only-value", "verified_at": "2026-09-02T00:00:00+00:00"}
        ]
        assert results["A.colleague"] != results["B.colleague"]

        # ---- github issues ----
        assert results["A.github"]["issues"] == [{"number": 101, "title": "A's issue"}]
        assert results["B.github"]["issues"] == [
            {"number": 202, "title": "B's issue"},
            {"number": 203, "title": "B's other"},
        ]
        assert results["A.github"] != results["B.github"]

        # ---- composite tool: must reflect the SAME per-caller data, via the
        # SAME three reads, for the caller the tool call was actually made as ----
        assert results["A.tool"]["profile"]["organization"] == "Org-A"
        assert results["A.tool"]["colleague_model"]["verified"] == [
            {"key": "pref_a", "value": "A-only-value", "verified_at": "2026-09-01T00:00:00+00:00"}
        ]
        assert results["A.tool"]["github_issues"]["issues"] == [
            {"number": 101, "title": "A's issue"}
        ]

        assert results["B.tool"]["profile"]["organization"] == "Org-B"
        assert results["B.tool"]["colleague_model"]["verified"] == [
            {"key": "pref_b", "value": "B-only-value", "verified_at": "2026-09-02T00:00:00+00:00"}
        ]
        assert results["B.tool"]["github_issues"]["issues"] == [
            {"number": 202, "title": "B's issue"},
            {"number": 203, "title": "B's other"},
        ]
        assert results["A.tool"] != results["B.tool"]

        # ---- the underlying stores were each called with the ACTUAL caller's own
        # user_id, never the other caller's or a default. profile_calls is not
        # asserted by exact order/count here: _read_colleague_model ALSO calls
        # get_user_context internally (for priorities), so its call count is a
        # function of resources.py's own internal composition, not this test's
        # interleaving order — re-deriving that count by hand is exactly the kind
        # of brittle, easy-to-get-wrong assertion this suite avoids. The dict-keyed
        # stub (`profile_by_user[user_id]`) already raises KeyError on any id other
        # than USER_A/USER_B, and the payload assertions above already prove each
        # caller got its OWN data — this is enough to prove no cross-caller leak.
        assert set(profile_calls) == {USER_A, USER_B}
        assert colleague_calls == [str(USER_B), str(USER_A), str(USER_B), str(USER_A)]
        assert github_calls == [str(USER_A), str(USER_B), str(USER_B), str(USER_A)]
