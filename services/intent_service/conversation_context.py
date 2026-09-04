"""
Discourse Working State (#427 MUX-IMPLEMENT-CONVERSE-MODEL)

Tracks conversational state to enable:
- Conversational follow-ups ("How about today?" after asking about tomorrow)
- Context-dependent phrase resolution
- Turn-by-turn memory within a session

Design principle: "Intent inherits from context when ambiguous"

The 10-turn context window (per PM-034) enables natural conversation
without surveillance-level tracking.

Architecture (#1207 unification, 2026-06-12 — where this module sits):
- This module's ``ConversationContext`` is the in-process **discourse
  working state** — a per-(user, session) PROJECTION the classifier/floor
  read and annotate (recent-turn window, lens stack, last offer, floor
  flags, provenance sidecar). It is NOT the domain Conversation aggregate
  and is NOT a system of record.
- The system of record is the database, reached only through
  ``ConversationManager`` (services/conversation/conversation_manager.py):
  turns hydrate IN via ``hydrate_turns_from_db()`` (#1122) and the Layer-4
  slice via ``apply_persisted_state()`` (#953); completed turns + state
  persist OUT at the process_intent outer seam via
  ``save_conversation_turn``. This module performs no I/O of its own.
- ``hydrate_turns_from_db`` is the single domain→working-state turn
  mapping point; ``build_recent_history`` is the single prompt-shaped
  reader. Add consumers to those, not new copies.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional
from uuid import UUID, uuid4

import structlog

from services.intent_service.intent_types import Intent, IntentCategory

logger = structlog.get_logger()


class FollowUpType(str, Enum):
    """Types of conversational follow-ups."""

    TEMPORAL_SHIFT = "temporal_shift"  # "How about today?" after "tomorrow"
    ENTITY_REFERENCE = "entity_reference"  # "What about that one?"
    CONFIRMATION = "confirmation"  # "Yes", "No", "Okay"
    REFINEMENT = "refinement"  # "Just the morning ones"
    CONTINUATION = "continuation"  # "And?" "What else?"
    NEGATION = "negation"  # "Not that one" "Something else"


@dataclass
class LastOffer:
    """Tracks the most recent contextual offer for continuation detection (#852).

    When Piper makes a contextual offer ("Would you like me to explain more?"),
    this stores the continuation hint so the next turn's classifier knows what
    "yes" refers to. One-turn memory — cleared on every new turn regardless.

    Bright-line rule (Chief Architect): If "yes" invokes a named workflow,
    use action_required. If "yes" means "continue/elaborate," use this.
    """

    offer_type: str  # "contextual" (for now; "actionable" reserved for future use)
    continuation_hint: str  # What to continue with, e.g. "explain how project context works"
    offer_text: str = ""  # Original offer text for logging/debugging


@dataclass
class ConversationTurn:
    """
    A single turn in the conversation.

    Captures the message, intent, and key entities for reference resolution.
    """

    id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.now)
    message: str = ""
    response: Optional[str] = None  # #922: Piper's response, added after processing
    intent: Optional[Intent] = None

    # Extracted entities for reference resolution
    temporal_reference: Optional[str] = None  # "tomorrow", "today", "this week"
    entity_references: list[str] = field(
        default_factory=list
    )  # stored, not yet consumed (audit #827)
    topic: Optional[str] = None  # Inferred topic

    # Conversational lens (#763 GLUE-FOLLOWUP)
    lens: Optional[str] = None  # ConversationalLens value or None

    @property
    def age_seconds(self) -> float:
        """How old this turn is in seconds."""
        return (datetime.now() - self.timestamp).total_seconds()


@dataclass
class ConversationContext:
    """
    Tracks the conversational context for a session.

    Maintains a sliding window of recent turns to enable:
    - Follow-up detection
    - Reference resolution
    - Intent inheritance
    - Lens tracking (#763 GLUE-FOLLOWUP)
    """

    session_id: UUID = field(default_factory=uuid4)
    user_id: Optional[UUID] = None
    turns: list[ConversationTurn] = field(default_factory=list)
    max_turns: int = 10  # PM-034: 10-turn context window
    max_age_minutes: int = 30  # Conversations older than 30 min are stale

    # Lens stack for topic digression/restoration (#763 GLUE-FOLLOWUP)
    lens_stack: list[str] = field(default_factory=list)

    # Issue #852: Track last contextual offer for continuation detection
    last_offer: Optional[LastOffer] = None

    # Issue #913: Track whether last response was a floor hit (continuation rate)
    last_response_was_floor: bool = False
    last_floor_category: Optional[str] = None

    # Issue #953: one-shot guard so the async floor path hydrates persisted
    # Layer-4 state (lens_stack + last_offer + floor flags) from the DB exactly
    # once per in-memory context lifetime (on resume / restart). Not persisted,
    # not part of equality (compare=False).
    _hydrated: bool = field(default=False, compare=False, repr=False)

    # #1688: the FTUX empty-state interview's bound answer -- session-scoped
    # working state, set at the offer seam (first_contact.handle_ftux_
    # interview_turn) and surfaced to the floor via the context assembler.
    # WITHIN-SESSION use only: cross-session recall is #1705 (Leg D
    # increment 6) and does not exist; no surface may claim otherwise.
    ftux_interview_answer: Optional[str] = None

    # Issue #1030 R4: per-turn provenance sidecar for "why did you suggest that?"
    # citations. Keyed by ConversationTurn.id. Values are dicts of
    # {domain_context_key: {source, identifier, fetch_timestamp, ...}} representing
    # what context the floor had available when composing that turn's response.
    # Pruned in lockstep with self.turns via _prune_old_turns() so size is bounded
    # by max_turns + max_age_minutes (per PM R2 disposition + Survey 3 recommendation).
    turn_provenance: dict = field(default_factory=dict)

    def add_turn(
        self,
        message: str,
        intent: Optional[Intent] = None,
        temporal_reference: Optional[str] = None,
        entity_references: Optional[list[str]] = None,
        topic: Optional[str] = None,
        lens: Optional[str] = None,
    ) -> ConversationTurn:
        """
        Add a new turn to the conversation.

        Automatically prunes old turns to maintain the context window.
        """
        turn = ConversationTurn(
            message=message,
            intent=intent,
            temporal_reference=temporal_reference,
            entity_references=entity_references or [],
            topic=topic,
            lens=lens,
        )
        self.turns.append(turn)
        self._prune_old_turns()
        return turn

    def _prune_old_turns(self) -> None:
        """Remove turns outside the context window."""
        # Remove by age
        cutoff = datetime.now() - timedelta(minutes=self.max_age_minutes)
        self.turns = [t for t in self.turns if t.timestamp > cutoff]

        # Remove by count (keep most recent)
        if len(self.turns) > self.max_turns:
            self.turns = self.turns[-self.max_turns :]

        # #1030 R4: prune turn_provenance entries in lockstep with turns.
        # Without this, the sidecar would grow unbounded over long sessions
        # (R2 risk from R4 design). Keep only entries for turns still present.
        if self.turn_provenance:
            kept_ids = {t.id for t in self.turns}
            self.turn_provenance = {k: v for k, v in self.turn_provenance.items() if k in kept_ids}

        # #763: Clear lens stack when all turns are pruned
        if not self.turns:
            self.lens_stack.clear()

    def get_turn_provenance(self, turn_id: UUID) -> Optional[dict]:
        """Issue #1030 R4: lookup provenance for a specific turn id.

        Returns None if the turn id isn't in the sidecar (either turn never had
        provenance attached, or it was pruned out of the 10-turn / 30-min window).
        """
        return self.turn_provenance.get(turn_id)

    def get_last_turn_provenance(self) -> Optional[dict]:
        """Issue #1030 R4: lookup provenance for the most recent turn that has any.

        Walks self.turns in reverse to find the newest turn with a provenance
        entry. Skips turns without provenance (user-only turns, errors, etc.).

        Bug-fix 2026-06-02: also handle the case where turn_provenance was
        written (Step 6) but conv_ctx.turns is empty — happens because
        IntentClassifier.classify() (the basic path used by intent_service)
        doesn't run conv_ctx.add_turn(). In that case fall back to the
        most-recently-inserted entry in turn_provenance (Python dicts preserve
        insertion order since 3.7), which represents the prior turn's
        provenance even when no turn-tracking happened.

        Returns the provenance dict or None.
        """
        for turn in reversed(self.turns):
            if turn.id in self.turn_provenance:
                return self.turn_provenance[turn.id]
        # Fallback: turn tracking didn't happen but a write did
        if self.turn_provenance:
            return next(reversed(list(self.turn_provenance.values())), None)
        return None

    def get_previous_assistant_turn(self) -> Optional[ConversationTurn]:
        """Issue #1030 R4: return the most recent turn that has an assistant
        response AND provenance available.

        Used by ProvenanceHandler to ground the citation in a specific prior
        turn ('when I mentioned X...'). Returns None if no eligible turn exists.
        """
        for turn in reversed(self.turns):
            if turn.response and turn.id in self.turn_provenance:
                return turn
        return None

    # ---- Layer-4 persistence (#953 CONTEXT-PERSIST) ----
    # The persistable slice of context = the in-memory-only state that dies on
    # restart/refresh: lens_stack + last_offer + the floor-continuation flags.
    # NOT turns (persisted via ConversationRepository/ConversationTurnDB) and NOT
    # turn_provenance (persisted to ConversationTurnDB.metadata, #1030 R4). These
    # (de)serialize the slice for the ConversationDB.context JSONB column; the
    # async persist/hydrate wiring at the floor seam is the companion increment.

    def to_persistable_state(self) -> dict[str, Any]:
        """Serialize the restart-fragile context slice to a JSON-safe dict.

        Round-trips with ``apply_persisted_state``. Excludes turns + provenance
        (persisted elsewhere). #953.
        """
        return {
            "lens_stack": list(self.lens_stack),
            "last_offer": (
                {
                    "offer_type": self.last_offer.offer_type,
                    "continuation_hint": self.last_offer.continuation_hint,
                    "offer_text": self.last_offer.offer_text,
                }
                if self.last_offer is not None
                else None
            ),
            "last_response_was_floor": self.last_response_was_floor,
            "last_floor_category": self.last_floor_category,
            # #1688: session-scoped (the persisted slice is keyed by THIS
            # session) -- surviving a mid-session restart is not
            # cross-session recall, which stays #1705's.
            "ftux_interview_answer": self.ftux_interview_answer,
        }

    def apply_persisted_state(self, state: Optional[dict[str, Any]]) -> None:
        """Hydrate the context slice from a persisted dict (inverse of
        ``to_persistable_state``). Fail-safe + backward-compatible: ``None`` or a
        missing/legacy key leaves the corresponding field at its default, so a
        context with no persisted state behaves exactly as before. #953.
        """
        if not state:
            return
        lens_stack = state.get("lens_stack")
        if isinstance(lens_stack, list):
            self.lens_stack = [str(x) for x in lens_stack]
        offer = state.get("last_offer")
        if isinstance(offer, dict) and offer.get("continuation_hint") is not None:
            self.last_offer = LastOffer(
                offer_type=offer.get("offer_type", "contextual"),
                continuation_hint=offer.get("continuation_hint", ""),
                offer_text=offer.get("offer_text", ""),
            )
        elif offer is None and "last_offer" in state:
            self.last_offer = None
        if "last_response_was_floor" in state:
            self.last_response_was_floor = bool(state.get("last_response_was_floor"))
        if "last_floor_category" in state:
            self.last_floor_category = state.get("last_floor_category")
        if "ftux_interview_answer" in state:  # #1688; legacy states lack the key
            answer = state.get("ftux_interview_answer")
            self.ftux_interview_answer = str(answer) if answer is not None else None

    # ---- Lens stack operations (#763 Phase 4) ----

    def push_lens(self, lens: str) -> None:
        """Push the current lens onto the stack before a sub-topic digression."""
        current = self.current_lens
        if current and current != lens:
            self.lens_stack.append(current)

    def pop_lens(self) -> Optional[str]:
        """Pop the most recent lens from the stack (returning from a digression)."""
        return self.lens_stack.pop() if self.lens_stack else None

    def reset_lens(self) -> None:
        """Clear the lens stack entirely (explicit topic change)."""
        self.lens_stack.clear()

    @property
    def last_turn(self) -> Optional[ConversationTurn]:
        """Get the most recent turn."""
        return self.turns[-1] if self.turns else None

    @property
    def last_intent(self) -> Optional[Intent]:
        """Get the intent from the most recent turn."""
        return self.last_turn.intent if self.last_turn else None

    @property
    def last_temporal_reference(self) -> Optional[str]:
        """Get the most recent temporal reference.

        NOTE: Not yet called in production. Reserved for future temporal
        reference resolution in follow-up handling. (Audit: #827, 2026-02-18)
        """
        for turn in reversed(self.turns):
            if turn.temporal_reference:
                return turn.temporal_reference
        return None

    @property
    def last_topic(self) -> Optional[str]:
        """Get the most recent topic."""
        for turn in reversed(self.turns):
            if turn.topic:
                return turn.topic
        return None

    @property
    def current_lens(self) -> Optional[str]:
        """Get the current conversational lens from the most recent turn with one."""
        for turn in reversed(self.turns):
            if turn.lens:
                return turn.lens
        return None

    @property
    def is_active(self) -> bool:
        """Check if there's an active conversation."""
        if not self.turns:
            return False
        return self.last_turn.age_seconds < (self.max_age_minutes * 60)


# Follow-up phrase patterns
FOLLOW_UP_PATTERNS: dict[FollowUpType, list[str]] = {
    FollowUpType.TEMPORAL_SHIFT: [
        r"^how about (today|tomorrow|yesterday|this week|next week|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\??$",
        r"^what about (today|tomorrow|yesterday|this week|next week|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\??$",
        r"^and (today|tomorrow|yesterday|this week|next week|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\??$",
        r"^(today|tomorrow|yesterday|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\??$",  # Single word temporal
    ],
    FollowUpType.CONFIRMATION: [
        r"^(yes|yeah|yep|yup|sure|ok|okay|alright|sounds good|perfect|great)\.?$",
        r"^(no|nope|nah|not really|never mind|cancel)\.?$",
    ],
    FollowUpType.ENTITY_REFERENCE: [
        r"^(that one|the first one|the second one|the last one)\.?$",
        r"^what about (that|this|it|them)\??$",
        r"^tell me more( about (that|it|this))?\??$",
    ],
    FollowUpType.REFINEMENT: [
        r"^just (the|my) (morning|afternoon|evening|work|personal) (ones?|meetings?|tasks?)\.?$",
        r"^only (the|my) (urgent|important|priority) (ones?|items?)\.?$",
        r"^(filter|show) (only|just) .+$",
    ],
    FollowUpType.CONTINUATION: [
        r"^(and|what else|anything else|more|continue)\??$",
        r"^go on\.?$",
        r"^keep going\.?$",
    ],
    FollowUpType.NEGATION: [
        r"^not (that|those|this|it)\.?$",
        r"^something else\.?$",
        r"^different (one|ones)\.?$",
    ],
}


def detect_follow_up(
    message: str,
    context: ConversationContext,
) -> Optional[tuple[FollowUpType, dict[str, Any]]]:
    """
    Detect if a message is a conversational follow-up.

    Args:
        message: The user's message
        context: The conversation context

    Returns:
        Tuple of (follow_up_type, extracted_data) or None if not a follow-up
    """
    import re

    if not context.is_active:
        return None

    clean_msg = message.strip().lower()

    # Check each follow-up type
    for follow_up_type, patterns in FOLLOW_UP_PATTERNS.items():
        for pattern in patterns:
            match = re.match(pattern, clean_msg, re.IGNORECASE)
            if match:
                extracted = {"groups": match.groups() if match.groups() else []}

                # Extract specific data based on type
                if follow_up_type == FollowUpType.TEMPORAL_SHIFT:
                    # Extract the new temporal reference
                    if match.groups():
                        extracted["new_temporal"] = match.group(1)

                return (follow_up_type, extracted)

    return None


def resolve_follow_up(
    follow_up_type: FollowUpType,
    extracted_data: dict[str, Any],
    context: ConversationContext,
) -> Optional[Intent]:
    """
    Resolve a follow-up into a concrete intent by inheriting from context.

    Args:
        follow_up_type: The type of follow-up detected
        extracted_data: Data extracted from the follow-up message
        context: The conversation context

    Returns:
        A resolved Intent that inherits from context, or None if unresolvable
    """
    last_intent = context.last_intent
    if not last_intent:
        return None

    # #763: Inherit lens from context for all follow-up types
    current_lens = context.current_lens

    if follow_up_type == FollowUpType.TEMPORAL_SHIFT:
        # Inherit the intent category and action, but update temporal context
        new_temporal = extracted_data.get("new_temporal")
        if new_temporal and last_intent:
            # Create a new intent with updated temporal reference
            return Intent(
                category=last_intent.category,
                action=last_intent.action,
                confidence=0.9,  # Slightly lower confidence for inferred intent
                context={
                    **(last_intent.context or {}),
                    "temporal_reference": new_temporal,
                    "inherited_from": str(context.last_turn.id) if context.last_turn else None,
                    "follow_up_type": follow_up_type.value,
                    "inherited_lens": current_lens,
                },
            )

    elif follow_up_type == FollowUpType.CONFIRMATION:
        # Return a confirmation intent with the original context
        return Intent(
            category=IntentCategory.CONVERSATION,
            action="confirmation",
            confidence=1.0,
            context={
                "confirmed_intent": last_intent.action if last_intent else None,
                "original_message": context.last_turn.message if context.last_turn else None,
                "inherited_lens": current_lens,
            },
        )

    elif follow_up_type == FollowUpType.CONTINUATION:
        # Return a continuation intent
        return Intent(
            category=last_intent.category if last_intent else IntentCategory.CONVERSATION,
            action="continue_previous",
            confidence=0.9,
            context={
                "previous_intent": last_intent.action if last_intent else None,
                "previous_topic": context.last_topic,
                "inherited_lens": current_lens,
            },
        )

    elif follow_up_type == FollowUpType.NEGATION:
        # Return a negation/change intent
        return Intent(
            category=IntentCategory.CONVERSATION,
            action="change_selection",
            confidence=0.9,
            context={
                "rejected_intent": last_intent.action if last_intent else None,
                "inherited_lens": current_lens,
            },
        )

    return None


def extract_temporal_reference(message: str) -> Optional[str]:
    """
    Extract temporal references from a message.

    Args:
        message: The user's message

    Returns:
        The temporal reference (e.g., "today", "tomorrow") or None
    """
    import re

    temporal_patterns = [
        (r"\b(today)\b", "today"),
        (r"\b(tomorrow)\b", "tomorrow"),
        (r"\b(yesterday)\b", "yesterday"),
        (r"\b(this week)\b", "this_week"),
        (r"\b(next week)\b", "next_week"),
        (r"\b(last week)\b", "last_week"),
        (r"\b(this month)\b", "this_month"),
        (r"\b(next month)\b", "next_month"),
        (r"\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", None),  # Day name
    ]

    clean_msg = message.lower()
    for pattern, replacement in temporal_patterns:
        match = re.search(pattern, clean_msg, re.IGNORECASE)
        if match:
            return replacement or match.group(1).lower()

    return None


def extract_topic(message: str, intent: Optional[Intent] = None) -> Optional[str]:
    """
    Extract the topic from a message.

    Args:
        message: The user's message
        intent: The classified intent (if available)

    Returns:
        The topic or None
    """
    # Topic inference based on intent category
    topic_by_category = {
        IntentCategory.QUERY: "information",
        IntentCategory.TEMPORAL: "time",
        IntentCategory.STATUS: "status",
        IntentCategory.PRIORITY: "priorities",
        IntentCategory.EXECUTION: "action",
    }

    if intent:
        # Use action as topic if specific
        if intent.action and intent.action not in ["get", "list", "query"]:
            return intent.action

        # Fall back to category-based topic
        return topic_by_category.get(intent.category)

    return None


# Session storage (in-memory for now, can be backed by Redis/DB later)
_conversation_contexts: dict[str, ConversationContext] = {}


def _context_key(session_id: str, user_id: Optional[str] = None) -> str:
    """Build composite key for user-scoped context storage (#817)."""
    return f"{user_id or 'anonymous'}:{session_id}"


def get_or_create_context(
    session_id: str,
    user_id: Optional[str] = None,
) -> ConversationContext:
    """
    Get or create a conversation context for a session.

    Args:
        session_id: The session identifier
        user_id: Optional user identifier (#817: used for scoped storage key)

    Returns:
        The conversation context
    """
    key = _context_key(session_id, user_id)
    if key not in _conversation_contexts:
        # Defensive UUID parsing — session_id may not be a valid UUID
        # (e.g., "default_session" for unauthenticated users)
        try:
            parsed_session = UUID(session_id) if session_id else uuid4()
        except (ValueError, AttributeError):
            parsed_session = uuid4()

        try:
            parsed_user = UUID(user_id) if user_id else None
        except (ValueError, AttributeError):
            parsed_user = None

        _conversation_contexts[key] = ConversationContext(
            session_id=parsed_session,
            user_id=parsed_user,
        )
    return _conversation_contexts[key]


def clear_context(session_id: str, user_id: Optional[str] = None) -> None:
    """Clear the conversation context for a session.

    NOTE: Not yet called in production. Reserved for explicit session cleanup
    (e.g., logout, session timeout). (Audit: #827, 2026-02-18)
    """
    key = _context_key(session_id, user_id)
    if key in _conversation_contexts:
        del _conversation_contexts[key]


def build_recent_history(
    session_id: Optional[str],
    user_id: Optional[str] = None,
    *,
    max_turns: int = 6,
    exclude_in_flight: bool = True,
) -> list[dict[str, str]]:
    """Build role/content conversation history for LLM prompts (#1122).

    The single shared history source for the floor's "Recent conversation"
    block and slot-filling antecedent resolution — replaces 7 hand-copied
    builder blocks that had drifted (two carried a positional `turns[:-1]`
    exclusion that silently dropped the latest prior turn whenever the
    current turn hadn't been recorded yet).

    The in-flight turn (the message currently being processed) is identified
    by `response is None` — every completed turn gets its response set in
    process_intent's outer flow — NOT by list position. A failed turn (never
    got a response) is therefore also excluded; acceptable, since its
    response-less record can't ground an antecedent the user saw.
    """
    if not session_id:
        return []
    history: list[dict[str, str]] = []
    try:
        conv_ctx = get_or_create_context(str(session_id), user_id=str(user_id) if user_id else None)
        turns = list(conv_ctx.turns)
        if exclude_in_flight and turns and turns[-1].response is None:
            turns = turns[:-1]
        for turn in turns[-max_turns:]:
            if turn.message:
                history.append({"role": "user", "content": turn.message})
            if turn.response:
                history.append({"role": "assistant", "content": turn.response})
    except Exception as e:  # silent-ok: degrades to no-history, but LOGGED — silently empty history is the floor-amnesia shape (#1596); the LLM loses the whole conversation with no trace (#1423 3b)
        logger.warning("conversation_history_assembly_failed", error=str(e))
        return []
    return history


# #1532 F3: local sentinel mirroring conversation_manager.UNSCOPED_PRINCIPAL
# (not imported — the manager is handed in as an argument precisely so this
# module never imports it). Distinguishes "principal not threaded" (legacy
# 3-arg callers → manager's unscoped shim) from user_id=None (anonymous,
# enforced against owned rows).
_UNSCOPED_PRINCIPAL = object()


async def hydrate_turns_from_db(
    conv_ctx: ConversationContext,
    conversation_manager,
    session_id: str,
    user_id=_UNSCOPED_PRINCIPAL,
) -> bool:
    """Backfill the in-memory turn window from persisted turns (#1122).

    The in-memory registry is process-local: it starts empty on server
    restart and after the 30-minute prune, while `conversation_turns` (the
    DB, written via ConversationManager #563) durably holds every completed
    turn. Without this backfill the floor and slot-filling see an empty
    history for any resumed conversation — the root cause behind the
    "the doc"/"that one" antecedent failures.

    Companion to the #953 Layer-4 hydration (lens_stack/last_offer/floor
    flags), which restores conversation *state*; this restores the *turns*.
    Called when the in-memory window is empty; cheap no-op when the DB has
    nothing. Returns True if any turns were backfilled.

    This is THE single mapping point between the domain ConversationTurn
    (user_message/assistant_response, system of record) and the
    working-state turn (message/response) — #1207. Don't add others.

    #1532 F3: ``user_id`` is the requesting principal, threaded through to the
    manager's ownership-checked read — hydrating another principal's session id
    backfills NOTHING (the manager treats an owner mismatch as not-found).
    """
    if conv_ctx.turns or conversation_manager is None:
        return False
    try:
        if user_id is _UNSCOPED_PRINCIPAL:
            persisted_turns = await conversation_manager.get_recent_turns(
                session_id, limit=conv_ctx.max_turns
            )
        else:
            persisted_turns = await conversation_manager.get_recent_turns(
                session_id, limit=conv_ctx.max_turns, user_id=user_id
            )
        for t in persisted_turns or []:
            msg = getattr(t, "user_message", None)
            if not msg:
                continue
            turn = conv_ctx.add_turn(message=msg)
            turn.response = getattr(t, "assistant_response", None)
        return bool(conv_ctx.turns)
    except Exception as e:  # silent-ok: #1423 — hydration stays best-effort (never block the turn), but the failure is now logged: this was a ZERO-telemetry swallow, and a hydration failure is exactly the "the doc"/"that one" antecedent-loss failure this function exists to prevent
        logger.warning(
            "turn_hydration_from_db_failed — resumed conversation will see an EMPTY "
            "history this turn (antecedents like 'the doc' will not resolve)",
            session_id=session_id,
            error=str(e),
            exc_info=True,
        )
        return False
