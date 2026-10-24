"""#2040 part 1 — the empty open-issues line names its scope.

Web's served run on 6f2916d10f (``web-pat-test``, default repo with 7 open
issues, none assigned): ``what open issues do I have?`` → "You don't have any
open issues right now." The OAuth connector read is ``assignee:@me`` (the
user-wide default query in ``GitHubMCPSpatialAdapter.list_open_issues``), so
the line was true only under a scope the user was never told.

CXO's ruling: the empty line names its scope ("You have no open issues
assigned to you."), and when the default repo has open issues the scope
excluded, it says so as a STATEMENT pointing at them. The count comes from
one extra read, only in the empty case: the same adapter's
``list_open_issues`` scoped to the user's default repo with a one-item page
(``total`` is the search's own ``total_count``). No new adapter method.

Layer: the REAL ``_handle_list_issues_query`` with the adapter stubbed at its
method and the default-repo store stubbed. Not a served run.

Also pinned here: the capped-list boundary for issues at ``cap=5`` and
``REMAINDER_OFFER_THRESHOLD=3`` — 7 and 8 open issues render whole with no
offer; 9 is the first count that shows 5 plus the offer and arms the rest.
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.conversation_context import get_or_create_context
from services.intent_service.list_remainder import REMAINDER_OFFER_THRESHOLD
from services.intent_service.workflow_entries import register_default_workflows
from services.mcp.consumer.github_adapter import GitHubIssuesResult
from services.shared_types import IntentCategory

_USER = "6b3d2e40-2040-4b00-9e00-000000002040"
_REPO = "dinp-machine/piper-test-activity"
_ADAPTER = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.list_open_issues"
_DEFAULT_REPO = "services.integrations.github.repo_resolver.get_user_default_repo"

SCOPED = "You have no open issues assigned to you."


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name}); this read is deterministic")


@pytest.fixture
def svc():
    register_default_workflows()
    return IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))


def _intent(message="what open issues do I have?"):
    return Intent(
        category=IntentCategory.QUERY,
        action="list_issues_query",
        confidence=0.95,
        original_message=message,
        context={"original_message": message, "user_id": _USER},
    )


def _issue(n):
    return {"number": n, "title": f"test issue {n}", "labels": []}


class _Adapter:
    """Records every ``list_open_issues`` call; answers by scope."""

    def __init__(self, *, assigned=(), repo_total=0, repo_degraded=False, repo_raises=False):
        self.calls: list[tuple] = []
        self.assigned = list(assigned)
        self.repo_total = repo_total
        self.repo_degraded = repo_degraded
        self.repo_raises = repo_raises

    @property
    def method(self):
        """A plain function, so ``patch`` binds it as the adapter method."""

        async def list_open_issues(_self, user_id, *, limit=50, repository=None):
            return await self._answer(repository, limit)

        return list_open_issues

    async def _answer(self, repository, limit):
        self.calls.append((repository, limit))
        if repository is None:
            return GitHubIssuesResult(issues=self.assigned, total=len(self.assigned))
        if self.repo_raises:
            raise RuntimeError("server unreachable")
        if self.repo_degraded:
            return GitHubIssuesResult(degradation=MagicMock())
        page = [_issue(n) for n in range(self.repo_total, 0, -1)][:limit]
        return GitHubIssuesResult(issues=page, total=self.repo_total)


async def _run(svc, adapter, *, default_repo=_REPO, message="what open issues do I have?"):
    with (
        patch(_ADAPTER, new=adapter.method),
        patch(_DEFAULT_REPO, new=AsyncMock(return_value=default_repo)),
    ):
        return await svc._handle_list_issues_query(_intent(message), "wf-2040", None)


class TestEmptyLineNamesItsScope:
    pytestmark = pytest.mark.asyncio

    async def test_empty_assigned_with_repo_issues_states_the_count_and_points(self, svc):
        """Web's served case: none assigned, 7 open in the default repo."""
        adapter = _Adapter(repo_total=7)
        result = await _run(svc, adapter)
        assert result.message == (
            "You have no open issues assigned to you. "
            f"There are 7 open issues in {_REPO}. "
            f"Say 'show open issues in {_REPO}' to see them."
        )
        assert "?" not in result.message  # a statement: the unarmed-ask census is unchanged
        assert "don't have any open issues" not in result.message
        # One extra read, only in the empty case, a one-item page of the default repo.
        assert adapter.calls == [(None, 50), (_REPO, 1)]
        ctx = result.intent_data["context"]
        assert ctx["issue_count"] == 0
        assert ctx["scope"] == "assigned_to_you"
        assert ctx["default_repo"] == _REPO
        assert ctx["default_repo_open_issue_count"] == 7
        assert "list_remainder_offer_pending" not in result.intent_data

    async def test_one_repo_issue_is_singular(self, svc):
        result = await _run(svc, _Adapter(repo_total=1))
        assert result.message == (
            f"{SCOPED} There is 1 open issue in {_REPO}. "
            f"Say 'show open issues in {_REPO}' to see them."
        )

    async def test_empty_assigned_and_empty_repo_is_the_scoped_line_only(self, svc):
        adapter = _Adapter(repo_total=0)
        result = await _run(svc, adapter)
        assert result.message == SCOPED
        assert adapter.calls == [(None, 50), (_REPO, 1)]
        assert result.intent_data["context"]["default_repo_open_issue_count"] == 0

    async def test_no_default_repo_is_the_scoped_line_only_and_no_extra_read(self, svc):
        adapter = _Adapter(repo_total=7)
        result = await _run(svc, adapter, default_repo=None)
        assert result.message == SCOPED
        assert adapter.calls == [(None, 50)]
        assert "default_repo" not in result.intent_data["context"]

    @pytest.mark.parametrize("failure", ["repo_degraded", "repo_raises"])
    async def test_a_count_it_could_not_read_is_never_stated(self, svc, failure):
        adapter = _Adapter(repo_total=7, **{failure: True})
        result = await _run(svc, adapter)
        assert result.success
        assert result.message == SCOPED

    async def test_the_named_repo_variant_is_repo_wide_and_keeps_its_line(self, svc):
        """A named repo is read ``repo:<name> is:issue is:open`` (repo-wide, no
        assignee filter), so "No open issues in <repo> right now." already
        names the whole scope; no extra read."""
        adapter = _Adapter(repo_total=0)
        result = await _run(svc, adapter, message=f"what open issues are in {_REPO}?")
        assert result.message == f"No open issues in {_REPO} right now."
        assert adapter.calls == [(_REPO, 50)]
        assert "scope" not in result.intent_data["context"]

    async def test_the_pointed_phrasing_scopes_the_read_to_that_repo(self, svc):
        """The statement teaches only what the handler cashes: the quoted
        phrasing, reaching this handler, reads that repo's open issues
        (the #1388 named-repo slot-fill). Routing it here is the
        classifier's; this pins the handler half."""
        adapter = _Adapter(repo_total=7)
        result = await _run(svc, adapter, message=f"show open issues in {_REPO}")
        assert adapter.calls == [(_REPO, 50)]
        assert "#7" in result.message and "#1" in result.message

    async def test_a_non_empty_assigned_read_makes_no_extra_read(self, svc):
        adapter = _Adapter(assigned=[_issue(3), _issue(2)], repo_total=7)
        result = await _run(svc, adapter)
        assert adapter.calls == [(None, 50)]
        assert result.message.startswith("You have **2 open issues**.")

    async def test_the_native_pat_fallback_line_is_unchanged(self, svc):
        """Not connected via OAuth: the native router lists the resolved
        default repo (repo-wide, not assignee-scoped), so "assigned to you"
        would be false there. Its empty line is untouched; no extra read."""
        from services.mcp.consumer.connector import DegradationReason

        not_connected = SimpleNamespace(
            issues=None,
            total=None,
            degradation=SimpleNamespace(
                reason=DegradationReason.CONNECT_REQUIRED, user_message="connect github"
            ),
        )
        adapter = MagicMock()
        adapter.list_open_issues = AsyncMock(return_value=not_connected)
        router = MagicMock()
        router.initialize = AsyncMock(return_value=None)
        router.get_open_issues = AsyncMock(return_value=[])
        router.get_open_items_strict = router.get_open_issues  # #2151 GH-NONSTRICT
        with (
            patch(
                "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter",
                return_value=adapter,
            ),
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
                return_value=router,
            ),
            patch(_DEFAULT_REPO, new=AsyncMock(return_value=_REPO)) as default_repo,
        ):
            result = await svc._handle_list_issues_query(_intent(), "wf-2040", None)
        assert result.message == "You don't have any open issues right now."
        assert adapter.list_open_issues.await_count == 1
        default_repo.assert_not_awaited()


class TestIssuesCapBoundary:
    """Confirmed, not changed: ``compose_capped_list(cap=5)`` with
    ``REMAINDER_OFFER_THRESHOLD=3`` shows the whole list while the hidden tail
    is 3 or fewer, so 7 AND 8 open issues render whole with no "That's 5 of N"
    line; 9 is the first count that shows five, offers, and arms the rest."""

    def test_the_threshold_is_three(self):
        assert REMAINDER_OFFER_THRESHOLD == 3

    async def _list(self, svc, n, sid):
        get_or_create_context(sid, user_id=_USER).pending_list_remainder = None
        adapter = _Adapter(assigned=[_issue(k) for k in range(n, 0, -1)])
        with patch(_ADAPTER, new=adapter.method):
            result = await svc._handle_list_issues_query(_intent(), "wf-2040", sid)
        return result, get_or_create_context(sid, user_id=_USER).pending_list_remainder

    @pytest.mark.asyncio
    @pytest.mark.parametrize("n", [7, 8])
    async def test_seven_and_eight_render_whole_with_no_arm(self, svc, n):
        result, stored = await self._list(svc, n, f"2040-cap-{n}")
        assert result.message.count("\n- **#") == n
        assert "That's 5 of" not in result.message
        assert "say the word" not in result.message
        assert stored is None
        assert "list_remainder_offer_pending" not in result.intent_data

    @pytest.mark.asyncio
    async def test_nine_shows_five_offers_and_arms_four(self, svc):
        result, stored = await self._list(svc, 9, "2040-cap-9")
        assert result.message.count("\n- **#") == 5
        assert "That's 5 of 9 — say the word and I'll pull the rest." in result.message
        assert result.intent_data["list_remainder_offer_pending"] is True
        assert stored is not None and len(stored.lines) == 4
        assert stored.lines[0] == "\n- **#4**: test issue 4"
