"""Tests for #1155: PRIORITY floor consumes connected GitHub data.

The PRIORITY context previously set `github_connected=true` but never pulled the
open issues, so the floor composed "no project visibility." These cover the new
high-priority-issues gatherer (ranking + fail-graceful) and the floor formatter
that surfaces it.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.intent_service.context_assembler import ContextAssembler


class _NoOpCache:
    """No-op stand-in so ContextAssembler() needs no Redis."""

    async def get_or_compute(self, key, ttl_seconds, compute_fn):
        return await compute_fn()


@pytest.fixture(autouse=True)
def _patch_context_cache(monkeypatch):
    monkeypatch.setattr(
        "services.intent_service.context_assembler.ContextCache",
        lambda *args, **kwargs: _NoOpCache(),
    )


def _issue(number, title, labels, updated_at):
    return {
        "number": number,
        "title": title,
        "labels": labels,
        "updated_at": updated_at,
        "uri": f"https://github.test/{number}",
    }


def _patch_router(open_issues):
    """Patch GitHubIntegrationRouter so initialize()/get_open_issues() are mocked."""
    router = MagicMock()
    router.initialize = AsyncMock(return_value=None)
    router.get_open_issues = AsyncMock(return_value=open_issues)
    return patch(
        "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
        return_value=router,
    )


def _patch_resolve_repo(unresolved: bool):
    """#1226 Phase 3: patch repo_resolver.resolve_repo — raise UnresolvedRepoError
    (no repo configured) or return a resolved repo."""
    from services.integrations.github.repo_resolver import UnresolvedRepoError

    if unresolved:
        mock = AsyncMock(side_effect=UnresolvedRepoError("no repo"))
    else:
        mock = AsyncMock(return_value=MagicMock(full_name="o/r", owner="o", name="r"))
    return patch("services.integrations.github.repo_resolver.resolve_repo", new=mock)


class TestComputeHighPriorityIssues:
    @pytest.mark.asyncio
    async def test_ranks_priority_labeled_first_then_recency(self):
        issues = [
            _issue(1, "high old", ["priority: high"], "2026-06-01"),
            _issue(2, "unlabeled recent", [], "2026-06-05"),
            _issue(3, "critical", ["priority: critical"], "2026-05-01"),
            _issue(4, "high recent", ["priority: high"], "2026-06-03"),
        ]
        with _patch_router(issues):
            result = await ContextAssembler()._compute_high_priority_issues("uid")
        assert result is not None
        order = [i["number"] for i in result["high_priority_issues"]]
        # critical(3) first; then high tier by recency (4 before 1); unlabeled(2) last.
        assert order == [3, 4, 1, 2]
        assert result["open_issue_count"] == 4

    @pytest.mark.asyncio
    async def test_empty_with_repo_returns_none(self):
        # Repo IS configured but genuinely has zero open issues → None (stays silent/normal).
        with _patch_router([]), _patch_resolve_repo(unresolved=False):
            result = await ContextAssembler()._compute_high_priority_issues("uid")
        assert result is None

    @pytest.mark.asyncio
    async def test_no_repo_returns_unconfigured_flag(self):
        # #1226 Phase 3: empty + NO repo resolves → honest-degrade signal (not a silent None).
        with _patch_router([]), _patch_resolve_repo(unresolved=True):
            result = await ContextAssembler()._compute_high_priority_issues("uid")
        assert result == {
            "high_priority_issues": [],
            "open_issue_count": 0,
            "github_repo_unconfigured": True,
        }

    @pytest.mark.asyncio
    async def test_caps_at_five(self):
        issues = [_issue(n, f"t{n}", [], f"2026-06-{n:02d}") for n in range(1, 9)]
        with _patch_router(issues):
            result = await ContextAssembler()._compute_high_priority_issues("uid")
        assert len(result["high_priority_issues"]) == 5
        assert result["open_issue_count"] == 8

    @pytest.mark.asyncio
    async def test_router_error_is_fail_graceful(self):
        router = MagicMock()
        router.initialize = AsyncMock(side_effect=RuntimeError("boom"))
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ):
            result = await ContextAssembler()._compute_high_priority_issues("uid")
        assert result is None


class TestGatherHighPriorityIssues:
    @pytest.mark.asyncio
    async def test_no_user_returns_empty(self):
        result = await ContextAssembler()._gather_high_priority_issues_context(None)
        assert result == {}

    @pytest.mark.asyncio
    async def test_gather_threads_unconfigured_flag(self):
        # #1226 Phase 3: the no-repo signal survives the cache unpack → reaches domain_context.
        with _patch_router([]), _patch_resolve_repo(unresolved=True):
            result = await ContextAssembler()._gather_high_priority_issues_context("uid")
        assert result.get("github_repo_unconfigured") is True


class TestFloorFormatsHighPriorityIssues:
    def _floor(self):
        from services.intent_service.conversational_floor import ConversationalFloor

        return ConversationalFloor(llm_client=MagicMock())

    def test_high_priority_issues_rendered(self):
        ctx = {
            "high_priority_issues": [
                {"number": 42, "title": "Fix the thing", "labels": ["priority: high"]},
                {"number": 7, "title": "Another", "labels": []},
            ],
            "open_issue_count": 12,
        }
        out = self._floor()._format_domain_context(ctx)
        assert "High-priority open issues" in out
        assert "12 open" in out
        assert "#42" in out and "Fix the thing" in out
        assert "[priority: high]" in out
        assert "#7" in out

    def test_empty_high_priority_issues_no_section(self):
        out = self._floor()._format_domain_context({"high_priority_issues": []})
        assert "High-priority open issues" not in out

    def test_unconfigured_repo_renders_honest_message(self):
        # #1226 Phase 3: no repo configured → floor context tells the user to set one,
        # explicitly NOT implying they simply have zero open issues.
        out = self._floor()._format_domain_context({"github_repo_unconfigured": True})
        assert "not configured" in out.lower()
        assert "Settings" in out
        assert "do not imply" in out.lower()
