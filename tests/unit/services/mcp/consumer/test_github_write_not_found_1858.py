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
_GH_404_COMMENT = (
    "failed to create comment: POST https://api.github.com/repos/o/r/issues/9999/comments: "
    "404 Not Found []"
)
_GH_404_READ = (
    "failed to get issue: GET https://api.github.com/repos/o/r/issues/99999: 404 Not Found []"
)


async def _fake_grant(owner_id):
    return "gho_test_grant_2266"


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
    # #2266: the resolver reads the OAuth grant strictly; this fixture stores none, so
    # the seam answers with a fake bearer (the connect itself is faked below).
    monkeypatch.setattr(gh_mod.GitHubMCPSpatialAdapter, "_oauth_grant", staticmethod(_fake_grant))
    async with maker() as s:
        await ConnectorBindingRepository(s).upsert(
            _ALPHA, "github", status="bound", mcp_server_ref="http://srv/mcp"
        )
        await s.commit()
    yield maker
    await engine.dispose()


# 2026-10-01 (PM's test card, Test 3, alpha v156): the 404 can also arrive as
# GitHub's API error BODY — valid JSON — which the issue parser accepted as an
# "issue" dict (no number, a message/status), so the definitive branch never
# fired and the close of #99999 fell to the "may or may not have landed" hedge.
_GH_404_JSON = json.dumps(
    {
        "message": "Not Found",
        "documentation_url": "https://docs.github.com/rest/issues/issues#update-an-issue",
        "status": "404",
    }
)


def _fixture(
    adapter,
    *,
    read_finds_it=False,
    write_404=True,
    err_text=None,
    read_raises=False,
    write_raises=False,
    write_err_text=None,
    read_err_text=None,
):
    """Fake server: issue 7 exists; anything else 404s on write. Read-back 404s unless
    ``read_finds_it`` (the pathological write-404-but-read-ok case). ``err_text``
    overrides the 404 shape for BOTH legs (default: the text shape; the JSON
    body shape is the 2026-10-01 regression). ``read_raises`` / ``write_raises``
    make that leg surface its 404 as a JSON-RPC error (``McpError``) instead of
    content text — the shape the live server used for the read-back on alpha
    v169 (PM's Test A, 2026-10-05)."""
    server = FastMCP("github-404-fixture")
    write_err = write_err_text or err_text or _GH_404
    read_err = read_err_text or err_text or _GH_404_READ
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
            return write_err if write_404 else json.dumps({"number": 8, "html_url": "u"})
        if issue_number in existing:
            if title is not None:
                existing[issue_number]["title"] = title
            if state is not None:
                existing[issue_number]["state"] = state
            return json.dumps(existing[issue_number])
        return write_err

    @server.tool(name="add_issue_comment")
    def add_issue_comment(owner: str, repo: str, issue_number: int, body: str) -> str:
        # #1858 amended (2026-11-03): a comment on a missing issue 404s on the write leg.
        if issue_number in existing:
            return json.dumps({"id": 101, "body": body, "html_url": "u"})
        return write_err

    @server.tool(name="issue_read")
    def issue_read(method: str, owner: str, repo: str, issue_number: int) -> str:
        if issue_number in existing:
            return json.dumps(existing[issue_number])
        if read_finds_it:
            return json.dumps({"number": issue_number, "title": "ghost", "state": "open"})
        return read_err

    @contextlib.asynccontextmanager
    async def _ctx(binding):
        async with create_connected_server_and_client_session(server) as session:
            client = MCPClient(session)
            if read_raises or write_raises:
                real_call = client.call_tool

                async def _call(name, arguments=None):
                    number = (arguments or {}).get("issue_number")
                    if number not in existing:
                        if name == "issue_read" and read_raises:
                            raise McpError(ErrorData(code=-32603, message=read_err))
                        if name in ("issue_write", "add_issue_comment") and write_raises:
                            raise McpError(ErrorData(code=-32603, message=write_err))
                    return await real_call(name, arguments)

                client.call_tool = _call
            yield client

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

    async def test_update_of_nonexistent_issue_is_definitive_with_a_json_error_body(self, sm):
        """The shape PM hit live 2026-10-01: GitHub's JSON error body on both
        legs. Must be the SAME definitive bucket, not the hedge."""
        adapter = GitHubMCPSpatialAdapter()
        _fixture(adapter, err_text=_GH_404_JSON)
        wr = await adapter.update_issue_connector(
            _ALPHA, owner="o", repo="r", issue_number=99999, state="closed"
        )
        assert wr.not_found is True, wr
        assert wr.verified is False and wr.attempted is True

    async def test_update_of_nonexistent_issue_is_definitive_when_readback_raises(self, sm):
        """The shape PM hit live 2026-10-05 (Test A, alpha v169): the write leg
        returns the 404 as content text, but the live server answers the
        READ-BACK with a JSON-RPC error (McpError "failed to get issue: GET
        …/99999: 404 Not Found"). The read-back leg lands in the mid-flight
        except, which used to degrade to the hedge. Same two-leg evidence →
        same definitive bucket."""
        adapter = GitHubMCPSpatialAdapter()
        _fixture(adapter, read_raises=True)
        wr = await adapter.update_issue_connector(
            _ALPHA, owner="o", repo="r", issue_number=99999, state="closed"
        )
        assert wr.not_found is True, wr
        assert wr.verified is False and wr.attempted is True
        assert wr.issue_number == 99999

    async def test_update_write_leg_raising_with_404_and_readback_404_is_definitive(self, sm):
        """Arch's #1858 amendment (2026-11-03 18:53, from #2258 F1): a TARGET-ADDRESSED
        write whose WRITE leg raised with a not-found leaf, confirmed by a fresh
        read-back that also says 404, provably never landed. Until then this pin
        said the opposite ("the write may have fired"); a 404 is GitHub's answer to
        the request itself, so there is no double-write to fear."""
        adapter = GitHubMCPSpatialAdapter()
        _fixture(adapter, write_raises=True)
        wr = await adapter.update_issue_connector(
            _ALPHA, owner="o", repo="r", issue_number=99999, state="closed"
        )
        assert wr.not_found is True, wr
        assert wr.verified is False and wr.attempted is True
        assert wr.issue_number == 99999

    def test_error_body_is_not_an_issue_payload(self):
        f = GitHubMCPSpatialAdapter._parse_issue_payload
        assert f(_GH_404_JSON) is None
        assert f(json.dumps({"number": 7, "title": "t"})) == {"number": 7, "title": "t"}

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


class TestWriteLegNotFound1858Amended:
    """Arch 2026-11-03 18:53: a target-addressed write (comment or update) whose write
    leg raises with a not-found leaf is definitive ONLY with a positive read-back on
    the same binding; a found or unknown read-back, a non-404 leaf, or a create stays
    honest-uncertain. CXO: the person's line is "didn't go through", no cause."""

    async def test_a_comment_on_a_missing_issue_is_definitive(self, sm):
        adapter = GitHubMCPSpatialAdapter()
        _fixture(adapter, write_raises=True, write_err_text=_GH_404_COMMENT)
        wr = await adapter.add_comment_connector(
            _ALPHA, owner="o", repo="r", issue_number=9999, comment="PA 2258 probe"
        )
        assert wr.not_found is True, wr
        assert wr.verified is False and wr.attempted is True
        assert wr.issue_number == 9999

    async def test_a_404_leaf_but_a_readback_that_finds_the_issue_is_uncertain(self, sm):
        adapter = GitHubMCPSpatialAdapter()
        _fixture(adapter, write_raises=True, write_err_text=_GH_404_COMMENT, read_finds_it=True)
        wr = await adapter.add_comment_connector(
            _ALPHA, owner="o", repo="r", issue_number=9999, comment="x"
        )
        assert wr.not_found is False, wr
        assert wr.verified is False and wr.attempted is True

    async def test_a_non_404_write_leaf_is_uncertain(self, sm):
        """A transport failure or timeout on the write leg says nothing about the
        target: the write may have fired. No read-back is consulted."""
        adapter = GitHubMCPSpatialAdapter()
        _fixture(adapter, write_raises=True, write_err_text="server disconnected mid-request")
        wr = await adapter.add_comment_connector(
            _ALPHA, owner="o", repo="r", issue_number=9999, comment="x"
        )
        assert wr.not_found is False, wr
        assert wr.attempted is True

    async def test_a_readback_of_unknown_is_uncertain(self, sm):
        """The read-back erroring with anything but GitHub's 404 shape is unknown,
        never not-found (the #1959 rule); the write stays honest-uncertain."""
        adapter = GitHubMCPSpatialAdapter()
        _fixture(
            adapter,
            write_raises=True,
            write_err_text=_GH_404_COMMENT,
            read_raises=True,
            read_err_text="internal error: upstream unavailable",
        )
        wr = await adapter.add_comment_connector(
            _ALPHA, owner="o", repo="r", issue_number=9999, comment="x"
        )
        assert wr.not_found is False, wr

    async def test_a_create_with_a_404_leaf_is_uncertain(self, sm):
        """A create addresses no issue, so a 404 leaf proves nothing about it."""
        adapter = GitHubMCPSpatialAdapter()
        _fixture(adapter, write_raises=True)
        wr = await adapter.create_issue_connector(_ALPHA, owner="o", repo="r", title="t", body="b")
        assert wr.not_found is False, wr

    async def test_a_comment_on_a_missing_issue_answered_in_band_is_definitive(self, sm):
        """PA's F1 on alpha 3f7994e873 (2026-11-04 08:32): the live server answers the
        comment POST with the 404 as CONTENT TEXT, not an exception, and the comment
        path used to return "no artifact id" before any not-found check. Same two
        legs as the update case: the write text says 404, the read-back says 404."""
        adapter = GitHubMCPSpatialAdapter()
        _fixture(adapter, write_err_text=_GH_404_COMMENT)
        wr = await adapter.add_comment_connector(
            _ALPHA, owner="o", repo="r", issue_number=9998, comment="PA 1858 probe"
        )
        assert wr.not_found is True, wr
        assert wr.verified is False and wr.attempted is True
        assert wr.issue_number == 9998

    async def test_an_in_band_404_but_a_readback_that_finds_it_is_uncertain(self, sm):
        adapter = GitHubMCPSpatialAdapter()
        _fixture(adapter, write_err_text=_GH_404_COMMENT, read_finds_it=True)
        wr = await adapter.add_comment_connector(
            _ALPHA, owner="o", repo="r", issue_number=9998, comment="x"
        )
        assert wr.not_found is False, wr

    async def test_an_in_band_non_404_error_is_uncertain(self, sm):
        adapter = GitHubMCPSpatialAdapter()
        _fixture(adapter, write_err_text="failed to create comment: something else went wrong")
        wr = await adapter.add_comment_connector(
            _ALPHA, owner="o", repo="r", issue_number=9998, comment="x"
        )
        assert wr.not_found is False, wr

    async def test_a_comment_on_an_existing_issue_still_verifies(self, sm):
        adapter = GitHubMCPSpatialAdapter()
        _fixture(adapter)
        wr = await adapter.add_comment_connector(
            _ALPHA, owner="o", repo="r", issue_number=7, comment="hello"
        )
        assert wr.not_found is False and wr.verified is True, wr

    def test_the_router_turns_the_result_into_not_found_and_the_outcome_into_failed(self):
        from services.security.consequential_outcomes import github_write_outcome

        status, details = github_write_outcome(
            GitHubIssueNotFound(issue_number=9999, owner="o", repo="r")
        )
        assert status == "failed"
        assert details["error_type"] == "GitHubIssueNotFound"


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

    def test_not_found_gets_the_couldnt_find_sentence(self):
        """CXO 2026-11-04 08:52: one sentence for close, update and comment that is
        true both for a missing issue and for a repository the credential cannot
        see; the next step is kept; the old "There's no issue" asserted too much."""
        svc, intent = self._svc_and_intent()
        e = GitHubIssueNotFound(issue_number=99999, owner="o", repo="r")
        res = svc._unverified_write_result(e, intent, "wf")
        assert res is not None
        assert res.message == (
            "I couldn't find issue #99999 in o/r, so nothing was changed. "
            "Check the number and try again, or say 'show open issues' to find it."
        )
        assert res.success is False  # #2188 (Arch 13:43): the write was not performed
        assert res.intent_data["not_performed"] == "not_found"
        assert "There's no issue" not in res.message
        assert "may or may not" not in res.message and "duplicate" not in res.message

    def test_unverified_keeps_the_honest_uncertain_sentence(self):
        svc, intent = self._svc_and_intent()
        e = RuntimeError("GitHub write could not be verified — it may or may not have landed.")
        res = svc._unverified_write_result(e, intent, "wf")
        assert res is not None and "may or may not" in res.message and "duplicate" in res.message

    def test_unrelated_error_is_not_claimed(self):
        svc, intent = self._svc_and_intent()
        assert svc._unverified_write_result(ValueError("x"), intent, "wf") is None
