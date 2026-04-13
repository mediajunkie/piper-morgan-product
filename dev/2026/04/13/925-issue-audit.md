# Audit: #925 against bug_report_alpha.md

Note: #925 is an enhancement (floor migration), not a bug. Auditing against the feature template's relevant criteria.

| Requirement | Status | Notes |
|-------------|--------|-------|
| Problem statement | ✅ | STATUS/PRIORITY use canonical handlers with template responses |
| Expected behavior | ✅ | Floor-first with context assembly for natural LLM responses |
| Current state | ✅ | Both return True from _requires_canonical_handler |
| Evidence of need | ✅ | #962 inversion sweep identified these as the keystone |
| Acceptance criteria | ⚠️ | Need to add: retest scores must remain ≥7 (current baseline 9/9) |
| Scope | ⚠️ | Issue includes Phase 4 (greeting refactor) — PM approved deferring greeting per ADR-059. Focus on Phase 3 only. |

## Scope Decision

Phase 3 (STATUS + PRIORITY floor migration) — proceed.
Phase 4 (greeting refactor) — defer. Greeting stays canonical per existing decision (calendar side effects, onboarding on ice per ADR-059).

## Key Investigation Finding

Q11-14 and Q21 already score 9/9 via floor in the Apr 12 canonical retest. The safety net is already rerouting generic canonical responses to floor. This migration formalizes that behavior and eliminates the unnecessary canonical → safety-net → floor roundtrip.

## Audit Result

Proceeding with Phase 3 only. TDD approach. PRIORITY first (simpler), then STATUS.
