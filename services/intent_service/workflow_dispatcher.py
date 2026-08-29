"""
Workflow Dispatcher — registry-based routing for offer acceptance.

ADR-059: Replaces the if/elif switch in soft offer acceptance with a
registry lookup. New workflow types are added by registering an entry,
not modifying a switch statement.

Design principle (from OpenClaw Gateway pattern): this is dumb plumbing.
Maps workflow_type → entry_point. No business logic in the dispatch layer.
Unknown workflow types route to the conversational floor (safe default).

Issue #922: Fixes dead-end acceptances where workflow types were added
to the offer map but never wired to real handlers.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Coroutine, Dict, Optional

import structlog

from services.shared_types import EffectClass, Outwardness

logger = structlog.get_logger(__name__)


# ─── #1667 flip groups — the inversion flip UNIT (Lead decision 2026-08-20) ──
# The measurement that forced this: 70 of 93 rail READ keys have NO
# ACTION_REGISTRY category, so a flip flag keyed on registry categories
# addressed 23 of 93 READ operations and silently covered nothing for the rest.
# The thing being flipped is *routing for an operation*, and the operation's
# identity lives HERE, on the rail — so the flip unit is declared here too
# (the #1509 precedent: declare on the entry, derive everything else).
#
# The vocabulary is CLOSED and validated at construction (see
# WorkflowEntry.__post_init__). A typo'd group would otherwise be doubly
# silent: the op becomes unaddressable by any wave AND the flag token that
# names the intended group matches nothing. Adding a wave-2 group means
# editing this set — the deliberate opt-in the decision asked for.
#
#   read_status    — status / listing / identity reads. The zero-armed-state
#                    class: the answer needs no referent resolution and no
#                    temporal-expression parsing. Lowest risk, highest volume.
#   read_referent  — reads that resolve a referent (an issue/PR/document/repo
#                    the user named or implied), plus the analysis family.
#                    This is the group that exercises the snapshot's recent-
#                    referent fields.
#   read_synthesis — the summarize/generate family: output is generated prose
#                    over source material, nothing is written anywhere.
#
# Ops with NO group are unaddressable by any WAVE flip, by design, until
# someone assigns one. `scripts/inversion_phase2_gate.py --audit` lists them
# by name with denominators so "unassigned" is never a silent remainder.
FLIP_GROUPS: frozenset[str] = frozenset({"read_status", "read_referent", "read_synthesis"})


# ─── #1677 named-WRITE flip allowlist (Arch ruling 2026-08-25; PM chose this ──
# option 2026-08-28) — the ONE way a non-READ operation may route via the
# inversion, and it is a NAMED LIST, never a class-wide relaxation.
#
# Why not just relax the guard to `READ or WRITE`: the effect guard caught
# something real. ACTION_REGISTRY files `create_issue` under QUERY (a rail-
# migration artifact, Arch's #1663 find), so a category flag alone is not a
# READ guarantee — the guard reads the entry's TRUE EffectClass and refuses.
# Relaxing the class removes that protection for every future write at once.
# An allowlist keeps it for all of them and spends it on exactly the ops
# someone has looked at.
#
# ⚠️ ADDING AN ENTRY IS NOT A CONFIG CHANGE. Every name below must have had
# ALL THREE of Arch's conditions RE-RUN — not cited from a previous memo:
#
#   1. CONFIRMED REGISTERED on the #1124 action-dispatch rail
#      (`get_action_workflows()[name]` exists, `action_triggered=True`).
#      An unregistered op never reaches the rail at all, so "it's fine, the
#      rail gates it" would be vacuous.
#   2. CONFIRMED the declared EffectClass is CORRECT by READING THE HANDLER'S
#      BEHAVIOR — never a docstring, a name, or a previous reviewer's claim.
#      The whole point of the guard is catching an operation that LIES about
#      its own class; an allowlist entry taken on trust re-opens that hole.
#   3. CONFIRMED it reaches `consent_gate.evaluate_consent` on the shared
#      rail (`entry.needs_consent` derives True and the rail's consent block
#      actually evaluates it) — i.e. the write is COVERED, not merely
#      uncontroversial. "Nothing evaluated it" and "something evaluated it
#      and proceeded" are indistinguishable from a transcript (m-44); only
#      the second one licenses a flip.
#
# Both enforcement points consult THIS constant — `flip_write_allowed()`
# below is used by `WorkflowEntry.__post_init__` (structural) and by
# `inversion_live`'s dispatch check (runtime). They move together on purpose:
# relaxing one and not the other leaves a gap between what is checked and
# what is enforced (Arch, verbatim).
#
#   create_todo — verified 2026-08-28 for #1677 (all three re-run, evidence in
#                 the #1677 commit message and tests/…/test_inversion_write_
#                 allowlist_1677.py). Registered by #1685 (WRITE, PRIVATE,
#                 action_triggered); `todo_handlers.handle_create_todo`
#                 persists one row via `todo_service.create_todo` and deletes
#                 nothing → WRITE, never DESTRUCTIVE; `needs_consent` derives
#                 True and the rail evaluates it (PRIVATE x WRITE x execute
#                 framing = PROCEED, so evaluation without ceremony).
FLIP_WRITE_ALLOWLIST: frozenset[str] = frozenset({"create_todo"})


def flip_write_allowed(entry: "WorkflowEntry") -> bool:
    """Is this entry's effect flip-eligible at all? (#1677)

    READ — always, unchanged (flip-1's contract). Non-READ — only if the entry
    DECLARES an allowlist key that is in ``FLIP_WRITE_ALLOWLIST``. The entry
    declaring its own key is the reviewable act: the constructor cannot see
    the registry key it will be filed under (one entry object serves a whole
    alias family), so the name has to be said at the construction site, beside
    ``effect``, where the #1509 precedent puts every other consent-relevant
    declaration.
    """
    if entry.effect == EffectClass.READ:
        return True
    key = entry.flip_write_allowlist_key
    return key is not None and key in FLIP_WRITE_ALLOWLIST


@dataclass
class WorkflowEntry:
    """
    Registry entry for a dispatchable workflow.

    Attributes:
        entry_point: Async callable that starts the workflow.
            Signature: (session_id, user_id, context) -> IntentProcessingResult
        effect: REQUIRED, DEFAULTLESS (Arch ruling 2026-08-09 / PDR-006
            condition 2, ruled 2026-08-04). What the workflow's operation does
            in the world: EffectClass.READ / WRITE / DESTRUCTIVE (ordered;
            destructive ⊂ write). Not computable from the entry point or
            description — classify by READING the handler, never by its name.
            Defaultless is load-bearing: every other optional field here is
            defaulted, and a defaulted effect would let future entries
            silently inherit a mutation-semantics value nobody chose. The
            construction-site break IS THE FEATURE — you cannot register a
            handler without saying whether it writes. Consumers derive their
            predicates from the properties below; they never re-infer.
        resume_point: Optional async callable for resuming a suspended workflow.
            If None, resume falls back to entry_point with existing session context.
        requires_context: List of context keys the workflow expects.
        description: Human-readable description for logging.
        action_triggered: If True, this workflow may be dispatched directly by a
            classified ``intent.action`` (#1124 pre-floor handler migration), in
            addition to / instead of offer-acceptance. Offer-only workflows (e.g.
            ``meeting``) leave this False so the action-dispatch rail never picks
            them up by an accidental key/action collision.
        flip_group: #1667 inversion flip unit — which wave this operation flips
            with (see FLIP_GROUPS above). DEFAULTS TO None and that default is
            the safe direction: an ungrouped op is unaddressable by any wave
            flip, so a forgotten assignment can only ever under-flip. READ-ONLY
            BY CONSTRUCTION, ONE NAMED EXCEPTION ASIDE — a non-READ entry
            carrying a flip_group raises at construction (__post_init__)
            unless it declares an allowlisted ``flip_write_allowlist_key``
            (#1677), so "a write flipped live" stays unrepresentable except
            for individually reviewed operations. Declared beside effect
            and outwardness, with each assignment's reasoning in the comment
            above it (workflow_entries.py), per the #1509 precedent.
        flip_write_allowlist_key: #1677 named-WRITE flip. The name this entry
            claims in ``FLIP_WRITE_ALLOWLIST`` (see that constant for the three
            verification conditions every entry owes). None for every READ
            entry — READ needs no exception — and None is the safe default: an
            undeclared write cannot flip by any flag configuration. It is a
            NAME, not a boolean, because the inversion's dispatch check also
            requires the ROUTED operation name to be this key: one entry object
            serves an alias family (create_todo/add_todo/new_todo), and the
            declaration alone would not say which of those names was reviewed.
    """

    entry_point: Callable[..., Coroutine[Any, Any, Any]]
    effect: EffectClass
    # #1509 outwardness axis (ratified PM+CXO+PPM 2026-08-15): who else
    # witnesses the action — orthogonal to effect, declared HERE so the two
    # ride together (one declaration site, per the effect precedent). The
    # scope boundary lives on the Outwardness enum (shared_types.py): OUTWARD
    # = the action IS a communication act, nothing broader.
    #
    # DEFAULTED (unlike effect — a deliberate, flagged asymmetry): the
    # default direction is safe in the consent-tier sense. PRIVATE reproduces
    # today's behavior exactly — a mis-defaulted PRIVATE on a future outward
    # action can never skip a gate or weaken a tier (the WRITE consent check
    # and the DESTRUCTIVE confirm are outwardness-independent); the only loss
    # is the TRUST-mode disclosure line, a transparency add-on. Every entry
    # whose effect is WRITE-or-above still declares outwardness EXPLICITLY
    # with evidence (see workflow_entries.py) — the default exists for READ
    # entries, where outwardness cannot alter any consent cell.
    outwardness: Outwardness = Outwardness.PRIVATE
    resume_point: Optional[Callable[..., Coroutine[Any, Any, Any]]] = None
    requires_context: list[str] = field(default_factory=list)
    description: str = ""
    action_triggered: bool = False
    # #1667 flip unit (Lead decision 2026-08-20): the wave this operation
    # flips with, or None = not addressable by any wave flip. Vocabulary +
    # rationale in the FLIP_GROUPS block above; the READ-only invariant is
    # enforced in __post_init__ below, not by convention.
    flip_group: Optional[str] = None
    # #1677 named-WRITE flip allowlist key (Arch ruling 2026-08-25). See the
    # FLIP_WRITE_ALLOWLIST block above; validated in __post_init__ below.
    flip_write_allowlist_key: Optional[str] = None

    def __post_init__(self) -> None:
        """Reject an unrepresentable flip declaration LOUDLY, at construction.

        Three rejections, all at the earliest possible moment (import of
        ``workflow_entries``, i.e. app startup and every test that registers
        the rail) so a bad declaration can never reach a live consult:

        1. **Unknown allowlist key** (#1677) — a typo'd key fails SAFE at
           dispatch (the write simply never flips) and is therefore silent;
           raise instead, so a name that was meant to be reviewed can't sit
           there looking reviewed while naming nothing. Checked before the
           flip_group early-return: the key is meaningful on its own.
        2. **Unknown group name** — a typo would be doubly silent (the op is
           unaddressable AND the flag token names nothing).
        3. **Non-READ entry with a flip_group and NO allowlisted key** — the
           inversion flip is READ-only by contract (#1663 addendum) with the
           one #1677 exception. ``inversion_live`` also checks the effect at
           dispatch time; that check is the belt, THIS is the structural
           guarantee: a WRITE/DESTRUCTIVE entry that nobody put on the
           allowlist cannot be constructed with a group, so no configuration
           of any flag can produce an unreviewed flipped write.
        """
        if (
            self.flip_write_allowlist_key is not None
            and self.flip_write_allowlist_key not in FLIP_WRITE_ALLOWLIST
        ):
            raise ValueError(
                f"Unknown flip_write_allowlist_key "
                f"{self.flip_write_allowlist_key!r} (#1677) on "
                f"{self.description or 'unnamed'}. Allowlisted: "
                f"{sorted(FLIP_WRITE_ALLOWLIST)}. Adding a name to "
                f"FLIP_WRITE_ALLOWLIST owes all three verification conditions "
                f"in that constant's comment — it is not a config change."
            )
        if self.flip_group is None:
            return
        if self.flip_group not in FLIP_GROUPS:
            raise ValueError(
                f"Unknown flip_group {self.flip_group!r} (#1667). Known groups: "
                f"{sorted(FLIP_GROUPS)}. Add a new wave's group to FLIP_GROUPS "
                f"deliberately — a typo here silently unaddresses the operation."
            )
        if not flip_write_allowed(self):
            raise ValueError(
                f"flip_group {self.flip_group!r} declared on a "
                f"{self.effect.name} entry ({self.description or 'unnamed'}) — "
                f"#1667/#1663: the inversion flip is READ-only, with the one "
                f"#1677 exception of an individually verified named write. A "
                f"write must never be flippable by any flag configuration "
                f"unless it declares a flip_write_allowlist_key in "
                f"FLIP_WRITE_ALLOWLIST ({sorted(FLIP_WRITE_ALLOWLIST)}) — and "
                f"adding a name there owes all three verification conditions "
                f"in that constant's comment. Otherwise: remove the "
                f"flip_group, or re-classify the effect if the handler truly "
                f"only reads."
            )

    # ── Derivations (Arch ruling 2026-08-09): one declaration, four ─────────
    # predicates. Each consumer reads ITS property; none re-derives effect
    # from names, descriptions, or write sets.

    @property
    def read_only_hint(self) -> bool:
        """MCP ``readOnlyHint`` annotation (PDR-006 §30, PA's spec)."""
        return self.effect == EffectClass.READ

    @property
    def destructive_hint(self) -> bool:
        """MCP ``destructiveHint`` annotation (PDR-006 §30, PA's spec)."""
        return self.effect == EffectClass.DESTRUCTIVE

    @property
    def needs_consent(self) -> bool:
        """#1509 consent gate: any write (destructive included) needs consent."""
        return self.effect >= EffectClass.WRITE

    @property
    def needs_confirm(self) -> bool:
        """#1190 destructive-mutation gate: destructive writes need explicit
        confirmation on top of consent."""
        return self.effect == EffectClass.DESTRUCTIVE


# ─── Workflow Registry ───────────────────────────────────────────────
# Each entry maps a workflow_type string to its WorkflowEntry.
# To add a new workflow: add an entry here and implement the entry_point.
# The dispatcher handles the routing — no switch statement needed.

WORKFLOW_REGISTRY: Dict[str, WorkflowEntry] = {}


def register_workflow(workflow_type: str, entry: WorkflowEntry) -> None:
    """
    Register a workflow entry point.

    Raises ValueError if workflow_type is already registered
    (prevents silent overwrites).
    """
    if workflow_type in WORKFLOW_REGISTRY:
        raise ValueError(
            f"Workflow type '{workflow_type}' is already registered. "
            f"Existing: {WORKFLOW_REGISTRY[workflow_type].description}"
        )
    WORKFLOW_REGISTRY[workflow_type] = entry
    logger.info(
        "workflow_registered",
        workflow_type=workflow_type,
        description=entry.description,
    )


def get_registered_workflows() -> Dict[str, WorkflowEntry]:
    """Return a copy of the workflow registry for inspection."""
    return dict(WORKFLOW_REGISTRY)


def get_action_workflows() -> Dict[str, WorkflowEntry]:
    """Return only the workflows that may be dispatched by a classified
    ``intent.action`` (#1124). Offer-only workflows (action_triggered=False)
    are excluded so the action-dispatch rail can't pick them up by accident.
    """
    return {k: v for k, v in WORKFLOW_REGISTRY.items() if v.action_triggered}


async def dispatch_workflow(
    workflow_type: str,
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
    resume: bool = False,
) -> Optional[Any]:
    """
    Dispatch a workflow by type.

    Args:
        workflow_type: The type of workflow to start (e.g., "meeting").
        session_id: Current session ID.
        user_id: Current user ID.
        context: Additional context (trigger_message, active_lens, etc.).
        resume: If True, use resume_point instead of entry_point.

    Returns:
        IntentProcessingResult from the workflow entry point, or None if
        the workflow type is unknown (caller should route to floor).
    """
    entry = WORKFLOW_REGISTRY.get(workflow_type)

    if entry is None:
        # ADR-059: Unknown workflow type → log as wiring bug, return None.
        # Caller routes to conversational floor.
        logger.warning(
            "workflow_dispatch_unknown_type",
            workflow_type=workflow_type,
            registered_types=list(WORKFLOW_REGISTRY.keys()),
            reason="no_registered_entry_point",
        )
        return None

    # Choose entry point or resume point
    if resume and entry.resume_point is not None:
        handler = entry.resume_point
        logger.info(
            "workflow_dispatch_resume",
            workflow_type=workflow_type,
            description=entry.description,
        )
    else:
        handler = entry.entry_point
        logger.info(
            "workflow_dispatch_start",
            workflow_type=workflow_type,
            description=entry.description,
            resume_fallback=resume and entry.resume_point is None,
        )

    try:
        return await handler(
            session_id=session_id,
            user_id=user_id,
            context=context or {},
        )
    except Exception as e:
        logger.error(
            "workflow_dispatch_error",
            workflow_type=workflow_type,
            error=str(e),
            exc_info=True,
        )
        return None


def validate_registry() -> list[str]:
    """
    Validate that all registered workflows have callable entry points.

    Returns list of error messages (empty = valid).
    Called at startup to catch wiring bugs early.
    """
    errors = []
    for workflow_type, entry in WORKFLOW_REGISTRY.items():
        if not callable(entry.entry_point):
            errors.append(
                f"Workflow '{workflow_type}' entry_point is not callable: {entry.entry_point}"
            )
        if entry.resume_point is not None and not callable(entry.resume_point):
            errors.append(
                f"Workflow '{workflow_type}' resume_point is not callable: {entry.resume_point}"
            )
    return errors


# ---------------------------------------------------------------------------
# #1283 AC-4 (b): near-miss emission normalization — Arch-ratified 2026-07-08.
#
# The live probe proved the LLM emits paraphrase VARIANTS of canonical action
# names that slip past hand-maintained alias lists (run 1: list_stale_prs past
# four stale aliases; analyze_productivity past four productivity aliases;
# run 2: get_pull_requests, a third stale-family variant). This shim is the
# ruled second net UNDER the aliases (additive — never a reason to prune
# them): a conservative prefix-strip that maps an unknown emission to a rail
# key only on an EXACT post-strip match — unambiguous by construction. No
# fuzzy scoring: a wrong confident map is worse than a pass-through (the
# pass-through still lands in category handling, and the structured log line
# feeds the alias/vocabulary loop).
# ---------------------------------------------------------------------------

_NORMALIZE_PREFIXES = ("list_", "get_", "show_", "analyze_", "fetch_", "display_")


def normalize_action(action: str) -> str:
    """Map a near-miss LLM action emission onto its rail key, conservatively.

    Known action (already a rail key) → unchanged. Unknown action whose
    prefix-stripped form IS a rail key → that key (logged). Anything else →
    unchanged (falls through to category routing exactly as before this shim).
    """
    if not action:
        return action
    workflows = get_action_workflows()
    if action in workflows:
        return action
    for prefix in _NORMALIZE_PREFIXES:
        if action.startswith(prefix):
            stripped = action[len(prefix) :]
            if stripped in workflows:
                logger.info("action_normalized", emitted=action, rail_key=stripped)
                return stripped
    logger.debug("action_unnormalized", emitted=action)
    return action


# ---------------------------------------------------------------------------
# #1517 wired-capability derivation — the capability-gaslighting fix's source.
#
# Incident (PM live, 2026-08-08): a floor turn DENIED a wired capability
# ("I can't actually set reminders from chat") and fabricated a retraction of
# a real prior create_reminder success. The floor had no manifest of what IS
# wired, so it improvised — and improvised a lie. The manifest source below is
# DERIVED, never hand-maintained (a hand list would drift exactly like the
# UNWIRED_WRITE_ACTIONS list #1333 retired):
#
#   1. The workflow registry's action_triggered entries (this module) — the
#      #1124 rail, effect-classified WorkflowEntries (PDR-006). Canonical
#      name = first-registered key per unique entry (aliases follow their
#      canonical in every _default_entries cohort).
#   2. The legacy _handle_execution_intent elif chain, enumerated by
#      ActionMapper.ACTION_MAPPING's TARGET names (#284) — the mapper's
#      values are exactly the handler tokens that chain dispatches (e.g.
#      create_reminder, the incident capability, which is NOT rail-registered).
#      The "unknown_intent" fallback sentinel is excluded: it is a routing
#      outcome, not a capability.
# ---------------------------------------------------------------------------


def wired_chat_actions() -> list[str]:
    """Canonical action names genuinely wired for chat dispatch, sorted.

    Derived at call time from the two dispatch surfaces above — see the
    block comment. Consumers: the conversational floor's capability
    manifest (#1517) and its tests.
    """
    # Lazy imports: workflow_entries imports this module at module level,
    # and ActionMapper is EXECUTION-legacy plumbing this module otherwise
    # doesn't need.
    from services.intent_service.action_mapper import ActionMapper
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()  # idempotent; no-op when already registered

    wired: set[str] = set()

    # 1. Registry rail — one canonical name per unique action-triggered entry.
    seen_entries: set[int] = set()
    for key, entry in WORKFLOW_REGISTRY.items():
        if not entry.action_triggered:
            continue  # offer-only (e.g. "meeting") — never action-dispatched
        if id(entry) in seen_entries:
            continue  # alias of an already-named entry
        seen_entries.add(id(entry))
        wired.add(key)

    # 2. Legacy EXECUTION elif chain, via the mapper's target names.
    wired |= set(ActionMapper.ACTION_MAPPING.values()) - {"unknown_intent"}

    return sorted(wired)
