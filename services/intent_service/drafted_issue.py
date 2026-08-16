"""#1571 — the drafted-issue pending binding (the #1190 carrier's named next consumer).

PM's live sequence (verdict-7 tail 2026-08-10; repro'd in the 2026-08-15
baseline): the compose flow builds a draft, PM says "Please file it as is" —
and then: double-confirm friction ("want me to go ahead?"), a FABRICATED
"Filed! … #[issue number]" with the template placeholder showing, and a retry
that LOST the whole draft ("What should the issue be about?").

The fix binds the draft the moment the #1510 collaborate gate renders it:

- The collaborate turn in ``_handle_create_issue`` ARMS a pending action in
  the #846 session-scoped offer store (kind ``drafted_issue``) carrying the
  ORIGINAL classified Intent — the same deferred-action carrier shape #1190
  documents in ``destructive_confirm.py`` (whose ``TODO(#1571)`` names this
  module as the next consumer).
- "file it" / "file it as is" / "please file it" / a generic accept IS the
  confirmation — ONE turn, no second ask. Acceptance delegates to
  ``run_confirm_pending_action_workflow`` (the #1190 acceptance mirror): the
  original Intent is re-dispatched through the create_issue rail entry with
  the ``destructive_confirmed`` context marker, which the collaborate gate
  now honors as consent-already-given (the #1509 principle: the explicit
  confirmation IS the consent — never ask twice).
- Success copy derives from the ACTUAL tool result (the rail handler's
  "Created issue #N in repo: title" — the number comes from GitHub's
  response), never a template slot.
- FAILURE keeps the draft bound: any outcome that did not verifiably create
  (dispatch error, degraded-connector copy, clarification ask) re-arms the
  SAME pending record and says so honestly — retry does not lose the draft.
- Off-intent abandons per the carrier's rules (the pop already removed the
  offer; normal processing answers the new message). Declines/bare exits
  drop the draft with honest copy via the generic decline path.

#1627 (2026-08-15, round 2): while the draft's open question ("What should
the body say…?") is on the table, a PROSE ANSWER binds to the draft — it is
consumed at this seam (which runs above the whole 4-surface routing chain)
and never reaches any classification surface. The live theft: PM's long
body answer contained "delete …" and "(a destructive action)", and surface
1's greedy portfolio pattern (#1527 family, ``\\bdelete\\s+…(.+)``) claimed
the turn — "I couldn't find a project called '(a destructive action)…'" —
losing the composed body. The draft flow is floor-composed prose, not a
registered gathering process, so the #1623 mid-interview hold could not
cover it; this is the draft flow's own hold. It is NOT a turn lock:
file/accept phrases still file, declines and bare exits still drop the
draft honestly, and clearly-imperative asks still route normally
(abandoning the draft — the carrier's documented off-intent rule). See
``is_body_prose_answer`` for the discrimination and its stated limits.

Deliberately NOT built (flagged for Lead): instruction-shaped draft
refinement ("make the title snappier", "add a labels section"). #1627 binds
prose CONTENT (appended to the body verbatim); it does not interpret
editing instructions — an anchored-imperative refinement ask still abandons
the binding. Interpreting edits over an evolving floor-composed draft needs
a durable draft store and is a different design (the
routing-moratorium/corpus half of #1571 lives there too; durable fix is
Inversion Phase 2 context-carrying).
"""

from __future__ import annotations

import re
from typing import Any, Dict, Optional

import structlog

from services.domain.models import Intent
from services.intent_service.destructive_confirm import (
    CONFIRM_PENDING_ACTION_WORKFLOW,
)

logger = structlog.get_logger(__name__)

DRAFTED_ISSUE_KIND = "drafted_issue"

# Full-message file commands (the phrases PM was TAUGHT and the phrases PM
# actually typed). Conservative: verb + a draft-referring object, optional
# "as is" tail, optional politeness, optional "in owner/repo" (the original
# #1571 incident phrase — with a draft pending it is unambiguous and the
# named repo overrides the draft's). Anchored full-message so a NEW ask
# ("file an issue about X") never reads as accepting the old draft.
_FILE_COMMAND_RE = re.compile(
    r"^(?:please\s+)?(?:go\s+ahead\s+(?:and\s+)?)?"
    r"(?:file|create|submit|open)\s+"
    r"(?:it|this|that|the\s+(?:issue|ticket|draft))"
    r"(?:\s+as[\s\-]is)?"
    r"(?:\s+in\s+(?P<repo>[\w.\-]+/[\w.\-]+))?"
    r"(?:\s*,?\s*please)?\s*[.!]*$",
    re.IGNORECASE,
)


def detect_file_command(message: Optional[str]) -> Optional[Dict[str, Any]]:
    """Return ``{"repo": <override-or-None>}`` when the whole message is a
    file-this-draft command; ``None`` otherwise."""
    if not message:
        return None
    m = _FILE_COMMAND_RE.match(message.strip())
    if not m:
        return None
    return {"repo": m.group("repo")}


# --- #1627: mid-compose prose binding --------------------------------------

# A turn at/above this length (or any multi-line turn) is prose regardless of
# how it opens. Body answers often LEAD with an imperative-looking verb ("Add
# a guard so that deleting a project…") or a politeness word the unanchored
# accept row would claim ("Please note that…"); commands are short and
# single-line — nobody types 200 characters of "close issue #108". The floor
# is deliberately above every taught command phrase and below PM's live
# stolen answer by a wide margin.
_PROSE_LENGTH_FLOOR = 160

# Anchored-imperative supplement: verb families the shared collaborate-gate
# execute check (collaboration_gate._EXECUTE_RE) deliberately omits — reads
# and destructives are consented elsewhere, so that regex never needed them.
# Mid-compose they are exactly the "clearly imperative unrelated ask" that
# must keep routing normally ("close issue #108", "list my reminders",
# "delete my reminders" — the #1527 phrase itself, as a command). Prefix
# structure mirrors _EXECUTE_RE's (politeness/address, go-ahead, can-you).
_COMMAND_SUPPLEMENT_RE = re.compile(
    r"^\s*"
    r"(?:(?:please|hey|hi|ok(?:ay)?|piper)[,!\s]+)*"
    r"(?:go\s+ahead\s+and\s+)?"
    r"(?:(?:can|could|would|will)\s+you\s+(?:please\s+)?)?"
    r"(?:close|reopen|delete|remove|archive|restore|cancel|stop"
    r"|list|show|search|find|fetch|get|check|tell|give)\b",
    re.IGNORECASE,
)


def is_body_prose_answer(message: Optional[str]) -> bool:
    """#1627 — with a drafted issue armed and its body question open, is this
    turn a prose ANSWER (bind to the draft) rather than a deliberate exit or
    an explicit command (fall through to the generic flow / normal routing)?

    Deterministic, and deliberately biased toward binding: a mis-bound
    command is recoverable (the draft re-arms, nothing files, the copy shows
    exactly what was captured), while a mis-routed body answer loses the
    composed prose to whichever greedy surface claims it — the live #1627
    failure. Known limits, stated honestly:

    - A SHORT turn that opens with an imperative verb from either anchored
      check ("add steps to reproduce") reads as a command and abandons the
      draft — instruction-shaped refinement is deliberately not built (see
      module docstring).
    - A question mid-compose ("what would make a good body?") is not an
      anchored imperative, so it BINDS as body text rather than being
      answered. Visible and recoverable; the alternative (routing it)
      silently abandons the draft.
    - A LONG turn that is genuinely a new imperative ask binds as prose —
      the length override is what protects body answers that open with
      "Please…"/"Add…", and it cannot tell those apart from a 200-character
      command. Interim guard; the durable fix is Inversion Phase 2
      context-carrying.
    """
    text = (message or "").strip()
    if not text:
        return False
    from services.intent_service.destructive_confirm import detect_bare_exit

    if detect_bare_exit(text):
        return False  # "cancel" / "stop" / "forget it" → honest decline
    if "\n" in text or len(text) >= _PROSE_LENGTH_FLOOR:
        # Checked BEFORE the accept/decline consult on purpose: the
        # unanchored accept/decline rows ("^please\s", "\bnot today\b")
        # match into long prose and would file or drop a half-shaped draft
        # off a substring of the body answer.
        return True
    from services.intent_service.soft_invocation import detect_offer_response

    if detect_offer_response(text) is not None:
        return False  # short accept/decline — the generic seam's business
    from services.intent_service.collaboration_gate import (
        FRAMING_EXECUTE,
        classify_framing,
    )

    if classify_framing(text) == FRAMING_EXECUTE:
        return False  # anchored imperative (create/update/remind families)
    if _COMMAND_SUPPLEMENT_RE.match(text):
        return False  # anchored imperative (close/read/destructive families)
    return True


def build_drafted_issue_offer(
    intent: Intent,
    subject: str,
    repository: Optional[str] = None,
) -> Dict[str, Any]:
    """The #846 pending-offer record binding a rendered draft (the generic
    deferred-action carrier shape documented in ``destructive_confirm.py``)."""
    summary = f'file the drafted issue "{subject}"'
    if repository:
        summary += f" in {repository}"
    return {
        "workflow_type": CONFIRM_PENDING_ACTION_WORKFLOW,
        "pending_action": {
            "kind": DRAFTED_ISSUE_KIND,
            "action": intent.action,
            "intent": intent,
            "summary": summary,
            "draft": {"title": subject, "repository": repository},
        },
        "decline_message": (
            "Okay — I've set that draft aside. Nothing was filed. "
            "Ask me again anytime if you want to shape it back up."
        ),
    }


_DRAFT_RETAINED_LINE = (
    "Your draft is still here — say \"file it\" to try again, "
    "or \"no\" to drop it."
)


def _retained_intent_data(pending_action: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "category": "execution",
        "action": pending_action.get("action") or "create_issue",
        "confidence": 1.0,
        "drafted_issue_pending": True,  # _apply_soft_offer clobber guard
        "drafted_issue_retained": True,
    }


def _bind_body_prose(
    pending_offer: Dict[str, Any],
    pending_action: Dict[str, Any],
    prose: str,
    *,
    session_id: str,
    user_id: Optional[str],
    intent_service: Any,
) -> Dict[str, Any]:
    """#1627 — append a prose answer to the bound draft's body, re-arm the
    SAME offer, and show the draft honestly. Consuming the turn here is the
    hold: no classification surface ever sees the prose."""
    draft = pending_action.setdefault("draft", {})
    existing = (draft.get("body") or "").strip()
    body = f"{existing}\n\n{prose.strip()}" if existing else prose.strip()
    draft["body"] = body

    # The filing path reads intent.context["description"] first
    # (_handle_create_issue's description precedence), so the bound body is
    # what actually lands in the created issue — a binding that didn't file
    # would be the #1571 original defect (teaching a phrase with nothing
    # behind it) wearing a new hat.
    intent = pending_action.get("intent")
    if intent is not None:
        intent.context = dict(intent.context or {})
        intent.context["description"] = body

    rearmed = True
    try:
        intent_service.workflow_offer_service.set_pending_offer(
            session_id, pending_offer, user_id=user_id
        )
    except Exception as e:  # silent-ok: #1627 — a store failure must not crash the compose turn; logged ERROR, and the copy below never claims a bound draft that isn't there
        logger.error("drafted_issue_body_bind_rearm_failed", error=str(e))
        rearmed = False

    logger.info(
        "drafted_issue_body_prose_bound",
        session_id=session_id,
        body_chars=len(body),
        rearmed=rearmed,
    )

    if not rearmed:
        return {
            "message": (
                "I've got what you wrote, but I couldn't keep the draft "
                "bound — nothing was filed. Ask me to draft the issue "
                "again and we'll rebuild it, including what you just said."
            ),
            "intent_data": _retained_intent_data(pending_action),
        }

    title = draft.get("title") or "(untitled)"
    intent_data = _retained_intent_data(pending_action)
    intent_data["drafted_issue_body_bound"] = True
    return {
        "message": (
            "Added to the draft — nothing is filed yet. Here's where it "
            "stands:\n\n"
            f"**Title**: {title}\n\n"
            f"**Body**:\n{body}\n\n"
            "Keep going if there's more to add. When it's ready, say "
            '"file it as is" — or "no" to set the draft aside.'
        ),
        "intent_data": intent_data,
        "requires_clarification": True,
    }


async def handle_drafted_issue_turn(
    pending_offer: Dict[str, Any],
    message: str,
    *,
    session_id: str,
    user_id: Optional[str],
    intent_service: Any,
) -> Optional[Dict[str, Any]]:
    """Kind-specific turn handling for a pending drafted issue, run BEFORE
    the generic accept/decline detection (the #1605/#1510 sanctioned
    handler-internal seam — the pop already happened).

    Returns a ``{"message", "intent_data", ...}`` dict when this turn is
    consumed here; ``None`` to fall through to the generic offer flow
    (declines and bare exits drop honestly there via ``decline_message``;
    off-intent abandons per the carrier's rules).
    """
    from services.intent_service.soft_invocation import detect_offer_response

    pending_action = pending_offer.get("pending_action") or {}
    file_cmd = detect_file_command(message)
    if file_cmd is None:
        # #1627: a prose turn that answers the draft's open question BINDS
        # to the draft. Checked BEFORE the generic accept consult so the
        # unanchored accept rows ("^please\s", "^yes,?\s") can't file a
        # half-shaped draft off the front of a long body answer, and
        # returned BEFORE the off-intent fall-through so no classification
        # surface (surface 1's greedy portfolio pattern was the live thief)
        # ever sees body prose. Deliberate exits and explicit commands fall
        # through exactly as before — the hold is not a turn lock.
        if is_body_prose_answer(message):
            return _bind_body_prose(
                pending_offer,
                pending_action,
                message,
                session_id=session_id,
                user_id=user_id,
                intent_service=intent_service,
            )
        if detect_offer_response(message) != "accept":
            return None  # decline / bare-exit / explicit command → generic flow

    intent = pending_action.get("intent")
    if intent is None:
        logger.error("drafted_issue_missing_intent", session_id=session_id)
        return None

    # "file it in owner/repo" with a draft pending: the named repo wins.
    if file_cmd and file_cmd.get("repo"):
        intent.context = dict(intent.context or {})
        intent.context["repository"] = file_cmd["repo"]

    # The #1190 acceptance mirror — delegate, never a parallel dispatch path.
    from services.intent_service.workflow_entries import (
        run_confirm_pending_action_workflow,
    )

    result: Optional[Dict[str, Any]] = None
    try:
        result = await run_confirm_pending_action_workflow(
            session_id=session_id,
            user_id=user_id,
            context={
                "pending_action": pending_action,
                "intent_service": intent_service,
            },
        )
    except Exception as e:  # silent-ok: #1571 — a raised dispatch must NOT crash the confirmation turn (the draft would be lost, the exact live failure); logged ERROR + traceback, and the None path below re-arms the draft and tells the user honestly
        logger.error("drafted_issue_dispatch_raised", error=str(e), exc_info=True)
        result = None

    def _rearm() -> bool:
        """Failure keeps the draft bound — retry must not lose it. Returns
        False when the store write itself failed, so the copy never claims a
        retained draft that isn't there."""
        try:
            intent_service.workflow_offer_service.set_pending_offer(
                session_id, pending_offer, user_id=user_id
            )
            return True
        except Exception as e:  # silent-ok: #1571 — a store failure must not crash the turn; logged ERROR, and the False return keeps the user-facing copy honest (no false "draft is still here" claim)
            logger.error("drafted_issue_rearm_failed", error=str(e))
            return False

    def _retained_line(rearmed: bool) -> str:
        return _DRAFT_RETAINED_LINE if rearmed else (
            "I couldn't keep the draft bound either — ask me again and "
            "we'll re-draft it."
        )

    if result is None:
        rearmed = _rearm()
        logger.info("drafted_issue_create_failed_draft_retained", session_id=session_id, rearmed=rearmed)
        return {
            "message": (
                "I wasn't able to file that issue just now — nothing was "
                f"created. {_retained_line(rearmed)}"
            ),
            "intent_data": _retained_intent_data(pending_action),
        }

    intent_data = result.get("intent_data") or {}
    if intent_data.get("issue_number") is None:
        # The rail answered but did NOT verifiably create (degraded-connector
        # copy, clarification ask, honest failure). Pass its honest message
        # through and keep the draft bound.
        rearmed = _rearm()
        logger.info(
            "drafted_issue_create_unverified_draft_retained",
            session_id=session_id,
            rail_action=pending_action.get("action"),
            rearmed=rearmed,
        )
        merged = dict(intent_data)
        merged.update(_retained_intent_data(pending_action))
        return {
            "message": f"{result.get('message', '')}\n\n{_retained_line(rearmed)}".strip(),
            "intent_data": merged,
        }

    # Verified create — the success copy is the rail handler's own, derived
    # from the actual tool result (real number, real repo). Never a template
    # slot.
    logger.info(
        "drafted_issue_filed",
        session_id=session_id,
        issue_number=intent_data.get("issue_number"),
    )
    return result
