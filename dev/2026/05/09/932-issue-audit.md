# Audit: #932 against feature.md template

**Issue**: SEC: HIBP integration stub — key leak detection returns false safe result
**Auditor**: Lead Developer
**Date**: 2026-05-09 ~09:05
**Phase**: 1 of 3 (Issue audit) — pre-gameplan gate

---

## TL;DR

**Verdict: ⚠️ Issue is narrow + clear about WHERE/WHAT, but vague about WHICH SERVICE/HOW.** The TODO points at `key_leak_detector.py:92`. The body says "HIBP API integration implemented (or explicit decision to use alternative)." That parenthetical is the load-bearing question.

**1 PM question** before gameplan. (Smaller surface than #933's 4-question audit.)

---

## Audit matrix

| Template Requirement | Status | Notes |
|---|---|---|
| Title + LABEL | ✅ | "SEC: HIBP integration stub..." |
| Priority (P0–P3) | ⚠️ | "Pre-beta" stated; per #933 disposition that = now (M2f) |
| Labels | ✅ | bug, priority: high |
| Milestone | ❌ | Not set; M2f per m2-structure.md |
| Epic / Related | ⚠️ | Should reference #933 (sibling Group A item; #933 reorder gates on this) |
| Problem Statement — Current State | ✅ | Clear: stub at `key_leak_detector.py:92` returns `leaked=False, confidence=0.8` without checking anything |
| Problem Statement — Impact | ✅ | "Users get false assurance about key safety" — accurate |
| Strategic Context | ❌ | Missing. WHY HIBP specifically? HIBP's Pwned Passwords is password-focused; coverage of API-key leaks is uncertain |
| Goal — Primary Objective | ⚠️ | "HIBP API integration" stated, but the parenthetical ("or alternative") leaves the actual choice open |
| Goal — Not In Scope | ❌ | Missing. Likely out-of-scope: GitHub secret scanning, TruffleHog/Gitleaks, custom hash-DB |
| What Already Exists | ⚠️ | Implicit. The local `_quick_leak_checks` (`key_leak_detector.py:112`) already catches: known test keys, weak patterns ("password", "12345", etc.), and obvious fakes (repeated chars, sequential patterns, keyboard patterns). HIBP is filling a NARROWER gap than the body suggests. |
| What's Missing | ❌ | Not articulated against existing |
| Requirements — Phases | ❌ | Missing |
| Acceptance Criteria — Functionality | ⚠️ | "check_key_leaked() returns real results" — vague. What's "real"? HIBP API call? Network failure handling? Rate-limit response? |
| Acceptance Criteria — Testing | ❌ | Missing |
| Acceptance Criteria — Quality | ❌ | Missing |
| Effort Estimate | ❌ | Missing. My read: ~3-5 hr if HIBP path; ~1-2 hr if "decide-not-to-use-HIBP" path with documented rationale |
| Dependencies | ⚠️ | None blocking. Sibling: #933 (reorder agreed: do #932 first per PM) |

---

## The 1 question that blocks gameplan

### Q1: Is HIBP actually the right service, or should we use an alternative (or skip)?

The issue body acknowledges this with "(or explicit decision to use alternative)" — but doesn't decide.

**Three options I see** for the leak-check that the validator's `leak_safe` dimension expects:

#### Option A: Wire HIBP Pwned Passwords API (k-anonymity)

- **What it is**: HIBP's free public API. Hash key with SHA-1, send first 5 chars of hash, get back list of suffix-hashes that matched. Locally check if our full hash is in the list.
- **Pros**:
  - Free, no API key required, well-known service
  - K-anonymity means we never send the actual key
  - Implementation is ~30 lines
- **Cons**:
  - HIBP's Pwned Passwords is **password-focused**. Coverage of API-key-shaped strings (e.g., `sk-...`, `ghp_...`) is uncertain — most leaked OpenAI keys probably aren't in HIBP's dataset
  - We'd be advertising a check that doesn't actually catch most realistic leaks
- **Effort**: ~3 hr (implementation + tests + network-failure handling + retry logic)

#### Option B: Use GitHub secret scanning patterns + local hash DB

- **What it is**: skip HIBP; expand `_quick_leak_checks` with provider-specific known-leak detection. E.g., a small bundled hash-DB of historically-leaked OpenAI/Anthropic/GitHub keys.
- **Pros**: actually catches API-key leaks vs HIBP's password focus; no network dependency; deterministic
- **Cons**: hash DB is small (we'd have to source it); doesn't cover NEW leaks unless we update; still a stub-shaped check vs a real lookup service
- **Effort**: ~2-3 hr (sourcing hash list + integration + tests)

#### Option C: Honest stub with clear API contract — `leak_safe = unknown` semantics

- **What it is**: replace stub-returns-safe with stub-returns-unknown. The validator's `leak_safe` dimension becomes informational, not blocking. Document explicitly that we don't have a real leak DB and aren't pretending to.
- **Pros**:
  - Smallest scope; immediately accurate (no false reassurance)
  - Local checks (`_quick_leak_checks`) still catch test keys / weak patterns / fakes
  - Defers the real solve to a beta-readiness issue when we have a clear leak-detection service
- **Cons**: doesn't ship a NEW capability; just stops lying about an existing one
- **Effort**: ~1-2 hr (rename+rewire + tests + doc)

---

## My recommendation

**Option C — honest unknown semantics.** Reasoning:

1. **Pre-release dev env, no production users**: the threat model "user accidentally stores a known-leaked key" is small. Local checks already catch the common cases (test keys, "password", "12345", obvious fakes). The marginal value of HIBP-on-API-keys against zero alpha testers is ~0.
2. **HIBP coverage of API keys is questionable**: implementing it means advertising a security feature that doesn't actually catch most realistic leaks (sk-, ghp-, etc. probably aren't in HIBP's password-leaked dataset). That's a worse outcome than honest "unknown."
3. **#933 unblocks immediately**: with Option C, leak_safe becomes "unknown" not "false safe." When #933 re-enables validation, format + strength run for real; leak_safe is informational. No half-baked stub-while-enabled state.
4. **Beta-readiness is the right venue for the real solve**: when we know which service / DB we trust (GitHub secret scanning? Custom approach? HIBP?), we file a new issue with concrete scope. Don't pre-commit to HIBP if HIBP isn't the right answer.

**Option B is a reasonable runner-up** if we want a NEW capability now. But it's still a partial solve.

**Option A I'd push back on** unless we have evidence HIBP catches OpenAI/Anthropic/GitHub key leaks meaningfully.

---

## Smaller things I'd want to confirm

- **Q2** (low-stakes): does the validator already treat `confidence=0.8` differently from `confidence=1.0`? If so, current stub may already be hedging correctly via the confidence number. Worth a 5-min code read.

- **Q3** (low-stakes): is there a way for the user to see WHICH check passed/failed in the validation report? If yes, "leak_safe = unknown" needs UI consideration. If no, internal-only and we can land it.

These are not blockers; I can resolve in the gameplan.

---

## Action

Per audit-cascade discipline, surfacing **Q1 (Option A vs B vs C)** for PM disposition before writing the gameplan. Q2 + Q3 I'll resolve myself when drafting.

Once Q1 is answered, gameplan ~15 min.

— Lead Developer, 2026-05-09 ~09:10
