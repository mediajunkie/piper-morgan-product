"""#2223: an armed offer is acted on only under the principal that armed it.

Arch's ruling (decisions.log 2026-10-30 10:36 PT, generalizing 2026-10-29
13:04, #2199, #2207, #2222). The #846 pending-offer store is session-keyed and
``/api/v1/intent`` takes optional auth, so a turn with no principal, or a
different one, can pop an offer an authenticated user armed. The generic accept
seam then dispatched the record's workflow, and ``confirm_pending_action``
re-dispatched the STORED Intent, whose context carries the arming user: the
held write ran under that user on a turn that authenticated nobody.

The rule, applied ONCE at the pop seam (``IntentService._process_intent_internal``,
right after ``get_and_clear_pending_offer``):

- The record's principal is every user id it names: ``pending_action["user_id"]``
  and the stored Intent's ``context["user_id"]`` (``pending_action["intent"]``).
- A record that names a principal is acted on only when the turn's
  authenticated principal equals it (all named ids must equal it).
- A None or different turn principal DROPS the offer: logged
  ``pending_offer_dropped_principal_mismatch`` (with a reason); no handler of
  the offer's kind runs, no generic accept or decline runs, nothing is
  rendered, and the turn routes normally (Arch 11:14 (1): the per-kind checks
  stay inside the handlers as defence in depth, but this check never calls
  them; a line, if CXO wants one, is one constant rendered at the drop).
- A record naming NO principal was armed anonymously. If its workflow declares
  a non-READ effect (``declared_axes_for_workflow``), only a turn with no
  principal acts on it; a signed-in turn drops it the same way (Arch 11:14
  (2)). A READ or undeclared workflow naming no principal (the soft
  ``meeting`` offer, the canonical ``action_required`` offers) behaves exactly
  as before.

The per-kind checks (#2199 milestone pick, #2207/#2222 repo question, the
#1532/#1605 mismatch checks) stay in place; this check runs first.
"""

from __future__ import annotations

from typing import Any, Dict, FrozenSet, Optional

import structlog

logger = structlog.get_logger(__name__)

# SHRINK-ONLY. Kinds of WRITE-effect offer whose arm site cannot record the
# arming principal, so the pop-seam check cannot protect them. Empty at #2223:
# every write-effect arm site records ``pending_action["user_id"]`` or carries
# the stored Intent (whose context holds the principal stamped at the host
# boundary). The two record shapes that name no principal are not write-effect:
# the soft workflow offer (``_apply_soft_offer``; only registered types arm,
# and the one registered soft type, ``meeting``, is READ) and the canonical
# ``action_required`` offer (``priority_check`` / ``project_setup`` / ``setup``,
# none registered, so an accept routes to the floor under the turn's own
# principal). An anonymous arm of a write offer names no principal because
# there is none; rule (2) in the module docstring covers it. Pinned by size in
# ``tests/unit/services/intent_service/test_offer_principal_2223.py``: a new
# entry needs Arch's ruling and a reason here, and the pin only goes down.
UNRECORDED_PRINCIPAL_WRITE_OFFER_KINDS: FrozenSet[str] = frozenset()


def _intent_context(intent: Any) -> Optional[Dict[str, Any]]:
    if intent is None:
        return None
    ctx = intent.get("context") if isinstance(intent, dict) else getattr(intent, "context", None)
    return ctx if isinstance(ctx, dict) else None


def recorded_offer_principals(record: Any) -> FrozenSet[str]:
    """Every user id the offer record names (empty when it names none)."""
    if not isinstance(record, dict):
        return frozenset()
    payload = record.get("pending_action")
    if not isinstance(payload, dict):
        return frozenset()
    found = set()
    if payload.get("user_id"):
        found.add(str(payload["user_id"]))
    ctx = _intent_context(payload.get("intent"))
    if ctx and ctx.get("user_id"):
        found.add(str(ctx["user_id"]))
    return frozenset(found)


def _declares_non_read_effect(record: Dict[str, Any]) -> bool:
    """True when the record's workflow has a declared effect that is not READ
    (``declared_axes_for_workflow``; an unregistered workflow declares none)."""
    from services.intent_service.acceptance import declared_axes_for_workflow
    from services.shared_types import EffectClass

    axes = declared_axes_for_workflow(record.get("workflow_type"))
    effect = axes[0] if axes else None
    return effect is not None and effect != EffectClass.READ


def principal_drop_reason(record: Any, turn_user_id: Optional[Any]) -> Optional[str]:
    """Why this turn may not act on the offer, or None when it may.

    - ``recorded_principal_mismatch``: the record names a principal and the
      turn's is None or different.
    - ``anonymous_write_offer_signed_in_turn``: the record names no principal
      (armed anonymously), its workflow declares a non-READ effect, and the
      turn has a principal (Arch 11:14 (2)).
    A record naming no principal whose workflow is READ or undeclared behaves
    as before."""
    if not isinstance(record, dict):
        return None
    turn = str(turn_user_id) if turn_user_id else None
    recorded = recorded_offer_principals(record)
    if recorded:
        if turn is None or recorded != {turn}:
            return "recorded_principal_mismatch"
        return None
    if turn is not None and _declares_non_read_effect(record):
        return "anonymous_write_offer_signed_in_turn"
    return None


def offer_principal_mismatch(record: Any, turn_user_id: Optional[Any]) -> bool:
    """True when the turn may not act on the offer (see ``principal_drop_reason``)."""
    return principal_drop_reason(record, turn_user_id) is not None


def drop_offer_on_principal_mismatch(
    record: Optional[Dict[str, Any]],
    *,
    session_id: str,
    user_id: Optional[str],
) -> bool:
    """The pop-seam check. False when the offer may be acted on (the caller
    proceeds unchanged). True when it is dropped: logged, and the caller acts
    on nothing from the offer, calls no handler of its kind, renders nothing,
    and routes the turn normally."""
    if not record:
        return False
    reason = principal_drop_reason(record, user_id)
    if reason is None:
        return False
    payload = record.get("pending_action") or {}
    logger.warning(
        "pending_offer_dropped_principal_mismatch",
        reason=reason,
        offer_user=sorted(recorded_offer_principals(record)),
        turn_user=str(user_id) if user_id else None,
        kind=payload.get("kind") if isinstance(payload, dict) else None,
        workflow_type=record.get("workflow_type"),
        session_id=session_id,
    )
    return True
