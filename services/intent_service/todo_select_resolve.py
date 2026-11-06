"""#2219 / #2295 — which slice of the todo list a list ask wants, resolved op-locally.

Arch's ruling 2026-11-06 07:31 (option (b), after the next_todo_query split screened
NO-GO at 07:2x): the router keeps picking ``list_todos_query``; the sub-choice inside
it, whether the person asked for the whole list, only the next todo, or only the
completed ones, is resolved HERE by one small LLM call, in #2197's shape
(``milestone_resolve``). The call starts only on the router's pick, never on words.

The model's reply is one of three selectors and nothing else; code does the rest:
"next" is the first open row of the list code read, in the list's own order (priority,
due date, oldest first); "completed" is the done rows code read. Nothing the model
writes is ever rendered.

No regex and no phrase matching (ADR-080; the #1595 extraction-pattern ratchet): the
only text operations are strip and a fenced-block peel.

Every failure (a key refusal, a provider error, a timeout, unparseable or out-of-shape
JSON) is outcome ``failed``, and the caller renders today's list. One structured log
line per call (``todo_selector_call``) carries the provider's own token counts from
``served["usage"]`` (never estimated) and the latency.
"""

from __future__ import annotations

import asyncio
import json
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import structlog

from services.llm.request_key import LLMKeyRequiredError

logger = structlog.get_logger()

TASK_TYPE = "todo_selection"

SELECTOR_NEXT = "next"
SELECTOR_COMPLETED = "completed"

OUTCOME_NEXT = "next"
OUTCOME_COMPLETED = "completed"
OUTCOME_LIST = "list"
OUTCOME_FAILED = "failed"
OUTCOME_SKIPPED = "skipped"

TODO_SELECTOR_SYSTEM_PROMPT = (
    "You decide what part of their todo list a user's message asks to see. "
    "Reply with STRICT JSON only, no prose, exactly one of these objects:\n"
    '{"selector": "next"} when the message asks for the single next or first todo '
    "(one item, not the list);\n"
    '{"selector": "completed"} when the message asks only for todos that are already '
    "done or completed;\n"
    '{"selector": null} otherwise (the list of todos, including a list that also shows '
    "done ones)."
)


@dataclass
class TodoSelection:
    """The resolver's verdict: ``next``, ``completed`` or ``list`` (or failed/skipped)."""

    outcome: str
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    latency_ms: Optional[int] = None


def _json_object(text: str) -> Dict[str, Any]:
    """The reply's one JSON object: bare, or inside a fenced block. Raises
    ``json.JSONDecodeError`` / ``ValueError`` on anything else."""
    body = (text or "").strip()
    if body.startswith("```"):
        kept = [ln for ln in body.split("\n") if not ln.strip().startswith("```")]
        body = "\n".join(kept).strip()
    parsed = json.loads(body)
    if not isinstance(parsed, dict):
        raise ValueError(f"selector reply is not an object: {type(parsed).__name__}")
    return parsed


def parse_selection(reply: str) -> TodoSelection:
    """Strict parse. A ``selector`` key is required; its value must be "next",
    "completed" or null. Anything else raises (the caller turns it into ``failed``)."""
    obj = _json_object(reply)
    if "selector" not in obj:
        raise ValueError("selector reply has no selector key")
    value = obj["selector"]
    if value is None:
        return TodoSelection(outcome=OUTCOME_LIST)
    if value == SELECTOR_NEXT:
        return TodoSelection(outcome=OUTCOME_NEXT)
    if value == SELECTOR_COMPLETED:
        return TodoSelection(outcome=OUTCOME_COMPLETED)
    raise ValueError(f"selector value out of shape: {value!r}")


def _usage(served: Dict[str, Any]) -> Dict[str, Optional[int]]:
    usage = served.get("usage")
    if not isinstance(usage, dict):
        return {"input_tokens": None, "output_tokens": None}
    out: Dict[str, Optional[int]] = {}
    for key in ("input_tokens", "output_tokens"):
        value = usage.get(key)
        out[key] = value if isinstance(value, int) and not isinstance(value, bool) else None
    return out


async def resolve_todo_selection(
    message: str, *, llm_service: Any, user_id: Optional[str]
) -> TodoSelection:
    """One call: does the message want the list, the next todo, or the completed ones."""
    if not (message or "").strip():
        return TodoSelection(outcome=OUTCOME_SKIPPED)
    served: Dict[str, Any] = {}
    started = time.monotonic()
    try:
        reply = await llm_service.complete(
            task_type=TASK_TYPE,
            prompt=f"User message: {message.strip()}",
            system=TODO_SELECTOR_SYSTEM_PROMPT,
            user_id=user_id,
            served=served,
        )
        selection = parse_selection(reply)
    except (
        LLMKeyRequiredError,
        json.JSONDecodeError,
        ValueError,
        TypeError,
        asyncio.TimeoutError,
        RuntimeError,  # AllProvidersFailed and "no providers configured" are RuntimeErrors
    ) as e:
        logger.warning("todo_selector_failed", error_class=type(e).__name__)
        selection = TodoSelection(outcome=OUTCOME_FAILED)
    selection.latency_ms = int((time.monotonic() - started) * 1000)
    usage = _usage(served)
    selection.input_tokens = usage["input_tokens"]
    selection.output_tokens = usage["output_tokens"]
    logger.info(
        "todo_selector_call",
        outcome=selection.outcome,
        latency_ms=selection.latency_ms,
        input_tokens=selection.input_tokens,
        output_tokens=selection.output_tokens,
    )
    return selection


__all__ = (
    "TASK_TYPE",
    "TODO_SELECTOR_SYSTEM_PROMPT",
    "TodoSelection",
    "parse_selection",
    "resolve_todo_selection",
)
