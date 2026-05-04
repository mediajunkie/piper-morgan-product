"""
Anti-surveillance phrasing guardrail (#1033 MUX-COMPOSTED-EXPERIENCE).

Per `docs/internal/design/mux/composting-experience-design.md` (D3) §"Anti-Patterns":

> Composting is reflection, not surveillance. When Piper transforms old objects
> into learnings, users should experience this as thoughtful reflection — like
> a colleague who's "had time to think about things" — not as evidence of
> continuous monitoring.

This module catches surveillance-shaped phrasing in COMPOSTED-derived output
before it reaches the user. Per Q3 disposition (May 3) the guardrail is
**strict**: regex match → reject → caller falls back to a gentle
"I don't have anything to share right now" message; violations are logged.

Used by:
- `services.mux.premonition.frame_insight_for_surfacing` (surface-time framing)
- `services.mux.composting_scheduler.frame_learning` (compost-time framing)

The two-layer integration ensures both compost-time stored expressions AND
surface-time generated text are checked.

Mapping from D3 anti-patterns to patterns documented at
`dev/2026/05/03/1033-d3-alignment.md`.
"""

from __future__ import annotations

import logging
import re
from typing import List, Optional

logger = logging.getLogger(__name__)


# Forbidden surveillance-phrasing patterns. Each is a tuple
# (compiled-pattern, label-for-logging). Patterns are case-insensitive
# and word-boundary-anchored to avoid false positives on substrings.
#
# Per D3 spec (§"Anti-Patterns" + §"Language Patterns"). Mappings
# documented in the alignment doc cited above.
# `I(?:'ve| have) been` covers both contraction "I've been" and full form
# "I have been". Patterns are case-insensitive.
_FORBIDDEN_PATTERNS: List[tuple[re.Pattern, str]] = [
    (re.compile(r"\bI(?:'ve| have) been watching\b", re.IGNORECASE), "i've-been-watching"),
    (re.compile(r"\bwhile you were away\b", re.IGNORECASE), "while-you-were-away"),
    (re.compile(r"\bbased on my surveillance\b", re.IGNORECASE), "based-on-my-surveillance"),
    (re.compile(r"\bI(?:'ve| have) been monitoring\b", re.IGNORECASE), "i've-been-monitoring"),
    (re.compile(r"\bmonitoring your activit\w*\b", re.IGNORECASE), "monitoring-your-activity"),
    (re.compile(r"\bI(?:'ve| have) been tracking\b", re.IGNORECASE), "i've-been-tracking"),
    (re.compile(r"\bI detected (?:a |the )?pattern\b", re.IGNORECASE), "i-detected-pattern"),
    (re.compile(r"\bbased on your behavior at\b", re.IGNORECASE), "based-on-your-behavior-at"),
    (re.compile(r"\bafter analyzing your data\b", re.IGNORECASE), "after-analyzing-your-data"),
    (re.compile(r"\bmy analysis shows\b", re.IGNORECASE), "my-analysis-shows"),
    (re.compile(r"\bI(?:'ve| have) been observing\b", re.IGNORECASE), "i've-been-observing"),
]


# User-facing fallback when the guardrail rejects output.
SURVEILLANCE_FALLBACK_MESSAGE = "I don't have anything to share right now."


class SurveillancePhrasingViolation(ValueError):
    """Raised when text contains forbidden surveillance phrasing.

    Carries the matched phrase labels so callers / tests can introspect.
    """

    def __init__(self, message: str, matched_labels: List[str]):
        super().__init__(message)
        self.matched_labels = matched_labels


def detect_surveillance_phrasing(text: str) -> List[str]:
    """Return list of matched pattern labels; empty list = clean.

    Soft check: doesn't raise. Used for testing + telemetry.
    """
    if not text:
        return []
    return [label for pattern, label in _FORBIDDEN_PATTERNS if pattern.search(text)]


def assert_no_surveillance_phrasing(text: str) -> None:
    """Strict check: raises SurveillancePhrasingViolation if any pattern matches.

    Logs the violation with structured fields so operators can see the
    guardrail firing in production.

    Per Q3 (May 3): strict; production callers wrap with try/except and
    fall back to SURVEILLANCE_FALLBACK_MESSAGE on violation.
    """
    matched = detect_surveillance_phrasing(text)
    if matched:
        # Truncate text in log to avoid leaking long content; keep first 120 chars
        preview = (text[:120] + "...") if len(text) > 120 else text
        logger.warning(
            "anti_surveillance_violation",
            extra={
                "matched_labels": matched,
                "text_preview": preview,
            },
        )
        raise SurveillancePhrasingViolation(
            f"Surveillance-shaped phrasing detected: {matched}",
            matched_labels=matched,
        )


def safe_surface(text: Optional[str]) -> str:
    """Convenience wrapper for callers that want fallback semantics inline.

    Returns the input text if clean; returns the fallback message if a
    surveillance pattern matched. None or empty input also returns the
    fallback (defensive).

    Use this when you want strict-with-fallback in one call:

        framed = frame_insight_for_surfacing(insight)
        return safe_surface(framed)
    """
    if not text:
        return SURVEILLANCE_FALLBACK_MESSAGE
    try:
        assert_no_surveillance_phrasing(text)
        return text
    except SurveillancePhrasingViolation:
        return SURVEILLANCE_FALLBACK_MESSAGE
