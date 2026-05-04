"""GitHub repository resolution helper (Issue #1042).

Replaces hardcoded `piper-morgan-product` / `mediajunkie` defaults across the
GitHub adapter, integration router, and intent-service handlers with a
per-call resolution decision tree:

1. **Explicit arg**: caller passed `owner/name` directly → use it
2. **Project-scoped**: caller has a project context → return first linked
   Repository (ordered by ProjectRepositoryLink.linked_at; multi-link case
   per PM Q2 disposition 2026-05-04 — edge case, deterministic)
3. **User default-repo preference**: per-user `default_repo` setting (Issue
   #1042 Phase 1.5) → use it
4. **Env-var fallback**: `PIPER_DEFAULT_REPO` (dev escape hatch per PM Q4
   disposition 2026-05-04) → use it + log a deprecation warning
5. **Unresolved**: raise `UnresolvedRepoError` for handler to render as a
   graceful "which repo?" message

The function is async (DB lookup paths) and pure (no global state). Callers
catch `UnresolvedRepoError` and emit a graceful response; they should never
silently fall back to a hardcoded repo.
"""

from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass
from typing import Literal, Optional
from uuid import UUID

logger = logging.getLogger(__name__)

ENV_DEFAULT_REPO = "PIPER_DEFAULT_REPO"

ResolutionSource = Literal["explicit", "project", "user_default", "env_var"]

_FULL_NAME_RE = re.compile(r"^[A-Za-z0-9._\-]+/[A-Za-z0-9._\-]+$")


@dataclass(frozen=True)
class ResolvedRepo:
    """Repository resolved from one of the per-call resolution paths.

    Attributes:
        owner: GitHub user/org (e.g., "octocat")
        name: GitHub repo name (e.g., "hello-world")
        source: which resolution path produced this result
    """

    owner: str
    name: str
    source: ResolutionSource

    @property
    def full_name(self) -> str:
        return f"{self.owner}/{self.name}"


class UnresolvedRepoError(Exception):
    """Raised when no repo can be resolved for a query.

    Handlers should catch this and render a graceful "which repo?" message
    rather than silently fall back to a hardcoded value.
    """


def parse_full_name(value: str) -> tuple[str, str]:
    """Parse `owner/name` into a tuple, raising ValueError on bad shape."""
    if not value or not _FULL_NAME_RE.match(value):
        raise ValueError(
            f"Invalid repo full_name {value!r}; expected 'owner/name' shape"
        )
    owner, name = value.split("/", 1)
    return owner, name


async def resolve_repo(
    *,
    user_id: Optional[UUID] = None,
    project_id: Optional[str] = None,
    explicit: Optional[str] = None,
) -> ResolvedRepo:
    """Resolve a repo for a GitHub query.

    Decision tree (first match wins):

    1. ``explicit`` (str "owner/name") — caller passed it directly
    2. ``project_id`` — first Repository linked to the project (by linked_at)
    3. ``user_id`` — user's ``default_repo`` preference
    4. ``$PIPER_DEFAULT_REPO`` env var (dev fallback; logs deprecation warning)
    5. Otherwise → raise ``UnresolvedRepoError``

    Args:
        user_id: Authenticated user UUID. Used for the user-default lookup.
        project_id: Active project context. Used for the project-link lookup.
        explicit: ``owner/name`` string passed by the caller. Highest priority.

    Returns:
        ``ResolvedRepo`` with the resolved owner + name + source label.

    Raises:
        UnresolvedRepoError: when no resolution path produces a repo.
        ValueError: when ``explicit`` is provided but malformed.
    """
    # Path 1: explicit
    if explicit:
        owner, name = parse_full_name(explicit)
        return ResolvedRepo(owner=owner, name=name, source="explicit")

    # Path 2: project-scoped
    if project_id:
        repo = await _resolve_from_project(project_id)
        if repo is not None:
            return repo

    # Path 3: user-default preference
    if user_id is not None:
        repo = await _resolve_from_user_default(user_id)
        if repo is not None:
            return repo

    # Path 4: env-var dev fallback (logs deprecation warning)
    env_value = os.environ.get(ENV_DEFAULT_REPO)
    if env_value:
        try:
            owner, name = parse_full_name(env_value)
        except ValueError:
            logger.warning(
                "PIPER_DEFAULT_REPO env var has invalid shape %r; "
                "skipping env-var fallback (Issue #1042)",
                env_value,
            )
        else:
            logger.warning(
                "Repo resolved via PIPER_DEFAULT_REPO env-var fallback "
                "(%s/%s). This is a dev escape hatch and should not be "
                "relied on in production. Configure a per-project "
                "linked-repo or user default_repo preference. (Issue #1042)",
                owner,
                name,
            )
            return ResolvedRepo(owner=owner, name=name, source="env_var")

    # Path 5: unresolved
    raise UnresolvedRepoError(
        "No repo could be resolved for this query. "
        "Pass owner/name explicitly, link a repository to the active project, "
        "set a default_repo preference, or set PIPER_DEFAULT_REPO."
    )


async def _resolve_from_project(project_id: str) -> Optional[ResolvedRepo]:
    """Return first Repository linked to the project, or None.

    Multi-link resolution (per PM Q2 2026-05-04): order by
    ProjectRepositoryLink.linked_at ascending; first wins.
    """
    try:
        from sqlalchemy import select

        from services.database.models import (
            ProjectRepositoryLinkDB,
            RepositoryDB,
        )
        from services.database.session_factory import AsyncSessionFactory

        async with AsyncSessionFactory.session_scope() as session:
            result = await session.execute(
                select(RepositoryDB)
                .join(
                    ProjectRepositoryLinkDB,
                    RepositoryDB.id == ProjectRepositoryLinkDB.repository_id,
                )
                .where(ProjectRepositoryLinkDB.project_id == project_id)
                .order_by(ProjectRepositoryLinkDB.linked_at)
                .limit(1)
            )
            repo_db = result.scalar_one_or_none()

        if repo_db is None or not repo_db.full_name:
            return None
        try:
            owner, name = parse_full_name(repo_db.full_name)
        except ValueError:
            logger.warning(
                "Repository %s has malformed full_name %r; skipping",
                repo_db.id,
                repo_db.full_name,
            )
            return None
        return ResolvedRepo(owner=owner, name=name, source="project")
    except Exception as e:
        logger.warning(f"Project-scoped repo resolution failed: {e}")
        return None


async def _resolve_from_user_default(user_id: UUID) -> Optional[ResolvedRepo]:
    """Return user's default_repo preference, or None."""
    try:
        from services.domain.user_preference_manager import UserPreferenceManager

        preference_manager = UserPreferenceManager()
        value = await preference_manager.get_default_repo(user_id)
        if not value:
            return None
        try:
            owner, name = parse_full_name(value)
        except ValueError:
            logger.warning(
                "User %s default_repo preference has invalid shape %r; "
                "skipping user-default fallback",
                user_id,
                value,
            )
            return None
        return ResolvedRepo(owner=owner, name=name, source="user_default")
    except Exception as e:
        logger.warning(f"User-default repo resolution failed: {e}")
        return None
