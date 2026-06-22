## Problem Statement

The `tests/security/` suite (e.g. `tests/security/test_user_api_key_service.py`) **does not execute in any gating CI job**. A pre-existing fixture bug there set `User.id` to a 45-char string against the UUID `users.id` column (#262), leaving the entire file silently red against a real Postgres — but CI never caught it, because CI never runs that file. The bug was found by hand during #358 and fixed in `99299f6f1`.

Surfaced by: #358 (encryption-at-rest). Related: #1224 (pre-existing test failures), #1253 (CI ruff gate red cohort-wide).

## Evidence — how `tests/security/` falls through every net

**No workflow targets it.** `grep -rn "tests/security" .github/workflows/` → zero hits.

**The two workflows that would collect it via broad `pytest tests/` never reach it:**

1. **`test.yml` (Tests)** — the full-suite job (`Full Test Suite`, runs `pytest tests/ -m "not llm"`) `needs: smoke-tests`. The `smoke-tests` job runs `pytest -m smoke`, which must first *collect* all of `tests/`; collection hits `tests/load/test_cache_effectiveness.py:15` → top-level `from .setup_real_system import ...`, but `tests/load/setup_real_system.py` **does not exist** → `ModuleNotFoundError` at collection. With `pytest.ini` `addopts = -x --maxfail=1`, the session aborts during collection (0 tests run). Result on run 27883152229: `Smoke Tests = failure`, `Full Test Suite = skipped`. **The security tests never run.**

2. **`ci.yml` (CI)** — the Linux `test` job dies at the **"Configuration Validation Test"** step (`❌ Invalid configuration incorrectly accepted` → exit 1: the config validator now *accepts* a config the test expects it to reject) — **before** the `Run tests` step (`pytest tests/ || echo "No tests found"`) ever executes. Even if it ran, `|| echo` swallows any failure (step would report green regardless), and there is no Postgres service, so DB tests would error on connect. Result on run 27883152253: Linux `test = failure`, plus the Windows job fails at `actions/checkout` (`invalid path 'dev/2025/11/10/3.'`).

**The only workflow with a real Postgres never includes it.** `e2e-aaxt.yml` provisions `postgres:16` on 5433 and runs `alembic upgrade head`, but executes only targeted paths: `tests/e2e/test_task_lifecycle_e2e.py`, `tests/e2e/test_canonical_conversations.py`, `tests/aaxt/`. It does **not** run `tests/security/`.

**Why the failure is invisible:** `main` has **no required status checks** (branch-protection JSON has no `required_status_checks` key) and `required_approving_review_count: 0`. CI has been **uniformly red on every recent push to `main`** (Tests + CI both `failure` for the last 8+ runs) for the three unrelated reasons above. A signal that is always red carries no information — new breakage is indistinguishable from old breakage, and nothing blocks the merge either way.

## Why It Matters

Encryption-at-rest (#358) and the multi-user key-isolation guarantees in `tests/security/` are exactly the kind of security-critical invariants that must not regress silently. Right now a fully-red security suite merges to `main` with zero friction. This is the "broken windows" / alarm-fatigue failure mode: the alarm is on, but it's been ringing so long nobody hears it.

## Proposed Remediation (options — not pre-decided; PM/Lead Dev to scope/split)

1. **Run `tests/security/` against Postgres in a gating job.** Add a Postgres-backed job (copy `e2e-aaxt.yml`'s `services: postgres` + `alembic upgrade head`) that runs `pytest tests/security/`. This is the direct fix for the PM's question.
2. **Un-break the smoke gate.** Fix `tests/load/test_cache_effectiveness.py` (+ `test_sequential_load.py`) — restore/replace the missing `tests/load/setup_real_system` module, or guard the import so a missing load-test helper can't abort collection of the whole suite. Consider dropping `-x --maxfail=1` from the *full-suite* CI run so one broken import doesn't mask everything (keep it for fast local smoke if desired).
3. **Stop swallowing failures in `ci.yml`.** Remove `|| echo "No tests found"` from the `Run tests` step; fix or update the "Configuration Validation Test" step (config-validator behavior drifted vs. the test's expectation).
4. **Make at least one core test job a required status check on `main`** so red CI actually blocks merges. Without this, fixes #1–3 still don't *gate* anything.
5. (Adjacent) Windows checkout is broken by `dev/2025/11/10/3.` (trailing-dot path illegal on Windows) — rename/remove that path so `ci.yml`'s Windows job can even check out.

Items 1–3 make the security suite *run and report truthfully*; item 4 makes it *gate*. Recommend at minimum 1 + 4 to close the literal gap the PM raised, with 2/3/5 as the broader CI-hygiene cleanup (coordinate with #1224 / #1253).

## Acceptance Criteria

- [ ] `tests/security/` executes against a real Postgres in a CI job on push/PR to `main`
- [ ] That job is a **required status check** on `main` (or explicit PM decision to defer gating, recorded)
- [ ] A deliberately-broken security test demonstrably turns the job red (and blocks merge, if gating enabled)
- [ ] Smoke gate no longer aborts on the `tests/load/setup_real_system` import (or full-suite run decoupled from it)
- [ ] Decision recorded on `ci.yml`'s `|| echo` swallow + config-validation step
