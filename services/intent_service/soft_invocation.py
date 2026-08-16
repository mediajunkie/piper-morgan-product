"""
Soft workflow invocation from natural language.

Issue #767: GLUE-SOFTINVOKE — Detect implied workflow needs in natural
conversation and offer relevant capabilities softly.

Instead of requiring explicit commands ("/standup", "start project setup"),
this module detects natural expressions of need and generates soft offers:

    User: "I need to get the team together Tuesday"
    Piper: [normal response] + "I could help set up a meeting. Want me to find a time?"

Architecture:
- SoftInvocationDetector: Pattern-based detection of implied workflow needs
- WorkflowOffer: Data model for a soft offer
- SoftInvocationResult: Detection result with throttle info
- WorkflowOfferService: Offer generation, formatting, throttling via ProactivityGate
"""

import re
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import structlog

from services.domain.models import Intent
from services.personality.formality import formality_label
from services.trust.proactivity_gate import ProactivityGate, TrustStage

logger = structlog.get_logger(__name__)

# --- Constants ---

# Maximum offers per exchange window (requirement: max 2 per 5 exchanges)
MAX_OFFERS_PER_WINDOW = 2
EXCHANGE_WINDOW_SIZE = 5


# --- Data Models ---


@dataclass(frozen=True)
class WorkflowOffer:
    """A soft offer to start a workflow."""

    workflow_type: str  # e.g., "meeting", "standup", "project_setup", "status_check"
    offer_message: str  # "I could help set up a meeting. Want me to find a time?"
    decline_message: str  # "No worries, just let me know if you change your mind."
    confidence: float  # Pattern match confidence (0.0-1.0)
    trigger_pattern: str = ""  # Which pattern group matched


@dataclass
class SoftInvocationResult:
    """Result of soft invocation detection."""

    has_offer: bool
    offer: Optional[WorkflowOffer] = None
    throttled: bool = False  # True if offer was suppressed
    reason: str = ""  # Why offer was/wasn't generated


@dataclass
class OfferWindow:
    """Tracks offers within a sliding exchange window."""

    offer_turns: List[int] = field(default_factory=list)  # Turn numbers with offers

    def count_in_window(self, current_turn: int) -> int:
        """Count offers in the last EXCHANGE_WINDOW_SIZE turns."""
        window_start = max(0, current_turn - EXCHANGE_WINDOW_SIZE)
        return sum(1 for t in self.offer_turns if t >= window_start)

    def record_offer(self, turn: int) -> None:
        """Record that an offer was made at this turn."""
        self.offer_turns.append(turn)


# --- Pattern Definitions ---

# Each entry: (compiled patterns, workflow_type, offer_messages_by_tier, decline_messages_by_tier)
# Patterns are intentionally conservative to avoid false positives.
# Message dicts map formality tier ("warm", "balanced", "professional") to text.

_SOFT_TRIGGER_PATTERNS: List[Tuple[List[re.Pattern], str, Dict[str, str], Dict[str, str]]] = []


def _compile_patterns() -> List[Tuple[List[re.Pattern], str, Dict[str, str], Dict[str, str]]]:
    """Compile pattern definitions. Called once at module load."""
    raw = [
        # Meeting / scheduling needs
        (
            [
                r"\b(?:i need to|we need to|should|let'?s)\b.*\b(?:get\b.*\btogether|meet|sync up|catch up|huddle)\b",
                r"\b(?:i need to|we need to|should|let'?s)\b.*\b(?:schedule|set up|plan)\b.*\b(?:meeting|call|sync)\b",
                r"\bwe should\b.*\b(?:talk about|discuss|go over)\b",
                r"\b(?:can someone|can we|could we)\b.*\b(?:meet|get\b.*\btogether|sync)\b",
                # Issue #844: Implied meeting needs with team discussion
                r"\b(?:i need to|we need to|should)\b.*\b(?:discuss|talk about|go over)\b.*\bwith (?:the team|everyone)\b",
            ],
            "meeting",
            {
                "warm": "I could help set up a meeting! Want me to find a time?",
                "balanced": "I could help set up a meeting. Want me to find a time?",
                "professional": "I can schedule a meeting. Shall I check availability?",
            },
            {
                "warm": "No worries, just let me know if you change your mind!",
                "balanced": "No worries, just let me know if you change your mind.",
                "professional": "Understood. Let me know if you'd like to revisit.",
            },
        ),
        # Project organization / structure needs
        (
            [
                r"\b(?:this|the) project is (?:getting|becoming)\b.*\b(?:complicated|messy|disorganized|unwieldy|out of hand)\b",
                r"\b(?:i need to|we need to|help me)\b.*\b(?:organize|structure|plan out)\b",
                r"\bthings are (?:getting|becoming)\b.*\b(?:complicated|messy|scattered|disorganized)\b",
                r"\b(?:i don'?t know|not sure)\b.*\b(?:where to start|how to organize|how to structure)\b",
                # Issue #850: "lost track" / "lost sight of" / "fallen behind on"
                r"\bi'?ve (?:lost track|lost sight)\b.*\bof\b",
                r"\bi'?ve (?:fallen behind|gotten behind)\b.*\bon\b",
            ],
            "project_setup",
            {
                "warm": "I could help organize things! Want to set up some structure?",
                "balanced": "I could help organize things. Want to set up some structure?",
                "professional": "I can help establish project structure. Shall I draft an outline?",
            },
            {
                "warm": "Got it, no worries! I'm here if you need help later.",
                "balanced": "Got it, no worries. I'm here if you need help later.",
                "professional": "Understood. I'm available when you're ready.",
            },
        ),
        # Status / deadline concerns
        (
            [
                r"\b(?:i'?m worried|i'?m concerned|worried|nervous)\b.*\b(?:deadline|timeline|schedule|behind|late)\b",
                r"\b(?:i don'?t know|not sure)\b.*\b(?:where (?:things|we) stand|progress|how (?:things|we) are doing)\b",
                r"\bare we (?:on track|behind|going to make)\b",
                r"\bhow (?:are things|is the project|are we)\b.*\b(?:going|progressing|looking)\b",
                # Issue #850: "will we finish on time" / "will we make it by..."
                r"\bwill we (?:finish|make it|be (?:done|ready))\b.*\b(?:on time|by|before|in time)\b",
            ],
            "status_check",
            {
                "warm": "I can pull up the project status so we can see where things stand! Want me to?",
                "balanced": "Want me to pull up the project status so we can see where things stand?",
                "professional": "Shall I compile a status summary?",
            },
            {
                "warm": "No problem! Just ask whenever you want an update.",
                "balanced": "No problem. Just ask whenever you want an update.",
                "professional": "Understood. Status reports are available on request.",
            },
        ),
        # Team alignment / standup needs
        (
            [
                r"\b(?:the team needs|we need)\b.*\b(?:alignment|to be aligned|to sync|coordination)\b",
                r"\b(?:everyone|the team|people) (?:seems?|are|is)\b.*\b(?:out of sync|disconnected|not aligned|on different pages)\b",
                r"\bwe should (?:do|have|start)\b.*\b(?:standup|check-in|daily sync)\b",
                # Issue #844: Personal agency + team alignment expressions
                r"\bi (?:really )?(?:need to|want to|gotta|have to)\b.*\b(?:get )?(?:the team|everyone|people)\b.*\b(?:aligned|in sync|on the same page|coordinated|together)\b",
                r"\b(?:i need to|we need to|should)\b.*\b(?:make sure|ensure)\b.*\b(?:everyone|the team|people)\b.*\b(?:aligned|in sync|on the same page|coordinated)\b",
            ],
            "standup",
            {
                "warm": "A standup could help with that! Want me to start one?",
                "balanced": "A standup could help with that. Want me to start one?",
                "professional": "A standup may address this. Shall I initiate one?",
            },
            {
                "warm": "Sure thing! Let me know if you change your mind.",
                "balanced": "Sure thing. Let me know if you change your mind.",
                "professional": "Understood. Let me know if you'd like to reconsider.",
            },
        ),
        # Review / feedback needs
        (
            [
                r"\b(?:can someone|could someone|someone needs to|need someone to)\b.*\b(?:review|look at|check|give feedback)\b",
                r"\b(?:i need|we need)\b.*\b(?:feedback|review|second opinion|another set of eyes)\b",
                # Issue #850: "another pair of eyes" / "another set of eyes" / "another look"
                r"\b(?:needs?|could use|wants?)\b.*\b(?:another (?:pair of eyes|set of eyes|look)|a (?:second|fresh) (?:look|pair of eyes))\b",
                # Issue #850: "could use some feedback" / "would love feedback"
                r"\b(?:could use|would (?:love|appreciate|like))\b.*\b(?:some )?(?:feedback|input|review)\b",
                # Issue #850: "can this get another look" / "get a look at this"
                r"\b(?:can|could)\b.*\b(?:this|it|that)\b.*\bget\b.*\b(?:another look|a (?:look|review|check))\b",
            ],
            "review",
            {
                "warm": "I could help coordinate a review! Want me to set that up?",
                "balanced": "I could help coordinate a review. Want me to set that up?",
                "professional": "I can coordinate a review. Shall I arrange it?",
            },
            {
                "warm": "No worries, just let me know when you're ready!",
                "balanced": "No worries, just let me know when you're ready.",
                "professional": "Understood. Let me know when you'd like to proceed.",
            },
        ),
        # Priority / focus needs
        (
            [
                r"\b(?:i don'?t know|not sure)\b.*\b(?:what to (?:focus on|work on|prioritize)|my priorities)\b",
                r"\b(?:too many|so many)\b.*\b(?:things|tasks|priorities|items)\b.*\b(?:to do|going on|happening)\b",
                r"\bwhat should i\b.*\b(?:focus on|work on|do (?:first|next))\b",
                # Issue #850: Emotional overwhelm expressions
                r"\bi'?m (?:so |really )?(?:overwhelmed|drowning|swamped|buried|underwater)\b",
                r"\beverything (?:feels|seems|is)\b.*\b(?:urgent|pressing|a priority|on fire)\b",
            ],
            "priority_check",
            {
                "warm": "I can help sort out priorities! Want me to take a look at what's on your plate?",
                "balanced": "I can help sort out priorities. Want me to take a look at what's on your plate?",
                "professional": "I can help prioritize. Shall I review your current workload?",
            },
            {
                "warm": "Okay, just let me know when you want to dig in!",
                "balanced": "Okay, just let me know when you want to dig in.",
                "professional": "Understood. I'm available when you're ready to review.",
            },
        ),
        # Reminder / tracking needs
        (
            [
                r"\bi keep forgetting\b.*\b(?:to|about)\b",
                r"\bi always forget\b.*\b(?:to|about)\b",
                r"\b(?:i need to|don'?t let me forget to)\b.*\b(?:remember|follow up|check back)\b",
            ],
            "reminder",
            {
                "warm": "I can help you keep track of that! Want me to set a reminder?",
                "balanced": "I can help you keep track of that. Want me to set a reminder?",
                "professional": "I can set a reminder for that. Shall I?",
            },
            {
                "warm": "No problem! Just mention it again if you need a nudge.",
                "balanced": "No problem. Just mention it again if you need a nudge.",
                "professional": "Understood. Feel free to mention it again if needed.",
            },
        ),
    ]

    compiled = []
    for patterns, workflow_type, offer_msgs, decline_msgs in raw:
        compiled_patterns = [re.compile(p, re.IGNORECASE) for p in patterns]
        compiled.append((compiled_patterns, workflow_type, offer_msgs, decline_msgs))
    return compiled


_SOFT_TRIGGER_PATTERNS = _compile_patterns()

# --- #1631: prose-shape override ---

# A turn at/above this length (or any multi-line turn) is free-text prose
# regardless of how it opens — never an offer response. The unanchored
# accept/decline rows below ("^(?:yes|yeah|sure|please|go ahead),?\s",
# "\bnot today\b") match into long prose, so without a shape check a long
# reply to ANY armed offer — consent check, destructive confirm,
# verification read-back, soft workflow offer — could accept or decline it
# off a substring ("Please note that we should not delete this yet, not
# today anyway, because…"). Genuine accepts/declines are short and
# single-line; the floor sits well above every taught confirm phrase and
# well below real composed prose. First shipped for the drafted_issue kind
# in #1627 (drafted_issue.is_body_prose_answer), lifted here for every kind
# by #1631 — one seam, one threshold, no drift.
PROSE_LENGTH_FLOOR = 160


def is_prose_reply(message: str) -> bool:
    """#1631 — True when a turn is prose by shape: multi-line, or at/above
    ``PROSE_LENGTH_FLOOR`` characters. Callers pass stripped text."""
    return "\n" in message or len(message) >= PROSE_LENGTH_FLOOR


# Accept/decline detection patterns
ACCEPT_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"^(?:yes|yeah|yep|yup|sure|please|okay|ok|go ahead|do it|let'?s do it|sounds good|sounds great|that would be great|please do|yes please)\.?!?$",
        r"^(?:yes|yeah|sure|please|go ahead),?\s",
        r"\byes,?\s*(?:please|go ahead|do it|that would)\b",
        r"\bsure,?\s*(?:let'?s|go ahead|please)\b",
    ]
]

DECLINE_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"^(?:no|nah|nope|not now|not right now|never mind|i'?m good|no thanks|no thank you|just venting|skip)\.?!?$",
        r"^(?:no|nah),?\s",
        r"\b(?:not (?:now|right now|yet|today)|maybe later|i'?m (?:good|fine|okay)|just (?:venting|thinking|wondering))\b",
        r"\bno,?\s*(?:thanks|thank you|i'?m good|that'?s okay)\b",
    ]
]


# --- Lens ↔ Workflow Affinity (#822) ---

# When the user's active conversational lens aligns with the detected
# workflow type, we boost confidence — the user is already thinking
# about this topic, so a soft offer is more likely welcome.
_LENS_WORKFLOW_AFFINITY: Dict[str, List[str]] = {
    "calendar": ["meeting", "standup"],
    "issues": ["priority_check", "status_check", "review"],
    "projects": ["project_setup", "status_check"],
    "people": ["meeting", "standup", "review"],
}

# Confidence boost when lens matches workflow type (+0.15, capped at 0.95)
_LENS_AFFINITY_BOOST = 0.15


# --- SoftInvocationDetector ---


class SoftInvocationDetector:
    """
    Detects implied workflow needs in natural conversation.

    Uses pattern matching against compiled expression groups.
    Each group maps to a workflow type with a pre-written offer message.
    """

    def detect(
        self,
        message: str,
        active_lens: Optional[str] = None,
        formality_baseline: Optional[float] = None,
    ) -> SoftInvocationResult:
        """
        Check if a message implies a workflow need.

        Only offers workflows that have registered entry points in the
        dispatcher registry (#923). Patterns that match unregistered
        workflow types are logged but not surfaced as offers.

        Args:
            message: User's message text
            active_lens: Current conversational lens value (#822).
                When the lens aligns with the detected workflow type,
                confidence is boosted.
            formality_baseline: Warmth level 0.0-1.0 from unified formality
                framework (#838). Controls offer/decline message tone.
                None defaults to "balanced" tier.

        Returns:
            SoftInvocationResult with offer if pattern matched AND
            workflow type is registered in the dispatcher.
        """
        if not message or len(message) < 10:
            return SoftInvocationResult(
                has_offer=False,
                reason="Message too short for soft invocation",
            )

        clean = message.strip().lower()

        # Resolve formality tier once for this detection pass
        tier = formality_label(formality_baseline) if formality_baseline is not None else "balanced"

        # #923: Only offer workflow types that have registered entry points
        from services.intent_service.workflow_dispatcher import get_registered_workflows

        registered = get_registered_workflows()

        for compiled_patterns, workflow_type, offer_msgs, decline_msgs in _SOFT_TRIGGER_PATTERNS:
            for pattern in compiled_patterns:
                if pattern.search(clean):
                    # #923: Skip offers for unregistered workflow types
                    if workflow_type not in registered:
                        logger.debug(
                            "soft_invocation_suppressed",
                            workflow_type=workflow_type,
                            pattern=pattern.pattern,
                            reason="no_registered_entry_point",
                            registered_types=list(registered.keys()),
                            message_preview=message[:50],
                        )
                        continue

                    # #822: Boost confidence when lens matches workflow type
                    confidence = 0.7
                    if active_lens and workflow_type in _LENS_WORKFLOW_AFFINITY.get(
                        active_lens, []
                    ):
                        confidence = min(confidence + _LENS_AFFINITY_BOOST, 0.95)

                    offer = WorkflowOffer(
                        workflow_type=workflow_type,
                        offer_message=offer_msgs.get(tier, offer_msgs["balanced"]),
                        decline_message=decline_msgs.get(tier, decline_msgs["balanced"]),
                        confidence=confidence,
                        trigger_pattern=pattern.pattern,
                    )
                    logger.debug(
                        "soft_invocation_detected",
                        workflow_type=workflow_type,
                        pattern=pattern.pattern,
                        confidence=confidence,
                        lens_boosted=confidence > 0.7,
                        formality_tier=tier,
                        message_preview=message[:50],
                    )
                    return SoftInvocationResult(
                        has_offer=True,
                        offer=offer,
                        reason=f"Matched {workflow_type} pattern",
                    )

        return SoftInvocationResult(
            has_offer=False,
            reason="No soft invocation patterns matched",
        )


def detect_offer_response(
    message: str, *, prose_override: bool = True
) -> Optional[str]:
    """
    Detect if a message is accepting or declining a previous offer.

    #1631: a multi-line or >= PROSE_LENGTH_FLOOR-character turn is prose by
    shape and returns None BEFORE any pattern consult — the unanchored
    accept/decline rows would otherwise claim a substring of a long
    free-text reply and fire (or drop) whatever offer is armed. Each kind's
    existing off-intent rule then handles the turn honestly.

    Args:
        message: User's response message
        prose_override: When True (default), multi-line or long turns are
            never offer responses. Pass False ONLY where a long turn can
            legitimately carry the response — sole opt-out today is
            verified_inference's meta-feedback seam, where a decline caught
            inside prose is the conservative direction (it prevents a
            store, nothing fires).

    Returns:
        "accept" if accepting, "decline" if declining, None if neither
    """
    if not message:
        return None

    clean = message.strip()

    if prose_override and is_prose_reply(clean):
        return None

    for pattern in ACCEPT_PATTERNS:
        if pattern.search(clean):
            return "accept"

    for pattern in DECLINE_PATTERNS:
        if pattern.search(clean):
            return "decline"

    return None


# --- WorkflowOfferService ---


class WorkflowOfferService:
    """
    Manages soft workflow offers with ProactivityGate integration.

    Handles:
    - ProactivityGate trust-stage checking
    - Exchange window throttling (max 2 per 5 exchanges)
    - Natural offer formatting with decline paths
    """

    def __init__(self, proactivity_gate: Optional[ProactivityGate] = None):
        self.proactivity_gate = proactivity_gate or ProactivityGate()
        self._offer_windows: Dict[str, OfferWindow] = {}  # composite key → window
        self._pending_offers: Dict[str, Dict[str, Any]] = {}  # composite key → offer

    @staticmethod
    def _key(session_id: str, user_id: Optional[str] = None) -> str:
        """Build composite key for user-scoped throttling stores (#817)."""
        return f"{user_id or 'anonymous'}:{session_id}"

    @staticmethod
    def _offer_key(session_id: str, **kwargs) -> str:
        """Build key for pending offer store — session-scoped only.

        Issue #846: Pending offers use session_id alone, not composite key.
        user_id in the key caused mismatch when auth state changes between
        turns (e.g., Turn 1 stores as 'alice:sess', Turn 2 looks up
        'anonymous:sess' after cookie expiry). Offers are transient
        (one-turn lifetime) so user scoping is unnecessary.
        """
        return session_id

    def should_offer(
        self,
        trust_stage: TrustStage,
        session_id: str,
        current_turn: int,
        suggestions_this_session: int,
        user_id: Optional[str] = None,
    ) -> Tuple[bool, str]:
        """
        Check if an offer should be presented right now.

        Checks:
        1. ProactivityGate allows hints at this trust stage
        2. Exchange window not saturated (< MAX_OFFERS_PER_WINDOW in last EXCHANGE_WINDOW_SIZE)
        3. Session-level limit not reached

        Args:
            trust_stage: User's current trust stage
            session_id: Current session ID
            current_turn: Current conversation turn number
            suggestions_this_session: Total suggestions already offered this session
            user_id: Optional user ID for scoped throttling (#817)

        Returns:
            Tuple of (should_offer, reason)
        """
        # Check ProactivityGate — use can_offer_capability_hints for soft offers
        # (softer than can_proactive_suggest, available at Stage 2+)
        if not self.proactivity_gate.can_offer_capability_hints(trust_stage):
            return False, f"Trust stage {trust_stage.name} doesn't allow hints"

        # Check session-level limit directly (don't use should_suggest_now
        # which also checks can_proactive_suggest, blocking Stage 2 users)
        max_allowed = self.proactivity_gate.get_max_suggestions_per_session(trust_stage)
        if suggestions_this_session >= max_allowed:
            return False, "Session suggestion limit reached"

        # Check exchange window throttling (#817: user-scoped key)
        key = self._key(session_id, user_id)
        window = self._offer_windows.get(key)
        if window is None:
            window = OfferWindow()
            self._offer_windows[key] = window

        offers_in_window = window.count_in_window(current_turn)
        if offers_in_window >= MAX_OFFERS_PER_WINDOW:
            return (
                False,
                f"Exchange window saturated ({offers_in_window}/{MAX_OFFERS_PER_WINDOW} in last {EXCHANGE_WINDOW_SIZE} turns)",
            )

        return True, "Offer allowed"

    def record_offer(self, session_id: str, turn: int, user_id: Optional[str] = None) -> None:
        """Record that an offer was made."""
        key = self._key(session_id, user_id)
        window = self._offer_windows.get(key)
        if window is None:
            window = OfferWindow()
            self._offer_windows[key] = window
        window.record_offer(turn)

    def set_pending_offer(
        self, session_id: str, offer: Dict[str, Any], user_id: Optional[str] = None
    ) -> None:
        """Store a pending offer awaiting user response."""
        self._pending_offers[self._offer_key(session_id)] = offer

    def get_and_clear_pending_offer(
        self, session_id: str, user_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Retrieve and clear a pending offer. Returns None if no offer pending."""
        return self._pending_offers.pop(self._offer_key(session_id), None)

    def peek_pending_offer(
        self, session_id: str, user_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Read a pending offer WITHOUT clearing it (#1595 shadow snapshot).

        Observer-only: the inversion shadow-check uses this for its
        lightweight session snapshot. Production offer handling must keep
        using ``get_and_clear_pending_offer`` — the pop IS the #1529
        offer-binding semantic (off-intent abandons via the clear); a peek
        must never replace it on the dispatch path. Store is session-keyed
        (#846); ``user_id`` is accepted for signature parity with the
        get/set pair.
        """
        return self._pending_offers.get(self._offer_key(session_id))

    def format_offer(self, offer: WorkflowOffer, base_response: str) -> str:
        """
        Append a soft offer to the base response with a natural transition.

        Args:
            offer: The workflow offer to append
            base_response: The existing response message

        Returns:
            Combined message with offer appended
        """
        # Natural transition between response and offer
        transition = "\n\n"
        return f"{base_response.rstrip()}{transition}{offer.offer_message}"

    def format_acceptance(
        self, workflow_type: str, formality_baseline: Optional[float] = None
    ) -> str:
        """Generate a natural workflow start message.

        Args:
            workflow_type: The workflow being accepted.
            formality_baseline: Warmth level 0.0-1.0 (#838).
                None defaults to "balanced" tier.
        """
        tier = formality_label(formality_baseline) if formality_baseline is not None else "balanced"

        _starts: Dict[str, Dict[str, str]] = {
            "meeting": {
                "warm": "Great! Let me help set that up.",
                "balanced": "Great! Let me help set that up.",
                "professional": "Confirmed. I'll arrange the meeting.",
            },
            "project_setup": {
                "warm": "Let's get things organized!",
                "balanced": "Let's get things organized.",
                "professional": "I'll draft the project structure.",
            },
            "status_check": {
                "warm": "Let me pull that up for you!",
                "balanced": "Let me pull that up for you.",
                "professional": "Compiling status now.",
            },
            "standup": {
                "warm": "Let's do a quick standup!",
                "balanced": "Let's do a quick standup.",
                "professional": "Initiating standup.",
            },
            "review": {
                "warm": "I'll help coordinate that!",
                "balanced": "I'll help coordinate that.",
                "professional": "I'll arrange the review.",
            },
            "priority_check": {
                "warm": "Let me take a look at what you've got going on!",
                "balanced": "Let me take a look at what you've got going on.",
                "professional": "Reviewing your current priorities.",
            },
            "reminder": {
                # #1198: claim the action being taken, not durable tracking —
                # "I'll keep track of that" promised an unspecified ongoing
                # watch; these fire at workflow START, before anything is saved.
                "warm": "Let me set that reminder for you!",
                "balanced": "Setting that reminder.",
                "professional": "Setting reminder.",
            },
        }

        tier_map = _starts.get(workflow_type)
        if tier_map is None:
            # Unknown workflow type — return a sensible default per tier
            _defaults = {
                "warm": "Let me help with that!",
                "balanced": "Let me help with that.",
                "professional": "I'll proceed.",
            }
            return _defaults.get(tier, _defaults["balanced"])

        return tier_map.get(tier, tier_map["balanced"])

    def format_decline(
        self, offer: WorkflowOffer, formality_baseline: Optional[float] = None
    ) -> str:
        """Generate a graceful decline acknowledgment.

        The offer already carries a formality-appropriate decline_message
        selected during detection. This method returns it directly.

        The *formality_baseline* parameter is accepted for forward
        compatibility but currently unused — the tier was already resolved
        when the offer was created.

        NOTE: Not yet called in production — decline path in intent_service.py
        reads decline_message from the pending_offer dict directly. Reserved
        for future use when decline formatting needs customization beyond the
        stored message. (Audit: #827, 2026-02-18)
        """
        return offer.decline_message
