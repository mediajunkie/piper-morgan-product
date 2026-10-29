"""#2205: a GitHub write that GitHub REFUSED is said as a refusal, in GitHub's words.

xian, #1386 scenario A3 on alpha b9a8a43600 (2026-10-29): "Create an issue: 'Add search to
the main navigation bar'" went to mediajunkie/7cups-testbot, which has issues disabled.
GitHub answered 410 "Issues are disabled for this repo"; the adapter read the error body
as "no artifact", ran the #2097 title confirm, found nothing and the reply was the
"GitHub didn't confirm it" hedge. A4 "Show me that issue." then asked for a number.

CXO's words (2026-10-29 13:44): refused create → "GitHub wouldn't create it in <repo>:
<GitHub's message>. Tell me another repository and I'll try there."; refused update-shaped
write → "GitHub wouldn't <verb> #N in <repo>: <message>."; A4 after a refused create → "I
couldn't find an issue to show, because the last create in <repo> didn't go through. Give
me an issue number, or ask me to create it again."

LAYER: the adapter against a REAL in-memory MCP round-trip (the #2097/#1220 fixture idiom)
plus the router's unwrap; the renderer, the create handler and the review handler by direct
call with the router patched at its seam. DENOMINATOR: create (JSON body, go-github text),
update, close, reopen, comment; the transport-error and empty-response hedges; 401/404/5xx
bodies that are not refusals; the A4 line after a refused create and not after a landed one.
"""

from __future__ import annotations

import contextlib
import json
import uuid
from unittest.mock import AsyncMock, MagicMock, patch

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
from services.domain.models import Intent  # noqa: E402
from services.integrations.github.github_integration_router import (  # noqa: E402
    GitHubIntegrationRouter,
    GitHubIssueNotFound,
    GitHubWriteRefused,
    GitHubWriteRejected,
)
from services.intent.intent_service import IntentService  # noqa: E402
from services.intent_service.classifier import IntentClassifier  # noqa: E402
from services.mcp.consumer import github_adapter as gh_mod  # noqa: E402
from services.mcp.consumer.github_adapter import (  # noqa: E402
    GitHubMCPSpatialAdapter,
    _github_rejection,
)
from services.mcp.consumer.mcp_client import MCPClient  # noqa: E402
from services.shared_types import IntentCategory  # noqa: E402

_ALPHA = "11111111-1111-1111-1111-111111111111"
TITLE = "Add search to the main navigation bar"
OWNER, REPO = "mediajunkie", "7cups-testbot"
FULL = f"{OWNER}/{REPO}"
ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"

DISABLED_410 = json.dumps(
    {
        "message": "Issues are disabled for this repo",
        "documentation_url": "https://docs.github.com/v3/issues/",
        "status": "410",
    }
)
FORBIDDEN_403 = json.dumps(
    {
        "message": "Resource not accessible by integration",
        "documentation_url": "https://docs.github.com/rest/issues/issues#update-an-issue",
        "status": "403",
    }
)
# github-mcp-server's in-band text for the same refusal (go-github's error format).
DISABLED_410_TEXT = (
    f"failed to create issue: POST https://api.github.com/repos/{FULL}/issues: "
    "410 Issues are disabled for this repo []"
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


def _fixture(adapter, *, write_text=None, write_raises=None, comment_text=None):
    """Fake github-mcp-server whose writes answer ``write_text`` (or raise ``write_raises``,
    which the SDK turns into in-band error text). ``calls`` counts every tool the adapter
    touched, so a test can prove the title confirm and the read-back never ran."""
    server = FastMCP("github-2205-fixture")
    calls: dict[str, int] = {}

    def _hit(name):
        calls[name] = calls.get(name, 0) + 1

    @server.tool(name="issue_write")
    def issue_write(
        method: str,
        owner: str,
        repo: str,
        title: str = None,
        body: str = None,
        issue_number: int = None,
        state: str = None,
    ) -> str:
        _hit("issue_write")
        if write_raises:
            raise RuntimeError(write_raises)
        return write_text

    @server.tool(name="add_issue_comment")
    def add_issue_comment(owner: str, repo: str, issue_number: int, body: str) -> str:
        _hit("add_issue_comment")
        return comment_text

    @server.tool(name="issue_read")
    def issue_read(method: str, owner: str, repo: str, issue_number: int) -> str:
        _hit("issue_read")
        return json.dumps({})

    @server.tool(name="search_issues")
    def search_issues(query: str, sort: str = None, order: str = None, perPage: int = 30) -> str:
        _hit("search_issues")
        return json.dumps({"total_count": 0, "items": []})

    @server.tool(name="list_issues")
    def list_issues(
        owner: str,
        repo: str,
        state: str = None,
        sort: str = None,
        direction: str = None,
        perPage: int = 30,
    ) -> str:
        _hit("list_issues")
        return json.dumps([])

    @contextlib.asynccontextmanager
    async def _ctx(binding):
        async with create_connected_server_and_client_session(server) as session:
            yield MCPClient(session)

    adapter._mcp_client_ctx = _ctx
    return calls


def _router(adapter) -> GitHubIntegrationRouter:
    router = GitHubIntegrationRouter.__new__(GitHubIntegrationRouter)
    router.mcp_adapter = adapter
    router._user_id = _ALPHA
    return router


class TestRejectionParse:
    def test_json_error_body(self):
        assert _github_rejection(DISABLED_410) == (410, "Issues are disabled for this repo")

    def test_go_github_text(self):
        assert _github_rejection(DISABLED_410_TEXT) == (410, "Issues are disabled for this repo")

    def test_validation_failed(self):
        body = json.dumps({"message": "Validation Failed", "errors": [], "status": "422"})
        assert _github_rejection(body) == (422, "Validation Failed")

    @pytest.mark.parametrize(
        "text",
        [
            None,
            "",
            "not json and not an http error",
            json.dumps({"number": 10, "title": TITLE, "message": "x", "status": "410"}),
            json.dumps({"message": "Not Found", "status": "404"}),  # #1858's bucket
            json.dumps({"message": "Bad credentials", "status": "401"}),  # the auth rail
            json.dumps({"message": "Server Error", "status": "502"}),  # outcome unknown
            "failed to get issue: GET https://api.github.com/repos/o/r/issues/9: 404 Not Found []",
        ],
    )
    def test_not_a_refusal(self, text):
        assert _github_rejection(text) is None


@pytest.mark.asyncio
class TestAdapterRaisesTheRefusal:
    async def test_create_410_body_is_rejected_without_the_title_confirm(self, sm):
        adapter = GitHubMCPSpatialAdapter()
        calls = _fixture(adapter, write_text=DISABLED_410)
        with (
            patch.object(
                adapter, "_confirm_create_by_title", new=AsyncMock(return_value=None)
            ) as confirm,
            patch.object(
                adapter, "_confirm_create_by_title_after", new=AsyncMock(return_value=None)
            ) as confirm_after,
        ):
            wr = await adapter.create_issue_connector(
                _ALPHA, owner=OWNER, repo=REPO, title=TITLE, body="b"
            )
            with pytest.raises(GitHubWriteRejected) as exc:
                await _router(adapter)._try_connector_write(
                    "create_issue_connector", owner=OWNER, repo=REPO, title=TITLE, body="b"
                )
        assert wr.rejected is True and wr.verified is False and wr.attempted is True
        assert wr.github_status == 410
        assert wr.github_message == "Issues are disabled for this repo"
        e = exc.value
        assert (e.message, e.status, e.owner, e.repo, e.verb) == (
            "Issues are disabled for this repo",
            410,
            OWNER,
            REPO,
            "create",
        )
        confirm.assert_not_awaited()
        confirm_after.assert_not_awaited()
        assert set(calls) == {"issue_write"}  # no read-back, no list, no search

    async def test_create_410_go_github_text_is_rejected(self, sm):
        adapter = GitHubMCPSpatialAdapter()
        calls = _fixture(adapter, write_raises=DISABLED_410_TEXT)
        with pytest.raises(GitHubWriteRejected) as exc:
            await _router(adapter)._try_connector_write(
                "create_issue_connector", owner=OWNER, repo=REPO, title=TITLE, body="b"
            )
        assert exc.value.status == 410
        assert exc.value.message == "Issues are disabled for this repo"
        assert set(calls) == {"issue_write"}

    async def test_update_403_is_rejected_as_update(self, sm):
        adapter = GitHubMCPSpatialAdapter()
        _fixture(adapter, write_text=FORBIDDEN_403)
        with pytest.raises(GitHubWriteRejected) as exc:
            await _router(adapter)._try_connector_write(
                "update_issue_connector", owner=OWNER, repo=REPO, issue_number=7, title="New"
            )
        e = exc.value
        assert (e.status, e.message, e.verb, e.issue_number, e.repository) == (
            403,
            "Resource not accessible by integration",
            "update",
            7,
            FULL,
        )

    async def test_close_403_is_rejected_as_close(self, sm):
        adapter = GitHubMCPSpatialAdapter()
        calls = _fixture(adapter, write_text=FORBIDDEN_403)
        with pytest.raises(GitHubWriteRejected) as exc:
            await _router(adapter)._try_connector_write(
                "update_issue_connector", owner=OWNER, repo=REPO, issue_number=7, state="closed"
            )
        assert (exc.value.status, exc.value.verb, exc.value.issue_number) == (403, "close", 7)
        assert set(calls) == {"issue_write"}

    async def test_reopen_and_comment_403_name_their_verbs(self, sm):
        adapter = GitHubMCPSpatialAdapter()
        _fixture(adapter, write_text=FORBIDDEN_403, comment_text=FORBIDDEN_403)
        with pytest.raises(GitHubWriteRejected) as reopen:
            await _router(adapter)._try_connector_write(
                "update_issue_connector", owner=OWNER, repo=REPO, issue_number=7, state="open"
            )
        with pytest.raises(GitHubWriteRejected) as comment:
            await _router(adapter)._try_connector_write(
                "add_comment_connector", owner=OWNER, repo=REPO, issue_number=7, comment="hi"
            )
        assert reopen.value.verb == "reopen"
        assert comment.value.verb == "comment on" and comment.value.status == 403

    async def test_transport_error_still_hedges(self, sm):
        adapter = GitHubMCPSpatialAdapter()

        class _Broken:
            async def call_tool(self, name, args):
                raise ConnectionError("connection reset by peer")

        @contextlib.asynccontextmanager
        async def _ctx(binding):
            yield _Broken()

        adapter._mcp_client_ctx = _ctx
        with pytest.raises(RuntimeError) as exc:
            await _router(adapter)._try_connector_write(
                "create_issue_connector", owner=OWNER, repo=REPO, title=TITLE, body="b"
            )
        assert not isinstance(exc.value, (GitHubWriteRejected, GitHubWriteRefused))
        assert "may or may not have landed" in str(exc.value)

    async def test_empty_response_still_hedges(self, sm):
        adapter = GitHubMCPSpatialAdapter()
        _fixture(adapter, write_text="")
        with pytest.raises(RuntimeError) as exc:
            await _router(adapter)._try_connector_write(
                "create_issue_connector", owner=OWNER, repo=REPO, title=TITLE, body="b"
            )
        assert not isinstance(exc.value, GitHubWriteRejected)
        assert "may or may not have landed" in str(exc.value)

    async def test_a_5xx_body_still_hedges(self, sm):
        adapter = GitHubMCPSpatialAdapter()
        _fixture(adapter, write_text=json.dumps({"message": "Server Error", "status": "502"}))
        with pytest.raises(RuntimeError) as exc:
            await _router(adapter)._try_connector_write(
                "create_issue_connector", owner=OWNER, repo=REPO, title=TITLE, body="b"
            )
        assert not isinstance(exc.value, GitHubWriteRejected)
        assert "may or may not have landed" in str(exc.value)


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name})")


@pytest.fixture
def service():
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            clf = IntentClassifier(llm_service=_ExplosiveLLM())
            return IntentService(intent_classifier=clf)


def _intent(message=f"Create an issue: '{TITLE}'", action="create_issue", **extra):
    ctx = {"original_message": message, "user_id": _ALPHA, **extra}
    return Intent(
        category=IntentCategory.EXECUTION,
        action=action,
        original_message=message,
        confidence=1.0,
        context=ctx,
    )


def _rejected(verb="create", issue_number=None, status=410, message=None):
    return GitHubWriteRejected(
        message or "Issues are disabled for this repo",
        status,
        OWNER,
        REPO,
        verb=verb,
        issue_number=issue_number,
    )


CREATE_LINE = (
    "GitHub wouldn't create it in mediajunkie/7cups-testbot: Issues are disabled for this "
    "repo. Tell me another repository and I'll try there."
)
A4_LINE = (
    "I couldn't find an issue to show, because the last create in mediajunkie/7cups-testbot "
    "didn't go through. Give me an issue number, or ask me to create it again."
)


class TestRendererWords:
    def test_refused_create_is_cxos_line(self, service):
        out = service._unverified_write_result(_rejected(), _intent(), "wf", repository=FULL)
        assert out.message == CREATE_LINE
        assert out.intent_data["write_refused"] is True
        assert out.intent_data["github_status"] == 410
        assert out.intent_data["github_message"] == "Issues are disabled for this repo"
        assert out.intent_data["repository"] == FULL
        assert "write_unconfirmed" not in out.intent_data

    def test_refused_update_is_the_same_shape_without_a_retry(self, service):
        e = _rejected(
            verb="update",
            issue_number=7,
            status=403,
            message="Resource not accessible by integration",
        )
        out = service._unverified_write_result(e, _intent(action="update_issue"), "wf")
        assert out.message == (
            "GitHub wouldn't update #7 in mediajunkie/7cups-testbot: "
            "Resource not accessible by integration."
        )
        assert "check" not in out.message.lower()
        assert "try" not in out.message.lower()
        assert out.intent_data["github_status"] == 403
        assert out.intent_data["repository"] == FULL

    def test_a_message_with_its_own_period_is_not_doubled(self, service):
        e = _rejected(verb="close", issue_number=7, status=403, message="Must have admin rights.")
        out = service._unverified_write_result(e, _intent(action="close_issue"), "wf")
        assert out.message == (
            "GitHub wouldn't close #7 in mediajunkie/7cups-testbot: Must have admin rights."
        )

    def test_the_2106_and_1858_branches_are_unchanged(self, service):
        refused = service._unverified_write_result(
            GitHubWriteRefused(user_message="Nothing was created.", action_hint="Reconnect."),
            _intent(),
            "wf",
        )
        assert refused.message == "Nothing was created. Reconnect."
        assert "github_status" not in refused.intent_data
        missing = service._unverified_write_result(
            GitHubIssueNotFound(issue_number=99, owner=OWNER, repo=REPO),
            _intent(action="close_issue"),
            "wf",
        )
        assert missing.message.startswith(f"There's no issue #99 in {FULL}")


def _gate_open():
    return patch(
        "services.intent_service.collaboration_gate.gate_holds", new=AsyncMock(return_value=False)
    )


def _github_config():
    return patch(
        "services.configuration.piper_config_loader.piper_config_loader.load_github_config",
        return_value=MagicMock(default_labels=[]),
    )


def _create_patches(create_effect):
    return (
        _gate_open(),
        _github_config(),
        patch(f"{ROUTER}.initialize", new=AsyncMock()),
        patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
        patch(f"{ROUTER}.find_open_issue_by_title", new=AsyncMock(return_value=None)),
        patch(f"{ROUTER}.create_issue", new=create_effect),
    )


async def _create(service, sid, create_effect):
    with contextlib.ExitStack() as stack:
        for p in _create_patches(create_effect):
            stack.enter_context(p)
        return await service._handle_create_issue(
            _intent(title=TITLE, repository=FULL), "wf", sid, user_id=_ALPHA
        )


async def _show_that_issue(service, sid):
    with patch.object(service, "_issue_referent_from_ledger", new=AsyncMock(return_value=None)):
        return await service._handle_review_issue_query(
            _intent(message="Show me that issue.", action="get_issue"), "wf", sid
        )


@pytest.mark.asyncio
class TestCreateHandlerAndTheA4Referent:
    async def test_a3_a4_refused_create_then_show_that_issue(self, service):
        sid = f"s-2205-{uuid.uuid4()}"
        created = await _create(service, sid, AsyncMock(side_effect=_rejected()))
        assert created.message == CREATE_LINE
        assert created.intent_data["write_refused"] is True
        shown = await _show_that_issue(service, sid)
        assert shown.message == A4_LINE

    async def test_after_a_landed_create_the_a4_line_is_gone(self, service):
        sid = f"s-2205-{uuid.uuid4()}"
        await _create(service, sid, AsyncMock(side_effect=_rejected()))
        landed = {"number": 3, "title": TITLE, "html_url": f"https://github.com/{FULL}/issues/3"}
        ok = await _create(service, sid, AsyncMock(return_value=landed))
        assert ok.message.startswith("Created issue #3")
        shown = await _show_that_issue(service, sid)
        assert "didn't go through" not in shown.message
        assert shown.message.startswith("I couldn't find an issue number")

    async def test_another_session_does_not_see_the_refusal(self, service):
        sid = f"s-2205-{uuid.uuid4()}"
        await _create(service, sid, AsyncMock(side_effect=_rejected()))
        shown = await _show_that_issue(service, f"s-2205-other-{uuid.uuid4()}")
        assert "didn't go through" not in shown.message

    async def test_an_unconfirmed_create_does_not_claim_it_failed(self, service):
        sid = f"s-2205-{uuid.uuid4()}"
        hedge = RuntimeError("GitHub write could not be verified — it may or may not have landed.")
        out = await _create(service, sid, AsyncMock(side_effect=hedge))
        assert out.intent_data.get("write_unconfirmed") is True
        shown = await _show_that_issue(service, sid)
        assert "didn't go through" not in shown.message


@pytest.mark.asyncio
class TestReopenHandlerSaysTheRefusal:
    async def test_refused_reopen(self, service):
        intent = _intent(
            message=f"reopen issue #7 in {FULL}", action="reopen_issue", repository=FULL
        )
        e = _rejected(verb="reopen", issue_number=7, status=403, message="Forbidden")
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.get_issue", new=AsyncMock(side_effect=RuntimeError("no fetch"))),
            patch(f"{ROUTER}.update_issue", new=AsyncMock(side_effect=e)),
        ):
            out = await service._handle_reopen_issue_query(intent, "wf", None)
        assert out.message == "GitHub wouldn't reopen #7 in mediajunkie/7cups-testbot: Forbidden."
        assert out.intent_data["write_refused"] is True
