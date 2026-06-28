"""
Issue #900 Phase 3: Completion-signal detection for standup conversations.

Pure decision function — given a user message, the current
StandupPartialCapture, and the current StandupConversationState, return
a CompletionSignal describing whether the standup should advance early
to GENERATING (skip remaining parts).

Design intent: heuristic-first, regex-based. No LLM gate for MVP. Keeps
the function pure so it's trivially unit-testable and produces
deterministic behavior. LLM-classification of completion intent is
deferred to post-MVP per the #900 gameplan.

The detection rules are layered so the most-specific signal wins:
1. **Explicit done** — user types "done", "stop", "that's it", "that's
   all", "finish", "finished", "complete". User is unambiguously asking
   to finalize early.
2. **Natural completion** — user types "nothing else", "all good", "no
   more", "that's everything". Softer signal but clear intent.
3. **Structural full** — current state is GATHERING_BLOCKERS AND any
   non-empty parts captured. The flow has reached its final part; we
   advance regardless of message content (the per-part handler is
   responsible for routing this).

Negatives that should NOT trigger:
- Substring matches inside larger phrases ("done with this thought" while
  mid-yesterday capture, "finish the rebase tomorrow" as a today item).
  We use word-boundary regex to avoid these.
- Skip signals during gathering — those are part-level skips handled by
  `_is_skip_signal` in the handler, not full standup completion.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from services.domain.models import StandupPartialCapture
from services.shared_types import StandupConversationState


@dataclass
class CompletionSignal:
    """Output of `detect_completion` — should we finalize early?

    `is_complete=True` means the per-part handler should transition to
    GENERATING instead of advancing to the next gathering state.
    `reason` names which rule fired so callers (and tests) can disambiguate.
    """

    is_complete: bool
    reason: Optional[str] = None  # "explicit_done" | "natural_signal" | "structural_full" | None


# Word-boundary regexes — avoid substring matches inside larger phrases.
_EXPLICIT_DONE_RE = re.compile(
    r"\b(done|stop|finish(?:ed)?|complete)\b|that['’]s (?:it|all)",
    re.IGNORECASE,
)
_NATURAL_COMPLETION_RE = re.compile(
    r"\b(nothing else|all good|no more|that['’]s everything)\b",
    re.IGNORECASE,
)


def detect_completion(
    *,
    user_message: str,
    capture: StandupPartialCapture,
    current_state: StandupConversationState,
) -> CompletionSignal:
    """Decide whether to finalize the standup early.

    Args:
        user_message: The user's most recent reply (already stripped is fine
            but not required).
        capture: Current `StandupPartialCapture` state for this conversation.
        current_state: Conversation's current state at the time of decision.

    Returns:
        CompletionSignal. `is_complete=True` means transition to GENERATING.
    """
    # Only the gathering states can trigger early completion. Other states
    # have their own routing logic and shouldn't be short-circuited here.
    if current_state not in (
        StandupConversationState.GATHERING_YESTERDAY,
        StandupConversationState.GATHERING_TODAY,
        StandupConversationState.GATHERING_BLOCKERS,
    ):
        return CompletionSignal(is_complete=False, reason=None)

    text = (user_message or "").strip()

    # Explicit done — most specific, wins over natural-completion phrasing
    if text and _EXPLICIT_DONE_RE.search(text):
        return CompletionSignal(is_complete=True, reason="explicit_done")

    # Natural completion phrases
    if text and _NATURAL_COMPLETION_RE.search(text):
        return CompletionSignal(is_complete=True, reason="natural_signal")

    # Structural: at the final part with at least one captured item, the
    # blockers handler is the natural place for the last advance — but we
    # don't auto-advance from blockers based purely on capture-completeness;
    # the user still needs to send a message to trigger the handler. This
    # signal is therefore informational for the handler, not load-bearing.
    if current_state == StandupConversationState.GATHERING_BLOCKERS and capture.is_complete():
        return CompletionSignal(is_complete=True, reason="structural_full")

    return CompletionSignal(is_complete=False, reason=None)
