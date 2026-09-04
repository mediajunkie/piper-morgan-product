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
from services.utils.text_sanitation import display_title

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
        if (
            parsed is None
        ):  # ensure_utc is None-in-None-out; fromisoformat never returns None, narrowed for mypy
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


async def gather_first_contact_demo(user_id: Optional[str], cache: Any = None) -> Dict[str, Any]:
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

    # #1615: the chat frontend renders this through marked.parse
    # (web/assets/bot-message-renderer.js), where a single "\n" inside a
    # paragraph collapses to a space — "•"-glyph lines became one run-on
    # sentence in PM's 08-13 retest. Emit real markdown list syntax instead:
    # a blank line before/after the list and "- " items, which marked breaks
    # into <ul><li> rows.
    # #1539 purpose line (CXO final strings, 2026-08-22; PM confirmed the
    # articulation 08-21): the demo's WORDS carry the reassurance value prop
    # ("holds the threads"), not just capability ("look what I can see").
    # Honesty check done CXO-side: "keeping track of" is a true claim about
    # connected data — the gather re-reads real state; nothing persistent is
    # claimed that isn't.
    lines = [
        f"Here's what I'm already keeping track of in {repo} — the GitHub "
        f"repo you've connected: {open_count} {noun}, most recently active:",
        "",
    ]
    for it in items:
        kind = "PR" if it.get("type") == "pr" else "issue"
        recency = it.get("recency") or ""
        recency_part = f", {recency}" if recency else ""
        # #1628: degenerate GitHub titles (the literal "{" class) never render verbatim
        title = display_title(it.get("title"), f"(untitled {kind} #{it.get('number')})")
        lines.append(f'- #{it.get("number")} "{title}" ({kind}{recency_part})')
    lines.append("")
    lines.append("You don't need to hold this list — I've got it. Want to dig into any of these?")
    return "\n".join(lines)


# --- #1688: the FTUX empty-state interview (Leg D increment 1) --------------
#
# The sibling gap to the demo above: #1536 handles the RICH case (real held
# state -> honest demonstration) and honestly declines to fabricate in the
# EMPTY case -- which left the cold user (zero connected sources) meeting an
# ordinary greeting. The FTUX model (ftux-experience-model-2026-08-21.md) says
# that empty moment is where the most important work happens; the interview
# OWNS it (same rule that suppresses the #1635 Radar placeholder on empty).
#
# Copy is CXO's, VERBATIM, from the v0.2 copy spec
# (docs/internal/design/ftux-mcp-first-turn-copy-2026-09-02.md §3a), with ONE
# scope cut ruled by PPM 2026-09-03 (mail thread ruling-ppm-to-lead-...-1688):
# the spec's third string (`why_asking`) promised cross-session recall --
# a capability that belongs to increment 6 (#1705) and does not exist -- so it
# is CUT ENTIRELY, not reworded. The question ships alone ("a weaker true
# opening beats a strong false one" -- CXO's own stated fallback). No string
# on this surface may claim or imply persistence beyond the session.
#
# The answer BINDS at the offer seam per the #1654 carrier idiom (no new
# message-parsing regex -- the extraction ratchet is frozen): the interview
# arms a #846 pending-offer record; the next turn's substantive answer is
# stored into the session's ConversationContext (within-session use only) and
# the turn routes to the conversational floor so the reply engages with the
# answer's content. Declines, bare exits, and pre-classifier-claimed commands
# release WITHOUT binding.

# CXO v0.2 §3a literals -- pinned verbatim in
# tests/unit/services/intent_service/test_ftux_interview_1688.py. Do not edit
# without a new CXO ruling; drift fails there.
FTUX_INTERVIEW_OPENING_LINE = (
    "I don't have anything of yours in front of me yet — nothing's connected."
)
FTUX_INTERVIEW_QUESTION = "What's the thing most on your mind at work right now?"

# The #846 carrier vocabulary (the #1654 idiom).
FTUX_INTERVIEW_QUESTION_KIND = "ftux_interview_question"
FTUX_INTERVIEW_WORKFLOW = "ftux_interview"

# Honest decline copy: no claim about anything saved, remembered, or pending
# (#1648 action-claims contract; nothing WAS saved).
_FTUX_INTERVIEW_DECLINE = "No problem — we can start anywhere you like."


async def is_cold_user(user_id: Optional[str]) -> bool:
    """True iff the user has ZERO configured integrations (the interview's
    "nothing's connected" must be literally true before it renders).

    Canonical connector truth is ``IntegrationStatusService`` (#1547,
    binding-first) across the whole user-facing set -- never the registry
    (#784). Fail-closed both ways that matter: no principal or any status
    error -> False (no interview; a skipped interview is recoverable, a
    false "nothing's connected" over a connected account is a fabrication).
    """
    if not user_id:
        return False
    try:
        from services.integrations.integration_status_service import (
            IntegrationStatusService,
        )

        statuses = await IntegrationStatusService().get_all(user_id)
        return not any(s.get("configured") for s in statuses.values())
    except Exception as e:  # silent-ok: cold probe only gates the interview; a broken probe must never break the greeting, and False = no-interview (safe default, #1688)
        logger.warning("ftux_interview_cold_check_error", error=str(e))
        return False


def render_ftux_interview() -> str:
    """The interview opening, CXO's two strings verbatim, nothing else.

    Deterministic user copy (the render_first_contact_block discipline):
    structurally incapable of adding a promise the increment doesn't keep.
    """
    return f"{FTUX_INTERVIEW_OPENING_LINE}\n\n{FTUX_INTERVIEW_QUESTION}"


def build_ftux_interview_offer(user_id: Optional[str]) -> Dict[str, Any]:
    """The #846 pending-offer record arming the interview question.

    ``question`` (#1665): the ask verbatim as rendered -- stored on the
    record so the SessionSnapshot's pending_offer_question matches what the
    user saw. An open question, NOT a yes/no (outside the #1664
    confirm-kind set, like the repo question and the #1654 task question).
    """
    return {
        "workflow_type": FTUX_INTERVIEW_WORKFLOW,
        "question": FTUX_INTERVIEW_QUESTION,
        "pending_action": {
            "kind": FTUX_INTERVIEW_QUESTION_KIND,
            "action": "ftux_interview",
            "user_id": str(user_id) if user_id else None,
            "summary": "answer the opening question",
        },
        "decline_message": _FTUX_INTERVIEW_DECLINE,
    }


async def ftux_interview_greeting(
    session_id: Optional[str], user_id: Optional[str]
) -> Optional[Dict[str, Any]]:
    """The greeting seam: first-exchange gate + cold gate, in one call.

    Returns ``{"message": <rendered interview>, "offer": <#846 record>}``
    when the interview owns this greeting, else None (the normal greeting
    stands). Ordering: newness first (cheap, in-memory) then coldness (a
    status read). Fail-closed at both gates.

    The interview REPLACES the canned greeting rather than appending to it
    (the demo-block pattern): the canned greeting ends in its own question
    ("What would you like to work on today?"), and two competing questions
    is the plain greeting wearing a costume. The empty moment is owned or
    it isn't.
    """
    if not user_id or not is_first_exchange(session_id, user_id):
        return None
    if not await is_cold_user(user_id):
        return None
    return {
        "message": render_ftux_interview(),
        "offer": build_ftux_interview_offer(user_id),
    }


def _bind_interview_answer(session_id: str, user_id, answer: str) -> bool:
    """Store the answer as session-scoped working state (within-session use
    ONLY -- cross-session recall is #1705 and does not exist). Returns False
    on any failure so the caller releases instead of claiming a binding."""
    try:
        from services.intent_service.conversation_context import get_or_create_context

        conv_ctx = get_or_create_context(session_id, user_id=user_id)
        conv_ctx.ftux_interview_answer = answer
        return True
    except Exception as e:  # silent-ok: a failed bind releases the turn to normal routing (the floor still answers); logged, never crashes the turn
        logger.warning("ftux_interview_bind_error", error=str(e))
        return False


async def handle_ftux_interview_turn(
    pending_offer: dict,
    message: str,
    *,
    session_id: str,
    user_id,
    intent_service,
) -> Optional[dict]:
    """#1688 -- kind-specific turn handling for a pending interview question,
    run at the offer seam BEFORE any classification surface (the #1605/#1648
    sanctioned handler-internal seam; the pop already happened).

    Returns a ``{"message", "intent_data"}`` dict when this turn is consumed
    here, ``{"route_to_floor": True, ...}`` when the answer bound and the
    reply should be composed on the floor (so the turn ENGAGES with the
    answer's content -- deterministic dispatch, never re-classification), or
    ``None`` to fall through to the generic offer flow (declines and bare
    exits drop honestly via ``decline_message``; pre-classifier-claimed
    commands abandon via the pop and route normally).

    Off-intent discrimination follows #1654's exactly: the answer space is
    arbitrary work talk, so the discriminator is the pre-classifier's
    DETERMINISTIC claim, never a verb-shape read. No time/task extraction --
    the answer binds WHOLE (extraction ratchet frozen; nothing to parse).
    """
    text = (message or "").strip()
    if not text:
        return None

    payload = pending_offer.get("pending_action") or {}

    # Principal binding (the #1605 discipline): the question was asked of the
    # user who greeted -- a different principal's turn releases unbound.
    offer_user = payload.get("user_id")
    if offer_user and user_id and str(user_id) != str(offer_user):
        logger.warning(
            "ftux_interview_principal_mismatch",
            offer_user=offer_user,
            turn_user=str(user_id),
        )
        return None

    from services.intent_service.destructive_confirm import detect_bare_exit
    from services.intent_service.soft_invocation import detect_offer_response

    if detect_bare_exit(text):
        return None  # generic flow -> honest decline via decline_message
    resp = detect_offer_response(text)
    if resp == "decline":
        return None  # same honest decline path

    if resp == "accept":
        # A bare "yes" doesn't answer an open question -- re-ask verbatim
        # (#1648 direction 2: the honest re-ask, never a silent abandon).
        # If re-arming fails the question still renders; the next turn just
        # routes normally (degraded, never dishonest -- nothing is claimed).
        try:
            intent_service.workflow_offer_service.set_pending_offer(
                session_id, pending_offer, user_id=user_id
            )
        except Exception as e:  # silent-ok: a failed re-arm degrades to normal routing next turn; logged ERROR, copy stays honest (claims nothing)
            logger.error("ftux_interview_rearm_failed", error=str(e))
        return {
            "message": FTUX_INTERVIEW_QUESTION,
            "intent_data": {
                "category": "conversation",
                "action": "ftux_interview",
                "ftux_interview_question_pending": True,
            },
        }

    # Off-intent: a turn the pre-classifier claims deterministically is a
    # product command -- release it unbound (routes normally; the question
    # is abandoned per the carrier's rules). Same granularity as #1654 and
    # for the same reason: verb-shape reads claim legitimate answers.
    from services.intent_service.pre_classifier import PreClassifier

    claimed = PreClassifier.pre_classify(text)
    if claimed is not None:
        logger.info(
            "ftux_interview_command_released",
            session_id=session_id,
            claimed_action=claimed.action,
        )
        return None

    # The turn IS the answer. Bind it whole -- session-scoped, within-session
    # use only -- then compose the reply on the floor so this turn engages
    # with the content (the bound answer is already in context for the
    # assembler by the time the floor gathers).
    if not _bind_interview_answer(session_id, user_id, text):
        return None  # failed bind -> honest release; normal routing answers
    logger.info("ftux_interview_answer_bound", session_id=session_id)
    return {
        "route_to_floor": True,
        "intent_data": {
            "category": "conversation",
            "action": "ftux_interview_answer",
            "ftux_interview_answer_bound": True,
        },
    }


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
