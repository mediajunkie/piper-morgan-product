"""#1595 Phase 1 — the standing async shadow-check (SHADOW-ONLY observer).

Arch (decisions.log 2026-08-09 09:0x): point 3 is "the actual cure, not a
workaround" — surface 1's claims were unfalsifiable in production because the
LLM never saw the phrases it claimed. This module makes them falsifiable
CONTINUOUSLY: when ``PIPER_INVERSION_SHADOW`` is on, after a production turn
completes, a fire-and-forget task routes the same utterance through the
constrained inversion router and logs a structured comparison line
(``shadow_route_agreement`` / ``shadow_route_disagreement``). Deterministic
answers ship live; the shadow opinion is corpus telemetry; zero latency cost.

TWO MODES since #1668 (2026-08-21), branched on how the turn was ROUTED:

- **ROUTER SHADOW** (legacy-routed turn) — the original behavior above,
  unchanged byte-for-byte: run the constrained router, compare against the
  production label, log ``shadow_route_*``.
- **LEGACY COUNTERFACTUAL** (inversion-routed turn, i.e. the #1595 Phase 2.2
  live consult chose this turn's rail key) — re-running the router here would
  ask the same router the same question and score its self-agreement, which is
  not signal. Instead the observer computes what the LEGACY chain would have
  done and logs ``shadow_legacy_counterfactual_*``. During a flip wave, "what
  would the old router have done here" is precisely the comparison the wave
  needs, and disagreement is the corpus-worthy artifact.

The turn's routing provenance is PASSED IN (``live_route``, produced by
``inversion_live.consult_inversion_live`` and threaded through the dispatch
layer) — this module never re-derives how a turn was routed.

⚠️ **Cost never grows.** The counterfactual replaces the router call; it does
not join it. Its legs short-circuit exactly like the legacy chain's own do, so
it spends ONE LLM call when both deterministic legs decline and ZERO when
either claims — never more than the single router call it replaced.

Structural no-execution guarantee: this is the ONLY production module allowed
to import ``inversion_router`` (enforced by
``TestInversionShadowNoExecutionBoundary`` in
``tests/test_architecture_enforcement.py``). The scheduler returns the task
for testability, but the task's coroutine returns ``None`` and its only
side effect is a log line — there is nothing for a dispatch layer to consume.

Config (read at call time, never import time):

- ``PIPER_INVERSION_SHADOW``          — "1"/"true"/"on" enables; default OFF.
- ``PIPER_INVERSION_SHADOW_SAMPLE``   — sampling rate 0.0–1.0; default 1.0
                                        (shadow phase samples everything).
- ``PIPER_INVERSION_LOG_UTTERANCE``   — "0" logs the utterance hash only;
                                        default "1" (full utterance — shadow
                                        mode is itself operator-opt-in, and
                                        the lines are corpus material). The
                                        sha256 is always logged either way.

EffectClass: n/a — observer only; nothing dispatches, nothing is written.
"""

from __future__ import annotations

import asyncio
import hashlib
import os
import random
from typing import Any, Optional

import structlog

from services.intent_service.session_snapshot import (
    SessionSnapshot as StateSnapshot,
)
from services.intent_service.session_snapshot import serialize_for_prompt

logger = structlog.get_logger(__name__)

_TRUTHY = {"1", "true", "on", "yes"}

# Keep strong references to in-flight shadow tasks so the event loop can't
# garbage-collect a fire-and-forget task mid-run (standard asyncio idiom).
_INFLIGHT: set[asyncio.Task] = set()


def shadow_enabled() -> bool:
    return os.environ.get("PIPER_INVERSION_SHADOW", "").strip().lower() in _TRUTHY


def _sample_rate() -> float:
    raw = os.environ.get("PIPER_INVERSION_SHADOW_SAMPLE", "1.0")
    try:
        return max(0.0, min(1.0, float(raw)))
    except ValueError:
        return 1.0


def _log_full_utterance() -> bool:
    return os.environ.get("PIPER_INVERSION_LOG_UTTERANCE", "1").strip().lower() in _TRUTHY


# ── #1668 legacy-counterfactual mode: the layer statement (m-43) ─────────────
#
# The legacy chain is Stage 0 (B3 referent resolution) → multi-intent rules →
# [classifier: cache → pre-classifier → LLM]. The counterfactual runs the
# DETERMINISTIC surfaces plus, only when both decline, the classifier's LLM
# stage — and runs it UNSCOPED and UNCACHED, so a post-turn observer performs
# no owner-scoped ledger read and can never write the production classifier
# cache. Which legs actually ran is on every line (``legacy_legs_run``); which
# were deliberately skipped is too (``legacy_legs_not_run``). Naming both is
# the point: a counterfactual that says "legacy would have said X" without
# saying which legacy is a measurement of an unnamed layer.
LEGACY_LEGS_NOT_RUN = (
    "b3_referent_resolution",  # Stage 0 — needs an owner-scoped ledger read
    "classifier_cache",  # read and write share one gate; an observer must not write it
    "identity_scoped_system_prompt",  # ADR-075 D4 per-principal classification prompt
    "graph_context",  # #278 enrichment, keyed on context["user_id"]
    "preference_detection_hooks",  # #248 — a hook that can WRITE preferences
)

LEGACY_LAYER_NOTE = (
    "legacy counterfactual measured at the UNSCOPED, UNCACHED, SINGLE-INTENT "
    "layer of the legacy chain: legacy_legs_run is what executed, "
    "legacy_legs_not_run is what did not. This line does not claim to be the "
    "full production classify_multiple call (m-43)."
)


def maybe_schedule_shadow_check(
    message: str,
    production_intent: Optional[str],
    *,
    session_id: Optional[str] = None,
    user_id: Optional[str] = None,
    llm_service: Any = None,
    offer_service: Any = None,
    snapshot: Optional[StateSnapshot] = None,
    live_route: Any = None,
    classifier: Any = None,
) -> Optional[asyncio.Task]:
    """Fire-and-forget a shadow route of ``message`` after a completed turn.

    Returns the created task (for tests), or ``None`` when the flag is off,
    the turn is sampled out, the message is empty, or no event loop is
    running. NEVER blocks or fails the turn: everything after task creation
    is inside the task, and the task's coroutine cannot raise.

    ``production_intent`` is the production decision label from the turn's
    existing observability (``_resolve_turn_intent_label`` — the #1518
    ``"category:action"`` / bare-``"category"`` shape). ``offer_service`` is
    the intent service's ``WorkflowOfferService`` for the lightweight
    post-turn snapshot peek.

    ``snapshot`` (#1595 Phase 2.0) is the assembled contract
    ``session_snapshot.SessionSnapshot`` from the call site; when provided,
    its ``serialize_for_prompt`` block becomes the shadow call's session
    state and the legacy ad-hoc offer peek is skipped (the snapshot's own
    peek already covered it, with more fields). When None the pre-2.0 peek
    path runs unchanged. Shadow-only either way — the snapshot changes what
    the OBSERVER sees, never what production routing does.

    ``live_route`` (#1668) is this turn's routing provenance —
    ``inversion_live.LiveRouteProvenance``, produced by the live consult and
    handed here EXPLICITLY by the dispatch layer. When it says the turn was
    routed by the inversion, the task runs the LEGACY COUNTERFACTUAL instead
    of a router re-route (see the module docstring's two-mode note); anything
    else — ``None``, ``routed_live`` False, an object that doesn't answer —
    takes the original router-shadow path unchanged. ``classifier`` is the
    intent service's ``IntentClassifier``, used only by the counterfactual's
    LLM leg (and only when the deterministic legs decline).
    """
    if not shadow_enabled() or not message:
        return None
    if random.random() >= _sample_rate():
        return None
    if getattr(live_route, "routed_live", False):
        coro = _legacy_counterfactual_check(
            message,
            live_route,
            session_id=session_id,
            user_id=user_id,
            classifier=classifier,
            snapshot=snapshot,
        )
    else:
        coro = _shadow_check(
            message,
            production_intent,
            session_id=session_id,
            user_id=user_id,
            llm_service=llm_service,
            offer_service=offer_service,
            snapshot=snapshot,
        )
    try:
        task = asyncio.get_running_loop().create_task(coro)
    except RuntimeError:
        coro.close()  # never scheduled → close it so it can't warn as never-awaited
        # No running loop (sync caller) — shadow observation is best-effort.
        logger.debug("inversion_shadow_no_event_loop")
        return None
    _INFLIGHT.add(task)
    task.add_done_callback(_INFLIGHT.discard)
    return task


async def _shadow_check(
    message: str,
    production_intent: Optional[str],
    *,
    session_id: Optional[str],
    user_id: Optional[str],
    llm_service: Any,
    offer_service: Any,
    snapshot: Optional[StateSnapshot] = None,
) -> None:
    """The shadow route + comparison. Cannot raise; silent-ok on failure."""
    try:
        from services.intent_service.inversion_router import (
            SessionSnapshot as RouterSnapshot,
        )
        from services.intent_service.inversion_router import (
            derive_routing_grammar,
            route,
        )

        session_state: Optional[RouterSnapshot] = None
        if snapshot is not None:
            # #1595 Phase 2.0: the assembled contract snapshot, serialized
            # via the golden-pinned renderer, IS the session-state block.
            try:
                block = serialize_for_prompt(snapshot)
            except Exception as e:  # silent-ok: a serialization failure (cap breach) degrades to no-session-state for THIS shadow call, logged loudly — never fails the task
                logger.error("shadow_snapshot_serialize_failed", error=str(e))
                block = ""
            if block:
                session_state = RouterSnapshot(state_block=block)
        elif offer_service is not None and session_id:
            # Pre-2.0 fallback peek (no assembled snapshot passed).
            try:
                # #1532: owner-scoped, read-only peek — never pops the store.
                pending = offer_service.peek_pending_offer(session_id, user_id=user_id)
            except Exception:  # silent-ok: the snapshot peek is best-effort observer input — a failed peek degrades to no-session-state; the shadow task itself logs its failures
                pending = None
            if pending:
                kind = (pending.get("pending_action") or {}).get("kind")
                summary = pending.get("workflow_type", "offer")
                if kind:
                    summary = f"{summary} ({kind})"
                session_state = RouterSnapshot(pending_offer_summary=summary)

        grammar = derive_routing_grammar()
        decision = await route(
            message,
            session_state,
            llm_service=llm_service,
            grammar=grammar,
            user_id=user_id,
        )

        agreement = _compare(production_intent, decision, grammar)
        if agreement is True:
            event = "shadow_route_agreement"
        elif agreement is False:
            event = "shadow_route_disagreement"
        else:
            event = "shadow_route_incomparable"  # refused/error/no label

        fields = dict(
            utterance_sha256=hashlib.sha256(message.encode()).hexdigest(),
            production_intent=production_intent,
            shadow_route=decision.route_label,
            shadow_outcome=decision.outcome,
            shadow_operation=decision.operation,
            shadow_confidence=decision.confidence,
            shadow_rationale=decision.rationale,
            shadow_args=decision.args or None,
            shadow_llm_calls=decision.llm_calls,
            shadow_error=decision.error,
            # #1620: the RESOLVED provider+model that answered this call
            # (post-fallback), not the configured/requested one — None when
            # no call succeeded (e.g. an "error" outcome).
            shadow_served_provider=decision.served_provider,
            shadow_served_model=decision.served_model,
            agreement=agreement,
            session_id=session_id,
            user_id=user_id,
            sample_rate=_sample_rate(),
            # m-44: a snapshot whose reads failed open must be VISIBLE in the
            # corpus line, or a dead store read scores as "empty session".
            snapshot_field_errors=(
                list(snapshot.field_errors) if snapshot and snapshot.field_errors else None
            ),
        )
        if _log_full_utterance():
            fields["utterance"] = message
        logger.info(event, **fields)
    except Exception as e:  # silent-ok: shadow failure must NEVER fail or delay the turn (#1595 AC); it is error-logged with context so a dead shadow lane is visible, not silent (m-44)
        logger.error("shadow_route_check_failed", error=str(e), exc_info=True)


async def _legacy_counterfactual_check(
    message: str,
    live_route: Any,
    *,
    session_id: Optional[str],
    user_id: Optional[str],
    classifier: Any,
    snapshot: Optional[StateSnapshot] = None,
) -> None:
    """#1668 mode 2 — what the LEGACY chain would have done on a turn the
    inversion routed LIVE. Cannot raise; silent-ok on failure.

    Legs, in the legacy chain's own order, each short-circuiting exactly as the
    legacy chain short-circuits (``classifier.classify_multiple`` →
    ``classify``):

    1. ``multi_intent_rules``  — ``PreClassifier.detect_multiple_intents``:
       pure, deterministic, ZERO LLM calls.
    2. ``pre_classifier``      — ``PreClassifier.pre_classify``: same.
    3. ``llm_classifier``      — ``IntentClassifier.classify`` UNSCOPED
       (no ``user_id`` / ``session_id`` / ``context``) and UNCACHED
       (``use_cache=False``). Runs ONLY when both deterministic legs decline,
       and issues exactly ONE ``llm.complete`` call.

    Cost: 0 or 1 LLM calls, against the 1 the router re-route spent here
    before this mode existed. The router is not called on this path at all.
    """
    legs_run: list[str] = []
    leg_errors: dict[str, str] = {}
    legacy_action: Optional[str] = None
    legacy_category: Optional[str] = None
    decided_by: Optional[str] = None
    legacy_llm_calls = 0

    try:
        from services.intent_service.pre_classifier import PreClassifier

        # ── Leg 1: multi-intent rules (deterministic, free).
        legs_run.append("multi_intent_rules")
        try:
            multi = PreClassifier.detect_multiple_intents(message)
        except Exception as e:  # silent-ok: one leg of a comparison — a broken leg degrades this line to "leg errored", recorded in leg_errors and logged, and never touches routing
            leg_errors["multi_intent_rules"] = str(e)
            multi = None
        first = (getattr(multi, "intents", None) or [None])[0]
        if first is not None:
            decided_by = "multi_intent_rules"
            legacy_action = first.action
            legacy_category = getattr(first.category, "value", None)

        # ── Leg 2: the deterministic pre-classifier (free).
        if decided_by is None:
            legs_run.append("pre_classifier")
            try:
                pre = PreClassifier.pre_classify(message)
            except Exception as e:  # silent-ok: as leg 1 — comparison telemetry only, recorded and logged, never routing
                leg_errors["pre_classifier"] = str(e)
                pre = None
            if pre is not None:
                decided_by = "pre_classifier"
                legacy_action = pre.action
                legacy_category = getattr(pre.category, "value", None)

        # ── Leg 3: the classifier's LLM stage — the ONE call, and only when
        # the legacy chain itself would have reached for it.
        if decided_by is None and classifier is not None:
            legs_run.append("llm_classifier")
            try:
                # Counted BEFORE the await: a call that raises mid-flight may
                # still have been spent, and under-reporting cost is the one
                # dishonesty this line cannot afford.
                legacy_llm_calls = 1
                intent = await classifier.classify(message, use_cache=False)
                decided_by = "llm_classifier"
                legacy_action = intent.action
                legacy_category = getattr(intent.category, "value", None)
            except Exception as e:  # silent-ok: the LLM leg is comparison telemetry — a classifier failure degrades this line to incomparable, recorded in leg_errors and logged, never affecting the (already-completed) turn
                leg_errors["llm_classifier"] = str(e)

        # ── The comparison, alias-aware (exact-name comparison under-credits:
        # set_reminder IS create_reminder — the Phase-0 scoring correction).
        from services.intent_service.inversion_router import derive_routing_grammar

        canon = derive_routing_grammar().alias_to_canonical
        live_op = getattr(live_route, "canonical", None) or getattr(live_route, "operation", None)
        if not legacy_action or not live_op:
            agreement: Optional[bool] = None
        else:
            agreement = canon.get(legacy_action, legacy_action) == canon.get(live_op, live_op)

        if agreement is True:
            event = "shadow_legacy_counterfactual_agreement"
        elif agreement is False:
            event = "shadow_legacy_counterfactual_disagreement"
        else:
            event = "shadow_legacy_counterfactual_incomparable"

        fields = dict(
            mode="legacy_counterfactual",
            utterance_sha256=hashlib.sha256(message.encode()).hexdigest(),
            # What the inversion actually did (from the consult's own record).
            live_route=live_op,
            live_operation=getattr(live_route, "operation", None),
            live_category=getattr(live_route, "category", None),
            live_match=getattr(live_route, "live_match", None),
            live_confidence=getattr(live_route, "confidence", None),
            # What the legacy chain would have done, and by which leg.
            legacy_action=legacy_action,
            legacy_category=legacy_category,
            legacy_label=(f"{legacy_category}:{legacy_action}" if legacy_action else None),
            legacy_decided_by=decided_by,
            # m-43: name the layer on the line itself, not only in the doc.
            legacy_legs_run=legs_run,
            legacy_legs_not_run=list(LEGACY_LEGS_NOT_RUN),
            legacy_leg_errors=leg_errors or None,
            legacy_llm_calls=legacy_llm_calls,
            layer_note=LEGACY_LAYER_NOTE,
            agreement=agreement,
            session_id=session_id,
            user_id=user_id,
            sample_rate=_sample_rate(),
            snapshot_present=snapshot is not None,
            snapshot_field_errors=(
                list(snapshot.field_errors) if snapshot and snapshot.field_errors else None
            ),
        )
        if _log_full_utterance():
            fields["utterance"] = message
        logger.info(event, **fields)
    except Exception as e:  # silent-ok: the counterfactual observer must NEVER fail or delay the turn (#1595 AC); error-logged with context so a dead lane is visible, not silent (m-44)
        logger.error(
            "shadow_legacy_counterfactual_failed",
            error=str(e),
            legacy_legs_run=legs_run,
            exc_info=True,
        )


def _compare(production_intent: Optional[str], decision: Any, grammar: Any) -> Optional[bool]:
    """Registry-alias-aware agreement between production label and shadow route.

    Returns True/False for comparable pairs, None when no honest comparison
    exists (no production label, or the shadow outcome is refused/error).
    Aliases resolve via the grammar's registry-derived alias map — exact-name
    comparison under-credits (``set_reminder`` IS ``create_reminder``), the
    Phase-0 scoring correction.
    """
    if not production_intent:
        return None
    if decision.outcome in ("refused", "error"):
        return None
    _, _, prod_action = production_intent.partition(":")
    if decision.outcome == "operation":
        if not prod_action:
            return False  # production floored/category-routed; shadow picked an op
        canon = grammar.alias_to_canonical
        return canon.get(prod_action, prod_action) == canon.get(
            decision.operation, decision.operation
        )
    if decision.outcome == "none":
        # NONE = "no operation; floor" — agrees when production also resolved
        # no action (bare-category label).
        return not prod_action
    # CLARIFY has no production analogue in the label shape → disagreement
    # with any concrete production decision (it is the router asking).
    return False
