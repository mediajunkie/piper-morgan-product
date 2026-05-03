"""
Push-mode insight surfacing (#1032 MUX-INSIGHT-PUSH).

Piper proactively surfaces insights to Stage 3+ users at contextually
appropriate moments. Most-constrained mode: multi-axis gating
(trust + confidence + relevance + cooldown + mute + user availability)
must all pass before any output reaches the user.

Per `docs/internal/design/mux/insight-surfacing-rules.md` §"Push Mode" (D4)
+ Phase 0 design doc at `dev/2026/05/03/1032-design-v0.md`.

Architecture: eligibility logic is **channel-agnostic**. The same
`maybe_push(ctx)` returns a structured `FramedPushPayload` (or None).
For MVP, the in-chat renderer is the only consumer (`ConversationalFloor.respond`
appends the payload to its response). Future system-push channel (mobile/
website OS notification) reuses the same eligibility decision pathway.

Per #1032 audit dispositions May 3:
- Q1: Phase 0 design pass = deliverable; this module + design doc are it
- Q2 Option B: tag-overlap relevance scoring (no embeddings)
- Q3: conservative initial timing (Stage 3+ + relevance + 30-min anti-spam
  + not-in-decline; conversation-pause deferred Post-MVP)
- Q4 A+B: session-mute (NL detection) + per-insight dismiss (existing)
- Q5 Option A: in-chat for MVP; eligibility designed channel-agnostic
- Q6: ENFORCED STOP if embeddings or other unscoped infra needed
- Q7: hard gate Stage 1+2 → no push; trust-read errors → no push (fail-safe)
"""

from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Tuple


logger = logging.getLogger(__name__)


# =============================================================================
# Configuration (env-driven defaults per Phase 0 design)
# =============================================================================


def _env_float(name: str, default: float) -> float:
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        v = float(raw)
        return v if v >= 0 else default
    except (ValueError, TypeError):
        return default


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        v = int(raw)
        return v if v >= 0 else default
    except (ValueError, TypeError):
        return default


def get_min_confidence() -> float:
    return _env_float("PIPER_PUSH_MIN_CONFIDENCE", 0.75)


def get_relevance_threshold() -> int:
    return _env_int("PIPER_PUSH_RELEVANCE_THRESHOLD", 3)


def get_min_interval_minutes() -> int:
    return _env_int("PIPER_PUSH_MIN_INTERVAL_MINUTES", 30)


def get_stage_stability_hours() -> int:
    return _env_int("PIPER_PUSH_STAGE_STABILITY_HOURS", 2)


# =============================================================================
# Trust Gate (Phase 2)
# =============================================================================


# Stage 3 (ESTABLISHED) is the canonical "Push eligible" threshold per D1.
TRUST_STAGE_PUSH_MIN = 3


async def is_eligible_by_trust(
    user_id: str,
    trust_service=None,
    stage_promoted_at: Optional[datetime] = None,
    now: Optional[datetime] = None,
) -> bool:
    """Per Q7 hard gate: Stage 3+ required; trust-read errors → fail-safe.

    Args:
        user_id: User to check
        trust_service: optional injected trust service for testing.
            If None, dynamically imports TrustComputationService.
        stage_promoted_at: optional timestamp of last stage transition.
            If provided, stability window is enforced (must be ≥ N hours).
            None means stability unknown → treated as stable (acceptable
            during MVP since trust-stage history isn't always available).
        now: override for time injection in tests

    Returns:
        True only if Stage 3+ AND past stability window (when known) AND
        no exceptions raised. Any error → False (fail-safe per Q7).
    """
    try:
        from services.shared_types import TrustStage

        if trust_service is None:
            from services.trust.trust_computation_service import TrustComputationService
            from uuid import UUID

            # In real wiring, the route resolves a TrustComputationService
            # via dependency injection. For module-level callers, late-bind.
            # Defensive: callers should pass trust_service explicitly when
            # they have one to avoid the import cost + object creation cost.
            from services.database.session_factory import AsyncSessionFactory
            from services.repositories.user_trust_profile_repository import (
                UserTrustProfileRepository,
            )

            async with AsyncSessionFactory.session_scope() as session:
                trust_repo = UserTrustProfileRepository(session)
                trust_service = TrustComputationService(trust_repo)
                stage = await trust_service.get_trust_stage(UUID(user_id))
        else:
            stage = await trust_service.get_trust_stage(user_id)

        # Convert stage to int for comparison (TrustStage is IntEnum)
        stage_value = int(stage) if stage is not None else 0
        if stage_value < TRUST_STAGE_PUSH_MIN:
            return False

        # Stability window check (when promotion timestamp known)
        if stage_promoted_at is not None:
            now_aware = now or datetime.now(timezone.utc)
            if stage_promoted_at.tzinfo is None:
                stage_promoted_at = stage_promoted_at.replace(tzinfo=timezone.utc)
            elapsed = now_aware - stage_promoted_at
            stability_hours = get_stage_stability_hours()
            if elapsed < timedelta(hours=stability_hours):
                return False

        return True
    except Exception as e:
        logger.warning(
            "push_trust_read_error",
            extra={"user_id": user_id, "error": str(e)},
        )
        # Fail-safe: any error → no push
        return False


# =============================================================================
# Right-Moment + Anti-Spam (Phase 3)
# =============================================================================


def is_right_moment(
    *,
    last_push_at: Optional[datetime],
    in_decline_state: bool = False,
    in_onboarding: bool = False,
    now: Optional[datetime] = None,
) -> Tuple[bool, str]:
    """Check timing/state gates: anti-spam, decline, onboarding.

    Returns (eligible: bool, reason: str). Reason is for telemetry/logging
    when a gate blocks; "ok" when all pass.
    """
    if in_decline_state:
        return False, "in_decline_state"
    if in_onboarding:
        return False, "in_onboarding"

    if last_push_at is not None:
        now_aware = now or datetime.now(timezone.utc)
        if last_push_at.tzinfo is None:
            last_push_at = last_push_at.replace(tzinfo=timezone.utc)
        elapsed = now_aware - last_push_at
        min_interval = timedelta(minutes=get_min_interval_minutes())
        if elapsed < min_interval:
            return False, "anti_spam_cooldown"

    return True, "ok"


# =============================================================================
# Relevance Scoring (Phase 4)
# =============================================================================


def score_context_relevance(
    insight,
    context_entities: Optional[List[str]] = None,
    context_topics: Optional[List[str]] = None,
) -> int:
    """Tag-overlap relevance score per Q2 Option B.

    Formula:
        2 × (entities ∩ insight.applies_to_entities)
      + 1 × (topics ∩ insight.topic_tags)
      + 1 × (any context_tag ∩ {entities + topics})

    Returns the integer score; caller compares to threshold via
    `get_relevance_threshold()` (default 3).
    """
    if insight is None or insight.learning is None:
        return 0

    entity_set = set(context_entities or [])
    topic_set = set(context_topics or [])

    score = 0
    learning = insight.learning

    # Entity overlap (weight 2)
    for ent in learning.applies_to_entities or []:
        if ent in entity_set:
            score += 2

    # Topic overlap (weight 1)
    for tag in learning.topic_tags or []:
        if tag in topic_set:
            score += 1

    # Context-tag overlap (weight 1)
    combined = entity_set | topic_set
    for tag in insight.context_tags or []:
        if tag in combined:
            score += 1

    return score


def is_relevant(
    insight,
    context_entities: Optional[List[str]] = None,
    context_topics: Optional[List[str]] = None,
    threshold: Optional[int] = None,
) -> bool:
    """Boolean wrapper around score_context_relevance with the configured
    threshold (default 3 per Phase 0 design)."""
    threshold = threshold if threshold is not None else get_relevance_threshold()
    return score_context_relevance(insight, context_entities, context_topics) >= threshold


# =============================================================================
# Mute (Phase 5)
# =============================================================================


# NL trigger patterns for session-mute (Q4 + Phase 0 design Decision 4)
SESSION_MUTE_PATTERNS: List[re.Pattern] = [
    re.compile(
        r"\b(don'?t|stop|no more|hold off on|silence)\s+(insights?|learnings?|suggestions?|surfac\w*|push\w*|reflect\w*)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bmute\s+(insights?|learnings?|suggestions?)\b", re.IGNORECASE),
    re.compile(r"\b(not now|hold off|hold up).{0,20}\binsights?\b", re.IGNORECASE),
    re.compile(
        r"\bquiet (the|those|all)\s+(insights?|learnings?|suggestions?)\b",
        re.IGNORECASE,
    ),
]


def is_session_mute_trigger(user_message: str) -> bool:
    """Detect NL session-mute request in user message.

    Per Q4: session mute is volatile (resets at session end). When this
    fires, caller flips a session-state flag; subsequent push attempts
    return None.
    """
    if not user_message:
        return False
    return any(p.search(user_message) for p in SESSION_MUTE_PATTERNS)


# =============================================================================
# FramedPushPayload — channel-agnostic eligibility output (Phase 5)
# =============================================================================


# Mute affordance text + explain affordance text per D4 §Push Format
MUTE_AFFORDANCE_TEXT = "(Not now — quiet insights for this conversation)"
EXPLAIN_AFFORDANCE_TEXT = "Tell me more"


@dataclass
class FramedPushPayload:
    """Channel-agnostic Push payload.

    Eligibility logic produces this structured value; channel renderers
    consume it. For #1032 MVP, only the in-chat renderer (floor composer)
    consumes; future system-push channel reuses with its own renderer.

    `framed_text` has already been passed through
    `frame_insight_for_surfacing` from #1033, so it's guardrail-protected
    against surveillance phrasing.
    """

    insight_id: str
    framed_text: str
    mute_affordance: str = MUTE_AFFORDANCE_TEXT
    explain_affordance: str = EXPLAIN_AFFORDANCE_TEXT


# =============================================================================
# maybe_push — top-level orchestrator (Phase 5)
# =============================================================================


@dataclass
class PushContext:
    """Channel-agnostic context for push decisions.

    Caller (e.g., floor composer at MVP, future system-push at Post-MVP)
    populates this from its own state and passes to maybe_push.
    """

    user_id: str
    user_message: Optional[str] = None
    context_entities: List[str] = field(default_factory=list)
    context_topics: List[str] = field(default_factory=list)
    session_mute_active: bool = False
    last_push_at: Optional[datetime] = None
    stage_promoted_at: Optional[datetime] = None  # for stability window
    in_decline_state: bool = False
    in_onboarding: bool = False


async def maybe_push(
    ctx: PushContext,
    journal=None,
    trust_service=None,
    now: Optional[datetime] = None,
) -> Optional[FramedPushPayload]:
    """Channel-agnostic Push eligibility orchestrator.

    Multi-axis gating per Phase 0 design:
    1. Session mute (Q4 A) → no push
    2. NL session-mute trigger in current user message → no push (caller
       is expected to flip session_mute_active before next call)
    3. Right-moment + anti-spam (Q3) → no push
    4. Trust gate Stage 3+ + stability (Q7) → no push
    5. Retrieve unsurfaced insights for user (existing repo method
       already excludes deleted, dismissed, recently-surfaced)
    6. Score relevance for each candidate (Q2 Option B)
    7. Pick highest-scoring relevant insight; if none, no push
    8. Frame via #1033 guardrail-protected helper
    9. Return FramedPushPayload

    Args:
        ctx: PushContext populated by caller
        journal: optional InsightJournal; defaults to durable journal
        trust_service: optional trust service for testing
        now: time injection for tests

    Returns:
        FramedPushPayload if all gates pass, else None.
    """
    # Gate 1: session mute
    if ctx.session_mute_active:
        return None

    # Gate 2: NL session-mute trigger (volatile — caller should flip flag
    # for next turn but we also short-circuit here defensively)
    if ctx.user_message and is_session_mute_trigger(ctx.user_message):
        return None

    # Gate 3: right-moment + anti-spam
    ok, reason = is_right_moment(
        last_push_at=ctx.last_push_at,
        in_decline_state=ctx.in_decline_state,
        in_onboarding=ctx.in_onboarding,
        now=now,
    )
    if not ok:
        logger.debug(
            "push_skipped_right_moment",
            extra={"user_id": ctx.user_id, "reason": reason},
        )
        return None

    # Gate 4: trust gate (hard + stability)
    eligible = await is_eligible_by_trust(
        user_id=ctx.user_id,
        trust_service=trust_service,
        stage_promoted_at=ctx.stage_promoted_at,
        now=now,
    )
    if not eligible:
        return None

    # Gate 5: retrieve candidate insights
    if journal is None:
        from services.mux.composting_pipeline import InsightJournal

        journal = InsightJournal()

    candidates = await journal.get_unsurfaced(
        user_id=ctx.user_id,
        min_confidence=get_min_confidence(),
        trust_stage=4,  # Pull all eligible; we already gated trust above
        limit=20,
    )

    if not candidates:
        return None

    # Gate 6+7: score relevance, pick best
    scored: List[Tuple[int, object]] = []
    for insight in candidates:
        score = score_context_relevance(insight, ctx.context_entities, ctx.context_topics)
        if score >= get_relevance_threshold():
            scored.append((score, insight))

    if not scored:
        return None

    scored.sort(key=lambda x: x[0], reverse=True)
    best_insight = scored[0][1]

    # Gate 8: frame via #1033 guardrail-protected helper
    from services.mux.premonition import frame_insight_for_surfacing

    framed_text = frame_insight_for_surfacing(best_insight)

    # Gate 9: package
    return FramedPushPayload(
        insight_id=best_insight.id,
        framed_text=framed_text,
    )


# =============================================================================
# Format for in-chat rendering (Phase 6 — MVP renderer only)
# =============================================================================


def format_push_for_chat(
    floor_response: str, payload: FramedPushPayload
) -> str:
    """In-chat renderer for FramedPushPayload (MVP only).

    Appends the framed insight to the floor's response with a separator
    + affordance text per D4 §Push Format.

    Future system-push renderer (mobile/website OS notification) will use
    a different layout but consumes the same FramedPushPayload.
    """
    return (
        f"{floor_response}\n"
        f"\n"
        f"---\n"
        f"\n"
        f"{payload.framed_text}\n"
        f"\n"
        f"_{payload.mute_affordance}_ · _{payload.explain_affordance}_"
    )
