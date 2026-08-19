"""#1595 Phase 1 — the standing async shadow-check (SHADOW-ONLY observer).

Arch (decisions.log 2026-08-09 09:0x): point 3 is "the actual cure, not a
workaround" — surface 1's claims were unfalsifiable in production because the
LLM never saw the phrases it claimed. This module makes them falsifiable
CONTINUOUSLY: when ``PIPER_INVERSION_SHADOW`` is on, after a production turn
completes, a fire-and-forget task routes the same utterance through the
constrained inversion router and logs a structured comparison line
(``shadow_route_agreement`` / ``shadow_route_disagreement``). Deterministic
answers ship live; the shadow opinion is corpus telemetry; zero latency cost.

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


def maybe_schedule_shadow_check(
    message: str,
    production_intent: Optional[str],
    *,
    session_id: Optional[str] = None,
    user_id: Optional[str] = None,
    llm_service: Any = None,
    offer_service: Any = None,
    snapshot: Optional[StateSnapshot] = None,
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
    """
    if not shadow_enabled() or not message:
        return None
    if random.random() >= _sample_rate():
        return None
    try:
        task = asyncio.get_running_loop().create_task(
            _shadow_check(
                message,
                production_intent,
                session_id=session_id,
                user_id=user_id,
                llm_service=llm_service,
                offer_service=offer_service,
                snapshot=snapshot,
            )
        )
    except RuntimeError:
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


def _compare(
    production_intent: Optional[str], decision: Any, grammar: Any
) -> Optional[bool]:
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
