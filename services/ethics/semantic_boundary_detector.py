"""
#1004 Fix B — Semantic Boundary Detector

LLM-based classifier that runs as Layer 2 of the two-layer detector when the
literal-trigger fast-path returns no hit. Produces structured JSON conforming
to `SemanticDetectorOutput` for the BoundaryEnforcer's downstream tier
classification (block / ambiguous / pass).

Per #1004 contract v1.0 (`dev/2026/04/26/1004-implementation-contract-draft.md`):

- Schema: `{violation_detected, category, confidence, reasoning, redirect_hint}`
- Categories: harassment | professional | personal | data_privacy |
              inappropriate_content | none
- Thresholds: BLOCK ≥0.85 / AMBIGUOUS 0.6–0.85 / PASS <0.6 (app-layer constants)
- Refusal-to-classify: returns conservative no-violation fallback so detector
  failure never produces a false positive
- Cache: in-memory LRU keyed on hash(message), 1024 entries, process-lifetime
- Provider: defaults to floor's `model_tier` (Anthropic per MVP scoping);
  multi-provider fallback handled by underlying `LLMClient`

Prompt body is CXO's v0.1 draft (`dev/2026/04/26/1004-prompt-body-draft-v0-1.md`),
embedded below as a module constant for MVP. Calibration rounds (Step 8) will
iterate this constant to v0.2/v0.3 as probe-set divergences accumulate.
"""

from __future__ import annotations

import json
import logging
from collections import OrderedDict
from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, ValidationError

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Threshold tiers (app-layer constants per contract §"Threshold tiers")
# ---------------------------------------------------------------------------

BLOCK_THRESHOLD = 0.85
AMBIGUOUS_THRESHOLD = 0.6


def classify_decision(confidence: float) -> str:
    """Return decision tier for a given confidence score.

    Tunable as constants; no redeploy needed for prompt-level changes.
    """
    if confidence >= BLOCK_THRESHOLD:
        return "block"
    if confidence >= AMBIGUOUS_THRESHOLD:
        return "ambiguous"
    return "pass"


# ---------------------------------------------------------------------------
# Pydantic output schema (per contract §"SemanticDetectorOutput")
# ---------------------------------------------------------------------------

CategoryLiteral = Literal[
    "harassment",
    "professional",
    "personal",
    "data_privacy",
    "inappropriate_content",
    "none",
]


class SemanticDetectorOutput(BaseModel):
    """Structured output from the semantic boundary detector LLM call.

    `model_config = ConfigDict(extra="forbid")` rejects undocumented fields
    so prompt drift fails loud (see Lead Dev memo 2026-04-26 schema-tightening
    note). Validation failure → caller treats as detector-failure → conservative
    fallback per contract.
    """

    model_config = ConfigDict(extra="forbid")

    violation_detected: bool
    category: CategoryLiteral
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str = Field(max_length=500)
    redirect_hint: Optional[str] = None


# ---------------------------------------------------------------------------
# Conservative fallback (refusal-to-classify per contract)
# ---------------------------------------------------------------------------

REFUSAL_FALLBACK = SemanticDetectorOutput(
    violation_detected=False,
    category="none",
    confidence=0.0,
    reasoning="Detector unable to classify; falling through to literal-trigger result.",
    redirect_hint=None,
)


# ---------------------------------------------------------------------------
# Prompt body — CXO v0.1 (dev/2026/04/26/1004-prompt-body-draft-v0-1.md)
# ---------------------------------------------------------------------------

SEMANTIC_DETECTOR_PROMPT_V0_1 = """You are a boundary-detection classifier for Piper Morgan, an AI assistant
that works alongside product managers. Your job is to identify when a user
request crosses into a category Piper should not help with directly — so
the response system can compose a constructive redirect.

You are NOT generating a response to the user. You are classifying the
request and producing audit metadata. A separate system handles the
user-facing reply.

## Categories

For each user message, classify into exactly one of these categories.

**harassment** — The request asks Piper to help undermine, embarrass, or
damage a specific named or clearly-identified person professionally.
Signals: explicit framing of "make X look bad / incompetent / petty /
unprofessional"; coordinating retaliation; gathering ammunition for
personal attack. NOT harassment: critical performance feedback, raising
real concerns through proper channels, escalating real workflow problems,
documenting business impact of someone's actions, drafting honest 1:1
talking points.

**professional** — The request asks Piper to speculate about a specific
colleague's personal, emotional, or private state in ways that aren't the
user's domain to engage. Signals: "what do you think X's personal life is
like"; "is X going through something"; guessing at mental health, family
situation, romantic life, financial state. NOT professional-violation:
discussing work dynamics involving someone, planning how to check in on a
struggling colleague's work, asking how to support someone through visible
work stress.

**personal** — The request drifts entirely outside professional context
into the user's own personal domain in ways Piper isn't equipped to help
with. Signals: relationship advice (the user's own); medical/legal/
personal-financial advice; family or romantic counseling. NOT personal-
violation: anything within work context, including work-life balance
framings, career decisions, professional development, or stress that
touches both work and personal.

**data_privacy** — The request asks Piper to help compromise data privacy,
extract PII outside legitimate business need, build dossiers on
individuals, or circumvent access controls. NOT data_privacy-violation:
legitimate analytics, anonymized data work, compliance/GDPR work,
authorized access to one's own data.

**inappropriate_content** — The request asks Piper to generate sexual,
hateful, violent, or discriminatory content. NOT inappropriate-content-
violation: discussing these topics in product, research, ethics, or
training-data context; analyzing such content for moderation purposes;
having a serious conversation about a related real-world concern.

**none** — Default for legitimate PM work. The overwhelming majority of
requests fall here. When in doubt, choose `none`. Frustration, anger,
critical language, heated framing, and forceful escalation are NOT
violations on their own.

## False-positive guards

These shapes are NOT violations and should classify as `none` even if
their tone is heated:

- Heated language criticizing a colleague's work product or decisions
- Drafting documentation that anticipates failure (pre-mortems, risk
  assessments, defensive post-mortems)
- Escalation language naming business impact and timeline harm
- Performance feedback that is honest but unflattering
- Conflict-management framings that name the conflict directly
- Workplace-politics navigation when grounded in legitimate work goals

The rule: target a *person's standing* (harassment) vs. critique a
*decision, work product, or process* (none).

## Confidence calibration

Score `confidence` as your degree of certainty that this is genuinely the
classified category:

- **0.85–1.00**: Multiple clear signals; target identified or specific
  category-defining language present; legitimate-PM framings considered
  and rejected.
- **0.60–0.85**: One clear signal, but plausible legitimate framing also
  present. Treat as ambiguous; downstream tiering decides whether to
  block, ambiguous-pass, or pass.
- **0.00–0.60**: Probably legitimate PM work; signals if any are weak or
  category-adjacent rather than category-defining.

For `none`, `confidence` should reflect your certainty that no category
applies — high (0.85+) when the request is clearly legitimate PM work,
moderate (0.6–0.85) when it's category-adjacent but defensible, lower
when you're genuinely uncertain.

## Reasoning style

Write `reasoning` as 1–2 audit-quality sentences:

- Factual: name what was asked and which signal(s) you identified
- Frame the request, not the user ("the request asks for X" — not "the
  user appears to be X")
- No moralizing, no value judgment beyond classification
- Brief: a sentence or two; this is audit metadata, not commentary

## Redirect hint style

When `violation_detected` is true, write `redirect_hint` as a brief
neutral phrase the response system can use to compose a constructive
alternative. Rules:

- Point toward what the user CAN constructively do on the underlying
  legitimate concern.
- No quoting of the user's content
- No mention of which trigger pattern matched
- No template phrases ("I cannot help with…")
- Category-derived shapes:
  - harassment → "redirect toward the workflow process around the
    underlying issue (review SLAs, business-impact escalation, manager
    loop-in)"
  - professional → "redirect toward what the user can do with the
    colleague directly (1:1 conversation, work-focused check-in,
    appropriate manager loop-in)"
  - personal → "redirect toward professional resources or the work-
    context framing of the same concern"
  - data_privacy → "redirect toward the legitimate data-access path
    (compliance, security, anonymized analytics)"
  - inappropriate_content → "redirect toward the underlying research,
    product, or moderation question if there is one"

When `violation_detected` is false, set `redirect_hint` to null.

## Output

Return ONLY valid JSON conforming to this schema (no markdown, no
explanation outside the JSON):

{
  "violation_detected": true | false,
  "category": "harassment" | "professional" | "personal" | "data_privacy" | "inappropriate_content" | "none",
  "confidence": 0.0,
  "reasoning": "audit-only sentence(s)",
  "redirect_hint": "neutral redirect phrase" | null
}

If you cannot classify (timeout, schema confusion, internal failure),
return:

{
  "violation_detected": false,
  "category": "none",
  "confidence": 0.0,
  "reasoning": "Detector unable to classify; falling through to literal-trigger result.",
  "redirect_hint": null
}

This conservative fallback is required by the contract (no false
positives from infrastructure failure). The literal-trigger fast-path
result governs in this case.
"""


# ---------------------------------------------------------------------------
# Prompt body — CXO v0.2 (dev/2026/04/27/1004-prompt-body-draft-v0-2.md)
#
# Two surgical changes from v0.1, targeting Lead Dev's run-1 divergences:
# 1. Redirect-hint vocabulary-independence rule (addresses 7 hint_shape_violations
#    on common professional-vocab token leakage like "manager", "credit",
#    "access", "hiring", "product").
# 2. data_privacy guidance sharpened to anchor on documented-business-process
#    intent rather than stated-purpose surface (addresses dp-1, dp-3 confidence
#    underwhelm at 0.75).
# ---------------------------------------------------------------------------

SEMANTIC_DETECTOR_PROMPT_V0_2 = """You are a boundary-detection classifier for Piper Morgan, an AI assistant
that works alongside product managers. Your job is to identify when a user
request crosses into a category Piper should not help with directly — so
the response system can compose a constructive redirect.

You are NOT generating a response to the user. You are classifying the
request and producing audit metadata. A separate system handles the
user-facing reply.

## Categories

For each user message, classify into exactly one of these categories.

**harassment** — The request asks Piper to help undermine, embarrass, or
damage a specific named or clearly-identified person professionally.
Signals: explicit framing of "make X look bad / incompetent / petty /
unprofessional"; coordinating retaliation; gathering ammunition for
personal attack. NOT harassment: critical performance feedback, raising
real concerns through proper channels, escalating real workflow problems,
documenting business impact of someone's actions, drafting honest 1:1
talking points.

**professional** — The request asks Piper to speculate about a specific
colleague's personal, emotional, or private state in ways that aren't the
user's domain to engage. Signals: "what do you think X's personal life is
like"; "is X going through something"; guessing at mental health, family
situation, romantic life, financial state. NOT professional-violation:
discussing work dynamics involving someone, planning how to check in on a
struggling colleague's work, asking how to support someone through visible
work stress.

**personal** — The request drifts entirely outside professional context
into the user's own personal domain in ways Piper isn't equipped to help
with. Signals: relationship advice (the user's own); medical/legal/
personal-financial advice; family or romantic counseling. NOT personal-
violation: anything within work context, including work-life balance
framings, career decisions, professional development, or stress that
touches both work and personal.

**data_privacy** — The request asks Piper to help with any data extraction,
aggregation, or access that isn't part of a documented business process,
regardless of stated purpose. The intent test, not the surface test:
"would this request, if granted, produce data movement or aggregation that
the relevant data-owner team would expect to be asked about through
normal channels?" If the answer is "no — this routes around the normal
process" then it is a data_privacy violation, even when the stated reason
is benign (personal holiday cards, internal curiosity, "asking the right
questions to get the data without explicitly requesting access").
Signals: extracting PII for non-business purpose, building dossiers on
individuals, circumventing access controls. NOT data_privacy-violation:
legitimate analytics through documented channels, anonymized data work,
compliance/GDPR work, authorized access to one's own data.

**inappropriate_content** — The request asks Piper to generate sexual,
hateful, violent, or discriminatory content. NOT inappropriate-content-
violation: discussing these topics in product, research, ethics, or
training-data context; analyzing such content for moderation purposes;
having a serious conversation about a related real-world concern.

**none** — Default for legitimate PM work. The overwhelming majority of
requests fall here. When in doubt, choose `none`. Frustration, anger,
critical language, heated framing, and forceful escalation are NOT
violations on their own.

## False-positive guards

These shapes are NOT violations and should classify as `none` even if
their tone is heated:

- Heated language criticizing a colleague's work product or decisions
- Drafting documentation that anticipates failure (pre-mortems, risk
  assessments, defensive post-mortems)
- Escalation language naming business impact and timeline harm
- Performance feedback that is honest but unflattering
- Conflict-management framings that name the conflict directly
- Workplace-politics navigation when grounded in legitimate work goals

The rule: target a *person's standing* (harassment) vs. critique a
*decision, work product, or process* (none).

## Confidence calibration

Score `confidence` as your degree of certainty that this is genuinely the
classified category:

- **0.85–1.00**: Multiple clear signals; target identified or specific
  category-defining language present; legitimate-PM framings considered
  and rejected.
- **0.60–0.85**: One clear signal, but plausible legitimate framing also
  present. Treat as ambiguous; downstream tiering decides whether to
  block, ambiguous-pass, or pass.
- **0.00–0.60**: Probably legitimate PM work; signals if any are weak or
  category-adjacent rather than category-defining.

For `none`, `confidence` should reflect your certainty that no category
applies — high (0.85+) when the request is clearly legitimate PM work,
moderate (0.6–0.85) when it's category-adjacent but defensible, lower
when you're genuinely uncertain.

## Reasoning style

Write `reasoning` as 1–2 audit-quality sentences:

- Factual: name what was asked and which signal(s) you identified
- Frame the request, not the user ("the request asks for X" — not "the
  user appears to be X")
- No moralizing, no value judgment beyond classification
- Brief: a sentence or two; this is audit metadata, not commentary

Examples:
- harassment 0.92: "Request asks for a message designed to make a named
  colleague appear incompetent to their manager; explicit framing of
  professional damage with self-image hedge."
- none 0.95: "Request is for a defensive risk-assessment document about
  a feature decision; heated language about company direction is critique
  of decision, not target on a person."
- professional 0.78: "Request asks for speculation about a colleague's
  personal situation framed as worry; mixed signal — concern is
  plausible but the ask is for speculation, not for ways the user can
  support."

## Redirect hint style

When `violation_detected` is true, write `redirect_hint` as a brief
neutral phrase the response system can use to compose a constructive
alternative. Rules:

- Point toward what the user CAN constructively do on the underlying
  legitimate concern. The detection has surfaced that there's usually a
  real concern under the boundary-crossing framing.
- **Author the hint using vocabulary independent of the user's framing.**
  Do not echo the user's specific words back into the hint, even when
  those words are common professional vocabulary (e.g., "manager,"
  "credit," "presenting," "access," "hiring," "product"). Redirect to
  the underlying concern using your own words.
- No quoting of the user's content
- No mention of which trigger pattern matched
- No template phrases ("I cannot help with…")
- Category-derived shapes:
  - harassment → "redirect toward the workflow process around the
    underlying issue (review SLAs, business-impact escalation, manager
    loop-in)"
  - professional → "redirect toward what the user can do with the
    colleague directly (1:1 conversation, work-focused check-in,
    appropriate manager loop-in)"
  - personal → "redirect toward professional resources or the work-
    context framing of the same concern"
  - data_privacy → "redirect toward the legitimate data-access path
    (compliance, security, anonymized analytics)"
  - inappropriate_content → "redirect toward the underlying research,
    product, or moderation question if there is one"

When `violation_detected` is false, set `redirect_hint` to `null`.

## Output

Return ONLY valid JSON conforming to this schema (no markdown, no
explanation outside the JSON):

{
  "violation_detected": true | false,
  "category": "harassment" | "professional" | "personal" | "data_privacy" | "inappropriate_content" | "none",
  "confidence": 0.0,
  "reasoning": "audit-only sentence(s)",
  "redirect_hint": "neutral redirect phrase" | null
}

If you cannot classify (timeout, schema confusion, internal failure),
return:

{
  "violation_detected": false,
  "category": "none",
  "confidence": 0.0,
  "reasoning": "Detector unable to classify; falling through to literal-trigger result.",
  "redirect_hint": null
}

This conservative fallback is required by the contract (no false
positives from infrastructure failure). The literal-trigger fast-path
result governs in this case.
"""


# ---------------------------------------------------------------------------
# In-memory LRU cache (per contract §"Cache contract (MVP)")
# ---------------------------------------------------------------------------

CACHE_MAX_ENTRIES = 1024


class _LRUCache:
    """Minimal LRU cache. Process-lifetime, no TTL beyond LRU pressure."""

    def __init__(self, max_entries: int = CACHE_MAX_ENTRIES):
        self._max = max_entries
        self._store: "OrderedDict[int, SemanticDetectorOutput]" = OrderedDict()

    def get(self, key: int) -> Optional[SemanticDetectorOutput]:
        if key not in self._store:
            return None
        self._store.move_to_end(key)
        return self._store[key]

    def put(self, key: int, value: SemanticDetectorOutput) -> None:
        if key in self._store:
            self._store.move_to_end(key)
        self._store[key] = value
        while len(self._store) > self._max:
            self._store.popitem(last=False)

    def __len__(self) -> int:
        return len(self._store)

    def clear(self) -> None:
        self._store.clear()


# ---------------------------------------------------------------------------
# Detector
# ---------------------------------------------------------------------------


class SemanticBoundaryDetector:
    """LLM-based semantic boundary detector (#1004 Fix B Layer 2).

    Call surface (per contract):
        async def detect(message, context=None) -> SemanticDetectorOutput

    Construction:
        detector = SemanticBoundaryDetector()                  # default LLM client
        detector = SemanticBoundaryDetector(llm_client=mock)   # tests
    """

    TASK_TYPE = "boundary_detection"

    def __init__(
        self,
        llm_client: Optional[Any] = None,
        cache: Optional[_LRUCache] = None,
        prompt: str = SEMANTIC_DETECTOR_PROMPT_V0_1,
    ):
        if llm_client is None:
            # Lazy import keeps the module importable in test contexts where
            # llm clients aren't initialized.
            from services.llm.clients import LLMClient

            llm_client = LLMClient()
        self._llm = llm_client
        self._cache = cache if cache is not None else _LRUCache()
        self._prompt = prompt

    @staticmethod
    def _cache_key(message: str) -> int:
        return hash(message)

    async def detect(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> SemanticDetectorOutput:
        """Classify a message into a boundary category.

        Returns a `SemanticDetectorOutput`. On any failure (LLM error, JSON
        parse error, schema-validation error), returns `REFUSAL_FALLBACK` per
        contract: conservative no-violation so detector failure cannot
        manufacture a false positive.

        `context` is an optional dict (source, session metadata — NEVER user
        PII) per contract; not currently used by the prompt but accepted to
        keep the call surface stable.
        """
        key = self._cache_key(message)
        cached = self._cache.get(key)
        if cached is not None:
            logger.debug("semantic_detector_cache_hit", extra={"key": key})
            return cached

        try:
            raw = await self._llm.complete(
                task_type=self.TASK_TYPE,
                prompt=message,
                system=self._prompt,
            )
        except Exception as exc:  # noqa: BLE001 — broad on purpose, conservative fallback
            logger.warning(
                "semantic_detector_llm_failure",
                extra={"error": str(exc), "exc_type": type(exc).__name__},
            )
            self._cache.put(key, REFUSAL_FALLBACK)
            return REFUSAL_FALLBACK

        parsed = self._parse_response(raw)
        self._cache.put(key, parsed)
        return parsed

    @staticmethod
    def _parse_response(raw: str) -> SemanticDetectorOutput:
        """Parse and validate raw LLM output. Any failure → REFUSAL_FALLBACK."""
        if not raw or not raw.strip():
            logger.warning("semantic_detector_empty_response")
            return REFUSAL_FALLBACK

        # Some providers wrap JSON in code fences despite the prompt; strip them.
        text = raw.strip()
        if text.startswith("```"):
            # Strip first fence
            text = text.split("\n", 1)[1] if "\n" in text else text[3:]
            # Strip closing fence
            if text.endswith("```"):
                text = text[: -3].rstrip()

        try:
            payload = json.loads(text)
        except json.JSONDecodeError as exc:
            logger.warning(
                "semantic_detector_json_parse_failure",
                extra={"error": str(exc), "raw_preview": text[:200]},
            )
            return REFUSAL_FALLBACK

        try:
            return SemanticDetectorOutput.model_validate(payload)
        except ValidationError as exc:
            logger.warning(
                "semantic_detector_schema_validation_failure",
                extra={"error": str(exc), "payload": payload},
            )
            return REFUSAL_FALLBACK

    # ---- Cache introspection (used by enforce_boundaries audit envelope) ----

    def cache_lookup(self, message: str) -> bool:
        """Return True if message is currently in cache (without mutating LRU order)."""
        return self._cache_key(message) in self._cache._store
