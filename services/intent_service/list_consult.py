"""ADR-083 D5 (PROPOSED; Arch 11-06 17:29, amended 17:52): a second router call only
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

Built on a branch for the screen; it reaches main only after the screen passes and xian's
veto window closes (ADR-083's own text).
"""

from __future__ import annotations

import asyncio
import dataclasses
from typing import Any, Optional

import structlog

logger = structlog.get_logger(__name__)

# The list family's ops by list kind (D5: complete_todo and delete_todo serve both).
D5_FAMILY = {
    "todos": frozenset({"complete_todo", "delete_todo"}),
    "reminders": frozenset({"complete_todo", "delete_todo"}),
}
_WORD_POSITIONS = frozenset({"first", "last"})


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
    from services.intent_service.todo_handlers import SELECTOR_CEILING_S

    try:
        second = await asyncio.wait_for(
            route(
                message,
                router_snapshot(state_block=serialize_for_prompt(snapshot)),
                llm_service=llm_service,
                grammar=grammar,
                user_id=user_id,
            ),
            timeout=SELECTOR_CEILING_S,
        )
    except Exception as e:  # silent-ok: Arch 17:52, a timeout or failure keeps the CLARIFY, logged
        logger.info(
            "inversion_live_d5_consult",
            outcome="kept",
            reason=type(e).__name__,
            session_id=session_id,
        )
        return decision
    ok = accepts(second, kind, lines)
    targets = (getattr(second, "args", None) or {}).get("targets")
    logger.info(
        "inversion_live_d5_consult",
        outcome="accepted" if ok else "kept",
        operation=getattr(second, "operation", None),
        target_count=len(targets) if isinstance(targets, list) else 0,
        session_id=session_id,
    )
    return second if ok else decision
