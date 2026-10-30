"""#2151 FLOOR-ABSENT, the STATUS gather (Arch 2026-10-29 21:08, decisions.log).

A failed read inside ``ContextAssembler._gather_status_priority_context`` reaches the floor
prompt as a STATED failure ("DATA CHECKS FAILED this turn — could not check: <source>"),
never as nothing. Two reads in the gather still turned a failure into silence or a
verified-sounding claim:

- **user context** (projects, priorities, organization): ``UserContextService`` swallowed a
  failed projects or preferences DB read and served PIPER.md's generic projects and
  priorities as the user's; the assembler's own catch returned None with no flag.
- **the default repo under the open-issues read**: ``resolve_repo`` reads the user's
  default repo best-effort, so a failed DB read became ``UnresolvedRepoError`` and the
  floor said "GitHub repository: not configured for this user".

Each read is pinned in its four states where they apply: FAILED arms the flag and the
composed prompt names the check; NOT PERFORMED arms nothing; VERIFIED-EMPTY keeps its
existing wording.

LAYER: unit, the gather and the floor's real prompt builder (the model is a MagicMock and
is never called). Not served: a forced read failure cannot be produced on alpha.
"""

from __future__ import annotations

from typing import Any, Dict, Optional
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

import pytest

from services.intent_service.context_assembler import ContextAssembler, _UserContextReadFailed
from services.intent_service.conversational_floor import (
    SOURCE_FAILED_FLAGS,
    ConversationalFloor,
    FloorContext,
)
from services.user_context_service import UserContext, UserContextService

UID = "00000000-0000-0000-0000-000000002151"
AGGREGATE_PREFIX = "- DATA CHECKS FAILED this turn — could not check: "
UNCONFIGURED_LINE = "- GitHub repository: not configured for this user."
LABELS = {entry.flag: entry.check_name for entry in SOURCE_FAILED_FLAGS}


class _NoOpCache:
    async def get_or_compute(self, key, ttl_seconds, compute_fn):
        return await compute_fn()


@pytest.fixture(autouse=True)
def _patch_context_cache(monkeypatch):
    monkeypatch.setattr(
        "services.intent_service.context_assembler.ContextCache",
        lambda *args, **kwargs: _NoOpCache(),
    )


def _prompt(domain_context: Dict[str, Any]) -> str:
    ctx = FloorContext(
        user_message="what am I working on?",
        session_id="pin-2151-status",
        domain_context=domain_context,
    )
    return ConversationalFloor(llm_client=MagicMock())._build_prompt(ctx)


def _failed_checks(prompt: str) -> set:
    for line in prompt.splitlines():
        if line.strip().startswith(AGGREGATE_PREFIX.strip()):
            listed = line.strip()[len(AGGREGATE_PREFIX.strip()) :].split(".", 1)[0]
            return {name.strip() for name in listed.split(",")}
    return set()


async def _status_gather(user_ctx: Optional[UserContext], user_id: Optional[str] = UID):
    """The real STATUS gather, its other reads held verified-empty, over a stubbed
    ``user_context_service.get_user_context``."""
    assembler = ContextAssembler()
    empty = AsyncMock(return_value={})
    iss = MagicMock()
    iss.return_value.get_status = AsyncMock(return_value={"configured": True})
    with (
        patch.object(ContextAssembler, "_gather_calendar_context", empty),
        patch.object(ContextAssembler, "_get_pending_todos_cached", AsyncMock(return_value=None)),
        patch.object(ContextAssembler, "_gather_blocked_items_context", empty),
        patch.object(ContextAssembler, "_gather_active_milestones_context", empty),
        patch.object(ContextAssembler, "_gather_recent_activity_context", empty),
        patch.object(ContextAssembler, "_gather_high_priority_issues_context", empty),
        patch("services.integrations.integration_status_service.IntegrationStatusService", iss),
        patch(
            "services.user_context_service.user_context_service.get_user_context",
            AsyncMock(return_value=user_ctx),
        ) as get_ctx,
    ):
        out = await assembler._gather_status_priority_context(user_id)
    return out, get_ctx


# ─── The registry entry ─────────────────────────────────────────────────────


def test_priorities_flag_is_registered_with_a_noun_label():
    assert LABELS["priorities_source_failed"] == "priorities"
    assert LABELS["projects_source_failed"] == "projects"


# ─── User context: projects ─────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_failed_projects_read_is_stated_and_the_fallback_is_not_served():
    ctx = UserContext(
        user_id=UUID(UID),
        projects=["Generic PIPER.md project"],
        projects_source="config",
        priorities=["Ship the thing"],
        projects_read_failed=True,
    )
    out, _ = await _status_gather(ctx)
    assert out["projects_source_failed"] is True
    assert "projects" not in out and "project_count" not in out
    # The part that was read still renders (CXO: one failure never blanks the rest).
    assert out["priorities"]["user_priorities"] == ["Ship the thing"]
    assert "priorities_source_failed" not in out
    prompt = _prompt(out)
    assert _failed_checks(prompt) == {"projects"}
    assert "Generic PIPER.md project" not in prompt


@pytest.mark.asyncio
async def test_user_context_read_that_raises_is_stated_for_both_checks():
    assembler = ContextAssembler()
    with (
        patch(
            "services.user_context_service.user_context_service.get_user_context",
            AsyncMock(side_effect=RuntimeError("fake: the user-context read failed")),
        ),
        pytest.raises(_UserContextReadFailed) as raised,
    ):
        await assembler._compute_user_context(UID)
    assert set(raised.value.flags) == {"projects_source_failed", "priorities_source_failed"}
    assert raised.value.partial == {}


@pytest.mark.asyncio
async def test_gather_states_a_user_context_read_that_raised():
    with patch.object(
        ContextAssembler,
        "_get_user_context_cached",
        AsyncMock(
            side_effect=_UserContextReadFailed(
                {}, ("projects_source_failed", "priorities_source_failed")
            )
        ),
    ):
        out, _ = await _status_gather(None)
    assert out["projects_source_failed"] is True
    assert out["priorities_source_failed"] is True
    assert _failed_checks(_prompt(out)) == {"projects", "priorities"}


@pytest.mark.asyncio
async def test_not_performed_with_no_user_reads_nothing_and_states_nothing():
    ctx = UserContext(user_id=UUID(UID), projects_read_failed=True)
    out, get_ctx = await _status_gather(ctx, user_id=None)
    get_ctx.assert_not_awaited()
    assert "projects_source_failed" not in out
    assert "priorities_source_failed" not in out
    assert "projects" not in _failed_checks(_prompt(out))


@pytest.mark.asyncio
async def test_verified_projects_render_as_before_with_no_flag():
    ctx = UserContext(user_id=UUID(UID), projects=["Alpha", "Beta"], projects_source="database")
    out, _ = await _status_gather(ctx)
    assert out["projects"] == [{"name": "Alpha"}, {"name": "Beta"}]
    assert out["project_count"] == 2
    assert "projects_source_failed" not in out
    assert not _failed_checks(_prompt(out))


@pytest.mark.asyncio
async def test_verified_empty_context_adds_nothing_and_states_no_failure():
    out, _ = await _status_gather(UserContext(user_id=UUID(UID)))
    assert not {"projects", "priorities", "projects_source_failed"} & set(out)
    assert not _failed_checks(_prompt(out))


# ─── User context: preferences (priorities, organization) ───────────────────


@pytest.mark.asyncio
async def test_failed_preferences_read_is_stated_and_generic_priorities_are_not_served():
    ctx = UserContext(
        user_id=UUID(UID),
        organization="Generic Org",
        projects=["Alpha"],
        projects_source="database",
        priorities=["Generic PIPER.md priority"],
        preferences_read_failed=True,
    )
    out, _ = await _status_gather(ctx)
    assert out["priorities_source_failed"] is True
    assert "priorities" not in out and "organization" not in out
    assert out["projects"] == [{"name": "Alpha"}]
    prompt = _prompt(out)
    assert _failed_checks(prompt) == {"priorities"}
    assert "Generic PIPER.md priority" not in prompt


# ─── UserContextService: a failed read is marked, and never cached ──────────


def _service(projects: Any, prefs: Any) -> UserContextService:
    svc = UserContextService()
    svc._load_projects_from_db = AsyncMock(return_value=projects)  # type: ignore[method-assign]
    svc._load_user_preferences_from_db = AsyncMock(return_value=prefs)  # type: ignore[method-assign]
    return svc


@pytest.mark.asyncio
async def test_service_marks_a_failed_projects_read_and_does_not_cache_it():
    svc = _service(projects=None, prefs={})
    ctx = await svc.get_user_context(session_id=None, user_id=UUID(UID))
    assert ctx.projects_read_failed is True
    assert ctx.preferences_read_failed is False
    assert svc.cache == {}


@pytest.mark.asyncio
async def test_service_marks_a_failed_preferences_read_and_does_not_cache_it():
    svc = _service(projects=[], prefs=None)
    ctx = await svc.get_user_context(session_id=None, user_id=UUID(UID))
    assert ctx.preferences_read_failed is True
    # No project rows, so the projects fallback is the preferences read that failed.
    assert ctx.projects_read_failed is True
    assert svc.cache == {}


@pytest.mark.asyncio
async def test_service_verified_empty_reads_are_not_failures_and_are_cached():
    svc = _service(projects=[], prefs={})
    ctx = await svc.get_user_context(session_id=None, user_id=UUID(UID))
    assert ctx.projects_read_failed is False
    assert ctx.preferences_read_failed is False
    assert f"user:{UID}" in svc.cache


@pytest.mark.asyncio
async def test_service_cache_hit_whose_reread_fails_is_marked_on_a_copy():
    svc = _service(projects=["Alpha"], prefs={})
    first = await svc.get_user_context(session_id=None, user_id=UUID(UID))
    assert first.projects == ["Alpha"] and not first.projects_read_failed
    svc._load_projects_from_db = AsyncMock(return_value=None)  # type: ignore[method-assign]
    second = await svc.get_user_context(session_id=None, user_id=UUID(UID))
    assert second.projects_read_failed is True
    # The cached context is untouched, so the next successful re-read is clean.
    assert svc.cache[f"user:{UID}"].projects_read_failed is False


@pytest.mark.asyncio
async def test_loaders_return_none_on_a_failed_read():
    svc = UserContextService()
    with patch(
        "services.database.session_factory.AsyncSessionFactory.session_scope_fresh",
        side_effect=RuntimeError("fake: the database is unreachable"),
    ):
        assert await svc._load_projects_from_db(UUID(UID)) is None
        assert await svc._load_user_preferences_from_db(UUID(UID)) is None


# ─── The default repo under the open-issues read ────────────────────────────


def _router_with_no_issues():
    from services.integrations.github.github_integration_router import GitHubIntegrationRouter
    from services.mcp.consumer.github_adapter import GitHubIssuesResult

    router = GitHubIntegrationRouter.__new__(GitHubIntegrationRouter)
    router._initialized = True
    router._user_id = UID
    adapter = MagicMock()
    adapter.list_open_issues = AsyncMock(return_value=GitHubIssuesResult(issues=[], total=0))
    router.mcp_adapter = adapter
    router.spatial_github = None
    # The router's own resolver is best-effort: a failed default-repo read is None here.
    router._resolve_default_repo = AsyncMock(return_value=None)
    return router


async def _hp_gather(default_repo_read: AsyncMock, router=None):
    from services.integrations.github.repo_resolver import UnresolvedRepoError

    router = router or _router_with_no_issues()
    with (
        patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ),
        patch(
            "services.integrations.github.repo_resolver.resolve_repo",
            AsyncMock(side_effect=UnresolvedRepoError("no repo resolved")),
        ),
        patch(
            "services.integrations.github.repo_resolver.get_user_default_repo_and_source",
            default_repo_read,
        ),
    ):
        return await ContextAssembler()._gather_high_priority_issues_context(UID)


@pytest.mark.asyncio
async def test_failed_default_repo_read_is_stated_never_not_configured():
    from sqlalchemy.exc import OperationalError

    read = AsyncMock(side_effect=OperationalError("fake", None, Exception("fake")))
    out = await _hp_gather(read)
    assert out == {"open_issues_source_failed": True}
    read.assert_awaited_once_with(UUID(UID), strict=True)
    prompt = _prompt(out)
    assert _failed_checks(prompt) == {"open issues"}
    assert UNCONFIGURED_LINE not in prompt


@pytest.mark.asyncio
async def test_verified_absent_default_repo_keeps_the_unconfigured_wording():
    out = await _hp_gather(AsyncMock(return_value=(None, None)))
    assert out.get("github_repo_unconfigured") is True
    assert "open_issues_source_failed" not in out
    prompt = _prompt(out)
    assert UNCONFIGURED_LINE in prompt
    assert not _failed_checks(prompt)


@pytest.mark.asyncio
async def test_not_connected_github_is_not_performed():
    from services.mcp.consumer.connector import DegradationReason, DegradationResponse
    from services.mcp.consumer.github_adapter import GitHubIssuesResult

    router = _router_with_no_issues()
    router._resolve_default_repo = AsyncMock(return_value=("o", "r"))
    router.mcp_adapter.list_open_issues = AsyncMock(
        return_value=GitHubIssuesResult(
            degradation=DegradationResponse(
                reason=DegradationReason.CONNECT_REQUIRED, user_message="fake degrade"
            )
        )
    )
    read = AsyncMock(return_value=(None, None))
    out = await _hp_gather(read, router=router)
    assert out == {}
    read.assert_not_awaited()
    prompt = _prompt(out)
    assert not _failed_checks(prompt)
    assert UNCONFIGURED_LINE not in prompt


@pytest.mark.asyncio
async def test_strict_default_repo_read_raises_and_the_default_still_swallows():
    from services.integrations.github import repo_resolver

    with patch(
        "services.database.session_factory.AsyncSessionFactory.session_scope",
        side_effect=RuntimeError("fake: the database is unreachable"),
    ):
        assert await repo_resolver.get_user_default_repo_and_source(UUID(UID)) == (None, None)
        with pytest.raises(RuntimeError):
            await repo_resolver.get_user_default_repo_and_source(UUID(UID), strict=True)
