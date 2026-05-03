"""
Pull-mode insight surfacing (#1030 MUX-INSIGHT-PULL).

User-initiated insight retrieval. When a user asks Piper about its insights
or learnings ("what have you learned about deadlines?"), Piper responds with
relevant insights organized by confidence, with always-available correction
invitation. Works at all 4 trust stages per D1.

Per `docs/internal/design/mux/insight-surfacing-rules.md` §"Pull Mode":
5 rules:
1. Response completeness — show all relevant insights (don't hide low-confidence)
2. Confidence display — always indicate confidence level
3. Correction invitation — always offer to correct/explain
4. Scope matching — match response scope to query scope
5. No deflection — never say "I don't have insights" if any exist

Per #1030 audit dispositions May 3:
- Q1 Option C hybrid: regex/keyword pre-classifier flags candidate Pull
  queries; LLM verifies + retrieves. This module provides the
  trigger-detection helpers + the response composer.
- Q2 Hybrid format: backend builds structured sectioned markdown per spec;
  thin LLM-wrapped intro/outro at consumer-of-this-module layer
- Q3 Option C context extraction: simple keyword-extraction inside this
  module; revisit if probe-set accuracy is poor
- Q4 Option A: identical response shape at all 4 trust stages for MVP
- Q5: enforce no-deflection rule (count > 0 → response contains insight text;
  empty → honest "haven't noticed anything specific yet")

#1033 framing-layer integration: insight content is already framed via
`frame_insight_for_surfacing` (which runs the anti-surveillance guardrail);
this module composes a sectioned response wrapping those framed insights.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional, Tuple


# =============================================================================
# Trigger detection (Phase 1)
# =============================================================================


# Per D4 §"Trigger Phrases" categories: direct query / topic-specific /
# explanation request / confidence check / source inquiry. Patterns are
# case-insensitive.
PULL_TRIGGER_PATTERNS: List[Tuple[re.Pattern, str]] = [
    (re.compile(r"\bwhat have you learned\b", re.IGNORECASE), "direct-learned"),
    (re.compile(r"\bwhat have you noticed\b", re.IGNORECASE), "direct-noticed"),
    (re.compile(r"\bwhat (?:do you|did you|have you) figure[d]? out\b", re.IGNORECASE), "direct-figured"),
    (re.compile(r"\bwhat (?:do|did) you (?:know|find)\b", re.IGNORECASE), "direct-know"),
    (re.compile(r"\bwhat insights\b", re.IGNORECASE), "topic-insights"),
    (re.compile(r"\bwhat (?:patterns|learnings)\b", re.IGNORECASE), "topic-patterns"),
    (re.compile(r"\bwhy did you (?:say|suggest|recommend|think)\b", re.IGNORECASE), "explanation"),
    (re.compile(r"\bhow (?:sure|confident) are you\b", re.IGNORECASE), "confidence-check"),
    (re.compile(r"\bwhere did (?:that|this) (?:insight|come from)\b", re.IGNORECASE), "source-inquiry"),
    (re.compile(r"\btell me about your (?:insights|learnings|observations)\b", re.IGNORECASE), "direct-tell"),
    (re.compile(r"\bhave you noticed (?:anything|any pattern)s?\b", re.IGNORECASE), "direct-noticed-anything"),
]


def is_pull_trigger(user_message: str) -> bool:
    """Return True if user_message matches a Pull-mode trigger pattern.

    Q1 Option C hybrid: this is the pre-classifier flag. The LLM consumer
    of this module verifies the trigger before actually retrieving from
    the journal — defense against false positives.
    """
    if not user_message:
        return False
    return any(pattern.search(user_message) for pattern, _ in PULL_TRIGGER_PATTERNS)


def matched_trigger_labels(user_message: str) -> List[str]:
    """Return list of matched trigger pattern labels (for telemetry/tests)."""
    if not user_message:
        return []
    return [
        label for pattern, label in PULL_TRIGGER_PATTERNS if pattern.search(user_message)
    ]


# Stop-words removed during keyword extraction. Conservative list; covers
# the most common low-signal tokens that would create noise in entity/topic
# matching against insights.
_STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "do", "did", "for",
    "from", "have", "has", "he", "her", "i", "in", "is", "it", "me", "my", "of",
    "on", "or", "she", "that", "the", "to", "was", "we", "what", "when", "where",
    "which", "who", "why", "with", "you", "your", "yours", "yes", "no", "not",
    "this", "these", "those", "any", "all", "some", "if", "then", "than", "so",
    "such", "now", "just", "also", "very", "more", "most", "less", "few", "many",
    "they", "them", "their", "theirs", "us", "our", "ours", "his", "hers", "him",
    "been", "being", "had", "would", "could", "should", "will", "shall", "may",
    "might", "must", "can", "ought", "there", "here", "how", "much", "let",
    "do", "doing", "does", "done", "seem", "seems", "seemed", "look", "looks",
    "looked", "tell", "told", "telling", "ask", "asked", "asking", "say", "said",
    "saying", "know", "knew", "known", "learn", "learning", "learned", "noticed",
    "noticing", "notice", "find", "finds", "found", "finding", "think", "thought",
    "thinking", "feel", "felt", "feeling", "want", "wants", "wanted", "wanting",
    "need", "needs", "needed", "needing", "go", "goes", "went", "going", "come",
    "comes", "came", "coming", "get", "gets", "got", "getting", "make", "makes",
    "made", "making", "take", "takes", "took", "taking", "give", "gives", "gave",
    "given", "giving", "use", "uses", "used", "using", "see", "sees", "saw",
    "seen", "seeing", "look", "looks", "looked", "looking",
    "insights", "insight", "learnings", "learning", "patterns", "pattern",
    "observations", "observation",
}


def extract_context(user_message: str) -> Tuple[List[str], List[str]]:
    """Q3 Option C: simple keyword extraction inside this helper.

    Returns (entity_candidates, topic_candidates) — for #1030 MVP, entities
    and topics are extracted from the same source (the user's words after
    stop-word filtering). The InsightJournal's get_for_context method scores
    relevance by overlap with insight.applies_to_entities + topic_tags +
    context_tags, so these candidate lists are matched against multiple axes.

    Future enhancement: distinguish entities (proper nouns / domain objects)
    from topics (general subject areas) via NLP. Out of scope per Q3 lean.
    """
    if not user_message:
        return [], []

    # Lowercase + word boundary split + filter
    words = re.findall(r"\b[a-zA-Z][a-zA-Z\-]+\b", user_message.lower())
    keywords = [w for w in words if len(w) > 2 and w not in _STOP_WORDS]

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for w in keywords:
        if w not in seen:
            seen.add(w)
            unique.append(w)

    # Q3 Option C: entities and topics use the same candidate list for MVP.
    # InsightJournal.get_for_context scores both axes; passing the same
    # list to both gives the maximum-signal match.
    return unique, unique


# =============================================================================
# Response composer (Phase 2)
# =============================================================================


# Confidence binning per D3 spec §"Confidence Expression":
# high (0.8+), medium (0.6-0.8), low (<0.6).
CONFIDENCE_HIGH_THRESHOLD = 0.8
CONFIDENCE_MEDIUM_THRESHOLD = 0.6


# No-deflection honest fallback per Rule 5
NO_INSIGHTS_RESPONSE = "I haven't noticed anything specific about that yet."


# Correction invitation appended to every non-empty Pull response per Rule 3
CORRECTION_INVITATION = (
    "Would you like me to explain any of these, or correct something that's off?"
)


@dataclass
class PullResponseSections:
    """Internal data shape for the sectioned response.

    Fields are lists of human-framed insight texts (already passed through
    the #1033 anti-surveillance guardrail via `frame_insight_for_surfacing`
    upstream of this module).
    """

    high: List[str]
    medium: List[str]
    low: List[str]

    @property
    def total_count(self) -> int:
        return len(self.high) + len(self.medium) + len(self.low)


def _bin_by_confidence(insights) -> PullResponseSections:
    """Bin a list of SurfaceableInsight by confidence band.

    Each section's contents are framed via `frame_insight_for_surfacing`
    (which applies the #1033 anti-surveillance guardrail).
    """
    from services.mux.premonition import frame_insight_for_surfacing

    high: List[str] = []
    medium: List[str] = []
    low: List[str] = []

    for insight in insights:
        # frame_insight_for_surfacing does the guardrail-safe framing
        framed = frame_insight_for_surfacing(insight)
        confidence = insight.learning.confidence if insight.learning else 0.0

        if confidence >= CONFIDENCE_HIGH_THRESHOLD:
            high.append(framed)
        elif confidence >= CONFIDENCE_MEDIUM_THRESHOLD:
            medium.append(framed)
        else:
            low.append(framed)

    return PullResponseSections(high=high, medium=medium, low=low)


def format_pull_response(insights) -> str:
    """Build the user-facing Pull-mode response per D4 §"Response Format".

    Q5: enforces no-deflection rule. If `insights` is empty or None,
    returns the honest fallback. Otherwise builds the sectioned markdown
    + correction invitation per spec.

    Q4: identical shape at all trust stages for MVP. Caller is responsible
    for not invoking this if trust-stage gating is in play (Pull is
    available at all stages per D1, so this is normally always called).
    """
    if not insights:
        return NO_INSIGHTS_RESPONSE

    sections = _bin_by_confidence(insights)

    # Pull mode always returns SOMETHING per Rule 5 (no deflection)
    if sections.total_count == 0:
        # Defensive: insights list non-empty but all binned out (e.g.,
        # confidence=None). Show all insights as "less sure" rather than
        # deflecting.
        return NO_INSIGHTS_RESPONSE

    parts: List[str] = []

    if sections.high:
        parts.append("**High confidence:**")
        parts.extend(f"- {text}" for text in sections.high)
        parts.append("")  # blank line between sections

    if sections.medium:
        parts.append("**Medium confidence:**")
        parts.extend(f"- {text}" for text in sections.medium)
        parts.append("")

    if sections.low:
        parts.append("**Something I'm less sure about:**")
        parts.extend(f"- {text}" for text in sections.low)
        parts.append("")

    # Strip trailing blank line
    while parts and parts[-1] == "":
        parts.pop()

    parts.append("")  # blank line before correction invitation
    parts.append(CORRECTION_INVITATION)

    return "\n".join(parts)


# =============================================================================
# Top-level Pull responder
# =============================================================================


async def respond_to_pull(
    user_message: str,
    user_id: str,
    trust_stage: int = 1,
    journal=None,
    limit: int = 10,
) -> str:
    """End-to-end Pull-mode handler.

    1. Extract context from user_message
    2. Query InsightJournal.get_for_context (durable per #1035)
    3. Format response per D4 spec
    4. Return string ready for the user

    Args:
        user_message: The user's natural-language Pull query
        user_id: The user (passed to journal for user-scoping)
        trust_stage: 1-4 (Pull works at all stages per D1; passed through
            to journal so it can apply per-insight min_trust_stage gates)
        journal: Optional InsightJournal instance; defaults to
            constructing one (which is repository-backed per #1035)
        limit: Max insights to retrieve

    Returns:
        Formatted response string ready for the conversational floor
    """
    # Defensive: empty/missing message → honest no-deflection
    if not user_message:
        return NO_INSIGHTS_RESPONSE

    if journal is None:
        from services.mux.composting_pipeline import InsightJournal

        journal = InsightJournal()

    entities, topics = extract_context(user_message)
    insights = await journal.get_for_context(
        user_id=user_id,
        context_entities=entities,
        context_topics=topics,
        trust_stage=trust_stage,
        limit=limit,
    )

    return format_pull_response(insights)
