"""#2197 — which READ milestone a progress ask names, resolved op-locally.

Arch's rulings 2026-11-01 (10:48 (2), 11:01, 11:14): the router picks the op
(``get_project_status`` / ``list_milestones``); the sub-choice inside it —
which milestone the message names — is resolved HERE, in the handler, after
the read, by one small LLM call. The model decides which milestone; code binds
only to what it read (#2184 D2): the reply is a list of indices into the
candidates code just read, and code keeps only those inside ``range(len(...))``
(Arch 11:28: one → picked, two or more → tie, none → none / named_absent).
Nothing the model writes is ever rendered (``milestone_render`` renders the
read dict).

"next" stays code's (Arch 11:01): on ``{"selector": "next"}`` this returns
outcome ``next`` with NO index, even when the model also sent one; the caller
picks the earliest ``due_on`` among the OPEN candidates it read
(``pick_next_index``), and an undated or tied earliest is a tie → default.

No regex and no phrase matching (ADR-080; the #1595 extraction-pattern
ratchet): the only text operations are strip and a fenced-block peel.

Every failure (a key refusal, a provider error, a timeout, unparseable or
out-of-shape JSON) is outcome ``failed`` and the caller renders its default.
One structured log line per call (``milestone_resolver_call``) carries the
provider's own token counts from ``served["usage"]`` (never estimated): PPM's
cost measure.
"""

from __future__ import annotations

import asyncio
import json
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import structlog

from services.llm.request_key import LLMKeyRequiredError
from services.utils.text_sanitation import display_title

logger = structlog.get_logger()

TASK_TYPE = "milestone_resolution"

OUTCOME_PICKED = "picked"
OUTCOME_NEXT = "next"
OUTCOME_NONE = "none"
OUTCOME_NAMED_ABSENT = "named_absent"
OUTCOME_TIE = "tie"
OUTCOME_FAILED = "failed"
OUTCOME_SKIPPED = "skipped"

MILESTONE_RESOLVER_SYSTEM_PROMPT = (
    "You decide which milestone, if any, a user's message is asking about. "
    "You are given the user's message and the numbered list of milestones that were "
    "read from their GitHub repository. Reply with STRICT JSON only, no prose, exactly "
    "one of these objects:\n"
    '{"indices": [<int>, ...]} with the index of every listed milestone the message '
    "could be naming (one index when it names exactly one; two or more when more than "
    "one listed milestone could be meant);\n"
    '{"selector": "next"} when the message asks for the next or upcoming milestone '
    "WITHOUT naming one;\n"
    '{"index": null, "named_absent": true} when the message names a milestone that is '
    "not in the list;\n"
    '{"index": null} otherwise (an ask about the project as a whole, or no milestone meant).\n'
    "Never invent a milestone. Use only the indexes shown."
)


@dataclass
class MilestoneResolution:
    """The resolver's verdict. ``index`` is set only on ``picked``;
    ``selector`` only on ``next`` (and then ``index`` is always None)."""

    outcome: str
    index: Optional[int] = None
    selector: Optional[str] = None
    named_absent: bool = False
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    latency_ms: Optional[int] = None


def _due_part(due_on: Any) -> str:
    if isinstance(due_on, str) and due_on.strip():
        return due_on.strip().split("T")[0]
    return "none"


def _int_or_zero(value: Any) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) else 0


def build_resolver_prompt(message: str, candidates: List[Dict[str, Any]]) -> str:
    """The user's message plus the candidates exactly as code read them."""
    lines = [
        "Milestones read from the repository (index | title | state | due | open | closed):"
    ]
    for i, m in enumerate(candidates):
        title = display_title(m.get("title"), "(untitled milestone)")
        lines.append(
            f"{i} | {title} | {m.get('state') or 'open'} | {_due_part(m.get('due_on'))} | "
            f"{_int_or_zero(m.get('open_issues'))} | {_int_or_zero(m.get('closed_issues'))}"
        )
    lines.append("")
    lines.append(f"User message: {message.strip()}")
    return "\n".join(lines)


def _json_object(text: str) -> Dict[str, Any]:
    """The reply's one JSON object: bare, or inside a fenced block. Raises
    ``json.JSONDecodeError`` / ``ValueError`` on anything else."""
    body = (text or "").strip()
    if body.startswith("```"):
        kept = [ln for ln in body.split("\n") if not ln.strip().startswith("```")]
        body = "\n".join(kept).strip()
    parsed = json.loads(body)
    if not isinstance(parsed, dict):
        raise ValueError(f"resolver reply is not an object: {type(parsed).__name__}")
    return parsed


def parse_resolution(reply: str, candidate_count: int) -> MilestoneResolution:
    """Strict parse (Arch 2026-11-01 11:28). Raises on an unparseable reply or a
    non-list ``indices`` (the caller turns that into ``failed``).

    Code keeps only the indices inside ``range(candidate_count)`` (#2184 D2:
    bind only to the read): exactly one → ``picked``; two or more → ``tie``
    (the tie comes ONLY from the model returning several in-range indices,
    never from code comparing titles or confidence); zero → ``none``, or
    ``named_absent`` when that flag is true. Lenient to a bare
    ``{"index": n}`` (read as ``indices: [n]``; a non-int ``n`` fails)."""
    obj = _json_object(reply)
    if obj.get("selector") == "next":
        # Arch 11:01: code picks "next"; any index the model sent is ignored.
        return MilestoneResolution(outcome=OUTCOME_NEXT, selector="next")
    if "indices" in obj:
        raw = obj["indices"]
        if not isinstance(raw, list):
            raise TypeError(f"resolver indices is not a list: {type(raw).__name__}")
    elif obj.get("index") is not None:
        if isinstance(obj["index"], bool) or not isinstance(obj["index"], int):
            raise TypeError(f"resolver index is not an int: {type(obj['index']).__name__}")
        raw = [obj["index"]]
    else:
        raw = []
    in_read: List[int] = []
    for n in raw:
        if isinstance(n, int) and not isinstance(n, bool) and n in range(candidate_count):
            if n not in in_read:
                in_read.append(n)
    if len(in_read) == 1:
        return MilestoneResolution(outcome=OUTCOME_PICKED, index=in_read[0])
    if len(in_read) > 1:
        return MilestoneResolution(outcome=OUTCOME_TIE)
    if obj.get("named_absent") is True:
        return MilestoneResolution(outcome=OUTCOME_NAMED_ABSENT, named_absent=True)
    return MilestoneResolution(outcome=OUTCOME_NONE)


def _usage(served: Dict[str, Any]) -> Dict[str, Optional[int]]:
    usage = served.get("usage")
    if not isinstance(usage, dict):
        return {"input_tokens": None, "output_tokens": None}
    out: Dict[str, Optional[int]] = {}
    for key in ("input_tokens", "output_tokens"):
        value = usage.get(key)
        out[key] = value if isinstance(value, int) and not isinstance(value, bool) else None
    return out


async def resolve_milestone(
    message: str,
    candidates: List[Dict[str, Any]],
    *,
    llm_service: Any,
    user_id: Optional[str],
) -> MilestoneResolution:
    """One call: which of ``candidates`` (read this turn) the message names."""
    if not candidates or not (message or "").strip():
        return MilestoneResolution(outcome=OUTCOME_SKIPPED)
    served: Dict[str, Any] = {}
    started = time.monotonic()
    try:
        reply = await llm_service.complete(
            task_type=TASK_TYPE,
            prompt=build_resolver_prompt(message, candidates),
            system=MILESTONE_RESOLVER_SYSTEM_PROMPT,
            user_id=user_id,
            served=served,
        )
        resolution = parse_resolution(reply, len(candidates))
    except (
        LLMKeyRequiredError,
        json.JSONDecodeError,
        ValueError,
        TypeError,
        asyncio.TimeoutError,
        RuntimeError,  # AllProvidersFailed and "no providers configured" are RuntimeErrors
    ) as e:
        logger.warning(
            "milestone_resolver_failed",
            error_class=type(e).__name__,
            candidates=len(candidates),
        )
        resolution = MilestoneResolution(outcome=OUTCOME_FAILED)
    resolution.latency_ms = int((time.monotonic() - started) * 1000)
    usage = _usage(served)
    resolution.input_tokens = usage["input_tokens"]
    resolution.output_tokens = usage["output_tokens"]
    logger.info(
        "milestone_resolver_call",
        outcome=resolution.outcome,
        candidates=len(candidates),
        latency_ms=resolution.latency_ms,
        input_tokens=resolution.input_tokens,
        output_tokens=resolution.output_tokens,
    )
    return resolution


def pick_next_index(candidates: List[Dict[str, Any]]) -> Optional[int]:
    """Code's "next" (Arch 11:01): the OPEN candidate with the earliest
    ``due_on`` date. None (a tie → default) when no open candidate is dated or
    the two earliest share a date."""
    dated = []
    for i, m in enumerate(candidates):
        if (m.get("state") or "open") != "open":
            continue
        due = m.get("due_on")
        if isinstance(due, str) and due.strip():
            dated.append((due.strip().split("T")[0], i))
    if not dated:
        return None
    dated.sort()
    if len(dated) > 1 and dated[0][0] == dated[1][0]:
        return None
    return dated[0][1]


__all__ = (
    "TASK_TYPE",
    "MilestoneResolution",
    "MILESTONE_RESOLVER_SYSTEM_PROMPT",
    "build_resolver_prompt",
    "parse_resolution",
    "resolve_milestone",
    "pick_next_index",
)
