# Audit: #935 against feature.md template

**Issue**: TECH-DEBT: BudgetManager + APIUsageTracker have zero database persistence
**Auditor**: Lead Developer
**Date**: 2026-05-09 ~13:30
**Phase**: 1 of 3 (Issue audit) — pre-gameplan gate

---

## TL;DR

**Verdict: ⚠️ Issue body is ALSO partially wrong** (same shape as #936). Investigation:

- **BudgetManager** — ZERO production callers (same pattern as deleted UserService)
- **APIUsageTracker** — has real INSERT SQL into `api_usage_logs` table (table EXISTS, 0 rows). One production callsite at `llm_domain_service.py:159` BUT it's gated `if session and context:` and **callers don't pass a session**. So `_log_usage` is never reached in production; the INSERT path is dead. Body's claim "in-memory only" is wrong on the implementation detail (writes WOULD persist, if reached); right on the practical effect (no data persists because the call is unreachable).

**Same disposition tree as #936**: A (delete), B (wire it up properly + cost tracking infra), or C (defer to beta-readiness).

---

## Findings

### BudgetManager (`services/analytics/budget_manager.py`, 428 LOC)

```bash
$ grep -rn "BudgetManager\|from services.analytics.budget_manager" services/ web/ tests/ --include="*.py" | grep -v "test_\|class BudgetManager"
# ZERO production callsites
```

Same shape as deleted UserService — wired-into-nothing dead code.

The 5 TODOs the issue references (lines 126, 399, 410, 416, 427) are all "Implement actual database storage / queries" placeholders. The class itself is fully unreachable.

### APIUsageTracker (`services/analytics/api_usage_tracker.py`, 393 LOC)

Production callsite chain:
1. `services/domain/llm_domain_service.py:53`: `self._usage_tracker = APIUsageTracker()`
2. Line 158-165: `if session and context: await self._log_usage(...)`
3. `_log_usage` at line 201 calls `self._usage_tracker.log_api_call(session=session, ...)`
4. `log_api_call` at `api_usage_tracker.py:155` runs `INSERT INTO api_usage_logs (...)` against the `api_usage_logs` table (which **does** exist in postgres).

But here's the catch: the only callers of `LLMDomainService.complete()` are at `lens_inference.py:275` and `slot_extractor.py:50`. Both call `llm_service.complete(task_type=..., prompt=...)` **without passing a session**. So `if session and context:` is False, `_log_usage` is never called, the INSERT never fires.

**`api_usage_logs` table has 0 rows** — confirmed via `psql -c "SELECT COUNT(*) FROM api_usage_logs;"`.

The "7 TODOs for database queries" the body references (lines 223, 233, 264, 328, 345, 370, 381 in api_usage_tracker.py) are all in the **read** methods (`check_budget`, `get_usage_summary`, `get_budget_status`, `get_recommendations`, etc.). Each is "TODO: Implement actual database queries" — they return stub data without querying. So even if writes WERE persisting, reads wouldn't find them.

### Issue body's framing

> *"Two analytics services have no persistent storage — all data is in-memory only and lost on server restart"*

Reality: BudgetManager has no callers (no data to persist or lose). APIUsageTracker has real INSERT SQL but is unreachable because callers don't pass a session. So neither stores data, but the reasons are different:
- BudgetManager: dead code
- APIUsageTracker: half-implemented (writes work, reads stubbed) AND unreachable (gate filters out all calls)

> *"Users have no historical usage visibility"*

Correct effect, wrong cause. They have no visibility because the data isn't being written, not because it's being lost on restart.

---

## Three options (mirroring #936's disposition tree)

### Option A — Delete both classes + dead callsite (recommended)

- Delete `services/analytics/budget_manager.py` (zero callers)
- Delete `services/analytics/api_usage_tracker.py` (unreachable in production)
- Remove `_usage_tracker` instantiation + `_log_usage` method + `if session and context: await self._log_usage(...)` block from `services/domain/llm_domain_service.py`
- Drop `api_usage_logs` table from schema (Alembic migration)
- Update `tests/integration/test_api_usage_tracking.py` accordingly
- **Mooting effect**: #1029 (wire APIUsageTracker into LLMClient) becomes moot — the thing it was wiring is gone. Should close #1029 as superseded.
- **Effort**: ~2-3 hr

**Reasoning**:
- Pre-release dev env, no production users → cost tracking has minimal MVP value
- Dev visibility comes from API provider dashboards (Anthropic console, OpenAI usage page) directly
- Same "don't pre-build" framing PM endorsed for #936

### Option B — Wire up properly (with #1029 + #935 together)

- Implement APIUsageTracker's read methods (replace 7 TODOs with real SQL)
- Wire `LLMDomainService.complete()` to pass a session (or use a non-blocking session-acquisition helper)
- Wire #1029's "sync call sites" — adds APIUsageTracker calls in LLMClient itself
- Implement BudgetManager properly (5 TODOs → real DB)
- Tests + verification
- **Effort**: ~10-15 hr; significant work; needs Architect review for data-model + concurrency questions

**Why I'd push back**: implements features (cost analytics, budget enforcement) that no production callsite needs at MVP. Same "don't pre-build" antipattern as keeping UserService alive. Cost tracking is a beta-readiness concern, not alpha.

### Option C — DEPRECATED comments + defer

- Add DEPRECATED comments to both files
- Tag the unreachable callsite in LLMDomainService
- File a beta-readiness issue for actual cost-tracking design (with concrete scope)
- **Effort**: ~1 hr
- **Risk**: same as #936's Option C — kicks the can; future agents may try to "fix"

---

## My recommendation: Option A

Same logic as #936:
1. Dead code wired to (or near) production is worse than no code — it confuses readers + invites accidental "fixes"
2. The body's "lost on restart" framing presumes the code is functional; investigation shows it's not
3. Cost tracking is beta-readiness, not MVP. We don't need it now.
4. **#1029 should be closed as superseded** if we go with A — it's wiring the thing we'd be deleting

**Architect-routing recommendation**: same as #936, file an Architect-CC memo after-the-fact for review-after, not gate. PM has authorized this pattern.

---

## Audit matrix (abbreviated)

| Template Requirement | Status |
|---|---|
| Title + LABEL | ✅ |
| Priority | ⚠️ "P:medium" stated; if dead-code disposition, smaller-scope fix |
| Problem Statement — Current State | ❌ Body's framing wrong on causes (right on effect) |
| Goal | ⚠️ Acceptance criteria assumes wire-up path; doesn't acknowledge "delete" option |
| What Already Exists | ❌ Body doesn't acknowledge `api_usage_logs` table exists + INSERT SQL is implemented |
| Phases / Effort | ❌ Missing |
| Dependencies | ⚠️ Should reference #1029 (which would moot under Option A) and #691 (mentioned in body, M2 tail) |

---

## Cross-references

- #936 (UserService deletion — same dead-code pattern; closed today)
- #1029 (Wire APIUsageTracker into LLMClient — would be **superseded** by Option A here)
- #691 (WIRE-CANONICAL — referenced in body)
- `services/domain/llm_domain_service.py:53,159,201,253` — the unreachable call chain
- `api_usage_logs` table — exists in DB; 0 rows; DROP migration if Option A

---

## Action

Surfacing 1 PM question + 1 cohort-impact note:

**Q1**: Option A / B / C? My read = A (consistent with #936; pre-MVP scope rationale).

**Cohort note**: If A, **#1029 should also be closed as superseded.** That's a cohort-level change to the M2f Group D mapping (#1029 is in Group D currently). Worth confirming.

Once Q1 is answered, gameplan ~20 min (similar shape to #936).

— Lead Developer, 2026-05-09 ~13:50
