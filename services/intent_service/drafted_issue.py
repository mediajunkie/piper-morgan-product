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

Deliberately NOT built (flagged for Lead): multi-turn draft refinement. A
refinement turn ("add steps to reproduce…") is off-intent to the one-slot
carrier and abandons the binding — carrying an evolving floor-composed draft
across turns needs a durable draft store and is a different design (the
routing-moratorium/corpus half of #1571 lives there too).
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
    if file_cmd is None and detect_offer_response(message) != "accept":
        return None  # decline / bare-exit / off-intent → generic flow

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
