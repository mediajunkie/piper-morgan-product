"""ADR-083 D5 (Arch 11-06 17:29, amended 17:52; xian GO 11-07): a second router call only
when the first one CLARIFYs with a numbered list in scope, accepting only the list's own
op with a position.

The main router call stays slot-free, so every turn it answers today is untouched by
construction. Only when it returns CLARIFY and the session snapshot carries the D3a list
fact does code make one more ``route()`` call on the same message, with the D1a slot in
the session block. Its answer is used only if it names the list family's op with a
``targets`` list whose every token is a position within the recorded list (a 1-based line
number, a range of them, "first" or "last"); anything else keeps the CLARIFY, byte for
byte. Meaning stays with the router; code decides when to ask (on the router's own output
and recorded state) and what it may accept (by op and arg shape), the #1886(b) pattern.

Screened 11-06 (``dev/2026/11/06/controls/adr-083-d5-result-2026-11-06.md``: sentinels 6/6,
1 of 624 rows moved); xian said go 11-07 (decisions.log 11-07 08:04).
"""

from __future__ import annotations

import asyncio
import dataclasses
import time
from typing import Any, Optional

import structlog

logger = structlog.get_logger(__name__)

# The list family's ops by list kind (D5: complete_todo and delete_todo serve both).
D5_FAMILY = {
    "todos": frozenset({"complete_todo", "delete_todo"}),
    "reminders": frozenset({"complete_todo", "delete_todo"}),
}
_WORD_POSITIONS = frozenset({"first", "last"})

# Arch 11-07 09:24: D5's own ceiling, not the todo selector's 2.5 s (set 11-06 for a
# selector, not a router call). #2318: complete's second call timed out at 2.5 s
# 3 of 3 on alpha while delete's took 1.1 s, so this is a MEASUREMENT setting at
# Arch's 5 s cap until five served complete times set it (highest, next half second).
D5_CONSULT_CEILING_S = 5.0


def _line_number(token: str, lines: int) -> bool:
    return token.isdigit() and 1 <= int(token) <= lines


def is_position(token: Any, lines: int) -> bool:
    """Arch 17:52: a 1-based line number, a range of them, "first" or "last", each within
    the recorded list's line count. "all" or any other token is not a position."""
    if not isinstance(token, str):
        return False
    t = token.strip().lower()
    if t in _WORD_POSITIONS:
        return True
    if _line_number(t, lines):
        return True
    low, sep, high = t.partition("-")
    return (
        bool(sep)
        and _line_number(low, lines)
        and _line_number(high, lines)
        and int(low) <= int(high)
    )


def accepts(decision: Any, kind: Optional[str], lines: Optional[int]) -> bool:
    """Whether the second call's answer may replace the CLARIFY."""
    family = D5_FAMILY.get(kind or "")
    if not family or not lines or getattr(decision, "outcome", None) != "operation":
        return False
    if getattr(decision, "operation", None) not in family:
        return False
    targets = (getattr(decision, "args", None) or {}).get("targets")
    return (
        isinstance(targets, list) and bool(targets) and all(is_position(t, lines) for t in targets)
    )


def without_list_fact(snapshot: Any) -> Any:
    """The main call's snapshot: the D1a fields dropped, so its block is main's bytes."""
    return dataclasses.replace(snapshot, last_list_kind=None, last_list_lines=None)


async def consult_on_clarify(
    message: str,
    decision: Any,
    snapshot: Any,
    *,
    route: Any,
    router_snapshot: Any,
    llm_service: Any,
    grammar: Any,
    user_id: Optional[str],
    session_id: Optional[str] = None,
) -> Any:
    """D5: the first decision, or the second call's answer when it is accepted."""
    kind = getattr(snapshot, "last_list_kind", None)
    lines = getattr(snapshot, "last_list_lines", None)
    if getattr(decision, "outcome", None) != "clarify" or not kind or not lines:
        return decision
    # The router and its snapshot type come from the caller (inversion_live, the one
    # allowed referrer of the router: TestInversionShadowNoExecutionBoundary).
    from services.intent_service.session_snapshot import serialize_for_prompt

    started = time.monotonic()
    try:
        second = await asyncio.wait_for(
            route(
                message,
                router_snapshot(state_block=serialize_for_prompt(snapshot)),
                llm_service=llm_service,
                grammar=grammar,
                user_id=user_id,
            ),
            timeout=D5_CONSULT_CEILING_S,
        )
    except Exception as e:  # silent-ok: Arch 17:52, a timeout or failure keeps the CLARIFY, logged
        logger.warning(
            "inversion_live_d5_consult",
            outcome="kept",
            reason=type(e).__name__,
            elapsed_ms=int((time.monotonic() - started) * 1000),
            session_id=session_id,
        )
        return decision
    ok = accepts(second, kind, lines)
    targets = (getattr(second, "args", None) or {}).get("targets")
    # Warning, not info: alpha keeps warning-level events only, and these turns are
    # rare (a CLARIFY right after a numbered list). #2318 needed them served.
    logger.warning(
        "inversion_live_d5_consult",
        outcome="accepted" if ok else "kept",
        operation=getattr(second, "operation", None),
        target_count=len(targets) if isinstance(targets, list) else 0,
        # #2318 (Arch 11-07 11:10): whether the second call needed the router's
        # repair retry, and what served it. No message text.
        llm_calls=getattr(second, "llm_calls", None),
        repair_attempted=getattr(second, "repair_attempted", None),
        repair_error=(getattr(second, "repair_error", None) or "")[:200] or None,
        served_provider=getattr(second, "served_provider", None),
        served_model=getattr(second, "served_model", None),
        output_tokens=(getattr(second, "usage", None) or {}).get("output_tokens"),
        # #2318: the router's own time around the provider call, beside elapsed_ms.
        llm_latency_ms=getattr(second, "llm_latency_ms", None),
        # Arch 11-07 09:24: how long the second call took, kept or accepted.
        elapsed_ms=int((time.monotonic() - started) * 1000),
        session_id=session_id,
    )
    return second if ok else decision
