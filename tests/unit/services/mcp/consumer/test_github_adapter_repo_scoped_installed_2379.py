"""#2379 (Arch 2026-11-15 15:49): on a GitHub App grant, a read of one repository
(branches, releases, one issue, and the close/reopen probe) runs only when the App is
installed on that repository.

Before this, those reads called github-mcp-server with ``{owner, repo}`` on the App
user token, which can read a public repository with no installation. So a person could
get branches or an issue from a repository they never gave the App, while "my
repositories" (#2342) and "my issues" (#2374) left it out.

Layer: unit. The MCP client, the repository resolver and the installation read are
fakes; nothing calls GitHub.

The write half (same ruling: "the same check, before the confirm") is pinned below:
the adapter's choke point in ``_verified_write``, the duplicate-title read, and the
three places a confirm is built (create, update, close and reopen). A comment has no
confirm; the choke point answers it.
"""

from __future__ import annotations

import contextlib
import json
from typing import Any, Dict, List
from unittest.mock import AsyncMock

import pytest

from services.integrations.github.repo_resolver import ResolutionSource, ResolvedRepo
from services.mcp.consumer import github_adapter as gh_mod
from services.mcp.consumer import github_app_grant as grant_mod
from services.mcp.consumer import github_app_install as install_mod
from services.mcp.consumer.connector import DegradationReason
from services.mcp.consumer.github_adapter import GitHubCredential, GitHubMCPSpatialAdapter
from services.mcp.consumer.github_app_install import (
    DETAIL_APP_INSTALL_LINK_MISSING,
    DETAIL_APP_NOT_INSTALLED,
    DETAIL_APP_NOT_ON_REPOSITORY,
    InstallationReadFailed,
    InstalledRepositories,
    installation_read_scope,
)

pytestmark = pytest.mark.asyncio

_OWNER = "11111111-1111-1111-1111-111111111111"
_ISSUE = json.dumps({"number": 7, "title": "t", "state": "open", "html_url": "u"})
_LIST = json.dumps([{"name": "main", "tag_name": "v1"}])


@pytest.fixture(autouse=True)
def _install_link(monkeypatch):
    monkeypatch.setenv(grant_mod.ENV_APP_SLUG, "piper-example")


def _credential(leg="oauth", app_grant=True):
    return GitHubCredential(
        owner_id=_OWNER, mcp_server_ref="github", token="access-live", leg=leg, app_grant=app_grant
    )


def _installed(*names):
    return InstalledRepositories(
        installations=1 if names else 0,
        repositories=[
            {"id": i, "name": n.split("/")[1], "full_name": n} for i, n in enumerate(names)
        ],
    )


def _adapter(monkeypatch, installed, *, credential=None, target="octo/public"):
    """An adapter that resolves every read to ``target``, records each MCP call, and
    whose installation read answers ``installed``."""
    seen: List[Dict[str, Any]] = []

    class _Client:
        async def call_tool(self, tool, args):
            seen.append({"tool": tool, **args})
            return _ISSUE if tool == gh_mod._ISSUE_READ_TOOL else _LIST

    @contextlib.asynccontextmanager
    async def _ctx(_binding):
        yield _Client()

    owner, name = target.split("/")
    monkeypatch.setattr(
        gh_mod,
        "resolve_repo",
        AsyncMock(
            return_value=ResolvedRepo(owner=owner, name=name, source=list(ResolutionSource)[0])
        ),
    )
    adapter = GitHubMCPSpatialAdapter()
    adapter.resolve_credential = AsyncMock(return_value=credential or _credential())
    adapter._mcp_client_ctx = _ctx
    monkeypatch.setattr(GitHubMCPSpatialAdapter, "_tool_text", classmethod(lambda cls, r: r))
    read = (
        AsyncMock(side_effect=installed)
        if isinstance(installed, Exception)
        else AsyncMock(return_value=installed)
    )
    monkeypatch.setattr(gh_mod, "list_installed_repositories", read)
    return adapter, seen, read


#: name -> (the call, the attribute that holds what was read)
_READS = {
    "branches": (lambda a: a.list_branches_connector(_OWNER), "items"),
    "releases": (lambda a: a.list_releases_connector(_OWNER), "items"),
    "one issue": (lambda a: a.get_issue_connector(_OWNER, issue_number=7), "item"),
}


@pytest.mark.parametrize("read_name", sorted(_READS))
class TestARepoScopedReadOnAnAppGrant:
    async def test_installed_on_the_repository_reads_it(self, monkeypatch, read_name):
        call, holds = _READS[read_name]
        adapter, seen, read = _adapter(monkeypatch, _installed("octo/a", "octo/public"))
        result = await call(adapter)
        assert result.degradation is None
        assert getattr(result, holds)
        assert [(s["owner"], s["repo"]) for s in seen] == [("octo", "public")]
        read.assert_awaited_once_with("access-live")

    async def test_the_match_ignores_case(self, monkeypatch, read_name):
        call, _ = _READS[read_name]
        adapter, seen, _ = _adapter(monkeypatch, _installed("Octo/Public"))
        result = await call(adapter)
        assert result.degradation is None and len(seen) == 1

    async def test_not_installed_on_it_refuses_with_no_client_call(self, monkeypatch, read_name):
        call, holds = _READS[read_name]
        adapter, seen, _ = _adapter(monkeypatch, _installed("octo/a"))
        result = await call(adapter)
        assert seen == []  # the public repository was never read
        assert getattr(result, holds) is None
        assert result.degradation.reason is DegradationReason.REPO_UNRESOLVED
        assert result.degradation.detail == DETAIL_APP_NOT_ON_REPOSITORY
        assert result.degradation.user_message == gh_mod.GITHUB_APP_NOT_ON_REPOSITORY_REPLY

    async def test_not_installed_on_it_with_no_install_link_is_the_on_our_side_line(
        self, monkeypatch, read_name
    ):
        monkeypatch.delenv(grant_mod.ENV_APP_SLUG)
        call, _ = _READS[read_name]
        adapter, seen, _ = _adapter(monkeypatch, _installed("octo/a"))
        result = await call(adapter)
        assert seen == []
        assert result.degradation.detail == DETAIL_APP_INSTALL_LINK_MISSING

    async def test_installed_nowhere_is_the_install_step(self, monkeypatch, read_name):
        call, _ = _READS[read_name]
        adapter, seen, _ = _adapter(monkeypatch, _installed())
        result = await call(adapter)
        assert seen == []
        assert result.degradation.reason is DegradationReason.REPO_UNRESOLVED
        assert result.degradation.detail == DETAIL_APP_NOT_INSTALLED

    @pytest.mark.parametrize("status", [None, 403, 500])
    async def test_a_failed_installation_read_degrades_and_never_reads(
        self, monkeypatch, read_name, status
    ):
        call, holds = _READS[read_name]
        adapter, seen, _ = _adapter(monkeypatch, InstallationReadFailed(status))
        result = await call(adapter)
        assert seen == []
        assert getattr(result, holds) is None
        assert result.degradation.reason is DegradationReason.UNREACHABLE

    async def test_a_401_on_the_installation_read_is_the_stale_path(self, monkeypatch, read_name):
        call, _ = _READS[read_name]
        adapter, seen, _ = _adapter(monkeypatch, InstallationReadFailed(401))
        adapter._rejected_token_was_replaced = AsyncMock(return_value=False)
        adapter._mark_oauth_binding_stale = AsyncMock()
        result = await call(adapter)
        assert seen == []
        assert result.degradation.reason is DegradationReason.STALE_TOKEN

    async def test_a_malformed_installed_name_fails_the_read(self, monkeypatch, read_name):
        call, _ = _READS[read_name]
        adapter, seen, _ = _adapter(monkeypatch, _installed("octo/public", "not a name/x y"))
        result = await call(adapter)
        assert seen == []
        assert result.degradation.reason is DegradationReason.UNREACHABLE

    @pytest.mark.parametrize(
        "credential",
        [_credential(leg="pat", app_grant=False), _credential(leg="oauth", app_grant=False)],
        ids=["personal token", "classic grant"],
    )
    async def test_the_other_legs_make_no_installation_read(
        self, monkeypatch, read_name, credential
    ):
        call, holds = _READS[read_name]
        adapter, seen, read = _adapter(
            monkeypatch, AssertionError("no installation read"), credential=credential
        )
        result = await call(adapter)
        assert result.degradation is None and getattr(result, holds)
        assert len(seen) == 1
        read.assert_not_awaited()


class TestTheCloseReopenProbe:
    async def test_installed_reads_the_issue(self, monkeypatch):
        adapter, seen, _ = _adapter(monkeypatch, _installed("octo/public"))
        status, item, repo = await adapter.probe_issue_connector(_OWNER, issue_number=7)
        assert status == "found" and item["number"] == 7 and repo == "octo/public"

    @pytest.mark.parametrize(
        "installed",
        [_installed("octo/a"), _installed(), InstallationReadFailed(500)],
        ids=["not on it", "installed nowhere", "read failed"],
    )
    async def test_otherwise_unknown_with_no_client_call(self, monkeypatch, installed):
        adapter, seen, _ = _adapter(monkeypatch, installed)
        assert await adapter.probe_issue_connector(_OWNER, issue_number=7) == (
            "unknown",
            None,
            None,
        )
        assert seen == []  # never "not found" from a read that didn't run


class TestOneInstallationReadPerRequest:
    """Arch's cost ruling: once per request, held on the request, never across."""

    @pytest.fixture
    def github(self, monkeypatch):
        calls: List[str] = []
        answers: List[Any] = []

        async def _read(token):
            calls.append(token)
            answer = answers.pop(0) if answers else _installed("octo/a")
            if isinstance(answer, Exception):
                raise answer
            return answer

        monkeypatch.setattr(install_mod, "_read_installed_repositories", _read)
        return calls, answers

    async def test_outside_a_request_every_call_reads(self, github):
        calls, _ = github
        await install_mod.list_installed_repositories("t1")
        await install_mod.list_installed_repositories("t1")
        assert calls == ["t1", "t1"]

    async def test_inside_a_request_the_second_call_reuses_the_answer(self, github):
        calls, _ = github
        with installation_read_scope():
            first = await install_mod.list_installed_repositories("t1")
            second = await install_mod.list_installed_repositories("t1")
        assert calls == ["t1"] and first is second

    async def test_the_answer_is_per_token(self, github):
        calls, _ = github
        with installation_read_scope():
            await install_mod.list_installed_repositories("t1")
            await install_mod.list_installed_repositories("t2")
        assert calls == ["t1", "t2"]

    async def test_nothing_is_held_into_the_next_request(self, github):
        calls, answers = github
        answers.extend([_installed("octo/a"), _installed("octo/a", "octo/b")])
        with installation_read_scope():
            await install_mod.list_installed_repositories("t1")
        with installation_read_scope():
            later = await install_mod.list_installed_repositories("t1")
        assert calls == ["t1", "t1"]
        assert [r["full_name"] for r in later.repositories] == ["octo/a", "octo/b"]
        assert install_mod._request_reads.get() is None

    async def test_a_failed_read_is_not_held(self, github):
        calls, answers = github
        answers.extend([InstallationReadFailed(502), _installed("octo/a")])
        with installation_read_scope():
            with pytest.raises(InstallationReadFailed):
                await install_mod.list_installed_repositories("t1")
            assert (await install_mod.list_installed_repositories("t1")).repositories
        assert calls == ["t1", "t1"]

    async def test_a_scope_inside_a_scope_keeps_the_outer_answers(self, github):
        calls, _ = github
        with installation_read_scope():
            await install_mod.list_installed_repositories("t1")
            with installation_read_scope():
                await install_mod.list_installed_repositories("t1")
            await install_mod.list_installed_repositories("t1")
        assert calls == ["t1"]

    async def test_a_task_that_outlives_the_request_reads_again(self, github):
        """Arch 2026-11-16 16:45: a task started inside the request copied the context
        and still holds the request's holder. Once the request ends it must not reuse
        the installed set, or store into it."""
        import asyncio

        calls, answers = github
        answers.extend([_installed("octo/a"), _installed("octo/a", "octo/b")])
        request_over = asyncio.Event()
        seen: List[Any] = []

        async def background():
            await request_over.wait()
            seen.append(await install_mod.list_installed_repositories("t1"))
            seen.append(await install_mod.list_installed_repositories("t1"))

        with installation_read_scope():
            await install_mod.list_installed_repositories("t1")
            task = asyncio.create_task(background())  # copies the context here
            await asyncio.sleep(0)
        request_over.set()
        await task
        assert calls == ["t1", "t1", "t1"]  # both reads after the request went to GitHub
        assert [r["full_name"] for r in seen[0].repositories] == ["octo/a", "octo/b"]

    async def test_the_middleware_opens_one_scope_per_http_request(self, github):
        from web.middleware.installation_read_scope import InstallationReadScopeMiddleware

        calls, _ = github
        held_inside: List[Any] = []

        async def app(scope, receive, send):
            await install_mod.list_installed_repositories("t1")
            await install_mod.list_installed_repositories("t1")
            held_inside.append(install_mod._request_reads.get() is not None)

        wrapped = InstallationReadScopeMiddleware(app)
        await wrapped({"type": "http"}, None, None)
        await wrapped({"type": "http"}, None, None)
        assert calls == ["t1", "t1"] and held_inside == [True, True]
        await wrapped({"type": "lifespan"}, None, None)
        assert held_inside[-1] is False and len(calls) == 4  # no scope: both calls read

    async def test_the_app_registers_the_middleware(self):
        source = open("web/app.py", encoding="utf-8").read()
        assert "app.add_middleware(InstallationReadScopeMiddleware)" in source


# --- the write half ------------------------------------------------------------------

_WRITES = {
    "create": lambda a: a.create_issue_connector(
        _OWNER, owner="octo", repo="public", title="t", body="b"
    ),
    "update": lambda a: a.update_issue_connector(
        _OWNER, owner="octo", repo="public", issue_number=7, state="closed"
    ),
    "comment": lambda a: a.add_comment_connector(
        _OWNER, owner="octo", repo="public", issue_number=7, comment="c"
    ),
}


@pytest.mark.parametrize("write_name", sorted(_WRITES))
class TestAWriteOnAnAppGrantIsNeverFiredAtARepositoryTheAppIsNotOn:
    async def test_not_installed_on_it_is_refused_with_the_write_line(
        self, monkeypatch, write_name
    ):
        adapter, seen, _ = _adapter(monkeypatch, _installed("octo/a"))
        result = await _WRITES[write_name](adapter)
        assert seen == []  # nothing was fired
        assert result.verified is False and result.refused is True
        # Not "never fired": that state sends the router to the native-token path.
        assert result.attempted is True
        assert result.degradation.detail == DETAIL_APP_NOT_ON_REPOSITORY
        assert result.degradation.user_message == gh_mod.GITHUB_APP_NOT_ON_REPOSITORY_WRITE_REPLY
        assert result.degradation.action_hint is None

    async def test_installed_nowhere_is_refused_with_the_install_step(
        self, monkeypatch, write_name
    ):
        adapter, seen, _ = _adapter(monkeypatch, _installed())
        result = await _WRITES[write_name](adapter)
        assert seen == [] and result.refused is True and result.attempted is True
        assert result.degradation.user_message == gh_mod.GITHUB_APP_NOT_INSTALLED_REPLY

    async def test_a_failed_installation_read_is_refused_and_nothing_is_fired(
        self, monkeypatch, write_name
    ):
        adapter, seen, _ = _adapter(monkeypatch, InstallationReadFailed(502))
        result = await _WRITES[write_name](adapter)
        assert seen == [] and result.refused is True
        assert result.degradation.reason is DegradationReason.UNREACHABLE

    async def test_installed_on_it_fires_the_write(self, monkeypatch, write_name):
        adapter, seen, read = _adapter(monkeypatch, _installed("octo/public"))
        await _WRITES[write_name](adapter)
        assert seen and (seen[0]["owner"], seen[0]["repo"]) == ("octo", "public")
        read.assert_awaited_once()

    @pytest.mark.parametrize(
        "credential",
        [_credential(leg="pat", app_grant=False), _credential(leg="oauth", app_grant=False)],
        ids=["personal token", "classic grant"],
    )
    async def test_the_other_legs_make_no_installation_read(
        self, monkeypatch, write_name, credential
    ):
        adapter, seen, read = _adapter(
            monkeypatch, AssertionError("no installation read"), credential=credential
        )
        await _WRITES[write_name](adapter)
        assert seen
        read.assert_not_awaited()


class TestTheRouterSaysTheLineAndNeverFallsBackToAnotherCredential:
    async def test_a_refused_write_raises_refused_with_the_write_line(self, monkeypatch):
        from services.integrations.github.github_integration_router import (
            GitHubIntegrationRouter,
            GitHubWriteRefused,
        )

        adapter, seen, _ = _adapter(monkeypatch, _installed("octo/a"))
        router = GitHubIntegrationRouter.__new__(GitHubIntegrationRouter)
        router.mcp_adapter = adapter
        router._user_id = _OWNER
        with pytest.raises(GitHubWriteRefused) as refused:
            await router._try_connector_write(
                "add_comment_connector", owner="octo", repo="public", issue_number=7, comment="c"
            )
        assert refused.value.user_message == gh_mod.GITHUB_APP_NOT_ON_REPOSITORY_WRITE_REPLY
        assert refused.value.action_hint is None
        assert seen == []


class TestTheDuplicateTitleReadBeforeACreate:
    async def test_not_installed_on_it_reads_nothing_and_answers_none(self, monkeypatch):
        adapter, seen, _ = _adapter(monkeypatch, _installed("octo/a"))
        found = await adapter.find_open_issue_by_title_connector(
            _OWNER, owner="octo", repo="public", title="t"
        )
        assert found is None and seen == []

    async def test_installed_on_it_reads(self, monkeypatch):
        adapter, seen, _ = _adapter(monkeypatch, _installed("octo/public"))
        await adapter.find_open_issue_by_title_connector(
            _OWNER, owner="octo", repo="public", title="t"
        )
        assert seen and seen[0]["repo"] == "public"


class TestTheLineSaidInPlaceOfAConfirm:
    """``github_app_write_refusal_line``: the one check the confirm builders share."""

    def _patch(self, monkeypatch, answer):
        refusal = AsyncMock(side_effect=answer) if isinstance(answer, Exception) else None
        refusal = refusal or AsyncMock(return_value=answer)
        monkeypatch.setattr(GitHubMCPSpatialAdapter, "app_write_refusal", refusal)
        return refusal

    async def test_not_on_the_repository_is_the_write_line(self, monkeypatch):
        adapter, _, _ = _adapter(monkeypatch, _installed("octo/a"))
        self._patch(monkeypatch, await adapter._not_on_repository_response())
        line = await gh_mod.github_app_write_refusal_line(_OWNER, "octo/public")
        assert line == gh_mod.GITHUB_APP_NOT_ON_REPOSITORY_WRITE_REPLY
        assert "can't read it" not in line  # the read line's reason is wrong for a write

    async def test_installed_nowhere_is_the_install_step(self, monkeypatch):
        adapter, _, _ = _adapter(monkeypatch, _installed())
        self._patch(monkeypatch, await adapter._install_step_response())
        line = await gh_mod.github_app_write_refusal_line(_OWNER, "octo/public")
        assert line == gh_mod.GITHUB_APP_NOT_INSTALLED_REPLY

    async def test_may_go_ahead_is_none(self, monkeypatch):
        self._patch(monkeypatch, None)
        assert await gh_mod.github_app_write_refusal_line(_OWNER, "octo/public") is None

    @pytest.mark.parametrize("repository", [None, "", "no-slash", "a/b c"])
    async def test_no_usable_repository_asks_nothing(self, monkeypatch, repository):
        asked = self._patch(monkeypatch, AssertionError("not asked"))
        assert await gh_mod.github_app_write_refusal_line(_OWNER, repository) is None
        asked.assert_not_awaited()

    async def test_no_principal_asks_nothing(self, monkeypatch):
        asked = self._patch(monkeypatch, AssertionError("not asked"))
        assert await gh_mod.github_app_write_refusal_line(None, "octo/public") is None
        asked.assert_not_awaited()

    async def test_a_broken_check_says_the_could_not_reach_line_in_place_of_the_confirm(
        self, monkeypatch
    ):
        # Arch 2026-11-16 16:45, CXO 16:31: a confirm offered after the check broke is
        # a yes to a write that can't succeed (the write uses the same resolver).
        self._patch(monkeypatch, RuntimeError("store down, with a secret in its text"))
        line = await gh_mod.github_app_write_refusal_line(_OWNER, "octo/public")
        # CXO 2026-11-16 17:27, verbatim. It names no cause and no machinery.
        assert line == (
            "I couldn't check whether the Piper GitHub app is installed on that repository, "
            "so I haven't done anything. Try again in a moment."
        )
        assert line == gh_mod.GITHUB_APP_WRITE_CHECK_FAILED_REPLY
        assert "secret" not in line and "MCP" not in line

    async def test_a_broken_check_lets_a_draft_go_ahead(self, monkeypatch):
        # A draft arms no write; the confirm that follows makes the check.
        self._patch(monkeypatch, RuntimeError("store down"))
        assert (
            await gh_mod.github_app_write_refusal_line(_OWNER, "octo/public", drafting=True) is None
        )

    async def test_app_write_refusal_on_an_account_with_no_credential_is_none(self, monkeypatch):
        adapter, _, read = _adapter(monkeypatch, AssertionError("no installation read"))
        adapter.resolve_credential = AsyncMock(
            return_value=await adapter.degrade(DegradationReason.CONNECT_REQUIRED)
        )
        assert await adapter.app_write_refusal(_OWNER, "octo/public") is None
        read.assert_not_awaited()


class TestTheConfirmBuilders:
    """Create and update say the line with nothing armed or bound; close and reopen
    answer it before the probe and before any confirm."""

    _LINE = "the line"

    @pytest.fixture
    def refused(self, monkeypatch):
        check = AsyncMock(return_value=self._LINE)
        monkeypatch.setattr(gh_mod, "github_app_write_refusal_line", check)
        return check

    @staticmethod
    def _intent(message, action, **context):
        from services.domain.models import Intent
        from services.shared_types import IntentCategory

        return Intent(
            category=IntentCategory.EXECUTION,
            action=action,
            confidence=1.0,
            original_message=message,
            context={"original_message": message, "user_id": _OWNER, **context},
        )

    async def test_create_says_the_line_and_binds_nothing(self, refused):
        from services.intent_service.not_performed import NOT_PERFORMED_KEY, NotPerformed
        from services.intent_service.write_confirm_words import (
            WriteAskRequest,
            create_issue_write_ask,
        )

        intent = self._intent(
            "create an issue", "create_issue", title="Login fails", repository="octo/public"
        )
        before = dict(intent.context)
        ask = await create_issue_write_ask(
            WriteAskRequest(intent=intent, message="create an issue", user_id=_OWNER)
        )
        assert ask.reply == self._LINE and ask.words is None and ask.armed is False
        assert ask.intent_data[NOT_PERFORMED_KEY] == NotPerformed.DEGRADED
        assert intent.context == before  # no bound write values
        refused.assert_awaited_once_with(_OWNER, "octo/public")

    async def test_update_says_the_line_and_binds_nothing(self, refused):
        from services.intent_service.write_confirm_words import (
            WriteAskRequest,
            update_issue_write_ask,
        )

        intent = self._intent(
            "retitle issue 7",
            "update_issue",
            issue_number=7,
            title="New title",
            repository="octo/public",
        )
        before = dict(intent.context)
        ask = await update_issue_write_ask(
            WriteAskRequest(intent=intent, message="retitle issue 7", principal=_OWNER)
        )
        assert ask.reply == self._LINE and ask.words is None
        assert intent.context == before
        refused.assert_awaited_once_with(_OWNER, "octo/public")

    async def test_create_and_update_offer_the_confirm_when_the_write_may_go_ahead(
        self, monkeypatch
    ):
        from services.intent_service.write_confirm_words import (
            WriteAskRequest,
            create_issue_write_ask,
            update_issue_write_ask,
        )

        monkeypatch.setattr(gh_mod, "github_app_write_refusal_line", AsyncMock(return_value=None))
        create = await create_issue_write_ask(
            WriteAskRequest(
                intent=self._intent(
                    "create an issue", "create_issue", title="Login fails", repository="octo/a"
                ),
                message="create an issue",
                user_id=_OWNER,
            )
        )
        assert create.reply is None and "octo/a" in create.words.question
        update = await update_issue_write_ask(
            WriteAskRequest(
                intent=self._intent(
                    "retitle issue 7",
                    "update_issue",
                    issue_number=7,
                    title="N",
                    repository="octo/a",
                ),
                message="retitle issue 7",
                user_id=_OWNER,
            )
        )
        assert update.reply is None and "octo/a" in update.words.question

    @pytest.mark.parametrize("action", ["close_issue_query", "reopen_issue_query"])
    async def test_close_and_reopen_answer_before_the_probe_and_arm_nothing(
        self, monkeypatch, refused, action
    ):
        from unittest.mock import MagicMock

        from services.intent_service.destructive_confirm import build_close_reopen_confirmation

        probe = AsyncMock(side_effect=AssertionError("no probe of that repository"))
        monkeypatch.setattr(GitHubMCPSpatialAdapter, "probe_issue_connector", probe)
        verb = "close" if action.startswith("close") else "reopen"
        intent = self._intent(f"{verb} issue 7 in octo/public", action, repository="octo/public")
        gate = await build_close_reopen_confirmation(intent, MagicMock(), None)
        from services.intent_service.not_performed import NOT_PERFORMED_KEY, NotPerformed

        assert gate.offer is None
        assert gate.passthrough_result == {
            "message": self._LINE,
            "requires_clarification": False,
            # Arch 2026-11-16 16:45: the same marker create and update carry.
            "intent_data": {
                NOT_PERFORMED_KEY: NotPerformed.DEGRADED,
                "repository": "octo/public",
            },
        }
        probe.assert_not_awaited()
        refused.assert_awaited_once_with(_OWNER, "octo/public")

    @pytest.mark.parametrize("builder", ["create", "update", "close", "reopen"])
    async def test_a_broken_check_says_could_not_reach_and_arms_nothing(self, monkeypatch, builder):
        """The real line function over a check that raises, through each of the four
        confirm builders."""
        from unittest.mock import MagicMock

        from services.intent_service.destructive_confirm import build_close_reopen_confirmation
        from services.intent_service.write_confirm_words import (
            WriteAskRequest,
            create_issue_write_ask,
            update_issue_write_ask,
        )

        monkeypatch.setattr(
            GitHubMCPSpatialAdapter,
            "app_write_refusal",
            AsyncMock(side_effect=RuntimeError("store down")),
        )
        probe = AsyncMock(side_effect=AssertionError("no probe"))
        monkeypatch.setattr(GitHubMCPSpatialAdapter, "probe_issue_connector", probe)
        unreachable = gh_mod.GITHUB_APP_WRITE_CHECK_FAILED_REPLY
        if builder == "create":
            intent = self._intent(
                "create an issue", "create_issue", title="Login fails", repository="octo/public"
            )
            ask = await create_issue_write_ask(
                WriteAskRequest(intent=intent, message="create an issue", user_id=_OWNER)
            )
            assert ask.reply == unreachable and ask.words is None and ask.armed is False
        elif builder == "update":
            intent = self._intent(
                "retitle issue 7",
                "update_issue",
                issue_number=7,
                title="N",
                repository="octo/public",
            )
            ask = await update_issue_write_ask(
                WriteAskRequest(intent=intent, message="retitle issue 7", user_id=_OWNER)
            )
            assert ask.reply == unreachable and ask.words is None and ask.armed is False
        else:
            intent = self._intent(
                f"{builder} issue 7 in octo/public",
                f"{builder}_issue_query",
                repository="octo/public",
            )
            gate = await build_close_reopen_confirmation(intent, MagicMock(), None)
            assert gate.offer is None
            assert gate.passthrough_result["message"] == unreachable
            probe.assert_not_awaited()


class TestTheCreateDraftStep:
    """CXO 2026-11-16 16:08: the line replaces the create's draft offer entirely. The
    handler's draft step ("help me write a ticket …") answers it before a draft is
    offered or armed; a named repository and the default a write would use both count."""

    _GATE = "services.intent_service.collaboration_gate"
    _ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
    _TARGET = "services.integrations.github.repo_resolver.get_user_write_target"
    _DEFAULT = "services.integrations.github.repo_resolver.get_user_default_repo"

    @staticmethod
    def _draft_intent(message):
        from services.domain.models import Intent
        from services.shared_types import IntentCategory

        return Intent(
            original_message=message,
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            confidence=0.95,
            context={},
        )

    async def _run(self, monkeypatch, message, *, line, default="octo/default"):
        from unittest.mock import patch

        from services.intent.intent_service import IntentService

        check = AsyncMock(return_value=line)
        monkeypatch.setattr(gh_mod, "github_app_write_refusal_line", check)
        service = IntentService()
        armed = []
        monkeypatch.setattr(
            service.workflow_offer_service,
            "set_pending_offer",
            lambda *a, **k: armed.append(a),
        )
        with (
            patch(f"{self._GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{self._ROUTER}.initialize", new=AsyncMock()),
            patch(f"{self._ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{self._ROUTER}.create_issue", new=AsyncMock()) as write,
            patch(self._TARGET, new=AsyncMock(return_value=default)),
            patch(self._DEFAULT, new=AsyncMock(return_value=default)),
        ):
            result = await service._handle_create_issue(
                self._draft_intent(message), "wf-1", "sess-1", user_id=_OWNER
            )
        write.assert_not_awaited()
        return result, check, armed

    async def test_a_named_repository_the_app_is_not_on_gets_the_line_and_no_draft(
        self, monkeypatch
    ):
        from services.intent_service.not_performed import NOT_PERFORMED_KEY, NotPerformed

        result, check, armed = await self._run(
            monkeypatch,
            "help me write a ticket about the login timeout in octo/public",
            line="the line",
        )
        assert result.message == "the line"
        assert result.success is False and result.requires_clarification is False
        assert result.intent_data[NOT_PERFORMED_KEY] == NotPerformed.DEGRADED
        assert not result.intent_data.get("collaboration_gate")
        assert armed == []  # no draft was armed
        check.assert_awaited_once_with(_OWNER, "octo/public", drafting=True)

    async def test_no_repository_named_checks_the_default_a_write_would_use(self, monkeypatch):
        result, check, armed = await self._run(
            monkeypatch, "help me write a ticket about the login timeout", line="the line"
        )
        assert result.message == "the line" and armed == []
        check.assert_awaited_once_with(_OWNER, "octo/default", drafting=True)

    async def test_the_draft_is_offered_when_the_write_may_go_ahead(self, monkeypatch):
        result, check, armed = await self._run(
            monkeypatch, "help me write a ticket about the login timeout", line=None
        )
        assert result.intent_data.get("collaboration_gate") is True
        assert "login timeout" in result.message
        assert armed  # the draft was armed as before
        check.assert_awaited_once()
