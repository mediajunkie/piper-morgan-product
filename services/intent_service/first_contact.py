"""First-contact demonstration (#1536 FTUX-COLDSTART).

The user's own data in the FIRST exchange, unprompted. Design spec:
``dev/active/design-spec-first-contact-plugin-surface-2026-07-31.md`` §7a
(gate RULED 2026-08-10): (1) cold account + one connector authorized → the
first reply names at least one REAL entity from the user's own data;
(2) NO fabricated entities — a named entity is a stored-state claim and may
only come from a read that happened THIS turn; (3) "only Piper could produce
it" is conformance judgment, aimed at via specificity (real names, real
recency), never gated here.

How the pieces divide:

- ``is_first_exchange`` — the honest newness signal: the conversation has no
  COMPLETED exchange yet. By handler/gather time ``process_intent`` has
  hydrated turns from the DB when empty (#1122) and recorded the in-flight
  turn, so a new conversation shows ≤1 turn, none with a response. Scope is
  per-conversation: a returning user's brand-new conversation re-fires the
  demonstration, scoped to what is connected (spec §8 open question 3's lean).
- ``gather_first_contact_demo`` — the READ. Connector truth comes from the
  canonical ``IntegrationStatusService`` (#1547, binding-first; never the
  registry, whose plugins hardcode configured=False, #784). The repo comes
  from the #1042/#1327 default-repo rail (``resolve_repo``) — CXO item (i):
  when no repo resolves there is NO demo and NO "which repo?" question ahead
  of data; the normal greeting stands. Cached per #984 (TTL 300s — GitHub
  mutations are out-of-band, same family as high-priority issues).
- ``render_first_contact_block`` — deterministic user copy for the canonical
  greeting path. Pure string formatting over the gathered payload: it is
  structurally incapable of naming an entity the read didn't return (gate
  item 2). The floor path renders the same payload inside the
  ``[Available context]`` block (conversational_floor._format_domain_context)
  with a name-ONLY-these directive.

Honesty (#1425 / m-44): a FAILED read yields ``first_contact_source_failed``
(the floor renders "couldn't check", never emptiness); an EMPTY read yields
no demo at all — the MCP adapter returns [] on swallowed errors, so [] cannot
honestly be asserted as "your repo has nothing open".

Why not reuse ``feed_factory.WorkItemProvider`` (#1547-F4) directly: it
returns [] for BOTH read failure and genuine emptiness, which erases exactly
the failure/empty distinction the honesty rules above require, and it
assignee-filters (a cold account's brand-new binding often has nothing
assigned yet). The read below follows its binding-first shape (status-service
gate → router init → read → close per #1279) with failure kept distinct.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

import structlog

from services.utils.datetime_utils import ensure_utc, utc_now

logger = structlog.get_logger()

# Small on purpose: the demonstration is a taste of "I can see your work",
# not a report. Spec §3: specific, verifiable at a glance, bounded.
_FIRST_CONTACT_ITEM_CAP = 3

# #984 family: GitHub mutations are out-of-band → TTL-only, matches
# _TTL_HIGH_PRIORITY_ISSUES in context_assembler.
_TTL_FIRST_CONTACT = 300


def is_first_exchange(session_id: Optional[str], user_id: Optional[str] = None) -> bool:
    """True iff this conversation has no completed exchange yet.

    Fail-closed: any doubt (no session, unreadable context) → False — a
    skipped demonstration is recoverable; a wrongly-injected unprompted read
    on turn 40 is noise the user never asked for.
    """
    if not session_id:
        return False
    try:
        from services.intent_service.conversation_context import get_or_create_context

        conv_ctx = get_or_create_context(session_id, user_id=user_id)
        turns = getattr(conv_ctx, "turns", None) or []
        if any(getattr(t, "response", None) is not None for t in turns):
            return False
        return len(turns) <= 1  # at most the in-flight turn (#1122)
    except Exception as e:  # silent-ok: newness probe only gates a demo; a broken probe must never break the greeting, and False = no-demo (safe default, #1536)
        logger.warning("first_contact_newness_check_error", error=str(e))
        return False


def _humanize_recency(updated_at: Optional[str]) -> str:
    """Deterministic lived-time phrase from an ISO timestamp (voice: lived
    time, not clock time). Falls back to the raw date on parse trouble."""
    if not updated_at:
        return ""
    try:
        # GitHub returns Zulu time; fromisoformat needs +00:00 (#1573 pattern:
        # ensure_utc guards naive-vs-aware comparisons).
        parsed = ensure_utc(datetime.fromisoformat(str(updated_at).replace("Z", "+00:00")))
        if parsed is None:  # ensure_utc is None-in-None-out; fromisoformat never returns None, narrowed for mypy
            return f"updated {str(updated_at)[:10]}"
        days = (utc_now() - parsed).days
        if days <= 0:
            return "updated today"
        if days == 1:
            return "updated yesterday"
        if days < 14:
            return f"updated {days} days ago"
        return f"updated {parsed.strftime('%B %d')}"
    except Exception:  # silent-ok: pure display formatting; fallback renders the raw date rather than losing the row
        return f"updated {str(updated_at)[:10]}"


async def gather_first_contact_demo(
    user_id: Optional[str], cache: Any = None
) -> Dict[str, Any]:
    """Gather the first-contact demonstration payload for this user.

    NOT newness-gated — the caller gates on ``is_first_exchange``. Returns:

    - ``{"first_contact_demo": {...}}`` — connector configured, read
      succeeded, ≥1 real item
    - ``{"first_contact_source_failed": True}`` — connector configured but
      the read FAILED (#1425: flag, never fake)
    - ``{}`` — no principal / no configured connector / no resolvable repo /
      genuinely-or-indistinguishably empty read

    Principal-threaded: a None user_id performs no read at all.
    """
    if not user_id:
        return {}

    # Canonical connector truth (#1547) — never the registry (#784).
    try:
        from services.integrations.integration_status_service import (
            IntegrationStatusService,
        )

        if not await IntegrationStatusService().is_configured(user_id, "github"):
            # GitHub is the first (and currently only) first-contact source.
            # Calendar/Slack/Notion reads are cheap follow-ups: the status
            # gate above already covers them; each needs only its own
            # _compute + renderer lines.
            return {}
    except Exception as e:  # silent-ok: integration-status probe failure -> skip the demo ({}); the demo is an enhancement, never a gate on the turn
        logger.warning("first_contact_status_check_error", error=str(e))
        return {}

    if cache is None:
        from services.intent_service.context_cache import ContextCache

        cache = ContextCache()

    try:
        cached = await cache.get_or_compute(
            key=f"context:first_contact:{user_id}",
            ttl_seconds=_TTL_FIRST_CONTACT,
            compute_fn=lambda: _compute_first_contact_github(user_id),
        )
    except Exception as e:  # silent-ok: cache/gather failure -> skip the demo ({}); logged, and the floor makes no claim about it (#1536 AC3)
        logger.warning("first_contact_gather_error", error=str(e))
        return {}

    if not cached:
        return {}
    if cached.get("source_failed"):
        return {"first_contact_source_failed": True}
    if not cached.get("items"):
        return {}
    return {"first_contact_demo": cached}


async def _compute_first_contact_github(user_id: str) -> Optional[Dict[str, Any]]:
    """Compute the GitHub demonstration payload (uncached).

    Returns the payload dict, ``{"source_failed": True}`` on a failed read,
    or None when nothing can honestly be shown (no repo / empty read).
    """
    from uuid import UUID

    from services.integrations.github.repo_resolver import (
        UnresolvedRepoError,
        resolve_repo,
    )

    try:
        uid = UUID(str(user_id))
    except (ValueError, TypeError):
        uid = None

    try:
        resolved = await resolve_repo(user_id=uid)
    except UnresolvedRepoError:
        # CXO item (i): no bound/default repo → no data to show → no demo,
        # and crucially no "which repo?" question injected ahead of data.
        logger.info("first_contact_no_repo_resolved", user_id=user_id)
        return None
    except Exception as e:  # silent-ok: honest degrade — source_failed renders as "couldn't check", never fake-empty (#1425)
        logger.warning("first_contact_repo_resolve_error", error=str(e))
        return {"source_failed": True}

    try:
        from services.integrations.github.github_integration_router import (
            GitHubIntegrationRouter,
        )

        router = GitHubIntegrationRouter()
        try:
            await router.initialize(user_id=user_id)
            open_items = await router.get_open_issues(
                owner=resolved.owner, repo=resolved.name, limit=100
            )
        finally:
            await router.close()  # #1279: release the per-call aiohttp session
    except Exception as e:  # silent-ok: honest degrade — source_failed renders as "couldn't check", never fake-empty (#1425)
        logger.warning("first_contact_github_read_error", error=str(e))
        return {"source_failed": True}

    if not open_items:
        # [] conflates adapter-swallowed errors with genuine zero (the MCP
        # adapter returns [] on failure) — asserting emptiness would be an
        # unverified stored-state claim (m-44). No demo; behavior unchanged.
        return None

    ranked = sorted(open_items, key=lambda i: i.get("updated_at") or "", reverse=True)
    items: List[Dict[str, Any]] = [
        {
            "number": i.get("number"),
            "title": i.get("title"),
            "type": "pr" if i.get("is_pull_request") else "issue",
            "updated_at": i.get("updated_at"),
            "recency": _humanize_recency(i.get("updated_at")),
            "url": i.get("uri") or i.get("html_url"),
        }
        for i in ranked[:_FIRST_CONTACT_ITEM_CAP]
    ]
    return {
        "connector": "github",
        "repo": resolved.full_name,
        "items": items,
        # m-44: row-derived denominator — the count of what the read returned,
        # never the length of the display slice.
        "open_count": len(open_items),
    }


def render_first_contact_block(payload: Optional[Dict[str, Any]]) -> str:
    """Deterministic user-copy demonstration block (canonical greeting path).

    Pure string formatting over the gathered payload — structurally incapable
    of naming an entity the read didn't return (gate item 2). Scope is named
    INSIDE the primary claim (spec §3 boundedness: a trailing caveat is the
    construction that vanishes; an inline one can't be separated from the
    assertion). Returns "" when there is nothing honest to show.
    """
    if not payload:
        return ""
    items = payload.get("items") or []
    if not items:
        return ""

    repo = payload.get("repo") or "your connected repository"
    open_count = payload.get("open_count", len(items))
    noun = "open item" if open_count == 1 else "open items"

    lines = [
        f"Here's what I can already see in {repo} — the GitHub repo you've "
        f"connected: {open_count} {noun}, most recently active:"
    ]
    for it in items:
        kind = "PR" if it.get("type") == "pr" else "issue"
        recency = it.get("recency") or ""
        recency_part = f", {recency}" if recency else ""
        lines.append(f'• #{it.get("number")} "{it.get("title")}" ({kind}{recency_part})')
    lines.append("Want me to dig into any of these?")
    return "\n".join(lines)


async def first_contact_demo_block(
    session_id: Optional[str], user_id: Optional[str], cache: Any = None
) -> str:
    """The canonical-greeting seam: newness gate + gather + deterministic
    render, in one call. Returns "" unless a demonstration should append.

    A failed read appends NOTHING here (the greeting shouldn't open with an
    error report the user didn't ask for); the failure stays visible in logs
    and, on floor-bound turns, as the rendered "couldn't check" caution.
    """
    if not user_id or not is_first_exchange(session_id, user_id):
        return ""
    result = await gather_first_contact_demo(user_id, cache=cache)
    return render_first_contact_block(result.get("first_contact_demo"))
