# Audit: #933 against feature.md template

**Issue**: SEC: API key validation disabled for alpha — no re-enable plan
**Auditor**: Lead Developer
**Date**: 2026-05-09 ~08:20
**Phase**: 1 of 3 (Issue audit) — pre-gameplan gate

---

## TL;DR

**Verdict: ⚠️ Issue is under-specified relative to template; minor bug-shape exception applies.** The issue clearly identifies WHERE (one file, one line, one flag) and WHAT (re-enable validation) but lacks Strategic Context, Effort Estimate, Phases, Testing Strategy. For a 1-flag-flip + tests change, full template compliance is overkill — but a few gaps DO matter for the gameplan: re-enable trigger criterion, validator dependency status (was disabled "for alpha onboarding format validator issues" — are those issues still present?), and rollback plan.

**Recommendation**: proceed to gameplan with 4 explicit clarifications surfaced inline (not requiring issue rewrite). Doc the answers in the gameplan.

---

## Audit matrix

| Template Requirement | Status | Notes |
|---|---|---|
| Title + LABEL | ✅ | "SEC: API key validation disabled for alpha — no re-enable plan" |
| Priority (P0–P3) | ⚠️ | Body says "Pre-beta" — translates to P1 or P2 depending on alpha-vs-beta gating; clarify |
| Labels | ✅ | bug, priority: high |
| Milestone | ❌ | Not set on issue; M2f per m2-structure.md |
| Epic / Related | ❌ | Should reference: M2f sub-epic, Issue #228 (CORE-USERS-API Phase 1C — original feature), Issue #268 (where validator was added), Issue #485 (validation-only mode) |
| Problem Statement — Current State | ✅ | Clear: `skip_validation = True` at `user_api_key_service.py:76` (now 77 in current code) |
| Problem Statement — Impact | ⚠️ | "Pre-beta" stated but no enumeration of: who's affected (alpha users storing keys), what risk is being deferred (format/leak/entropy weaknesses unchecked), what attack surface this opens |
| Strategic Context | ❌ | Missing. Why was alpha onboarding's format-validator issue more important than security validation? Is that trade-off still in force? |
| Goal — Primary Objective | ⚠️ | Implicit ("re-enable validation") but no success-state articulation |
| Goal — Example UX | N/A → ⚠️ | For a security/internal change, UX is "user sees same flow but invalid keys are now rejected with appropriate error." Worth stating. |
| Goal — Not In Scope | ❌ | Missing. Likely out-of-scope: HIBP integration (#932 separate), key rotation, multi-key per provider |
| What Already Exists | ⚠️ | Implicit — `APIKeyValidator` exists at `services/security/api_key_validator.py`; should reference. Format validator + entropy strength + leak-safe checks are wired but bypassed. |
| What's Missing | ⚠️ | The original "format validator issues" cause — needs investigation. Were specific providers failing the format check at alpha onboarding? Is that still true? |
| Requirements — Phases | ❌ | Missing. Feature template wants Phase 0 (Investigation) → Phase 1+ → Phase Z. Audit-cascade discipline requires phasing. |
| Acceptance Criteria — Functionality | ⚠️ | "Re-enable validation with appropriate error handling" — vague. Should specify: what are the validator's three checks, which return error vs warning, what user-facing message |
| Acceptance Criteria — Testing | ❌ | Missing entirely |
| Acceptance Criteria — Quality | ❌ | Missing |
| Acceptance Criteria — Documentation | ⚠️ | "TODO comment removed" — partial; should also mention updating any docs that reference the disabled state |
| Completion Matrix | ❌ | Missing |
| Testing Strategy | ❌ | Missing — should include: unit test that `skip_validation=False` invokes validator; integration test that invalid key formats raise ValueError; manual test that valid keys still pass |
| Success Metrics | ❌ | Missing — for security work, metrics like "0 invalid-format keys stored after re-enable" |
| STOP Conditions | ❌ | Missing — e.g., STOP if validator throws unexpected exception type, STOP if existing alpha-stored keys would be invalidated |
| Effort Estimate | ❌ | Missing. My read: ~2 hours (small) — flag flip + add 2-3 tests + verify alpha-stored keys still pass + update TODO comment |
| Dependencies — Required | ❌ | Missing — none I can see (validator already exists; no other issue blocks this) |
| Dependencies — Related | ⚠️ | Should reference #932 (HIBP — sibling Group A item) explicitly |
| Rollback Plan | ❌ | Missing — for a security-tightening change: if alpha users can't store keys post-re-enable, flip flag back, file regression issue, surface to PM same day |

---

## Gaps that BLOCK gameplan-writing

Most of the missing template sections (Completion Matrix, Success Metrics, etc.) are appropriate for larger features and overkill for a 1-flag-flip. But these 4 questions DO need answers before the gameplan:

### Q1: What were the original "format validator issues"?

The TODO comment says "TEMPORARILY DISABLED for alpha onboarding (format validator issues)". Need to understand what was breaking — if specific providers (OpenAI? Anthropic? GitHub?) had format patterns that were too strict, just re-enabling would re-break alpha. Investigation step needed: read the validator's per-provider format patterns and compare to known-good keys from current alpha users.

### Q2: When does PM want this re-enabled?

The body says "Pre-beta" but M2f doesn't have an explicit beta-gate scheduled. Is this:
- (a) Re-enable now as part of M2f Group A (treat as "no longer alpha-onboarding")?
- (b) Wait until a specific milestone (beta-readiness gate)?
- (c) Re-enable conditionally — keep flag for environments still onboarding, default-on for production?

### Q3: What about existing alpha-stored keys?

If users have already stored API keys with `skip_validation=True`, those keys are in the keychain. Re-enabling validation only affects NEW key stores. Should we:
- (a) Leave existing keys alone (status quo, post-re-enable only new keys validated)
- (b) Bulk-revalidate at startup (potentially invalidates existing keys → user lockout risk)
- (c) Re-validate at next-use (lazy validation, user gets error when API call fails downstream)

### Q4: Confirm not-in-scope: #932 HIBP integration

#933 = format/strength/leak validator re-enable. #932 = HIBP integration stub. The validator's `leak_safe` check uses #932's stub. Should #933 re-enable include or exclude leak_safe? My read: re-enable format + strength but keep leak_safe stubbed (returns "safe") until #932 ships, since flipping leak_safe on against a stubbed-true detector achieves nothing. Confirm.

---

## Action

Per audit-cascade discipline, I should not proceed to gameplan with these 4 unresolved questions. **Surfacing for PM disposition.** None of them are template-N/A — all 4 are real decisions PM owns.

Once answered, gameplan can proceed. Estimated gameplan-write time after answers: ~20 min.

— Lead Developer, 2026-05-09 ~08:25
