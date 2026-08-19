"""#1509 TRUST-CONSENT — the UNIFIED consent decision (one function, one seam).

THE NAMED BOUNDARY CONDITION (issue #1509 AC-1 — written down here, never
inferred per call site):

    A consent check stands between intent-formation and execution whenever the
    classified action's DECLARED EffectClass is WRITE or above (the Arch-ruled
    ``needs_consent = effect >= WRITE`` derivation, shared_types.py) AND the
    request's framing does not itself carry consent:

    - DESTRUCTIVE effect  -> CONFIRM, always (the #1190 yes/no gate; framing
      and working mode never weaken it — an execute-mode user still confirms).
    - WRITE effect, COMPOSE framing ("help me write...")   -> COLLABORATE.
    - WRITE effect, EXECUTE framing (explicit imperative)  -> PROCEED — the
      imperative IS the consent; the gate confiscates ambiguity, never
      imperatives (#1510).
    - WRITE effect, AMBIGUOUS framing -> the user's declared WorkingMode
      decides: COLLABORATE by default; PROCEED only after the user has
      established execute mode ("just do things directly from now on").
    - READ effect -> PROCEED, always. Reads are not consent territory
      (PM 2026-08-13, effect-weighting: "wrong list != lost data").

    THE OUTWARDNESS AXIS (#1509, ratified PM + CXO + PPM 2026-08-15) — a
    SECOND dimension, orthogonal to effect: effect measures how hard the data
    state is to undo; outwardness measures who else witnesses the action.
    Scope boundary (CXO's ruling, declared on ``shared_types.Outwardness``,
    never inferred per call site): OUTWARD = the action IS a communication
    act (a comment, a message, a filed issue) — NOT "touches data someone
    could theoretically later see". Consequence in this matrix (CXO's
    mechanism ruling): outward-WRITE is neither a second DESTRUCTIVE
    ("always confirm") nor a silent pass-with-logging. Under
    collaborate/ambiguous cells it checks exactly as today; wherever a
    DECLARED trust mode (WorkingMode.EXECUTE) lets an outward WRITE proceed,
    it proceeds WITH a disclosure line — Piper states what it's about to do
    and to whom BEFORE doing it (the #1605 variant-two "say it out loud"
    pattern), a transparency add-on, never a yes/no gate. DESTRUCTIVE stays
    CONFIRM in every outwardness cell (close/reopen stay DESTRUCTIVE and
    PRIVATE — PPM's settled boundary case; the axes are jointly exhaustive
    over reasons for care, not redundant nets over the same actions).

This module generalizes — it does not parallel — the two prior gates:

- #1190 (``destructive_confirm.py``) built CONFIRM for the DESTRUCTIVE tier.
  Its rail branch now takes the CONFIRM verdict from :func:`decide_consent`
  (for DESTRUCTIVE the verdict is CONFIRM in every cell, so behavior is
  identical; the decision now has one home).
- #1510 (``collaboration_gate.py``) built COLLABORATE for the create-issue
  family. Its ``gate_holds`` now delegates to :func:`decide_consent`, with the
  action's effect looked up from the workflow registry (the swap its own
  GATED_WRITE_ACTIONS comment tracked) — the create family keeps its richer
  draft-collaboration copy, selected via ``DRAFT_COLLABORATION_ACTIONS``
  (a COPY-SURFACE choice, not a gate-membership list).
- The #1510 verified-inference rail (``verified_inference.py``) measures a
  DIFFERENT quantity — inference confidence, not action consent — and PM's
  ruling keeps process-steering signals distinct. The two compose here via
  :func:`decide_verb_interpretation` (PM 2026-08-13: unmapped verbs over
  stateful operations ASK, effect-weighted), which weights the rail's
  read-back trigger by the candidate mapping's EffectClass instead of
  re-deriving either mechanism.

WHERE IT FIRES (routing moratorium honored — no pre-classifier or prompt
changes): at the #1124 action rail in ``IntentService.process_intent``,
post-classification, exactly where #1190's gate already sat — plus the
``_handle_create_issue`` backstop for legacy non-rail paths. The check turn
binds via the EXISTING #846 pending-offer store using #1190's action-agnostic
``pending_action`` carrier and acceptance workflow — acceptance re-dispatches
the ORIGINAL intent; the "yes" is never re-classified. No parallel store, no
parallel acceptance path.

TRANSCRIPT LEGIBILITY (#1509 AC-5): every held turn SAYS a check happened —
the check copy names the action in plain words and states its effect tier
(derived via ``capability_legibility.describe_effect``, never hand-written
per action), and the result carries ``consent_check_pending`` /
``destructive_confirmation_pending`` intent_data flags.

DECLINE PROPERTIES (CXO's invitation properties): declining is cheap (one
word), changes nothing else (the pop already cancelled the pending action;
the decline copy says so), and nothing nags — the same request would be
checked again ONLY because consent is per-action-instance. Deliberately NOT
reused here: the verified-inference session decline memory. Suppressing a
CONSENT check after a decline would make the next identical request execute
silently — decline memory must never lower a safety gate (it suppresses
re-asking about a preference, not re-checking an action).
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional

from services.shared_types import EffectClass, Outwardness

logger = logging.getLogger(__name__)


# Marker inside a consent-check pending_action payload (the #1190 carrier is
# action-agnostic; ``kind`` is how the offer seam names an abandoned check in
# its logs without a parallel store — the verify_inference convention).
CONSENT_CHECK_KIND = "consent_check"


class ConsentDecision(str, Enum):
    """What the consent boundary requires before this action may execute."""

    PROCEED = "proceed"  # framing/mode/effect carry consent — execute now
    # #1509 outwardness: execute now, but the reply STATES what is being done
    # and to whom before the handler's own result — a disclosure line, never
    # a yes/no gate (CXO's mechanism ruling; the #1605 variant-two pattern).
    # Strictly MORE transparent than PROCEED, strictly LESS blocking than
    # COLLABORATE — a fourth verdict, not a modifier on the others.
    PROCEED_WITH_DISCLOSURE = "proceed_with_disclosure"
    COLLABORATE = "collaborate"  # engage the user first (draft/check turn)
    CONFIRM = "confirm"  # explicit yes/no required (#1190 destructive tier)


def decide_consent(
    effect: EffectClass,
    framing: str,
    mode: "WorkingMode",  # noqa: F821 — collaboration_gate.WorkingMode (import cycle)
    outwardness: Outwardness = Outwardness.PRIVATE,
) -> ConsentDecision:
    """THE consent decision — one function, consulted by every gate path.

    Full matrix (denominator: 2 outwardness x 3 effects x 3 framings x
    2 modes = 36 cells, every cell asserted in
    test_consent_gate_1509.TestConsentDecisionMatrix):

    ==========  ==========  =========  ===========  ==============
    outwardness effect      framing    COLLABORATE  EXECUTE mode
    ==========  ==========  =========  ===========  ==============
    PRIVATE     READ        compose    PROCEED      PROCEED
    PRIVATE     READ        execute    PROCEED      PROCEED
    PRIVATE     READ        ambiguous  PROCEED      PROCEED
    PRIVATE     WRITE       compose    COLLABORATE  COLLABORATE
    PRIVATE     WRITE       execute    PROCEED      PROCEED
    PRIVATE     WRITE       ambiguous  COLLABORATE  PROCEED
    PRIVATE     DESTRUCTIVE compose    CONFIRM      CONFIRM
    PRIVATE     DESTRUCTIVE execute    CONFIRM      CONFIRM
    PRIVATE     DESTRUCTIVE ambiguous  CONFIRM      CONFIRM
    OUTWARD     READ        compose    PROCEED      PROCEED
    OUTWARD     READ        execute    PROCEED      PROCEED
    OUTWARD     READ        ambiguous  PROCEED      PROCEED
    OUTWARD     WRITE       compose    COLLABORATE  COLLABORATE
    OUTWARD     WRITE       execute    PROCEED      PROCEED_W_DISC
    OUTWARD     WRITE       ambiguous  COLLABORATE  PROCEED_W_DISC
    OUTWARD     DESTRUCTIVE compose    CONFIRM      CONFIRM
    OUTWARD     DESTRUCTIVE execute    CONFIRM      CONFIRM
    OUTWARD     DESTRUCTIVE ambiguous  CONFIRM      CONFIRM
    ==========  ==========  =========  ===========  ==============

    The PRIVATE half IS the pre-axis 18-cell matrix, unchanged — PRIVATE is
    today's semantics, which is why the parameter may default to it (the
    default can never weaken a cell; see WorkflowEntry.outwardness).

    The OUTWARD half differs from PRIVATE in exactly two cells, both under
    the DECLARED trust mode (WorkingMode.EXECUTE), and in both the decision
    gets STRICTLY MORE careful, never less (the doctrine tests pin this):
    wherever trust mode lets an outward WRITE proceed, Piper still states
    what it's about to do and to whom BEFORE doing it (CXO's mechanism
    ruling: a disclosure line, not a yes/no gate — Jake's incident class
    keeps real protection, an ambiguous outward request under the default
    mode still asks, without making a trusted user re-confirm every GitHub
    comment forever).

    Cell-level rationale for the OUTWARD half:
    - OUTWARD x READ: PROCEED — a communication act creates or sends
      content, which is a write by definition, so an OUTWARD READ is
      unrepresentable by the scope boundary; the cells exist because the
      type space contains them, and they rule the safe thing.
    - OUTWARD x WRITE x compose: COLLABORATE both modes — same as PRIVATE
      (executing a request for drafting HELP is the Jake failure, #1510).
    - OUTWARD x WRITE x execute x COLLABORATE mode: PROCEED, no disclosure —
      same as today. The imperative IS the consent, and the user themselves
      said the action out loud this turn; the disclosure discipline attaches
      to the DECLARED trust mode, where actions can also fire on ambiguity.
    - OUTWARD x WRITE x execute x EXECUTE mode: PROCEED_WITH_DISCLOSURE —
      CXO's "under a declared TRUST mode, it still states what it's about
      to do and to whom before doing it" is unqualified over outward writes
      proceeding in trust mode; disclosure is not confirmation, so this
      re-confirms nothing.
    - OUTWARD x WRITE x ambiguous x EXECUTE mode: PROCEED_WITH_DISCLOSURE —
      the headline cell: the declared trust mode still proceeds (the
      graduation the user asked for, unrevoked), but the outward act is
      said out loud first.
    - OUTWARD x DESTRUCTIVE: CONFIRM in every cell — outwardness never
      substitutes for, weakens, or doubles the #1190 tier (a second
      "always confirm" would be DESTRUCTIVE by another name — CXO).

    Why DESTRUCTIVE never weakens: #1190's PM ruling is blast-radius
    protection — an execute-mode user still confirms destructive actions
    (different failures need different protections), and a compose-phrased
    destructive ask gets the STRONGER check, not a draft chat that would
    drop the deferred-action carrier.

    Why WRITE+compose collaborates even in execute mode: executing a request
    for drafting HELP is the Jake failure again (#1510).

    Mode-consultation property (updated for the axis): PRIVATE consults the
    declared mode in exactly the WRITE x AMBIGUOUS cell (unchanged); OUTWARD
    WRITE additionally consults it on execute framing (the disclosure hangs
    on whether trust mode is declared). Every other cell is mode-invariant —
    asserted in tests.
    """
    from services.intent_service.collaboration_gate import (
        FRAMING_COMPOSE,
        FRAMING_EXECUTE,
        WorkingMode,
    )

    if effect == EffectClass.DESTRUCTIVE:
        return ConsentDecision.CONFIRM
    if effect == EffectClass.READ:
        return ConsentDecision.PROCEED
    # WRITE — explicit framing wins both ways; ambiguity goes to the mode.
    if framing == FRAMING_COMPOSE:
        return ConsentDecision.COLLABORATE
    if framing == FRAMING_EXECUTE:
        if (
            outwardness == Outwardness.OUTWARD
            and mode is WorkingMode.EXECUTE
        ):
            return ConsentDecision.PROCEED_WITH_DISCLOSURE
        return ConsentDecision.PROCEED
    # AMBIGUOUS framing — the declared mode decides.
    if mode is WorkingMode.EXECUTE:
        if outwardness == Outwardness.OUTWARD:
            return ConsentDecision.PROCEED_WITH_DISCLOSURE
        return ConsentDecision.PROCEED
    return ConsentDecision.COLLABORATE


def effect_for_action(action: Optional[str]) -> Optional[EffectClass]:
    """The action's DECLARED effect, from the workflow registry (#1557: effect
    is declared once at the source; consumers look it up, never infer it from
    names). None for unregistered/off-rail actions — an action with no
    declared effect has no consent derivation here (its dispatch surface owns
    that gap; see the module docstring's legacy-chain note in the report).
    """
    if not action:
        return None
    from services.intent_service.workflow_dispatcher import get_action_workflows
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()  # idempotent; no-op when already registered
    entry = get_action_workflows().get(action)
    return entry.effect if entry is not None else None


def outwardness_for_action(action: Optional[str]) -> Optional[Outwardness]:
    """The action's DECLARED outwardness, from the workflow registry — the
    #1509 axis rides with the effect declaration (WorkflowEntry.outwardness);
    consumers look it up, never infer it from names (the effect_for_action
    contract, extended). None for unregistered/off-rail actions."""
    if not action:
        return None
    from services.intent_service.workflow_dispatcher import get_action_workflows
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()  # idempotent; no-op when already registered
    entry = get_action_workflows().get(action)
    return entry.outwardness if entry is not None else None


async def evaluate_consent(
    effect: EffectClass,
    message: Optional[str],
    user_id: Optional[str],
    outwardness: Outwardness = Outwardness.PRIVATE,
) -> ConsentDecision:
    """The async wrapper the seams call: framing from the message, declared
    mode loaded ONLY for the cells that consult it — WRITE x AMBIGUOUS
    (unchanged), plus OUTWARD WRITE x EXECUTE framing (#1509 axis: the
    disclosure hangs on whether a trust mode is declared).
    READ/DESTRUCTIVE turns never touch storage (preserves #1190's
    no-DB-touch property on destructive turns), and PRIVATE
    explicitly-framed turns still never touch storage. Honest scope change:
    the #1510 no-DB-touch note this docstring used to make about
    "explicitly-framed create turns" no longer holds — the create family is
    OUTWARD, so an outward imperative now reads the mode preference. That is
    the cost of knowing whether to say the act out loud, and it is one
    fail-safe preference read (get_working_mode degrades to collaborate-mode
    semantics on storage error, which for an execute-framed WRITE is plain
    PROCEED — an error can drop the disclosure, never the action's gate).
    """
    from services.intent_service.collaboration_gate import (
        FRAMING_AMBIGUOUS,
        FRAMING_EXECUTE,
        WorkingMode,
        classify_framing,
        get_working_mode,
    )

    framing = classify_framing(message)
    consults_mode = effect == EffectClass.WRITE and (
        framing == FRAMING_AMBIGUOUS
        or (outwardness == Outwardness.OUTWARD and framing == FRAMING_EXECUTE)
    )
    if consults_mode:
        mode = await get_working_mode(user_id)
    else:
        mode = WorkingMode.COLLABORATE  # unread by decide_consent for these cells
    return decide_consent(effect, framing, mode, outwardness=outwardness)


# ---------------------------------------------------------------------------
# The generic consent-check turn (non-draft actions) — #1190 carrier reuse
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ConsentCheckOffer:
    """What the rail seam stores + asks for a held non-draft WRITE action:
    the check question for this turn, and the pending-offer record in #1190's
    action-agnostic ``pending_action`` carrier shape — acceptance re-dispatches
    the ORIGINAL intent via the existing confirm_pending_action workflow."""

    question: str
    offer: Dict[str, Any]


def _summary_for(intent) -> str:
    """Plain-words action summary for the check copy (the #1190 phrasing
    convention), with the parsed issue number appended when the action is
    issue-shaped and the message carries one — same cheap parse the #1190
    gate uses; never a new read."""
    action = intent.action or "do that"
    summary = action.replace("_", " ")
    if "issue" in action or "ticket" in action:
        message = ""
        if intent.context:
            message = intent.context.get("original_message", "") or ""
        if not message:
            message = intent.original_message or ""
        match = re.search(r"#?(\d+)", message)
        if match:
            summary += f" #{match.group(1)}"
    return summary


def build_consent_check_offer(intent, effect: EffectClass) -> ConsentCheckOffer:
    """Build the consent-check turn for a held WRITE-effect rail action.

    Composes with — never parallels — the existing machinery:
    - The offer IS a #1190 ``pending_action`` record dispatched through
      ``CONFIRM_PENDING_ACTION_WORKFLOW`` on "yes" (original intent, original
      params, never re-classified). "no"/bare-exit cancels honestly via the
      same decline path; off-intent abandons via the pop.
    - The effect phrase is derived from the declared EffectClass
      (``capability_legibility.describe_effect``), so the user sees WHY this
      action warranted a check (#1509 legibility: the check names its reason).
    - The graduation teaching phrase is the #1510 declaration-surface
      phrasing — a phrase that genuinely routes (pinned in tests); the copy
      never teaches a phrase that doesn't (#1571).

    ⚠️ COPY SEAM: the wording below is Lead-drafted mechanism copy. CXO owns
    the voice of this surface; adjust wording here (one place), not at call
    sites.
    """
    from services.intent_service.capability_legibility import describe_effect
    from services.intent_service.destructive_confirm import (
        CONFIRM_PENDING_ACTION_WORKFLOW,
    )

    summary = _summary_for(intent)
    question = (
        f"Quick check before I act: I'm reading that as asking me to {summary}, "
        f"which {describe_effect(effect)}. Should I go ahead? (yes/no)\n\n"
        "(If you'd rather I just act on requests like this without checking, "
        'say "just do things directly from now on.")'
    )
    return ConsentCheckOffer(
        question=question,
        offer={
            "workflow_type": CONFIRM_PENDING_ACTION_WORKFLOW,
            # #1665: the rendered ask rides the record — same string the rail
            # seam returns as the turn's message (built once, above), so the
            # SessionSnapshot's pending_offer_question never drifts from what
            # the user saw.
            "question": question,
            "pending_action": {
                # "kind" lets the offer seam log an abandoned consent check
                # under its own name (honest observability); the acceptance
                # path ignores it — the carrier contract (action + intent +
                # summary) is #1190's, unchanged.
                "kind": CONSENT_CHECK_KIND,
                "action": intent.action,
                "intent": intent,
                "summary": summary,
            },
            "decline_message": (
                f"Okay — I won't {summary}. Nothing has been changed."
            ),
        },
    )


# ---------------------------------------------------------------------------
# #1509 outwardness axis — the TRUST-mode disclosure line (say it out loud)
# ---------------------------------------------------------------------------


def build_outward_disclosure(intent) -> str:
    """The disclosure line for an OUTWARD WRITE proceeding under a declared
    trust mode (PROCEED_WITH_DISCLOSURE) — states WHAT is about to happen and
    TO WHOM, in the transcript, ahead of the handler's own result.

    NOT a gate (CXO's mechanism ruling): nothing is held, nothing asks yes/no
    — the same "say it out loud" pattern as #1605's stored-default variant-2
    disclosure. The summary reuses ``_summary_for`` (the #1190 phrasing
    convention — same plain words, same cheap issue-number parse; never a new
    read), and the repository renders only when the classified intent's
    context already carries one — this builder never performs a lookup to
    decorate a transparency line.

    ⚠️ COPY SEAM: Lead-drafted mechanism copy. CXO owns the voice of this
    surface; adjust wording here (one place), not at call sites.
    """
    summary = _summary_for(intent)
    repository = None
    if intent.context:
        repository = intent.context.get("repository") or intent.context.get("repo")
    where = f" in {repository}" if repository else ""
    return (
        f"Saying it out loud before I act: I'm about to {summary}{where} — "
        "that lands in front of other people, not just the two of us."
    )


# ---------------------------------------------------------------------------
# PM 2026-08-13 ruling — unmapped verbs over stateful operations ASK,
# effect-weighted (decisions.log ~14:1x; implementation slots (b)+(c))
# ---------------------------------------------------------------------------


def decide_verb_interpretation(
    confidence: float,
    candidate_effect: EffectClass,
    meta_mode: Optional["VerificationMetaMode"] = None,  # noqa: F821
) -> "VerificationDecision":  # noqa: F821
    """Effect-weighted verb-interpretation gate: the #1510 rail's
    low-confidence read-back applied to VERB mapping (PM's slot (c)), with
    the ask EFFECT-WEIGHTED per #1557 (PM's slot (b)):

    - ambiguous-toward-READ may best-effort ("wrong list != lost data"):
      a READ-candidate mapping above the suggestion floor auto-applies —
      unless the user explicitly said "don't make assumptions" (ALWAYS_ASK),
      which stays the stronger signal.
    - ambiguous-toward-WRITE asks exactly per the rail's ruled behavior
      (``verified_inference.decide`` unchanged — one scoring system).
    - ambiguous-toward-DESTRUCTIVE always asks below the auto-apply bar,
      even under a "stop asking me" meta-preference — the same principle as
      #1190's mode-proof CONFIRM: a wrong destructive mapping deletes data,
      so process-steering never lowers this ask.

    DISCARD below the suggestion floor is mode- and effect-independent (too
    weak to surface; a property of the inference, not the process).

    Full matrix (denominator: 3 effects x 3 meta modes x 3 confidence bands
    = 27 cells) asserted in test_consent_gate_1509.TestVerbInterpretation.

    Deliberately NOT wired to #1605's reminder-clear offer here — PM's slot
    (a) is PPM/CXO-held design, Lead builds when sequenced. This is the
    mechanism that build consumes.
    """
    from services.intent_service.verified_inference import (
        VerificationDecision,
        VerificationMetaMode,
        decide,
        is_low_confidence,
    )

    mode = meta_mode or VerificationMetaMode.DEFAULT
    base = decide(confidence, mode)
    if base is VerificationDecision.DISCARD:
        return base
    if (
        candidate_effect == EffectClass.READ
        and mode is not VerificationMetaMode.ALWAYS_ASK
    ):
        return VerificationDecision.AUTO_APPLY
    if candidate_effect == EffectClass.DESTRUCTIVE and is_low_confidence(confidence):
        return VerificationDecision.READ_BACK
    return base
