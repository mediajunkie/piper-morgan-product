"""
Output filter rule modules — PII, secrets, boundary categories.

Issue #1017 Phase 2.1 — scaffold landing.

Three rule categories:

1. **PII rules** — reuse `SecurityRedactor` patterns already in
   `audit_transparency.py` (email, SSN, phone formats, credit card).
   Severity medium; action redact-in-place.

2. **Secret rules** — fresh pattern set for API keys + bearer tokens +
   URL-with-embedded-credentials. These aren't in SecurityRedactor today
   because that module was designed for input redaction where secrets
   are less common.  Severity high; action redact + operator-flag.

3. **Boundary rules** — thin wrapper over `BoundaryEnforcer.enforce_boundaries()`.
   Severity critical; action drop-with-canned-substitute (handled by
   the caller in `OutputFilter.filter`; this module just signals
   is_violation).

Each rule function returns a `RuleMatchResult` with the redacted text
+ matched-rule IDs + redaction count. The main `OutputFilter` aggregates
across rules to build the `OutputFilterDecision`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Tuple

import structlog

logger = structlog.get_logger(__name__)


REDACTED_TOKEN = "[REDACTED]"


@dataclass
class RuleMatchResult:
    """Result of applying a rule module to content."""

    matched_rules: List[str] = field(default_factory=list)
    redactions_count: int = 0
    is_violation: bool = False  # For category violations (boundary rules)


# ============================================================================
# Tier 1 — PII rules (reuse SecurityRedactor patterns)
# ============================================================================
#
# SecurityRedactor's patterns at `audit_transparency.py:42-49`:
# - Email
# - SSN (3-2-4)
# - Phone (3-3-4 hyphen) — added #1007 May 2
# - Phone ((NNN) NNN-NNNN)
# - Credit card (4-4-4-4)
# - Phone (10-11 digit-only)
#
# Output-filter applies these to LLM output rather than audit log content,
# but the patterns themselves are identical. Importing SecurityRedactor's
# instance directly keeps a single source of truth — when the pattern set
# evolves, both audit redaction and output filtering update together.

_PII_RULE_IDS = {
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b": "pii:email",
    r"\b\d{3}-\d{2}-\d{4}\b": "pii:ssn",
    r"\b\d{3}-\d{3}-\d{4}\b": "pii:phone_hyphen",
    r"(?<!\d)\(\d{3}\)\s*\d{3}-\d{4}\b": "pii:phone_paren",
    r"\b\d{4}-\d{4}-\d{4}-\d{4}\b": "pii:credit_card",
    r"\b\d{10,11}\b": "pii:phone_digits",
}


def apply_pii_rules(content: str) -> Tuple[str, RuleMatchResult]:
    """Apply Tier 1 PII regex rules; redact-in-place with [REDACTED]."""
    result = RuleMatchResult()
    if not content:
        return content, result

    filtered = content
    for pattern, rule_id in _PII_RULE_IDS.items():
        matches = re.findall(pattern, filtered)
        if matches:
            count = len(matches)
            result.matched_rules.append(rule_id)
            result.redactions_count += count
            filtered = re.sub(pattern, REDACTED_TOKEN, filtered)

    return filtered, result


# ============================================================================
# Tier 1 — Secret format rules
# ============================================================================
#
# Patterns for common API key + bearer token + credential-embedded URL
# shapes. Fail-loud (high severity) because secret exposure is operator-
# incident-territory: even partial redaction is dangerous if the
# unredacted half is enough to identify the secret.
#
# Pattern coverage (not exhaustive — first-pass scaffold; extend as new
# secret formats surface):
# - OpenAI keys: sk-... (40+ chars)
# - GitHub tokens: ghp_/gho_/ghu_/ghs_/ghr_... (36+ chars)
# - AWS access keys: AKIA... (20 chars)
# - Generic Bearer tokens: "Bearer ..." in headers/strings
# - URL with embedded credentials: https://user:pass@host/...

_SECRET_RULE_IDS = {
    r"\bsk-[A-Za-z0-9_\-]{20,}\b": "secret:openai_key",
    r"\bgh[pousr]_[A-Za-z0-9]{30,}\b": "secret:github_token",
    r"\bAKIA[A-Z0-9]{16}\b": "secret:aws_access_key",
    r"(?i)\bBearer\s+[A-Za-z0-9._\-=]{20,}\b": "secret:bearer_token",
    r"\bhttps?://[^\s:]+:[^\s@]+@[^\s/]+": "secret:url_credentials",
}


def apply_secret_rules(content: str) -> Tuple[str, RuleMatchResult]:
    """Apply secret-format rules; redact in place with [REDACTED]."""
    result = RuleMatchResult()
    if not content:
        return content, result

    filtered = content
    for pattern, rule_id in _SECRET_RULE_IDS.items():
        matches = re.findall(pattern, filtered)
        if matches:
            count = len(matches)
            result.matched_rules.append(rule_id)
            result.redactions_count += count
            filtered = re.sub(pattern, REDACTED_TOKEN, filtered)

    return filtered, result


# ============================================================================
# Tier 2 — BoundaryEnforcer category check on output
# ============================================================================


async def apply_boundary_rules(content: str, boundary_enforcer) -> RuleMatchResult:
    """Apply BoundaryEnforcer category check to LLM output text.

    Reuses `BoundaryEnforcer.enforce_boundaries(content, ...)` whose
    signature already accepts arbitrary content. If the enforcer flags
    a violation, this rule signals is_violation=True; the caller in
    `OutputFilter.filter` substitutes the canned response.

    Args:
        content: the LLM output (already PII-filtered).
        boundary_enforcer: instance of `BoundaryEnforcer`.

    Returns:
        RuleMatchResult with is_violation set + matched_rules populated.
    """
    result = RuleMatchResult()
    if not content or boundary_enforcer is None:
        return result

    try:
        decision = await boundary_enforcer.enforce_boundaries(
            message=content,
            context={"source": "output_filter"},
        )
    except Exception as exc:  # pragma: no cover — defensive log
        logger.warning("output_filter_boundary_check_failed", error=str(exc))
        return result

    if getattr(decision, "is_violation", False):
        result.is_violation = True
        violation_type = getattr(decision, "violation_type", "unknown")
        result.matched_rules.append(f"boundary:{violation_type}")

    return result
