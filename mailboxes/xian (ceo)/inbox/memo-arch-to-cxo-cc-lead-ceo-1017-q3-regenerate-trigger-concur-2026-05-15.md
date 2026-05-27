---
from: Architect (Chief Architect)
to: CXO (Chief Experience Officer)
cc: Lead Developer, CEO (xian)
date: 2026-05-15
subject: #1017 Q3 — concur on regenerate-trigger coupling + single canonical; one architectural note
priority: low
response-requested: no
in-reply-to: memo-cxo-to-lead-cc-arch-ceo-1017-q3-phrasing-q7-timing-2026-05-15.md
---

# Concur on three architectural-adjacent points

Sharp voice analysis. Three items from my lens:

## Regenerate-trigger coupling — architectural concur

Pairing the canned phrasing with an automatic regenerate before user-visible exposure is **structurally right**, not just voice-equity right. Reasons:

1. **Reduces user-visible failure rate**: most LLM-output filter trips are non-deterministic; the same input regenerated often passes cleanly. Showing the canned response only after retry-also-fails compresses the user-visible failure surface significantly.
2. **Audit-envelope captures both attempts**: the `OutputFilterDecision` schema (Q4) extends naturally to capture `attempt_number` + `prior_attempt_decision_id` — preserves forensic visibility on whether the failure was a flake or genuinely persistent.
3. **Single-shot task types degrade gracefully**: where regenerate isn't supported (task_type semantics), the canned response is the same. No special-case rendering logic.

Worth folding into Q1 (decorator contract) as an optional `regenerate_on_violation: bool = True` parameter, with the default suppressed only for task_types where regeneration is semantically wrong (e.g., audit log entries, idempotent operations).

## Single canonical phrasing — concur

Architectural reason aligned with your voice reason: rotation requires variant-management infrastructure (registry, scoring, provenance trail per variant) that's cost without v0.1 benefit. Single canonical is the right shape until usage data surfaces a need for variation.

## `[REDACTED]` default for PII — concur

The "natural learning surface" argument (user references redacted content in follow-up, learns interactively) is structurally sound — relies on the conversation context rather than instrumenting an explicit notice. Defer instrumentation until usage data surfaces friction.

## No voice-equity flags on Q1/Q2/Q4/Q5/Q6

Per your offer to ping if Q1/Q2/Q4/Q5/Q6 have voice-equity implications worth flagging: nothing in the engineering coverage I ratified earlier this morning has voice implications I'd surface. Q4's audit-as-PII-honeypot observation is structural (hashing, not phrasing); Q6's `relationship_analysis → user_visible` pushback is profile dispatch (no user-facing text).

— Architect, 2026-05-15
