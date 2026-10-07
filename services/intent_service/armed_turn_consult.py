"""#1886(b) — Arch's binding ruling, 2026-10-07: the stateless armed-turn
router consult, ONE helper shared by every armed-carrier off-intent
discriminator that needs to decide "is this reply the ANSWER to my open
question, or a NEW request" — the general case Arch's 2026-10-05 (b) already
named the router as authority for (D1: LLM decides meaning). #1886's
armed-name-question collision (mail
``rule-arch-to-lead-cc-cxo-1886-b-router-decides-answer-vs-new-ask-confirm-fallback-one-helper-both-carriers-2026-10-07.md``)
is the FIRST INSTANCE of this general decision, not a special case — which is
why this module exists once and is called from both the #1886 add-project
name carrier (``add_project_clarify.py``) and the reminder-task carrier
(``todo_handlers.py``), replacing each carrier's own bespoke off-intent
release logic (the #1886 add-project carrier's ``manage_portfolio``-excluded
``PreClassifier`` release, and the reminder-task carrier's
``PreClassifier.pre_classify`` + ``inversion_live.read_op_claims_turn``
two-layer release) rather than living beside it. "Two copies of 'release or
bind' are how they drift" (Arch).

THE THREE OUTCOMES (Arch, binding):

1. **RELEASE** — the router names an operation at/above the live-consult
   threshold (``inversion_live.live_min_confidence()``, default 0.8 via
   ``PIPER_INVERSION_LIVE_MIN_CONFIDENCE``). The turn is a NEW request, not
   an answer. The caller returns ``None``/disarms; the turn then routes
   NORMALLY — every gate (consent, the #1190 confirm, the live-dispatch
   flag) runs exactly as it would on a fresh turn. **This module NEVER
   dispatches** — it only classifies (Arch's first structural constraint).
   A caller MAY thread ``operation``/``confidence``/``rationale`` forward as
   data to skip a second router call on the released turn; that is an
   optimization the caller opts into, never something this module does.
2. **BIND** — the router returns ``none`` or ``clarify``: the turn
   genuinely looks like an answer, not a command. The caller binds as it
   would have before this module existed.
3. **CONFIRM** — the router names an operation BELOW threshold, or the
   consult errors, refuses, or cannot run at all (no key, quota, timeout):
   meaning is uncertain, so neither a silent bind nor a silent release is
   safe (ADR-078 D4 — never act on an inferred value without showing it
   first). The CALLER arms its own yes/no confirm (CXO's copy, when one
   exists for that carrier) or falls back to its own existing CLARIFY
   re-ask idiom when no confirm copy has been written for it — this module
   never invents copy, it only tells the caller which of the three
   happened.

STATELESS BY DESIGN (ADR-078 D4): the router call carries the message and
the registry-derived grammar ONLY — ``route(text, None, ...)``, exactly
``inversion_live.read_op_claims_turn``'s own call shape, never
``consult_inversion_live``'s session-snapshot-threaded one. An armed turn is
a #1190/#846 pending-offer turn by construction (a carrier only runs this
turn because an offer WAS popped), so a session-aware consult would just
re-discover the thing that is already armed.

NO LIVE-CATEGORIES GATE, DELIBERATELY. ``consult_inversion_live`` and
``read_op_claims_turn`` both stand down for free (zero work, zero LLM calls)
when ``PIPER_INVERSION_LIVE_CATEGORIES`` is unset/empty — correct THERE,
because that flag governs what may be DISPATCHED live, and an unreviewed
operation must never dispatch. This module never dispatches anything, so
that guard does not apply here: gating THIS consult on the dispatch flag
would mean the #1886 bug (a bare-name-question answer turn binding
"show my projects" as a literal project name) stays unfixed on exactly the
deployments that haven't flipped any category live yet — the opposite of
what this fix is for. The consult runs unconditionally on every armed
answer-turn that reaches it.

NEVER DISPATCHES (Arch's second structural constraint): this module calls
the router and nothing else — no ``dispatch_workflow``, no rail call, no
write, no store mutation. Release hands the turn back to
``IntentService.process_intent``'s normal chain, which decides (and gates)
as it always does; this is what keeps the armed-turn seam from becoming a
route around the live-dispatch flag and the #1190/consent gates.

BYOC (spend): the router call reuses the SAME llm_service resolution
``read_op_claims_turn`` already uses — ``intent_service.intent_classifier._llm``
— and threads ``user_id`` through to it exactly as that helper does, so
per-principal key resolution (#1415) happens inside ``LLMClient.complete``,
never a Piper-held key. This is why outcome 3 exists at all: a user with no
quota configured gets CONFIRM (or the caller's own clarify re-ask), never a
silent bind on a guess.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

import structlog

logger = structlog.get_logger()


class ArmedReplyOutcome(str, Enum):
    RELEASE = "release"
    BIND = "bind"
    CONFIRM = "confirm"


@dataclass(frozen=True)
class ArmedReplyDecision:
    """The consult's verdict, plus enough of the router's own decision that
    a caller MAY skip a second router call on a RELEASEd turn (Arch: "pass
    the decision forward as data" — optional, never required). ``reason`` is
    for logging/debugging only — callers must not branch on its exact
    string, only on ``outcome``."""

    outcome: ArmedReplyOutcome
    operation: Optional[str] = None
    confidence: Optional[float] = None
    rationale: Optional[str] = None
    reason: Optional[str] = None


async def classify_armed_reply(
    text: str,
    user_id: Optional[str],
    *,
    session_id: Optional[str],
    intent_service: Any,
) -> ArmedReplyDecision:
    """The stateless armed-turn router consult. See the module docstring for
    the three outcomes and why no live-categories gate applies here.

    ``text`` is the ANSWER-turn message (the pending offer was already
    popped this turn by the caller). An empty/whitespace-only ``text`` binds
    — callers that need to react to emptiness themselves (the established
    "no text, return None/generic-decline" shape every carrier already has)
    check that BEFORE calling this helper; this function never claims an
    empty turn is a command.
    """
    from services.intent_service.inversion_live import live_min_confidence
    from services.intent_service.inversion_router import derive_routing_grammar, route

    clean = (text or "").strip()
    if not clean:
        return ArmedReplyDecision(outcome=ArmedReplyOutcome.BIND, reason="empty_text")

    grammar = derive_routing_grammar()
    llm_service = getattr(getattr(intent_service, "intent_classifier", None), "_llm", None)

    try:
        decision = await route(
            clean,
            None,  # stateless — ADR-078 D4: message + catalog only, no SessionSnapshot
            llm_service=llm_service,
            grammar=grammar,
            user_id=user_id,
        )
    except Exception as e:  # silent-ok: #1886(b) — a consult failure must CONFIRM, never bind a guess or crash the armed turn; logged WARNING
        logger.warning(
            "armed_turn_consult_exception",
            session_id=session_id,
            error=str(e),
        )
        return ArmedReplyDecision(outcome=ArmedReplyOutcome.CONFIRM, reason="consult_exception")

    if decision.outcome == "none":
        logger.info(
            "armed_turn_consult_bind",
            session_id=session_id,
            router_outcome=decision.outcome,
        )
        return ArmedReplyDecision(
            outcome=ArmedReplyOutcome.BIND, reason=f"router_{decision.outcome}"
        )
    # CLARIFY confirms, it does not bind (Lead, 2026-10-07, the rule-8 live probe): the router
    # answered CLARIFY for "delete my project Klatch" (no delete-project op exists, so it asked)
    # — binding would have created a project with that literal name. CLARIFY means "unsure",
    # not "not a command"; uncertain meaning confirms before a write (ADR-080 D4). Cost: some
    # real names ("Piper Morgan Website" also drew CLARIFY) take one extra yes/no turn.

    if decision.outcome != "operation" or not decision.operation:
        # refused / error / plan / anything else unnamed — the consult
        # couldn't name a concrete operation; never a silent bind on a guess.
        logger.info(
            "armed_turn_consult_confirm",
            session_id=session_id,
            router_outcome=decision.outcome,
        )
        return ArmedReplyDecision(
            outcome=ArmedReplyOutcome.CONFIRM, reason=f"router_{decision.outcome}"
        )

    threshold = live_min_confidence()
    if decision.confidence is not None and decision.confidence >= threshold:
        logger.info(
            "armed_turn_consult_release",
            session_id=session_id,
            operation=decision.operation,
            confidence=decision.confidence,
            threshold=threshold,
        )
        return ArmedReplyDecision(
            outcome=ArmedReplyOutcome.RELEASE,
            operation=decision.operation,
            confidence=decision.confidence,
            rationale=decision.rationale,
        )

    logger.info(
        "armed_turn_consult_confirm",
        session_id=session_id,
        operation=decision.operation,
        confidence=decision.confidence,
        threshold=threshold,
        reason="sub_threshold",
    )
    return ArmedReplyDecision(
        outcome=ArmedReplyOutcome.CONFIRM,
        operation=decision.operation,
        confidence=decision.confidence,
        rationale=decision.rationale,
        reason="sub_threshold",
    )
