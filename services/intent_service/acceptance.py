"""#1739 — THE acceptance contract (one predicate, every armed seam).

PM's 2026-09-09 round (Exec's convergence memo): three failures in one
session were the same contract failing in opposite directions —

    #1617  "are we done with that standup?"  (a QUESTION)  → FIRED
    #1694  "yes"  (the least ambiguous acceptance)         → did nothing
    #1631/#1650  prose asides opening "please"/"yes,"      → FIRED

"A mechanism that accepts a question and rejects a bare yes does not have a
threshold problem. It has no single arming contract." PM's directive: "we're
not patching via whack-a-mole, but capturing patterns."

THE CONTRACT (issue #1739, Arch ruling + CXO pass 2026-09-09, both binding):

(a) **Question-forms NEVER accept.** An interrogative turn is a DIFFERENT
    SPEECH ACT — a query about state, not consent (CXO: treating "are we
    done?" as an acceptance-that-didn't-parse is the category error that
    produced #1617; treating it as a failed acceptance and re-prompting is
    the same error the other way, #1579). The verdict is STATE_QUESTION:
    the seam answers truthfully from state and the arm SURVIVES — it is
    neither consumed nor silently dropped.
(b) **Bare affirmatives accept exactly-armed offers.** #1694's "yes" doing
    nothing is the contract failing in the strict direction.
(c) **Prose asides neither accept nor steal** — the #1631 shape floor and
    the #1650 crisp-confirm rule, generalized (both consulted here).
(d) **Strictness scales on BOTH ratified axes** — EffectClass AND
    Outwardness, exactly the two axes ``decide_consent`` takes (ratified
    PM+CXO+PPM 2026-08-15). CXO's structural correction: the ask and the
    acceptance are two halves of ONE gate; if they scale on different axes
    the gate has a seam exactly where the axes disagree. An OUTWARD WRITE
    accepts at the DESTRUCTIVE-tier bar — "shall I post this comment?" must
    not have the acceptance bar of "shall I retitle your todo?".

BUILT ON — ABSORBING — the #1650 machinery, not beside it: the accept /
decline vocabularies (``ACCEPT_PATTERNS`` / ``DECLINE_PATTERNS`` /
``CONFIRM_ACCEPT_RE``) and the #1631 prose floor stay declared in
``soft_invocation.py``; THIS function is the single place they are composed
into a verdict. ``detect_confirm_response`` is now a compatibility alias
that delegates here (soft_invocation.py). ``detect_offer_response`` remains
byte-for-byte legacy behavior for NOT-YET-ADOPTED seams (the #1739 ratchet
in tests/test_architecture_enforcement.py enumerates them; the set only
shrinks — Arch condition (c)).

SEQUENCING (Arch's three binding conditions):
(a) input-adequacy before DESTRUCTIVE-adjacent adoption — a seam adopts only
    when its arm-site stores what was actually asked (#1665's rendered-ask
    contract). Mechanical form here: at the NAMED_OBJECT tier, an accept
    against a missing armed ask is REFUSED — "a predicate fed None returns
    confidence, not judgment" (Arch). CXO's user-facing statement of the
    same condition: if Piper cannot quote the acceptance back into a true
    sentence, the offer was not specific enough to be accepted.
(b) adopt by EffectClass ASCENDING — READ seams first; DESTRUCTIVE last,
    after the predicate has mileage.
(c) the shrink-only KNOWN_UNADOPTED ratchet — a contract that doesn't break
    the build is a convention, and conventions decay per-seam (m-53).
"""

from __future__ import annotations

import re
from enum import Enum, IntEnum
from typing import Iterable, Optional, Tuple

import structlog

from services.shared_types import EffectClass, Outwardness

logger = structlog.get_logger(__name__)


class AcceptanceVerdict(Enum):
    """What the user's turn does to an armed offer — the four speech acts.

    Deliberately NOT a new vocabulary (CXO): these are the reply-halves of
    the verdicts ``ConsentDecision`` already implies at the ask-half.
    """

    ACCEPT = "accept"  # consent granted — the armed action may fire
    DECLINE = "decline"  # consent withheld — cancel honestly, nothing fires
    # A query about state — NOT a failed acceptance (CXO's ruling). The seam
    # answers truthfully and the arm SURVIVES (restated, never re-fired).
    STATE_QUESTION = "state_question"
    # An aside / off-intent turn: neither accepts nor steals. Each seam's
    # documented off-intent rule applies (#1190: the pop already cancelled
    # the action; normal processing answers the turn).
    PASS = "pass"


class AcceptanceTier(IntEnum):
    """How crisp an accept must be — derived from BOTH ratified axes."""

    # CXO's COLLABORATE row: "yes / go / send it / looks good" — looking at
    # a draft with a colleague; ceremony here reads as distrust.
    LOW_CEREMONY = 1
    # CXO's DESTRUCTIVE / OUTWARD-WRITE row: a bare affirmative ONLY against
    # an offer that named its object — one beat of earned friction.
    NAMED_OBJECT = 2


# Sentinel for the legacy ``detect_confirm_response`` alias ONLY: it marks a
# call path that predates the contract and does not thread its arm-site's
# stored ask through. Adopted seams pass the REAL stored ask (or None, and
# at the NAMED_OBJECT tier a None ask refuses to accept — Arch condition
# (a) with teeth). Do not use this sentinel at new call sites; the #1739
# ratchet tracks the alias's callers as unadopted.
LEGACY_UNTHREADED = object()


def acceptance_tier(
    effect: Optional[EffectClass],
    outwardness: Optional[Outwardness] = None,
) -> AcceptanceTier:
    """Strictness from the TWO ratified axes (CXO's structural correction).

    - DESTRUCTIVE (any outwardness)  → NAMED_OBJECT (the #1190/#1650 bar)
    - WRITE × OUTWARD                → NAMED_OBJECT — a communication act is
      socially irreversible the instant it lands (the reason the axis
      exists); it accepts at the DESTRUCTIVE-tier bar.
    - WRITE × PRIVATE, READ          → LOW_CEREMONY
    - undeclared effect (None)       → NAMED_OBJECT — the safe direction; an
      undeclared seam can never get a WEAKER bar than a declared one.
    """
    if effect is None:
        return AcceptanceTier.NAMED_OBJECT
    if effect == EffectClass.DESTRUCTIVE:
        return AcceptanceTier.NAMED_OBJECT
    if effect == EffectClass.WRITE and outwardness == Outwardness.OUTWARD:
        return AcceptanceTier.NAMED_OBJECT
    return AcceptanceTier.LOW_CEREMONY


# --- Question-shape detection (contract axis (a)) ---------------------------

# A turn that ENDS in "?" is interrogative regardless of how it opens
# (trailing quotes/brackets tolerated).
_TERMINAL_QUESTION_RE = re.compile(r"\?[\s\"'’”\)\]]*$")

# Openers that cannot plausibly begin an acceptance ("are we done with that
# standup" carries no "?" in PM's live transcript shape and must still read
# as a question). DELIBERATELY EXCLUDED: do / can / could / will / would /
# shall / should / may / might / have — each also opens imperatives or
# accept vocabulary ("do it", "go ahead and do it", "have at it"); those
# shapes are questions only with a terminal "?".
_INTERROGATIVE_OPENER_RE = re.compile(
    r"^(?:are|is|am|was|were|does|did|what|when|where|which|who|whom|whose|why|how)\b",
    re.IGNORECASE,
)


def is_state_question(message: str) -> bool:
    """True when the turn is interrogative BY SHAPE — a state query.

    Contract axis (a): a '?' or interrogative shape is a query about state,
    not consent. Never consulted for prose-shaped turns (the #1631 floor
    runs first in :func:`evaluate_acceptance`)."""
    clean = (message or "").strip()
    if not clean:
        return False
    if _TERMINAL_QUESTION_RE.search(clean):
        return True
    # Opener-only questions need at least one more word ("are we done…");
    # a bare "what?"-style single token already carries the "?".
    return bool(_INTERROGATIVE_OPENER_RE.match(clean)) and len(clean.split()) >= 2


# --- Taught-vocabulary normalization ----------------------------------------

_TRAILING_PUNCT_RE = re.compile(r"[\s.!,;:]+$")


def _normalize_taught(text: str) -> str:
    return _TRAILING_PUNCT_RE.sub("", text.strip().lower())


# --- THE predicate -----------------------------------------------------------


def evaluate_acceptance(
    message: str,
    *,
    effect: Optional[EffectClass],
    outwardness: Optional[Outwardness] = None,
    armed_question,  # Optional[str], or LEGACY_UNTHREADED (alias path only)
    taught_accepts: Optional[Iterable[str]] = None,
) -> AcceptanceVerdict:
    """THE acceptance predicate — one function, consulted by every adopted
    armed seam (#1739; the ``decide_consent`` idiom at the reply-half).

    Args:
        message: the user's turn, raw.
        effect: the armed action's DECLARED EffectClass (from its
            WorkflowEntry / arm site — never inferred from names, #1557).
            None = undeclared → strictest tier.
        outwardness: the armed action's DECLARED Outwardness (#1509 axis).
            None = PRIVATE (matches WorkflowEntry's safe default).
        armed_question: the rendered ask the arm-site stored (#1665) — what
            the user actually saw. At the NAMED_OBJECT tier a missing ask
            REFUSES to accept (Arch condition (a): a seam adopts only when
            its arm-site stores what was actually asked). REQUIRED keyword:
            every adopted seam states what it knows, even when that is None.
        taught_accepts: seam-taught closing phrases ("looks good", "done" at
            the standup tail; the drafted-issue "file it" family precedent)
            accepted as FULL-MESSAGE matches only, and only at the
            LOW_CEREMONY tier — taught vocabulary never loosens the
            NAMED_OBJECT bar.

    Verdict order (most protective first):
        empty/prose → PASS  (asides neither accept nor steal, #1631)
        question    → STATE_QUESTION  (never accept, never decline — a
                      different speech act; the seam answers state and the
                      arm survives)
        accept      → tier-scaled (crisp full-message at NAMED_OBJECT, the
                      generic vocabulary + taught phrases at LOW_CEREMONY)
        decline     → the shared decline vocabulary (declines were never the
                      greedy hazard, and a decline only cancels)
        otherwise   → PASS
    """
    # Absorbed #1650/#1631 machinery — the vocabularies stay declared at
    # their original site; this is the one place they are composed.
    from services.intent_service.soft_invocation import (
        ACCEPT_PATTERNS,
        CONFIRM_ACCEPT_RE,
        DECLINE_PATTERNS,
        is_prose_reply,
    )

    if not message:
        return AcceptanceVerdict.PASS

    clean = message.strip()
    if not clean:
        return AcceptanceVerdict.PASS

    if is_prose_reply(clean):
        return AcceptanceVerdict.PASS

    if is_state_question(clean):
        return AcceptanceVerdict.STATE_QUESTION

    tier = acceptance_tier(effect, outwardness)

    if tier == AcceptanceTier.NAMED_OBJECT:
        if CONFIRM_ACCEPT_RE.match(clean):
            # Arch condition (a), mechanical: an accept against an arm-site
            # that stored no rendered ask is refused — the predicate must
            # never return confidence where it was fed nothing to judge
            # against. (LEGACY_UNTHREADED marks the pre-contract alias path,
            # which keeps #1650 behavior and is ratchet-tracked.)
            if armed_question is LEGACY_UNTHREADED or armed_question:
                return AcceptanceVerdict.ACCEPT
            logger.warning(
                "acceptance_refused_no_armed_ask",
                tier="named_object",
                reason="arm site stored no rendered ask (#1665 / #1739 input-adequacy)",
            )
            return AcceptanceVerdict.PASS
    else:
        if taught_accepts:
            normalized = _normalize_taught(clean)
            if normalized and normalized in {_normalize_taught(t) for t in taught_accepts}:
                return AcceptanceVerdict.ACCEPT
        # The tiers are ordered: anything crisp enough for the NAMED_OBJECT
        # bar is a fortiori an accept at the low-ceremony one ("y",
        # "confirm" — strict vocabulary ⊂ loose acceptance).
        if CONFIRM_ACCEPT_RE.match(clean):
            return AcceptanceVerdict.ACCEPT
        for pattern in ACCEPT_PATTERNS:
            if pattern.search(clean):
                return AcceptanceVerdict.ACCEPT

    for pattern in DECLINE_PATTERNS:
        if pattern.search(clean):
            return AcceptanceVerdict.DECLINE

    return AcceptanceVerdict.PASS


# --- Registry lookup helper (the effect_for_action idiom) --------------------


def declared_axes_for_workflow(
    workflow_type: Optional[str],
) -> Optional[Tuple[EffectClass, Outwardness]]:
    """The armed workflow's DECLARED axes, from the registry — both axes ride
    the one WorkflowEntry declaration (#1557 / #1509; consumers look up,
    never infer from names). None for unregistered workflow types — an offer
    with no declared axes gets no predicate derivation here (its seam stays
    on its documented legacy behavior, ratchet-tracked)."""
    if not workflow_type:
        return None
    from services.intent_service.workflow_dispatcher import get_registered_workflows
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()  # idempotent; no-op when already registered
    entry = get_registered_workflows().get(workflow_type)
    if entry is None:
        return None
    return (entry.effect, entry.outwardness)
