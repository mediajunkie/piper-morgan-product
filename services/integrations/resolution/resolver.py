"""Connector-agnostic target resolution entry point (#1342, RECONNECT-WS3 Phase 2).

``resolve_target()`` is the shared resolution-service seam Arch ruled for
(decisions.log 2026-07-01): a SEPARATE resolution service, not a 5th
Connector-protocol method. Build-GitHub-only (m-40) — it dispatches to
``resolve_repo`` for ``connector="github"`` and wraps the result via
``ResolvedRepo.to_target()``. No existing GitHub caller is migrated onto this (they
keep calling ``resolve_repo`` directly, unchanged) — this is the additive seam a
future non-GitHub connector (calendar is the natural next one, same
explicit→user-default→primary shape) will plug into on demand, not speculatively.
Until then, any other ``connector`` value raises ``NotImplementedError`` rather than
silently degrading.
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from services.integrations.resolution.target import ResolvedTarget


async def resolve_target(
    connector: str,
    *,
    user_id: Optional[UUID] = None,
    project_id: Optional[str] = None,
    explicit: Optional[str] = None,
) -> ResolvedTarget:
    """Resolve a target for ``connector`` via the shared explicit→…→env_var decision
    tree (#1342). GitHub-only today (m-40); raises ``NotImplementedError`` for any
    other connector rather than guessing at behavior nothing has designed/tested.

    Args:
        connector: which connector to resolve for (currently only ``"github"``).
        user_id / project_id / explicit: forwarded to the connector's resolver
            unchanged — the same shared vocabulary every connector's resolution walks.

    Returns:
        ``ResolvedTarget`` wrapping the connector-specific payload.

    Raises:
        UnresolvedRepoError: (github) when no resolution path produces a repo.
        NotImplementedError: for any connector other than ``"github"`` (not yet built).
    """
    if connector == "github":
        from services.integrations.github.repo_resolver import resolve_repo

        repo = await resolve_repo(user_id=user_id, project_id=project_id, explicit=explicit)
        return repo.to_target()

    raise NotImplementedError(
        f"resolve_target: connector={connector!r} not yet implemented "
        "(#1342 build-GitHub-only, m-40 — design calendar on paper, build on demand)"
    )
