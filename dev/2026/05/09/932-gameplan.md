# Gameplan: #932 — Honest "unknown" semantics for leak_safe

**Issue**: SEC: HIBP integration stub — key leak detection returns false safe result
**PM Disposition (2026-05-09)**: **Option C — honest "unknown" semantics**. Replace stub-returns-safe with stub-returns-unknown. Document explicitly that we don't have a real leak DB. Local quick-checks (test keys / weak patterns / fakes) keep working unchanged.
**Auditor**: Lead Developer
**Date**: 2026-05-09 ~09:15
**Phase**: 2 of 3 (Gameplan) — pre-prompts gate
**Audit-cascade reference**: `dev/2026/05/09/932-issue-audit.md`

---

## Phase -1: Infrastructure Verification

**Work characteristics**: Single-file backend change + small test additions. Pre-release dev env, no production users. No frontend, no migrations, no integration with new services. Standard audit-cascade discipline applies but Phase 0.5 (frontend), 0.6 (data flow), 0.7 (conversation), 0.8 (post-completion side effects) are **N/A** because this is a contained backend change.

**Requesting PM N/A approval for**: Phase 0.5, 0.6, 0.7, 0.8 (they don't apply to a stub-rewrite + validator-tweak with no UI / no data flow / no conversation / no completion side-effects).

**Phase -1 verification**:
- ✅ Issue exists (#932)
- ✅ Disposition recorded (Option C, PM 2026-05-09 09:13)
- ✅ Audit-cascade Phase 1 done (`dev/2026/05/09/932-issue-audit.md`)
- ✅ No worktree collision risk: 1 file in `services/security/`, 1 file in `services/security/`, 1 test file
- ✅ Sibling #933 reorder agreed: this lands first

---

## Phase 0: Investigation (~15 min)

### Read

- `services/security/key_leak_detector.py` (231 lines) — current stub at line 92
- `services/security/api_key_validator.py` — how `leak_safe` participates in `overall_valid` (line 91, 94, 214)
- Any callers of `LeakCheckResult` fields (`severity`, `confidence`, `leaked`)

### Confirm

- The stub-path is the only path returning `leaked=False` non-deterministically (check `_quick_leak_checks` and `_is_obviously_fake` for false-leak-paths)
- The validator's `leak_safe = not leak_result.leaked` (line 91) and `overall_valid = format_valid and strength_acceptable and leak_safe` (line 94) are the only places `leak_safe` is consumed downstream
- No external API depends on the current "0.8 confidence stub-returns-safe" behavior

### STOP if

- Multiple callers depend on the current stub returning `leak_safe=True` to pass validation → surface to PM
- Validator's `overall_valid` logic is more complex than the linear AND chain → adapt design

---

## Phase 1: Honest "unknown" semantics in `key_leak_detector.py` (~30 min)

### What changes

Replace stub at line 92–100. New behavior:

- When `_quick_leak_checks` returns leak-safe (no obvious problem detected in local checks)
- AND we have not implemented a real leak DB lookup yet
- → return a `LeakCheckResult` that signals **"we didn't actually check"** rather than **"safe"**

### Specific change

```python
# OLD (lines 92-100):
# TODO(#932): Implement actual HIBP integration
# Returns false safe result until implemented — tracked as security issue
return LeakCheckResult(
    leaked=False,
    source=None,
    severity="ok",
    recommendation=None,
    confidence=0.8,  # Lower confidence without full check
)

# NEW:
# #932 honest semantics: no real leak-DB lookup wired yet. Returning
# "unknown" rather than "safe" so the validator's overall_valid doesn't
# depend on a check we didn't perform. Local quick-checks above still
# catch test keys, weak patterns, and obvious fakes — those return
# leaked=True with high confidence as before.
return LeakCheckResult(
    leaked=False,
    source=None,
    severity="unknown",
    recommendation="Leak-DB lookup not yet implemented; key passes local quick-checks only.",
    confidence=0.0,
)
```

**Note**: `severity="unknown"` is a new value. Existing values are `'ok'`, `'warning'`, `'critical'`. Add `'unknown'` to the docstring on the dataclass.

---

## Phase 2: Validator treats "unknown" as informational, not blocking (~20 min)

### What changes

In `services/security/api_key_validator.py`:

- The current `overall_valid = format_valid and strength_acceptable and leak_safe` (line 94) treats leak_safe as a blocking gate. Under "honest unknown" semantics, when we didn't check, we shouldn't fail the key.

### Specific change

```python
# OLD (around line 91-94):
leak_safe = not leak_result.leaked
# ...
overall_valid = format_valid and strength_acceptable and leak_safe

# NEW:
leak_safe = not leak_result.leaked
leak_check_performed = leak_result.confidence > 0.0
# When the leak check wasn't actually performed (confidence=0.0), don't
# let it gate overall_valid — informational only. When it WAS performed
# (e.g., local quick-checks found a problem, returning confidence>=0.9),
# leak_safe gates as before.
overall_valid = format_valid and strength_acceptable and (
    leak_safe if leak_check_performed else True
)
```

The user-facing report still shows `leak_safe` and a low-confidence warning (line 214 already does this). The `severity="unknown"` propagates so consumers can distinguish "checked and safe" from "didn't check."

---

## Phase 3: Tests (~40 min)

### Unit tests to add

In `tests/unit/services/security/test_key_leak_detector.py` (or wherever existing tests live):

1. **`test_check_key_leaked_returns_unknown_for_unrecognized_key`**: pass a key that doesn't trigger any quick-check (random valid-looking format). Assert: `leaked=False`, `severity="unknown"`, `confidence=0.0`, recommendation references "not yet implemented."

2. **`test_check_key_leaked_returns_critical_for_known_test_key`**: pass a known test key (from `_load_known_test_keys`). Assert: `leaked=True`, `severity="critical"`, `confidence>=0.9` (existing behavior preserved).

3. **`test_check_key_leaked_returns_critical_for_weak_pattern`**: pass a key containing "password" or "12345". Same shape as #2.

In `tests/unit/services/security/test_api_key_validator.py` (or equivalent):

4. **`test_overall_valid_unaffected_by_unknown_leak_check`**: provide a key that passes format + strength but gets `leak_result.confidence=0.0`. Assert: `overall_valid=True`. **This is the load-bearing test for Option C.**

5. **`test_overall_valid_blocks_on_known_leak`**: provide a key that fails leak check with confidence=1.0 (e.g., from quick-checks). Assert: `overall_valid=False`.

### Existing tests to verify don't break

- Anything calling `KeyLeakDetector.check_key_leaked()` without expecting `severity="unknown"` — there shouldn't be any tests asserting `severity="ok"` for unknown keys, but verify
- Any test asserting `leak_safe=True` for arbitrary keys — was relying on the stub's permissive default

---

## Phase Z: Verification + handoff (~15 min)

### Required actions

1. **Run security test suite**: `pytest tests/unit/services/security/ -v`
2. **Run broader test sweep for callers**: `pytest tests/ -k "leak or validator or api_key" -v` (catches indirect callers)
3. **Smoke test**: store a fake key via `UserAPIKeyService.store_user_key` with `validate=True` (in dev shell) — verify `validation_report` shows `severity="unknown"` for leak; format + strength results unchanged
4. **Update issue**: post evidence comment to #932 with: tests-passed counts, file:line references, smoke-test transcript
5. **Cross-reference #933**: comment on #933 noting #932 landed and unblocks the simple flag flip

### Acceptance criteria

- [ ] `LeakCheckResult` no longer claims `severity="ok"` for keys that weren't actually leak-checked
- [ ] `severity="unknown"` value documented in `LeakCheckResult` dataclass docstring
- [ ] `overall_valid` is no longer gated by an unperformed leak check
- [ ] All new unit tests pass
- [ ] No regression in existing security-suite tests
- [ ] Smoke test shows the validation report distinguishes "unknown" from "safe"
- [ ] TODO comment at `key_leak_detector.py:92` updated/removed (now reflects intentional honest semantics, not aspirational HIBP wiring)

---

## STOP Conditions

- New unit tests fail in unexpected ways (e.g., another caller relying on `severity="ok"` semantics for unchecked keys) → surface to PM
- Smoke test reveals UI flow that assumes `leak_safe=True` for all keys → surface to PM
- Validator's `overall_valid` actually has more complex logic than the AND chain (e.g., user-permission-based overrides) → adapt design

---

## Effort Estimate

**Total: ~2 hours**

- Phase 0 (investigation): 15 min
- Phase 1 (detector change): 30 min
- Phase 2 (validator change): 20 min
- Phase 3 (tests): 40 min
- Phase Z (verify + handoff): 15 min

---

## Dependencies

- **None blocking**. This is the leading edge of M2f Group A.
- **Sibling**: #933 reorder agreed — #933 picks up after #932 lands. The flag flip will be straightforward.

---

## Audit-cascade self-check

| Template Requirement | Status |
|---|---|
| Phase -1 Infrastructure | ✅ (with N/A request for 0.5/0.6/0.7/0.8) |
| Phase 0 Investigation | ✅ |
| Phases 1-N Development | ✅ (Phase 1 + 2) |
| Test Strategy | ✅ |
| Phase Z Handoff | ✅ |
| Acceptance Criteria | ✅ |
| STOP Conditions | ✅ |
| Effort Estimate | ✅ |
| Dependencies | ✅ |
| Reference to issue | ✅ |
| Reference to audit memo | ✅ |
| Reference to PM disposition | ✅ |

**Phase 0.5 / 0.6 / 0.7 / 0.8** — flagged N/A; seeking PM approval inline. Not skipping silently.

---

## Action

Per audit-cascade discipline, gameplan complete. Phase 3 is **gameplan audit gate**: I should self-audit (the table above) and surface for PM approval before writing prompts (or, since this is small + tight scope, proceed directly to implementation).

Given the bounded scope (~2 hr, single-file changes + tests, PM-confirmed Option C), I propose **skipping the prompts phase and implementing directly** as a Lead Dev solo work item. The full audit-cascade with prompts is more useful for subagent delegation; for Lead Dev solo work the gameplan IS the prompt.

Confirm + I proceed to implementation.

— Lead Developer, 2026-05-09 ~09:25
