"""#1190 — multi-turn confirmation gate for DESTRUCTIVE rail actions.

PM ruling (decisions.log 2026-08-10 ~10:55): close_issue / reopen_issue are
DESTRUCTIVE (blast-radius protection — a close removes the issue from every
open-state board and query at once; the 2026-07 auto-close incident closed a
live Beta Blocker from a commit message). A classified intent whose rail
entry derives ``needs_confirm`` (== EffectClass.DESTRUCTIVE) must NOT
execute on the turn it was classified: the gate registers a pending action
and asks one clear yes/no question instead.

WHERE THE GATE SITS (routing-fix moratorium, Lead 2026-08-08): at the ACTION
layer, post-classification — the #1124 rail dispatch seam in
``IntentService.process_intent`` (the ``intent.action in
get_action_workflows()`` branch). No pre-classifier or prompt changes. The
#1510 collaborate-gate (compose-vs-execute working mode, upstream of
creates) is ORTHOGONAL: an execute-mode user still confirms destructive
actions — different failures need different protections (PPM).

HOW THE CONFIRMATION RIDES THE EXISTING SEAM (#846 / #1529 — verified by
reading, not invented in parallel):

- The confirmation IS a pending offer in ``WorkflowOfferService``'s
  session-scoped store (#846 — deliberately session-keyed, one-turn-shaped).
  No parallel store exists or is permitted.
- ``process_intent`` pops the pending offer BEFORE classification and before
  the process-resume check, so the #1529 offer-binding ordering (pending
  offer beats resume-check) holds for confirmations by construction.
- "yes" → the acceptance path dispatches ``workflow_type`` — here the
  CONFIRM_PENDING_ACTION_WORKFLOW entry — whose entry point re-dispatches
  the ORIGINAL rail action with the ORIGINAL classified Intent (resolved
  params intact). The "yes" itself is NEVER re-classified.
- "no" / refusal → the decline path returns the stored honest-cancel copy;
  nothing fires. Bare #888/#1529 exit commands ("cancel", "stop", "forget
  it") count as refusal via :func:`detect_bare_exit` — the #1529 exit tier
  applied to a one-turn offer.
- Any other message (off-intent) → the pop already cancelled the pending
  action (nothing can fire it later), and normal processing answers the new
  message — the #1529 off_intent tier ("let normal processing answer").

PENDING-ACTION RECORD SHAPE (the generic deferred-action carrier, Part 3):

    {
        "workflow_type": CONFIRM_PENDING_ACTION_WORKFLOW,
        "question": str,   # #1665: the ALREADY-RENDERED ask the user saw this
                           # turn — stored verbatim at arm time (never
                           # re-rendered later) so the SessionSnapshot's
                           # pending_offer_question can never drift from what
                           # was actually said. Optional on the shape; every
                           # arm site populates it.
        "pending_action": {
            "kind": str,       # offer family (#1664: confirm-ness derives from
                               # this — see offer_is_confirm below); this
                               # module's records carry DESTRUCTIVE_CONFIRM_KIND
            "action": str,     # rail key to dispatch on "yes" (e.g. "close_issue")
            "intent": Intent,  # ORIGINAL classified Intent — resolved params
                               # (issue number, repo context, principal) intact
            "summary": str,    # human phrase ("close issue #123 'title'"),
                               # reused in the question and the cancel copy
        },
        "decline_message": str,  # honest-cancel copy for the "no" path
    }

The carrier is deliberately action-agnostic: ``pending_action`` can hold ANY
deferred rail action + its params — acceptance always re-dispatches
``action`` with ``intent`` through the workflow registry. #1571's
drafted-issue binding SHIPPED as the second consumer (2026-08-15):
``services/intent_service/drafted_issue.py`` builds its own record (kind
``drafted_issue``) and delegates acceptance to the same
``run_confirm_pending_action_workflow`` mirror.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, Optional

import structlog

from services.domain.models import Intent

logger = structlog.get_logger(__name__)

# Registered in workflow_entries.register_default_workflows with
# action_triggered=False: the classifier can never emit it; only the
# offer-acceptance seam dispatches it.
CONFIRM_PENDING_ACTION_WORKFLOW = "confirm_pending_action"

# #1664: the destructive-confirmation records this module builds now carry a
# kind of their own (they were the one kindless #846 producer), so confirm-ness
# can be derived from the offer KIND instead of the carrier workflow_type —
# repo clarification rides the same carrier with a non-yes/no open question,
# and deriving from the carrier mislabeled it "(yes/no confirm)".
DESTRUCTIVE_CONFIRM_KIND = "destructive_action_confirmation"

# ---------------------------------------------------------------------------
# #1664 — is_confirm derives from the offer KIND, in ONE place.
#
# The #1650 confirm-kind table (soft_invocation's CONFIRM-tier comment +
# intent_service's offer-seam enumeration): the offer kinds whose OPEN
# QUESTION is a yes/no — an accept FIRES a held action, so they ride the
# strict detect_confirm_response detector. Exactly this set:
#
#   - destructive close/reopen confirms ..... DESTRUCTIVE_CONFIRM_KIND (here)
#   - reminder-clear delete confirms ........ reminder_clear.CLEAR_DELETE_CONFIRMATION_KIND
#   - consent checks ........................ consent_gate.CONSENT_CHECK_KIND
#   - unmapped-status-value close confirm ... intent_service._offer_status_close_clarification
#         (a destructive close confirm by another name — its copy is literally
#         "...? (yes/no)" and "yes" dispatches close_issue)
#   - drafted-issue FILE confirm ............ drafted_issue.DRAFTED_ISSUE_KIND,
#         but ONLY in the ready-to-file state (title AND body present) — the
#         mid-compose states' open question is "what's it about?"/"what should
#         the body say?", which is NOT a yes/no
#   - closed-default repo bind .............. repo_clarification.REPO_QUESTION_KIND,
#         but ONLY with a default on offer (payload["default_repo"]) — a crisp
#         "yes" then binds the default and FIRES the held operation; the OPEN
#         repo question ("Which repository...?") is NOT a yes/no (issue 1664's
#         literal defect)
#
# The kind strings are literals here (their home modules import THIS module,
# so importing theirs back would be circular); the #1664 tests pin each
# literal against its source constant so drift fails loudly.
_CONFIRM_KINDS = frozenset(
    {
        DESTRUCTIVE_CONFIRM_KIND,
        "reminder_clear_delete_confirmation",  # reminder_clear.CLEAR_DELETE_CONFIRMATION_KIND
        "consent_check",  # consent_gate.CONSENT_CHECK_KIND
        "unmapped_field_value_clarification",  # intent_service._offer_status_close_clarification
    }
)

_DRAFTED_ISSUE_KIND = "drafted_issue"  # drafted_issue.DRAFTED_ISSUE_KIND
_REPO_QUESTION_KIND = "issue_repo_question"  # repo_clarification.REPO_QUESTION_KIND


def offer_is_confirm(offer: Optional[Dict[str, Any]]) -> bool:
    """#1664 — is the pending offer's open question a yes/no confirm?

    Derived from the offer KIND per the #1650 confirm-kind table (enumerated
    above), never from the carrier workflow_type: repo clarification rides
    CONFIRM_PENDING_ACTION_WORKFLOW with an open "Which repository...?" ask,
    so carrier-derived confirm-ness lied to the router about what kind of
    answer is expected. The two state-dependent rows (drafted-issue file
    confirm, closed-default repo bind) read the payload fields that define
    the state; everything else is a set membership.

    One deliberate fallback: a carrier record with NO kind at all reads as a
    confirm — the only kindless #846 producer was ever this module's own
    destructive-confirmation builder (which now stamps its kind), so a stale
    in-flight record still renders honestly instead of losing its confirm
    marker.
    """
    if not offer:
        return False
    pending = offer.get("pending_action") or {}
    kind = pending.get("kind")
    if kind in _CONFIRM_KINDS:
        return True
    if kind == _DRAFTED_ISSUE_KIND:
        # File confirm only when the draft is fully shaped: with title AND
        # body present the open ask is 'say "file it as is"' — a yes/no.
        # Mid-compose (either slot empty) the open ask is the compose
        # question, and a crisp "yes" is re-asked, not fired blind.
        draft = pending.get("draft") or {}
        return bool(
            (draft.get("title") or "").strip() and (draft.get("body") or "").strip()
        )
    if kind == _REPO_QUESTION_KIND:
        # Closed-default bind only: with a default on offer, a crisp "yes"
        # binds it and fires the held operation (#1650). The open form's
        # "yes" merely re-asks — not a confirm.
        return bool(pending.get("default_repo"))
    return (
        kind is None
        and offer.get("workflow_type") == CONFIRM_PENDING_ACTION_WORKFLOW
    )

# Context marker the confirm entry point sets before re-dispatching, so the
# close/reopen handlers' own in-message confirmation (#902's "yes, close
# #123" regex) recognizes the rail confirmation and executes in ONE turn
# instead of asking a second time.
CONFIRMED_CONTEXT_KEY = "destructive_confirmed"

# Rail-key families whose handlers were READ (verify-first, 2026-08-10) to
# take every mutating call ONLY after a successful issue-number parse: with
# no number in the message, both handlers run fuzzy-match / clarification
# paths that never write. For those messages the gate passes through — there
# is no blast radius to confirm, and the handler's clarification copy is the
# better turn. ⚠️ Invariant: if either handler ever writes on its no-number
# path, this pass-through must be removed in the same commit.
_CLOSE_FAMILY = frozenset({"close_issue", "close_issue_query"})
_REOPEN_FAMILY = frozenset({"reopen_issue", "reopen_issue_query"})

# Bare full-message exits that cancel a pending confirmation honestly —
# the #888 registry set ∪ the #1529 additions, applied at the offer seam.
# (detect_offer_response's DECLINE_PATTERNS already catch "no"/"nope"/
# "not now"/"never mind"; this covers the exit-verb shapes it misses.)


def _bare_exit_commands() -> frozenset:
    from services.process.escape import BARE_EXIT_COMMANDS
    from services.process.registry import ESCAPE_COMMANDS

    return ESCAPE_COMMANDS | BARE_EXIT_COMMANDS | frozenset({"abort", "don't", "dont"})


def detect_bare_exit(message: str) -> bool:
    """True when the whole message is a bare exit command ("cancel", "stop",
    "forget it") — the #1529 exit tier for a pending confirmation. Exact
    match on the stripped, lowercased full message (Arch guidance on #888)."""
    if not message:
        return False
    return message.strip().lower().rstrip(".!?") in _bare_exit_commands()


@dataclass(frozen=True)
class ConfirmationOffer:
    """What the gate hands back: the question to ask this turn, and the
    pending-offer record (shape documented in the module docstring) to store
    in the #846 session-scoped store."""

    question: str
    offer: Dict[str, Any]


def _issue_number_from(intent: Intent) -> Optional[int]:
    """The same parse the handlers use (their first mutating step is gated on
    it): first ``#N`` / bare number in the original message."""
    message = ""
    if intent.context:
        message = intent.context.get("original_message", "") or ""
    if not message:
        message = intent.original_message or ""
    match = re.search(r"#?(\d+)", message)
    return int(match.group(1)) if match else None


def _issue_title_from(intent: Intent) -> Optional[str]:
    """Cheap-read-only title lookup (#1190 spec: fetch the title only if a
    read is ALREADY available on the path — never issue a new call here).
    Present when an upstream turn (e.g. the #902 fuzzy-match flow) stashed it."""
    if not intent.context:
        return None
    return intent.context.get("issue_title") or intent.context.get("matched_issue_title")


def build_confirmation_offer(intent: Intent) -> Optional[ConfirmationOffer]:
    """Build the confirmation question + pending-action record for a
    DESTRUCTIVE rail intent, or ``None`` to pass through to the handler.

    ``None`` is returned ONLY for the two verified read-only-clarification
    shapes (close/reopen with no parseable issue number — see the
    ``_CLOSE_FAMILY`` invariant note). Unknown destructive actions ALWAYS
    defer (safe default: an unconfirmed destructive write must never fire).
    """
    action = intent.action
    issue_number = _issue_number_from(intent)

    if action in _CLOSE_FAMILY or action in _REOPEN_FAMILY:
        if issue_number is None:
            # Verified read-only clarification path — nothing destructive can
            # fire without a number; let the handler ask "which issue?".
            return None
        verb = "close" if action in _CLOSE_FAMILY else "reopen"
        title = _issue_title_from(intent)
        summary = f"{verb} issue #{issue_number}"
        if title:
            summary += f" '{title}'"
        question = f"{summary[0].upper()}{summary[1:]}? (yes/no)"
    else:
        # Generic carrier: a future destructive rail action lands here with a
        # generic (but honest) question. Refine per-action summaries as
        # consumers arrive.
        # #1571 SHIPPED (2026-08-15): the drafted-issue binding is the
        # carrier's second consumer — it builds its own record in
        # services/intent_service/drafted_issue.py (kind "drafted_issue",
        # armed at the #1510 collaborate turn, accepted via the same
        # run_confirm_pending_action_workflow mirror), not through this
        # builder, which stays destructive-classification-only.
        summary = action.replace("_", " ")
        question = f"Are you sure you want me to {summary}? (yes/no)"

    return ConfirmationOffer(
        question=question,
        offer={
            "workflow_type": CONFIRM_PENDING_ACTION_WORKFLOW,
            # #1665: the rendered ask rides the record — same string the
            # caller returns as the turn's message (built once, above).
            "question": question,
            "pending_action": {
                "kind": DESTRUCTIVE_CONFIRM_KIND,
                "action": action,
                "intent": intent,
                "summary": summary,
            },
            "decline_message": (
                f"Okay — I won't {summary}. Nothing has been changed."
            ),
        },
    )
