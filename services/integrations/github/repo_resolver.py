"""GitHub repository resolution helper (Issue #1042).

Replaces hardcoded `piper-morgan-product` / `mediajunkie` defaults across the
GitHub adapter, integration router, and intent-service handlers with a
per-call resolution decision tree:

1. **Explicit arg**: caller passed `owner/name` directly → use it
2. **User default-repo preference**: per-user `default_repo` setting (Issue
   #1042 Phase 1.5) → use it
3. **Env-var fallback**: `PIPER_DEFAULT_REPO` (dev escape hatch per PM Q4
   disposition 2026-05-04) → use it + log a deprecation warning
3.5 **Read-time recovery** (#1590): GitHub connected but no default repo ever
   set → search the user's repos once, apply #1314's default-default rule,
   persist it, and re-resolve. Additive: it runs only where step 4 used to fire.
4. **Unresolved**: raise `UnresolvedRepoError` for handler to render as a
   graceful "which repo?" message

The function is async (DB lookup paths) and pure (no global state). Callers
catch `UnresolvedRepoError` and emit a graceful response; they should never
silently fall back to a hardcoded repo.

RETIRED (#1315, PM-directed 2026-07-04): the project-scoped path
(``ProjectRepositoryLink``-based) and the default-project path (#1192(b)-v1)
were removed. `project_repository_links` and `repositories` were empty
system-wide with no live population path, and PM ruled retire over ship. See
`_resolve_from_project`/`_resolve_from_default_project`'s prior home in git
history if this ever needs reviving alongside real project↔repo linking UI.
"""

from __future__ import annotations

import logging
import os
import re
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional
from uuid import UUID

logger = logging.getLogger(__name__)

ENV_DEFAULT_REPO = "PIPER_DEFAULT_REPO"

# ── #1590 read-time recovery guard ────────────────────────────────────────────
# Recovery costs one GitHub search; the live incident logged TEN unresolved
# resolutions inside one window, so an unguarded attempt would be ten searches.
# In-process, monotonic, per-user, TTL-bounded.
_RECOVERY_TTL_SECONDS = 300
_recovery_attempts: Dict[str, float] = {}

# WS-1 P4 (#1226 / #1199): the flat-file GitHub-preferences store
# (data/github_preferences.json) was RETIRED 2026-06-21. The user-default and github-handle
# resolution paths read the DB-backed connector_configs store (ADR-070 D4) — the SOLE store.

# ResolutionSource + ResolvedTarget are promoted to the shared resolution module
# (#1342, Arch-ruled 2026-07-01) — imported here (and re-exported) so existing
# `from ...repo_resolver import ResolutionSource` callers keep working unchanged.
from services.integrations.resolution.target import (  # noqa: E402
    ResolutionSource,
    ResolvedTarget,
)

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

    def to_target(self) -> ResolvedTarget:
        """Wrap this GitHub-resolved repo in the connector-agnostic ``ResolvedTarget``
        envelope (#1342, Arch-ruled): ``source`` carries over, ``connector`` is
        ``"github"``, and ``payload`` is this ``ResolvedRepo`` (the GitHub payload)."""
        return ResolvedTarget(source=self.source, connector="github", payload=self)


class UnresolvedRepoError(Exception):
    """Raised when no repo can be resolved for a query.

    Handlers should catch this and render a graceful "which repo?" message
    rather than silently fall back to a hardcoded value.
    """


def reset_recovery_guard() -> None:
    """Clear the in-process #1590 recovery guard.

    For tests and for any surface that deliberately re-arms recovery (e.g. after
    a user connects a new account mid-process). Not called on any hot path.
    """
    _recovery_attempts.clear()


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
    2. ``user_id``'s ``default_repo`` preference (source="user_default")
    3. ``$PIPER_DEFAULT_REPO`` env var (dev fallback; logs deprecation warning;
       source="env_var")
    3.5. **Read-time recovery** (#1590) — when ``user_id`` is present, GitHub is
       connected (binding-first ``IntegrationStatusService``), and no preference
       exists: search the user's repos ONCE, apply #1314's default-default rule,
       persist, re-resolve (source="user_default"). See
       ``_attempt_default_repo_recovery``. Strictly additive — it can only turn a
       raise into a success, never change an existing outcome.
    4. Otherwise → raise ``UnresolvedRepoError``

    RETIRED (#1315, PM-directed 2026-07-04): the project-scoped path and the
    default-project path (#1192(b)-v1) were removed — ``project_repository_links``
    and ``repositories`` were empty system-wide with no population path, and PM
    ruled retire over ship. ``project_id`` is accepted but currently unused;
    kept in the signature so callers don't need updating if project-scoped
    resolution is ever rebuilt alongside real linking UI.

    Args:
        user_id: Authenticated user UUID. Used for the user-default lookup.
        project_id: Currently unused (see RETIRED note above).
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

    # Path 2: user-default preference
    if user_id is not None:
        repo = await _resolve_from_user_default(user_id)
        if repo is not None:
            return repo

    # Path 3: env-var dev fallback (logs deprecation warning)
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
                "relied on in production. Configure a "
                "default_repo preference. (Issue #1042)",
                owner,
                name,
            )
            return ResolvedRepo(owner=owner, name=name, source="env_var")

    # Path 3.5 (#1590): read-time recovery of a never-set default repo.
    # STRICTLY additive — it runs only where the code above would already have
    # raised, so every existing resolution outcome is unchanged.
    if user_id is not None:
        recovered = await _attempt_default_repo_recovery(user_id)
        if recovered is not None:
            return recovered

    # Path 4: unresolved
    raise UnresolvedRepoError(
        "No repo could be resolved for this query. "
        "Pass owner/name explicitly, set a default_repo preference, "
        "or set PIPER_DEFAULT_REPO."
    )


def _claim_recovery_attempt(key: str) -> bool:
    """Claim the one recovery attempt allowed for ``key`` in this TTL window.

    Returns True if the caller may proceed, False if an attempt was already made
    recently. The claim is stamped BEFORE the caller awaits anything: the live
    incident logged ten unresolved resolutions inside one window, and a guard that
    stamps on completion would let all ten race past it into ten GitHub searches.

    Scope is process-lifetime + TTL, deliberately NOT Redis-backed:
    ``ContextCache`` (#984) degrades to a cache MISS whenever Redis is unavailable,
    which would turn the guard off exactly when the system is least healthy — the
    opposite of what a rate guard must do. A per-worker in-process bound is the
    honest claim: at most one recovery search per user per worker per TTL.
    """
    now = time.monotonic()
    last = _recovery_attempts.get(key)
    if last is not None and (now - last) < _RECOVERY_TTL_SECONDS:
        return False
    _recovery_attempts[key] = now
    return True


async def _attempt_default_repo_recovery(user_id: UUID) -> Optional[ResolvedRepo]:
    """Recover a missing ``default_repo`` at READ time (#1590), then re-resolve.

    #1314's ``apply_default_default_if_unset`` was wired only into the GitHub OAuth
    callback (``web/api/routes/settings_integrations.py``), behind
    ``if repos_result.repositories:``. Any account that connected before that shipped
    (2026-07-04), or whose repo search was empty/failed at that instant, is stuck at
    zero forever: every GitHub read comes back empty and the #1536 first-contact demo
    correctly refuses to show anything — the blank generic interface it exists to
    prevent. Diagnosed from live Fly logs (v48): ``UnresolvedRepoError`` ten times in
    one window for a user whose connector was BOUND.

    Placed at the ``resolve_repo`` seam so every GitHub surface benefits at once
    (first-contact, Radar, the adapter's repo-scoped reads, the integration router,
    spatial, the intent handlers, and #1342's ``resolve_target``) — those callers
    share no other common point.

    Guarantees:

    - **Principal-safe**: the caller only reaches here with a non-None ``user_id``;
      anonymous resolution is untouched.
    - **Gated on connection**: the canonical binding-first
      ``IntegrationStatusService`` (#1329/#1547) — the same gate Radar passed while
      resolution was failing. An unconfigured user never costs a search.
    - **Never asks a scope question**: this persists a default, it does not prompt.
      A user with genuinely zero accessible repos degrades exactly as before (the
      caller's existing ``UnresolvedRepoError`` path).
    - **Never overwrites**: ``apply_default_default_if_unset`` short-circuits on an
      existing preference, and resolution only reaches here when there wasn't one.
    - **Never raises**: any failure returns None and the caller raises
      ``UnresolvedRepoError`` as it does today.

    Returns:
        The newly-resolved ``ResolvedRepo`` (source ``user_default`` — the preference
        now genuinely exists and is what every later read will find), or None.
    """
    key = str(user_id)
    if not _claim_recovery_attempt(key):
        logger.debug(
            "default_repo_recovery_skipped user=%s reason=recently_attempted ttl=%ss",
            key,
            _RECOVERY_TTL_SECONDS,
        )
        return None

    try:
        from services.integrations.integration_status_service import (
            IntegrationStatusService,
        )

        if not await IntegrationStatusService().is_configured(key, "github"):
            logger.info(
                "default_repo_recovery_skipped user=%s reason=github_not_configured", key
            )
            return None
    except Exception as e:
        logger.warning("default_repo_recovery_status_check_failed user=%s error=%s", key, e)
        return None

    logger.info(
        "default_repo_recovery_attempt user=%s reason=unresolved_repo_with_github_connected "
        "(#1590, applying #1314 rule)",
        key,
    )

    try:
        from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

        repos_result = await GitHubMCPSpatialAdapter().search_user_repositories(key)
        repos = list(repos_result.repositories or [])
    except Exception as e:
        logger.warning("default_repo_recovery_search_failed user=%s error=%s", key, e)
        return None

    if not repos:
        # Genuinely zero accessible repos, or an honest degrade (no binding /
        # unreachable). Either way there is nothing to default to — m-44: this is
        # not an assertion that the account HAS no repos, only that the read
        # returned none. The guard keeps it to one attempt per TTL.
        logger.info(
            "default_repo_recovery_no_repos user=%s degraded=%s",
            key,
            repos_result.degradation is not None,
        )
        return None

    rule = "single_repo" if len(repos) == 1 else "oldest_active"
    try:
        await apply_default_default_if_unset(user_id, repos)
    except Exception as e:
        logger.warning("default_repo_recovery_persist_failed user=%s error=%s", key, e)
        return None

    resolved = await _resolve_from_user_default(user_id)
    if resolved is None:
        # Persisted-but-unreadable is a real state change we failed to confirm;
        # say so rather than reporting a clean miss (m-44).
        logger.warning(
            "default_repo_recovery_unverified user=%s repo_count=%d "
            "detail=preference_not_readable_after_write",
            key,
            len(repos),
        )
        return None

    logger.info(
        "default_repo_recovery_succeeded user=%s repo=%s rule=%s repo_count=%d "
        "(#1314 default-default applied at read time)",
        key,
        resolved.full_name,
        rule,
        len(repos),
    )
    return resolved


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


async def get_user_default_repo(user_id: UUID) -> Optional[str]:
    """WS-1 (#1226 / #1199): read ``default_repository`` from the DB-backed
    connector_configs store (ADR-070 D4) — the SOLE, per-user-scoped store as of P4.
    Best-effort — returns None on any DB error (honest-degrade: the user-default path
    simply yields nothing and resolution falls through to the env-var fallback, NOT to
    a second store). Uses ``session_scope()`` to mirror the other repo_resolver DB
    reads (#1192(b)).

    Promoted from a module-private helper (2026-07-06, #1366 Component A) — this is
    now the ONE correct way to read a user's default GitHub repo anywhere in the
    codebase. Every caller that previously read `PIPER.user.md`'s GitHub section
    directly (unscoped, same value for every user on a shared instance) must resolve
    through this function instead.
    """
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
        value = await get_user_default_repo(user_id)  # WS-1 P4: DB is the sole store
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


def compute_default_default(repos: List[Dict[str, Any]]) -> Optional[str]:
    """#1314 "default default" — PM's rule (2026-07-04) for auto-setting a fresh user's
    default repo when they connect GitHub, so a first-run user isn't stuck at zero.

    Rule: if exactly one repo exists, use it (no choice to make). If multiple exist and
    none is user-designated, fall back to the first/oldest ACTIVE (non-archived) one.

    Each dict is the normalized repo shape from ``GitHubMCPSpatialAdapter._parse_repo_search``
    (``full_name``, ``created_at``, ``archived``). Edge case PM's rule didn't name: if every
    repo happens to be archived, falls back to oldest-overall rather than returning nothing —
    "some default" beats "no default" when repos genuinely exist. A repo with no ``created_at``
    (malformed/unexpected payload) sorts after every repo with a real timestamp, so it's never
    picked over one with a known creation date.

    Args:
        repos: normalized repo dicts to choose from (may be empty).

    Returns:
        The chosen repo's ``owner/name``, or ``None`` if ``repos`` is empty.
    """
    if not repos:
        return None
    if len(repos) == 1:
        return repos[0].get("full_name") or None

    active = [r for r in repos if not r.get("archived", False)]
    candidates = active if active else repos  # all-archived edge case: fall back to all

    def _sort_key(r: Dict[str, Any]) -> tuple:
        created = r.get("created_at")
        return (created is None, created or "")

    oldest = sorted(candidates, key=_sort_key)[0]
    return oldest.get("full_name") or None


async def apply_default_default_if_unset(
    user_id: "str | UUID", repos: List[Dict[str, Any]]
) -> None:
    """Auto-set the user's ``default_repo`` preference per #1314's rule, but ONLY if they
    don't already have one — never overwrites an explicit user choice. Intended call site:
    right after a GitHub OAuth connection completes (the first-run moment), not on every
    query — this persists a preference, it isn't a live per-resolution fallback.

    ``user_id`` accepts ``str`` (the OAuth callback's ``result["user_id"]`` shape) or
    ``UUID``, mirroring ``ConnectorConfigService``'s own ``Union[str, UUID, None]``.

    No-ops (logs at debug) if ``repos`` is empty — nothing to default to yet.
    """
    from services.connectors.config_service import ConnectorConfigService
    from services.database.session_factory import AsyncSessionFactory

    async with AsyncSessionFactory.session_scope() as session:
        config_service = ConnectorConfigService(session)
        existing = await config_service.get_default_repo(user_id)
        if existing:
            return  # never override an explicit user preference

        chosen = compute_default_default(repos)
        if chosen is None:
            logger.debug("apply_default_default: no repos to default to for user %s", user_id)
            return

        await config_service.set_default_repo(user_id, chosen)
        # #1436: stdlib logger — kwargs raised TypeError when this line ran
        logger.info(
            f"default_repo_auto_set user={user_id} repo={chosen} repo_count={len(repos)}"
        )
