# Gameplan: #933 — Re-enable API key validation

**Issue**: SEC: API key validation disabled for alpha — no re-enable plan
**PM Disposition (2026-05-09)**: re-enable now (pre-beta = MVP→0.9 trajectory). Leave existing alpha-stored keys alone (no bulk-revalidation). Re-enable all 3 checks (format + strength + leak); leak now uses #932's honest-unknown semantics so it's informational, not blocking. PM 09:13 + 09:25.
**Auditor**: Lead Developer
**Date**: 2026-05-09 ~10:30
**Phase**: 2 of 3 (Gameplan) — pre-implementation gate
**Audit-cascade reference**: `dev/2026/05/09/933-issue-audit.md`
**Sibling**: #932 shipped (commit `c9591108`); leak_safe is now informational
**Branch**: `claude/933-reenable-key-validation` (worktree at `../piper-morgan-product-933` per branch-worktree-discipline)

---

## Phase -1: Infrastructure verification

**Work characteristics**: Single-file backend change (1-line flag flip + small message tidy) + test-fixture updates across multiple test files + new unit tests for the active-validation path. Pre-release dev env, no production users. No frontend, no migrations, no integration with new services.

**Phase 0.5/0.6/0.7/0.8 — N/A** (same shape as #932; PM pre-approved this skip pattern for the M2f Group A pair). No UI, no data flow change, no conversation, no completion side effects.

**Phase -1 verification**:
- ✅ Issue exists (#933)
- ✅ Disposition recorded (PM 09:13 / 09:25)
- ✅ Sibling #932 shipped (leak_safe=informational, not blocking)
- ✅ Working in worktree (`piper-morgan-product-933`); no cross-agent collision risk
- ✅ Audit-cascade Phase 1 done (`dev/2026/05/09/933-issue-audit.md`)

---

## Phase 0: Investigation — DONE

### What was investigated

The TODO comment at `services/security/user_api_key_service.py:75-77` reads:

```python
# TEMPORARILY DISABLED for alpha onboarding (format validator issues)
# TODO(#933): Re-enable after alpha onboarding complete
skip_validation = True  # Set to False to re-enable
```

The "format validator issues" reference unspecified breakage. Investigation goal: identify what was breaking before flipping the flag.

### Finding: the original cause is GONE

Git history shows the format-validator issues were **fixed Oct 30, 2025** in commit `214f4afe`:

> *"fix(security): Update OpenAI key format validation for new key types — OpenAI now issues project-scoped keys (sk-proj-...) and service account keys with different formats than the legacy sk-... pattern. Increased max length from 60 to 200 chars (project keys are longer). Decreased min length from 50 to 20 (more flexible). Updated regex to allow hyphens and underscores in key body. This fixes wizard validation errors when using modern OpenAI API keys."*

The bypass remained in place but the root cause was addressed 6+ months ago. **Re-enabling validation is safe at the production-code level.**

### Secondary finding: test fixtures need updating

Existing tests use obviously-test-shaped key strings that would trigger the leak detector's `_quick_leak_checks` once the flag flips:

| File | Fixture | Why it'd fail |
|---|---|---|
| `tests/security/integration_test_api_key_audit_logging.py:107` | `sk-test-key-12345` | Contains weak pattern `12345` → `severity="critical"` |
| `tests/security/integration_test_api_key_audit_logging.py:166` | `sk-test-key-updated` | Likely matches known-test-keys |
| `tests/security/integration_test_api_key_audit_logging.py:208` | `sk-test-key-rotated` | Likely matches known-test-keys |
| `tests/security/test_key_storage_validation.py:207` | `sk-test-demo-key-12345` | Contains weak pattern + matches test-keys |
| `tests/security/test_key_storage_validation.py:292` | `sk-proj-1234567890abcdefghijklmnopqrstuvwxyz` | Contains weak pattern `1234567890` |
| `tests/integration/test_setup_wizard_flow.py` | TBD — needs scan | Likely similar |
| `tests/integration/test_fresh_install_flow.py` | TBD — needs scan | Likely similar |
| `tests/unit/web/api/routes/test_setup_notion.py` | TBD — needs scan | Likely similar |

These tests assume `skip_validation=True` (they pass without a real validator running). After the flag flip, they'll fail at the validator's leak-check before reaching their actual assertions.

### Strategy options

**(a) Update test fixtures to use validator-passing strings** — generate realistic-looking but synthetic keys (no weak patterns, no known-test-key matches, sufficient entropy). Tests would test the real validation path.

**(b) Keep test fixtures, pass `validate=False` in test calls** — wait, `validate` param is for provider-API validation; `skip_validation` is a separate flag for the format/strength/leak validator. Need a different bypass mechanism for tests.

**(c) Add a per-call `skip_security_validation` parameter** — let tests opt-out cleanly. Production callers default to security-validation-on.

**Recommendation**: (a) for most tests (they're testing storage/audit paths and synthetic keys serve fine) + (c) for tests that specifically need to test "what happens when validation REJECTS a key" — but for those we want to PASS in a known-bad key and assert ValueError.

Actually simpler: **(a) only**. If a test specifically wants to test rejection, it should pass a known-bad key and assert ValueError. The current tests that use bad-shaped keys aren't testing rejection — they're testing audit/storage paths and need replacement fixtures.

---

## Phase 1: Flip the flag + tidy message (~10 min)

In `services/security/user_api_key_service.py`:

```python
# OLD (lines 75-77):
# Validate key security before storage (Issue #268)
# TEMPORARILY DISABLED for alpha onboarding (format validator issues)
# TODO(#933): Re-enable after alpha onboarding complete
skip_validation = True  # Set to False to re-enable

if not skip_validation:
    try:
        validation_report = await self._validator.validate_api_key(provider, api_key)
        ...

# NEW:
# Validate key security before storage (Issue #268).
# #933 May 9 2026: re-enabled. The original bypass was for "format
# validator issues" — those were fixed Oct 30 2025 in commit 214f4afe
# (OpenAI sk-proj-* support). #932 made leak_safe informational, so the
# validator no longer falsely-blocks on a leak check we didn't perform.
try:
    validation_report = await self._validator.validate_api_key(provider, api_key)
    ...
```

Remove the `skip_validation` flag and the `if not skip_validation:` guard; validation runs unconditionally. The existing exception-handling around the validate call already covers ValueError + unexpected exceptions.

**No production behavior change for keys that would have passed**: format check + strength check are the gates; leak_safe is informational per #932 (only blocks when quick-checks find an obvious problem with confidence ≥ 0.9).

---

## Phase 2: Update test fixtures (~1.5 hr)

### Approach

Generate synthetic test keys that:
- Match the provider's format pattern (e.g., `sk-` prefix + 20+ chars for OpenAI)
- Have sufficient entropy (no repeated chars, no sequential runs, no keyboard patterns)
- Don't contain weak patterns (`password`, `12345`, `qwerty`, etc.)
- Aren't in `_load_known_test_keys()` (so they don't trigger known-test-key path)

Example fixture: `sk-X7k9mP2nQ5tR8wY3jL6hN4vC1bM0sD9fG8eA7zK5x2W4uT` (already used in #932's tests; passes all quick-checks).

### Files to update

For each file in the table above, replace test-shaped keys with synthetic-realistic keys. Verify each test still asserts what it's meant to assert (e.g., audit logging captures key preview correctly with the new fixture).

### How to verify

For each test file: run before-and-after to confirm:
- Before flag-flip + old fixtures: tests pass (current state)
- After flag-flip + new fixtures: tests still pass (test target unchanged)
- After flag-flip + OLD fixtures: tests fail at validator (confirms our hypothesis)

Subagent task — see Phase 3.

---

## Phase 3: Tests for the active-validation path (~1 hr) — subagent

After Phase 1+2 land, deploy subagent to:

1. **Add new unit tests** in `tests/security/test_user_api_key_service.py` (or new dedicated file) covering:
   - `test_store_user_key_validates_format` — invalid format → ValueError raised, no DB write, no keychain write
   - `test_store_user_key_validates_strength` — low-entropy key → ValueError, no write
   - `test_store_user_key_blocks_known_test_key` — known-leak quick-check fires → ValueError
   - `test_store_user_key_passes_unknown_leak` — passes format + strength, leak=unknown → key stored successfully (load-bearing for #932 honest-unknown integration)
   - `test_store_user_key_audit_logs_validation_failure` — validation failure path is audit-logged

2. **Run the full security test suite + storage suite + integration suites for setup**:
   - `pytest tests/unit/services/security/ -v`
   - `pytest tests/security/ -v`
   - `pytest tests/integration/test_setup_wizard_flow.py tests/integration/test_fresh_install_flow.py -v`

3. **Verify** no new failures vs current baseline (some existing fails in security suites are pre-existing DB-fixture issues — confirmed in #932's verification).

---

## Phase Z: Verification + handoff (~15 min)

1. **Smoke**: in dev shell, attempt `store_user_key` with a real-shape OpenAI key (synthetic) — confirm validation report is generated and key stores. Attempt with `sk-test-12345` — confirm ValueError raised.

2. **Update issue evidence comment on #933**: tests-passed counts, file:line references, smoke transcript.

3. **Cross-reference**: comment on #932 + the original #228 (CORE-USERS-API Phase 1C) noting the re-enable shipped.

4. **Branch sign-off**: merge to main with `--no-ff`. Worktree cleanup deferred to PM ratification.

---

## Acceptance criteria

- [ ] `skip_validation` flag and bypass removed from `user_api_key_service.py`
- [ ] Comment block updated to reflect history (Oct 30 fix + #932 + #933 re-enable)
- [ ] All test files in Phase 2 table updated with synthetic-realistic fixtures
- [ ] 5 new unit tests in Phase 3 added and passing
- [ ] Full security/storage/setup-integration suites pass (modulo pre-existing DB-fixture failures verified pre-merge)
- [ ] Smoke test confirms validation runs for new key stores; existing keys unaffected

---

## STOP conditions

- Test-fixture sweep reveals a test that genuinely needs to test "validation REJECTS a key" path with the current fixtures (rare; surface to PM if found)
- A new failure mode appears that's caused by re-enabling validation, not by stale fixtures (e.g., a real provider whose format pattern is too strict against actual valid keys → would mean the Oct 30 fix wasn't comprehensive)
- The full security suite shows >5 NEW failures (vs baseline) → over budget; surface to PM

---

## Effort estimate

**Total: ~3 hours**

- Phase 0 (investigation): DONE (~30 min)
- Phase 1 (flag flip + comment): 10 min
- Phase 2 (test fixtures): 1.5 hr
- Phase 3 (new unit tests + suite verification, subagent): 1 hr
- Phase Z (verify + handoff): 15 min

---

## Audit-cascade self-check

| Template Requirement | Status |
|---|---|
| Phase -1 Infrastructure | ✅ (Phase 0.5/0.6/0.7/0.8 N/A pattern from #932 carries forward) |
| Phase 0 Investigation | ✅ DONE inline |
| Phases 1-N Development | ✅ (Phase 1 + 2 + 3) |
| Test Strategy | ✅ |
| Phase Z Handoff | ✅ |
| Acceptance Criteria | ✅ |
| STOP Conditions | ✅ |
| Effort Estimate | ✅ |
| Dependencies | ✅ (none — #932 shipped) |
| Reference to issue | ✅ |
| Reference to audit memo | ✅ |
| Reference to PM disposition | ✅ |

---

## Action

Surfacing the **Phase 2 fixture-update scope** for PM awareness. The 1-line flag flip is paper-cut sized; the test-fixture sweep is the larger half of the work. I propose:

- I do Phase 1 directly (flag flip, ~10 min)
- I do Phase 2 directly (fixture sweep — need close eyes on each test's intent, not a pure mechanical change)
- Subagent does Phase 3 (new unit tests + full verification sweep) — same pattern as #932

Confirm approach + I proceed.

— Lead Developer, 2026-05-09 ~10:35
