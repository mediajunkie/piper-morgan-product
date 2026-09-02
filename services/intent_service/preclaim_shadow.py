"""The PRE-CLAIM SHADOW PROBE — measurement backbone for the pre-classifier
narrowing schedule (PM-ratified 2026-08-29, decisions.log same date: a
surface-1 pattern claim must meet ~100% precision measured by shadow
divergence; patterns below the bar get deleted ON EVIDENCE).

This is the MIRROR of #1668. The #1668 legacy counterfactual answers "on a
turn the INVERSION routed, what would the LEGACY chain have done?"; this
module answers the inverse: **on a turn the PRE-CLASSIFIER claimed (surface
1), what would the INVERSION ROUTER have said?** Surface-1 claims are
exactly the turns the LLM never sees — the reason "the LLM classified X
wrong" is unobservable in production (intent-routing-stack.md, surface-1
cell) and the reason every fix has been a regex. When
``PIPER_PRECLAIM_SHADOW`` is on, a sampled pre-claimed turn fires ONE
fire-and-forget constrained routing call after the claim (the same
registry-derived grammar call the #1595 shadow uses) and logs a structured
comparison line carrying the CLAIMING PATTERN-LIST NAME — the unit the
narrowing schedule deletes at.

Scheduling sits at the two claim sites in ``classifier.py`` (the only
places surface 1 claims live turns): ``classify``'s ``pre_classify`` branch
and ``classify_multiple``'s ``detect_multiple_intents`` branch. A cached
repeat of a pre-claimed message returns from the intent cache without
re-claiming and is deliberately NOT re-sampled — precision is a property of
the pattern, not of traffic volume, and the first (fresh) claim already
sampled the utterance.

MEASUREMENT ONLY: nothing here changes what the pre-classifier claims, and
nothing dispatches from the router's opinion (``RoutingDecision`` is logged
and dropped — this module is on the ``TestInversionShadowNoExecutionBoundary``
allowlist as an OBSERVER, like ``inversion_shadow.py``). Narrowing happens
later, in reviewed commits, each citing this probe's rows (the 08-09
condition: "a narrowing without its probe row is not narrowing, it is
guessing").

Layer statement (m-43): the router is consulted STATELESS — no session
snapshot — matching the layer at which surface-1 patterns claim (regex over
the bare utterance, no state). A disagreement therefore means "given exactly
what the pattern saw, the constrained router reads the utterance
differently"; it does not claim to reproduce the stateful Phase-2.2 live
consult. The note rides every line.

Config (read at call time, never import time — the shadow-flag idiom):

- ``PIPER_PRECLAIM_SHADOW``          — "1"/"true"/"on" enables; default OFF
                                       (default-off is byte-identical, pinned).
- ``PIPER_PRECLAIM_SHADOW_SAMPLE``   — sampling rate 0.0–1.0; default 1.0.
- ``PIPER_INVERSION_LOG_UTTERANCE``  — the SAME privacy knob the other two
                                       inversion telemetry surfaces read:
                                       "0" logs the sha256 only; default "1".

Cost: one Haiku-class LLM call per SAMPLED pre-claimed turn, bounded by the
sample rate; zero latency cost (fire-and-forget, never awaited by the turn).

FAIL-OPEN everywhere (mirrors inversion_shadow's guarantees): scheduling
failures are swallowed at the call site; the task's coroutine cannot raise;
a shadow failure is error-logged (``preclaim_shadow_check_failed``) so a
dead probe lane is visible, never silent (m-44).

EffectClass: n/a — observer only; nothing dispatches, nothing is written.
"""

from __future__ import annotations

import asyncio
import hashlib
import os
import random
from typing import Any, Dict, Iterable, List, Optional, Tuple

import structlog

logger = structlog.get_logger(__name__)

_TRUTHY = {"1", "true", "on", "yes"}

PRECLAIM_SHADOW_ENV = "PIPER_PRECLAIM_SHADOW"
PRECLAIM_SAMPLE_ENV = "PIPER_PRECLAIM_SHADOW_SAMPLE"

AGREEMENT_EVENT = "preclaim_shadow_agreement"
DISAGREEMENT_EVENT = "preclaim_shadow_disagreement"
INCOMPARABLE_EVENT = "preclaim_shadow_incomparable"
FAILURE_EVENT = "preclaim_shadow_check_failed"

LAYER_NOTE = (
    "pre-claim shadow measured STATELESS: router consulted with no session "
    "snapshot, matching the layer at which surface-1 patterns claim (regex "
    "over the bare utterance). Not the stateful Phase-2.2 consult (m-43)."
)

# Keep strong references to in-flight tasks so the event loop can't
# garbage-collect a fire-and-forget task mid-run (standard asyncio idiom,
# same as inversion_shadow._INFLIGHT).
_INFLIGHT: set[asyncio.Task] = set()


def preclaim_shadow_enabled() -> bool:
    return os.environ.get(PRECLAIM_SHADOW_ENV, "").strip().lower() in _TRUTHY


def _sample_rate() -> float:
    raw = os.environ.get(PRECLAIM_SAMPLE_ENV, "1.0")
    try:
        return max(0.0, min(1.0, float(raw)))
    except ValueError:
        return 1.0


def _log_full_utterance() -> bool:
    return os.environ.get("PIPER_INVERSION_LOG_UTTERANCE", "1").strip().lower() in _TRUTHY


def maybe_schedule_preclaim_shadow(
    message: str,
    *,
    claimed_category: Optional[str],
    claimed_action: Optional[str],
    pattern_list: Optional[str],
    entry_surface: str,
    all_pattern_lists: Optional[List[str]] = None,
    session_id: Optional[str] = None,
    user_id: Optional[str] = None,
    llm_service: Any = None,
) -> Optional[asyncio.Task]:
    """Fire-and-forget the pre-claim probe for ONE surface-1 claim.

    Returns the created task (for tests), or ``None`` when the flag is off,
    the turn is sampled out, the message is empty, or no event loop is
    running. NEVER blocks or fails the turn: everything after task creation
    is inside the task, and the task's coroutine cannot raise.

    ``claimed_category``/``claimed_action`` are the claim as surface 1 made
    it; ``pattern_list`` is the claiming ``*PATTERNS`` list's name (threaded
    out of ``pre_classify_with_pattern_list`` / ``MultiIntentResult.
    pattern_lists``); ``entry_surface`` names which of the two surface-1
    entry points claimed (``"pre_classify"`` / ``"detect_multiple_intents"``);
    ``all_pattern_lists`` (multi-intent path only) lists EVERY claiming list
    on the turn — the probe's comparison runs against the primary claim, but
    each co-claiming list is on the line for the aggregate's claim counts.
    """
    if not preclaim_shadow_enabled() or not message:
        return None
    if random.random() >= _sample_rate():
        return None
    coro = _preclaim_check(
        message,
        claimed_category=claimed_category,
        claimed_action=claimed_action,
        pattern_list=pattern_list,
        entry_surface=entry_surface,
        all_pattern_lists=all_pattern_lists,
        session_id=session_id,
        user_id=user_id,
        llm_service=llm_service,
    )
    try:
        task = asyncio.get_running_loop().create_task(coro)
    except RuntimeError:
        coro.close()  # never scheduled → close it so it can't warn as never-awaited
        logger.debug("preclaim_shadow_no_event_loop")
        return None
    _INFLIGHT.add(task)
    task.add_done_callback(_INFLIGHT.discard)
    return task


async def _preclaim_check(
    message: str,
    *,
    claimed_category: Optional[str],
    claimed_action: Optional[str],
    pattern_list: Optional[str],
    entry_surface: str,
    all_pattern_lists: Optional[List[str]],
    session_id: Optional[str],
    user_id: Optional[str],
    llm_service: Any,
) -> None:
    """The router consult + comparison. Cannot raise; silent-ok on failure."""
    try:
        from services.intent_service.inversion_router import (
            derive_routing_grammar,
            route,
        )

        grammar = derive_routing_grammar()
        # STATELESS by design — see the module docstring's layer statement.
        decision = await route(
            message,
            None,
            llm_service=llm_service,
            grammar=grammar,
            user_id=user_id,
        )

        agreement, incomparable_reason = compare_claim(claimed_action, decision, grammar)
        if agreement is True:
            event = AGREEMENT_EVENT
        elif agreement is False:
            event = DISAGREEMENT_EVENT
        else:
            event = INCOMPARABLE_EVENT

        canon = grammar.alias_to_canonical
        fields = dict(
            utterance_sha256=hashlib.sha256(message.encode()).hexdigest(),
            # The claim, as surface 1 made it — and the unit the narrowing
            # schedule deletes at: the claiming pattern-list's NAME.
            pattern_list=pattern_list,
            entry_surface=entry_surface,
            all_pattern_lists=all_pattern_lists,
            pre_category=claimed_category,
            pre_action=claimed_action,
            pre_label=(
                f"{claimed_category}:{claimed_action}" if claimed_action else claimed_category
            ),
            # The router's opinion (logged and dropped — never dispatched).
            shadow_route=decision.route_label,
            shadow_outcome=decision.outcome,
            shadow_operation=decision.operation,
            shadow_canonical=(
                canon.get(decision.operation, decision.operation) if decision.operation else None
            ),
            shadow_confidence=decision.confidence,
            shadow_rationale=decision.rationale,
            shadow_llm_calls=decision.llm_calls,
            shadow_error=decision.error,
            agreement=agreement,
            incomparable_reason=incomparable_reason,
            layer_note=LAYER_NOTE,
            session_id=session_id,
            user_id=user_id,
            sample_rate=_sample_rate(),
        )
        if _log_full_utterance():
            fields["utterance"] = message
        logger.info(event, **fields)
    except Exception as e:  # silent-ok: the probe must NEVER fail or delay the turn (mirror of the #1595 shadow AC); error-logged with context so a dead probe lane is visible, not silent (m-44)
        logger.error(
            FAILURE_EVENT,
            error=str(e),
            pattern_list=pattern_list,
            entry_surface=entry_surface,
            exc_info=True,
        )


def compare_claim(
    claimed_action: Optional[str], decision: Any, grammar: Any
) -> Tuple[Optional[bool], Optional[str]]:
    """Alias-aware agreement between a surface-1 claim and the router.

    Returns ``(agreement, incomparable_reason)``:

    - ``(True, None)`` / ``(False, None)`` for comparable pairs, aliases
      resolved via the grammar's registry-derived map (exact-name comparison
      under-credits — ``set_reminder`` IS ``create_reminder``, the Phase-0
      scoring correction).
    - ``(None, reason)`` when no honest comparison exists. Three reasons:
      ``no_claimed_action`` (nothing to compare), ``router_refused`` /
      ``router_error`` (the router gave no opinion — never scored as
      disagreement, m-44), and ``claimed_action_outside_grammar`` (the claim's
      action canonicalizes to nothing the grammar can express, so agreement
      is impossible BY CONSTRUCTION — counting it against the pattern would
      manufacture false imprecision, and counting it FOR the pattern would
      manufacture false precision; it is its own bucket).

    ``NONE`` (router says floor) and ``CLARIFY`` (router asks) against a
    concrete in-grammar claim are DISAGREEMENTS: the router had the claimed
    operation available and chose not to pick it.
    """
    if not claimed_action:
        return None, "no_claimed_action"
    if decision.outcome in ("refused", "error"):
        return None, f"router_{decision.outcome}"
    canon = grammar.alias_to_canonical
    claimed_canon = canon.get(claimed_action, claimed_action)
    if claimed_canon not in grammar.names():
        return None, "claimed_action_outside_grammar"
    if decision.outcome == "operation" and decision.operation:
        return claimed_canon == canon.get(decision.operation, decision.operation), None
    # none / clarify against an expressible concrete claim.
    return False, None


# ── Aggregation for the narrowing schedule's readout ─────────────────────────
#
# These are the report helper's brain, importable (and pinned) without the
# CLI. scripts/preclaim_shadow_report.py is the thin log-parsing wrapper.


def aggregate_preclaim_events(events: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    """Per-pattern-list claim counts + agreement rates from probe events.

    ``events`` are dicts with at least ``event`` and ``pattern_list`` keys
    (the structured log lines this module emits). Precision is
    ``agree / (agree + disagree)`` — incomparable rows are EXCLUDED from the
    denominator and reported beside it (m-44: state the denominator, never
    fold "couldn't compare" into either side).
    """
    per: Dict[str, Dict[str, Any]] = {}
    scored = {
        AGREEMENT_EVENT: "agree",
        DISAGREEMENT_EVENT: "disagree",
        INCOMPARABLE_EVENT: "incomparable",
    }
    for ev in events:
        bucket = scored.get(ev.get("event", ""))
        if bucket is None:
            continue
        name = ev.get("pattern_list") or "UNKNOWN"
        row = per.setdefault(name, {"claims": 0, "agree": 0, "disagree": 0, "incomparable": 0})
        row["claims"] += 1
        row[bucket] += 1
    totals = {"claims": 0, "agree": 0, "disagree": 0, "incomparable": 0}
    for row in per.values():
        comparable = row["agree"] + row["disagree"]
        row["comparable"] = comparable
        row["precision"] = (row["agree"] / comparable) if comparable else None
        for k in totals:
            totals[k] += row[k]
    comparable = totals["agree"] + totals["disagree"]
    totals["comparable"] = comparable
    totals["precision"] = (totals["agree"] / comparable) if comparable else None
    return {"per_pattern_list": per, "totals": totals}


def render_preclaim_report(aggregate: Dict[str, Any], *, bar: float = 1.0) -> str:
    """The precision-vs-bar readout the narrowing schedule reads.

    ``bar`` defaults to 1.0 — the PM-ratified ~100% precision bar
    (decisions.log 2026-08-29). Verdicts: ``MEETS BAR`` / ``BELOW BAR`` /
    ``NO COMPARABLE DATA`` (a list with only incomparable rows has been
    measured at nothing — never printed as clean, m-44). The denominator is
    on every row.
    """
    per = aggregate["per_pattern_list"]
    totals = aggregate["totals"]
    lines = [
        "PRE-CLAIM SHADOW PROBE — per-pattern-list precision vs the narrowing bar",
        f"bar = {bar:.2f}  ·  precision = agree/(agree+disagree); "
        "incomparable rows excluded from the denominator and shown beside it",
        "",
        f"{'pattern list':<36} {'claims':>6} {'agree':>6} {'disagr':>6} "
        f"{'incomp':>6} {'precision':>10}  verdict",
        "-" * 92,
    ]

    def _verdict(row: Dict[str, Any]) -> str:
        if row["precision"] is None:
            return "NO COMPARABLE DATA"
        return "MEETS BAR" if row["precision"] >= bar else "BELOW BAR"

    def _sort_key(item: Tuple[str, Dict[str, Any]]) -> Tuple[int, int, str]:
        _, row = item
        return (-row["disagree"], -row["claims"], item[0])

    for name, row in sorted(per.items(), key=_sort_key):
        precision = f"{row['precision']:.3f}" if row["precision"] is not None else "—"
        lines.append(
            f"{name:<36} {row['claims']:>6} {row['agree']:>6} {row['disagree']:>6} "
            f"{row['incomparable']:>6} {precision:>10}  {_verdict(row)}"
        )
    lines.append("-" * 92)
    precision = f"{totals['precision']:.3f}" if totals["precision"] is not None else "—"
    lines.append(
        f"{'TOTAL (' + str(len(per)) + ' lists)':<36} {totals['claims']:>6} "
        f"{totals['agree']:>6} {totals['disagree']:>6} {totals['incomparable']:>6} "
        f"{precision:>10}"
    )
    lines.append("")
    lines.append(
        "Reading the verdicts: BELOW BAR = narrowing candidate — each deletion "
        "cites its rows here (decisions.log 2026-08-09: a narrowing without its "
        "probe row is guessing). MEETS BAR at small n is weak evidence; the "
        "claim counts ARE the denominator, read them."
    )
    return "\n".join(lines)
