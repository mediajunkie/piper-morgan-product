"""#1858 — an update of a NONEXISTENT issue is a definitive outcome, not an unverified one.

PM's live retest (2026-09-23) closed issue #99999 on purpose and got the unverified-write
copy ("may or may not have gone through — check the repository"). GitHub had answered 404
on both the write and the same-session read-back: the write provably never landed. This is
the #1824 bucket discipline applied to GitHub writes — NOT_FOUND is a definitive bucket;
the honest-uncertain copy belongs to timeouts/mid-flight failures, which keep it.

LAYER (m-43): the adapter's guard runs against a REAL in-memory MCP round-trip (the #1220
fixture pattern) whose fake server emits GitHub's real 404 error text; the router and the
floor's result-builder are unit-pinned by direct call. DENOMINATOR: both legs' evidence
required (write + read-back), update-shaped writes only, create/comment excluded.
"""

from __future__ import annotations

import contextlib
import json
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from mcp.server.fastmcp import FastMCP  # noqa: E402
from mcp.shared.memory import create_connected_server_and_client_session  # noqa: E402
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.connectors.binding_repository import ConnectorBindingRepository  # noqa: E402
from services.database.models import ConnectorBinding  # noqa: E402
from services.integrations.github.github_integration_router import (  # noqa: E402
    GitHubIntegrationRouter,
    GitHubIssueNotFound,
)
from services.mcp.consumer import github_adapter as gh_mod  # noqa: E402
from services.mcp.consumer.github_adapter import (  # noqa: E402
    GitHubMCPSpatialAdapter,
    GitHubWriteResult,
)
from services.mcp.consumer.mcp_client import MCPClient  # noqa: E402

pytestmark = pytest.mark.asyncio

_ALPHA = "11111111-1111-1111-1111-111111111111"
# The real github-mcp-server surfaces API errors as content text, verbatim-shaped:
_GH_404 = (
    "failed to update issue: PATCH https://api.github.com/repos/o/r/issues/99999: 404 Not Found []"
)
_GH_404_READ = (
    "failed to get issue: GET https://api.github.com/repos/o/r/issues/99999: 404 Not Found []"
)


@pytest_asyncio.fixture
async def sm(monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: ConnectorBinding.__table__.create(c, checkfirst=True))
    maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def _scope():
        async with maker() as s:
            yield s

    monkeypatch.setattr(gh_mod.AsyncSessionFactory, "session_scope", staticmethod(_scope))
    async with maker() as s:
        await ConnectorBindingRepository(s).upsert(
            _ALPHA, "github", status="bound", mcp_server_ref="http://srv/mcp"
        )
        await s.commit()
    yield maker
    await engine.dispose()


def _fixture(adapter, *, read_finds_it=False, write_404=True):
    """Fake server: issue 7 exists; anything else 404s on write. Read-back 404s unless
    ``read_finds_it`` (the pathological write-404-but-read-ok case)."""
    server = FastMCP("github-404-fixture")
    existing = {7: {"number": 7, "title": "t", "state": "open", "html_url": "u"}}

    @server.tool(name="issue_write")
    def issue_write(
        method: str,
        owner: str,
        repo: str,
        title: str = None,
        body: str = None,
        issue_number: int = None,
        state: str = None,
        labels: list = None,
        assignees: list = None,
    ) -> str:
        if method == "create":
            return _GH_404 if write_404 else json.dumps({"number": 8, "html_url": "u"})
        if issue_number in existing:
            if title is not None:
                existing[issue_number]["title"] = title
            if state is not None:
                existing[issue_number]["state"] = state
            return json.dumps(existing[issue_number])
        return _GH_404

    @server.tool(name="issue_read")
    def issue_read(method: str, owner: str, repo: str, issue_number: int) -> str:
        if issue_number in existing:
            return json.dumps(existing[issue_number])
        if read_finds_it:
            return json.dumps({"number": issue_number, "title": "ghost", "state": "open"})
        return _GH_404_READ

    @contextlib.asynccontextmanager
    async def _ctx(binding):
        async with create_connected_server_and_client_session(server) as session:
            yield MCPClient(session)

    adapter._mcp_client_ctx = _ctx


class TestAdapterDefinitiveNotFound:
    async def test_update_of_nonexistent_issue_is_definitive(self, sm):
        """THE #1858 pin: both legs say 404 on an update → not_found, never 'may have landed'."""
        adapter = GitHubMCPSpatialAdapter()
        _fixture(adapter)
        wr = await adapter.update_issue_connector(
            _ALPHA, owner="o", repo="r", issue_number=99999, state="closed"
        )
        assert wr.not_found is True
        assert wr.verified is False and wr.attempted is True
        assert wr.issue_number == 99999

    async def test_write_404_but_readback_finds_it_is_not_definitive(self, sm):
        """One leg is not evidence: if the read-back parses to an issue, stay honest-uncertain."""
        adapter = GitHubMCPSpatialAdapter()
        _fixture(adapter, read_finds_it=True)
        wr = await adapter.update_issue_connector(
            _ALPHA, owner="o", repo="r", issue_number=99999, state="closed"
        )
        assert wr.not_found is False

    async def test_existing_issue_update_still_verifies(self, sm):
        adapter = GitHubMCPSpatialAdapter()
        _fixture(adapter)
        wr = await adapter.update_issue_connector(
            _ALPHA, owner="o", repo="r", issue_number=7, state="closed"
        )
        assert wr.verified is True and wr.not_found is False

    async def test_create_never_claims_not_found(self, sm):
        """Create-shaped writes have no pre-existing artifact — the bucket is update-only."""
        adapter = GitHubMCPSpatialAdapter()
        _fixture(adapter, write_404=True)
        wr = await adapter.create_issue_connector(_ALPHA, owner="o", repo="r", title="t", body="b")
        assert wr.not_found is False

    def test_not_found_text_is_narrow(self):
        f = GitHubMCPSpatialAdapter._is_not_found_text
        assert f(_GH_404) and f('{"message": "Not Found", "status": "404"}')
        assert not f("failed to update issue: 403 Forbidden")
        assert not f("rate limit exceeded")
        assert not f(None) and not f("")


class TestRouterTypedOutcome:
    async def test_not_found_result_raises_typed_error_with_location(self):
        router = GitHubIntegrationRouter.__new__(GitHubIntegrationRouter)
        router._user_id = _ALPHA
        router.mcp_adapter = MagicMock()
        router.mcp_adapter.update_issue_connector = AsyncMock(
            return_value=GitHubWriteResult(
                verified=False, attempted=True, not_found=True, issue_number=99999
            )
        )
        with pytest.raises(GitHubIssueNotFound) as ei:
            await router._try_connector_write(
                "update_issue_connector", owner="o", repo="r", issue_number=99999
            )
        assert ei.value.issue_number == 99999 and ei.value.owner == "o" and ei.value.repo == "r"
        assert "does not exist" in str(ei.value)

    async def test_unverified_result_still_raises_the_uncertain_error(self):
        router = GitHubIntegrationRouter.__new__(GitHubIntegrationRouter)
        router._user_id = _ALPHA
        router.mcp_adapter = MagicMock()
        router.mcp_adapter.update_issue_connector = AsyncMock(
            return_value=GitHubWriteResult(verified=False, attempted=True, issue_number=5)
        )
        with pytest.raises(RuntimeError) as ei:
            await router._try_connector_write("update_issue_connector", owner="o", repo="r")
        assert not isinstance(ei.value, GitHubIssueNotFound)
        assert "may or may not have landed" in str(ei.value)


class TestFloorCopyBuckets:
    def _svc_and_intent(self):
        from services.domain.models import Intent
        from services.intent.intent_service import IntentService
        from services.shared_types import IntentCategory

        svc = IntentService.__new__(IntentService)
        intent = Intent(category=IntentCategory.EXECUTION, action="update_issue", confidence=1.0)
        return svc, intent

    def test_not_found_gets_the_definitive_sentence(self):
        svc, intent = self._svc_and_intent()
        e = GitHubIssueNotFound(issue_number=99999, owner="o", repo="r")
        res = svc._unverified_write_result(e, intent, "wf")
        assert res is not None
        assert "no issue #99999 in o/r" in res.message
        assert "nothing was changed" in res.message
        assert "may or may not" not in res.message and "duplicate" not in res.message

    def test_unverified_keeps_the_honest_uncertain_sentence(self):
        svc, intent = self._svc_and_intent()
        e = RuntimeError("GitHub write could not be verified — it may or may not have landed.")
        res = svc._unverified_write_result(e, intent, "wf")
        assert res is not None and "may or may not" in res.message and "duplicate" in res.message

    def test_unrelated_error_is_not_claimed(self):
        svc, intent = self._svc_and_intent()
        assert svc._unverified_write_result(ValueError("x"), intent, "wf") is None
