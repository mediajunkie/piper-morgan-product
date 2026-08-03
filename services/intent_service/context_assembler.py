"""
Context Assembler for Conversational Floor (#911 Phase 2)

Gathers structured data for the conversational floor, organized by intent
category. The floor LLM receives raw facts and decides what's relevant to
the user's question.

Design principles:
1. Declarative — returns structured data (facts, lists), not formatted text
2. Fail-graceful — partial results on failure, never throws
3. Cache-ready — design for Redis TTL caching later (not implemented yet)
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import structlog

from services.intent_service.context_cache import ContextCache

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
    except Exception:
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


def _compute_deadline_proximity(due_date: Optional[datetime]) -> str:
    """
    #951: Bucket a due_date into a proximity label for floor context.

    Returns one of:
    - "none": no due_date
    - "overdue": due_date is in the past
    - "due_today": due_date is today (before end of day, not yet past)
    - "due_this_week": due in the next 1-7 days
    - "later": due > 7 days out

    Uses naive datetime.now() to match existing gatherer pattern.
    Timezone-aware proximity is a future enhancement (#586 territory).
    """
    if due_date is None:
        return "none"

    now = datetime.now()
    if due_date < now:
        return "overdue"

    end_of_today = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    if due_date <= end_of_today:
        return "due_today"

    end_of_week = now + timedelta(days=7)
    if due_date <= end_of_week:
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
        "projects": {"source": "ProjectManagementService"},
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
            elif category == "CONVERSATION":
                # Issue #903: Surface due reminders for greeting context
                ctx = await self._gather_reminder_context(user_id)
                if ctx:
                    context.update(ctx)
                    self._attribute_provenance(list(ctx.keys()), user_id=user_id)
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
        """
        context: Dict[str, Any] = {}

        # #1428: ledger-derived, user-register capability lines (pure function,
        # no registry/plugin dependency — deterministic and marker-free).
        from services.intent_service.chat_pointers import capability_answer_lines

        context["capabilities"] = capability_answer_lines()

        # Integrations from plugin registry (dynamic, reflects runtime state)
        try:
            from services.plugins import get_plugin_registry

            registry = get_plugin_registry()
            plugin_status = registry.get_status_all()

            integrations = []
            for name, status in plugin_status.items():
                is_configured = status.get("configured", False)
                is_active = status.get("active", False) or status.get("status") == "active"
                integrations.append(
                    {
                        "name": name,
                        "status": "active" if (is_configured or is_active) else "inactive",
                    }
                )

            context["integrations"] = integrations
        except Exception as e:
            logger.warning("context_assembler_identity_capabilities_error", error=str(e))

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

        return context

    async def _gather_memory_context(
        self, user_id: str = None, session_id: str = None
    ) -> Dict[str, Any]:
        """
        Gather conversation history summary for MEMORY intents.

        Reads from in-memory conversation context and UserHistoryService.
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
                logger.warning("context_assembler_memory_history_error", error=str(e))

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
                logger.warning("context_assembler_memory_persistent_error", error=str(e))

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

        Fail-graceful: any DB error → empty insights dict (NOT exception).
        Empty dict signals to the floor that no insights are available,
        which lets it respond with the honest "nothing learned yet" framing
        the AC requires (vs. fabricating or deflecting).
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
                insights = await repo.list_for_user(
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
                "total_count": len(insights),
                "is_empty": len(insights) == 0,
            }
        except Exception as e:
            logger.warning(
                "context_assembler_insight_pull_error",
                user_id=user_id,
                error=str(e),
            )
            context["insights"] = {
                "high_confidence": [],
                "medium_confidence": [],
                "low_confidence": [],
                "total_count": 0,
                "is_empty": True,
            }

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
            user_ctx_data = await self._get_user_context_cached(user_id)
            if user_ctx_data:
                context.update(user_ctx_data)

        # #984: Cached pending todos. Eager-invalidated on todo CRUD (Q3=c).
        # Note: cap at 5 here vs. 10 in temporal — but the cache stores the
        # full list (up to 10) and we slice on read for consistency.
        if user_id:
            pending_data = await self._get_pending_todos_cached(user_id, limit=5)
            if pending_data and "pending_todos" in pending_data:
                context["pending_todos"] = pending_data["pending_todos"]

        # #1155: GitHub connection flag (the high-priority issues themselves are
        # gathered below — this block only records whether GitHub is connected).
        try:
            from services.plugins import get_plugin_registry

            registry = get_plugin_registry()
            github_status = registry.get_status_all().get("github", {})
            if github_status.get("configured") or github_status.get("active"):
                context["github_connected"] = True
            else:
                context["github_connected"] = False
        except Exception as e:
            logger.warning("context_assembler_status_github_error", error=str(e))
            context["github_connected"] = False

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
        return await self.cache.get_or_compute(
            key=f"context:calendar:{user_id}",
            ttl_seconds=_TTL_CALENDAR,
            compute_fn=lambda: self._compute_calendar_context(user_id),
        )

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

        Fail-graceful: calendar unavailable (no OAuth, plugin disabled,
        router raises) returns {} — no "calendar" key, no exception.
        """
        try:
            # Lazy-import to avoid startup cost and break potential import cycles
            from services.integrations.calendar.calendar_integration_router import (
                CalendarIntegrationRouter,
            )

            router = CalendarIntegrationRouter(user_id=user_id)
            summary = await router.get_temporal_summary(user_id=user_id)
        except Exception as e:
            logger.warning("context_assembler_calendar_error", error=str(e))
            return {}

        if not summary:
            return {}

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
                return {
                    "due_reminders": due_reminders,
                    "reminder_count": len(due_reminders),
                }
        except Exception as e:  # silent-ok: failure surfaces via source_failed flag, not an empty context (#1425)
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
        if not cached or "pending_todos" not in cached:
            return None
        return {
            "pending_todos": cached["pending_todos"][:limit],
            "pending_todo_count": cached.get("pending_todo_count", len(cached["pending_todos"])),
        }

    async def _compute_pending_todos(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Compute pending-todos (uncached) for cache miss. Stores up to 10."""
        try:
            from uuid import UUID

            from services.todo.todo_management_service import TodoManagementService

            todo_svc = TodoManagementService()
            pending = await todo_svc.list_todos(user_id=UUID(user_id), include_completed=False)
            if not pending:
                return None
            return {
                "pending_todos": [_todo_to_dict(t) for t in pending[:10]],
                "pending_todo_count": len(pending),
            }
        except Exception as e:
            logger.warning("context_assembler_pending_todos_error", error=str(e))
            return None

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
        if not cached or "completed_todos" not in cached:
            return None
        return {
            "completed_todos": cached["completed_todos"][:limit],
            "completed_todo_count": cached.get(
                "completed_todo_count", len(cached["completed_todos"])
            ),
        }

    async def _compute_completed_todos(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Compute completed-todos (uncached) for cache miss. Stores up to 10."""
        try:
            from uuid import UUID

            from services.todo.todo_management_service import TodoManagementService

            todo_svc = TodoManagementService()
            all_todos = await todo_svc.list_todos(user_id=UUID(user_id), include_completed=True)
            completed = [t for t in all_todos if getattr(t, "completed", False)]
            if not completed:
                return None
            return {
                "completed_todos": [
                    {"text": t.text, "completed_at": str(getattr(t, "completed_at", ""))}
                    for t in completed[:10]
                ],
                "completed_todo_count": len(completed),
            }
        except Exception as e:
            logger.warning("context_assembler_completed_todos_error", error=str(e))
            return None

    async def _get_projects_cached(self, user_id: str, limit: int = 5) -> Optional[Dict[str, Any]]:
        """Cached projects list (from `projects` table). TTL 5min.

        Key: `context:projects:{user_id}`. TTL-only invalidation (Q3=c).
        """
        cached = await self.cache.get_or_compute(
            key=f"context:projects:{user_id}",
            ttl_seconds=_TTL_PROJECTS,
            compute_fn=lambda: self._compute_projects(user_id),
        )
        if not cached or "projects" not in cached:
            return None
        return {"projects": cached["projects"][:limit]}

    async def _compute_projects(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Compute project list (uncached) for cache miss. Stores up to 5."""
        try:
            from services.database.session_factory import AsyncSessionFactory

            async with AsyncSessionFactory.session_scope() as session:
                from sqlalchemy import text

                result = await session.execute(
                    text(
                        "SELECT name, created_at, updated_at FROM projects "
                        "WHERE owner_id = :uid ORDER BY updated_at DESC LIMIT 5"
                    ),
                    {"uid": user_id},
                )
                rows = result.fetchall()
                if not rows:
                    return None
                return {
                    "projects": [
                        {
                            "name": r[0],
                            "created_at": str(r[1]) if r[1] else None,
                            "last_updated": str(r[2]) if r[2] else None,
                        }
                        for r in rows
                    ]
                }
        except Exception as e:
            logger.warning("context_assembler_projects_error", error=str(e))
            return None

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
        """Compute user_context_service output (uncached) for cache miss."""
        try:
            from services.user_context_service import user_context_service

            user_ctx = await user_context_service.get_user_context(session_id=None, user_id=user_id)
            if not user_ctx:
                return None
            result: Dict[str, Any] = {}
            if hasattr(user_ctx, "projects") and user_ctx.projects:
                result["projects"] = [
                    {"name": p} if isinstance(p, str) else p for p in user_ctx.projects[:10]
                ]
            if hasattr(user_ctx, "priorities") and user_ctx.priorities:
                # #496: the floor formatter (conversational_floor._format_domain_context)
                # reads domain_context["priorities"] as a DICT (p.get("user_priorities")),
                # matching intent_service.py's other producer. Emitting a bare list here
                # meant configured PIPER.md priorities never rendered (and would AttributeError
                # if non-empty). Wrap in the dict shape so the floor surfaces them.
                result["priorities"] = {"user_priorities": user_ctx.priorities[:5]}
            if hasattr(user_ctx, "organization") and user_ctx.organization:
                result["organization"] = user_ctx.organization
            return result or None
        except Exception as e:
            logger.warning("context_assembler_user_context_error", error=str(e))
            return None

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
        cached = await self._get_blocked_items_cached(user_id)
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
        }

    async def _compute_blocked_items(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Compute blocked-items (uncached) for cache miss.

        Fetches up to 100 open issues from the default repo, filters those
        carrying `status: blocked`, sorts by `updated_at` desc, caps the
        cached list at 10. Fail-graceful — returns None on any error or
        empty result.
        """
        try:
            from services.integrations.github.github_integration_router import (
                GitHubIntegrationRouter,
            )

            github = GitHubIntegrationRouter()
            await github.initialize(user_id=user_id)

            # Pull a generous slice so the post-filter still finds blocked
            # items even when there are many non-blocked open issues.
            all_open = await github.get_open_issues(limit=100)
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
            }
        except Exception as e:
            logger.warning("context_assembler_blocked_items_error", error=str(e))
            return None

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
        cached = await self._get_high_priority_issues_cached(user_id)
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
            # #1226 Phase 3: preserve the no-repo signal through the cache unpack.
            "github_repo_unconfigured": cached.get("github_repo_unconfigured", False),
        }

    async def _compute_high_priority_issues(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Compute high-priority issues (uncached) for cache miss.

        Fetches up to 100 open issues from the default repo; ranks
        priority-labeled first (critical > urgent > high), then most-recently
        updated. Caps the cached list at the surfaced count. Fail-graceful —
        returns None on any error or empty result.
        """
        try:
            from services.integrations.github.github_integration_router import (
                GitHubIntegrationRouter,
            )

            github = GitHubIntegrationRouter()
            await github.initialize(user_id=user_id)

            all_open = await github.get_open_issues(limit=100)
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
            }
        except Exception as e:
            logger.warning("context_assembler_high_priority_issues_error", error=str(e))
            return None

    async def _github_repo_resolves(self, user_id: str = None) -> bool:
        """#1226 Phase 3: True iff a GitHub repo resolves for this user.

        Distinguishes "no repo configured" from "repo configured, zero open issues"
        on the empty path. Best-effort: any resolution failure (incl.
        ``UnresolvedRepoError``) → False (treated as unconfigured)."""
        from uuid import UUID

        from services.integrations.github.repo_resolver import resolve_repo

        try:
            uid = UUID(user_id) if user_id and user_id != "system" else None
        except (ValueError, TypeError):
            uid = None
        try:
            await resolve_repo(user_id=uid)
            return True
        except Exception:
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
        cached = await self._get_active_milestones_cached(user_id)
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
        (nulls last), caps at _ACTIVE_MILESTONES_CAP. Fail-graceful — returns
        None on any error or empty result.
        """
        try:
            from services.integrations.github.github_integration_router import (
                GitHubIntegrationRouter,
            )

            github = GitHubIntegrationRouter()
            await github.initialize(user_id=user_id)
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
        except Exception as e:
            logger.warning("context_assembler_active_milestones_error", error=str(e))
            return None

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
        cached = await self._get_recent_activity_cached(user_id)
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
        if not cached or "recent_activity" not in cached:
            return None
        return {
            "recent_activity": cached["recent_activity"][:limit],
            "recent_activity_count": cached.get(
                "recent_activity_count", len(cached["recent_activity"])
            ),
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
        github_items = await self._fetch_github_activity_items(user_id)
        calendar_items = await self._fetch_calendar_activity_items(user_id)
        slack_items = await self._fetch_slack_activity_items(user_id)
        slack_mention_items = await self._fetch_slack_mentions_items(user_id)

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
            return None

        # Cross-source sort by updated_at desc (each item carries its own
        # `updated_at` from the appropriate source field).
        all_items.sort(key=lambda i: i.get("updated_at") or "", reverse=True)

        return {
            "recent_activity": all_items[:_RECENT_ACTIVITY_CAP],
            "recent_activity_count": len(all_items),
            "recent_activity_window_days": _RECENT_ACTIVITY_WINDOW_DAYS,
        }

    async def _fetch_github_activity_items(self, user_id: str) -> List[Dict[str, Any]]:
        """Fetch GitHub issues + PRs within the activity window.

        Per-source helper for `_compute_recent_activity`. Fail-graceful:
        returns [] on any error. Each item carries `source: 'github'`
        (#1085 slice 1 schema unification).
        """
        try:
            from services.integrations.github.github_integration_router import (
                GitHubIntegrationRouter,
            )

            github = GitHubIntegrationRouter()
            await github.initialize(user_id=user_id)

            resolved = await github._resolve_default_repo()
            if not resolved:
                return []
            owner, repo = resolved

            adapter = github.mcp_adapter
            if not adapter:
                return []
            all_items = await adapter.list_github_issues_direct(repo, owner)
            if not all_items:
                return []

            # Time-window filter.
            now = datetime.now(timezone.utc)
            cutoff = now - timedelta(days=_RECENT_ACTIVITY_WINDOW_DAYS)

            def _parse_updated(s):
                """Best-effort ISO parse; returns None on failure."""
                if not s:
                    return None
                try:
                    # GitHub returns Zulu time; fromisoformat needs +00:00
                    return datetime.fromisoformat(s.replace("Z", "+00:00"))
                except Exception:
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
            ]
        except Exception as e:
            logger.warning("context_assembler_github_activity_error", error=str(e))
            return []

    async def _fetch_calendar_activity_items(self, user_id: str) -> List[Dict[str, Any]]:
        """Fetch past calendar meetings within the activity window (#1086).

        Calendar-as-activity is a distinct lens from `_gather_calendar_context`
        (future-looking). This helper fetches past meetings within
        _RECENT_ACTIVITY_WINDOW_DAYS using the existing
        CalendarIntegrationRouter.get_events_in_range method.

        Per-source helper for `_compute_recent_activity`. Fail-graceful:
        returns [] on any error (calendar API down → caller still gets
        GitHub items). Filters out all-day events to keep "activity" focused
        on meetings (matches the pattern in `_handle_meeting_time_query`).
        Each item carries `source: 'calendar'`.
        """
        try:
            from services.integrations.calendar.calendar_integration_router import (
                CalendarIntegrationRouter,
            )

            calendar = CalendarIntegrationRouter(user_id=user_id)
            now = datetime.now(timezone.utc)
            cutoff = now - timedelta(days=_RECENT_ACTIVITY_WINDOW_DAYS)

            events = await calendar.get_events_in_range(cutoff, now)
            if not events:
                return []

            # Filter to non-all-day events that are actually in the past
            # (get_events_in_range may include future events that overlap
            # with the start of the range).
            def _parse_event_time(s):
                if not s:
                    return None
                try:
                    return datetime.fromisoformat(str(s).replace("Z", "+00:00"))
                except Exception:
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
        except Exception as e:
            logger.warning("context_assembler_calendar_activity_error", error=str(e))
            return []

    async def _fetch_slack_activity_items(self, user_id: str) -> List[Dict[str, Any]]:
        """Fetch the user's recent Slack DM activity (#1085 slice 2 — V1).

        V1 shape: messages in the user's direct-message channels (`im` + `mpim`)
        within `_RECENT_ACTIVITY_WINDOW_DAYS`. Per PM disposition 2026-05-17,
        option (a) `search.messages` was deferred to a future slice because it
        requires the `search:read` OAuth scope which isn't currently granted
        (would need PM re-authorization of the Slack workspace). V1 uses
        existing `im:history` / `mpim:history` scopes.

        Per-source helper for `_compute_recent_activity`. Fail-graceful:
        returns [] on any error (Slack unavailable / token missing / DM
        listing fails). Caps at 5 DMs × 20 messages = 100 messages
        examined; final aggregator caps at _RECENT_ACTIVITY_CAP.

        Each item carries `source: 'slack'`.
        """
        try:
            from services.integrations.slack.config_service import SlackConfigService
            from services.integrations.slack.slack_integration_router import (
                SlackIntegrationRouter,
            )

            config_service = SlackConfigService()
            slack = SlackIntegrationRouter(config_service=config_service)

            # List the user's DM channels (im + mpim).
            # #1110: scope credential lookup to this user (ADR-058 multi-tenancy).
            list_resp = await slack.list_im_channels(user_id=user_id)
            if not list_resp or not list_resp.success:
                return []
            channels = list_resp.data.get("channels", []) if list_resp.data else []
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
                try:
                    hist_resp = await slack.get_conversation_history(
                        channel_id, limit=20, oldest=cutoff_slack_ts, user_id=user_id
                    )
                except Exception:
                    # Per-channel fail-graceful: continue with other channels.
                    continue
                if not hist_resp or not hist_resp.success:
                    continue
                messages = hist_resp.data.get("messages", []) if hist_resp.data else []
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
        except Exception as e:
            logger.warning("context_assembler_slack_activity_error", error=str(e))
            return []

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
            slack = SlackIntegrationRouter(config_service=config_service)

            # Step 1: auth.test (USER token) to discover the user's Slack handle
            # so we can build the `@<handle>` mention query. #1338: routed through
            # the router's user-token path (honest-degrades if no user token).
            auth_resp = await slack.test_auth(user_id=user_id, use_user_token=True)
            if not auth_resp or not auth_resp.success:
                return []
            slack_handle = (auth_resp.data or {}).get("user")
            if not slack_handle:
                return []

            # Step 2: search.messages for mentions of @<handle>, newest first.
            search_resp = await slack.search_messages(
                f"@{slack_handle}", user_id=user_id, count=20
            )
            if not search_resp or not search_resp.success:
                return []
            matches = ((search_resp.data or {}).get("messages") or {}).get("matches") or []

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
        except Exception as e:
            logger.warning("context_assembler_slack_mentions_error", error=str(e))
            return []
