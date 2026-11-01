"""Understanding-Layer Inversion Phase 1 (#1595) — the constrained routing call.

SHADOW-ONLY in this phase. The router's decision is NEVER executed: no
production dispatch path consumes a ``RoutingDecision``. The only production
consumer is the async shadow observer (``inversion_shadow.py``), which logs
the decision next to the production one and discards it. The import boundary
is enforced structurally by
``tests/test_architecture_enforcement.py::TestInversionShadowNoExecutionBoundary``
— only ``inversion_shadow.py`` (and tests/scripts) may import this module.

What this module implements (proposal
``understanding-layer-inversion-proposal-2026-08-08.md`` §inversion points 1–2,
as ratified WITH corrections in decisions.log 2026-08-09 07:1x/08:3x/09:0x):

1. **Tool-selection routing** — ONE Haiku-class LLM call per utterance whose
   output is CONSTRAINED to the registry-derived grammar of CANONICAL
   operations. 🔴 Per Arch's material correction: the grammar is canonical
   actions, NOT the ~110 alias rail keys — "the property that makes the alias
   set good input makes it bad catalog." Aliases stay input-side; the rail
   resolves them AFTER selection. 🔴 The grammar/schema is DERIVED FROM THE
   REGISTRY AT CALL TIME (PDR-006 condition 2) — a hand-written operation list
   is the drift problem relocated (+4 rail keys in 5 days proved it
   empirically).

2. **Context-carrying** — ``route()`` accepts an optional ``SessionSnapshot``
   (pending-offer summary, active flow, the user's own entity names). In
   shadow mode the caller populates it from a lightweight post-turn peek; see
   ``SessionSnapshot`` for what Phase 2 must thread instead.

Structured-output enforcement: the codebase's ``LLMClient.complete`` is a
text-completion surface with JSON mode (``response_format={"type":
"json_object"}``) and no tool-use mechanism, so enforcement here is: strict
JSON contract in the prompt → parse → validate the operation against the
live grammar → ONE repair retry carrying the validation error → a decision of
``refused`` recorded honestly when the model still can't comply. A REFUSED
parse is never turned into a guessed route; an LLM transport failure is
recorded as ``error``, never faked (the Phase-0 scorer discipline).

Model selection rides the app's standard config path: task type
``inversion_routing`` (services/llm/config.py) resolves to the "light" tier —
``claude-haiku-4-5`` on Anthropic, the cheapest current model. Changing the
router's model is a config.py change, not a code change.

EffectClass: n/a — nothing here dispatches; the router performs no reads or
writes on behalf of the user (grammar derivation reads process-local
registries only).

3. **The ``plan`` outcome (#1595 unit 4b, 2026-09-27, grammar shape ruled by
   Arch — #1897/#1606)** — ADDITIVE to points 1–2 above, never replacing
   them. A message that genuinely asks for 2+ DISTINCT operations may be
   answered as ``{"outcome": "plan", "operations": [<op>, <op>, ...]}``
   instead of a single ``{"operation": ...}`` object; every element is
   validated against the identical grammar a single object is. The
   single-op shape stays the DEFAULT at every layer (prompt, schema, parser)
   — the plan shape is the exception clause, both in the prompt's own
   wording and in ``_parse_and_validate``'s control flow. Consumption (what
   iterates a plan's operations and dispatches them) is NOT this module's
   concern — see ``services/intent_service/inversion_live.py`` and
   ``docs/internal/architecture/current/intent-routing-stack.md``'s unit-4b
   subsection for the rail-loop side.
"""

from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Mapping, Optional, Tuple

import structlog

from services.shared_types import ROUTE_GROUP_LINES, RouteGroup

logger = structlog.get_logger(__name__)

# Sentinel routes (part of the grammar alongside the canonical operations).
NONE_ROUTE = "NONE"  # no operation applies → conversational floor
CLARIFY_ROUTE = "CLARIFY"  # the utterance is genuinely ambiguous → ask

# #2149 build step 2: stage 2 of the two-stage router offers this instead of an op when the
# stage-1 group was wrong. It renders as a clarify decision; code never re-routes it.
OTHER_GROUP_ROUTE = "OTHER_GROUP"

TASK_TYPE = "inversion_routing"

#: #2149 step 2: the most groups a stage-1 plan may name.
MAX_PLAN_GROUPS = 3

_TWO_STAGE_TRUTHY = {"1", "true", "on", "yes"}  # same set as inversion_shadow._TRUTHY


def two_stage_enabled() -> bool:
    """The #2149 two-stage router flag, read at call time. Default OFF: with it off,
    ``route()`` runs the flat one-call path exactly as before."""
    return os.environ.get("PIPER_INVERSION_TWO_STAGE", "").strip().lower() in _TWO_STAGE_TRUTHY


# Registry descriptions carry internal migration markers ("via action
# dispatch (#1124)") that are prompt noise for the router; strip them
# mechanically — the derivation stays registry-only, no hand-written text.
_DESC_NOISE_RE = re.compile(r"\s*(?:via action dispatch)?\s*\(#\d+[^)]*\)\s*$")


@dataclass(frozen=True)
class RoutingOperation:
    """One canonical operation the router may select."""

    name: str  # canonical name (first-registered rail key / registry action)
    description: str
    example: Optional[str]  # from ACTION_EXAMPLES where present
    aliases: Tuple[str, ...]  # input-side only; never shown to the model
    source: str  # "rail" | "action_registry"
    # #2149 build step 1: the op's declared RouteGroup (entry metadata for rail ops,
    # ROUTE_GROUPS for registry ops). NOT read by build_routing_prompt: the flat catalog
    # renders byte-identically with or without it.
    route_group: Optional[RouteGroup] = None


@dataclass(frozen=True)
class RoutingGrammar:
    """The registry-derived grammar: canonical operations + NONE + CLARIFY."""

    operations: Tuple[RoutingOperation, ...]
    alias_to_canonical: Mapping[str, str]

    def names(self) -> Tuple[str, ...]:
        return tuple(op.name for op in self.operations)

    def is_valid_route(self, name: str) -> bool:
        return name in (NONE_ROUTE, CLARIFY_ROUTE) or name in self.names()


@dataclass(frozen=True)
class SessionSnapshot:
    """Lightweight session state for the routing call (proposal §2).

    Shadow-mode provenance (and the Phase-2 gap, stated so it can't be
    forgotten): in shadow mode these fields come from a POST-TURN peek —
    ``WorkflowOfferService.peek_pending_offer`` after the production turn
    completed, so a pending offer consumed by THIS turn is already gone and
    an offer set BY this turn is visible. Phase 2 must thread the
    PRE-classification state instead: the pending offer popped at the top of
    ``process_intent`` (the #846 store read that currently feeds the
    offer-acceptance seam), the active guided flow from
    ``ProcessRegistry.check_active_processes``, and the user's entity names
    (project/list names) from the owner-scoped repositories — all before the
    router call replaces surface-2 classification.
    """

    pending_offer_summary: Optional[str] = None
    active_flow: Optional[str] = None
    entity_names: Tuple[str, ...] = ()
    # #1595 Phase 2.0: the serialized session_snapshot.SessionSnapshot block
    # (serialize_for_prompt output — bounded, deterministic, golden-pinned).
    # When present it IS the session-state content; the shadow caller no
    # longer duplicates it into the legacy fields above (those remain for
    # the pre-2.0 peek path and batch scorers).
    state_block: Optional[str] = None

    def is_empty(self) -> bool:
        return not (
            self.pending_offer_summary or self.active_flow or self.entity_names or self.state_block
        )


@dataclass(frozen=True)
class RoutingDecision:
    """The router's answer. SHADOW-ONLY: logged and scored, never executed.

    ``outcome`` is one of:
      - ``"operation"`` — a canonical operation was selected (``operation`` set)
      - ``"plan"``      — #1595 unit 4b (#1897), ADDITIVE: the message
                          genuinely asked for 2+ DISTINCT operations, returned
                          in order in ``operations``. ``operation``/``args``/
                          ``confidence``/``rationale`` stay at their dataclass
                          defaults on a plan decision — a plan never populates
                          both ``operation`` and ``operations``. Every element
                          of ``operations`` is validated against the SAME
                          grammar a single-op ``operation`` is (vocabulary, no
                          invented names, confidence numeric/clamped) — see
                          ``_validate_operation_element``.
      - ``"none"``      — the model chose NONE (conversational floor)
      - ``"clarify"``   — the model chose CLARIFY (ask the user)
      - ``"refused"``   — output failed validation twice; recorded honestly,
                          NEVER converted into a guessed route
      - ``"error"``     — the LLM call itself failed; recorded, never faked

    ``operations`` (#1595 unit 4b): populated ONLY when ``outcome == "plan"``;
    each element is a dict shaped exactly like the single-op contract
    (``{"operation": ..., "args": ..., "confidence": ..., "rationale": ...}``)
    — never a second, differently-shaped schema. Empty for every other
    outcome. This field is ADDITIVE: nothing about the existing
    ``operation``/``args``/``confidence``/``rationale`` fields changes shape
    or meaning, and every consumer that checks ``outcome == "operation"``
    (there is exactly one production consumer today,
    ``services/intent_service/inversion_live.py``) is untouched — a
    single-op decision routes byte-identically to before this change.

    ``served_provider``/``served_model`` (#1620): the RESOLVED provider+model
    that actually answered the routing call, after fallback — None when no
    call succeeded (``error``, or every attempt raised before a completion
    returned). This is what m-43 calls the layer the measurement is at: a
    cross-run comparison of route labels is only comparable if the model
    that produced them is also recorded, not inferred from what was
    *configured*.

    ``framing`` (#1970, ADR-080 D1/D6 step 1): the TOP-LEVEL
    ``collaboration_gate.FRAMING_*`` value the router claims for the whole
    MESSAGE (not per-element — a single property of how the user spoke, so
    it sits beside ``outcome`` even for a ``"plan"`` decision, never inside
    each ``operations[i]``). No new vocabulary: the parser accepts ONLY the
    gate's existing three strings (``is_valid_framing``) and drops any other
    value to ``None``. This field is LLM-written and unverified provenance —
    a consumer may *prefer* it but never trust it beyond what
    ``consent_gate.evaluate_consent``'s ``framing_hint`` asymmetry allows.
    Stays ``None`` today: the router prompt does not yet ask for it (that is
    ADR-080 step (1), out of scope for this step), so every live decision
    parses it as absent — byte-identical to before this field existed.
    """

    outcome: str
    operation: Optional[str] = None
    args: Dict[str, Any] = field(default_factory=dict)
    confidence: Optional[float] = None
    rationale: str = ""
    operations: List[Dict[str, Any]] = field(default_factory=list)
    llm_calls: int = 0
    repair_attempted: bool = False
    error: Optional[str] = None
    raw_response: Optional[str] = None
    served_provider: Optional[str] = None
    served_model: Optional[str] = None
    framing: Optional[str] = None
    # #2149 step 2 (two-stage router, flag PIPER_INVERSION_TWO_STAGE; both None when the flag
    # is off): ``route_group`` is the stage-1 pick (a plan: the picked groups joined by
    # ","); ``stage_metrics`` holds one dict per stage call sequence:
    # {"stage": 1|2, "latency_ms", "prompt_chars", "response_chars", "llm_calls", "pick"}
    # (+ "group" on stage 2). Token counts are absent: ``complete()`` exposes only the
    # served provider/model, never usage, and nothing here estimates them.
    route_group: Optional[str] = None
    stage_metrics: Optional[List[Dict[str, Any]]] = None

    @property
    def route_label(self) -> str:
        """Compact label for logs/reports: the operation, or the outcome.

        A plan renders as ``PLAN[op1→op2→...]`` (#1595 unit 4b) — an ordered
        arrow chain, never a bag, since sequencing is load-bearing to what the
        plan means once it reaches a dispatch consumer.
        """
        if self.outcome == "operation" and self.operation:
            return self.operation
        if self.outcome == "plan" and self.operations:
            names = "→".join(str(op.get("operation", "?")) for op in self.operations)
            return f"PLAN[{names}]"
        return self.outcome.upper()


def derive_routing_grammar() -> RoutingGrammar:
    """Derive the routing grammar from the LIVE registries, at call time.

    Never hand-write an operation list (Arch, decisions.log 2026-08-09: a
    hand-written schema "is the drift problem relocated to a new file" — the
    registry gained 4 keys in 5 days). A registry mutation MUST change the
    next grammar derivation; a test asserts exactly that.

    Sources, in order:

    1. **The action rail** (``get_action_workflows()`` — the #1124 dispatch
       surface). Aliases are collapsed by shared ``WorkflowEntry`` OBJECT
       identity — the ``wired_chat_actions()`` idiom: aliases of one
       operation literally share one entry object, and the canonical name is
       the first-registered key (the cohort convention in
       ``workflow_entries.py``). NOTE deliberately NOT the Phase-0 scorer's
       ``entry_point`` collapse: ``create_reminder`` (WRITE) and the todo
       READ keys share ``run_todo_query_workflow`` as a delegation entry
       point while being distinct operations with distinct declared effects —
       entry_point-collapse would erase that distinction from the grammar.
       (The scorer keeps entry_point equivalence for SCORING, unchanged, so
       Phase-1 numbers stay comparable to the Phase-0 baseline.)

    2. **``ACTION_REGISTRY``** — canonical (category, action) pairs whose
       action has no rail key (the CANONICAL/FLOOR-disposition surface:
       greeting, get_identity, manage_portfolio, get_contextual_guidance,
       …). The Phase-0 corpus asserts several of these as expected actions,
       so a rail-only grammar would make those rows unanswerable by
       construction. A registry action is SKIPPED when a synonymous rail
       canonical already covers it (exact name, ``_query``-suffix sibling
       either direction) — PA's rule: no synonymous options in the catalog.

    Descriptions are registry metadata (rail ``entry.description`` with
    internal issue markers stripped; ``ACTION_DESCRIPTIONS`` for
    registry-only canonicals, with the honest disposition fallback when an
    entry has none; ``ACTION_EXAMPLES`` examples attached where present) —
    never hand-written here (#1595 Phase 1b Family-1 enrichment: the fix for
    a grammar-description gap is richer REGISTRY metadata, this function
    only derives).
    """
    from services.intent_service.action_registry import (
        ACTION_DESCRIPTIONS,
        ACTION_EXAMPLES,
        ACTION_REGISTRY,
        ROUTE_GROUPS,
    )
    from services.intent_service.router_catalog_order import order_operations
    from services.intent_service.workflow_dispatcher import get_action_workflows
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()  # idempotent
    workflows = get_action_workflows()

    # Example lookup by bare action name (ACTION_EXAMPLES keys are
    # (category, action); action names are globally unique per the registry's
    # own ACTION_TO_VERB keying).
    examples_by_action = {action: ex for (_, action), ex in ACTION_EXAMPLES.items()}

    # 1. Rail operations — collapse aliases by shared entry object.
    ops: list[RoutingOperation] = []
    by_entry_id: dict[int, dict] = {}
    order: list[int] = []
    hidden: set[str] = set()
    for key, entry in workflows.items():  # dict preserves registration order
        # #2132 option (b): a router-hidden entry adds no op and no catalog text; its
        # keys are still "covered" so the registry pass below never re-adds them.
        if not getattr(entry, "router_visible", True):
            hidden.add(key)
            continue
        rec = by_entry_id.get(id(entry))
        if rec is None:
            by_entry_id[id(entry)] = {"canonical": key, "aliases": [], "entry": entry}
            order.append(id(entry))
        else:
            rec["aliases"].append(key)

    covered: set[str] = set(hidden)
    alias_to_canonical: dict[str, str] = {}
    for eid in order:
        rec = by_entry_id[eid]
        desc = _DESC_NOISE_RE.sub("", rec["entry"].description or "").strip()
        ops.append(
            RoutingOperation(
                name=rec["canonical"],
                description=desc or rec["canonical"].replace("_", " "),
                example=examples_by_action.get(rec["canonical"]),
                aliases=tuple(rec["aliases"]),
                source="rail",
                route_group=getattr(rec["entry"], "route_group", None),
            )
        )
        covered.add(rec["canonical"])
        alias_to_canonical[rec["canonical"]] = rec["canonical"]
        for a in rec["aliases"]:
            covered.add(a)
            alias_to_canonical[a] = rec["canonical"]

    # 2. ACTION_REGISTRY actions with no rail coverage (nor a synonymous
    #    rail sibling differing only by the legacy `_query` suffix).
    for (category, action), disposition in ACTION_REGISTRY.items():
        if (
            action in covered
            or f"{action}_query" in covered
            or (action.endswith("_query") and action[: -len("_query")] in covered)
        ):
            continue
        example = ACTION_EXAMPLES.get((category, action))
        description = ACTION_DESCRIPTIONS.get((category, action))
        ops.append(
            RoutingOperation(
                name=action,
                # Enriched registry metadata where present (#1595 Phase 1b);
                # otherwise the honest fallback — the catalog says only what
                # the registry actually records, never an invented claim.
                description=description
                or f"{category.lower()} action ({disposition.value}-handled)",
                example=example,
                aliases=(),
                source="action_registry",
                route_group=ROUTE_GROUPS.get((category, action)),
            )
        )
        covered.add(action)
        alias_to_canonical[action] = action

    # #2195 (Arch, decisions.log 2026-10-29 19:39): membership is derived above;
    # ORDER comes from the append-only ledger, so a registration or a rail entry
    # for an existing op never moves a rendered catalog line.
    ops = order_operations(ops)
    return RoutingGrammar(operations=tuple(ops), alias_to_canonical=alias_to_canonical)


# ---------------------------------------------------------------------------
# Prompt construction (this prompt is NEW and owned by the router — no change
# to any existing surface's prompt; the routing moratorium is untouched).
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = (
    "You are the intent router for Piper Morgan, a product-management "
    "assistant. Your ONLY job is to select which single operation should "
    "handle the user's message. You never answer the message yourself.\n\n"
    "Rules:\n"
    "- Choose exactly ONE operation name from the provided catalog, or "
    f"{NONE_ROUTE} when no catalog operation applies (the message is "
    "conversational, out of scope, or best answered in prose), or "
    f"{CLARIFY_ROUTE} when the message is genuinely ambiguous between "
    "materially different operations.\n"
    "- Route what the user asked for, never the steps you would take to do "
    "it: 'archive the project' is the archive operation alone, not a lookup "
    "followed by an archive. A destructive ask routes to the destructive "
    "operation itself, never to a listing 'first'.\n"
    "- The same operation applied to several targets ('mark 1, 2 and 4 "
    "done') is ONE operation with those targets in args.\n"
    "- If the message contains a refusal or topic change while a flow is "
    "active, route the user's actual words, not the flow's expectation.\n"
    "- Extract obvious arguments (issue numbers, project names, times, "
    "repo names) into args as simple key/value strings.\n"
    "- Respond with STRICT JSON only, no prose, no markdown fences, as a "
    "single object:\n"
    '{"operation": "<name>", "args": {}, "confidence": <0.0-1.0>, '
    '"rationale": "<at most 15 words>"}\n'
    "- Rare exception — a message that EXPLICITLY asks for two or more "
    "DIFFERENT operations (typically joined by 'and', 'also' or 'then', "
    "e.g. 'close the issue and remind me Friday'): reply with a plan object "
    "listing each requested operation in the user's order, each element in "
    "the single-object shape above:\n"
    '{"outcome": "plan", "operations": [{"operation": "<name>", "args": {}, '
    '"confidence": <0.0-1.0>, "rationale": "<at most 15 words>", '
    '"text": "<the user\'s own words for this part, copied exactly>"}, ...]}\n'
    "  Use the plan form only for that case; one request is always a single "
    'object, however many clauses it has. In a plan, each element\'s "text" '
    "is a verbatim, contiguous quote of the part of the message it covers — "
    "copy the user's words, do not paraphrase."
)


def _session_state_lines(session_state: Optional[SessionSnapshot]) -> List[str]:
    """The session-state block, shared by the flat prompt and both two-stage prompts."""
    lines: List[str] = []
    if session_state is not None and not session_state.is_empty():
        lines.append("")
        lines.append("Session state:")
        if session_state.state_block:
            # #1595 Phase 2.0: the contract-serialized snapshot, verbatim —
            # already bounded (≤ MAX_SERIALIZED_CHARS) and golden-pinned.
            lines.append(session_state.state_block)
        if session_state.pending_offer_summary:
            lines.append(f"- pending offer: {session_state.pending_offer_summary}")
        if session_state.active_flow:
            lines.append(f"- active guided flow: {session_state.active_flow}")
        if session_state.entity_names:
            names = ", ".join(session_state.entity_names[:20])
            lines.append(f"- the user's entity names: {names}")

    return lines


def build_routing_prompt(
    utterance: str,
    grammar: RoutingGrammar,
    session_state: Optional[SessionSnapshot] = None,
) -> str:
    """Build the user-side prompt: catalog + optional session state + message."""
    lines = [
        "Operation catalog (choose exactly one; a message explicitly asking "
        "for two or more different operations may use the plan form in the "
        "system instructions):"
    ]
    for op in grammar.operations:
        entry = f"- {op.name}: {op.description}"
        if op.example:
            entry += f' (e.g. "{op.example}")'
        lines.append(entry)
    lines.append(f"- {NONE_ROUTE}: no catalog operation applies")
    lines.append(f"- {CLARIFY_ROUTE}: genuinely ambiguous; ask the user")

    lines.extend(_session_state_lines(session_state))

    lines.append("")
    lines.append(f"User message: {utterance!r}")
    return "\n".join(lines)


def _extract_json_object(response: str) -> Optional[str]:
    """Extract the first balanced top-level JSON object from a reply.

    #1595 unit 4b: replaces the earlier fixed-one-level-of-nesting regex
    (``\\{[^{}]*(?:\\{[^{}]*\\}[^{}]*)*\\}``), which could represent a
    single-op object's own nested ``args`` dict (one level) but not a PLAN
    object — ``{"outcome": "plan", "operations": [{"operation": ..., "args":
    {...}}, ...]}`` nests THREE levels deep (plan → operations[i] → args).
    Tracks string literals (including escaped quotes) so a brace inside a
    quoted value is never mistaken for structure; depth-balances braces of
    any nesting depth. Byte-identical behavior for every single-op reply the
    old regex already matched (single-level nesting is a special case of
    arbitrary-depth balancing).
    """
    start = response.find("{") if response else -1
    if start == -1:
        return None
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(response)):
        ch = response[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return response[start : i + 1]
    return None


def _validate_operation_element(
    parsed: Dict[str, Any], grammar: RoutingGrammar
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Validate ONE operation object against the grammar.

    Shared by the single-op parse path and each element of a plan's
    ``operations`` list (#1595 unit 4b) — same vocabulary constraint, same
    rejection of invented names, same confidence clamp, applied identically
    whether the object stands alone or lives inside a plan.
    """
    operation = parsed.get("operation")
    if not isinstance(operation, str) or not operation.strip():
        return None, "missing or non-string 'operation'"
    operation = operation.strip()
    if not grammar.is_valid_route(operation):
        return None, (
            f"'{operation}' is not in the operation catalog "
            f"(and is not {NONE_ROUTE}/{CLARIFY_ROUTE})"
        )
    args = parsed.get("args")
    if args is not None and not isinstance(args, dict):
        return None, "'args' must be an object"
    confidence = parsed.get("confidence")
    if confidence is not None and not isinstance(confidence, (int, float)):
        return None, "'confidence' must be a number"
    return (
        {
            "operation": operation,
            "args": dict(args or {}),
            "confidence": (
                max(0.0, min(1.0, float(confidence))) if confidence is not None else None
            ),
            "rationale": str(parsed.get("rationale") or "")[:200],
            # #1606: a plan element's verbatim slice of the user's words (the
            # single-op shape never carries one — the whole message is its
            # text). Validated against the message in _parse_and_validate.
            "text": str(parsed.get("text") or "")[:500],
        },
        None,
    )


def _extract_framing(parsed: Dict[str, Any]) -> Optional[str]:
    """The top-level ``"framing"`` claim (#1970), validated against the
    gate's own vocabulary (``collaboration_gate.is_valid_framing`` — no new
    enum here, per ADR-080 D1). Anything else — wrong type, an unknown
    string, a missing key — drops to ``None``: an invalid or absent claim is
    silently ignored, never passed on as if it were valid. Shared by both
    accepted shapes (single-op and plan) because ``parsed`` is always the
    TOP-LEVEL JSON object in both cases — the plan shape never nests
    ``framing`` inside an element (see ``RoutingDecision.framing``)."""
    from services.intent_service.collaboration_gate import is_valid_framing

    value = parsed.get("framing")
    return value if is_valid_framing(value) else None


def _parse_and_validate(
    response: str, grammar: RoutingGrammar
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Parse the model reply against the contract. Returns (parsed, error).

    Two accepted top-level shapes (#1595 unit 4b, ADDITIVE — the single-op
    shape is byte-identical to before this change and remains the default):

    - a single operation object (no ``"outcome"`` key, or any ``"outcome"``
      value other than ``"plan"`` — unchanged validation, unchanged return
      shape: ``{"operation", "args", "confidence", "rationale"}``);
    - a plan object, ``{"outcome": "plan", "operations": [<op>, ...]}``.
      EVERY element is validated against the grammar exactly as a single
      object is (:func:`_validate_operation_element`) — vocabulary, no
      invented names, confidence numeric/clamped. Any of the following makes
      the WHOLE plan invalid — the same parse failure a bad single object
      gets (the repair path), never partial acceptance of the valid
      elements: fewer than 2 elements; any element that is not an object;
      any element that fails ``_validate_operation_element``; any element
      resolving to the ``NONE``/``CLARIFY`` sentinel (a plan is a list of
      real operations, not sentinels); or fewer than 2 DISTINCT operation
      names among the validated elements (a plan whose elements are all the
      same operation collapses to nothing special and is rejected).
    """
    raw = _extract_json_object(response or "")
    if not raw:
        return None, "no JSON object found in reply"
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as e:
        return None, f"invalid JSON: {e}"
    if not isinstance(parsed, dict):
        return None, "top-level JSON value is not an object"

    if parsed.get("outcome") == "plan":
        operations = parsed.get("operations")
        if not isinstance(operations, list):
            return None, "'operations' must be a list when outcome is 'plan'"
        if len(operations) < 2:
            return None, "a plan must carry at least 2 operations"
        validated: List[Dict[str, Any]] = []
        for i, element in enumerate(operations):
            if not isinstance(element, dict):
                return None, f"plan operations[{i}] is not an object"
            v, err = _validate_operation_element(element, grammar)
            if v is None:
                return None, f"plan operations[{i}]: {err}"
            if v["operation"] in (NONE_ROUTE, CLARIFY_ROUTE):
                return None, (
                    f"plan operations[{i}]: {NONE_ROUTE}/{CLARIFY_ROUTE} "
                    "cannot appear inside a plan"
                )
            validated.append(v)
        distinct = {v["operation"] for v in validated}
        if len(distinct) < 2:
            return None, "a plan must name at least 2 DISTINCT operations"
        return {
            "outcome": "plan",
            "operations": validated,
            "framing": _extract_framing(parsed),
        }, None

    op_result, err = _validate_operation_element(parsed, grammar)
    if op_result is None:
        return None, err
    op_result["framing"] = _extract_framing(parsed)
    return op_result, None


@dataclass
class _StageResult:
    """What one LLM stage (initial call + at most ONE repair retry) produced."""

    parsed: Optional[Any] = None
    validation_error: Optional[str] = None  # the last parse/validate error, when parsed is None
    llm_error: Optional[str] = None  # set when complete() itself raised
    raw: Optional[str] = None
    llm_calls: int = 0
    repair_attempted: bool = False
    prompt_chars: int = 0
    response_chars: int = 0
    latency_ms: float = 0.0
    # #2149 step 3: the provider's own token counts, summed over the stage's calls,
    # when complete() reported them in served["usage"]; None when it did not.
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None


async def _complete_with_repair(
    llm_service: Any,
    *,
    system: str,
    prompt: str,
    parse: Callable[[str], Tuple[Optional[Any], Optional[str]]],
    repair_prompt: Callable[[str, Optional[str]], str],
    user_id: Optional[str],
    served: Dict[str, str],
) -> _StageResult:
    """The router's call loop: one call, then ONE repair retry on a parse/validation
    failure. Shared by the flat path and each two-stage stage, so the single
    transport-failure handler below serves both."""
    result = _StageResult()
    started = time.perf_counter()
    last_error: Optional[str] = None
    for attempt in (1, 2):  # initial + ONE repair retry
        attempt_prompt = prompt
        if attempt == 2:
            result.repair_attempted = True
            attempt_prompt = repair_prompt(prompt, last_error)
        try:
            result.llm_calls += 1
            result.prompt_chars += len(system) + len(attempt_prompt)
            raw = await llm_service.complete(
                task_type=TASK_TYPE,
                prompt=attempt_prompt,
                system=system,
                response_format={"type": "json_object"},
                user_id=user_id,
                served=served,
            )
        except Exception as e:  # silent-ok: returned as an explicit ERROR decision + warning log — an honest recorded failure, never a faked route (#1595 scorer discipline)
            # ERROR is recorded, never faked into a route (scorer discipline).
            logger.warning("inversion_route_llm_error", error=str(e), llm_calls=result.llm_calls)
            result.llm_error = f"{type(e).__name__}: {e}"
            break
        result.raw = raw
        result.response_chars += len(raw) if isinstance(raw, str) else 0
        usage = served.get("usage") if isinstance(served, dict) else None
        if isinstance(usage, dict) and usage.get("input_tokens") is not None:
            result.input_tokens = (result.input_tokens or 0) + int(usage.get("input_tokens") or 0)
            result.output_tokens = (result.output_tokens or 0) + int(
                usage.get("output_tokens") or 0
            )
            served.pop(
                "usage", None
            )  # one call's numbers, consumed here; never carried to the next
        parsed, err = parse(raw)
        if parsed is not None:
            result.parsed = parsed
            result.validation_error = None
            break
        last_error = err
        result.validation_error = err
    result.latency_ms = (time.perf_counter() - started) * 1000.0
    return result


def _flat_repair_prompt(prompt: str, last_error: Optional[str]) -> str:
    # #1595 unit 4b: SHAPE-AWARE repair. Arch flagged this exact spot
    # (2026-09-26 ruling): the pre-4b repair prompt hard-coded "exactly
    # one object", which would tell a model that had correctly reached
    # for a plan on attempt 1 (and only mis-shaped an element, e.g. a
    # confidence string, or answered with 1 operation instead of 2+)
    # to throw the plan away and collapse to a single op — silently
    # discarding a genuine multi-operation request on the SECOND
    # attempt. The repair prompt now restates BOTH accepted shapes,
    # exactly as the system prompt teaches them.
    return (
        f"{prompt}\n\n"
        f"Your previous reply was invalid: {last_error}.\n"
        "Reply again with STRICT JSON only — either a single object "
        'of the form {"operation": "<name>", "args": {}, '
        '"confidence": <0.0-1.0>, "rationale": "<short>"}, or, only '
        "if the message genuinely asks for 2 or more distinct "
        'operations, a plan object of the form {"outcome": "plan", '
        '"operations": [{"operation": "<name>", "args": {}, '
        '"confidence": <0.0-1.0>, "rationale": "<short>"}, ...]}.'
    )


# ---------------------------------------------------------------------------
# #2149 build step 2: the two-stage router (flag PIPER_INVERSION_TWO_STAGE, default OFF).
# Stage 1 picks a RouteGroup (or NONE / CLARIFY / a plan of groups); stage 2 picks an op
# inside that group (or CLARIFY / OTHER_GROUP). The LLM chooses meaning at both stages;
# code only derives the prompts from the registry and validates the answers. There is no
# phrasing check here, and OTHER_GROUP is never re-routed by code to another group.
# ---------------------------------------------------------------------------

_STAGE1_SYSTEM_PROMPT = (
    "You are the intent router for Piper Morgan, a product-management "
    "assistant. Your ONLY job, at this first step, is to select which ONE "
    "group of operations should handle the user's message. You never answer "
    "the message yourself, and you do not pick an operation yet.\n\n"
    "Rules:\n"
    "- Choose exactly ONE group name from the provided list, or "
    f"{NONE_ROUTE} when no group applies (the message is conversational, "
    "out of scope, or best answered in prose), or "
    f"{CLARIFY_ROUTE} when the message is genuinely ambiguous between "
    "materially different groups.\n"
    "- Route what the user asked for, never the steps you would take to do "
    "it. A destructive ask goes to the group that holds the destructive "
    "operation, never to a listing 'first'.\n"
    "- If the message contains a refusal or topic change while a flow is "
    "active, route the user's actual words, not the flow's expectation.\n"
    "- Respond with STRICT JSON only, no prose, no markdown fences, as a "
    "single object:\n"
    '{"group": "<group name>", "confidence": <0.0-1.0>, '
    '"rationale": "<at most 15 words>"}\n'
    "- Rare exception — a message that EXPLICITLY asks for two or more "
    f"DIFFERENT operations (at most {MAX_PLAN_GROUPS}), typically joined by "
    "'and', 'also' or 'then': reply with a plan object listing the group "
    "for each requested operation in the user's order:\n"
    '{"outcome": "plan", "groups": [{"group": "<group name>", '
    '"text": "<the user\'s own words for this part, copied exactly>"}, ...]}\n'
    "  Use the plan form only for that case; one request is always a single "
    "object, however many clauses it has."
)

_STAGE2_SYSTEM_PROMPT = (
    "You are the intent router for Piper Morgan, a product-management "
    "assistant. A first step has already chosen the group of operations "
    "below. Your ONLY job is to select which single operation in that group "
    "should handle the user's message. You never answer the message "
    "yourself.\n\n"
    "Rules:\n"
    "- Choose exactly ONE operation name from the provided list, or "
    f"{CLARIFY_ROUTE} when the message is genuinely ambiguous between "
    f"materially different operations in it, or {OTHER_GROUP_ROUTE} when "
    "none of the listed operations is what the user asked for because the "
    "message belongs to a different group.\n"
    "- Route what the user asked for, never the steps you would take to do "
    "it: 'archive the project' is the archive operation alone, not a lookup "
    "followed by an archive.\n"
    "- The same operation applied to several targets ('mark 1, 2 and 4 "
    "done') is ONE operation with those targets in args.\n"
    "- Extract obvious arguments (issue numbers, project names, times, "
    "repo names) into args as simple key/value strings.\n"
    "- Respond with STRICT JSON only, no prose, no markdown fences, as a "
    "single object:\n"
    '{"operation": "<name>", "args": {}, "confidence": <0.0-1.0>, '
    '"rationale": "<at most 15 words>"}'
)


def build_stage1_prompt(
    utterance: str,
    session_state: Optional[SessionSnapshot] = None,
) -> str:
    """Stage 1 user prompt: one line per RouteGroup (enum order) + NONE + CLARIFY +
    the session state + the message. Names no operation."""
    lines = [
        "Group list (choose exactly one; a message explicitly asking for two "
        "or more different operations may use the plan form in the system "
        "instructions):"
    ]
    for group in RouteGroup:
        lines.append(f"- {group.value}: {ROUTE_GROUP_LINES[group]}")
    lines.append(f"- {NONE_ROUTE}: no group applies")
    lines.append(f"- {CLARIFY_ROUTE}: genuinely ambiguous; ask the user")
    lines.extend(_session_state_lines(session_state))
    lines.append("")
    lines.append(f"User message: {utterance!r}")
    return "\n".join(lines)


def build_stage2_prompt(
    utterance: str,
    grammar: RoutingGrammar,
    group: RouteGroup,
    session_state: Optional[SessionSnapshot] = None,
    part_text: Optional[str] = None,
) -> str:
    """Stage 2 user prompt: ONLY ``group``'s operations (same per-op line as the flat
    catalog) + CLARIFY + OTHER_GROUP + the session state + the message. ``part_text``
    is a plan element's own words, when this call serves one part of a plan."""
    lines = [f"Operations in the {group.value} group (choose exactly one):"]
    for op in grammar.operations:
        if op.route_group is not group:
            continue
        entry = f"- {op.name}: {op.description}"
        if op.example:
            entry += f' (e.g. "{op.example}")'
        lines.append(entry)
    lines.append(f"- {CLARIFY_ROUTE}: genuinely ambiguous; ask the user")
    lines.append(
        f"- {OTHER_GROUP_ROUTE}: none of the operations above is what the "
        "user asked for; the message belongs to a different group"
    )
    lines.extend(_session_state_lines(session_state))
    lines.append("")
    lines.append(f"User message: {utterance!r}")
    if part_text:
        lines.append(f"Route only this part of the message now: {part_text!r}")
    return "\n".join(lines)


def _parse_stage1(response: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Parse a stage-1 reply: ``{"group": <RouteGroup value | NONE | CLARIFY>, ...}`` or
    the plan form ``{"outcome": "plan", "groups": [...]}`` (2..MAX_PLAN_GROUPS)."""
    raw = _extract_json_object(response or "")
    if not raw:
        return None, "no JSON object found in reply"
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as e:
        return None, f"invalid JSON: {e}"
    if not isinstance(parsed, dict):
        return None, "top-level JSON value is not an object"
    valid_groups = {g.value for g in RouteGroup}

    if parsed.get("outcome") == "plan":
        groups = parsed.get("groups")
        if not isinstance(groups, list):
            return None, "'groups' must be a list when outcome is 'plan'"
        if len(groups) < 2 or len(groups) > MAX_PLAN_GROUPS:
            return None, f"a plan must carry 2 to {MAX_PLAN_GROUPS} groups"
        elements: List[Dict[str, Any]] = []
        for i, element in enumerate(groups):
            if not isinstance(element, dict):
                return None, f"plan groups[{i}] is not an object"
            name = element.get("group")
            if not isinstance(name, str) or name.strip() not in valid_groups:
                return None, f"plan groups[{i}]: not a group in the list"
            elements.append({"group": name.strip(), "text": str(element.get("text") or "")[:500]})
        return {"outcome": "plan", "groups": elements, "framing": _extract_framing(parsed)}, None

    name = parsed.get("group")
    if not isinstance(name, str) or not name.strip():
        return None, "missing or non-string 'group'"
    name = name.strip()
    if name not in valid_groups and name not in (NONE_ROUTE, CLARIFY_ROUTE):
        return None, (
            f"'{name}' is not in the group list (and is not {NONE_ROUTE}/{CLARIFY_ROUTE})"
        )
    confidence = parsed.get("confidence")
    if confidence is not None and not isinstance(confidence, (int, float)):
        return None, "'confidence' must be a number"
    return {
        "group": name,
        "confidence": max(0.0, min(1.0, float(confidence))) if confidence is not None else None,
        "rationale": str(parsed.get("rationale") or "")[:200],
        "framing": _extract_framing(parsed),
    }, None


def _parse_stage2(
    response: str, grammar: RoutingGrammar, group: RouteGroup
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Parse a stage-2 reply. Validation is the existing ``_parse_and_validate`` against
    the FULL grammar, plus: the op must belong to the stage-1 ``group`` (NONE and plans
    are not offered at this stage). OTHER_GROUP is returned as ``{"operation":
    OTHER_GROUP_ROUTE, ...}``."""
    raw = _extract_json_object(response or "")
    if raw:
        try:
            loose = json.loads(raw)
        except json.JSONDecodeError:
            loose = None
        if isinstance(loose, dict) and loose.get("operation") == OTHER_GROUP_ROUTE:
            return {
                "operation": OTHER_GROUP_ROUTE,
                "args": {},
                "confidence": None,
                "rationale": str(loose.get("rationale") or "")[:200],
                "framing": _extract_framing(loose),
            }, None
    parsed, err = _parse_and_validate(response, grammar)
    if parsed is None:
        return None, err
    if parsed.get("outcome") == "plan":
        return None, "a plan is not offered at this step; choose one operation"
    operation = parsed["operation"]
    if operation == NONE_ROUTE:
        return None, f"{NONE_ROUTE} is not offered at this step"
    if operation != CLARIFY_ROUTE:
        member = next((op for op in grammar.operations if op.name == operation), None)
        if member is None or member.route_group is not group:
            return None, f"'{operation}' is not in the {group.value} group"
    return parsed, None


def _stage1_repair_prompt(prompt: str, last_error: Optional[str]) -> str:
    return (
        f"{prompt}\n\n"
        f"Your previous reply was invalid: {last_error}.\n"
        "Reply again with STRICT JSON only — either "
        '{"group": "<group name>", "confidence": <0.0-1.0>, '
        '"rationale": "<short>"}, or, only if the message genuinely asks '
        'for 2 or more distinct operations, {"outcome": "plan", "groups": '
        '[{"group": "<group name>", "text": "<the user\'s words>"}, ...]}.'
    )


def _stage2_repair_prompt(prompt: str, last_error: Optional[str]) -> str:
    return (
        f"{prompt}\n\n"
        f"Your previous reply was invalid: {last_error}.\n"
        "Reply again with STRICT JSON only, a single object of the form "
        '{"operation": "<name>", "args": {}, "confidence": <0.0-1.0>, '
        '"rationale": "<short>"}.'
    )


def _stage_metric(
    stage: int, result: _StageResult, pick: Optional[str], group: Optional[str] = None
) -> Dict[str, Any]:
    metric: Dict[str, Any] = {
        "stage": stage,
        "latency_ms": result.latency_ms,
        "prompt_chars": result.prompt_chars,
        "response_chars": result.response_chars,
        "llm_calls": result.llm_calls,
        "pick": pick,
    }
    if result.input_tokens is not None:  # present only when the provider reported usage
        metric["input_tokens"] = result.input_tokens
        metric["output_tokens"] = result.output_tokens
    if group is not None:
        metric["group"] = group
    return metric


async def _route_two_stage(
    utterance: str,
    session_state: Optional[SessionSnapshot],
    *,
    llm_service: Any,
    grammar: RoutingGrammar,
    user_id: Optional[str],
) -> RoutingDecision:
    served: Dict[str, str] = {}
    metrics: List[Dict[str, Any]] = []
    llm_calls = 0
    repaired = False
    picked: Optional[str] = None

    def decision(outcome: str, **kw: Any) -> RoutingDecision:
        return RoutingDecision(
            outcome=outcome,
            llm_calls=llm_calls,
            repair_attempted=repaired,
            served_provider=served.get("provider"),
            served_model=served.get("model"),
            route_group=picked,
            stage_metrics=list(metrics),
            **kw,
        )

    def failure(res: _StageResult) -> RoutingDecision:
        if res.llm_error is not None:
            # served is not reported on an error decision (as in the flat path)
            return RoutingDecision(
                outcome="error",
                llm_calls=llm_calls,
                repair_attempted=repaired,
                error=res.llm_error,
                route_group=picked,
                stage_metrics=list(metrics),
            )
        logger.warning("inversion_route_refused", reason=res.validation_error, llm_calls=llm_calls)
        return decision("refused", error=res.validation_error, raw_response=res.raw)

    # ---- stage 1
    res1 = await _complete_with_repair(
        llm_service,
        system=_STAGE1_SYSTEM_PROMPT,
        prompt=build_stage1_prompt(utterance, session_state),
        parse=_parse_stage1,
        repair_prompt=_stage1_repair_prompt,
        user_id=user_id,
        served=served,
    )
    llm_calls += res1.llm_calls
    repaired = repaired or res1.repair_attempted
    s1 = res1.parsed
    if s1 is None:
        metrics.append(_stage_metric(1, res1, None))
        return failure(res1)
    if s1.get("outcome") == "plan":
        picked = ",".join(el["group"] for el in s1["groups"])
        metrics.append(_stage_metric(1, res1, "PLAN"))
        parts = [(RouteGroup(el["group"]), el["text"]) for el in s1["groups"]]
    else:
        picked = s1["group"]
        metrics.append(_stage_metric(1, res1, picked))
        if picked in (NONE_ROUTE, CLARIFY_ROUTE):
            outcome = "none" if picked == NONE_ROUTE else "clarify"
            return RoutingDecision(
                outcome=outcome,
                confidence=s1["confidence"],
                rationale=s1["rationale"],
                llm_calls=llm_calls,
                repair_attempted=repaired,
                raw_response=res1.raw,
                served_provider=served.get("provider"),
                served_model=served.get("model"),
                framing=s1.get("framing"),
                route_group=picked,
                stage_metrics=list(metrics),
            )
        parts = [(RouteGroup(picked), None)]

    # ---- stage 2: one call per planned group (a single pick is one part)
    ops: List[Dict[str, Any]] = []
    last_raw: Optional[str] = res1.raw
    for group, part_text in parts:

        def parse_stage2(r: str, g: RouteGroup = group) -> Tuple[Optional[Any], Optional[str]]:
            return _parse_stage2(r, grammar, g)

        res2 = await _complete_with_repair(
            llm_service,
            system=_STAGE2_SYSTEM_PROMPT,
            prompt=build_stage2_prompt(utterance, grammar, group, session_state, part_text),
            parse=parse_stage2,
            repair_prompt=_stage2_repair_prompt,
            user_id=user_id,
            served=served,
        )
        llm_calls += res2.llm_calls
        repaired = repaired or res2.repair_attempted
        last_raw = res2.raw
        s2 = res2.parsed
        metrics.append(_stage_metric(2, res2, s2["operation"] if s2 else None, group.value))
        if s2 is None:
            return failure(res2)
        if s2["operation"] in (CLARIFY_ROUTE, OTHER_GROUP_ROUTE):
            # OTHER_GROUP renders as clarify; code never re-routes it to another group.
            return decision(
                "clarify",
                rationale=s2["rationale"],
                confidence=s2["confidence"],
                raw_response=res2.raw,
                framing=s2.get("framing"),
            )
        if part_text is not None:
            s2 = dict(s2, text=part_text)
        ops.append(s2)

    if len(parts) == 1:
        only = ops[0]
        return decision(
            "operation",
            operation=only["operation"],
            args=only["args"],
            confidence=only["confidence"],
            rationale=only["rationale"],
            raw_response=last_raw,
            framing=only.get("framing"),
        )
    if len({o["operation"] for o in ops}) < 2:
        err = "a plan must name at least 2 DISTINCT operations"
        logger.warning("inversion_route_refused", reason=err, llm_calls=llm_calls)
        return decision("refused", error=err, raw_response=last_raw)
    plan_ops = [{k: v for k, v in o.items() if k != "framing"} for o in ops]
    return decision("plan", operations=plan_ops, raw_response=last_raw, framing=s1.get("framing"))


async def route(
    utterance: str,
    session_state: Optional[SessionSnapshot] = None,
    *,
    llm_service: Any = None,
    grammar: Optional[RoutingGrammar] = None,
    user_id: Optional[str],  # #2131: no default; None = a measurement/system call
) -> RoutingDecision:
    """One constrained routing call. SHADOW-ONLY — the result is data.

    ``llm_service`` follows #322 constructor-injection (the container is
    per-app, not a singleton — the counterfactual-probe pattern); when None a
    fresh ``LLMClient`` is built, which resolves keys via the app's own
    config path (Keychain first). ``grammar`` may be passed to amortize
    derivation across a batch (the scorer does); default derives fresh from
    the live registry.

    ``user_id`` threads to ``LLMClient.complete`` for per-principal provider
    selection (#1415) — the router itself reads no user state.

    #2149 step 2: with ``PIPER_INVERSION_TWO_STAGE`` truthy (default OFF, read at
    call time) the op is chosen in two stages (:func:`_route_two_stage`); with it
    off this is the flat one-call path, unchanged.
    """
    if grammar is None:
        grammar = derive_routing_grammar()
    if llm_service is None:
        from services.llm.clients import LLMClient

        llm_service = LLMClient()

    if two_stage_enabled():
        return await _route_two_stage(
            utterance, session_state, llm_service=llm_service, grammar=grammar, user_id=user_id
        )

    prompt = build_routing_prompt(utterance, grammar, session_state)
    served: Dict[str, str] = {}  # #1620: populated on a successful complete() call

    def parse_flat(r: str) -> Tuple[Optional[Any], Optional[str]]:
        return _parse_and_validate(r, grammar)

    res = await _complete_with_repair(
        llm_service,
        system=_SYSTEM_PROMPT,
        prompt=prompt,
        parse=parse_flat,
        repair_prompt=_flat_repair_prompt,
        user_id=user_id,
        served=served,
    )
    llm_calls = res.llm_calls
    repair_attempted = res.repair_attempted
    if res.llm_error is not None:
        return RoutingDecision(
            outcome="error",
            llm_calls=llm_calls,
            repair_attempted=repair_attempted,
            error=res.llm_error,
        )
    parsed = res.parsed
    raw = res.raw
    if parsed is not None:
        if parsed.get("outcome") == "plan":
            # #1595 unit 4b: additive — a plan decision leaves
            # operation/args/confidence/rationale at their defaults.
            return RoutingDecision(
                outcome="plan",
                operations=parsed["operations"],
                llm_calls=llm_calls,
                repair_attempted=repair_attempted,
                raw_response=raw,
                served_provider=served.get("provider"),
                served_model=served.get("model"),
                framing=parsed.get("framing"),
            )
        operation = parsed["operation"]
        outcome = (
            "none"
            if operation == NONE_ROUTE
            else "clarify"
            if operation == CLARIFY_ROUTE
            else "operation"
        )
        return RoutingDecision(
            outcome=outcome,
            operation=operation if outcome == "operation" else None,
            args=parsed["args"],
            confidence=parsed["confidence"],
            rationale=parsed["rationale"],
            llm_calls=llm_calls,
            repair_attempted=repair_attempted,
            raw_response=raw,
            served_provider=served.get("provider"),
            served_model=served.get("model"),
            framing=parsed.get("framing"),
        )

    # Both attempts failed validation → REFUSED, recorded honestly. Never a
    # guessed route: a wrong confident route is worse than an honest refusal.
    logger.warning("inversion_route_refused", reason=res.validation_error, llm_calls=llm_calls)
    return RoutingDecision(
        outcome="refused",
        llm_calls=llm_calls,
        repair_attempted=repair_attempted,
        error=res.validation_error,
        raw_response=res.raw,
        served_provider=served.get("provider"),
        served_model=served.get("model"),
    )
