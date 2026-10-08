"""#1959 — ``GitHubMCPSpatialAdapter.probe_issue_connector``: a tri-state
existence probe ("found" / "not_found" / "unknown") for the close/reopen
#1190 resolve-first gate, built after Lead review found the gate's first
version (commit 81bc120df1) read via the WRONG path for alpha's
OAuth-connected users (``GitHubIntegrationRouter.get_issue`` — a
separately-configured PAT session, not the connector) and treated a clean
``None`` as definitive not-found even though that same ``None`` also covers
401/403/network failures.

This probe must NEVER collapse "could not confirm" into "confirmed
not-found" — the same #1858/#1941 honesty class the write-verification path
(``test_github_write_not_found_1858.py``) already pins, applied here to a
plain READ instead of a write's readback leg.

LAYER (m-43): a REAL in-memory MCP round-trip (the #1220/#1858 fixture
pattern) whose fake server emits GitHub's real content-text and
JSON-RPC-error 404 shapes, plus a fake binding-repository DB (sqlite
in-memory) for the degradation legs. Nothing here mocks the probe's own
classification logic — only the transport/DB boundaries it reads through.
"""

from __future__ import annotations

import contextlib
import json

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from mcp.server.fastmcp import FastMCP  # noqa: E402
from mcp.shared.exceptions import McpError  # noqa: E402
from mcp.shared.memory import create_connected_server_and_client_session  # noqa: E402
from mcp.types import ErrorData  # noqa: E402
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.connectors.binding_repository import ConnectorBindingRepository  # noqa: E402
from services.database.models import ConnectorBinding  # noqa: E402
from services.mcp.consumer import github_adapter as gh_mod  # noqa: E402
from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter  # noqa: E402
from services.mcp.consumer.mcp_client import MCPClient  # noqa: E402

pytestmark = pytest.mark.asyncio

_ALPHA = "11111111-1111-1111-1111-111111111111"

# The real github-mcp-server's content-text 404 shape (same literal the
# #1858 write-verification tests pin).
_GH_404_TEXT = (
    "failed to get issue: GET https://api.github.com/repos/o/r/issues/99999: 404 Not Found []"
)
_GH_404_JSON = json.dumps(
    {
        "message": "Not Found",
        "documentation_url": "https://docs.github.com/rest/issues/issues#get-an-issue",
        "status": "404",
    }
)
_AUTH_ERROR_TEXT = (
    "failed to get issue: GET https://api.github.com/repos/o/r/issues/99999: 401 Unauthorized []"
)
_RATE_LIMIT_TEXT = "failed to get issue: GET https://api.github.com/repos/o/r/issues/99999: 403 Forbidden (rate limit exceeded) []"


@pytest_asyncio.fixture
async def sm(monkeypatch):
    """A real sqlite-backed ConnectorBindingRepository, same shape as the
    #1858 fixture — the probe's ``_bound_binding_or_degrade`` leg reads
    through this, not a mock."""
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


async def _bind(maker, *, status="bound"):
    async with maker() as s:
        await ConnectorBindingRepository(s).upsert(
            _ALPHA, "github", status=status, mcp_server_ref="http://srv/mcp"
        )
        await s.commit()


def _wire_fake_server(adapter, *, issue_read_returns=None, issue_read_raises=None):
    """Patch ``adapter._mcp_client_ctx`` to a real in-memory MCP session
    backed by a fake ``issue_read`` tool. Exactly one of
    ``issue_read_returns`` (content-text return) / ``issue_read_raises`` (an
    exception the tool call raises) is supplied."""
    server = FastMCP("probe-1959-fixture")

    @server.tool(name="issue_read")
    def issue_read(method: str, owner: str, repo: str, issue_number: int) -> str:
        if issue_read_raises is not None:
            raise issue_read_raises
        return issue_read_returns

    @contextlib.asynccontextmanager
    async def _ctx(binding):
        async with create_connected_server_and_client_session(server) as session:
            yield MCPClient(session)

    adapter._mcp_client_ctx = _ctx


class TestFoundLeg:
    async def test_real_issue_returns_found_with_item(self, sm):
        await _bind(sm)
        adapter = GitHubMCPSpatialAdapter()
        _wire_fake_server(
            adapter,
            issue_read_returns=json.dumps({"number": 108, "title": "Login bug", "state": "open"}),
        )
        status, item, resolved_repo = await adapter.probe_issue_connector(
            _ALPHA, issue_number=108, explicit_repo="o/r"
        )
        assert status == "found"
        assert item["title"] == "Login bug" and item["state"] == "open"
        assert resolved_repo == "o/r"

    async def test_title_mentioning_404_is_still_found_not_misread_as_not_found(self, sm):
        """A real issue whose own title/body happens to contain '404' (e.g.
        'Fix 404 error page') must not be misclassified by the loose
        _is_not_found_text substring/token match — the real parsed number
        is trusted first."""
        await _bind(sm)
        adapter = GitHubMCPSpatialAdapter()
        _wire_fake_server(
            adapter,
            issue_read_returns=json.dumps(
                {"number": 55, "title": "Fix 404 error page", "state": "open"}
            ),
        )
        status, item, _ = await adapter.probe_issue_connector(
            _ALPHA, issue_number=55, explicit_repo="o/r"
        )
        assert status == "found"
        assert item["title"] == "Fix 404 error page"


class TestNotFoundLeg:
    async def test_content_text_404_is_not_found(self, sm):
        """(b) Lead's pin: not-found text in the connector's CONTENT
        response (no exception raised) classifies as not_found."""
        await _bind(sm)
        adapter = GitHubMCPSpatialAdapter()
        _wire_fake_server(adapter, issue_read_returns=_GH_404_TEXT)
        status, item, resolved_repo = await adapter.probe_issue_connector(
            _ALPHA, issue_number=99999, explicit_repo="o/r"
        )
        assert status == "not_found"
        assert item is None
        assert resolved_repo == "o/r"

    async def test_json_error_body_content_is_not_found(self, sm):
        """The #1858-class in-band shape: a VALID JSON object with
        message/status but no issue number. _parse_issue_detail has no
        number-guard (unlike the write-side _parse_issue_payload fix), so
        the probe's own "trust a real number first" ordering is what keeps
        this definitive instead of a false 'found'."""
        await _bind(sm)
        adapter = GitHubMCPSpatialAdapter()
        _wire_fake_server(adapter, issue_read_returns=_GH_404_JSON)
        status, item, _ = await adapter.probe_issue_connector(
            _ALPHA, issue_number=99999, explicit_repo="o/r"
        )
        assert status == "not_found"
        assert item is None

    async def test_not_found_text_raised_as_a_plain_exception_is_not_found(self, sm):
        await _bind(sm)
        adapter = GitHubMCPSpatialAdapter()
        _wire_fake_server(
            adapter, issue_read_raises=McpError(ErrorData(code=-32603, message=_GH_404_TEXT))
        )
        status, item, resolved_repo = await adapter.probe_issue_connector(
            _ALPHA, issue_number=99999, explicit_repo="o/r"
        )
        assert status == "not_found"
        assert item is None
        assert resolved_repo == "o/r"

    async def test_not_found_text_inside_an_exception_group_leaf_is_not_found(
        self, sm, monkeypatch
    ):
        """(c) Lead's pin: the live shape (alpha v169, #1858's own finding)
        — the MCP session runs under an anyio task group, so a tool-call
        error can reach the caller wrapped in an ExceptionGroup, with the
        404 text one level down in a leaf. _leaf_exceptions must be walked,
        not just str(exc) on the outer wrapper."""
        await _bind(sm)
        adapter = GitHubMCPSpatialAdapter()

        leaf = McpError(ErrorData(code=-32603, message=_GH_404_TEXT))
        group = BaseExceptionGroup("unhandled errors in a TaskGroup", [leaf])

        @contextlib.asynccontextmanager
        async def _raising_ctx(binding):
            class _Client:
                async def call_tool(self, name, arguments=None):
                    raise group

            yield _Client()

        adapter._mcp_client_ctx = _raising_ctx
        status, item, resolved_repo = await adapter.probe_issue_connector(
            _ALPHA, issue_number=99999, explicit_repo="o/r"
        )
        assert status == "not_found"
        assert item is None
        assert resolved_repo == "o/r"


class TestUnknownLegNeverClaimsNotFound:
    async def test_auth_failure_is_unknown_never_not_found(self, sm):
        """(a) Lead's pin: a 401 failure on the tool call itself — no
        not-found evidence anywhere — must classify unknown, never
        not_found."""
        await _bind(sm)
        adapter = GitHubMCPSpatialAdapter()
        _wire_fake_server(
            adapter, issue_read_raises=McpError(ErrorData(code=-32603, message=_AUTH_ERROR_TEXT))
        )
        status, item, resolved_repo = await adapter.probe_issue_connector(
            _ALPHA, issue_number=108, explicit_repo="o/r"
        )
        assert status == "unknown"
        assert item is None and resolved_repo is None

    async def test_rate_limit_failure_is_unknown_never_not_found(self, sm):
        """(a) Lead's pin, the 403 variant."""
        await _bind(sm)
        adapter = GitHubMCPSpatialAdapter()
        _wire_fake_server(
            adapter, issue_read_raises=McpError(ErrorData(code=-32603, message=_RATE_LIMIT_TEXT))
        )
        status, item, resolved_repo = await adapter.probe_issue_connector(
            _ALPHA, issue_number=108, explicit_repo="o/r"
        )
        assert status == "unknown"
        assert item is None and resolved_repo is None

    async def test_network_failure_is_unknown_never_not_found(self, sm):
        await _bind(sm)
        adapter = GitHubMCPSpatialAdapter()
        _wire_fake_server(adapter, issue_read_raises=ConnectionError("connection reset by peer"))
        status, item, resolved_repo = await adapter.probe_issue_connector(
            _ALPHA, issue_number=108, explicit_repo="o/r"
        )
        assert status == "unknown"
        assert item is None and resolved_repo is None

    async def test_connect_required_degradation_is_unknown(self, sm):
        """(d) Lead's pin: no binding at all -> CONNECT_REQUIRED -> unknown."""
        # Deliberately do NOT call _bind: no binding row exists for _ALPHA.
        adapter = GitHubMCPSpatialAdapter()
        status, item, resolved_repo = await adapter.probe_issue_connector(
            _ALPHA, issue_number=108, explicit_repo="o/r"
        )
        assert status == "unknown"
        assert item is None and resolved_repo is None

    async def test_stale_token_degradation_is_unknown(self, sm):
        """(d) Lead's pin: a bound-but-non-BOUND status (token needs
        refresh) -> STALE_TOKEN -> unknown."""
        await _bind(sm, status="stale")
        adapter = GitHubMCPSpatialAdapter()
        status, item, resolved_repo = await adapter.probe_issue_connector(
            _ALPHA, issue_number=108, explicit_repo="o/r"
        )
        assert status == "unknown"
        assert item is None and resolved_repo is None

    async def test_unparseable_empty_response_is_unknown_not_not_found(self, sm):
        """An empty/garbage response with NO not-found text anywhere is
        honest-ambiguous, not a positive not-found signal."""
        await _bind(sm)
        adapter = GitHubMCPSpatialAdapter()
        _wire_fake_server(adapter, issue_read_returns="")
        status, item, resolved_repo = await adapter.probe_issue_connector(
            _ALPHA, issue_number=108, explicit_repo="o/r"
        )
        assert status == "unknown"
        assert item is None
