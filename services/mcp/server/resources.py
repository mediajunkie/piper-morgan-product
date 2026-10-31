"""Piper Morgan MCP server — three read-only, owner-scoped resources (Phase C unit 2, #1462).

Companion docs: ``docs/internal/architecture/current/mcp/phase-c-build-plan-2026-09-25.md``
(Lead, unit 2: "the three named resources") and
``phase-c-minimal-alpha-slice-2026-09-25.md`` (Arch: resources only, zero tools, the
escalation trigger back to Arch if any of them ever needs a mutation — none of the
three below does). Colleague-model referent per CXO's Q2 ruling
(``mailboxes/lead/read/rule-cxo-to-lead-arch-cc-ppm-exec-pm-mcp-q2-colleague-model-referent-plus-rubric-staleness-correction-2026-09-25.md``):
the #1510 verified-inference store, **never** #1735 (#1735's own body says three of
its four personalization stores are disconnected or a silent no-op).

Every resource here:

1. **Reads identity from ``current_user_id()`` only** (``services/mcp/server/identity.py``).
   That function raises if called with no verified identity on the request context — there
   is no fallback anywhere in this module, so a resource handler literally cannot run without
   the SDK's own ``RequireAuthMiddleware`` having already resolved a real caller (unit 1).
2. **Never raises past its own read.** Every external read (DB, the #1510 preference store,
   the GitHub connector) is wrapped so a failure becomes a structured, honest payload —
   ``{"available": false, "reason": "..."}`` or the connector's own honest-degrade shape —
   never a bare exception surfaced to the client and never a fabricated success.
3. **Returns ``application/json`` text.** FastMCP's ``@app.resource(...)`` decorator accepts
   a plain string return; each function here returns ``json.dumps(...)``, and registration
   passes ``mime_type="application/json"``.

``register_resources`` is called from ``services/mcp/server/app.py``'s own seam of the same
name (kept there per the server-README's documented seam location — this module holds the
resource logic itself so it stays independently testable and importable without pulling in
``app.py``'s ASGI-wiring concerns).
"""

from __future__ import annotations

import json
from typing import Any
from uuid import UUID

import structlog
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter
from services.mcp.server.identity import current_user_id
from services.user_context_service import user_context_service

logger = structlog.get_logger(__name__)

PROFILE_URI = "piper://me/profile"
COLLEAGUE_MODEL_URI = "piper://me/colleague-model"
GITHUB_ISSUES_URI = "piper://me/github/issues"

PROFILE_DESCRIPTION = (
    "The signed-in user's own profile: organization, active projects (each tagged with "
    "projects_source so the client can see where the list came from — database, "
    "preferences, or PIPER.md config), and stated priorities. Read via the same "
    "user-context service the chat surface uses, owner-scoped to the caller's verified "
    "identity. Never another user's data; a structured honest-empty payload "
    "(available: false) if the read fails, never a fabricated profile."
)

COLLEAGUE_MODEL_DESCRIPTION = (
    "What Piper has actually confirmed about this user, per CXO's ruling: entries from the "
    "#1510 verified-inference store (services/intent_service/verified_inference.py) that "
    "went through the read-back-and-confirm loop — never a raw, unconfirmed inference — "
    "plus the user's own hand-authored PIPER.md priorities (always real, no inference "
    "involved). Deliberately NOT #1735's personalization/learning-loop stores, which are "
    "known-disconnected. Structurally honest when nothing is confirmed yet (verified: [])."
)

GITHUB_ISSUES_DESCRIPTION = (
    "This user's own open GitHub issues (assignee:@me), read via their bound GitHub "
    "connector (owner-scoped, logical-key binding per ADR-070 Amendment A). If the user "
    "hasn't connected GitHub yet, returns the connector's own honest ConnectRequired shape "
    "(available: false, reason: connect_required) — never an exception, never an empty list "
    "pretending to be 'no issues'. issues is ONE PAGE: count is the page length, total is "
    "GitHub's full match count (total_count), truncated is total > count, and capped_at is "
    "the page cap. Report total as the number of open issues, never count (#2005: a 30-item "
    "page was read as the full set of 278). scope and note say exactly what was searched and "
    "how the page is ordered (#2022): quote them rather than inferring a repository from the "
    "items. Each item is slim (#2241): number, title, repository, state, labels (names), "
    "assignees (logins), created_at, updated_at, html_url, no body; the section is kept under "
    "a size budget by dropping items from the tail of the page, so count may be below "
    "capped_at with truncated true."
)

# #2241: the serialized github section's size budget. One served call shipped 431,097
# characters (50 raw GitHub REST objects); a client may truncate or refuse that. Items are
# slimmed to ISSUE_ITEM_KEYS and, if a page still exceeds the budget, dropped from the TAIL
# (count falls; truncated stays derived as total > count; capped_at stays the page cap).
GITHUB_SECTION_BUDGET_CHARS = 20_000
ISSUE_ITEM_KEYS = (
    "number",
    "title",
    "repository",
    "state",
    "labels",
    "assignees",
    "created_at",
    "updated_at",
    "html_url",
)
# The ordering word in the scope sentence, keyed on the adapter's own (sort, order). A
# (sort, order) with no entry renders the raw pair, so a new sort is never described by
# an old word (Arch, #2241: the sentence is rendered from the constants that build the call).
_ORDERING_WORDS = {
    # CXO 10-31 08:48: the words name the date the sort uses (opened, not touched).
    ("created", "desc"): "most recently opened first",
    ("created", "asc"): "oldest opened first",
    ("updated", "desc"): "most recently updated first",
}

# Mirrors the chat surface's list_open_issues default page size
# (services/intent/intent_service.py's GitHubMCPSpatialAdapter().list_open_issues call) —
# not a new cap invented for this resource.
GITHUB_ISSUES_PAGE_CAP = 50


def _json(payload: dict[str, Any]) -> str:
    return json.dumps(payload)


async def _read_profile() -> str:
    """``piper://me/profile`` — organization/projects/priorities for the verified caller."""
    user_id = current_user_id()
    try:
        # get_user_context's session_id param is typed plain `str` (not Optional) —
        # user_id is always provided here, so the cache-key/logging use of session_id
        # is functionally moot; a synthetic per-user value keeps this call mypy-clean
        # (the #1436 gate) without touching that service's signature.
        ctx = await user_context_service.get_user_context(
            session_id=f"mcp:{user_id}", user_id=UUID(user_id)
        )
    except (
        Exception
    ) as e:  # silent-ok: honest-empty, never a fabricated profile or a bare exception to the client
        logger.warning("mcp_resource_profile_read_failed", user_id=user_id, error=str(e))
        return _json({"available": False, "reason": "profile_read_failed"})
    return _json(_profile_payload(ctx))


def _profile_payload(ctx: Any) -> dict[str, Any]:
    """Shape the profile from a ``UserContext``, mirroring the chat floor's field-level
    contract (#2218, Arch's ruling on the #2151 residual; ``context_assembler``'s
    ``projects_source_failed`` / ``priorities_source_failed``).

    A FAILED read withholds its fields: ``null`` plus ``<field>_status: "read_failed"``.
    Never ``[]`` and never PIPER.md's config values dressed as the user's own. A failed
    projects read withholds ``projects`` (and its source label, which would otherwise read
    ``config`` for a value that is not served); a failed preferences read withholds
    ``priorities`` and ``organization``. Clean reads are byte-for-byte what they were.
    ``available: false`` stays for the whole-read exception in ``_read_profile`` only.
    ``is True``: only the service's own bool arms a withhold, as on the floor.
    """
    projects_failed = getattr(ctx, "projects_read_failed", False) is True
    preferences_failed = getattr(ctx, "preferences_read_failed", False) is True
    payload: dict[str, Any] = {"available": True}
    if preferences_failed:
        payload["organization"] = None
        payload["organization_status"] = "read_failed"
    else:
        payload["organization"] = ctx.organization
    if projects_failed:
        payload["projects"] = None
        payload["projects_source"] = None
        payload["projects_status"] = "read_failed"
    else:
        payload["projects"] = ctx.projects
        payload["projects_source"] = ctx.projects_source
    if preferences_failed:
        payload["priorities"] = None
        payload["priorities_status"] = "read_failed"
    else:
        payload["priorities"] = ctx.priorities
    return payload


async def _read_colleague_model() -> str:
    """``piper://me/colleague-model`` — #1510 confirmed entries + PIPER.md priorities.

    Reads the #1510 store the same way ``get_verified_inference`` does internally
    (``collaboration_gate._load_preferences``'s ``VERIFIED_INFERENCES_PREF_KEY`` bucket) but
    returns every confirmed entry for this user rather than one key at a time — there is no
    "list all" helper in ``verified_inference.py`` (checked; grepped every
    ``store_verified_inference`` call-site), so this reads the same seam that module's own
    ``get_verified_inference`` reads, rather than inventing a new shared-module function for
    a single unit-2 consumer.
    """
    user_id = current_user_id()
    verified: list[dict[str, Any]] = []
    try:
        from services.intent_service.collaboration_gate import _load_preferences
        from services.intent_service.verified_inference import VERIFIED_INFERENCES_PREF_KEY

        store = (await _load_preferences(user_id)).get(VERIFIED_INFERENCES_PREF_KEY) or {}
        for key, record in store.items():
            if not isinstance(record, dict):
                continue  # malformed row: skip rather than surface a raw/unconfirmed shape
            verified.append(
                {
                    "key": key,
                    "value": record.get("value"),
                    "verified_at": record.get("verified_at"),
                }
            )
    except Exception as e:  # silent-ok: fail-safe DIRECTION — a storage error reads as "nothing confirmed", mirrors get_verified_inference's own fail-safe
        logger.warning(
            "mcp_resource_colleague_model_verified_read_failed", user_id=user_id, error=str(e)
        )
        verified = []

    priorities: list[Any] = []
    try:
        ctx = await user_context_service.get_user_context(
            session_id=f"mcp:{user_id}", user_id=UUID(user_id)
        )
        priorities = ctx.priorities
    except Exception as e:  # silent-ok: honest-empty priorities list, never fabricated
        logger.warning(
            "mcp_resource_colleague_model_priorities_read_failed", user_id=user_id, error=str(e)
        )
        priorities = []

    payload: dict[str, Any] = {"verified": verified, "priorities": priorities}
    if not verified:
        payload["note"] = "nothing confirmed yet"
    return _json(payload)


def _repository_of(item: dict[str, Any]) -> str | None:
    """``owner/name`` parsed from GitHub's ``repository_url`` (``.../repos/owner/name``),
    else from ``html_url`` (``github.com/owner/name/issues/N``), else None. Code-parsed,
    never a label the model infers from the items (#2022)."""
    repo_url = item.get("repository_url")
    if isinstance(repo_url, str) and "/repos/" in repo_url:
        tail = repo_url.split("/repos/", 1)[1].strip("/")
        parts = tail.split("/")
        if len(parts) >= 2 and parts[0] and parts[1]:
            return f"{parts[0]}/{parts[1]}"
    html_url = item.get("html_url")
    if isinstance(html_url, str) and "github.com/" in html_url:
        parts = html_url.split("github.com/", 1)[1].strip("/").split("/")
        if len(parts) >= 2 and parts[0] and parts[1]:
            return f"{parts[0]}/{parts[1]}"
    return None


def _names(values: Any, key: str) -> list[str]:
    """Label names / assignee logins only; a raw GitHub object or a bare string each count."""
    out: list[str] = []
    for v in values if isinstance(values, list) else []:
        if isinstance(v, dict) and isinstance(v.get(key), str):
            out.append(v[key])
        elif isinstance(v, str):
            out.append(v)
    return out


def slim_issue(item: dict[str, Any]) -> dict[str, Any]:
    """#2241: exactly ``ISSUE_ITEM_KEYS``, in that order; no body, no ``*_url`` beyond
    ``html_url``, no reactions/user/node_id. Missing fields are None (lists: empty)."""
    return {
        "number": item.get("number"),
        "title": item.get("title"),
        "repository": _repository_of(item),
        "state": item.get("state"),
        "labels": _names(item.get("labels"), "name"),
        "assignees": _names(item.get("assignees"), "login"),
        "created_at": item.get("created_at"),
        "updated_at": item.get("updated_at"),
        "html_url": item.get("html_url"),
    }


def render_issues_scope(
    *, query: str | None = None, sort: str | None = None, order: str | None = None
) -> tuple[str, str]:
    """#2022: the scope phrase and its ordering word, rendered FROM the adapter's own query
    and sort constants (not a hand-written string beside them), so the sentence can only
    say what the call does. Returns ``(scope, ordering)``.

    Qualifiers are read from the query: ``assignee:@me`` -> assigned to you; ``is:open``;
    ``is:issue``/``is:pr``; ``archived:false`` -> archived repositories excluded. The
    repositories covered are those the user's GitHub connection can see, never "all".
    """
    from services.mcp.consumer import github_adapter as gh

    q = query if query is not None else gh._MY_OPEN_ISSUES_QUERY
    s = sort if sort is not None else gh._SEARCH_SORT
    o = order if order is not None else gh._SEARCH_ORDER
    terms = set(q.split())
    state = "open " if "is:open" in terms else ""
    kind = "pull requests" if "is:pr" in terms else "issues"
    who = (
        " assigned to you"
        if "assignee:@me" in terms
        else (" you opened" if "author:@me" in terms else "")
    )
    repos = "in the repositories your GitHub connection can see"
    if "archived:false" in terms:
        repos += ", archived repositories excluded"
    ordering = _ORDERING_WORDS.get((s, o), f"ordered by {s} {o}")
    return f"{state}{kind}{who}, {repos}", ordering


def _issues_note(*, total: int, count: int, scope: str, ordering: str) -> str:
    """The one sentence a client can quote (#2022; words are CXO's inside the two facts the
    constants fix: what was searched, and how the page is ordered)."""
    # CXO 10-31 08:48: "N of them" only when the page is cut; a whole page says "all of
    # them", and a single issue says "it". Both forms stay rendered from the same facts.
    if total == 1:
        return f"1 {scope.replace('issues', 'issue', 1)}; showing it, {ordering}."
    shown = "all of them" if count >= total else f"{count} of them"
    return f"{total} {scope}; showing {shown}, {ordering}."


def _github_issues_payload(issues: list[dict[str, Any]], total: int | None) -> dict[str, Any]:
    """Slim the page, state its scope, and keep the serialized section under the budget by
    dropping items from the tail. ``truncated`` is always derived (total > count), including
    after a trim; ``capped_at`` stays the page cap (Arch, #2241)."""
    items = [slim_issue(i) for i in issues if isinstance(i, dict)]
    scope, ordering = render_issues_scope()

    def _build(page: list[dict[str, Any]]) -> dict[str, Any]:
        count = len(page)
        # #2005: a missing total falls back to the page length, honestly not truncated as
        # far as this payload can tell.
        full_total = total if total is not None else len(items)
        return {
            "available": True,
            "scope": scope,
            "note": _issues_note(total=full_total, count=count, scope=scope, ordering=ordering),
            "issues": page,
            "count": count,
            "total": full_total,
            "truncated": full_total > count,
            "capped_at": GITHUB_ISSUES_PAGE_CAP,
        }

    payload = _build(items)
    while items and len(_json(payload)) > GITHUB_SECTION_BUDGET_CHARS:
        items = items[:-1]
        payload = _build(items)
    return payload


async def _read_github_issues() -> str:
    """``piper://me/github/issues`` — the user's open issues via their GitHub binding."""
    user_id = current_user_id()
    result = await GitHubMCPSpatialAdapter().list_open_issues(user_id, limit=GITHUB_ISSUES_PAGE_CAP)
    if result.issues is not None:
        return _json(_github_issues_payload(result.issues, result.total))
    degradation = result.degradation
    payload: dict[str, Any] = {
        "available": False,
        "connector": "github",
        "reason": degradation.reason.value if degradation else "unknown",
    }
    if degradation is not None:
        payload["message"] = degradation.user_message
    return _json(payload)


def register_resources(app: FastMCP) -> None:
    """Register the three owner-scoped resources onto ``app``.

    Called from ``services.mcp.server.app.register_resources`` (that module's own
    documented seam, unchanged in name/location so ``build_mcp_server()`` doesn't need to
    restructure) — kept here so the resource logic is independently testable without
    importing ``app.py``'s ASGI-wiring concerns.
    """
    app.resource(
        PROFILE_URI,
        name="profile",
        description=PROFILE_DESCRIPTION,
        mime_type="application/json",
    )(_read_profile)
    app.resource(
        COLLEAGUE_MODEL_URI,
        name="colleague-model",
        description=COLLEAGUE_MODEL_DESCRIPTION,
        mime_type="application/json",
    )(_read_colleague_model)
    app.resource(
        GITHUB_ISSUES_URI,
        name="github-issues",
        description=GITHUB_ISSUES_DESCRIPTION,
        mime_type="application/json",
    )(_read_github_issues)


# ---- Read-only tools (PM ruling 2026-10-01, Arch no-objection same day) ----
#
# ChatGPT discovers actions only via ``tools/list`` and has no documented path for
# MCP resources, so a resources-only server is unusable there ("its tools haven't
# been exposed" at PM's first live connection). Arch's conditions, all four
# load-bearing:
#   1. Tools COMPOSE the resource handlers above; they never re-implement a read,
#      so the tool and the resources are one source and cannot drift.
#   2. The set of tools is an exact allowlist, enforced at build time
#      (``app._restrict_capabilities``) and by the capability test.
#   3. No LLM call in any tool path. True by construction: every composed handler
#      reads ``user_context_service``, the #1510 preference store, or the GitHub
#      adapter only. A "summarise it for the client" edit crosses PDR-006's
#      no-server-LLM premise and must go back to Arch first.
#   4. PDR-006's own text is amended alongside (line ~276).
# Writes are tools too, but none exist; any write requires Arch review.

WHAT_PIPER_KNOWS_TOOL = "what_piper_knows_about_me"
READ_ONLY_TOOL_ALLOWLIST: tuple[str, ...] = (WHAT_PIPER_KNOWS_TOOL,)

WHAT_PIPER_KNOWS_DESCRIPTION = (
    "Read-only. Returns what Piper Morgan knows about the signed-in user, in one call: "
    "their profile (organization, active projects, stated priorities), their colleague "
    "model (what Piper has confirmed with them about how they work), and their open "
    "GitHub issues via their own connected GitHub account. Each section reports "
    "available=false or an explicit empty note rather than guessing; report empty "
    "sections as empty, never fill them in."
)


async def _section(read) -> Any:
    """One composed read, honest-degraded: a failing read yields its own
    ``available: false`` section, never a failed tool call."""
    try:
        return json.loads(await read())
    except Exception as e:  # silent-ok: per-section honest-degrade, mirrors the resources' own
        logger.warning("mcp_tool_section_read_failed", section=read.__name__, error=str(e))
        return {"available": False, "reason": "read_failed"}


async def what_piper_knows_about_me() -> dict[str, Any]:
    """Composite read-only tool. Composes the three resource handlers; no LLM call."""
    return {
        "profile": await _section(_read_profile),
        "colleague_model": await _section(_read_colleague_model),
        "github_issues": await _section(_read_github_issues),
    }


def register_tools(app: FastMCP) -> None:
    """Register exactly :data:`READ_ONLY_TOOL_ALLOWLIST`, each annotated read-only.

    ``readOnlyHint`` is advisory to the client (OpenAI: tools without it "are treated
    as write actions" and get confirmation prompts). It is not the guard. The guard is
    that every tool here only composes read functions.
    """
    app.tool(
        name=WHAT_PIPER_KNOWS_TOOL,
        title="What Piper knows about me",
        description=WHAT_PIPER_KNOWS_DESCRIPTION,
        annotations=ToolAnnotations(
            title="What Piper knows about me",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=False,
        ),
    )(what_piper_knows_about_me)
