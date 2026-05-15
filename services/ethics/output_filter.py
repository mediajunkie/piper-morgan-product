"""
OutputFilter — post-generation content filter for LLM outputs reaching users.

Issue #1017 Phase 2.1 — scaffold landing.

The filter wraps `LLMClient.complete()` (Phase 2.2 wiring; this module is the
filter implementation itself) and applies a profile selected by `task_type`.
Per #1017 design memo + Architect/CXO ratification (2026-05-15):

- Tier 1 PII: regex-based redaction reusing `SecurityRedactor` patterns +
  added API key / bearer-token / URL-with-credentials patterns.
- Tier 2 BoundaryEnforcer: applies the existing boundary category check
  (harassment, inappropriate content, professional-boundary) to the LLM
  output text using `BoundaryEnforcer.enforce_boundaries`.
- Tier 3 (hallucination grounding, length anomalies, cross-user leakage):
  deferred to follow-up.

Action matrix:

| Detection                  | Severity  | Action                       |
|----------------------------|-----------|------------------------------|
| PII regex                  | medium    | Redact in place → [REDACTED] |
| Secret formats             | high      | Redact + operator-flag       |
| URL with embedded creds    | high      | Redact whole URL             |
| BoundaryEnforcer violation | critical  | Drop output + canned         |
| No match                   | —         | Passthrough                  |

When a category violation drops the output, the decorator (Phase 2.2)
retries via `regenerate_on_violation` and only surfaces the canned
phrasing to the user if regenerate-also-fails. Both attempts are
captured in the audit envelope via `attempt_number` +
`prior_attempt_decision_id`.

Audit envelope writes through `log_output_filter_decision()` (Phase 2.3),
a sibling of `log_ethics_decision()` — separate entry points keep
evolution clean. Hashes only — never raw PII (per Architect Q4
observation: "audit logs for content-filtering decisions must never
store the filtered content; hashes and rule-IDs only").
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

import structlog

logger = structlog.get_logger(__name__)


# ============================================================================
# Constants — ratified design
# ============================================================================

REDACTED_TOKEN = "[REDACTED]"

# CXO-ratified canned response for category violations (Q3, 2026-05-15).
# Output-side ownership phrasing — see CT v2.3 §Tone-0 cadence analysis.
CANNED_VIOLATION_RESPONSE = "That came out wrong — let me try a different approach."


class Severity:
    """Severity levels for OutputFilterDecision."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Action:
    """Action taken on a filter decision."""

    PASSTHROUGH = "passthrough"
    REDACT_IN_PLACE = "redact_in_place"
    CANNED_SUBSTITUTE = "canned_substitute"
    DROP = "drop"


class Profile:
    """Filter profile selected by `task_type`."""

    USER_VISIBLE = "user_visible"  # Tier 1 + Tier 2
    INTERNAL = "internal"  # log-only, no transform
    MIXED = "mixed"  # defaults to user_visible


# ============================================================================
# Profile registry — task_type → profile mapping
# ============================================================================
#
# Folded from #1017 design memo + Architect Q6 pushback (2026-05-15):
# - relationship_analysis escalated to user_visible (transitive visibility:
#   KG content surfaces back to users via downstream queries)
# - slot_extraction escalated to user_visible (slot-confirmation prompts
#   echo extracted values via slot_prompts.format_confirmation)
# - work_item_extraction escalated to user_visible (becomes GitHub issue
#   body via content_generator)
# - intent_classification stays internal (parsed into structured Intent
#   object; not echoed verbatim to users)

_PROFILE_REGISTRY: Dict[str, str] = {
    # User-visible: outputs flow to users via chat surfaces, GitHub, etc.
    "conversation": Profile.USER_VISIBLE,
    "question_answering": Profile.USER_VISIBLE,
    "document_comparison": Profile.USER_VISIBLE,
    "conversational_reference": Profile.USER_VISIBLE,
    "summarize": Profile.USER_VISIBLE,
    "issue_analysis": Profile.USER_VISIBLE,
    "github_content_generation": Profile.USER_VISIBLE,
    "relationship_analysis": Profile.USER_VISIBLE,
    "slot_extraction": Profile.USER_VISIBLE,
    "work_item_extraction": Profile.USER_VISIBLE,
    # Internal: parsed into structured types; not surfaced verbatim.
    "intent_classification": Profile.INTERNAL,
    # Mixed: depends on caller; default to user_visible (fail-closed).
    "general": Profile.MIXED,
}


def profile_for(task_type: str) -> str:
    """Return the filter profile for a task_type, defaulting to user_visible.

    Unknown task_types fall back to `user_visible` (fail-closed default per
    Architect Q6 ratification — new task_types must opt out of filtering
    explicitly, not opt in).
    """
    profile = _PROFILE_REGISTRY.get(task_type, Profile.USER_VISIBLE)
    if profile == Profile.MIXED:
        return Profile.USER_VISIBLE
    return profile


# ============================================================================
# Decision + result schemas
# ============================================================================


@dataclass
class OutputFilterDecision:
    """Decision-shaped audit record for a single filter pass.

    Written to the durable audit log via `log_output_filter_decision()`
    (Phase 2.3). Mirrors `BoundaryDecision` shape for the audit-side
    surface; caller sees only `FilterResult.filtered_content`.

    Critical invariant: this record stores HASHES of content, never raw
    content. If a PII string was redacted, the original content's hash
    plus the redacted content's hash provide verification without making
    the audit log a PII honeypot.
    """

    decision_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    user_id: Optional[str] = None
    session_id: Optional[str] = None

    # Surface + profile
    surface: str = ""  # task_type acts as surface tag
    profile_applied: str = Profile.USER_VISIBLE

    # Detection
    matched_rules: List[str] = field(default_factory=list)
    severity: str = Severity.LOW
    redactions_count: int = 0

    # Action
    action_taken: str = Action.PASSTHROUGH

    # Content references (hashes only — never raw)
    original_content_hash: str = ""
    filtered_content_hash: str = ""

    # Regenerate-trigger chain (folded in per Architect 2026-05-15 cross-talk)
    attempt_number: int = 1
    prior_attempt_decision_id: Optional[str] = None

    # Extension point
    audit_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "timestamp": self.timestamp.isoformat(),
            "user_id": self.user_id,
            "session_id": self.session_id,
            "surface": self.surface,
            "profile_applied": self.profile_applied,
            "matched_rules": list(self.matched_rules),
            "severity": self.severity,
            "redactions_count": self.redactions_count,
            "action_taken": self.action_taken,
            "original_content_hash": self.original_content_hash,
            "filtered_content_hash": self.filtered_content_hash,
            "attempt_number": self.attempt_number,
            "prior_attempt_decision_id": self.prior_attempt_decision_id,
            "audit_metadata": dict(self.audit_metadata),
        }


@dataclass
class FilterResult:
    """Caller-facing result of `OutputFilter.filter()`.

    `filtered_content` is what the caller substitutes into its response
    path. `decision` is captured for the audit log; callers typically
    don't inspect it.
    """

    is_violation: bool
    filtered_content: str
    decision: OutputFilterDecision


# ============================================================================
# OutputFilter — main entry point
# ============================================================================


def _hash_content(content: str) -> str:
    """sha256 hex digest of UTF-8 content; empty string → empty digest."""
    if not content:
        return ""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


class OutputFilter:
    """Apply post-generation content filtering to LLM output.

    Single entry point: `await output_filter.filter(content, task_type, ...)`.
    Returns `FilterResult` with the content to actually return to the user
    plus the decision record for audit.

    The filter dispatches to rule modules based on profile:
    - `user_visible` profile: Tier 1 PII rules + Tier 2 BoundaryEnforcer
    - `internal` profile: log-only, no transformation

    Rule modules live in `services/ethics/output_filter_rules.py`.
    """

    def __init__(self, boundary_enforcer=None):
        """
        Args:
            boundary_enforcer: optional injected BoundaryEnforcer for Tier 2.
                If None, the filter operates Tier 1 only. Phase 2.2 wiring
                will pass the application's shared BoundaryEnforcer instance.
        """
        self._boundary_enforcer = boundary_enforcer

    async def filter(
        self,
        content: str,
        task_type: str,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        attempt_number: int = 1,
        prior_attempt_decision_id: Optional[str] = None,
    ) -> FilterResult:
        """Run the filter pipeline against `content` and return a result.

        Args:
            content: the LLM-generated output text.
            task_type: the LLMClient task_type that produced the output;
                drives profile selection.
            user_id, session_id: audit envelope context.
            attempt_number: 1 for the first generation; 2+ for retries from
                the `regenerate_on_violation` flow.
            prior_attempt_decision_id: links to the previous attempt's
                OutputFilterDecision when this is a retry.

        Returns:
            FilterResult with the filtered content + decision record.
        """
        from services.ethics.output_filter_rules import (
            apply_boundary_rules,
            apply_pii_rules,
            apply_secret_rules,
        )

        profile = profile_for(task_type)
        decision = OutputFilterDecision(
            user_id=user_id,
            session_id=session_id,
            surface=task_type,
            profile_applied=profile,
            attempt_number=attempt_number,
            prior_attempt_decision_id=prior_attempt_decision_id,
            original_content_hash=_hash_content(content),
        )

        # Internal profile: log the pass, no transform.
        if profile == Profile.INTERNAL:
            decision.action_taken = Action.PASSTHROUGH
            decision.filtered_content_hash = decision.original_content_hash
            return FilterResult(
                is_violation=False, filtered_content=content, decision=decision
            )

        # Tier 1 — PII + secrets, redact-in-place.
        filtered_content = content
        filtered_content, pii_match = apply_pii_rules(filtered_content)
        filtered_content, secret_match = apply_secret_rules(filtered_content)

        decision.redactions_count = pii_match.redactions_count + secret_match.redactions_count
        decision.matched_rules.extend(pii_match.matched_rules)
        decision.matched_rules.extend(secret_match.matched_rules)

        if decision.redactions_count > 0:
            decision.action_taken = Action.REDACT_IN_PLACE
            # Severity escalates to high if any secret-rule matched, else medium.
            if secret_match.matched_rules:
                decision.severity = Severity.HIGH
            else:
                decision.severity = Severity.MEDIUM

        # Tier 2 — BoundaryEnforcer category check.
        if self._boundary_enforcer is not None:
            boundary_match = await apply_boundary_rules(
                filtered_content, self._boundary_enforcer
            )
            if boundary_match.is_violation:
                # Critical: drop the LLM output, substitute canned response.
                decision.matched_rules.extend(boundary_match.matched_rules)
                decision.severity = Severity.CRITICAL
                decision.action_taken = Action.CANNED_SUBSTITUTE
                filtered_content = CANNED_VIOLATION_RESPONSE
                decision.filtered_content_hash = _hash_content(filtered_content)
                return FilterResult(
                    is_violation=True,
                    filtered_content=filtered_content,
                    decision=decision,
                )

        decision.filtered_content_hash = _hash_content(filtered_content)
        return FilterResult(
            is_violation=False,
            filtered_content=filtered_content,
            decision=decision,
        )


def build_default_output_filter() -> OutputFilter:
    """Construct an OutputFilter wired to the application's default BoundaryEnforcer.

    Phase 2.3 container-wiring entry point: called from startup.py's
    OutputFilterWiringPhase after BoundaryEnforcer dependencies (config,
    audit_transparency, etc.) are ready. Returns a configured OutputFilter
    ready to attach via `LLMClient.set_output_filter()`.

    Kept as a free function (not a class method) so the wiring surface is
    grep-able and discoverable from the startup phase that uses it.
    """
    from services.ethics.boundary_enforcer_refactored import BoundaryEnforcer

    boundary_enforcer = BoundaryEnforcer()
    return OutputFilter(boundary_enforcer=boundary_enforcer)
