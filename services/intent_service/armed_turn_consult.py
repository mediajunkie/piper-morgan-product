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
   ``PIPER_INVERSION_LIVE_MIN_CONFIDENCE``) that is NOT one of the caller's
   own ``answering_operations`` (see below). The turn is a NEW request, not
   an answer. The caller returns ``None``/disarms; the turn then routes
   NORMALLY — every gate (consent, the #1190 confirm, the live-dispatch
   flag) runs exactly as it would on a fresh turn. **This module NEVER
   dispatches** — it only classifies (Arch's first structural constraint).
   A caller MAY thread ``operation``/``confidence``/``rationale`` forward as
   data to skip a second router call on the released turn; that is an
   optimization the caller opts into, never something this module does.
2. **BIND** — the router returns ``none``, OR names an operation at/above
   threshold that IS one of the caller's ``answering_operations``: the turn
   genuinely looks like an answer, not a new command. The caller binds as it
   would have before this module existed (``operation`` is ``None`` on a
   ``none`` bind; ``decision.operation``/``decision.args`` are populated on
   an answering-operation bind — see "PER-CARRIER ANSWERING OPERATIONS"
   below).
3. **CONFIRM** — the router returns ``clarify``, names a NON-answering
   operation BELOW threshold, or the consult errors, refuses, or cannot run
   at all (no key, quota, timeout): meaning is uncertain, so neither a
   silent bind nor a silent release is safe (ADR-078 D4 — never act on an
   inferred value without showing it first). The CALLER arms its own
   yes/no confirm (CXO's copy, when one exists for that carrier) or falls
   back to its own existing CLARIFY re-ask idiom when no confirm copy has
   been written for it — this module never invents copy, it only tells the
   caller which of the three happened.

PER-CARRIER ANSWERING OPERATIONS (Arch, 2026-10-07, generalizing #1886(b)
for the clear-family verb carrier — mail
``rule-arch-to-lead-cc-cxo-clear-todos-three-points-...-2026-10-07.md``,
point 3): two armed carriers can differ on WHAT COUNTS AS AN ANSWER to
their own open question, so ``classify_armed_reply`` takes an optional
``answering_operations`` set, per call:

- **Name carrier (#1886)**: ``answering_operations`` is left at its default
  (empty). Only the router's bare ``none`` outcome answers (binds as the
  literal name); ANY named operation at/above threshold is a brand-new
  command and releases — this is the ORIGINAL, unchanged #1886(b) behavior.
- **Verb carrier (clear-family)**: ``answering_operations={"complete_todo",
  "delete_todo"}`` — the two verb choices. When the router names one of
  THOSE at/above threshold, that operation itself IS the answer (the user
  said, in effect, "mark them done" or "delete them, but not the PR one"),
  and ``decision.args`` carries that answer turn's OWN ``targets``/
  ``exclude`` so the caller can refine the previously-shown set rather than
  acting on it unrefined. Any OTHER operation at/above threshold still
  releases (the user moved on to an unrelated ask) — this carrier's ``none``
  outcome is deliberately NOT in its answering set (unlike the name
  carrier): for a yes/no verb question, "the router found no command" says
  nothing about which verb was meant, so that case is left to the caller's
  own CONFIRM-style fallback alongside ``clarify``/sub-threshold/error,
  never guessed as this module's default BIND.
- The helper STILL only classifies — it never dispatches, and the refined
  set is resolved by the CALLER's own code against the rows it actually
  showed the user (D2), never trusted verbatim from the router's args.

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

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, FrozenSet, Optional

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
    string, only on ``outcome``.

    ``args`` (2026-10-07, point 3's generalization): the router's OWN
    ``RoutingDecision.args`` for an answering-operation BIND — populated
    ONLY when ``operation`` was matched against the caller's
    ``answering_operations`` (never on a plain ``none`` bind, never on a
    RELEASE or CONFIRM). Exposed as data; this module never reads or
    resolves it — a caller that refines a shown set from it must resolve
    against the rows it actually showed (D2), never trust it verbatim."""

    outcome: ArmedReplyOutcome
    operation: Optional[str] = None
    confidence: Optional[float] = None
    rationale: Optional[str] = None
    reason: Optional[str] = None
    args: Dict[str, Any] = field(default_factory=dict)


async def classify_armed_reply(
    text: str,
    user_id: Optional[str],
    *,
    session_id: Optional[str],
    intent_service: Any,
    answering_operations: FrozenSet[str] = frozenset(),
) -> ArmedReplyDecision:
    """The stateless armed-turn router consult. See the module docstring for
    the three outcomes and why no live-categories gate applies here.

    ``text`` is the ANSWER-turn message (the pending offer was already
    popped this turn by the caller). An empty/whitespace-only ``text`` binds
    — callers that need to react to emptiness themselves (the established
    "no text, return None/generic-decline" shape every carrier already has)
    check that BEFORE calling this helper; this function never claims an
    empty turn is a command.

    ``answering_operations`` (2026-10-07, Arch's generalization of #1886(b)
    for the clear-family verb carrier, point 3): operation names that count
    as THIS carrier's own answer, not a new command. Left at its default
    (empty) frozenset, every call behaves byte-identically to the ORIGINAL
    #1886(b) helper (only ``none`` binds; any named operation at/above
    threshold releases) — this is the name carrier's behavior, unchanged.
    A carrier that passes a non-empty set (e.g. the verb carrier's
    ``{"complete_todo", "delete_todo"}``) gets a BIND — not a RELEASE —
    when the router names one of ITS operations at/above threshold, with
    that decision's ``args`` carried on the returned ``ArmedReplyDecision``
    so the caller can refine the set it already showed. The router's bare
    ``none`` outcome is NEVER itself in ``answering_operations`` (it isn't
    an operation name) and always binds with ``operation=None`` regardless
    of this parameter — a caller for whom that outcome is NOT informative
    (the verb carrier) distinguishes it from an answering-operation bind by
    checking ``decision.operation is None`` and falls back to its own logic.
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
        if decision.operation in answering_operations:
            # Point 3's generalization: for THIS carrier, this named
            # operation IS the answer to the open question, not a new
            # command — bind it, with the router's own args carried
            # forward so the caller can refine the shown set.
            logger.info(
                "armed_turn_consult_bind_answering_operation",
                session_id=session_id,
                operation=decision.operation,
                confidence=decision.confidence,
                threshold=threshold,
            )
            return ArmedReplyDecision(
                outcome=ArmedReplyOutcome.BIND,
                operation=decision.operation,
                confidence=decision.confidence,
                rationale=decision.rationale,
                reason=f"router_{decision.outcome}",
                args=dict(decision.args or {}),
            )
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
