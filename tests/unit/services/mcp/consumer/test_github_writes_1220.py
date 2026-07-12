"""#1220 — write-path cutover onto the per-user OAuth grant, with the #1322 guard.

The deterministic action-success guard (ruled 2026-07-01): a write is VERIFIED
only when a read-back through the same connector session confirms the artifact
in its expected state — never from the write response alone. These tests run
the guard against a REAL in-memory MCP round-trip (FastMCP, the #1322 fixture
pattern) with a stateful fake repo, so create→readback genuinely round-trips
and each failure mode is produced by breaking the repo, not by mocking the
guard's own logic. Also: the double-write hazard matrix (attempted flag) and
the router's connector-first / safe-fallback-only behavior.
"""

from __future__ import annotations

import contextlib
import json

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from mcp.server.fastmcp import FastMCP  # noqa: E402
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from mcp.shared.memory import create_connected_server_and_client_session  # noqa: E402

from services.connectors.binding_repository import ConnectorBindingRepository  # noqa: E402
from services.database.models import ConnectorBinding  # noqa: E402
from services.mcp.consumer import github_adapter as gh_mod  # noqa: E402
from services.mcp.consumer.connector import DegradationReason  # noqa: E402
from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter  # noqa: E402
from services.mcp.consumer.mcp_client import MCPClient  # noqa: E402

pytestmark = pytest.mark.asyncio

_ALPHA = "11111111-1111-1111-1111-111111111111"


@pytest_asyncio.fixture
async def sm(monkeypatch):
    """In-memory ConnectorBinding store (the #1322 fixture pattern)."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: ConnectorBinding.__table__.create(c, checkfirst=True))
    maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def _scope():
        async with maker() as s:
            yield s

    monkeypatch.setattr(gh_mod.AsyncSessionFactory, "session_scope", staticmethod(_scope))
    yield maker
    await engine.dispose()


async def _seed_bound(maker):
    async with maker() as s:
        await ConnectorBindingRepository(s).upsert(
            _ALPHA, "github", status="bound", mcp_server_ref="http://srv/mcp"
        )
        await s.commit()


def _writable_fixture(adapter, *, break_readback=False, comment_without_id=False, raises=False):
    """A stateful fake github-mcp-server: create/update/comment/get over one repo."""
    server = FastMCP("github-write-fixture")
    issues: dict[int, dict] = {}
    counter = {"n": 100}

    # Mirrors the REAL github-mcp-server >= v1.2.0 consolidated contract
    # ("Promote issue fields and deprecate legacy issue write tool"):
    # issue_write(method=create|update), issue_read(method=get),
    # add_issue_comment unchanged. The legacy names (create_issue/update_issue/
    # get_issue) deliberately DO NOT EXIST here — calling them must fail the
    # same way the pinned v1.5.0 image fails, which is exactly what broke the
    # live first-real-write on 2026-07-09 while this fixture still modeled the
    # old dialect and kept the tests green. The fixture drifting from the
    # pinned image's contract is the failure mode this comment guards.
    @server.tool(name="issue_write")
    def issue_write(method: str, owner: str, repo: str, title: str = None,
                    body: str = None, issue_number: int = None,
                    state: str = None, labels: list = None,
                    assignees: list = None) -> str:
        if method == "create":
            counter["n"] += 1
            n = counter["n"]
            issues[n] = {"number": n, "title": title, "body": body or "",
                         "state": "open",
                         "html_url": f"https://github.com/{owner}/{repo}/issues/{n}"}
            # REAL v1.5.0 behavior (live-observed 2026-07-09): the write response
            # is a MINIMAL envelope — id + url, NO number field. The guard must
            # derive the number from the URL and verify via issue_read.
            return json.dumps(
                {"id": str(4850000000 + n),
                 "url": f"https://github.com/{owner}/{repo}/issues/{n}"}
            )
        if method == "update":
            it = issues.get(issue_number, {"number": issue_number, "html_url": ""})
            if title is not None:
                it["title"] = title
            if state is not None:
                it["state"] = state
            issues[issue_number] = it
            return json.dumps(it)
        raise ValueError(f"unknown method: {method}")

    @server.tool(name="add_issue_comment")
    def add_issue_comment(owner: str, repo: str, issue_number: int, body: str = "") -> str:
        if comment_without_id:
            return json.dumps({"body": body})  # pathological: no GitHub-minted id
        return json.dumps({"id": 9001, "body": body})

    @server.tool(name="issue_read")
    def issue_read(method: str, owner: str, repo: str, issue_number: int) -> str:
        if method != "get":
            raise ValueError(f"unknown method: {method}")
        if break_readback:
            return json.dumps({})  # repo "lost" the issue — readback must fail the guard
        it = issues.get(issue_number)
        if it:
            # REAL v1.5.0 behavior (live-observed 2026-07-12, #1386-B2): the READ
            # path HTML-entity-escapes text fields while the write stores raw —
            # `Let's` reads back as `Let&#39;s`. The guard must entity-normalize
            # or every apostrophe'd title reads as a verify mismatch.
            import html as _html

            it = {k: (_html.escape(v, quote=False) if isinstance(v, str) and k in ("title", "body") else v)
                  for k, v in it.items()}
        return json.dumps(it if it else {})

    @contextlib.asynccontextmanager
    async def _ctx(binding):
        if raises:
            raise RuntimeError("server exploded mid-flight")
        async with create_connected_server_and_client_session(server) as session:
            yield MCPClient(session)

    adapter._mcp_client_ctx = _ctx
    return issues


class TestVerifiedCreate:
    async def test_create_verified_via_real_readback(self, sm):
        await _seed_bound(sm)
        adapter = GitHubMCPSpatialAdapter()
        _writable_fixture(adapter)
        wr = await adapter.create_issue_connector(
            _ALPHA, owner="o", repo="r", title="The title", body="b"
        )
        assert wr.verified is True and wr.attempted is True
        assert wr.issue_number == 101
        assert wr.url.endswith("/issues/101")
        assert wr.raw["title"] == "The title"

    async def test_create_readback_miss_is_unverified_not_success(self, sm):
        """The guard's whole point: write 'succeeded' but readback can't find
        it → verified=False (honest-uncertain), never a confident ✓."""
        await _seed_bound(sm)
        adapter = GitHubMCPSpatialAdapter()
        _writable_fixture(adapter, break_readback=True)
        wr = await adapter.create_issue_connector(
            _ALPHA, owner="o", repo="r", title="t", body="b"
        )
        assert wr.verified is False and wr.attempted is True

    async def test_no_binding_never_fires_attempted_false(self, sm):
        adapter = GitHubMCPSpatialAdapter()
        _writable_fixture(adapter)
        wr = await adapter.create_issue_connector(
            _ALPHA, owner="o", repo="r", title="t", body="b"
        )
        assert wr.attempted is False  # the ONLY safe-native-fallback state
        assert wr.degradation.reason is DegradationReason.CONNECT_REQUIRED

    async def test_midflight_failure_attempted_true_no_fallback_license(self, sm):
        await _seed_bound(sm)
        adapter = GitHubMCPSpatialAdapter()
        _writable_fixture(adapter, raises=True)
        wr = await adapter.create_issue_connector(
            _ALPHA, owner="o", repo="r", title="t", body="b"
        )
        assert wr.attempted is True  # may have landed — double-write forbidden
        assert wr.degradation.reason is DegradationReason.UNREACHABLE


class TestEntityEscapedReadback:
    async def test_apostrophe_title_still_verifies(self, sm):
        """#1386-B2 live: sidecar read escapes `'` → `&#39;`; a successful
        write with an apostrophe'd title must still verify=True."""
        await _seed_bound(sm)
        adapter = GitHubMCPSpatialAdapter()
        _writable_fixture(adapter)
        wr = await adapter.create_issue_connector(
            _ALPHA, owner="o", repo="r",
            title="Let's add search & filters", body="it's needed",
        )
        assert wr.verified is True


class TestVerifiedUpdate:
    async def test_update_state_verified_by_readback(self, sm):
        await _seed_bound(sm)
        adapter = GitHubMCPSpatialAdapter()
        issues = _writable_fixture(adapter)
        issues[7] = {"number": 7, "title": "x", "state": "open", "html_url": "u"}
        wr = await adapter.update_issue_connector(
            _ALPHA, owner="o", repo="r", issue_number=7, state="closed"
        )
        assert wr.verified is True
        assert wr.raw["state"] == "closed"


class TestVerifiedComment:
    async def test_comment_with_minted_id_verifies(self, sm):
        await _seed_bound(sm)
        adapter = GitHubMCPSpatialAdapter()
        issues = _writable_fixture(adapter)
        issues[7] = {"number": 7, "title": "x", "state": "open", "html_url": "u"}
        wr = await adapter.add_comment_connector(
            _ALPHA, owner="o", repo="r", issue_number=7, comment="hello"
        )
        assert wr.verified is True

    async def test_comment_without_minted_id_is_unverified(self, sm):
        """Issue-existence alone must NOT verify a comment — the response has
        to carry the GitHub-minted comment id."""
        await _seed_bound(sm)
        adapter = GitHubMCPSpatialAdapter()
        issues = _writable_fixture(adapter, comment_without_id=True)
        issues[7] = {"number": 7, "title": "x", "state": "open", "html_url": "u"}
        wr = await adapter.add_comment_connector(
            _ALPHA, owner="o", repo="r", issue_number=7, comment="hello"
        )
        assert wr.verified is False and wr.attempted is True


class TestRouterCutoverMatrix:
    """The router: verified → raw dict; never-fired → native fallback;
    fired-unverified → RuntimeError (no double-write, no fake ✓)."""

    def _router_with(self, wr):
        from unittest.mock import AsyncMock, MagicMock

        from services.integrations.github.github_integration_router import (
            GitHubIntegrationRouter,
        )

        r = GitHubIntegrationRouter()
        r._user_id = _ALPHA
        r.mcp_adapter = MagicMock()
        r.mcp_adapter.create_issue_connector = AsyncMock(return_value=wr)
        native = MagicMock()
        native.create_issue = AsyncMock(return_value={"number": 1, "native": True})
        r._get_integration = MagicMock(return_value=native)
        return r, native

    async def test_verified_returns_connector_raw_no_native_call(self):
        from services.mcp.consumer.github_adapter import GitHubWriteResult

        wr = GitHubWriteResult(verified=True, attempted=True, issue_number=5,
                               url="u", raw={"number": 5, "via": "connector"})
        r, native = self._router_with(wr)
        out = await r.create_issue("t", "b", owner="o", repo_name="r")
        assert out == {"number": 5, "via": "connector"}
        native.create_issue.assert_not_awaited()

    async def test_never_fired_falls_back_to_native(self):
        from services.mcp.consumer.github_adapter import GitHubWriteResult

        wr = GitHubWriteResult(verified=False, attempted=False)
        r, native = self._router_with(wr)
        out = await r.create_issue("t", "b", owner="o", repo_name="r")
        assert out == {"number": 1, "native": True}
        native.create_issue.assert_awaited_once()

    async def test_fired_unverified_raises_never_double_writes(self):
        from services.mcp.consumer.github_adapter import GitHubWriteResult

        wr = GitHubWriteResult(verified=False, attempted=True)
        r, native = self._router_with(wr)
        with pytest.raises(RuntimeError, match="may or may not have"):
            await r.create_issue("t", "b", owner="o", repo_name="r")
        native.create_issue.assert_not_awaited()

    async def test_no_user_id_goes_straight_native(self):
        from unittest.mock import AsyncMock, MagicMock

        from services.integrations.github.github_integration_router import (
            GitHubIntegrationRouter,
        )

        r = GitHubIntegrationRouter()
        r._user_id = None
        native = MagicMock()
        native.create_issue = AsyncMock(return_value={"native": True})
        r._get_integration = MagicMock(return_value=native)
        out = await r.create_issue("t", "b", owner="o", repo_name="r")
        assert out == {"native": True}


class TestToolContractDrift:
    async def test_legacy_tool_names_against_current_server_are_unverified_not_success(self, sm):
        """The 2026-07-09 live failure, pinned as a regression: an adapter speaking
        the deprecated dialect (create_issue) against the consolidated server must
        come back fired-but-unverified — NEVER a false success, and NEVER the
        attempted=False state that would license a PAT-fallback double-write."""
        from unittest.mock import patch

        await _seed_bound(sm)
        adapter = GitHubMCPSpatialAdapter()
        issues = _writable_fixture(adapter)
        with patch.object(adapter, "_CREATE_ISSUE_TOOL", "create_issue"):
            wr = await adapter.create_issue_connector(
                _ALPHA, owner="o", repo="r", title="drift", body="b"
            )
        assert wr.verified is False
        assert wr.attempted is True
        assert not issues, "no issue may exist after an unknown-tool call"
