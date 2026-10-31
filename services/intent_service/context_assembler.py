"""
Context Assembler for Conversational Floor (#911 Phase 2)

Gathers structured data for the conversational floor, organized by intent
category. The floor LLM receives raw facts and decides what's relevant to
the user's question.

Design principles:
1. Declarative — returns structured data (facts, lists), not formatted text
2. Fail-graceful — partial results on failure, never throws
3. Cached — Redis TTL caching via ContextCache (#984, PM-approved TTLs
   2026-05-12; fail-open: any Redis error → cache miss → compute from source)

Stable vs dynamic (973 audit, 2026-09-09) — the stable/dynamic split the
original design deferred is realized as per-source TTLs rather than a binary:
- STABLE (cached, longer TTL): trust (1h); projects, user_context,
  completed_todos, blocked_items, active_milestones, recent_activity,
  high_priority_issues (5min)
- SEMI-STABLE (cached, short TTL): calendar (60s — only external API call);
  pending_todos, reminders (30s, eager-invalidated on todo CRUD)
- DYNAMIC (per-request/per-session, deliberately uncached): current_time,
  identity/discovery (pure ledger read + live integration status +
  in-memory session state), conversation memory, insight pull, the
  per-session reminder mention gate (#1625), the ftux bound answer (#1688)
Assembly order is category dispatch + cross-cutting riders; ordering has no
caching consequence because caching is per-source inside get_or_compute,
not prompt-prefix-based.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

import structlog

from services.intent_service.context_cache import ContextCache
from services.utils.datetime_utils import ensure_utc, utc_now

logger = structlog.get_logger()


async def _current_time_for_user(user_id=None) -> str:
    """Current time in the USER's timezone, e.g. '12:54 PM PDT' — or "" (omit).

    #1150 made this configured-tz-aware via the single PM config file; #1381
    found the hosted consequence: on the multi-user droplet that file (or its
    naive-``datetime.now()`` fallback — a UTC container clock) fed every user
    the WRONG local time, and Piper confidently narrated "4:30 AM — you're
    either an early riser or deep in a late night" at 9:32 PM Pacific.

    Precedence: the user's own timezone from their personalization context
    (ADR-075 D1 carries one) → the file config (the single-tenant/local path,
    unchanged) → EMPTY STRING. The empty string is the #1381 fix's core rule:
    when we don't know the user's timezone we OMIT the time-of-day flourish
    (the floor's renderer skips absent keys) rather than guess from the server
    clock — a wrong confident time is worse than none.
    """
    tz_name = None
    if user_id:
        try:
            from services.configuration.personalization_repository import (
                PersonalizationContextRepository,
            )
            from services.database.session_factory import AsyncSessionFactory

            async with AsyncSessionFactory.session_scope() as session:
                row = await PersonalizationContextRepository(session).get(user_id)
            if row is not None and isinstance(row.context, dict):
                tz_name = row.context.get("timezone") or None
        except Exception:
            tz_name = None  # graceful: fall through to the file config
    if not tz_name:
        try:
            from services.configuration.piper_config_loader import piper_config_loader

            tz_name = piper_config_loader.load_standup_config()["timing"]["timezone"]
        except Exception:
            tz_name = None
    if not tz_name:
        return ""
    try:
        from zoneinfo import ZoneInfo

        return datetime.now(ZoneInfo(tz_name)).strftime("%I:%M %p %Z")
    except Exception:  # silent-ok: pure display; a stored bad tz would log every turn — no clock face beats a wrong one (#1589 rationale)
        return ""


# #984: TTL defaults per data type (PM-approved 2026-05-12).
# Short TTLs on user-mutable data (todos, reminders); longer on slow-
# changing data (projects, user_context, trust). Calendar is short because
# it's the only external API call (Google/MS Graph) where rate-limit risk
# is real.
_TTL_CALENDAR = 60
_TTL_TRUST = 3600  # 1h — trust-stage transitions are rare events
_TTL_REMINDERS = 30
_TTL_PENDING_TODOS = 30
_TTL_COMPLETED_TODOS = 300
_TTL_PROJECTS = 300
_TTL_USER_CONTEXT = 300
_TTL_BLOCKED_ITEMS = 300  # #983: GitHub mutations are out-of-band — TTL-only
_TTL_ACTIVE_MILESTONES = 300  # #985: milestone state changes slowly; TTL-only
_TTL_RECENT_ACTIVITY = 300  # #986: activity churns but 5min freshness OK
_TTL_HIGH_PRIORITY_ISSUES = 300  # #1155: GitHub mutations out-of-band — TTL-only

# #983: canonical label for "blocked items" (PM disposition 2026-05-05;
# Architect correction 2026-05-10). Matches `docs/internal/operations/labels-reference.md`.
_BLOCKED_LABEL = "status: blocked"

# #985: cap on milestones surfaced to floor. Repo has 4 open today; cap at 5
# for headroom without bloating context.
_ACTIVE_MILESTONES_CAP = 5

# #986: recent-activity window and cap. 7 days is the standard PM/standup
# cadence; 10 events surfaced so floor can compose specific recall.
_RECENT_ACTIVITY_WINDOW_DAYS = 7
_RECENT_ACTIVITY_CAP = 10

# #1155: priority labels in descending urgency; open issues carrying these rank
# first in the "what should I focus on" context, then most-recently-updated.
_PRIORITY_LABELS = ("priority: critical", "priority: urgent", "priority: high")
_HIGH_PRIORITY_ISSUES_CAP = 5

# #1625: per-session mentioned-set for due reminders. PM's ruling (v53 live,
# 2026-08-15): mention due reminders ONCE per conversation, then stay quiet —
# the Radar pin owns persistence. Keyed on reminder IDENTITY (the surfaced
# text), NOT a boolean, so "once" cannot become "never": a genuinely NEW
# reminder coming due mid-session is still mentioned once even after earlier
# ones were. Same lifetime class as the rail's session memory
# (verified_inference._SESSION_DECLINES): transient per-process conversational
# state, session-keyed, NEVER persisted as a preference. Capped so long-lived
# processes don't grow it unboundedly; eviction is oldest-session-first (dict
# insertion order).
_SESSION_REMINDER_MENTIONS: Dict[str, set] = {}
_SESSION_REMINDER_MENTIONS_MAX_SESSIONS = 2048


def _unmentioned_reminders(session_id: Optional[str], reminders: List[str]) -> List[str]:
    """#1625: the due reminders this session has NOT yet been told about."""
    if not session_id:
        return list(reminders)
    mentioned = _SESSION_REMINDER_MENTIONS.get(str(session_id), set())
    return [r for r in reminders if r not in mentioned]


def _mark_reminders_mentioned(session_id: Optional[str], reminders: List[str]) -> None:
    """#1625: record that this session's floor turn carried these reminders."""
    if not session_id or not reminders:
        return
    sid = str(session_id)
    if (
        sid not in _SESSION_REMINDER_MENTIONS
        and len(_SESSION_REMINDER_MENTIONS) >= _SESSION_REMINDER_MENTIONS_MAX_SESSIONS
    ):
        _SESSION_REMINDER_MENTIONS.pop(next(iter(_SESSION_REMINDER_MENTIONS)))
    _SESSION_REMINDER_MENTIONS.setdefault(sid, set()).update(reminders)


def _compute_deadline_proximity(due_date: Optional[datetime]) -> str:
    """
    #951: Bucket a due_date into a proximity label for floor context.

    Returns one of:
    - "none": no due_date
    - "overdue": due_date is in the past
    - "due_today": due_date is today (before end of day, not yet past)
    - "due_this_week": due in the next 1-7 days
    - "later": due > 7 days out

    #1573 (time audit F5, #1491 pattern): both sides normalized aware-UTC.
    The previous naive `datetime.now()` raised TypeError against the
    timestamptz-aware due_date every real todo row carries, which was
    warning-swallowed upstream — the user's pending todos silently
    vanished from floor context. "Today" is the UTC day until a per-user
    timezone exists (audit root cause; #586 territory).
    """
    if due_date is None:
        return "none"

    due = ensure_utc(due_date)
    if (
        due is None
    ):  # ensure_utc is None-in-None-out; guarded above, narrowed here for mypy and for honesty if the guard ever moves
        return "none"
    now = utc_now()
    if due < now:
        return "overdue"

    end_of_today = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    if due <= end_of_today:
        return "due_today"

    end_of_week = now + timedelta(days=7)
    if due <= end_of_week:
        return "due_this_week"

    return "later"


def _todo_to_dict(todo: Any) -> Dict[str, Any]:
    """
    #951: Serialize a Todo-like object into the floor context dict shape.

    Includes text, priority, due_date (ISO string or None), and
    deadline_proximity (one of the 5 proximity buckets). Matches what
    the floor formatter will surface and what tests assert against.
    """
    due_date = getattr(todo, "due_date", None)
    return {
        "text": todo.text,
        "priority": getattr(todo, "priority", "medium"),
        "due_date": due_date.isoformat() if due_date else None,
        "deadline_proximity": _compute_deadline_proximity(due_date),
    }


def _counts_by_source(items: List[Dict[str, Any]]) -> Dict[str, int]:
    """#2142: how many items each source contributed to the merged feed."""
    counts: Dict[str, int] = {}
    for item in items:
        source = item.get("source") or "unknown"
        counts[source] = counts.get(source, 0) + 1
    return counts


def _github_read_not_performed(exc: BaseException) -> bool:
    """#2151 (Arch 10-23 21:28): a GitHub read that was NOT PERFORMED, not failed — the
    user never connected (a CONNECT_REQUIRED degrade, or the REST path's
    ``detail="no_credential"``: no grant and no PAT), or no repository resolved. The
    gather returns {} with no source-failed flag, so the floor neither says "couldn't
    check" nor claims absence."""
    from services.integrations.github.read_failed import GitHubReadFailed
    from services.mcp.consumer.connector import DegradationReason

    if not isinstance(exc, GitHubReadFailed):
        return False
    return exc.reason in (
        DegradationReason.CONNECT_REQUIRED,
        DegradationReason.REPO_UNRESOLVED,
    ) or (exc.reason is None and exc.detail == "no_credential")


class _CalendarReadFailed(Exception):
    """#2151 FLOOR-ABSENT: a calendar read that did not happen (an error summary, an
    events read never established, or the adapter's ``last_read_error``)."""


def _calendar_feature_off(exc: BaseException) -> bool:
    """The router has no calendar integration (the feature is off on this deployment):
    not performed, so no "couldn't check" line."""
    return isinstance(exc, RuntimeError) and str(exc).startswith(
        "No calendar integration available"
    )


class _UserContextReadFailed(Exception):
    """#2151 FLOOR-ABSENT (Arch 2026-10-29 21:08): a user-context read that FAILED for
    part or all of the context. ``partial`` holds the parts that were read (shown, per
    CXO's bar: one failure must not blank the rest); ``flags`` are the registered
    source-failed flags the STATUS gather arms. Raised, so the context cache never
    stores a failure."""

    def __init__(self, partial: Dict[str, Any], flags: Tuple[str, ...]) -> None:
        super().__init__(", ".join(flags))
        self.partial = partial
        self.flags = flags


class _SlackReadFailed(Exception):
    """#2151 FLOOR-ABSENT: a Slack read that did not happen for a connected account."""


# Slack's own "never could read this" answers (not connected, or a scope the workspace
# never granted: search.messages needs search:read). Not performed, never "couldn't check".
_SLACK_NOT_PERFORMED_ERRORS = frozenset({"not_authed", "missing_scope", "no_permission"})


def _slack_read_or_raise(resp: Any, what: str) -> Optional[Dict[str, Any]]:
    """#2151: the response data when the read happened; None when Slack says it never
    could (``_SLACK_NOT_PERFORMED_ERRORS``); RAISES ``_SlackReadFailed`` otherwise. Slack
    answers an auth failure with HTTP 200 and ``ok: false``, which the client passes
    through as ``success=True``, so ``data["ok"]`` is read too."""
    data = (getattr(resp, "data", None) or {}) if resp is not None else {}
    error = data.get("error") if isinstance(data, dict) else None
    if resp is not None and getattr(resp, "success", False) and data.get("ok", True) is not False:
        return data
    if error in _SLACK_NOT_PERFORMED_ERRORS:
        return None
    detail = error or getattr(getattr(resp, "error", None), "message", None) or "failed"
    raise _SlackReadFailed(f"{what}: {detail}")


class _PartialSourceRead(Exception):
    """#2151 FLOOR-ABSENT: a multi-source compute where some sources failed. Carries
    the sources that were read (``result``, possibly None) and the registered flags of
    the ones that failed. Raised, not returned, so ``get_or_compute`` caches nothing:
    the next turn reads again instead of serving a known-partial result for the TTL."""

    def __init__(self, result: Optional[Dict[str, Any]], flags: List[str]):
        super().__init__(f"sources failed: {', '.join(flags)}")
        self.result = result
        self.flags = flags


class ContextAssembler:
    """Gathers structured context for the conversational floor."""

    def __init__(self, cache: Optional[ContextCache] = None):
        """Initialize with an optional cache override (for testing).

        #984: Default cache is a freshly-constructed ContextCache. The cache
        is shared across all gather methods on this instance. Graceful-
        fallback: any Redis error → cache miss → compute from source.
        """
        self.cache = cache or ContextCache()
        # Issue #1030 R4: per-call provenance map. Reset at gather_context()
        # entry, populated as each gatherer runs, retrieved via get_last_provenance().
        # Keyed by the domain_context key (e.g. "insights", "calendar"), value is
        # a dict {source, identifier?, fetch_timestamp, ...} describing where
        # that key's data came from.
        self._last_provenance: Dict[str, Dict[str, Any]] = {}

    def get_last_provenance(self) -> Dict[str, Dict[str, Any]]:
        """Issue #1030 R4: return provenance map from the most recent
        gather_context() call. Caller (intent_service) passes this through
        to FloorContext.domain_context_provenance.

        Returns the same dict reference (not a copy) — caller should not mutate.
        Always returns a dict (possibly empty).
        """
        return self._last_provenance

    # Issue #1030 R4: source mapping for each domain_context key. Per key,
    # the canonical source identifier + integration/repo origin. Centralizes
    # provenance attribution so each gatherer doesn't repeat itself, and so
    # adding a new key requires registering its source HERE (catches the
    # R5 risk: formatter/provenance drift).
    _KEY_SOURCES: Dict[str, Dict[str, str]] = {
        # Calendar
        "calendar": {"source": "CalendarIntegrationRouter", "integration": "google_calendar"},
        # Todos
        "pending_todos": {"source": "TodoManagementService", "filter": "open"},
        "completed_todos": {"source": "TodoManagementService", "filter": "completed"},
        # GitHub
        "blocked_items": {"source": "GitHubIntegrationRouter", "filter": "label:status:blocked"},
        "active_milestones": {"source": "GitHubIntegrationRouter", "filter": "state:open"},
        "recent_activity": {"source": "MultiSourceAggregator", "sources": "github+calendar+slack"},
        # User profile / context
        "user_projects": {"source": "UserContextService"},
        "organization": {"source": "UserContextService"},
        "user_priorities": {"source": "UserContextService"},
        "priorities": {"source": "UserContextService+GitHub"},
        "urgent_items": {"source": "GitHubIntegrationRouter", "filter": "priority:high"},
        # Conversation / memory
        "recent_topics": {"source": "ConversationContext"},
        "session_turn_count": {"source": "ConversationContext"},
        "conversation_history_summary": {"source": "ConversationContext"},
        "persistent_memory": {"source": "UserHistoryService"},
        # Identity / capabilities
        "capabilities": {"source": "ChatPointersLedger"},  # #1428
        "integrations": {"source": "PluginRegistry"},
        # Trust
        "trust_profile": {"source": "UserTrustProfileRepository"},
        # Insights (Issue #1030)
        "insights": {"source": "InsightRepository"},
        # Temporal
        "current_date": {"source": "ServerClock"},
        "current_day_of_week": {"source": "ServerClock"},
        # Reminders
        "reminders": {"source": "ReminderService"},
        # #1566: due-reminder keys ride every gather_context call
        "due_reminders": {"source": "TodoIntentHandlers.get_due_reminders"},
        "reminder_count": {"source": "TodoIntentHandlers.get_due_reminders"},
        "projects": {"source": "ProjectManagementService"},
        # #1530 (m-44): row-derived denominator riding with the sliced list
        "project_count": {"source": "UserContextService"},
        # #1536 FTUX-COLDSTART: first-exchange demonstration — the read that
        # licenses the floor to name the user's entities on a cold first turn
        "first_contact_demo": {
            "source": "GitHubIntegrationRouter",
            "filter": "state:open, recency-ranked",
        },
        "first_contact_source_failed": {"source": "GitHubIntegrationRouter"},
        # #1688: the FTUX interview's bound answer -- session-scoped working
        # state from the offer seam; within-session use only (#1705 owns
        # cross-session).
        "ftux_interview_answer": {"source": "ConversationContext"},
    }

    def _attribute_provenance(
        self,
        keys: List[str],
        user_id: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Issue #1030 R4: record provenance entries for a set of keys.

        Each entry gets the canonical source from _KEY_SOURCES (or a generic
        fallback if unknown), plus a fetch_timestamp, plus user_id when
        relevant, plus any extra metadata the caller provides (e.g. dedup
        decisions for recent_activity per R3).
        """
        ts = datetime.now(timezone.utc).isoformat()
        for key in keys:
            base = dict(self._KEY_SOURCES.get(key, {"source": "ContextAssembler"}))
            base["fetch_timestamp"] = ts
            if user_id:
                base["user_id_scoped"] = True
            if extra:
                base.update(extra)
            self._last_provenance[key] = base

    async def gather_context(
        self,
        intent_category: str,
        user_id: str = None,
        session_id: str = None,
        intent_action: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Main entry point. Returns structured data for floor injection.

        Routes to category-specific gatherers based on intent_category +
        optional intent_action (Issue #1030: action-aware routing so
        MEMORY/pull_insights gets InsightRepository enrichment distinct
        from MEMORY/get_memory conversation-history enrichment).
        Always returns a dict (possibly empty on total failure).
        """
        context: Dict[str, Any] = {}

        # Issue #1030 R4: reset per-call provenance map at gather_context entry
        self._last_provenance = {}

        # Current time — in the USER's timezone (#1381) or omitted entirely;
        # the floor's renderer skips the line when the key is absent. Never
        # the server clock in user clothing.
        _ct = await _current_time_for_user(user_id)
        if _ct:
            context["current_time"] = _ct
        # current_time has no provenance (always-available system value); we
        # deliberately don't attribute it — it's not a "fact about the user"
        # subject to "why did you cite that?"

        category = (intent_category or "").upper()
        action = intent_action or ""

        try:
            if category in ("IDENTITY", "DISCOVERY"):
                ctx = await self._gather_identity_context(user_id, session_id)
                context.update(ctx)
                self._attribute_provenance(list(ctx.keys()), user_id=user_id)
            elif category == "TRUST":
                ctx = await self._gather_trust_context(user_id)
                context.update(ctx)
                self._attribute_provenance(list(ctx.keys()), user_id=user_id)
            elif category == "MEMORY" and action == "pull_insights":
                # Issue #1030 INSIGHT-PULL: fetch insights from InsightRepository
                # for the floor to surface, sectioned by confidence band.
                ctx = await self._gather_insight_pull_context(user_id)
                context.update(ctx)
                self._attribute_provenance(list(ctx.keys()), user_id=user_id)
            elif category == "MEMORY":
                ctx = await self._gather_memory_context(user_id, session_id)
                context.update(ctx)
                self._attribute_provenance(list(ctx.keys()), user_id=user_id)
            # #1596: the CONVERSATION special-case (`pass` — deliberately-
            # minimal context "for greetings") is REMOVED; CONVERSATION now
            # falls to the #960 else-branch baseline below. The rationale it
            # carried was keyed to a caller that no longer exists: pure
            # pleasantries take the canned canonical greeting and never reach
            # this assembler, while the turns that DO arrive here as
            # CONVERSATION are the classifier's vague/low-confidence rewrite
            # (`clarification_needed` — exactly where post-guided-flow-escape
            # fragments like PM's verbatim 'none' land), compound greetings
            # (#1416), and chitchat/farewell floor turns. Those floored with
            # domain_context ≈ {current_time} — the wrong-empty half of the
            # #1529-transcript floor amnesia (the history half was #1394).
            # The #960 rationale applies a fortiori: a clarification turn's
            # whole job is to re-anchor the conversation in real entities.
            elif category == "TEMPORAL":
                # #965: Temporal context for non-date queries (agenda, retrospective, etc.)
                ctx = await self._gather_temporal_context(user_id, session_id)
                context.update(ctx)
                self._attribute_provenance(list(ctx.keys()), user_id=user_id)
            elif category in ("STATUS", "PRIORITY"):
                # #925: Project status and priority context for floor
                ctx = await self._gather_status_priority_context(user_id)
                context.update(ctx)
                self._attribute_provenance(list(ctx.keys()), user_id=user_id)
            else:
                # #960: UNKNOWN and other unhandled categories get basic user
                # context to reduce fabrication risk. Better to give the floor
                # real entities (even if not the right ones for the specific
                # query) than zero context where it might invent data.
                # #1596: CONVERSATION lands here too (see the removed
                # special-case above) — clarification/chitchat floor turns
                # get the same baseline UNKNOWN always had.
                if user_id:
                    ctx = await self._gather_status_priority_context(user_id)
                    context.update(ctx)
                    self._attribute_provenance(list(ctx.keys()), user_id=user_id)
        except Exception as e:
            logger.warning(
                "context_assembler_gather_error",
                category=category,
                error=str(e),
            )

        # #1566: due reminders ride EVERY floor-bound turn, not only
        # CONVERSATION greetings (#903's original scope). PM live 8/10: four
        # due-now reminders + 15 minutes of STATUS/EXECUTION/TEMPORAL turns
        # with zero surfacing. Gathered OUTSIDE the category dispatch's try
        # so a category-gatherer failure can't take reminders down with it
        # (and vice versa). Cost: cached TTL-30s (#984) — a dict merge on
        # hits. #1425 honesty preserved: a failed lookup merges
        # source_failed=True, which the floor renders as "couldn't check",
        # never "none due".
        # #2233 (Arch/CXO): the model sees ``due_reminders`` only on an op whose handler
        # needs it for its own answer (the reminder list). Everywhere else code places
        # one line after the answer (due_reminder_line.py), so the model never voices it.
        from services.intent_service.workflow_dispatcher import (
            DUE_REMINDER_SELF_RENDERING_OPS,
            normalize_action,
        )

        _ride_reminders = (
            bool(intent_action)
            and normalize_action(str(intent_action)) in DUE_REMINDER_SELF_RENDERING_OPS
        )
        try:
            reminder_ctx = await self._gather_reminder_context(user_id) if _ride_reminders else {}
            # #1625: gate the conversational mention AFTER the #984 cache (the
            # cached slice is per-user; the mention gate is per-session — gating
            # inside the cached compute would leak one session's quiet into
            # another's first mention).
            if reminder_ctx and reminder_ctx.get("due_reminders"):
                reminder_ctx = await self._gate_due_reminder_mentions(
                    reminder_ctx, user_id, session_id
                )
            if reminder_ctx:
                context.update(reminder_ctx)
                self._attribute_provenance(list(reminder_ctx.keys()), user_id=user_id)
                # #1985 (b) / CXO 2026-10-12: an item that is BOTH a pending todo
                # and a due reminder appears once — in the reminder block (the
                # floor prompt already says so; the model did not always obey,
                # so the context no longer offers it twice). Match on text: a
                # due reminder IS a todo's text (get_due_reminders).
                _due_texts = {
                    str(r).strip().casefold() for r in (context.get("due_reminders") or [])
                }
                if _due_texts and context.get("pending_todos"):
                    _before = len(context["pending_todos"])
                    context["pending_todos"] = [
                        td
                        for td in context["pending_todos"]
                        if str(td.get("text", "")).strip().casefold() not in _due_texts
                    ]
                    _moved = _before - len(context["pending_todos"])
                    if _moved:
                        # #1997: a list this dedup emptied is NOT "no pending
                        # todos" (alpha 651756d520: "Your todo list is clear"
                        # beside the three reminders that were the list).
                        # Carry how many moved so the floor says so.
                        context["pending_todos_in_reminders"] = _moved
        except Exception as e:  # silent-ok: reminder slice is additive; failure merges source_failed upstream so the floor says "couldn't check", never "none due" (#1425/#1566)
            logger.warning("context_assembler_reminder_gather_error", error=str(e))

        # #1536 FTUX-COLDSTART: on the FIRST exchange of a conversation, when
        # the user has a configured connector, gather a small recent slice of
        # their real data so the first reply demonstrates with THEIR entities
        # instead of greeting generically. Rides OUTSIDE the category dispatch
        # (the #1566 pattern) so any floor-bound first turn gets it — a cold
        # first message needn't be a greeting — and a first-contact failure
        # can't take the rest of the context down (or vice versa). Newness is
        # per-conversation: no completed exchange yet (#1122 in-flight turn
        # semantics; see first_contact.is_first_exchange). Cached per #984.
        # #1425 honesty: a failed read merges first_contact_source_failed,
        # which the floor renders as "couldn't check", never a fake demo.
        if user_id and session_id:
            try:
                from services.intent_service import first_contact as _first_contact

                if _first_contact.is_first_exchange(session_id, user_id):
                    fc_ctx = await _first_contact.gather_first_contact_demo(
                        user_id, cache=self.cache
                    )
                    if fc_ctx:
                        context.update(fc_ctx)
                        self._attribute_provenance(list(fc_ctx.keys()), user_id=user_id)
            except Exception as e:  # silent-ok: first-contact demo is an enhancement; failure skips the demo, logged, and the greeting proceeds without a claim (#1536)
                logger.warning("context_assembler_first_contact_error", error=str(e))

        # #1688: the FTUX interview's bound answer rides every floor-bound
        # turn for the rest of the session (within-session use is the whole
        # deliverable; cross-session is #1705). Rides OUTSIDE the category
        # dispatch like the #1536 block above, and a read failure can't take
        # the rest of the context down.
        if session_id:
            try:
                from services.intent_service.conversation_context import (
                    get_or_create_context,
                )

                _ftux_answer = get_or_create_context(
                    session_id, user_id=user_id
                ).ftux_interview_answer
                if _ftux_answer:
                    context["ftux_interview_answer"] = _ftux_answer
                    self._attribute_provenance(["ftux_interview_answer"], user_id=user_id)
            except Exception as e:  # silent-ok: the bound answer is an enhancement; failure omits it, logged, and the floor composes without it (#1688)
                logger.warning("context_assembler_ftux_answer_error", error=str(e))

        # #960: Context contract violation logging — warn when a data-query
        # category reaches the floor with no user data in context.
        _DATA_CATEGORIES = {"TEMPORAL", "STATUS", "PRIORITY"}
        _DATA_KEYS = {"pending_todos", "completed_todos", "projects", "priorities"}
        if category in _DATA_CATEGORIES:
            has_data = any(k in context for k in _DATA_KEYS)
            if not has_data:
                logger.warning(
                    "context_contract_empty_data",
                    category=category,
                    user_id=user_id,
                    session_id=session_id,
                    context_keys=list(context.keys()),
                    note="Floor received a data-query category with no user data",
                )

        return context

    async def _gather_identity_context(
        self, user_id: str = None, session_id: str = None
    ) -> Dict[str, Any]:
        """
        Gather Piper's capabilities and plugin status for identity-adjacent questions.

        #1428: Capabilities derive from the CHAT_POINTERS product-surface
        ledger (services/intent_service/chat_pointers.py) — the same source
        the #1433 reachability ratchet gates. Every POINTER row is a VERIFIED
        chat-reachable capability with a user-register example utterance; a
        new capability joins this answer by getting a ledger row. This
        replaces the #923 rail-descriptions-only build, which systematically
        understated capabilities (canonical/elif/floor/web-flow capabilities
        were invisible) and leaked internal markers like "(#1124)" into the
        floor prompt (census 2026-07-16, F8). CHAT_INVISIBLE surfaces are
        never claimed.

        #950 iteration (Apr 16): Adds user-anchoring data so Identity responses
        can reference specifics about *this user* rather than sounding generic.
        The canonical retest on Apr 16 showed Identity queries scored Context=1
        consistently — "generic response that could apply to any user" —
        because the gatherer only provided global capability + integration info.
        User-anchoring: projects, recent conversation topics. Fail-graceful.

        973: DYNAMIC (uncached). Capabilities are a pure in-process ledger
        read (nothing to cache); integration status should reflect a just-
        configured connector immediately; the rest is in-memory session state.
        """
        context: Dict[str, Any] = {}

        # #1428: ledger-derived, user-register capability lines (pure function,
        # no registry/plugin dependency — deterministic and marker-free).
        # #1632: decorated with the outward marker per line (bridges the
        # #1428 ledger answer to the #1509/#1462 outwardness axis without
        # forking the #1428 construction — see
        # capability_legibility.capability_answer_lines_with_outwardness).
        from services.intent_service.capability_legibility import (
            capability_answer_lines_with_outwardness,
        )

        context["capabilities"] = capability_answer_lines_with_outwardness()

        # Integrations from the canonical status service (#1547, audit F2).
        # Previously registry-fed: every real plugin hardcodes configured=False
        # (#784), so the floor computed all integrations "inactive" and the
        # renderer omitted the line entirely — PM's "no visibility" finding.
        # The canonical service is user-scoped and binding-first; Demo is
        # structurally excluded from its known set.
        try:
            from services.integrations.integration_status_service import (
                IntegrationStatusService,
                needs_reconnecting,
            )

            # #2072 follow-up (Arch's ruling): "active" is a claim that the connection
            # works, so a binding GitHub has rejected reads "needs_reconnecting" (#2029's
            # "Needs reconnecting"), never "active". The floor renders the three apart.
            def _identity_status(status: Dict[str, Any]) -> str:
                if status.get("check_failed"):
                    return "check_failed"  # #2151 ISS-STATUS: neither active nor absent
                if needs_reconnecting(status):
                    return "needs_reconnecting"
                return "active" if status.get("configured") else "inactive"

            statuses = await IntegrationStatusService().get_all(user_id)
            context["integrations"] = [
                {"name": name, "status": _identity_status(status)}
                for name, status in statuses.items()
            ]
            # #2151 ISS-STATUS: one integration's check failing arms the registered
            # flag, so the floor's aggregate says it couldn't check (#1717 registry).
            if any(st.get("check_failed") for st in statuses.values()):
                context["integrations_source_failed"] = True
        except Exception as e:
            logger.warning("context_assembler_identity_capabilities_error", error=str(e))
            # #2151: the floor must say it couldn't check, not infer "none connected".
            context["integrations_source_failed"] = True

        # #950 iteration: user-anchoring data so Identity responses can reference
        # *this user* rather than sounding generic. Failure anywhere here is silent
        # — we'd rather ship capability/integration info without user-anchoring than
        # throw. The fabrication guard in the floor prompt handles missing data.
        if user_id:
            try:
                from services.user_context_service import user_context_service

                user_ctx = await user_context_service.get_user_context(
                    session_id=session_id, user_id=user_id
                )
                if user_ctx:
                    if getattr(user_ctx, "projects", None):
                        context["user_projects"] = [
                            p if isinstance(p, str) else str(p) for p in user_ctx.projects[:5]
                        ]
                        # #1776 (m-44, the #1530/#1544 companion-count shape):
                        # the slice above is a GATHER cap — it truncates before
                        # any render exists — so without this the floor's
                        # denominator silently BECOMES 5 and a user with 8
                        # PIPER.md projects has a floor that believes they have
                        # 5, with nothing in the prompt to indicate otherwise.
                        # The source is an in-memory list, so the true count is
                        # free. Cap kept (context budget); denominator honest.
                        context["user_project_count"] = len(user_ctx.projects)
                    if getattr(user_ctx, "organization", None):
                        context["organization"] = user_ctx.organization
            except Exception as e:
                logger.warning("context_assembler_identity_user_context_error", error=str(e))

        if session_id:
            try:
                from services.intent_service.conversation_context import get_or_create_context

                conv_ctx = get_or_create_context(session_id, user_id=user_id)
                if conv_ctx and getattr(conv_ctx, "turns", None):
                    recent = [
                        t.message[:80] for t in conv_ctx.turns[-4:] if getattr(t, "message", None)
                    ]
                    if recent:
                        context["recent_topics"] = recent
                    context["session_turn_count"] = len(conv_ctx.turns)
            except Exception as e:
                logger.warning("context_assembler_identity_conv_context_error", error=str(e))

        return context

    async def _gather_discovery_context(self, user_id: str = None) -> Dict[str, Any]:
        """
        Gather available capabilities list for DISCOVERY intents.

        Same data as identity context — capabilities and integrations.
        973: DYNAMIC (uncached) — delegates to _gather_identity_context.
        """
        return await self._gather_identity_context(user_id)

    async def _gather_trust_context(self, user_id: str = None) -> Dict[str, Any]:
        """
        Gather trust profile data for TRUST intents.

        #984: Cached via ContextCache (TTL 1h, key `context:trust:{user_id}`).
        Eager invalidation on trust-stage transitions (Q3=c) keeps the
        floor immediately aware of stage changes; TTL is the bounded-stale
        safety net for cases where eager invalidation is missed.
        """
        if not user_id:
            return {
                "trust_profile": {
                    "stage": "unknown",
                    "note": "No user ID available — trust profile not loaded",
                }
            }
        return await self.cache.get_or_compute(
            key=f"context:trust:{user_id}",
            ttl_seconds=_TTL_TRUST,
            compute_fn=lambda: self._compute_trust_context(user_id),
        )

    async def _compute_trust_context(self, user_id: str) -> Dict[str, Any]:
        """Compute trust context (uncached) for cache miss."""
        context: Dict[str, Any] = {}

        try:
            from uuid import UUID

            from services.database.session_factory import AsyncSessionFactory
            from services.repositories.user_trust_profile_repository import (
                UserTrustProfileRepository,
            )

            async with AsyncSessionFactory.session_scope() as session:
                trust_repo = UserTrustProfileRepository(session)
                profile = await trust_repo.get_by_user_id(UUID(user_id))

                if profile:
                    context["trust_profile"] = {
                        "stage": profile.trust_stage.value if profile.trust_stage else "new",
                        "interaction_count": getattr(profile, "interaction_count", 0),
                    }
                else:
                    context["trust_profile"] = {
                        "stage": "new",
                        "interaction_count": 0,
                    }
        except Exception as e:
            logger.warning("context_assembler_trust_error", error=str(e))
            context["trust_profile"] = {
                "stage": "unknown",
                "note": "Could not load trust profile",
            }
            # #2151 (Arch 10-23): one mechanism; the registered flag arms the
            # floor's aggregate rather than leaving the LLM to infer it from prose.
            context["trust_source_failed"] = True

        return context

    async def _gather_memory_context(
        self, user_id: str = None, session_id: str = None
    ) -> Dict[str, Any]:
        """
        Gather conversation history summary for MEMORY intents.

        Reads from in-memory conversation context and UserHistoryService.
        973: DYNAMIC (uncached) — per-session conversational state; caching
        would serve one turn's history to a later turn.
        """
        context: Dict[str, Any] = {}

        # Conversation context (in-memory turns)
        if session_id:
            try:
                from services.intent_service.conversation_context import get_or_create_context

                conv_ctx = get_or_create_context(session_id, user_id=user_id)
                recent_topics = []
                for turn in conv_ctx.turns[-6:]:
                    if turn.message:
                        # Extract a short summary (first 80 chars)
                        summary = turn.message[:80]
                        if len(turn.message) > 80:
                            summary += "..."
                        recent_topics.append(summary)

                context["conversation_history_summary"] = {
                    "recent_topics": recent_topics,
                    "turn_count": len(conv_ctx.turns),
                }
            except Exception as e:
                # #2151 FLOOR-ABSENT: an unread history is not "we haven't talked".
                logger.warning("context_assembler_memory_history_error", error=str(e))
                context["memory_source_failed"] = True

        # User history service (persistent memory)
        # Issue #1021: switched from ephemeral InMemoryUserHistoryRepository
        # (per-call repo, never populated) to DBUserHistoryRepository, which
        # reads from the conversations table. The UserHistoryService now
        # exposes get_history_summary() for adaptive-greeting injection.
        if user_id:
            try:
                from services.database.repositories import DBUserHistoryRepository
                from services.database.session_factory import AsyncSessionFactory
                from services.memory.user_history import UserHistoryService

                async with AsyncSessionFactory.session_scope() as session:
                    history_repo = DBUserHistoryRepository(session)
                    history_service = UserHistoryService(history_repo)
                    summary = await history_service.get_history_summary(user_id=user_id)

                if summary:
                    context["persistent_memory"] = {
                        "has_history": True,
                        "summary": summary,
                    }
            except Exception as e:
                # #2151 FLOOR-ABSENT: a failed history read is not "no prior conversations".
                logger.warning("context_assembler_memory_persistent_error", error=str(e))
                context["memory_source_failed"] = True

        return context

    async def _gather_insight_pull_context(self, user_id: str = None) -> Dict[str, Any]:
        """
        Issue #1030 INSIGHT-PULL: Gather composted insights from InsightRepository
        for pull-mode chat responses ("What have you learned about X?").

        Sections insights by confidence band per PM R5 (2026-05-31):
        - high:   confidence ≥ 0.75
        - medium: 0.50 ≤ confidence < 0.75
        - low:    confidence < 0.50

        Returns dict shape consumed by _format_domain_context (#1030):
            {
                "insights": {
                    "high_confidence": [{...insight dict...}, ...],
                    "medium_confidence": [...],
                    "low_confidence": [...],
                    "total_count": int,
                    "is_empty": bool,
                }
            }

        A verified empty read writes the empty insights dict, which lets the floor
        respond with the honest "nothing learned yet" framing the AC requires. #2151:
        a failed read writes no insights dict and arms ``insights_source_failed``
        instead (it was the empty dict, so a failure read as "nothing learned").

        973: DYNAMIC (uncached). An explicit "what have you learned?" pull
        should read the repository fresh — a just-composted insight must be
        visible immediately, and the query is rare enough that caching buys
        nothing.
        """
        context: Dict[str, Any] = {}

        if not user_id:
            context["insights"] = {
                "high_confidence": [],
                "medium_confidence": [],
                "low_confidence": [],
                "total_count": 0,
                "is_empty": True,
            }
            return context

        try:
            from services.database.repositories import InsightRepository
            from services.database.session_factory import AsyncSessionFactory

            async with AsyncSessionFactory.session_scope() as session:
                repo = InsightRepository(session)
                # #1776 (m-44): `limit=50` is a GATHER cap, so the old
                # `total_count = len(insights)` was the cap wearing the word
                # "total" — and the floor renders it verbatim as "(N total,
                # sectioned by confidence)". The window count rides the same
                # query (#1645 idiom), so the denominator is row-derived at no
                # extra round trip. Cap kept: insights are class-(b) long, and
                # how to DISPLAY a long set honestly is the epic-6 question.
                insights, _skipped, insight_total = await repo.list_for_user_with_total(
                    user_id=user_id,
                    limit=50,  # cap to avoid context bloat
                    exclude_deleted=True,
                )

            high, medium, low = [], [], []
            for ins in insights:
                # Issue #1030 BUG FIX 2026-06-02: SurfaceableInsight nests its
                # content inside `learning: ExtractedLearning`, not at the top
                # level. Previous code did getattr(ins, "confidence", 0.0) which
                # silently defaulted to 0.0 for every insight, bucketing all
                # high-confidence insights as "low" — making the floor LLM
                # interpret them as effectively-no-data. Now reads:
                #   confidence from ins.learning.confidence
                #   topic_tags from ins.learning.topic_tags
                #   expression from ins.learning.{insight|pattern|correction}.expression
                learning = getattr(ins, "learning", None)
                confidence_val = (
                    float(getattr(learning, "confidence", 0.0) or 0.0) if learning else 0.0
                )
                # #1216: drop internal/seed-provenance tags before they reach the
                # floor prompt. Surfacing them (e.g. "uat-anniversary-2026-05-28",
                # "dev_seed") lets the LLM announce an ungroundable "these are seed
                # placeholders vs real observations" claim — the workstyle
                # confabulation. Legit TOPICAL tags (github, work-rhythm, …) still
                # surface, so the floor presents insights honestly by CONFIDENCE.
                # Real fix = a first-class provenance field (PPM lane, per the CXO
                # honest-provenance principle); this removes the leaked signal.
                _raw_tags = list(getattr(learning, "topic_tags", []) or []) if learning else []
                topic_tags_val = [
                    t
                    for t in _raw_tags
                    if (t or "").strip().lower() not in {"dev_seed", "seed_demo_object"}
                    and not (t or "").strip().lower().startswith("uat-")
                ]
                # Expression lives on whichever learning sub-object is populated
                expression_val = ""
                if learning:
                    for sub_attr in ("insight", "pattern", "correction"):
                        sub = getattr(learning, sub_attr, None)
                        if sub is not None:
                            expression_val = (
                                getattr(sub, "expression", "")
                                or getattr(sub, "description", "")
                                or ""
                            )
                            if expression_val:
                                break

                ins_dict = {
                    "id": str(getattr(ins, "id", "")),
                    "expression": expression_val,
                    "confidence": confidence_val,
                    "topic_tags": topic_tags_val,
                    "observation_count": int(getattr(ins, "surfaced_count", 0) or 0),
                    "created_at": (
                        getattr(ins, "created_at").isoformat()
                        if getattr(ins, "created_at", None)
                        else None
                    ),
                }
                # Bucket per PM R5 confidence cuts
                if ins_dict["confidence"] >= 0.75:
                    high.append(ins_dict)
                elif ins_dict["confidence"] >= 0.50:
                    medium.append(ins_dict)
                else:
                    low.append(ins_dict)

            context["insights"] = {
                "high_confidence": high,
                "medium_confidence": medium,
                "low_confidence": low,
                # #1776: the query's own pre-LIMIT row count, never the length
                # of the 50-row read slice.
                "total_count": insight_total,
                # Deliberately still keyed on the RENDERABLE rows, not the row
                # count: `is_empty` gates the floor's "NONE YET, do not
                # fabricate" branch, and switching it to the total would make a
                # hypothetical all-rows-malformed read (#1545) emit a "137
                # total, sectioned by confidence" header over zero items —
                # trading one wrong render for another. Telling
                # "has none" apart from "has some we could not deserialize"
                # needs the #1425 three-state treatment, not a one-line swap.
                "is_empty": len(insights) == 0,
            }
        except Exception as e:
            logger.warning(
                "context_assembler_insight_pull_error",
                user_id=user_id,
                error=str(e),
            )
            # #2151 FLOOR-ABSENT: a failed read is NOT the verified empty. Writing the
            # is_empty dict here made the floor say "NONE YET ... you have not yet
            # learned patterns" about a user whose insights it never read.
            context["insights_source_failed"] = True

        return context

    async def _gather_temporal_context(
        self, user_id: str = None, session_id: str = None
    ) -> Dict[str, Any]:
        """
        #965: Gather temporal context for non-date queries routed to the floor.

        Provides data that the LLM needs to answer questions like:
        - "What did we accomplish yesterday?" → completed todos, project activity
        - "What's on the agenda for today?" → calendar events, pending todos
        - "When was the last time we worked on this?" → project activity dates
        - "How long have we been working on this?" → project creation dates

        All sources are fail-graceful: missing data is expressed as absence,
        never as an exception. The floor LLM composes honestly around gaps.
        """
        context: Dict[str, Any] = {}

        # Current date with day of week (useful for all temporal questions)
        now = datetime.now()
        context["current_date"] = now.strftime("%A, %B %d, %Y")
        context["current_day_of_week"] = now.strftime("%A")

        # #951: Calendar context (next meeting, free blocks)
        cal_ctx = await self._gather_calendar_context(user_id)
        context.update(cal_ctx)

        # #2112 (CXO's words, Arch's ruling): a TEMPORAL floor turn ("check my
        # calendar for conflicts") must know whether the calendar is connected,
        # or the model writes its own guess and never offers the connection
        # (Web, 86ee0bbfa1, 15:10). The summary above is {} both when the
        # calendar is empty and when it is absent; this is the explicit fact.
        cal_conn = await self._gather_calendar_connection(user_id)
        if cal_conn:
            context["calendar_connection"] = cal_conn

        # #984: Cached todos (per-method per-user). Eager-invalidated on
        # todo CRUD (Q3=c) via TodoManagementService mutation hooks.
        if user_id:
            pending_data = await self._get_pending_todos_cached(user_id, limit=10)
            if pending_data:
                context.update(pending_data)

            completed_data = await self._get_completed_todos_cached(user_id, limit=10)
            if completed_data:
                context.update(completed_data)

        # #984: Cached projects (TTL-only, 5min — slow-changing).
        if user_id:
            projects_data = await self._get_projects_cached(user_id, limit=5)
            if projects_data:
                context.update(projects_data)

        # #985: Active milestones (due_on is temporal-relevant). Cached.
        if user_id:
            milestones_data = await self._gather_active_milestones_context(user_id)
            if milestones_data:
                context.update(milestones_data)

        # #986: Recent GitHub activity (TEMPORAL queries — "what happened
        # this week?"). Cached (5min TTL).
        if user_id:
            activity_data = await self._gather_recent_activity_context(user_id)
            if activity_data:
                context.update(activity_data)

        # Conversation history summary (for "what did we discuss" context)
        if session_id:
            try:
                from services.intent_service.conversation_context import get_or_create_context

                conv_ctx = get_or_create_context(session_id, user_id=user_id)
                if conv_ctx.turns:
                    context["conversation_history_summary"] = {
                        "turn_count": len(conv_ctx.turns),
                        "recent_topics": [t.message[:80] for t in conv_ctx.turns[-4:] if t.message],
                    }
            except Exception as e:
                logger.warning("context_assembler_temporal_history_error", error=str(e))

        return context

    async def _gather_status_priority_context(self, user_id: str = None) -> Dict[str, Any]:
        """
        #925: Gather project status and priority context for floor routing.

        Provides data for queries like:
        - "What am I working on?" → project list with GitHub metadata
        - "What's my top priority?" → priorities with high-priority issues
        - "Show me project landscape" → project overview
        - "Which project should I focus on?" → priority-ranked projects

        Same data sources as the canonical STATUS/PRIORITY handlers, but
        assembled as structured context for the floor LLM to compose from.
        """
        context: Dict[str, Any] = {}

        # #951: Calendar context (next meeting, free blocks) — relevant for
        # "what should I work on next?" style queries that need time awareness
        cal_ctx = await self._gather_calendar_context(user_id)
        context.update(cal_ctx)

        # #984: Cached user context (TTL-only, 5min — slow-changing).
        if user_id:
            try:
                user_ctx_data = await self._get_user_context_cached(user_id)
            except _UserContextReadFailed as failed:
                # #2151 FLOOR-ABSENT: a failed projects or preferences read is stated
                # ("couldn't check projects"), never a user with none; the parts that
                # were read still render.
                user_ctx_data = failed.partial
                for flag in failed.flags:
                    context[flag] = True
            if user_ctx_data:
                context.update(user_ctx_data)

        # #984: Cached pending todos. Eager-invalidated on todo CRUD (Q3=c).
        # Note: cap at 5 here vs. 10 in temporal — but the cache stores the
        # full list (up to 10) and we slice on read for consistency.
        if user_id:
            pending_data = await self._get_pending_todos_cached(user_id, limit=5)
            if pending_data and "pending_todos" in pending_data:
                context["pending_todos"] = pending_data["pending_todos"]
                # #1544: carry the row-derived count (m-44) — and an empty list
                # here is VERIFIED-empty (the read ran), which the floor renders
                # as an account-level "no pending todos" fact, never a
                # conversation-scoped absence hedge.
                context["pending_todo_count"] = pending_data.get(
                    "pending_todo_count", len(pending_data["pending_todos"])
                )
            elif pending_data and pending_data.get("pending_todos_source_failed"):
                # #1573 (#1425): propagate the failure flag — never fake-empty.
                context["pending_todos_source_failed"] = True

        # #1155: GitHub connection flag (the high-priority issues themselves are
        # gathered below — this block only records whether GitHub is connected).
        # #1547 (audit F2): from the canonical service, user-scoped and
        # binding-first — the registry read was constant-false (#784), so this
        # flag could never be True for anyone.
        try:
            from services.integrations.integration_status_service import (
                IntegrationStatusService,
                needs_reconnecting,
            )

            gh_status = await IntegrationStatusService().get_status(user_id, "github")
            context["github_connected"] = bool(gh_status.get("configured"))
            # #2072 follow-up (Arch's ruling): ``github_connected`` stays ``configured``
            # (a connection exists), and this flag says whether it works, so the floor
            # never renders a grant GitHub has rejected as plain "connected".
            context["github_needs_reconnecting"] = needs_reconnecting(gh_status)
            # #2151 ISS-STATUS: a check that couldn't run is not "not connected". The
            # registered flag arms the floor's aggregate, and ``github_connected`` is
            # left out so the floor renders no GitHub connection line either way.
            if gh_status.get("check_failed"):
                context.pop("github_connected", None)
                context["integrations_source_failed"] = True
        except Exception as e:
            logger.warning("context_assembler_status_github_error", error=str(e))
            context["github_needs_reconnecting"] = False
            context["integrations_source_failed"] = True

        # #983: Blocked items (open issues labeled `status: blocked`). Surfaced
        # for STATUS / PRIORITY / UNKNOWN-fallback. Cached (5min TTL).
        if user_id:
            blocked_data = await self._gather_blocked_items_context(user_id)
            if blocked_data:
                context.update(blocked_data)

        # #985: Active milestones (sprint tracking). Surfaced for STATUS /
        # PRIORITY / UNKNOWN-fallback. Cached (5min TTL).
        if user_id:
            milestones_data = await self._gather_active_milestones_context(user_id)
            if milestones_data:
                context.update(milestones_data)

        # #986: Recent GitHub activity (issues+PRs touched in last 7 days).
        # Cached (5min TTL).
        if user_id:
            activity_data = await self._gather_recent_activity_context(user_id)
            if activity_data:
                context.update(activity_data)

        # #1155: High-priority open issues — the actual "what should I focus on"
        # candidates. Previously this context set only `github_connected` (the
        # issues were never pulled), so the PRIORITY floor saw "connected" but had
        # nothing to reason over and floored as if it had no project data.
        if user_id:
            hp_data = await self._gather_high_priority_issues_context(user_id)
            if hp_data:
                context.update(hp_data)

        return context

    async def _gather_calendar_context(self, user_id: str = None) -> Dict[str, Any]:
        """
        #951: Gather calendar context for TEMPORAL and STATUS queries.

        #984: Cached via ContextCache (TTL 60s, key `context:calendar:{user_id}`).
        Cache invalidation is TTL-only (Q3=c hybrid): calendar data is
        external (Google/MS Graph) so we can't be notified of changes
        anyway. Bounded staleness ≤ 60s is acceptable.
        """
        if not user_id:
            return {}
        try:
            return await self.cache.get_or_compute(
                key=f"context:calendar:{user_id}",
                ttl_seconds=_TTL_CALENDAR,
                compute_fn=lambda: self._compute_calendar_context(user_id),
            )
        except Exception as e:
            # #2151 FLOOR-ABSENT: a failed calendar read is not a free day.
            # get_or_compute caches no failure (the exception propagates past it).
            logger.warning("context_assembler_calendar_error", error=str(e))
            return {"calendar_source_failed": True}

    async def _gather_calendar_connection(self, user_id: Optional[str]) -> Dict[str, Any]:
        """#2112: the calendar's connection state with CXO's sentence for it.

        ``{"status": "active" | "needs_reconnecting" | "not_connected", "line": str}``
        from the one status service every surface reads (#2072: ``configured``
        means a connection exists; a rejected grant renders as needs
        reconnecting, never as connected). No principal, or a status-service
        failure, returns {} — the floor then says nothing about the calendar
        rather than guessing.
        """
        if not user_id:
            return {}
        try:
            from services.integrations.integration_status_service import (
                IntegrationStatusService,
                needs_reconnecting,
            )
            from services.intent_service.capability_legibility import (
                chat_reads_line,
                not_connected_line,
            )

            status = await IntegrationStatusService().get_status(user_id, "calendar")
        except (
            Exception
        ) as e:  # silent-ok: logged; the floor gets no calendar fact rather than a wrong one
            logger.warning("context_assembler_calendar_connection_error", error=str(e))
            return {}
        # Arch (16:08): the floor's #2100 rule ("never promise a read an integration
        # does not list") points the model at the "what chat reads" line, which a
        # TEMPORAL turn never carried, so on ee952c73eb the model added "Once it's
        # connected, checking for conflicts is something I can do". The reads line
        # (CXO's words, already landed) rides every non-active state as `reads`.
        reads = chat_reads_line("calendar")
        if needs_reconnecting(status):
            # CXO's words (15:32): what happened and the one action, no guess why.
            return {
                "status": "needs_reconnecting",
                "line": (
                    "I can't read your calendar: Google no longer accepts the connection. "
                    "Reconnect it in Settings → Integrations → Google Calendar."
                ),
                "reads": reads,
            }
        # Arch's check (15:30): the status service counts the calendar configured
        # when GOOGLE_CALENDAR_CREDENTIALS or MCP_ENABLED is set (via "env"), a
        # deployment-wide legacy fallback, not this person's connection. The
        # floor's "I can read your calendar…" is a claim about THEIR calendar,
        # so only a per-user connection (via "keychain" / an OAuth binding) earns it.
        if status.get("configured") and status.get("via") != "env":
            return {"status": "active", "line": chat_reads_line("calendar")}
        return {
            "status": "not_connected",
            "line": not_connected_line("calendar") or "",
            "reads": reads,
        }

    async def _compute_calendar_context(self, user_id: str) -> Dict[str, Any]:
        """
        #951: Compute calendar context (uncached) for cache miss.

        Calls CalendarIntegrationRouter.get_temporal_summary() and maps
        the response to the schema `_format_domain_context` in
        conversational_floor.py already expects:

        {
          "calendar": {
            "next_meeting": {"title": str, "start": str},
            "next_free_block": {"start": str, "duration_minutes": int},
            "time_available_minutes": int,
          }
        }

        Never connected (``calendar_connected`` False with ``last_read_error ==
        "no_credential"``) or no calendar integration returns {} (not performed). #2151: a read that did not happen RAISES (the
        gather arms ``calendar_source_failed``): the router raising, an error summary
        (``success`` False), or a connected summary whose events read was never
        established (#1425).
        """
        # Lazy-import to avoid startup cost and break potential import cycles
        from services.integrations.calendar.calendar_integration_router import (
            CalendarIntegrationRouter,
        )

        router = CalendarIntegrationRouter(user_id=user_id)
        try:
            summary = await router.get_temporal_summary(user_id=user_id)
        except Exception as e:
            if _calendar_feature_off(e):
                return {}
            raise

        if not summary:
            raise _CalendarReadFailed("empty temporal summary")
        if summary.get("calendar_connected") is False:
            # #2151 (Arch 10-24 07:55): False is also a connected account whose sign-in
            # failed (a refresh that would not go through, a keychain error); only "no
            # stored credential" is not performed.
            read_error = router.last_read_error
            if read_error == "no_credential":
                return {}
            raise _CalendarReadFailed(read_error or "calendar sign-in failed")
        if not summary.get("success", False):
            raise _CalendarReadFailed(summary.get("error_type") or "calendar read failed")
        if not summary.get("events_read_established", False):
            raise _CalendarReadFailed("events read not established")

        calendar: Dict[str, Any] = {}

        next_meeting = summary.get("next_meeting")
        if next_meeting:
            calendar["next_meeting"] = {
                "title": next_meeting.get("title", "Untitled"),
                "start": next_meeting.get("start", "unknown"),
            }

        free_blocks = summary.get("free_blocks") or []
        if free_blocks:
            first_block = free_blocks[0]
            calendar["next_free_block"] = {
                "start": first_block.get("start", "unknown"),
                "duration_minutes": first_block.get("duration_minutes", 0),
            }

        time_available = summary.get("time_available_minutes")
        if time_available is not None:
            calendar["time_available_minutes"] = time_available

        if not calendar:
            return {}

        return {"calendar": calendar}

    async def _gather_reminder_context(self, user_id: str = None) -> Dict[str, Any]:
        """
        Issue #903: Check for due reminders to surface at greeting time.

        #984: Cached via ContextCache (TTL 30s, key `context:reminders:{user_id}`).
        Eager invalidation on todo CRUD (Q3=c) — reminders share a TTL
        family with pending_todos because they're both todo-derived.
        """
        if not user_id:
            return {}
        return await self.cache.get_or_compute(
            key=f"context:reminders:{user_id}",
            ttl_seconds=_TTL_REMINDERS,
            compute_fn=lambda: self._compute_reminder_context(user_id),
        )

    async def _due_reminder_ages(self, handlers, user_id: str) -> Dict[str, str]:
        """#1997: how old each due reminder is, on the user's calendar, keyed
        by its text — ``"due earlier today"`` or ``"N day(s) overdue"``. The
        reminder block used to carry text only, so the floor guessed ("three
        reminders have come due today" for items 3–5 days old). Additive:
        any failure returns ``{}`` and the block renders as before. The
        day-count rule is #1996's (calendar days at local midnight, never
        elapsed 24-hour periods)."""
        try:
            from uuid import UUID
            from zoneinfo import ZoneInfo

            from services.utils.datetime_utils import user_timezone_name

            rows = await handlers._due_reminder_todos(UUID(user_id))
            if not rows:
                return {}
            now = datetime.now(timezone.utc)
            try:
                local_now = now.astimezone(ZoneInfo(await user_timezone_name(user_id)))
            except Exception:  # silent-ok: unknown zone → UTC calendar; ages stay additive
                local_now = now
            ages: Dict[str, str] = {}
            for row in rows:
                when = getattr(row, "reminder_date", None)
                text = getattr(row, "text", None)
                if not when or not text:
                    continue
                if when.tzinfo is None:
                    when = when.replace(tzinfo=timezone.utc)
                days = (local_now.date() - when.astimezone(local_now.tzinfo).date()).days
                if days <= 0:
                    ages[str(text)] = "due earlier today"
                else:
                    ages[str(text)] = f"{days} day{'s' if days != 1 else ''} overdue"
            return ages
        except Exception as e:  # silent-ok: ages are an additive annotation; the reminder block itself is unaffected
            logger.warning("context_assembler_reminder_ages_error", error=str(e))
            return {}

    async def _gate_due_reminder_mentions(
        self,
        reminder_ctx: Dict[str, Any],
        user_id: Optional[str],
        session_id: Optional[str],
    ) -> Dict[str, Any]:
        """#1625: gate the CONVERSATIONAL mention of due reminders.

        PM's ruling (v53, 2026-08-15 — "reminders are a bit relentless"):
        mention due reminders once per conversation, then stay quiet; the
        Radar pin (ReminderEntitySource) owns persistence. Two gates, in
        order:

        1. **Active guided flow** (the standup interview mid-question shape
           from PM's transcript): drop the due-reminder keys entirely and do
           NOT mark them mentioned — the user hasn't been told, so the first
           floor turn after the flow ends mentions them. `source_failed`
           passes through untouched (#1425 honesty is not a nag block; it
           only speaks if reminders come up).
        2. **Mentioned-set filter**: only reminders this session hasn't been
           told about are included, and those are marked mentioned. The set
           keys on reminder identity, so a NEW reminder coming due
           mid-session is still surfaced once ("once" must not become
           "never").

        No session_id → no per-session gating possible; #1566 behavior is
        preserved unchanged (same opt-out shape as the floor's push-gating).
        Always returns a NEW dict — the input may be the #984 cache's shared
        reference and must not be mutated.
        """
        gated = dict(reminder_ctx)
        rems = gated.get("due_reminders") or []

        # Gate 1: never inside an active gathering/interview exchange.
        try:
            from services.process import get_process_registry

            if await get_process_registry().any_active(user_id, session_id):
                gated.pop("due_reminders", None)
                gated.pop("reminder_count", None)
                return gated
        except Exception as e:  # silent-ok: probe failure fails OPEN (reminders surface; the mention gate is a quieting layer, never a reason to break the #1566 surfacing promise)
            logger.warning("reminder_mention_gate_probe_error", error=str(e))

        # Gate 2: only not-yet-mentioned reminders, marked as they go out.
        fresh = _unmentioned_reminders(session_id, rems)
        if not fresh:
            gated.pop("due_reminders", None)
            gated.pop("reminder_count", None)
            return gated
        _mark_reminders_mentioned(session_id, fresh)
        gated["due_reminders"] = fresh
        gated["reminder_count"] = len(fresh)
        return gated

    async def _compute_reminder_context(self, user_id: str) -> Dict[str, Any]:
        """Compute reminder context (uncached) for cache miss."""
        try:
            from uuid import UUID

            from services.intent_service.todo_handlers import TodoIntentHandlers

            handlers = TodoIntentHandlers()
            due_reminders = await handlers.get_due_reminders(UUID(user_id))

            if due_reminders is None:
                # #1425: the handler's lookup failed — a promised reminder may
                # exist. Flag it instead of presenting "nothing due" (this pair
                # was the double-swallow: handler [] + this {} = promise
                # silently broken).
                return {"source_failed": True}
            if due_reminders:
                reminder_ctx: Dict[str, Any] = {
                    "due_reminders": due_reminders,
                    "reminder_count": len(due_reminders),
                }
                ages = await self._due_reminder_ages(handlers, user_id)
                if ages:
                    reminder_ctx["due_reminder_ages"] = ages
                return reminder_ctx
        except (
            Exception
        ) as e:  # silent-ok: failure surfaces via source_failed flag, not an empty context (#1425)
            logger.warning("context_assembler_reminder_error (source failed)", error=str(e))
            return {"source_failed": True}

        return {}

    # ------------------------------------------------------------------
    # #984: Source-level cached helpers
    #
    # These helpers cache the OUTPUT of expensive data sources (DB / external
    # API calls) at fine granularity, so callers in multiple gather methods
    # share a single cache entry per (data-source, user_id).
    #
    # Caching pattern: each cached helper returns the same shape as the
    # equivalent uncached compute method. compute methods are responsible
    # for the actual data fetch + serialization. Callers slice/limit on
    # read (cache stores the superset).
    # ------------------------------------------------------------------

    async def _get_pending_todos_cached(
        self, user_id: str, limit: int = 10
    ) -> Optional[Dict[str, Any]]:
        """Cached pending-todos dict for user, sliced to `limit` on read.

        Key: `context:pending_todos:{user_id}`. TTL 30s. Eager-invalidated
        by TodoManagementService mutations (Phase 3).
        """
        cached = await self.cache.get_or_compute(
            key=f"context:pending_todos:{user_id}",
            ttl_seconds=_TTL_PENDING_TODOS,
            compute_fn=lambda: self._compute_pending_todos(user_id),
        )
        if not cached:
            return None
        if cached.get("source_failed"):
            # #1573 (#1425 honesty): the todos lookup FAILED — todos may
            # exist. Translate to a todo-specific key (the generic
            # "source_failed" renders as a REMINDER-check failure on the
            # floor) so the floor says "couldn't check todos", never
            # fake-empty.
            return {"pending_todos_source_failed": True}
        if "pending_todos" not in cached:
            return None
        return {
            "pending_todos": cached["pending_todos"][:limit],
            "pending_todo_count": cached.get("pending_todo_count", len(cached["pending_todos"])),
        }

    async def _compute_pending_todos(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Compute pending-todos (uncached) for cache miss. Stores up to 10.

        #1573 (#1425 honesty): a genuine failure returns
        ``{"source_failed": True}`` at ERROR level — never a silent None.
        The old warning+None swallow masked a naive-vs-aware TypeError
        (time audit F5) that made every due-dated user's pending todos
        vanish from floor context with no trace.
        """
        pending = None
        try:
            from uuid import UUID

            from services.todo.todo_management_service import TodoManagementService

            todo_svc = TodoManagementService()
            pending = await todo_svc.list_todos(user_id=UUID(user_id), include_completed=False)
            if not pending:
                # #1544: zero pending todos is a FACT — the owner-scoped read
                # succeeded and found no rows. Returning None here made
                # verified-empty indistinguishable from never-gathered, so the
                # floor had no basis to say "your list is empty" and improvised
                # conversation-scoped hedges instead (PM live 2026-08-09).
                return {"pending_todos": [], "pending_todo_count": 0}
            return {
                "pending_todos": [_todo_to_dict(t) for t in pending[:10]],
                "pending_todo_count": len(pending),
            }
        except Exception as e:
            logger.error(
                "context_assembler_pending_todos_error",
                error=str(e),
                user_id=user_id,
                fetched_count=len(pending) if pending is not None else None,
                exc_info=True,
            )
            return {"source_failed": True}

    async def _get_completed_todos_cached(
        self, user_id: str, limit: int = 10
    ) -> Optional[Dict[str, Any]]:
        """Cached completed-todos dict for user, sliced to `limit` on read.

        Key: `context:completed_todos:{user_id}`. TTL 5min. Eager-invalidated
        by TodoManagementService mutations (Phase 3).
        """
        cached = await self.cache.get_or_compute(
            key=f"context:completed_todos:{user_id}",
            ttl_seconds=_TTL_COMPLETED_TODOS,
            compute_fn=lambda: self._compute_completed_todos(user_id),
        )
        if not cached:
            return None
        if cached.get("source_failed"):
            # #1645 (#1573 shape): the completed-todos lookup FAILED — the
            # user may have completed things. Translate to a lane-specific
            # key so the floor says "couldn't check", never fake-empty and
            # never a silent absence.
            return {"completed_todos_source_failed": True}
        if "completed_todos" not in cached:
            return None
        return {
            "completed_todos": cached["completed_todos"][:limit],
            "completed_todo_count": cached.get(
                "completed_todo_count", len(cached["completed_todos"])
            ),
        }

    async def _compute_completed_todos(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Compute completed-todos (uncached) for cache miss. Stores up to 10.

        #1645 (#1573 shape): a genuine failure returns
        ``{"source_failed": True}`` at ERROR level — never a silent None,
        which was indistinguishable from never-gathered at the floor.
        """
        try:
            from uuid import UUID

            from services.todo.todo_management_service import TodoManagementService

            todo_svc = TodoManagementService()
            all_todos = await todo_svc.list_todos(user_id=UUID(user_id), include_completed=True)
            completed = [t for t in all_todos if getattr(t, "completed", False)]
            if not completed:
                # #1639 (fix shape proven by #1544): zero completed todos is a
                # FACT — the owner-scoped read succeeded and found no completed
                # rows. Returning None here made verified-empty structurally
                # indistinguishable from never-gathered, so the floor could
                # never state "nothing completed" as an account-level fact.
                return {"completed_todos": [], "completed_todo_count": 0}
            return {
                "completed_todos": [
                    {"text": t.text, "completed_at": str(getattr(t, "completed_at", ""))}
                    for t in completed[:10]
                ],
                "completed_todo_count": len(completed),
            }
        except Exception as e:
            logger.error(
                "context_assembler_completed_todos_error",
                error=str(e),
                user_id=user_id,
                exc_info=True,
            )
            return {"source_failed": True}

    async def _get_projects_cached(self, user_id: str, limit: int = 5) -> Optional[Dict[str, Any]]:
        """Cached projects list (from `projects` table). TTL 5min.

        Key: `context:projects:{user_id}`. TTL-only invalidation (Q3=c).
        """
        cached = await self.cache.get_or_compute(
            key=f"context:projects:{user_id}",
            ttl_seconds=_TTL_PROJECTS,
            compute_fn=lambda: self._compute_projects(user_id),
        )
        if not cached:
            return None
        if cached.get("source_failed"):
            # #1645 (#1573 shape): the projects lookup FAILED — projects may
            # exist. Translate to a lane-specific key (the generic
            # "source_failed" renders as a REMINDER-check failure on the
            # floor) so the floor says "couldn't check projects", never
            # fake-empty and never a silent absence.
            return {"projects_source_failed": True}
        if "projects" not in cached:
            return None
        result: Dict[str, Any] = {"projects": cached["projects"][:limit]}
        # #1639/#1645: pass the row-derived count through — the verified-empty
        # zero, or the windowed COUNT riding the populated read (#1645). A
        # stale cache entry predating #1645 may lack the populated count;
        # never invent one from the truncated display slice (m-44).
        if "project_count" in cached:
            result["project_count"] = cached["project_count"]
        return result

    async def _compute_projects(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Compute project list (uncached) for cache miss. Stores up to 5.

        #1645 (m-44, #1530 shape): the populated read carries a REAL total —
        ``COUNT(*) OVER ()`` riding the same gather — because the display
        slice is LIMIT-capped and a denominator derived from slice length
        would present 5 as the total for a >5-project user.

        #1645 (#1573 shape): a genuine failure returns
        ``{"source_failed": True}`` at ERROR level — never a silent None,
        which was indistinguishable from never-gathered at the floor.
        """
        try:
            from services.database.session_factory import AsyncSessionFactory

            async with AsyncSessionFactory.session_scope() as session:
                from sqlalchemy import text

                result = await session.execute(
                    text(
                        "SELECT name, created_at, updated_at, COUNT(*) OVER () AS total "
                        "FROM projects "
                        "WHERE owner_id = :uid ORDER BY updated_at DESC LIMIT 5"
                    ),
                    {"uid": user_id},
                )
                rows = result.fetchall()
                if not rows:
                    # #1639 (fix shape proven by #1544): zero projects is a
                    # FACT — the owner-scoped read succeeded and found no
                    # rows, so the zero is exact (no LIMIT truncation at 0).
                    # Returning None here made verified-empty structurally
                    # indistinguishable from never-gathered, letting the floor
                    # reproduce the conversation-scoped hedge on the projects
                    # lane of #1570's transcript.
                    return {"projects": [], "project_count": 0}
                return {
                    "projects": [
                        {
                            "name": r[0],
                            "created_at": str(r[1]) if r[1] else None,
                            "last_updated": str(r[2]) if r[2] else None,
                        }
                        for r in rows
                    ],
                    # #1645 (m-44): the window COUNT is this owner's full row
                    # count — exact even though the display is LIMIT-5. The
                    # LIMIT applies after the window, so every returned row
                    # carries the same pre-LIMIT total.
                    "project_count": int(rows[0][3]),
                }
        except Exception as e:
            logger.error(
                "context_assembler_projects_error",
                error=str(e),
                user_id=user_id,
                exc_info=True,
            )
            return {"source_failed": True}

    async def _get_user_context_cached(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Cached user_context_service output. TTL 5min.

        Key: `context:user_context:{user_id}`. TTL-only invalidation (Q3=c).
        Returns dict containing projects / priorities / organization
        depending on what user_context exposes.
        """
        return await self.cache.get_or_compute(
            key=f"context:user_context:{user_id}",
            ttl_seconds=_TTL_USER_CONTEXT,
            compute_fn=lambda: self._compute_user_context(user_id),
        )

    async def _compute_user_context(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Compute user_context_service output (uncached) for cache miss.

        #2151 FLOOR-ABSENT: a failed read RAISES ``_UserContextReadFailed`` (so nothing
        is cached) carrying the parts that were read; a projects or preferences read the
        service marks failed is left out, never served as the PIPER.md fallback."""
        failed_flags: List[str] = []
        try:
            from services.user_context_service import user_context_service

            user_ctx = await user_context_service.get_user_context(session_id=None, user_id=user_id)
            if not user_ctx:
                return None
            result: Dict[str, Any] = {}
            # ``is True``: only the service's own bool arms a flag.
            projects_failed = getattr(user_ctx, "projects_read_failed", False) is True
            preferences_failed = getattr(user_ctx, "preferences_read_failed", False) is True
            if projects_failed:
                failed_flags.append("projects_source_failed")
            if preferences_failed:
                failed_flags.append("priorities_source_failed")
            if not projects_failed and hasattr(user_ctx, "projects") and user_ctx.projects:
                result["projects"] = [
                    {"name": p} if isinstance(p, str) else p for p in user_ctx.projects[:10]
                ]
                # #1530 (m-44): the display list above is sliced to 10; the
                # stated count must be the query's row count, never the length
                # of a truncated slice. The floor renders this explicitly so
                # the LLM never derives a denominator the query didn't produce.
                result["project_count"] = len(user_ctx.projects)
            if not preferences_failed and hasattr(user_ctx, "priorities") and user_ctx.priorities:
                # #496: the floor formatter (conversational_floor._format_domain_context)
                # reads domain_context["priorities"] as a DICT (p.get("user_priorities")),
                # matching intent_service.py's other producer. Emitting a bare list here
                # meant configured PIPER.md priorities never rendered (and would AttributeError
                # if non-empty). Wrap in the dict shape so the floor surfaces them.
                # #1776 (m-44): `user_priority_count` is the companion count for
                # the [:5] GATHER cap — a sibling of the list at the level the
                # list lives, mirroring `projects`/`project_count` above. The
                # floor rendered "User's stated priorities: a, b, c, d, e" as a
                # definite complete list; past five it was a subset wearing a
                # total's clothes.
                result["priorities"] = {
                    "user_priorities": user_ctx.priorities[:5],
                    "user_priority_count": len(user_ctx.priorities),
                }
            if (
                not preferences_failed
                and hasattr(user_ctx, "organization")
                and user_ctx.organization
            ):
                result["organization"] = user_ctx.organization
        except Exception as e:
            # #2151 FLOOR-ABSENT: the read failed, which is not "no projects".
            logger.warning("context_assembler_user_context_error", error=str(e))
            raise _UserContextReadFailed(
                {}, ("projects_source_failed", "priorities_source_failed")
            ) from e
        if failed_flags:
            raise _UserContextReadFailed(result, tuple(failed_flags))
        return result or None

    # ------------------------------------------------------------------
    # #983: Blocked-items gatherer
    #
    # Surfaces open GitHub issues labeled `status: blocked` for STATUS /
    # PRIORITY / UNKNOWN-fallback queries. Default repo resolved via
    # GitHubIntegrationRouter.repo_resolver. TTL 5min, no eager
    # invalidation (GitHub label changes happen out-of-band).
    # ------------------------------------------------------------------

    async def _gather_blocked_items_context(self, user_id: str = None) -> Dict[str, Any]:
        """Gather blocked-items context for STATUS / PRIORITY queries.

        Returns:
            {"blocked_items": [...], "blocked_count": N} on hit,
            {} when no user, no repo, or nothing labeled blocked.
        """
        if not user_id:
            return {}
        try:
            cached = await self._get_blocked_items_cached(user_id)
        except Exception as e:
            if _github_read_not_performed(e):
                return {}
            # #2151 FLOOR-ABSENT: a failed read is not "nothing blocked". get_or_compute
            # caches no failure (the exception propagates past it).
            logger.warning("context_assembler_blocked_items_error", error=str(e))
            return {"blocked_items_source_failed": True}
        return cached or {}

    async def _get_blocked_items_cached(
        self, user_id: str, limit: int = 10
    ) -> Optional[Dict[str, Any]]:
        """Cached blocked-items list. TTL 5min, key
        `context:blocked_items:{user_id}`."""
        cached = await self.cache.get_or_compute(
            key=f"context:blocked_items:{user_id}",
            ttl_seconds=_TTL_BLOCKED_ITEMS,
            compute_fn=lambda: self._compute_blocked_items(user_id),
        )
        if not cached or "blocked_items" not in cached:
            return None
        return {
            "blocked_items": cached["blocked_items"][:limit],
            "blocked_count": cached.get("blocked_count", len(cached["blocked_items"])),
            "blocked_count_capped": cached.get("blocked_count_capped", False),
        }

    async def _compute_blocked_items(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Compute blocked-items (uncached) for cache miss.

        Fetches up to 100 open issues from the default repo, filters those
        carrying `status: blocked`, sorts by `updated_at` desc, caps the
        cached list at 10. Returns None on an empty result; RAISES on a failed
        read (#2151: the gather arms ``blocked_items_source_failed``).
        """
        from services.integrations.github.github_integration_router import (
            GitHubIntegrationRouter,
        )

        github = GitHubIntegrationRouter()
        await github.initialize(user_id=user_id)

        # Pull a generous slice so the post-filter still finds blocked
        # items even when there are many non-blocked open issues. #2151
        # GH-NONSTRICT: strict, through the connector's one resolver, so a failed
        # read raises instead of returning [].
        all_open = await github.get_open_issues(limit=100, strict=True)
        if not all_open:
            return None

        blocked = [issue for issue in all_open if _BLOCKED_LABEL in (issue.get("labels") or [])]
        if not blocked:
            return None

        blocked.sort(key=lambda i: i.get("updated_at") or "", reverse=True)

        return {
            "blocked_items": [
                {
                    "number": i.get("number"),
                    "title": i.get("title"),
                    "labels": i.get("labels", []),
                    "url": i.get("uri") or i.get("html_url"),
                    "updated_at": i.get("updated_at"),
                }
                for i in blocked[:10]
            ],
            "blocked_count": len(blocked),
            # #1778: blocked is filtered from ONE page — a full page means
            # the count is a floor (unseen pages may hold more blocked items).
            "blocked_count_capped": len(all_open) >= 100,
        }

    # ------------------------------------------------------------------
    # #1155: High-priority open issues gatherer
    #
    # The "what should I focus on" candidates. Fetches open issues from the
    # default repo, ranks those carrying a `priority: critical|urgent|high`
    # label first, then most-recently-updated, capped at 5. Fixes the floor
    # flooring as "no project visibility" despite github_connected=true — the
    # data was connected but never consumed. Cached (5min TTL), fail-graceful.
    # ------------------------------------------------------------------

    async def _gather_high_priority_issues_context(self, user_id: str = None) -> Dict[str, Any]:
        """Gather high-priority open issues for STATUS / PRIORITY queries.

        Returns:
            {"high_priority_issues": [...], "open_issue_count": N} on hit,
            {} when no user, no repo, or no open issues.
        """
        if not user_id:
            return {}
        try:
            cached = await self._get_high_priority_issues_cached(user_id)
        except Exception as e:
            if _github_read_not_performed(e):
                return {}
            # #2151 FLOOR-ABSENT: a failed issues read is not "no open issues". The
            # registered flag arms the floor's aggregate; get_or_compute caches no
            # failure (the exception propagates past it).
            logger.warning("context_assembler_high_priority_issues_error", error=str(e))
            return {"open_issues_source_failed": True}
        return cached or {}

    async def _get_high_priority_issues_cached(
        self, user_id: str, limit: int = _HIGH_PRIORITY_ISSUES_CAP
    ) -> Optional[Dict[str, Any]]:
        """Cached high-priority issues. TTL 5min, key
        `context:high_priority_issues:{user_id}`."""
        cached = await self.cache.get_or_compute(
            key=f"context:high_priority_issues:{user_id}",
            ttl_seconds=_TTL_HIGH_PRIORITY_ISSUES,
            compute_fn=lambda: self._compute_high_priority_issues(user_id),
        )
        if not cached or "high_priority_issues" not in cached:
            return None
        return {
            "high_priority_issues": cached["high_priority_issues"][:limit],
            "open_issue_count": cached.get("open_issue_count", len(cached["high_priority_issues"])),
            "open_issue_count_capped": cached.get("open_issue_count_capped", False),
            # #1226 Phase 3: preserve the no-repo signal through the cache unpack.
            "github_repo_unconfigured": cached.get("github_repo_unconfigured", False),
        }

    async def _compute_high_priority_issues(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Compute high-priority issues (uncached) for cache miss.

        Fetches up to 100 open issues from the default repo; ranks
        priority-labeled first (critical > urgent > high), then most-recently
        updated. Caps the cached list at the surfaced count. Returns None on an
        empty result; RAISES on a failed read (#2151: the gather arms
        ``open_issues_source_failed``).
        """
        try:
            from services.integrations.github.github_integration_router import (
                GitHubIntegrationRouter,
            )

            github = GitHubIntegrationRouter()
            await github.initialize(user_id=user_id)

            # #2151 GH-NONSTRICT (Arch 10-23 21:28): strict, so a failed read raises
            # instead of returning [] (the non-strict direct read swallowed every
            # error), and it goes through the connector's one credential resolver
            # (grant, then the user's own PAT), not the router's native PAT.
            all_open = await github.get_open_issues(limit=100, strict=True)
            if not all_open:
                # #1226 Phase 3 (honest degradation): tell "no GitHub repo configured"
                # apart from "repo configured but genuinely zero open issues". The
                # resolvability check runs ONLY on the empty path (zero cost when the
                # user has issues), so the no-repo case carries a signal up to the floor
                # instead of collapsing into a silent "no open issues".
                if not await self._github_repo_resolves(user_id):
                    return {
                        "high_priority_issues": [],
                        "open_issue_count": 0,
                        "github_repo_unconfigured": True,
                    }
                return None

            def _priority_rank(issue: dict) -> int:
                labels = [str(label).lower() for label in (issue.get("labels") or [])]
                for rank, plabel in enumerate(_PRIORITY_LABELS):
                    if plabel in labels:
                        return rank
                return len(_PRIORITY_LABELS)  # unlabeled sorts after labeled

            # Stable two-stage sort: recency desc first, then priority asc — so
            # within each priority tier the most-recently-updated leads.
            ranked = sorted(all_open, key=lambda i: i.get("updated_at") or "", reverse=True)
            ranked.sort(key=_priority_rank)

            return {
                "high_priority_issues": [
                    {
                        "number": i.get("number"),
                        "title": i.get("title"),
                        "labels": i.get("labels", []),
                        "url": i.get("uri") or i.get("html_url"),
                        "updated_at": i.get("updated_at"),
                    }
                    for i in ranked[:_HIGH_PRIORITY_ISSUES_CAP]
                ],
                "open_issue_count": len(all_open),
                # #1778: a full page means the count is a floor, not a total.
                "open_issue_count_capped": len(all_open) >= 100,
            }
        except Exception:
            # #2151: raise, so the gather can say the read failed (None means empty).
            raise

    async def _github_repo_resolves(self, user_id: str = None) -> bool:
        """#1226 Phase 3: True iff a GitHub repo resolves for this user.

        Distinguishes "no repo configured" from "repo configured, zero open issues"
        on the empty path. ``UnresolvedRepoError`` → False (unconfigured). #2151: any
        OTHER exception propagates — a broken resolver is a failed read, not "no repo"
        (the caller's gather arms ``open_issues_source_failed``)."""
        from uuid import UUID

        from services.integrations.github.repo_resolver import (
            UnresolvedRepoError,
            get_user_default_repo_and_source,
            resolve_repo,
        )

        try:
            uid = UUID(user_id) if user_id and user_id != "system" else None
        except (ValueError, TypeError):
            uid = None
        try:
            await resolve_repo(user_id=uid)
            return True
        except UnresolvedRepoError:
            # #2151 FLOOR-ABSENT (Arch 2026-10-29 21:08): the resolver reads the user's
            # default repo best-effort, so a FAILED read also ends here. Re-read it
            # strictly: a failure raises (the gather arms ``open_issues_source_failed``),
            # and only a verified absence is "no repo configured".
            if uid is not None:
                await get_user_default_repo_and_source(uid, strict=True)
            return False

    # ------------------------------------------------------------------
    # #985: Active milestones gatherer
    #
    # Surfaces all open GitHub milestones (sorted by due_on asc, capped at 5)
    # for STATUS / PRIORITY / TEMPORAL / UNKNOWN-fallback queries. The floor
    # composes "how's MVP tracking?" / "what's due this week?" answers from
    # the milestone metadata. Counts only (no per-milestone issue titles) per
    # PM Q2 — keep first ship compact, iterate if floor responses lack
    # specificity.
    # ------------------------------------------------------------------

    async def _gather_active_milestones_context(self, user_id: str = None) -> Dict[str, Any]:
        """Gather active-milestones context.

        Returns:
            {"active_milestones": [...], "active_milestone_count": N} on hit;
            {} on no user / no milestones / unresolved repo / API error.
        """
        if not user_id:
            return {}
        try:
            cached = await self._get_active_milestones_cached(user_id)
        except Exception as e:
            if _github_read_not_performed(e):
                return {}
            # #2151 FLOOR-ABSENT: a failed read is not "no milestones". get_or_compute
            # caches no failure (the exception propagates past it).
            logger.warning("context_assembler_active_milestones_error", error=str(e))
            return {"milestones_source_failed": True}
        return cached or {}

    async def _get_active_milestones_cached(
        self, user_id: str, limit: int = _ACTIVE_MILESTONES_CAP
    ) -> Optional[Dict[str, Any]]:
        """Cached active-milestones list. TTL 5min, key
        `context:active_milestones:{user_id}`. Sliced on read."""
        cached = await self.cache.get_or_compute(
            key=f"context:active_milestones:{user_id}",
            ttl_seconds=_TTL_ACTIVE_MILESTONES,
            compute_fn=lambda: self._compute_active_milestones(user_id),
        )
        if not cached or "active_milestones" not in cached:
            return None
        return {
            "active_milestones": cached["active_milestones"][:limit],
            "active_milestone_count": cached.get(
                "active_milestone_count", len(cached["active_milestones"])
            ),
        }

    async def _compute_active_milestones(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Compute active-milestones list (uncached).

        Calls `list_milestones_via_mcp(state="open")`, sorts by `due_on` asc
        (nulls last), caps at _ACTIVE_MILESTONES_CAP. Returns None on an empty
        result; RAISES on a failed read (#2151: the gather arms
        ``milestones_source_failed``, or returns {} when the read was not performed).
        """
        from services.integrations.github.github_integration_router import (
            GitHubIntegrationRouter,
        )

        github = GitHubIntegrationRouter()
        await github.initialize(user_id=user_id)

        # #1524: the read raises GitHubReadFailed when it did not happen; [] means none.
        milestones = await github.list_milestones_via_mcp(state="open")
        if not milestones:
            return None

        # Sort by due_on asc; milestones without due_on go to the end.
        # Empty-string sorts before any ISO date, so use a high sentinel.
        def _sort_key(m: Dict[str, Any]):
            due = m.get("due_on")
            return (0, due) if due else (1, "")

        milestones.sort(key=_sort_key)

        return {
            "active_milestones": [
                {
                    "title": m.get("title", "Untitled"),
                    "number": m.get("number"),
                    "due_on": m.get("due_on"),
                    "open_issues": m.get("open_issues", 0),
                    "closed_issues": m.get("closed_issues", 0),
                    "url": m.get("html_url"),
                }
                for m in milestones[:_ACTIVE_MILESTONES_CAP]
            ],
            "active_milestone_count": len(milestones),
        }

    # ------------------------------------------------------------------
    # #986: Recent activity gatherer
    #
    # Surfaces recently-updated GitHub issues + PRs within a 7-day window
    # for STATUS / TEMPORAL / UNKNOWN-fallback queries. Floor composes
    # "what happened this week?" / "what did we ship?" responses. Issue
    # vs. PR distinguished via the adapter's `is_pull_request` field (#986
    # adapter prep).
    #
    # GitHub-only for first ship. Slack / commits / cross-integration
    # aggregation deferred to follow-ups (PM Q1 disposition).
    # ------------------------------------------------------------------

    async def _gather_recent_activity_context(self, user_id: str = None) -> Dict[str, Any]:
        """Gather recent-activity context for STATUS / TEMPORAL queries.

        Returns:
            {"recent_activity": [...], "recent_activity_count": N,
             "recent_activity_window_days": 7} on hit;
            {} on no user / no activity / API error.
        """
        if not user_id:
            return {}
        try:
            cached = await self._get_recent_activity_cached(user_id)
        except _PartialSourceRead as partial:
            # #2151 FLOOR-ABSENT: show what was read, and say which source wasn't.
            out = self._slice_recent_activity(partial.result) or {}
            out.update({flag: True for flag in partial.flags})
            return out
        return cached or {}

    async def _get_recent_activity_cached(
        self, user_id: str, limit: int = _RECENT_ACTIVITY_CAP
    ) -> Optional[Dict[str, Any]]:
        """Cached recent-activity list. TTL 5min, key
        `context:recent_activity:{user_id}`. Sliced on read."""
        cached = await self.cache.get_or_compute(
            key=f"context:recent_activity:{user_id}",
            ttl_seconds=_TTL_RECENT_ACTIVITY,
            compute_fn=lambda: self._compute_recent_activity(user_id),
        )
        return self._slice_recent_activity(cached, limit)

    @staticmethod
    def _slice_recent_activity(
        cached: Optional[Dict[str, Any]], limit: int = _RECENT_ACTIVITY_CAP
    ) -> Optional[Dict[str, Any]]:
        if not cached or "recent_activity" not in cached:
            return None
        return {
            "recent_activity": cached["recent_activity"][:limit],
            "recent_activity_count": cached.get(
                "recent_activity_count", len(cached["recent_activity"])
            ),
            "recent_activity_count_capped": cached.get("recent_activity_count_capped", False),
            "recent_activity_counts_by_source": cached.get("recent_activity_counts_by_source"),
            "recent_activity_window_days": cached.get(
                "recent_activity_window_days", _RECENT_ACTIVITY_WINDOW_DAYS
            ),
        }

    async def _compute_recent_activity(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Compute recent-activity list (uncached) across multiple sources.

        Aggregates per-source helpers (GitHub + calendar + Slack DMs +
        Slack @-mentions). Each helper is fail-graceful — exceptions are
        swallowed, empty lists returned. The aggregator combines, dedups,
        sorts by `updated_at` desc, caps at _RECENT_ACTIVITY_CAP. If all
        sources empty, returns None.

        Issue #1085 slice 1: source enum on each item.
        Issue #1086: calendar source added.
        Issue #1085 slice 2: Slack DM aggregator (channel_type 'im' / 'mpim').
        Issue #1085 slice 3: Slack @-mentions aggregator (channel_type 'mention').
        """
        failed_flags: Dict[str, bool] = {}
        try:
            github_items, _github_page_capped = await self._fetch_github_activity_items(user_id)
        except Exception as e:
            if _github_read_not_performed(e):
                github_items, _github_page_capped = [], False
            else:
                # #2151 FLOOR-ABSENT: the other sources still render; the floor says
                # which one it couldn't check.
                logger.warning("context_assembler_github_activity_error", error=str(e))
                github_items, _github_page_capped = [], False
                failed_flags["github_activity_source_failed"] = True
        try:
            calendar_items = await self._fetch_calendar_activity_items(user_id)
        except Exception as e:
            logger.warning("context_assembler_calendar_activity_error", error=str(e))
            calendar_items = []
            failed_flags["calendar_activity_source_failed"] = True
        slack_failed = False
        try:
            slack_items = await self._fetch_slack_activity_items(user_id)
        except Exception as e:
            logger.warning("context_assembler_slack_activity_error", error=str(e))
            slack_items, slack_failed = [], True
        try:
            slack_mention_items = await self._fetch_slack_mentions_items(user_id)
        except Exception as e:
            logger.warning("context_assembler_slack_mentions_error", error=str(e))
            slack_mention_items, slack_failed = [], True
        if slack_failed:
            failed_flags["slack_activity_source_failed"] = True

        # De-dup Slack items across DM + mention sources by (channel, ts).
        # A mention in a multi-party DM (mpim) could surface in both lists;
        # keep the first one encountered (DM aggregator's, which includes
        # the full text and a stable channel_type label).
        seen_slack_keys = {
            (i.get("channel"), i.get("ts")) for i in slack_items if i.get("channel") and i.get("ts")
        }
        slack_mention_items = [
            i for i in slack_mention_items if (i.get("channel"), i.get("ts")) not in seen_slack_keys
        ]

        all_items = github_items + calendar_items + slack_items + slack_mention_items
        if not all_items:
            if failed_flags:
                raise _PartialSourceRead(None, list(failed_flags))
            return None

        # Cross-source sort by updated_at desc (each item carries its own
        # `updated_at` from the appropriate source field).
        all_items.sort(key=lambda i: i.get("updated_at") or "", reverse=True)

        result = {
            "recent_activity": all_items[:_RECENT_ACTIVITY_CAP],
            "recent_activity_count": len(all_items),
            # #2142 (Arch 10-22 21:28): the feed is merged, so its counts are per
            # source; the floor renders each source under its own heading.
            "recent_activity_counts_by_source": _counts_by_source(all_items),
            # #1778: the GitHub source reads ONE page — a full page makes the
            # aggregate count a floor (older-in-window items may be unseen).
            "recent_activity_count_capped": _github_page_capped,
            "recent_activity_window_days": _RECENT_ACTIVITY_WINDOW_DAYS,
        }
        if failed_flags:
            raise _PartialSourceRead(result, list(failed_flags))
        return result

    async def _fetch_github_activity_items(self, user_id: str) -> tuple:
        """Fetch GitHub issues + PRs within the activity window.

        Per-source helper for `_compute_recent_activity`. Each item carries
        `source: 'github'` (#1085 slice 1 schema unification). #2151: RAISES on a
        failed read (the compute arms ``github_activity_source_failed``); no repo
        returns ([], False); no credential raises ``detail="no_credential"`` (not
        performed). The read uses this principal's credential (the #2121 rule).

        #1778: returns ``(items, page_capped)`` — the underlying read is ONE
        page, so a full page means the window census is incomplete and any
        count built on it is a floor.
        """
        from services.integrations.github.github_integration_router import (
            GitHubIntegrationRouter,
        )
        from services.integrations.github.read_failed import GitHubReadFailed

        github = GitHubIntegrationRouter()
        await github.initialize(user_id=user_id)

        resolved = await github._resolve_default_repo()
        if not resolved:
            return [], False
        owner, repo = resolved

        adapter = github.mcp_adapter
        if not adapter:
            raise GitHubReadFailed("no GitHub adapter for this read", None, detail="no_adapter")
        all_items = await adapter.list_github_issues_direct(
            repo, owner, strict=True, user_id=user_id
        )
        if not all_items:
            return [], False

        # Time-window filter.
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(days=_RECENT_ACTIVITY_WINDOW_DAYS)

        def _parse_updated(s):
            """Best-effort ISO parse; returns None on failure."""
            if not s:
                return None
            try:
                # GitHub returns Zulu time; fromisoformat needs +00:00.
                # #1573 sweep: ensure_utc guards an offset-less string
                # from a naive-vs-aware TypeError against the cutoff.
                return ensure_utc(datetime.fromisoformat(s.replace("Z", "+00:00")))
            except Exception:  # silent-ok: per-item parse, None-on-failure is the documented contract; per-row logging is noise
                return None

        recent = []
        for item in all_items:
            parsed = _parse_updated(item.get("updated_at"))
            if parsed is None or parsed < cutoff:
                continue
            recent.append(item)

        return [
            {
                "source": "github",
                "number": i.get("number"),
                "title": i.get("title"),
                "state": i.get("state"),
                "type": "pr" if i.get("is_pull_request") else "issue",
                "updated_at": i.get("updated_at"),
                "url": i.get("uri"),
            }
            for i in recent
        ], len(all_items) >= 100

    async def _fetch_calendar_activity_items(self, user_id: str) -> List[Dict[str, Any]]:
        """Fetch past calendar meetings within the activity window (#1086).

        Calendar-as-activity is a distinct lens from `_gather_calendar_context`
        (future-looking). This helper fetches past meetings within
        _RECENT_ACTIVITY_WINDOW_DAYS using the existing
        CalendarIntegrationRouter.get_events_in_range method.

        Per-source helper for `_compute_recent_activity`. #2151: RAISES on a
        read that did not happen (the compute arms ``calendar_activity_source_failed``
        and still renders the other sources); not connected or no calendar
        integration returns [] (not performed). Filters out all-day events to keep "activity" focused
        on meetings (matches the pattern in `_handle_meeting_time_query`).
        Each item carries `source: 'calendar'`.
        """
        from services.integrations.calendar.calendar_integration_router import (
            CalendarIntegrationRouter,
        )

        calendar = CalendarIntegrationRouter(user_id=user_id)
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(days=_RECENT_ACTIVITY_WINDOW_DAYS)

        try:
            events = await calendar.get_events_in_range(cutoff, now)
        except Exception as e:
            if _calendar_feature_off(e):
                return []
            raise
        if not events:
            # #2151: [] is also every no-read return; the adapter's class says which.
            # Only "no_credential" (never connected) is not performed (Arch 10-24).
            read_error = calendar.last_read_error
            if read_error and read_error != "no_credential":
                raise _CalendarReadFailed(read_error)
            return []

        # Filter to non-all-day events that are actually in the past
        # (get_events_in_range may include future events that overlap
        # with the start of the range).
        def _parse_event_time(s):
            if not s:
                return None
            try:
                # #1573 sweep: ensure_utc guards an offset-less string
                # from a naive-vs-aware TypeError against now/cutoff.
                return ensure_utc(datetime.fromisoformat(str(s).replace("Z", "+00:00")))
            except Exception:  # silent-ok: per-item parse, None-on-failure is the documented contract; per-row logging is noise
                return None

        items = []
        for event in events:
            if event.get("is_all_day"):
                continue
            start = _parse_event_time(event.get("start_time"))
            if start is None or start > now or start < cutoff:
                continue
            items.append(
                {
                    "source": "calendar",
                    "title": event.get("title") or event.get("summary") or "(untitled)",
                    # Use start_time as updated_at for cross-source sort —
                    # calendar events don't have an "updated" semantic
                    # comparable to GitHub; the meeting's start is the
                    # natural "when" for past-activity ordering.
                    "updated_at": event.get("start_time"),
                    "start_time": event.get("start_time"),
                    "end_time": event.get("end_time"),
                    "duration_minutes": event.get("duration_minutes"),
                    "attendees": event.get("attendees", 0),
                    "status": event.get("status"),
                }
            )
        return items

    async def _fetch_slack_activity_items(self, user_id: str) -> List[Dict[str, Any]]:
        """Fetch the user's recent Slack DM activity (#1085 slice 2 — V1).

        V1 shape: messages in the user's direct-message channels (`im` + `mpim`)
        within `_RECENT_ACTIVITY_WINDOW_DAYS`. Per PM disposition 2026-05-17,
        option (a) `search.messages` was deferred to a future slice because it
        requires the `search:read` OAuth scope which isn't currently granted
        (would need PM re-authorization of the Slack workspace). V1 uses
        existing `im:history` / `mpim:history` scopes.

        Per-source helper for `_compute_recent_activity`. #2151: no bot token, or
        Slack's not_authed / missing_scope, returns [] (not performed); any other
        failure RAISES (the compute arms ``slack_activity_source_failed``). Caps at 5 DMs × 20 messages = 100 messages
        examined; final aggregator caps at _RECENT_ACTIVITY_CAP.

        Each item carries `source: 'slack'`.
        """
        try:
            from services.integrations.slack.config_service import SlackConfigService
            from services.integrations.slack.slack_integration_router import (
                SlackIntegrationRouter,
            )

            config_service = SlackConfigService()
            # #2151: no bot token for this account is not connected (not performed).
            if not config_service.get_config(user_id=user_id).bot_token:
                return []
            slack = SlackIntegrationRouter(config_service=config_service)

            # List the user's DM channels (im + mpim).
            # #1110: scope credential lookup to this user (ADR-058 multi-tenancy).
            list_resp = await slack.list_im_channels(user_id=user_id)
            listed = _slack_read_or_raise(list_resp, "conversations.list")
            if listed is None:
                return []
            channels = listed.get("channels", [])
            if not channels:
                return []

            # Time-window filter: Slack timestamps are float seconds since epoch.
            now = datetime.now(timezone.utc)
            cutoff = now - timedelta(days=_RECENT_ACTIVITY_WINDOW_DAYS)
            cutoff_slack_ts = cutoff.timestamp()

            # Cap channels examined to keep V1 bounded (5 DMs × 20 msgs = 100 calls).
            channels_to_check = channels[:5]
            items: List[Dict[str, Any]] = []
            for channel in channels_to_check:
                channel_id = channel.get("id")
                if not channel_id:
                    continue
                channel_type = "mpim" if channel.get("is_mpim") else "im"
                # #2151: a channel whose history fails fails the leg (the flag says so);
                # dropping it silently left the list short with nothing said.
                hist_resp = await slack.get_conversation_history(
                    channel_id, limit=20, oldest=cutoff_slack_ts, user_id=user_id
                )
                history = _slack_read_or_raise(hist_resp, "conversations.history")
                if history is None:
                    continue
                messages = history.get("messages", [])
                for msg in messages:
                    ts_str = msg.get("ts")
                    if not ts_str:
                        continue
                    try:
                        ts_float = float(ts_str)
                    except (TypeError, ValueError):
                        continue
                    msg_dt = datetime.fromtimestamp(ts_float, tz=timezone.utc)
                    text = msg.get("text", "")
                    # Use first 80 chars as a preview title; mirrors GitHub's title slot.
                    preview = text[:80] if text else "(no text)"
                    items.append(
                        {
                            "source": "slack",
                            "title": preview,
                            # Use ISO format for cross-source sort with GitHub/calendar.
                            "updated_at": msg_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
                            "channel": channel_id,
                            "channel_type": channel_type,
                            "user": msg.get("user"),
                            "ts": ts_str,
                        }
                    )
            return items
        except _SlackReadFailed:
            raise
        except Exception as e:
            logger.warning("context_assembler_slack_activity_error", error=str(e))
            raise _SlackReadFailed(str(e)) from e

    async def _fetch_slack_mentions_items(self, user_id: str) -> List[Dict[str, Any]]:
        """Fetch the user's recent Slack @-mentions (#1085 slice 3).

        Uses Slack's `search.messages` Web API method, which requires a USER
        token (Slack docs: "User-only method") with the `search:read` scope.
        Per the 2026-05-20 OAuth re-auth + 2026-05-21 integration-health work,
        the `slack_user` token is now persisted in the user-scoped keychain
        after a successful OAuth callback (alongside the existing `slack_bot`
        token used by the DM aggregator).

        Implementation note (#1338): this method now goes through
        `SlackIntegrationRouter.test_auth(use_user_token=True)` +
        `SlackIntegrationRouter.search_messages()` rather than its own aiohttp
        call. The client layer's `_make_request` now supports a user-token path
        (`use_user_token=True`) and user-scoped `get_config(user_id)` (#1110), so
        the prior direct-aiohttp workaround (deferred from #1085 slice 3) is
        retired. Honest-degrades when no user token is configured (the router's
        user-token path returns an auth error → [] here).

        Per-source helper for `_compute_recent_activity`. Fail-graceful: returns
        [] on any error (no user token / auth.test fails / search.messages fails
        / network error). Caps at 20 most-recent mentions within
        `_RECENT_ACTIVITY_WINDOW_DAYS`; final aggregator caps at
        `_RECENT_ACTIVITY_CAP`.

        Each item carries `source: 'slack'`, `channel_type: 'mention'` to
        distinguish from the DM aggregator's `'im'` / `'mpim'` items.

        De-duplication against the DM aggregator (#1085 slice 2): a mention in
        a multi-party DM (mpim) could surface in both this method's results +
        the DM aggregator's. The aggregator-level merge in
        `_compute_recent_activity` is responsible for any de-dup; we do not
        de-dup here.
        """
        try:
            from services.integrations.slack.config_service import SlackConfigService
            from services.integrations.slack.slack_integration_router import (
                SlackIntegrationRouter,
            )

            config_service = SlackConfigService()
            # #2151: no user token (most accounts) is not performed, not a failure.
            if not config_service.get_config(user_id=user_id).user_token:
                return []
            slack = SlackIntegrationRouter(config_service=config_service)

            # Step 1: auth.test (USER token) to discover the user's Slack handle
            # so we can build the `@<handle>` mention query. #1338: routed through
            # the router's user-token path (honest-degrades if no user token).
            auth_resp = await slack.test_auth(user_id=user_id, use_user_token=True)
            authed = _slack_read_or_raise(auth_resp, "auth.test")
            if authed is None:
                return []
            slack_handle = authed.get("user")
            if not slack_handle:
                return []

            # Step 2: search.messages for mentions of @<handle>, newest first.
            search_resp = await slack.search_messages(f"@{slack_handle}", user_id=user_id, count=20)
            searched = _slack_read_or_raise(search_resp, "search.messages")
            if searched is None:
                return []
            matches = (searched.get("messages") or {}).get("matches") or []

            # Filter to time window + convert to items.
            now = datetime.now(timezone.utc)
            cutoff = now - timedelta(days=_RECENT_ACTIVITY_WINDOW_DAYS)
            cutoff_slack_ts = cutoff.timestamp()

            items: List[Dict[str, Any]] = []
            for msg in matches:
                ts_str = msg.get("ts")
                if not ts_str:
                    continue
                try:
                    ts_float = float(ts_str)
                except (TypeError, ValueError):
                    continue
                if ts_float < cutoff_slack_ts:
                    continue
                msg_dt = datetime.fromtimestamp(ts_float, tz=timezone.utc)
                text = msg.get("text") or ""
                preview = text[:80] if text else "(no text)"
                # search.messages returns channel info as a nested dict
                # (`{"channel": {"id": "...", "name": "..."}, ...}`) rather
                # than the flat top-level channel ID returned by
                # `conversations.history`. Normalize to the same shape.
                channel_obj = msg.get("channel") or {}
                channel_id = channel_obj.get("id") if isinstance(channel_obj, dict) else None
                items.append(
                    {
                        "source": "slack",
                        "title": preview,
                        "updated_at": msg_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "channel": channel_id,
                        "channel_type": "mention",
                        "user": msg.get("user"),
                        "ts": ts_str,
                        "permalink": msg.get("permalink"),
                    }
                )
            return items
        except _SlackReadFailed:
            raise
        except Exception as e:
            logger.warning("context_assembler_slack_mentions_error", error=str(e))
            raise _SlackReadFailed(str(e)) from e
