"""#2188 — a typed "not performed" marker on a chat result (Arch's rulings 2026-11-04 13:43 and 14:06).

``IntentProcessingResult.success`` says whether the requested operation was performed,
not whether Piper answered honestly. A GitHub degrade (unreachable, needs re-authorizing,
grant unreadable) and a not-found refusal ("I couldn't find issue #N, so nothing was
changed") are ``success=False`` with the text unchanged. Two readers of the flag then
need a way to tell such a turn from a real handler failure without matching text:

- conversation history saves any turn with a message, whatever its ``success`` (what the
  person was shown belongs in history; #563 excluded EMPTY results, and the message test
  still does);
- the learning handler (#300) skips ``record_outcome`` when the result carries this marker,
  because a degrade says nothing about whether the route was right; an unmarked
  ``success=False`` still records False.

The marker is one key in ``intent_data`` holding one of the kinds below. Set it with
``mark_not_performed``; read it with ``was_not_performed``. Never match on reply text.
The trust layer's ``task_completed`` reads ``success`` directly; this marker is its hook
if the trust owners want to exclude outages later (noted on #2188).
"""

from __future__ import annotations

from typing import Any, Dict, Optional

NOT_PERFORMED_KEY = "not_performed"


class NotPerformed:
    """The kinds. One constant set; a reader compares against these, never against text."""

    DEGRADED = "degraded"  # the read or write did not run: GitHub degrade (#1231 family)
    REFUSED_BEFORE_WRITE = "refused_before_write"  # the handler refused before any write
    NOT_FOUND = "not_found"  # the target was not there (#1858): nothing was changed
    NOT_CONNECTED = "not_connected"  # #2280: the connector was never connected, so nothing ran


NOT_PERFORMED_KINDS = frozenset(
    {
        NotPerformed.DEGRADED,
        NotPerformed.REFUSED_BEFORE_WRITE,
        NotPerformed.NOT_FOUND,
        NotPerformed.NOT_CONNECTED,
    }
)


def mark_not_performed(intent_data: Optional[Dict[str, Any]], kind: str) -> Dict[str, Any]:
    """Return ``intent_data`` with the marker set (a new dict when none was given)."""
    if kind not in NOT_PERFORMED_KINDS:
        raise ValueError(f"not a NotPerformed kind: {kind!r}")
    data: Dict[str, Any] = dict(intent_data) if isinstance(intent_data, dict) else {}
    data[NOT_PERFORMED_KEY] = kind
    return data


def was_not_performed(result: Any) -> bool:
    """True when the result's ``intent_data`` carries a known marker kind."""
    data = getattr(result, "intent_data", None)
    if not isinstance(data, dict):
        return False
    return data.get(NOT_PERFORMED_KEY) in NOT_PERFORMED_KINDS
