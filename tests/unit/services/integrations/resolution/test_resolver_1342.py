"""#1342 Inc 2 — the connector-agnostic resolve_target() entry point.

Arch ruling (2026-07-01): a SEPARATE resolution service; GitHub-only for now (m-40).
resolve_target() dispatches to resolve_repo for connector="github" and wraps via
.to_target() — no existing resolve_repo caller changes; this is the additive seam.
"""

import pytest

from services.integrations.github.repo_resolver import UnresolvedRepoError, resolve_repo
from services.integrations.resolution import ResolvedTarget, resolve_target

pytestmark = pytest.mark.asyncio


async def test_github_explicit_resolves_and_wraps():
    target = await resolve_target("github", explicit="octocat/hello-world")

    assert isinstance(target, ResolvedTarget)
    assert target.connector == "github"
    assert target.source == "explicit"
    assert target.payload.full_name == "octocat/hello-world"


async def test_matches_calling_resolve_repo_directly_then_to_target():
    # resolve_target must not alter resolve_repo's behavior — same result either way.
    direct = await resolve_repo(explicit="owner/name")
    via_seam = await resolve_target("github", explicit="owner/name")

    assert via_seam == direct.to_target()


async def test_github_unresolved_raises_the_github_specific_error():
    # No explicit/project/user_id/env fallback → the underlying UnresolvedRepoError
    # propagates unchanged (no generic exception invented prematurely, m-40).
    with pytest.raises(UnresolvedRepoError):
        await resolve_target("github")


async def test_unsupported_connector_raises_not_implemented_not_silent():
    # A connector-agnostic name that isn't built yet must fail LOUDLY, never
    # silently return an empty/None target.
    with pytest.raises(NotImplementedError, match="calendar"):
        await resolve_target("calendar", explicit="primary")


async def test_malformed_explicit_still_raises_value_error_through_the_seam():
    with pytest.raises(ValueError):
        await resolve_target("github", explicit="not-a-valid-full-name")
