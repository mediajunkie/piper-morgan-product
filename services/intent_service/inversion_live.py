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
- **THREE NAMING SURFACES, one flag** (#1667, Lead decision 2026-08-20 —
  env var name KEPT, semantics widened). A token in the flag set may name:
  a **flip group** (``read_status`` / ``read_referent`` / ``read_synthesis``
  — declared on the rail entry, ``WorkflowEntry.flip_group``; this is how a
  WAVE flips), an **individual operation** (``show_standup`` — a surgical
  one-op flip that needs no group), or an **ACTION_REGISTRY category**
  (``QUERY`` — flip-1's original unit, still valid wherever it exists).
  Matching is case-insensitive and the three vocabularies are disjoint in
  practice (categories are single uppercase words, operations and groups are
  snake_case; an operation named e.g. ``query`` would be the collision to
  watch, and none exists). Why the widening: registry categories addressed
  **23 of 93** rail READ operations — 70 had no category at all, so the
  wave-1 scope was not expressible in the flag that was supposed to express
  it. The flip unit now lives where the operation's identity lives.
  ⚠️ An operation with NO group is not thereby safe: if it carries a
  registry category, naming that CATEGORY still sweeps it in. ``--audit``
  states this per-op rather than implying "ungrouped ⇒ unreachable".
- **The rail does what it always did** — a dispatchable decision becomes an
  ``Intent`` that flows into the SAME #1124 action-dispatch rail the
  classifier feeds (``if intent.action in get_action_workflows()``). No new
  dispatch site (the #1124 ratchet is untouched); the router only chooses
  the key. Dispatch requires ALL of:
    1. the decision outcome is ``operation`` (REFUSED / error / NONE /
       CLARIFY all fall through to legacy, logged);
    2. the operation is NAMED LIVE by one of the three surfaces above — its
       own name (or its canonical alias), its rail entry's ``flip_group``,
       or its ACTION_REGISTRY category (alias-resolved via the registry-
       derived grammar — the Phase-1 scorer's ``_op_category_map`` idiom).
       The matching surface is logged as ``live_match`` so telemetry says
       WHICH one held, never just that something did;
    3. ``confidence >= PIPER_INVERSION_LIVE_MIN_CONFIDENCE`` (default 0.8);
    4. the operation is a rail key (``get_action_workflows``) whose declared
       effect is ``EffectClass.READ`` — **or** which is an individually
       verified NAMED WRITE on ``FLIP_WRITE_ALLOWLIST`` (#1677, Arch ruling
       2026-08-25, PM-chosen 2026-08-28). This guard is LOAD-BEARING, not
       belt: ACTION_REGISTRY files ``create_issue`` (WRITE) and
       ``close_issue`` (DESTRUCTIVE) under QUERY, so a category flag alone
       cannot be a READ guarantee. **An UNALLOWLISTED write can never flip
       via this module regardless of configuration** — the allowlist is a
       named list of reviewed operations, deliberately NOT a relaxation of
       the class check, because the class check is what catches an operation
       that lies about its own effect. (#1667 adds a SECOND, structural
       guarantee upstream: a non-READ entry cannot be constructed with a
       ``flip_group`` unless it declares an allowlisted key —
       ``WorkflowEntry.__post_init__`` raises. Both points consult the same
       constant and move together. This condition remains the belt, and
       remains the only guard for the category and operation-name surfaces.)
       ⚠️ Consequence worth stating rather than leaving to be discovered: an
       allowlisted write is reachable by ANY of the three naming surfaces
       that name it — ``create_todo`` carries registry category EXECUTION, so
       flipping the CATEGORY token ``EXECUTION`` sweeps it in too, not only
       the operation token. The allowlist bounds WHICH writes, never WHICH
       surface.
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
- **Routing provenance for the post-turn observer** (#1668) — the consult
  publishes its own decision to a per-turn ``ContextVar``
  (:class:`LiveRouteProvenance`, read via
  :func:`consume_live_route_provenance`). The dispatch layer takes it and
  passes it EXPLICITLY to ``maybe_schedule_shadow_check``, which uses it to
  pick the observer's mode: an inversion-routed turn gets the LEGACY
  COUNTERFACTUAL (what the old chain would have done — the flip's signal),
  a legacy-routed turn gets the unchanged router shadow. Nothing downstream
  routes on this record; it is telemetry provenance only.

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
from contextvars import ContextVar
from dataclasses import dataclass
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


# ── #1668: the turn's routing PROVENANCE, published by the consult itself ────
#
# The post-turn shadow observer needs to know HOW this turn was routed so it
# can pick its mode (re-route vs legacy counterfactual). That fact is known in
# exactly one place — the consult that decided it — and re-deriving it anywhere
# else would be a guess. So the consult records its own result here and the
# dispatch layer hands the record to the observer EXPLICITLY (a kwarg on
# ``maybe_schedule_shadow_check``); the observer never reaches back for it.
#
# ContextVar (not an attribute on the service) because a turn is a Task: each
# request runs in its own asyncio Task with its own copied Context, so two
# concurrent turns cannot see each other's provenance. Within one turn,
# ``process_intent`` and ``_process_intent_internal`` are the same Task, so the
# value set by the consult is visible to the shadow call site after the await.
@dataclass(frozen=True)
class LiveRouteProvenance:
    """How ONE turn was routed, as recorded by :func:`consult_inversion_live`.

    ``routed_live`` False (or a ``None`` record) means the legacy chain
    answered the turn — armed skip, fall-through, or the consult never ran.
    """

    routed_live: bool
    operation: Optional[str] = None
    canonical: Optional[str] = None
    category: Optional[str] = None
    live_match: Optional[str] = None
    confidence: Optional[float] = None
    reason: Optional[str] = None
    snapshot_present: bool = False


_LIVE_ROUTE: ContextVar[Optional[LiveRouteProvenance]] = ContextVar(
    "piper_inversion_live_route", default=None
)


def consume_live_route_provenance() -> Optional[LiveRouteProvenance]:
    """Take (and clear) this turn's routing provenance.

    One-shot by design: the record belongs to the turn that produced it, so a
    reader who takes it leaves nothing behind for the next turn to misread.
    ``consult_inversion_live`` also clears on entry, so a turn that never
    reaches a decision cannot inherit a stale record either.
    """
    record = _LIVE_ROUTE.get()
    if record is not None:
        _LIVE_ROUTE.set(None)
    return record


def live_categories() -> frozenset[str]:
    """The flip set — comma-separated names, case-insensitive, normalized to
    upper case.

    Each token may name a **flip group** (``read_status``), an **individual
    operation** (``show_standup``), or an **ACTION_REGISTRY category**
    (``QUERY``) — see the module docstring's three-surface note (#1667). The
    env var name and this function's name are KEPT from flip-1 (the semantics
    widened, not the switch), so every existing deploy string keeps working
    byte-for-byte.

    DEFAULT-EMPTY: unset/empty means the flip is fully off and the consult
    does zero work. Read at call time (the shadow-flag idiom)."""
    raw = os.environ.get(LIVE_CATEGORIES_ENV, "")
    return frozenset(t.strip().upper() for t in raw.split(",") if t.strip())


def resolve_live_match(
    *,
    operation: Optional[str],
    canonical: Optional[str],
    flip_group: Optional[str],
    category: Optional[str],
    cats: frozenset[str],
) -> Optional[str]:
    """Which naming surface (if any) puts this operation in the live set.

    Returns ``"operation"`` / ``"group"`` / ``"category"`` / ``None``.

    The order is REPORTING precedence, not policy: any single match makes the
    operation live, so the checks cannot conflict — the order only decides
    which surface gets NAMED in telemetry when more than one matches, most
    specific first. (m-43: a flip that says "live" without saying by what is
    a flip nobody can revert precisely.)
    """
    for name in (operation, canonical):
        if name and name.upper() in cats:
            return "operation"
    if flip_group and flip_group.upper() in cats:
        return "group"
    if category and category.upper() in cats:
        return "category"
    return None


def _effect_guard_passes(entry: Any, op: Optional[str], canonical: Optional[str]) -> bool:
    """The dispatch-time half of the #1677 effect guard (the constructor guard
    in ``WorkflowEntry.__post_init__`` is the structural half — they consult
    the SAME ``FLIP_WRITE_ALLOWLIST`` and were changed in the same commit,
    per Arch's ruling: relaxing one and not the other leaves a gap between
    what is checked and what is enforced).

    READ passes, unchanged — flip-1's contract. A non-READ entry passes ONLY
    if BOTH hold:

    - the entry DECLARES an allowlisted ``flip_write_allowlist_key``
      (``flip_write_allowed``), i.e. someone ran Arch's three verification
      conditions on it and wrote the name down; and
    - the operation being routed on THIS turn IS that name (or resolves to it
      canonically). One entry object serves an alias family — create_todo /
      add_todo / new_todo share this object — so the declaration alone says
      "this entry was reviewed", not "this name was". The reviewed name is
      the one that flips.

    Everything the guard caught before, it still catches: ``create_issue``
    (WRITE, filed under QUERY in ACTION_REGISTRY) declares no key, so naming
    it — or its category — still cannot flip it.
    """
    from services.intent_service.workflow_dispatcher import flip_write_allowed

    if entry.effect == EffectClass.READ:
        return True
    if not flip_write_allowed(entry):
        return False
    return entry.flip_write_allowlist_key in {op, canonical}


def unrecognized_flag_tokens(cats: frozenset[str], grammar: Any) -> list[str]:
    """Flag tokens that name NOTHING — not a known group, not a rail key or
    grammar alias, not an ACTION_REGISTRY category.

    A typo'd token is otherwise perfectly silent: the wave simply doesn't
    flip, and the telemetry line looks like a normal fall-through. Computed
    only on a consult that is already logging (so the default-empty
    zero-work pin is untouched) and reported on the decision line.
    """
    from services.intent_service.action_registry import ACTION_REGISTRY
    from services.intent_service.workflow_dispatcher import (
        FLIP_GROUPS,
        get_action_workflows,
    )

    known = {g.upper() for g in FLIP_GROUPS}
    known |= {k.upper() for k in get_action_workflows()}
    aliases = getattr(grammar, "alias_to_canonical", {}) or {}
    known |= {a.upper() for a in aliases}
    known |= {c.upper() for c in aliases.values()}
    known |= {n.upper() for n in grammar.names()}
    known |= {c.upper() for (c, _a) in ACTION_REGISTRY}
    return sorted(t for t in cats if t not in known)


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
    # #1668: clear this turn's provenance slot FIRST, on every path including
    # the default-empty one. A ContextVar assignment is not "work" in the
    # pinned sense (no snapshot assembly, no grammar derivation, no LLM call,
    # no log line — the DEFAULT-EMPTY test asserts exactly those four), and
    # clearing here is what makes a stale record structurally impossible when
    # two turns share one Task (tests, scripts, batch callers).
    _LIVE_ROUTE.set(None)

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
    canonical: Optional[str] = None
    flip_group: Optional[str] = None
    live_match: Optional[str] = None
    intent_category: Optional[IntentCategory] = None

    if decision.outcome != "operation" or not op:
        reason = f"router_{decision.outcome}"  # router_none/clarify/refused/error
    else:
        from services.intent_service.workflow_dispatcher import get_action_workflows

        canonical = grammar.alias_to_canonical.get(op, op)
        category = _category_by_operation(grammar).get(op)
        # The rail entry is fetched HERE (before the threshold check, where
        # flip-1 fetched it) because the group lives on it. Reason ORDER is
        # unchanged — not-live still precedes sub_threshold, which still
        # precedes not_rail_dispatchable — so every flip-1 telemetry bucket
        # keeps its exact meaning; only the lookup moved.
        entry = get_action_workflows().get(op)
        flip_group = entry.flip_group if entry is not None else None
        live_match = resolve_live_match(
            operation=op,
            canonical=canonical,
            flip_group=flip_group,
            category=category,
            cats=cats,
        )

        if live_match is None:
            # No naming surface put this op in the live set. The shared
            # not_live_ prefix asserts exactly that and enumerates no surfaces
            # (a fourth surface leaves both names true); the suffix states the
            # one fact that differs between the buckets — whether a registry
            # category existed at all. Both buckets were renamed by #1670
            # (2026-08-21; the #1667 widening made flip-1's names describe
            # half the check). Old→new mapping note:
            # docs/internal/architecture/current/inversion-phase2-gate-2026-08-19.md.
            # The precise account is on the line itself: live_match=None
            # plus flip_group, category, and live_categories.
            reason = "not_live_categorized" if category else "not_live_uncategorized"
        elif decision.confidence is None or decision.confidence < threshold:
            reason = "sub_threshold"
        elif entry is None:
            reason = "not_rail_dispatchable"
        elif not _effect_guard_passes(entry, op, canonical):
            reason = "not_read_effect"
        elif category:
            try:
                intent_category = IntentCategory[category.upper()]
            except KeyError:
                reason = "unknown_category_enum"
        elif entry.effect != EffectClass.READ:
            # An ALLOWLISTED WRITE that carries no ACTION_REGISTRY category
            # (#1677). The QUERY fall-through below is only honest for a
            # declared-READ operation — emitting IntentCategory.QUERY for a
            # write would be a lie in the Intent itself, and the rail's
            # category routing is the fall-through target if the action
            # dispatch ever returns None. No allowlisted op is in this state
            # today (create_todo is EXECUTION in the registry); this branch
            # exists so that the day one is, it takes LEGACY rather than a
            # fabricated category.
            reason = "allowlisted_write_uncategorized"
        else:
            # Flipped by GROUP or by OPERATION NAME, with no ACTION_REGISTRY
            # category to carry (70 of 93 rail READ ops are in this state —
            # the #1667 measurement). The rail dispatches on intent.action
            # BEFORE category routing (#1124), so this value chooses no
            # handler; it is the Intent's shape-required field and the
            # fall-through target if the rail ever returns None. QUERY is the
            # honest value rather than a guess: the branch DIRECTLY ABOVE has
            # already established this operation is declared READ (#1677 put
            # that fact one branch closer — an allowlisted WRITE with no
            # registry category takes legacy there and never reaches here), and
            # QUERY is IntentCategory's read-only-retrieval member
            # ("CQRS-lite", shared_types.py). It asserts nothing about the
            # registry, which is exactly the point — there is no registry row.
            intent_category = IntentCategory.QUERY

    dispatch = reason is None
    _log_decision(
        message,
        session_id=session_id,
        user_id=user_id,
        route="inversion" if dispatch else "legacy",
        reason=reason,
        operation=op,
        canonical=canonical,
        category=category,
        # #1667: WHICH naming surface made this live (or None), and the group
        # the rail declares for it. Without these, "route=inversion" can't be
        # traced back to the flag token that caused it — and an operator
        # reverting a bad wave would be guessing which token to remove.
        flip_group=flip_group,
        live_match=live_match,
        unrecognized_flag_tokens=unrecognized_flag_tokens(cats, grammar) or None,
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

    # #1668: publish the decision as this turn's routing provenance, from the
    # consult's OWN result — the post-turn shadow observer branches on it to
    # choose re-route vs legacy-counterfactual mode. Recorded for BOTH outcomes
    # so "legacy, and here is the gate that held" is on the record too.
    _LIVE_ROUTE.set(
        LiveRouteProvenance(
            routed_live=dispatch,
            operation=op,
            canonical=canonical,
            category=category,
            live_match=live_match,
            confidence=decision.confidence,
            reason=reason,
            snapshot_present=bool(block),
        )
    )
    if not dispatch:
        return None
    if op is None or intent_category is None or decision.confidence is None:
        # Structurally unreachable: each of these Nones sets a reason above,
        # and dispatch is exactly reason-is-None. Narrowed explicitly (mypy)
        # so the impossible state falls through to legacy rather than
        # constructing a malformed Intent.
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
