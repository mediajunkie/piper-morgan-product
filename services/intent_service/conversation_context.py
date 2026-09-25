"""
Discourse Working State (#427 MUX-IMPLEMENT-CONVERSE-MODEL)

Tracks conversational state to enable:
- Context-dependent phrase resolution
- Turn-by-turn memory within a session

(#1768, 2026-09-12: the rule-based follow-up detectors — FollowUpType,
FOLLOW_UP_PATTERNS, detect_follow_up, resolve_follow_up — and the
extract_temporal_reference/extract_topic annotators were deleted with their
sole caller, classify_conscious. The lens stack push/pop/reset trio went with
them.)

(#1863, 2026-09-23, Rule-0 rip, Arch GO: the writer-less lens surface —
ConversationTurn.lens, ConversationContext.current_lens, ConversationContext.
lens_stack (incl. its #953 persisted slice), and the small-fry
ConversationTurn.temporal_reference/topic/entity_references +
ConversationContext.last_temporal_reference — were deleted outright. No
writer ever existed for any of them post-#1768: the only producer was
classify_conscious's follow-up annotators, already gone. The #820
soft-invocation read and the #822 lens/workflow affinity boost (which failed
closed on the always-None value) were removed with their source. Design
record: docs/internal/architecture/design-records/
design-record-lens-surface-rip-1863-2026-09-23.md. Existing DB rows may still
carry the legacy lens_stack/current_lens keys inside the layer4_state JSONB
blob — apply_persisted_state's isinstance guard ignores unknown keys, pinned
by tests/unit/services/intent_service/
test_layer4_hydration_ignores_legacy_lens_keys_1863.py. No migration.)

Design principle: "Intent inherits from context when ambiguous"

The 10-turn context window (per PM-034) enables natural conversation
without surveillance-level tracking.

Architecture (#1207 unification, 2026-06-12 — where this module sits):
- This module's ``ConversationContext`` is the in-process **discourse
  working state** — a per-(user, session) PROJECTION the classifier/floor
  read and annotate (recent-turn window, last offer, floor flags,
  provenance sidecar). It is NOT the domain Conversation aggregate
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
from typing import Any, Optional
from uuid import UUID, uuid4

import structlog

from services.domain.models import Intent
from services.intent_service.list_remainder import ListRemainder

logger = structlog.get_logger()


@dataclass
class LastOffer:
    """Tracks the most recent contextual offer for continuation detection (#852).

    When Piper makes a contextual offer ("Would you like me to explain more?"),
    this stores the continuation hint so the next turn's classifier knows what
    "yes" refers to. One-turn memory — cleared on every new turn regardless.

    Bright-line rule (Chief Architect): If "yes" invokes a named workflow,
    it arms the #846 pending-offer store (``WorkflowOffer`` /
    ``set_pending_offer``). If "yes" means "continue/elaborate," use this.

    #1855 (Arch ruling, 2026-09-23): the reserved never-built ``offer_type``
    value was DELETED rather than built. It was never instantiated, never set and
    never checked — a reservation for a property the #846 store already owns
    cleanly. Building the adapter would have created a SECOND independently-
    truthful answer to "is anything armed this turn," and two such stores drift.
    One authority, not two. (Live values: ``"contextual"`` — the #852 default —
    and ``"process_resume"``, the #889/#1769 resume rail.)
    """

    offer_type: str
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

    @property
    def age_seconds(self) -> float:
        """How old this turn is in seconds."""
        return (datetime.now() - self.timestamp).total_seconds()


@dataclass
class ConversationContext:
    """
    Tracks the conversational context for a session.

    Maintains a sliding window of recent turns to enable:
    - Reference resolution
    - Intent inheritance
    """

    session_id: UUID = field(default_factory=uuid4)
    user_id: Optional[UUID] = None
    turns: list[ConversationTurn] = field(default_factory=list)
    max_turns: int = 10  # PM-034: 10-turn context window
    max_age_minutes: int = 30  # Conversations older than 30 min are stale

    # Issue #852: Track last contextual offer for continuation detection
    last_offer: Optional[LastOffer] = None

    # Issue #913: Track whether last response was a floor hit (continuation rate)
    last_response_was_floor: bool = False
    last_floor_category: Optional[str] = None

    # Issue #953: one-shot guard so the async floor path hydrates persisted
    # Layer-4 state (last_offer + floor flags) from the DB exactly
    # once per in-memory context lifetime (on resume / restart). Not persisted,
    # not part of equality (compare=False).
    _hydrated: bool = field(default=False, compare=False, repr=False)

    # #1688: the FTUX empty-state interview's bound answer -- session-scoped
    # working state, set at the offer seam (first_contact.handle_ftux_
    # interview_turn) and surfaced to the floor via the context assembler.
    # WITHIN-SESSION use only: cross-session recall is #1705 (Leg D
    # increment 6) and does not exist; no surface may claim otherwise.
    ftux_interview_answer: Optional[str] = None

    # #1762 (epic 6): the unrendered tail of the most recent capped list, so
    # "…and N more" is a claim we can CASH (GatherOutcome §5b). DELIBERATELY
    # NOT the ``last_offer`` rail above: that rail is always-cleared at turn
    # start (the #852 one-turn invariant), which is exactly the property the
    # #1770 no-clobber peek's soundness rests on — and a capped-list offer is
    # the kind users answer LATE (CXO 2026-09-13), so it needs a lifetime the
    # rail must not grow. Own store, own lifetime, rail untouched.
    #
    # Survival form, stated (CXO's per-tier ruling, READ × PRIVATE →
    # LOW_CEREMONY): PERSISTING — it survives arbitrary intervening turns
    # until cashed, declined, replaced by a newer capped list, or stale past
    # REMAINDER_MAX_AGE_MINUTES. Admissible because cashing FIRES NOTHING: it
    # prints lines already gathered. Not persisted across process restart
    # (#953 hydration untouched); a lost remainder degrades to the honest
    # "that list has moved" turn, never a silent re-fetch.
    pending_list_remainder: Optional[ListRemainder] = None

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
    ) -> ConversationTurn:
        """
        Add a new turn to the conversation.

        Automatically prunes old turns to maintain the context window.
        """
        turn = ConversationTurn(
            message=message,
            intent=intent,
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
    # restart/refresh: last_offer + the floor-continuation flags. NOT turns
    # (persisted via ConversationRepository/ConversationTurnDB) and NOT
    # turn_provenance (persisted to ConversationTurnDB.metadata, #1030 R4). These
    # (de)serialize the slice for the ConversationDB.context JSONB column; the
    # async persist/hydrate wiring at the floor seam is the companion increment.
    #
    # #1863 (2026-09-23): lens_stack was dropped from this slice — it had no
    # writer anywhere in production (see module docstring). Existing DB rows
    # may still carry a legacy "lens_stack" key inside layer4_state;
    # apply_persisted_state below simply no longer reads it (isinstance-guard
    # pattern below already treats unknown/legacy keys as no-ops — pinned in
    # test_layer4_hydration_ignores_legacy_lens_keys_1863.py). No migration.

    def to_persistable_state(self) -> dict[str, Any]:
        """Serialize the restart-fragile context slice to a JSON-safe dict.

        Round-trips with ``apply_persisted_state``. Excludes turns + provenance
        (persisted elsewhere). #953.
        """
        return {
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
            # #1784 (Lead ruling, 2026-09-24, option 1 — the cheap tombstone):
            # ``pending_list_remainder`` is in-process only (list_remainder.py
            # module docstring), so a restart/eviction makes it ABSENT, not
            # stale, and the #1762 consume seam silently falls through instead
            # of giving the §5b-i honest "that list has moved" turn. Persist
            # ONLY the tombstone fields — kind/shown/held_total/
            # source_total_display/armed_at — NEVER the item ``lines``. A
            # hydrated tombstone always carries an empty ``lines`` tuple, which
            # is exactly what makes ``_check_pending_list_remainder``'s
            # existing ``not remainder.lines`` guard take the render_moved
            # branch on its own — no new branching logic, and no path that
            # could ever cash a tombstone.
            "pending_list_remainder": (
                {
                    "kind": self.pending_list_remainder.kind,
                    "shown": self.pending_list_remainder.shown,
                    "held_total": self.pending_list_remainder.held_total,
                    "source_total_display": self.pending_list_remainder.source_total_display,
                    "armed_at": self.pending_list_remainder.armed_at.isoformat(),
                }
                if self.pending_list_remainder is not None
                else None
            ),
        }

    def apply_persisted_state(self, state: Optional[dict[str, Any]]) -> None:
        """Hydrate the context slice from a persisted dict (inverse of
        ``to_persistable_state``). Fail-safe + backward-compatible: ``None`` or a
        missing/legacy key leaves the corresponding field at its default, so a
        context with no persisted state behaves exactly as before. #953.
        """
        if not state:
            return
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
        # #1784: hydrate the tombstone. ``lines=()`` and ``offer_text=""`` are
        # deliberate, not omissions — the persisted dict never carried item
        # lines to restore, and ``offer_text`` is unused at the LOW_CEREMONY
        # tier every #1762 arm site declares (``evaluate_acceptance`` only
        # consults ``armed_question`` at NAMED_OBJECT), so there is nothing
        # honest to reconstruct it from. A hydrated tombstone therefore can
        # only ever reach ``render_moved`` at the consume seam, never
        # ``render_cash`` — see ``_check_pending_list_remainder``'s
        # ``not remainder.lines`` guard.
        if "pending_list_remainder" in state:
            remainder_state = state.get("pending_list_remainder")
            if isinstance(remainder_state, dict) and remainder_state.get("kind"):
                try:
                    armed_at = datetime.fromisoformat(remainder_state["armed_at"])
                except (KeyError, TypeError, ValueError):
                    # Malformed/missing timestamp: fail toward STALE, never
                    # toward an arm that looks freshly made this turn.
                    armed_at = datetime.min
                self.pending_list_remainder = ListRemainder(
                    kind=str(remainder_state.get("kind", "")),
                    shown=int(remainder_state.get("shown") or 0),
                    held_total=int(remainder_state.get("held_total") or 0),
                    source_total_display=str(remainder_state.get("source_total_display", "")),
                    lines=(),
                    offer_text="",
                    armed_at=armed_at,
                )
            else:
                self.pending_list_remainder = None

    @property
    def last_turn(self) -> Optional[ConversationTurn]:
        """Get the most recent turn."""
        return self.turns[-1] if self.turns else None

    @property
    def last_intent(self) -> Optional[Intent]:
        """Get the intent from the most recent turn."""
        return self.last_turn.intent if self.last_turn else None

    @property
    def is_active(self) -> bool:
        """Check if there's an active conversation."""
        if not self.turns:
            return False
        return self.last_turn.age_seconds < (self.max_age_minutes * 60)


# #1768 (2026-09-12): FOLLOW_UP_PATTERNS, detect_follow_up, resolve_follow_up,
# extract_temporal_reference, and extract_topic were deleted here — their sole
# production caller was classify_conscious (deleted in the same commit).
#
# #1863 (2026-09-23): the fields those annotators would have populated —
# ConversationTurn.temporal_reference/topic/entity_references and
# ConversationContext.last_temporal_reference/last_topic — were deleted too:
# stored-never-populated since the annotators went, zero readers outside this
# module. Same cut as the lens surface above.


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

    Companion to the #953 Layer-4 hydration (last_offer/floor flags), which
    restores conversation *state*; this restores the *turns*.
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
