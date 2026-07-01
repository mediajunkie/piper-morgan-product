"""GitHub repository resolution helper (Issue #1042).

Replaces hardcoded `piper-morgan-product` / `mediajunkie` defaults across the
GitHub adapter, integration router, and intent-service handlers with a
per-call resolution decision tree:

1. **Explicit arg**: caller passed `owner/name` directly → use it
2. **Project-scoped**: caller has a project context → return first linked
   Repository (ordered by ProjectRepositoryLink.linked_at; multi-link case
   per PM Q2 disposition 2026-05-04 — edge case, deterministic)
2.5. **Default project** (#1192(b)-v1, PM 2026-06-12): the user's
   `is_default=True AND is_archived=False` project's linked repo — the model's
   existing "primary project" expression; no request-threading required
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

# WS-1 P4 (#1226 / #1199): the flat-file GitHub-preferences store
# (data/github_preferences.json) was RETIRED 2026-06-21. The user-default and github-handle
# resolution paths read the DB-backed connector_configs store (ADR-070 D4) — the SOLE store.

ResolutionSource = Literal["explicit", "project", "default_project", "user_default", "env_var"]

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
        raise ValueError(f"Invalid repo full_name {value!r}; expected 'owner/name' shape")
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

    1. ``explicit`` (str "owner/name") — caller passed it directly (source="explicit")
    2. ``project_id`` — first Repository linked to that project, by linked_at
       (source="project")
    3. ``user_id``'s DEFAULT project's linked repo (#1192b; source="default_project")
    4. ``user_id``'s ``default_repo`` preference (source="user_default")
    5. ``$PIPER_DEFAULT_REPO`` env var (dev fallback; logs deprecation warning;
       source="env_var")
    6. Otherwise → raise ``UnresolvedRepoError``

    Paths 2–4 are DB-backed: each is structurally live but returns None when its
    data is absent (project unlinked / no default project / no preference) — an
    empty-data miss, NOT a dead branch (#1230). Per-path proof-tests
    (test_repo_resolver_paths_1230) assert each path can still resolve given
    seeded data, so a reorder can't silently leave a *code*-dead path; populating
    the data is #1199 (storage) / #1314 (auto-default) / #1315 (activate links).

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

    # Path 2.5 (#1192(b)-v1): the user's DEFAULT project's linked repo. The
    # Project model already expresses "primary" (is_default) and active-vs-not
    # (is_archived) — no separate "active project" concept or request-threading
    # needed (PM disposition 2026-06-12). Resolved here so every existing caller
    # gets project-scoped resolution free; per-conversation project SWITCHING
    # remains the CXO start-screen design thread.
    if user_id is not None:
        repo = await _resolve_from_default_project(user_id)
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


async def read_user_github_handle(user_id) -> Optional[str]:
    """The bound user's GitHub login, for scoping Radar work items to "assigned to me"
    (#1239 / #6). Reads ``github_username`` from the user's DB-backed connector config
    (connector_configs, ADR-070 D4 — the SOLE store as of WS-1 P4), falling back to the
    ``PIPER_GITHUB_HANDLE`` env var. Returns None when unset → callers apply NO assignee
    filter (show all open issues), so this is an opt-in enhancement, never a regression.

    Best-effort: any DB error (or a None/non-UUID ``user_id``, which the store reads as a
    graceful miss → empty config) falls through to the env var / None — a github hiccup must
    never blank Radar.

    This is the single-bound-user form of the #1233 identity map: one configured handle
    now, generalizes to the unified user→identity record later with no rework."""
    try:
        if user_id is not None:
            from services.connectors.config_service import ConnectorConfigService
            from services.database.session_factory import AsyncSessionFactory

            async with AsyncSessionFactory.session_scope() as session:
                config = await ConnectorConfigService(session).get_config(user_id, "github")
            handle = config.get("github_username")
            if handle:
                return handle
    except Exception as e:
        logger.warning(f"Reading github handle from connector config failed: {e}")
    return os.environ.get("PIPER_GITHUB_HANDLE") or None


async def _resolve_from_default_project(user_id: UUID) -> Optional[ResolvedRepo]:
    """Resolve via the user's DEFAULT (primary), non-archived project (#1192(b)-v1).

    Selection rule (PM 2026-06-12): ``is_default=True AND is_archived=False``
    for this owner — the model's existing "top priority" expression; no separate
    active-project flag. The project's repo is then resolved by the existing
    project-link path (first link by linked_at, per the #1042 Q2 multi-link
    rule). Returns None when the user has no default project or it has no
    linked repo — resolution falls through to the user default-repo preference.
    """
    try:
        from sqlalchemy import and_, select

        from services.database.models import ProjectDB
        from services.database.session_factory import AsyncSessionFactory

        async with AsyncSessionFactory.session_scope() as session:
            result = await session.execute(
                select(ProjectDB.id)
                .where(
                    and_(
                        ProjectDB.owner_id == str(user_id),
                        ProjectDB.is_default == True,  # noqa: E712
                        ProjectDB.is_archived == False,  # noqa: E712
                    )
                )
                .order_by(ProjectDB.updated_at.desc())
                .limit(1)
            )
            project_id = result.scalar_one_or_none()

        # #1230 guard: distinguish "no default project" from "default project has
        # no linked repo" — same None result, different remediation (create/mark a
        # default project vs link a repo to it). Kept at debug (resolution is hot).
        if project_id is None:
            logger.debug("default-project resolution: user %s has no default project", user_id)
            return None
        repo = await _resolve_from_project(project_id)
        if repo is None:
            logger.debug(
                "default-project resolution: user %s default project %s has no linked repo",
                user_id,
                project_id,
            )
            return None
        return ResolvedRepo(owner=repo.owner, name=repo.name, source="default_project")
    except Exception as e:
        logger.warning(f"Default-project repo resolution failed: {e}")
        return None


async def _read_user_default_repo_from_db(user_id: UUID) -> Optional[str]:
    """WS-1 (#1226 / #1199): read ``default_repository`` from the DB-backed
    connector_configs store (ADR-070 D4) — the SOLE store as of P4. Best-effort —
    returns None on any DB error (honest-degrade: the user-default path simply
    yields nothing and resolution falls through to the env-var fallback, NOT to a
    second store). Uses ``session_scope()`` to mirror the other repo_resolver DB
    reads (#1192(b))."""
    try:
        from services.connectors.config_service import ConnectorConfigService
        from services.database.session_factory import AsyncSessionFactory

        async with AsyncSessionFactory.session_scope() as session:
            return await ConnectorConfigService(session).get_default_repo(user_id)
    except Exception as e:
        logger.warning("DB default-repo read failed: %s", e)
        return None


async def _resolve_from_user_default(user_id: UUID) -> Optional[ResolvedRepo]:
    """Return the user's default_repo preference, or None.

    WS-1 P4 (#1226 / #1199): reads ``default_repository`` from the DB-backed
    connector_configs store (ADR-070 D4) — the SOLE store. The flat-file store
    (``data/github_preferences.json``) and the in-memory ``UserPreferenceManager``
    path were RETIRED 2026-06-21; there is now ONE canonical store.

    History: the flat file (#1192 slice a) replaced the old in-memory
    ``UserPreferenceManager`` path (#1042) which never resolved; P4 retired the
    flat file too once the DB store subsumed both.
    """
    try:
        value = await _read_user_default_repo_from_db(user_id)  # WS-1 P4: DB is the sole store
        if not value:
            return None
        try:
            owner, name = parse_full_name(value)
        except ValueError:
            logger.warning(
                "User %s default_repository has invalid shape %r; "
                "skipping user-default fallback",
                user_id,
                value,
            )
            return None
        return ResolvedRepo(owner=owner, name=name, source="user_default")
    except Exception as e:
        logger.warning(f"User-default repo resolution failed: {e}")
        return None
