"""#1595 Phase 2.2 flip-1 — the LIVE inversion routing consult (per-category flag).

This module is the reviewed act the Phase-1 no-execution boundary promised:
the ONE production module besides the shadow observer allowed to consume the
constrained router (``TestInversionShadowNoExecutionBoundary`` names exactly
this file in its allowlist — a named module, never a pattern). The dispatch
layer (``services/intent/intent_service.py``) stays structurally blind to
``RoutingDecision``: it calls :func:`consult_inversion_live` and receives a
fully-formed ``Intent`` or ``None``, nothing else.

Scope (the #1663 contract addendum, Arch 2026-08-19, binding):

- **Flip-1 only** — zero-armed-state READ categories. An ARMED turn (a
  pending offer popped at the seam this turn, a bare affirmative that just
  bound to a contextual offer, or a snapshot showing a pending offer /
  active guided process / draft-in-compose) NEVER takes the inversion path:
  the consult skips BEFORE any LLM call and the legacy chain runs unchanged.
  The seam-consumption amendment (armed emissions as validated hints) builds
  with the first armed-capable flip, not here.
- **DEFAULT-EMPTY flag set** — ``PIPER_INVERSION_LIVE_CATEGORIES`` unset or
  empty ⇒ :func:`consult_inversion_live` returns ``None`` with ZERO work
  (no snapshot assembly, no grammar derivation, no LLM call, no log line):
  routing is byte-identical to the pre-flip chain. Revert = unset. Nothing
  in code names a live category.
- **The rail does what it always did** — a dispatchable decision becomes an
  ``Intent`` that flows into the SAME #1124 action-dispatch rail the
  classifier feeds (``if intent.action in get_action_workflows()``). No new
  dispatch site (the #1124 ratchet is untouched); the router only chooses
  the key. Dispatch requires ALL of:
    1. the decision outcome is ``operation`` (REFUSED / error / NONE /
       CLARIFY all fall through to legacy, logged);
    2. the operation's ACTION_REGISTRY category (alias-resolved via the
       registry-derived grammar — the Phase-1 scorer's ``_op_category_map``
       idiom) is in the live set;
    3. ``confidence >= PIPER_INVERSION_LIVE_MIN_CONFIDENCE`` (default 0.8);
    4. the operation is a rail key (``get_action_workflows``) whose declared
       effect is ``EffectClass.READ``. This guard is LOAD-BEARING, not belt:
       ACTION_REGISTRY files ``create_issue`` (WRITE) and ``close_issue``
       (DESTRUCTIVE) under QUERY, so a category flag alone cannot be a READ
       guarantee. A write can never flip via this module regardless of
       configuration.
- **Honesty + telemetry** — every consult that reaches the router logs ONE
  structured ``inversion_live_decision`` line: route chosen, reason when
  legacy, operation/category/confidence/threshold, snapshot presence and
  field errors, and the flip's disagreement telemetry — for flip-1 the
  legacy comparison is the DETERMINISTIC pre-classifier only (surface 1,
  ``PreClassifier.pre_classify`` — no second LLM call; a turn the
  pre-classifier would not have claimed compares as ``None``/incomparable,
  and the standing post-turn shadow observer remains the deep comparison).
  Armed skips log the same event with an ``armed_*`` reason and no router
  fields. A transport-level router failure (outcome ``error``) logs at
  WARNING and falls through — an inversion error must never break the turn
  (#1423 discipline; the call site in intent_service.py adds its own
  belt-catch around this whole function).

Config resolution mirrors ``inversion_shadow.shadow_enabled()``: plain env
reads at CALL time, never import time — flipping a category live or reverting
is an environment change with no restart-order sensitivity, and tests can
monkeypatch the environment directly.

EffectClass: n/a for this module itself — it dispatches nothing; it returns
an ``Intent`` whose only consumers are the existing rail + category chain,
and it structurally cannot select anything but a declared-READ rail entry.
"""

from __future__ import annotations

import hashlib
import os
from typing import Any, Dict, Optional, Tuple

import structlog

from services.domain.models import Intent
from services.shared_types import EffectClass, IntentCategory

logger = structlog.get_logger(__name__)

_TRUTHY = {"1", "true", "on", "yes"}

# Conservative default: the router's self-reported confidence must clear this
# before a live dispatch. Deliberately ABOVE the shadow lane's typical agree
# band so early flips prefer false-legacy (safe, telemetered) over
# false-dispatch. Operator-tunable per deploy via the env var below.
DEFAULT_MIN_CONFIDENCE = 0.8

LIVE_CATEGORIES_ENV = "PIPER_INVERSION_LIVE_CATEGORIES"
MIN_CONFIDENCE_ENV = "PIPER_INVERSION_LIVE_MIN_CONFIDENCE"


def live_categories() -> frozenset[str]:
    """The per-category flip set — comma-separated registry category names
    (e.g. ``"QUERY"`` or ``"QUERY,STATUS"``), case-insensitive.

    DEFAULT-EMPTY: unset/empty means the flip is fully off and the consult
    does zero work. Read at call time (the shadow-flag idiom)."""
    raw = os.environ.get(LIVE_CATEGORIES_ENV, "")
    return frozenset(t.strip().upper() for t in raw.split(",") if t.strip())


def live_min_confidence() -> float:
    """Dispatch threshold, clamped to [0, 1]; unparseable → the default."""
    raw = os.environ.get(MIN_CONFIDENCE_ENV, "")
    try:
        value = float(raw)
    except ValueError:
        return DEFAULT_MIN_CONFIDENCE
    return max(0.0, min(1.0, value))


def _log_full_utterance() -> bool:
    # The SAME operator knob the shadow observer reads
    # (PIPER_INVERSION_LOG_UTTERANCE, default on) — one privacy switch for
    # both inversion telemetry surfaces. The sha256 is always logged.
    return (
        os.environ.get("PIPER_INVERSION_LOG_UTTERANCE", "1").strip().lower() in _TRUTHY
    )


def _category_by_operation(grammar: Any) -> Dict[str, str]:
    """operation → ACTION_REGISTRY category, alias-resolved both directions —
    the Phase-1 scorer's ``_op_category_map`` idiom, derived at call time
    (never hand-written; a registry mutation changes the next derivation)."""
    from services.intent_service.action_registry import ACTION_REGISTRY

    canon = dict(grammar.alias_to_canonical)
    by_action: Dict[str, str] = {}
    for (category, action), _ in ACTION_REGISTRY.items():
        by_action.setdefault(action, category)
        c = canon.get(action)
        if c:
            by_action.setdefault(c, category)
    return by_action


def _legacy_preclassifier_comparison(
    message: str, decision: Any, grammar: Any
) -> Tuple[Optional[str], Optional[bool]]:
    """Flip-1's cheap legacy counterfactual: what the DETERMINISTIC
    pre-classifier (surface 1) would have claimed. Returns
    ``(legacy_label, divergence)``:

    - label ``"category:action"`` when the pre-classifier claims the turn,
      else ``None`` (legacy would have consulted the LLM classifier — no
      deterministic counterfactual exists; the shadow observer covers it);
    - divergence True/False alias-aware against the router's operation;
      ``True`` when the pre-classifier claimed but the router chose a
      non-operation outcome; ``None`` when incomparable.
    """
    try:
        from services.intent_service.pre_classifier import PreClassifier

        pre = PreClassifier.pre_classify(message)
    except Exception as e:  # silent-ok: comparison telemetry only — a broken comparator degrades to "incomparable", logged, and never touches routing
        logger.warning("inversion_live_preclassifier_compare_failed", error=str(e))
        return None, None
    if pre is None:
        return None, None
    label = f"{pre.category.value}:{pre.action}"
    if decision.outcome == "operation" and decision.operation:
        canon = grammar.alias_to_canonical
        diverged = canon.get(pre.action, pre.action) != canon.get(
            decision.operation, decision.operation
        )
        return label, diverged
    # Pre-classifier had a concrete claim; the router chose none/clarify/
    # refused/error — a real disagreement with the deterministic legacy chain.
    return label, True


async def consult_inversion_live(
    message: str,
    *,
    session_id: Optional[str],
    user_id: Optional[str],
    intent_service: Any,
    turn_had_pending_offer: bool = False,
    turn_bound_contextual_offer: bool = False,
) -> Optional[Intent]:
    """One live routing consult. Returns a dispatch-ready ``Intent`` when the
    flip applies, else ``None`` (⇒ the legacy chain runs UNCHANGED).

    ``turn_had_pending_offer`` — the #846 pop seam found (and popped) an
    offer this turn; even when the kind-specific handlers fell through
    (off-intent abandon), the turn was ARMED and is out of flip-1 scope.
    ``turn_bound_contextual_offer`` — the #1529/#852 soft-offer binding
    claimed this turn's affirmative; the continuation hint belongs to the
    classifier path.
    """
    cats = live_categories()
    if not cats or not message:
        # DEFAULT-EMPTY pin: zero work, zero logs — byte-identical routing.
        return None

    # ── Armed guard, part 1: what the seams already told us (no LLM spent).
    if turn_had_pending_offer or turn_bound_contextual_offer:
        _log_decision(
            message,
            session_id=session_id,
            user_id=user_id,
            route="legacy",
            reason=(
                "armed_pending_offer_popped"
                if turn_had_pending_offer
                else "armed_contextual_offer_bound"
            ),
        )
        return None

    # ── Armed guard, part 2: the Phase-2.0 snapshot, assembled PRE-classification
    # (never raises, read-only by contract — peek, not pop).
    from services.intent_service.snapshot_assembly import assemble_session_snapshot

    snapshot = await assemble_session_snapshot(session_id, user_id, intent_service)
    if (
        snapshot.pending_offer_kind
        or snapshot.active_process_type
        or snapshot.draft_in_compose
    ):
        _log_decision(
            message,
            session_id=session_id,
            user_id=user_id,
            route="legacy",
            reason="armed_snapshot",
            snapshot_field_errors=list(snapshot.field_errors) or None,
        )
        return None

    from services.intent_service.inversion_router import (
        SessionSnapshot as RouterSnapshot,
    )
    from services.intent_service.inversion_router import (
        derive_routing_grammar,
        route,
    )
    from services.intent_service.session_snapshot import serialize_for_prompt

    try:
        block = serialize_for_prompt(snapshot)
    except Exception as e:  # silent-ok: a cap breach degrades THIS consult to no-session-state, error-logged — never fails the turn
        logger.error("inversion_live_snapshot_serialize_failed", error=str(e))
        block = ""

    grammar = derive_routing_grammar()
    decision = await route(
        message,
        RouterSnapshot(state_block=block) if block else None,
        llm_service=getattr(
            getattr(intent_service, "intent_classifier", None), "_llm", None
        ),
        grammar=grammar,
        user_id=user_id,
    )

    legacy_label, divergence = _legacy_preclassifier_comparison(
        message, decision, grammar
    )

    # ── The dispatch decision, one condition at a time (each reason is a
    # distinct telemetry bucket — the corpus needs to see WHICH gate held).
    threshold = live_min_confidence()
    op = decision.operation
    reason: Optional[str] = None
    category: Optional[str] = None
    intent_category: Optional[IntentCategory] = None

    if decision.outcome != "operation" or not op:
        reason = f"router_{decision.outcome}"  # router_none/clarify/refused/error
    else:
        category = _category_by_operation(grammar).get(op)
        if category is None:
            reason = "no_registry_category"
        elif category.upper() not in cats:
            reason = "category_not_live"
        elif decision.confidence is None or decision.confidence < threshold:
            reason = "sub_threshold"
        else:
            from services.intent_service.workflow_dispatcher import (
                get_action_workflows,
            )

            entry = get_action_workflows().get(op)
            if entry is None:
                reason = "not_rail_dispatchable"
            elif entry.effect != EffectClass.READ:
                reason = "not_read_effect"
            else:
                try:
                    intent_category = IntentCategory[category.upper()]
                except KeyError:
                    reason = "unknown_category_enum"

    dispatch = reason is None
    _log_decision(
        message,
        session_id=session_id,
        user_id=user_id,
        route="inversion" if dispatch else "legacy",
        reason=reason,
        operation=op,
        canonical=grammar.alias_to_canonical.get(op, op) if op else None,
        category=category,
        confidence=decision.confidence,
        threshold=threshold,
        outcome=decision.outcome,
        llm_calls=decision.llm_calls,
        error=decision.error,
        snapshot_present=bool(block),
        snapshot_field_errors=list(snapshot.field_errors) or None,
        legacy_preclassifier=legacy_label,
        legacy_divergence=divergence,
        loud=(decision.outcome == "error"),
    )
    if not dispatch:
        return None

    return Intent(
        category=intent_category,
        action=op,
        original_message=message,
        confidence=float(decision.confidence),
        context={
            # Transcript/telemetry marker — downstream code may LOG on this
            # but must never branch on it (the rail's behavior is identical
            # for classifier-chosen and router-chosen intents, by design).
            "inversion_live": True,
            # Router-extracted args, deliberately NAMESPACED: no handler
            # reads classifier slots from here in flip-1, so an LLM-guessed
            # arg cannot change handler behavior vs the legacy path. A later
            # flip that consumes them is its own reviewed change.
            "inversion_args": dict(decision.args or {}),
        },
    )


def _log_decision(
    message: str,
    *,
    session_id: Optional[str],
    user_id: Optional[str],
    route: str,
    reason: Optional[str],
    loud: bool = False,
    **fields: Any,
) -> None:
    """One structured ``inversion_live_decision`` line per consult decision."""
    payload = dict(
        route=route,
        reason=reason,
        utterance_sha256=hashlib.sha256(message.encode()).hexdigest(),
        session_id=session_id,
        user_id=user_id,
        live_categories=sorted(live_categories()),
        **fields,
    )
    if _log_full_utterance():
        payload["utterance"] = message
    if loud:
        logger.warning("inversion_live_decision", **payload)
    else:
        logger.info("inversion_live_decision", **payload)
