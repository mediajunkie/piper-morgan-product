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
    "pretending to be 'no issues'. The returned page is capped; capped_at states the cap so "
    "a client can tell a short list from a truncated one."
)

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
    return _json(
        {
            "available": True,
            "organization": ctx.organization,
            "projects": ctx.projects,
            "projects_source": ctx.projects_source,
            "priorities": ctx.priorities,
        }
    )


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


async def _read_github_issues() -> str:
    """``piper://me/github/issues`` — the user's open issues via their GitHub binding."""
    user_id = current_user_id()
    result = await GitHubMCPSpatialAdapter().list_open_issues(user_id, limit=GITHUB_ISSUES_PAGE_CAP)
    if result.issues is not None:
        return _json(
            {
                "available": True,
                "issues": result.issues,
                "count": len(result.issues),
                "capped_at": GITHUB_ISSUES_PAGE_CAP,
            }
        )
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
