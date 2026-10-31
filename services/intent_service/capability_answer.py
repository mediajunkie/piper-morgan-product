"""#2236: the capability answer is rendered in code, not composed by the model.

ADR-080: the model decides meaning, code decides what's true. On the
IDENTITY/DISCOVERY floor path (``DISCOVERY/get_capabilities`` included) the
capability claims are the #1428 ledger lines, verbatim and in order
(``capability_answer_lines_with_outwardness()``, which the #1433 ratchet
verifies row by row), and the connection state is the canonical status read
(#1547, ``context["integrations"]``). Both are rendered here. The floor model
contributes at most one opening line tied to the user's own data (#950), and
:func:`sanitize_opener` drops it if it makes a claim about what Piper can or will
do (CXO's three conditions, 2026-10-30).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

#: CXO's exact line (#2151 rule): a failed or untrustworthy status read states no
#: connection facts at all, and is never rendered as "not connected".
COULDNT_CHECK_LINE = "I couldn't check which tools you've connected just now."

#: The model is told this on a capability turn; a reply of exactly this token (or
#: nothing) means "no opener". A bare rendered list is a valid reply.
NO_OPENER_TOKEN = "NONE"

CAPABILITY_TURN_INSTRUCTION = (
    "[Capability turn: the list of what you can do and the state of the user's "
    "connected tools are rendered by the system below your reply, from verified "
    "records. Do NOT write any sentence about what you can do, will do, learn, "
    "remember, remind or proactively surface, and do NOT mention which tools are "
    "or aren't connected. Write at most ONE short opening line tied to this "
    "user's own projects or recent conversation, with no claim about your abilities "
    "and no commentary about being honest or about timing. If nothing in the user's "
    f"own data fits, reply with exactly {NO_OPENER_TOKEN}.]"
)

# This is a keyword check on the MODEL's output (the opener), never on user text:
# not an extraction pattern. The rendered block is the content; the opener is
# optional, so a false drop costs nothing and a false keep ships an unverified claim.
_OPENER_FORBIDDEN = (
    "learn",
    "remember",
    "remind",
    "proactiv",
    "honest",
    "good timing",
    "great question",
    "happy to",
    "i can",
    "i could",
    "i'll",
    "i will",
    "i'm able",
    "i am able",
    "i'd",
    "i would",
    "i'm going to",
    "i am going to",
    "we can",
    "surface",
    "keep track",
    "track",
    "notice",
    "anticipat",
    "nudge",
    "follow up",
    "follow-up",
    "ahead of",
)


def sanitize_opener(text: Optional[str]) -> Optional[str]:
    """The model's optional opening line, or None when it must be dropped.

    Dropped (never repaired) when: empty or the NONE token; more than one line;
    too long to be one line; or it contains a capability, learning, remembering,
    reminding, proactivity or honesty-announcing word.
    """
    if not text:
        return None
    opener = text.strip()
    if not opener or opener.upper().rstrip(".") == NO_OPENER_TOKEN:
        return None
    if "\n" in opener or len(opener) > 280:
        return None
    lowered = opener.lower().replace("\u2019", "'")
    if any(word in lowered for word in _OPENER_FORBIDDEN):
        return None
    return opener


def render_connection_lines(domain_context: Dict[str, Any]) -> List[str]:
    """Connection state from the canonical status service read, as code-rendered lines.

    A failed or missing read yields only CXO's couldn't-check line: no connection
    facts, never "not connected" as a default.
    """
    from services.integrations.integration_status_service import BETA_OFFERED_CONNECTORS
    from services.intent_service.capability_legibility import (
        INTEGRATION_DISPLAY,
        chat_reads_line,
    )

    integrations = domain_context.get("integrations")
    if (
        domain_context.get("integrations_source_failed")
        or not isinstance(integrations, list)
        or not integrations
    ):
        return [COULDNT_CHECK_LINE]

    def _disp(name: object) -> str:
        return INTEGRATION_DISPLAY.get(str(name), str(name).title())

    def _keys(status: str) -> List[str]:
        return [
            str(i.get("name"))
            for i in integrations
            if isinstance(i, dict) and i.get("name") and i.get("status") == status
        ]

    connected = _keys("active")
    reconnect = [_disp(k) for k in _keys("needs_reconnecting")]
    absent = [BETA_OFFERED_CONNECTORS[k] for k in BETA_OFFERED_CONNECTORS if k in _keys("inactive")]

    lines: List[str] = []
    if connected:
        lines.append("Connected, and what I read from each:")
        lines.extend(f"- {_disp(key)}: {chat_reads_line(key)}" for key in connected)
    else:
        lines.append(
            "None of your tools are connected yet, so I'm not reading from any of them. "
            "You can connect GitHub or Google Calendar in Settings → Integrations."
        )
    if reconnect:
        lines.append(
            "Needs reconnecting (reconnect in Settings → Integrations): " + ", ".join(reconnect)
        )
    if absent and connected:
        lines.append(
            "Not connected, so I'm not using them (connect in Settings → Integrations): "
            + ", ".join(absent)
        )
    return lines


def render_capability_block(domain_context: Dict[str, Any]) -> str:
    """The code-rendered capability answer: ledger lines verbatim, then connection state."""
    from services.intent_service.capability_legibility import (
        OUTWARDNESS_CONVENTION,
        describe_outwardness,
    )
    from services.shared_types import Outwardness

    caps = [str(c) for c in (domain_context.get("capabilities") or [])]
    parts: List[str] = []
    if caps:
        parts.append("What I can do today:\n" + "\n".join(f"- {c}" for c in caps))
        marker = describe_outwardness(Outwardness.OUTWARD)
        if marker and any(marker in c for c in caps):
            parts.append(OUTWARDNESS_CONVENTION)
    parts.append("\n".join(render_connection_lines(domain_context)))
    return "\n\n".join(parts)


#: The routed op whose answer is the capability list (Arch: "on the capability answer").
#: An IDENTITY turn (get_identity) keeps the floor's own answer, unchanged.
CAPABILITY_OPS = frozenset({"get_capabilities"})


def is_capability_turn(
    intent_action: Optional[str], domain_context: Optional[Dict[str, Any]]
) -> bool:
    """True when the router's verdict is a capability op AND the identity gatherer
    put the ledger lines on this floor turn. Keyed on the routed op, not on the
    context key alone."""
    caps = (domain_context or {}).get("capabilities")
    return intent_action in CAPABILITY_OPS and isinstance(caps, list) and bool(caps)


def compose_capability_reply(opener_raw: Optional[str], domain_context: Dict[str, Any]) -> str:
    """The opener (if it survives the guard) above the rendered block."""
    block = render_capability_block(domain_context)
    opener = sanitize_opener(opener_raw)
    return f"{opener}\n\n{block}" if opener else block
