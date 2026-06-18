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

import json
import logging
import os
import re
from dataclasses import dataclass
from typing import Literal, Optional
from uuid import UUID

logger = logging.getLogger(__name__)

ENV_DEFAULT_REPO = "PIPER_DEFAULT_REPO"

# #1192 slice (a): the persistent GitHub-preferences store the settings UI writes
# (web/api/routes/settings_integrations.py `GITHUB_PREFERENCES_FILE`). Keyed by
# user id (= JWT `sub`, a UUID string); each entry holds `default_repository` as
# an "owner/name" full_name. The user-default resolution path reads this so that
# designating a default repo in the UI actually reaches the chat-path resolver.
_GITHUB_PREFERENCES_FILE = "data/github_preferences.json"

ResolutionSource = Literal[
    "explicit", "project", "default_project", "user_default", "env_var"
]

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


def _read_user_default_repository(user_key: str) -> Optional[str]:
    """Read ``default_repository`` for a user from the persistent GitHub-prefs
    store the settings UI writes (#573). Returns None if the file, the user
    entry, or the field is absent. Path is cwd-relative — same as the writer."""
    try:
        if not os.path.exists(_GITHUB_PREFERENCES_FILE):
            return None
        with open(_GITHUB_PREFERENCES_FILE, "r") as f:
            all_prefs = json.load(f)
        return (all_prefs.get(user_key) or {}).get("default_repository") or None
    except Exception as e:
        logger.warning(f"Reading {_GITHUB_PREFERENCES_FILE} failed: {e}")
        return None


def read_user_github_handle(user_id) -> Optional[str]:
    """The bound user's GitHub login, for scoping Radar work items to "assigned to me"
    (#1239 / #6). Reads ``github_username`` from the same per-user GitHub-prefs store as
    the repo binding, falling back to the ``PIPER_GITHUB_HANDLE`` env var. Returns None
    when unset → callers apply NO assignee filter (show all open issues), so this is an
    opt-in enhancement, never a regression.

    This is the single-bound-user form of the #1233 identity map: one configured handle
    now, generalizes to the unified user→identity record later with no rework."""
    try:
        if user_id is not None and os.path.exists(_GITHUB_PREFERENCES_FILE):
            with open(_GITHUB_PREFERENCES_FILE, "r") as f:
                all_prefs = json.load(f)
            handle = (all_prefs.get(str(user_id)) or {}).get("github_username")
            if handle:
                return handle
    except Exception as e:
        logger.warning(f"Reading github handle from {_GITHUB_PREFERENCES_FILE} failed: {e}")
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

        if project_id is None:
            return None
        repo = await _resolve_from_project(project_id)
        if repo is None:
            return None
        return ResolvedRepo(owner=repo.owner, name=repo.name, source="default_project")
    except Exception as e:
        logger.warning(f"Default-project repo resolution failed: {e}")
        return None


async def _resolve_from_user_default(user_id: UUID) -> Optional[ResolvedRepo]:
    """Return the user's default_repo preference, or None.

    #1192 slice (a): reads the PERSISTENT GitHub-preferences store the settings
    UI writes (``data/github_preferences.json``, keyed by user id / JWT sub,
    holding ``default_repository`` as an "owner/name" full_name). The older
    ``UserPreferenceManager`` path (#1042) was in-memory AND re-instantiated
    empty on every call, so it never resolved — the UI setter and this reader
    were two disconnected stores. This bridges them at the read side, so
    designating a default repo in the UI reaches the chat-path resolver.
    """
    try:
        value = _read_user_default_repository(str(user_id))
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
