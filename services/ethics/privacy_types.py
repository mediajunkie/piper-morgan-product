"""Privacy-level + filter-reason typed catalog for KG node operations (#1089).

These enums govern the three-level privacy semantics ratified during the
2026-05-17 Phase 0 design substrate (HOST Q2 + Architect Q3+Q4 + CIO Q5 +
PM Q1 ratification ship-now 2026-05-20).

The catalog lives in `services.ethics` alongside `BoundaryType` and
`BoundaryDecision` because privacy filtering rides on the existing boundary-
enforcer infrastructure — `BoundaryEnforcer.check_inappropriate_content` and
`check_harassment_patterns` are the predicates that drive PrivacyLevel-
dependent filtering / redaction / rejection decisions.

Per CIO Q5 disposition, `PrivacyLevel` is Pattern-072's 5th independent
instance (typed catalog of behavior-deciding entries dispatched at
consumption — same shape as `task_type`, `safe_surface()`, probe registry,
index declarations). This file is the catalog; `KnowledgeGraphService`
methods (extended in subsequent increments) are the dispatch site.

Cross-references:
- #1089 KG-PRIVACY-FILTER tracking issue
- HOST Q2 reply (privacy_level semantics + filter_reason refinement):
  `mailboxes/lead/read/memo-host-to-lead-cc-ceo-arch-cio-exec-pa-1089-privacy-level-semantics-trust-lens-2026-05-17.md`
- Architect Q3+Q4 reply (write-path-first + kg_boundary_enforcer placement):
  `mailboxes/lead/read/memo-arch-to-lead-cc-host-cio-ceo-exec-pa-1016-epic-status-plus-1089-q3-q4-architect-input-2026-05-17.md`
- CIO Q5 reply (Pattern-073 instance 11 + Pattern-072 instance 5):
  `mailboxes/lead/read/memo-cio-to-lead-cc-ceo-arch-host-exec-pa-1089-q5-pattern-073-fifth-instance-plus-concurs-2026-05-17.md`
"""

from enum import Enum


class PrivacyLevel(str, Enum):
    """Three-level privacy filtering for KG node operations.

    Read behavior + write behavior + audit-trail behavior vary by level
    (full matrix in the #1089 issue body's "Ratified design" section).

    `str`-mixin makes values JSON-serializable + comparable to plain strings
    so callers can pass `"standard"` if they prefer the literal over the enum
    member (mirrors the pattern used by HTTP status codes / standard library
    enums elsewhere).
    """

    PUBLIC = "public"
    """No filtering on reads or writes. No special audit logging.

    Use when content is known-clean (e.g. system-generated nodes, test
    fixtures, content sourced from already-validated channels).
    """

    STANDARD = "standard"
    """Default level. Reads return flagged nodes with content REDACTED
    (`[FILTERED]` markers); IDs surface so graph structure is preserved.
    Writes of flagged content save with `is_filtered=True` flag + redacted
    content. Filtered-write events log to `EthicsAuditLog`.

    Use as the default for any KG access where the source of the content
    isn't pre-validated — typically all user-facing or LLM-touched paths.
    """

    STRICT = "strict"
    """Reads EXCLUDE flagged nodes entirely (not even ID surfaced). Writes
    of flagged content are REJECTED (raise + log). Rejected-write events
    log to `EthicsAuditLog`.

    Use for high-trust contexts (admin audit views, compliance reports,
    cohort-shared surfaces) where even the structural presence of flagged
    content would compromise the surface.
    """


class FilterReason(str, Enum):
    """Why a node was filtered / redacted / rejected.

    Per HOST Q2 refinement: audit log surfaces filter *category* without
    exposing filtered *content* (category-not-content discipline). The enum
    values document the predicate that fired, not the offending text.

    Open-set by design: new reasons can be added as the boundary-enforcer
    grows (e.g. PII detection, schema-violation gating). Each addition is
    a one-line change here + a corresponding `BoundaryEnforcer` predicate.
    """

    HARASSMENT_PATTERN_MATCHED = "harassment_pattern_matched"
    """`BoundaryEnforcer.check_harassment_patterns` returned True."""

    INAPPROPRIATE_CONTENT_MATCHED = "inappropriate_content_matched"
    """`BoundaryEnforcer.check_inappropriate_content` returned True."""

    BOUNDARY_PRINCIPLE_VIOLATION = "boundary_principle_violation"
    """Reserved for future expansion per HOST Q2: broader principle-level
    boundary violations beyond pattern-matching (e.g. PII surfaces, schema
    gating). Not yet wired into a predicate; placeholder for the open-set
    framing HOST surfaced."""


__all__ = ["PrivacyLevel", "FilterReason"]
