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

from services.shared_types import EffectClass

logger = logging.getLogger(__name__)


# Marker inside a consent-check pending_action payload (the #1190 carrier is
# action-agnostic; ``kind`` is how the offer seam names an abandoned check in
# its logs without a parallel store — the verify_inference convention).
CONSENT_CHECK_KIND = "consent_check"


class ConsentDecision(str, Enum):
    """What the consent boundary requires before this action may execute."""

    PROCEED = "proceed"  # framing/mode/effect carry consent — execute now
    COLLABORATE = "collaborate"  # engage the user first (draft/check turn)
    CONFIRM = "confirm"  # explicit yes/no required (#1190 destructive tier)


def decide_consent(
    effect: EffectClass,
    framing: str,
    mode: "WorkingMode",  # noqa: F821 — collaboration_gate.WorkingMode (import cycle)
) -> ConsentDecision:
    """THE consent decision — one function, consulted by every gate path.

    Full matrix (denominator: 3 effects x 3 framings x 2 modes = 18 cells,
    every cell asserted in test_consent_gate_1509.TestConsentDecisionMatrix):

    ==========  =========  ===========  ============
    effect      framing    COLLABORATE  EXECUTE mode
    ==========  =========  ===========  ============
    READ        compose    PROCEED      PROCEED
    READ        execute    PROCEED      PROCEED
    READ        ambiguous  PROCEED      PROCEED
    WRITE       compose    COLLABORATE  COLLABORATE
    WRITE       execute    PROCEED      PROCEED
    WRITE       ambiguous  COLLABORATE  PROCEED
    DESTRUCTIVE compose    CONFIRM      CONFIRM
    DESTRUCTIVE execute    CONFIRM      CONFIRM
    DESTRUCTIVE ambiguous  CONFIRM      CONFIRM
    ==========  =========  ===========  ============

    Why DESTRUCTIVE never weakens: #1190's PM ruling is blast-radius
    protection — an execute-mode user still confirms destructive actions
    (different failures need different protections), and a compose-phrased
    destructive ask gets the STRONGER check, not a draft chat that would
    drop the deferred-action carrier.

    Why WRITE+compose collaborates even in execute mode: executing a request
    for drafting HELP is the Jake failure again (#1510).

    Only the WRITE x AMBIGUOUS cell consults the declared mode — that is the
    "tied to the declared mode, not hardcoded per-verb" requirement.
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
        return ConsentDecision.PROCEED
    return (
        ConsentDecision.PROCEED
        if mode is WorkingMode.EXECUTE
        else ConsentDecision.COLLABORATE
    )


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


async def evaluate_consent(
    effect: EffectClass,
    message: Optional[str],
    user_id: Optional[str],
) -> ConsentDecision:
    """The async wrapper the seams call: framing from the message, declared
    mode loaded ONLY for the one cell that consults it (WRITE x AMBIGUOUS) —
    READ/DESTRUCTIVE and explicitly-framed turns never touch storage
    (preserves #1190's no-DB-touch property on destructive turns and
    #1510's on explicitly-framed create turns).
    """
    from services.intent_service.collaboration_gate import (
        FRAMING_AMBIGUOUS,
        WorkingMode,
        classify_framing,
        get_working_mode,
    )

    framing = classify_framing(message)
    if effect == EffectClass.WRITE and framing == FRAMING_AMBIGUOUS:
        mode = await get_working_mode(user_id)
    else:
        mode = WorkingMode.COLLABORATE  # unread by decide_consent for these cells
    return decide_consent(effect, framing, mode)


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
