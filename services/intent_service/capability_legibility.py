"""#1509 TRUST-CONSENT — capability legibility, DERIVED end to end.

The other half of the one feature (CXO synthesis pairing, four-lens 07-31):
the consent gate makes the action safe AFTER intent forms; THIS surface makes
the action discoverable WHILE intent forms. "Legibility without the gate is
dangerous; the gate without legibility is merely safe."

THE DERIVATION CHAIN (nothing here is hand-written per capability — the
#1517/#1428/#1433 discipline, extended):

    workflow registry (WorkflowEntry.effect, declared per #1557)
        -> decide_consent (consent_gate.py — THE one decision function)
            -> per-effect behavior lines (what happens on an ambiguous ask)
    workflow registry (WorkflowEntry.outwardness, declared per #1509)
        -> per-entry outward marker (#1632: which actions land in front of
           other people — OUTWARD entries only; absence means private, a
           convention stated ONCE in :data:`OUTWARDNESS_CONVENTION`)
    chat_pointers ledger (POINTER rows, resolution-VERIFIED by the #1433
    reachability ratchet on every build)
        -> example asks (real, routable phrasings — never a taught phrase
           that doesn't route, #1571)
    ==> capability_catalog(): one structured description per unique
        action-triggered rail entry.

CONSUMERS:
- (Until #2304, ``consent_gate.build_consent_check_offer`` also stated the
  held action's effect tier via :func:`describe_effect`. CXO 11-06: the check
  now asks the op's own question naming the thing, in the ordinary confirms'
  shape, so it no longer carries the effect phrase.)
- #1462 (tool-catalog descriptions under PDR-006): :func:`capability_catalog`
  is the seam that work consumes — entry-point copy IS the tool catalog, and
  this is the registry-derived source for it. Deliberately no MCP wiring
  here (#1462 owns that surface).
- The "what can you do?" answer path already derives from the same ledger
  (``chat_pointers.capability_answer_lines``, #1428) — untouched; this module
  adds the effect/consent dimension without forking that surface.

DENOMINATOR (m-44): the catalog covers exactly the ACTION-TRIGGERED workflow
registry entries — the surfaces with a DECLARED effect. Legacy
``_handle_execution_intent`` chain actions (e.g. the todo family) have no
declared effect and are EXCLUDED, stated per entry of omission by
``catalog_coverage()`` — an all-clear that silently skipped them would be the
freeze-watchdog mistake. Their consent + legibility ride their rail
migration (#1605/#1569 lane).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

from services.shared_types import EffectClass, Outwardness

if TYPE_CHECKING:
    from services.intent_service.workflow_dispatcher import WorkflowEntry

# Per-EFFECT phrases (3 tiers, keyed by the enum — a tier vocabulary, not a
# per-capability hand list; a new tier value fails loudly in describe_effect).
# ⚠️ COPY SEAM: CXO owns voice; adjust here, one place.
_EFFECT_PHRASES: Dict[EffectClass, str] = {
    EffectClass.READ: "only reads — it changes nothing outside our conversation",
    EffectClass.WRITE: "saves a change outside our conversation (you can change it back)",
    EffectClass.DESTRUCTIVE: "changes or removes existing work",
}

# Per-OUTWARDNESS marker (#1632, same tier-vocabulary shape). Only OUTWARD
# carries copy: private is the unmarked default, stated once in
# OUTWARDNESS_CONVENTION rather than repeated as noise on every private
# entry. Explicit None row keeps the defaultless property — a new
# Outwardness value fails loudly in describe_outwardness until it gets a
# row here in the same commit.
# ⚠️ COPY SEAM: CXO owns voice; adjust here, one place.
_OUTWARDNESS_PHRASES: Dict[Outwardness, Optional[str]] = {
    Outwardness.PRIVATE: None,  # unmarked BY CONVENTION — see OUTWARDNESS_CONVENTION
    Outwardness.OUTWARD: (
        "posts where your team can see it — visible to others the moment it happens"
    ),
}

# The one-time legend for the absence-means-private convention: consumers
# rendering the catalog state this ONCE (preamble/legend position), never
# per entry. ⚠️ COPY SEAM: CXO owns voice; adjust here, one place.
OUTWARDNESS_CONVENTION = (
    "Unless an action says otherwise, what I do stays between us — "
    "only the marked ones land in front of other people."
)


def describe_effect(effect: EffectClass) -> str:
    """User-register phrase for what an effect tier does in the world.
    Raises KeyError on an unknown tier — a new EffectClass value must get a
    phrase in the same commit (defaultless on purpose, the #1557 property)."""
    return _EFFECT_PHRASES[effect]


def describe_outwardness(outwardness: Outwardness) -> Optional[str]:
    """User-register marker for who else witnesses the action (#1632), or
    None for the unmarked private default (the convention
    OUTWARDNESS_CONVENTION states once). Raises KeyError on an unknown tier —
    a new Outwardness value must get an explicit row in the same commit
    (defaultless on purpose, the #1557 property)."""
    return _OUTWARDNESS_PHRASES[outwardness]


def consent_behavior_line(effect: EffectClass) -> str:
    """What the consent boundary does for this effect tier, DERIVED by asking
    the one decision function about the default cell (ambiguous framing,
    default collaborate mode) — the copy can never drift from the gate,
    because it is computed from the gate."""
    from services.intent_service.collaboration_gate import (
        FRAMING_AMBIGUOUS,
        WorkingMode,
    )
    from services.intent_service.consent_gate import ConsentDecision, decide_consent

    decision = decide_consent(effect, FRAMING_AMBIGUOUS, WorkingMode.COLLABORATE)
    if decision is ConsentDecision.CONFIRM:
        return "I always ask for an explicit yes before doing this"
    if decision is ConsentDecision.COLLABORATE:
        return "I check with you first unless you ask me outright"
    return "I do this right away"


@dataclass(frozen=True)
class CapabilityDescription:
    """One rail capability, described for humans — every field derived."""

    action: str  # canonical rail key (internal name; not user copy)
    effect: EffectClass
    effect_phrase: str  # describe_effect(effect)
    consent_line: str  # consent_behavior_line(effect)
    outwardness: Outwardness  # who else witnesses it (#1509 axis, from the entry)
    outward_phrase: Optional[str]  # describe_outwardness(outwardness); None = private
    example_ask: Optional[str]  # a POINTER utterance that routes here, if one exists


def _pointer_examples() -> Dict[str, str]:
    """action -> first ledger POINTER utterance expecting that action.
    Routability is inherited from the #1433 ratchet (every POINTER utterance
    is resolution-asserted on every build) — this module never invents an
    utterance (#1571)."""
    from services.intent_service.chat_pointers import CHAT_POINTERS, POINTER

    examples: Dict[str, str] = {}
    for row in CHAT_POINTERS.values():
        if isinstance(row, POINTER):
            _category, action = row.expects
            examples.setdefault(action, row.utterance)
    return examples


def _unique_rail_entries() -> List[Tuple[str, "WorkflowEntry"]]:
    """(canonical_key, entry) per unique action-triggered registry entry —
    the same first-registered-key dedup wired_chat_actions uses (#1517)."""
    from services.intent_service.workflow_dispatcher import WORKFLOW_REGISTRY
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()  # idempotent
    unique: List[Tuple[str, "WorkflowEntry"]] = []
    seen: set = set()
    for key, entry in WORKFLOW_REGISTRY.items():
        if not entry.action_triggered:
            continue
        if id(entry) in seen:
            continue
        seen.add(id(entry))
        unique.append((key, entry))
    return unique


def capability_catalog() -> List[CapabilityDescription]:
    """The registry-derived capability catalog — the #1462 tool-description
    seam and the legibility source of record. One entry per unique
    action-triggered rail entry; every field computed (see module docstring
    for the chain)."""
    examples = _pointer_examples()
    return [
        CapabilityDescription(
            action=key,
            effect=entry.effect,
            effect_phrase=describe_effect(entry.effect),
            consent_line=consent_behavior_line(entry.effect),
            outwardness=entry.outwardness,
            outward_phrase=describe_outwardness(entry.outwardness),
            example_ask=examples.get(key),
        )
        for key, entry in _unique_rail_entries()
    ]


def capability_answer_lines_with_outwardness() -> List[str]:
    """The #1428 'what can you do?' (DISCOVERY/IDENTITY) answer lines —
    ``chat_pointers.capability_answer_lines``'s own construction, UNTOUCHED
    (same ``CORE_CAPABILITIES``, same ``pointer_utterances()`` ledger order)
    — each POINTER-derived line suffixed with the #1632 outward marker when
    that POINTER's action carries a registry-declared ``OUTWARD``.

    Closes the #1632 live FAIL (PM, v70, 2026-09-09): :func:`capability_catalog`
    gained the outwardness axis, but the "what can you do?" answer is a
    SEPARATE #1428 derivation this module's own docstring says stays
    "untouched" — so the marker never reached that prompt at all (a plumbing
    gap, not a paraphrase). This bridges the two WITHOUT forking #1428's
    construction: identical ordering, only a per-line marker suffix, sourced
    from the SAME ``WORKFLOW_REGISTRY`` #1509/#1632 declare against. A
    POINTER action absent from the registry (a non-rail/legacy surface)
    renders unmarked — private-by-convention default, never an error.
    """
    from services.intent_service.chat_pointers import (
        CHAT_POINTERS,
        CORE_CAPABILITIES,
        POINTER,
        answer_utterances,
    )
    from services.intent_service.workflow_dispatcher import WORKFLOW_REGISTRY
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()  # idempotent

    # utterance -> action, first-registered row wins (mirrors the ledger's
    # own first-match dedup semantics in chat_pointers.pointer_utterances()).
    action_by_utterance: Dict[str, str] = {}
    for row in CHAT_POINTERS.values():
        if isinstance(row, POINTER) and row.utterance not in action_by_utterance:
            _category, action = row.expects
            action_by_utterance[row.utterance] = action

    lines: List[str] = list(CORE_CAPABILITIES)
    # #2245: the same offered-connector filter as capability_answer_lines, so
    # the decorated answer stays a pure suffix over the #1428 answer.
    for utterance in answer_utterances():
        line = f'you can ask me: "{utterance}"'
        entry = WORKFLOW_REGISTRY.get(action_by_utterance.get(utterance, ""))
        outwardness = getattr(entry, "outwardness", None)
        phrase = describe_outwardness(outwardness) if outwardness is not None else None
        if phrase:
            line = f"{line} — {phrase}"
        lines.append(line)
    return lines


def catalog_coverage() -> Dict[str, int]:
    """The honest denominator for any claim built on the catalog (m-44):
    how many wired chat actions the catalog describes vs. how many exist.
    ``uncovered`` counts legacy-chain actions with no declared effect —
    they are OUTSIDE this catalog's boundary, not clear."""
    from services.intent_service.workflow_dispatcher import wired_chat_actions

    covered = {d.action for d in capability_catalog()}
    wired = set(wired_chat_actions())
    return {
        "covered": len(covered & wired),
        "wired_total": len(wired),
        "uncovered": len(wired - covered),
    }


# ── #2100 (Arch's ruling on the issue, 2026-10-19 15:28 PT): what chat can READ from each
# connector is declared here by code, beside the readers that do it, and rendered on
# the floor's integration lines. Without this the model filled the gap itself
# ("Connect my Notion … would solve it") for a connector chat cannot read at all
# (ADR-080: a claim about Piper's own capability belongs to code). It changes
# WITH the reader: a new reader fills its entry in the same commit; a declaration
# that lags its reader is the same false claim.


@dataclass(frozen=True)
class ChatRead:
    """One thing chat reads from a connector, and the code symbol that reads it
    (``module:Qual.name``), so a pin can prove the reader exists."""

    what: str
    reader: str


#: The integration display set (one place; the floor imports it).
INTEGRATION_DISPLAY: Dict[str, str] = {
    "github": "GitHub",
    "slack": "Slack",
    "calendar": "Google Calendar",
    "notion": "Notion",
}

#: Per connector, what chat reads today. EMPTY means: connects, chat reads nothing.
CHAT_READS: Dict[str, Tuple[ChatRead, ...]] = {
    "github": (
        ChatRead(
            "open issues and their status",
            "services.mcp.consumer.github_adapter:GitHubMCPSpatialAdapter.list_open_issues",
        ),
        ChatRead(
            "one issue by number",
            "services.mcp.consumer.github_adapter:GitHubMCPSpatialAdapter.get_issue_connector",
        ),
    ),
    "slack": (
        ChatRead(
            "recent conversation history",
            "services.intent_service.context_assembler:ContextAssembler._fetch_slack_activity_items",
        ),
        ChatRead(
            "messages that mention you",
            "services.intent_service.context_assembler:ContextAssembler._fetch_slack_mentions_items",
        ),
    ),
    "calendar": (
        ChatRead(
            "your agenda for today and tomorrow",
            "services.intent_service.canonical_handlers:CanonicalHandlers._handle_agenda_query",
        ),
        ChatRead(
            "your meetings this week",
            "services.intent.intent_service:IntentService._handle_week_calendar_query",
        ),
    ),
    # Notion connects and tests; no chat path reads its pages (Lead's source read,
    # 2026-10-19). Fill this in the commit that lands a reader.
    "notion": (),
}

#: CXO's words for a connector chat cannot read (#2100).
CANNOT_READ_LINE: Dict[str, str] = {
    "notion": "connects, but chat can't read your Notion pages yet",
}


#: #2112 (CXO's words, Arch's ruling): a connector whose reads have a stated
#: limit renders CXO's sentence instead of the generic "chat reads …" list, so
#: the floor never implies a read it does not have (conflicts, other people's
#: availability). The claim is confirmed against the rail: meeting_time (one
#: day) and week_calendar (the week, free time included).
READS_WITH_LIMITS_LINE: Dict[str, str] = {
    "calendar": (
        "I can read your calendar for today, tomorrow or this week, including your "
        "free time. I can't check for conflicts or find a time that works for other "
        "people yet."
    ),
}

#: #2112 (CXO's words): what the floor says when this connector is not connected.
NOT_CONNECTED_LINE: Dict[str, str] = {
    "calendar": (
        "Your calendar isn't connected, so I can't look at it. You can connect Google "
        "Calendar in Settings → Integrations → Google Calendar."
    ),
}


def chat_reads_line(key: str) -> str:
    """The rendered reads for one connector key: what chat reads, or the can't-read
    sentence when the declaration is empty, or CXO's limits sentence (#2112)."""
    reads = CHAT_READS.get(key, ())
    if not reads:
        return CANNOT_READ_LINE.get(key, "connects, but chat can't read its content yet")
    if key in READS_WITH_LIMITS_LINE:
        return READS_WITH_LIMITS_LINE[key]
    return "chat reads " + ", ".join(r.what for r in reads)


def not_connected_line(key: str) -> Optional[str]:
    """CXO's sentence for a connector that is not connected (#2112), or None."""
    return NOT_CONNECTED_LINE.get(key)


def reader_symbol_resolves(symbol: str) -> bool:
    """True when ``module:Qual.name`` imports and resolves (the pin's check)."""
    import importlib

    module_name, _, dotted = symbol.partition(":")
    try:
        obj = importlib.import_module(module_name)
        for part in dotted.split("."):
            obj = getattr(obj, part)
    except (ImportError, AttributeError):
        return False
    return True
