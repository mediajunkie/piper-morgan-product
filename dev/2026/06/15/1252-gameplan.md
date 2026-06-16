# Gameplan: #1252 — User-auth anchoring consolidation (ADR-071 D2–D6)

_Lead Dev · 2026-06-15 · audit-cascade GAMEPLAN gate. Issue: #1252 (audited, ISSUE-gate passed). Decision: ADR-071 (ratified). Audit: #1241 (`dev/2026/06/15/1241-content-anchoring-audit.md`)._

---

## Phase -1: Infrastructure Verification Checkpoint

**Purpose**: prevent a wrong gameplan from bad assumptions. For this refactor the verification is *already done* — it IS the #1241 audit (Arch-confirmed) + the ratified ADR-071 + PM's endorsement.

### Part A: Current understanding (grounded, not assumed)
- **Web framework**: FastAPI (`web/api/routes/`), Flask-style Jinja templates. **DB**: PostgreSQL (asyncpg + SQLAlchemy async; port 5433), 37 tables in `services/database/models.py` + ChromaDB `pm_knowledge`. **Testing**: pytest (`asyncio_mode=auto`, in-memory SQLite for repo tests) + jest/jsdom (`tests/frontend/`).
- **The task** (verified by audit, not assumed): consolidate 3-way principal anchoring → canonical `owner_id` FK + thread the principal as a required param + close the (c,3)/(a,3) gaps + AST-guard, per ADR-071 D2/D3/D4/D5/D6.

### Part A.2: Work characteristics
- **Worktree**: ephemeral auto-worktree (Option B canonical) — already running in one. No per-phase decision (per the current model; gameplan-template A.2's `.trees/` flow is deprecated — see #1206 item-2).
- Multi-phase, multi-file, DB-migration-bearing → **full excellence flywheel** (audit-cascade + DDD + TDD), per substantive-work rigor.

### Part B: PM verification — SATISFIED
- PM 2026-06-15 endorsed "an architectural decision AND a consolidating refactor"; directed this kickoff gameplan-first + full audit-cascade; chose refactor-handles-#1250 (not a band-aid). ADR-071 ratified by Arch. **No open assumptions requiring PM correction before proceeding.**

### Part C: Proceed/Revise — **PROCEED** (understanding grounded in ratified ADR + completed audit).

---

## Phase 0: Initial Bookending — GitHub Investigation
- **Issues verified to exist**: #1252 (umbrella, this gameplan's target), #1238 (doc-store, P2), #1250 (learning toggle, P5), #1248 (jest CI, parallel), #1239 (Radar WorkItem — already handled by ADR-071 D1 render-guard, no schema change), #1241 (audit, closed-analytical).
- **Current state**: 3-way inconsistency + (c,3) gaps + 4 (a,3) leak paths + 40+ D4 resolution sites, all enumerated in #1241. ADR-071 ratified.
- **STOP conditions cleared**: ADR ratified (no ADR conflict); audit complete (no missing investigation); PM-endorsed (no authority gap).

## Phase 0.5: Frontend–Backend Contract Verification
**Applies to**: the #1250 (learning toggle) + #1248 (jest) UI-adjacent parts only; the core refactor is data-layer.
- `/api/v1/learning/settings` (PUT) — exists (`learning.py:1349`); the 500 is the FK violation, not a missing route (verified via server log). Frontend `learning-dashboard.html` already calls it correctly (`API_BASE='/api/v1/learning'`). So the #1250 fix is backend-only (principal anchoring); no FE contract change.
- `tests/frontend/` jest harness — exists + runnable (`npm ci && npx jest`); not in CI (the #1248 gap).

## Phase 0.6: Data Flow & Integration Verification — **CORE OF THIS REFACTOR**
This refactor *is* a data-flow fix. The required handoff: **principal originates at the host boundary → threaded as a required param → applied at the data-layer read/write.**
- **Origination (verified)**: `auth_middleware.py:177` (`request.state.user_id` from JWT), `:316` (`get_current_user`).
- **The break (verified, #1241)**: the principal is *re-fetched* opportunistically as `intent.context.get("user_id") if intent.context else None` at 40+ sites → degrades to `None` → unscoped reads. The fix is to thread it as a required parameter (D4), not re-fetch from mutable context.
- **Per-store write/read anchoring**: `owner_id` FK (write) + JOIN/filter (read), per the #1241 store-by-store table.
- **Integration points**: `services/database/repositories.py` (read methods), `services/auth/auth_middleware.py` (origination), the intent/classifier/handler chain (threading), `services/knowledge_graph/` + `document_service.py` (doc-store), `learning.py` (#1250).
- **Pitfall (from #490 retrospective + #1250)**: lookup-key mismatch — `user_id`-string vs `owner_id`-FK-UUID are NOT interchangeable (the #1250 bug is exactly this: a UUID used where the FK target doesn't exist). The shim must handle both during migration.

## Phase 0.7: Conversation Design — **Not applicable** (template scopes this to conversational features; this is a data-layer refactor, no conversation surface). Not a unilateral N/A — the template's own condition ("For Conversational Features") isn't met.

## Phase 0.8: Post-Completion Integration — **APPLIES** (this refactor changes DB records — adds owner_id columns, backfills, drops user_id-string)

### Migration side-effects (verify per phase)
| Side effect | Table/Field | Phase | Verified? |
|---|---|---|---|
| owner_id FK added | stakeholders; doc-store metadata; migrated user_id tables | P3 / P2 / P7 | [ ] |
| Backfill applied (no NULL owner on user-content) | each migrated table | P3 / P7 | [ ] |
| user_id-string column dropped | conversations/insights/feedback/memory/standup | P7 (shim-then-drop) | [ ] |
| is_global_pm_domain marker set | products/features/work_items/intents/workflows/tasks | P8 | [ ] |

### Downstream behavior changes
| Behavior | Before | After |
|---|---|---|
| Doc-store / stakeholders reads | global (all users) | scoped to the principal |
| The 4 (a,3) read methods | can return cross-owner content | return none/404 cross-owner |
| `intent.context.get("user_id")` | silently `None` → unscoped | threaded required param; D5 fails new uses |
| #1250 learning toggle | 500 (FK violation) | persists (real principal) |

### Verification query (post-migration, per store)
```sql
-- e.g. after P3 (stakeholders) + P7 (consolidation) — expect 0 unanchored user-content rows
SELECT count(*) FROM stakeholders WHERE owner_id IS NULL;   -- expect 0
SELECT count(*) FROM learning_settings ls LEFT JOIN users u ON ls.user_id = u.id WHERE u.id IS NULL;  -- expect 0 (no orphan FK), validates #1250
```

---

## Phases 1–N: the migration (layer-then-migrate, m-40; privacy-first ordering per ADR-071 D6)

> Each phase = DDD (domain model first) + TDD (test-first) + close-issue-properly. The fine-grained per-file task breakdown is produced at the **PROMPTS gate** when each phase is picked up. Phases 2–4 (the (c,3)/(a,3) gaps) are privacy-first; D4 threading (P5) runs partly in parallel; guards (P6) ratchet as populations reach zero.

### Phase 1: D2 canonical convention + shim infrastructure
- **Objective**: establish the canonical `owner_id` FK pattern + a dual-read shim so `user_id`-string columns migrate without breaking callers.
- **Approach**: DDD — define the anchoring contract (owner_id FK type, read-scope mechanic). Build the shim helper (read owner_id, fall back to user_id-string during the window). TDD the shim.
- **Deliverable**: documented canonical pattern + shim helper + unit tests. **Rollback**: additive (new helper, no column drops) → revert the helper commit.
- **Depends on**: P0 Arch-confirm of the convention/shim shape.

### Phase 2: (c,3) doc-store anchoring — #1238 (worked example)
- **Objective**: anchor the ChromaDB doc-store to a principal (or `is_global` escape per D6); scope reads.
- **Approach**: add owner metadata at ingest + upload path; scope `document_service.py` queries by principal; backfill policy per ADR-071 Open Questions (designated-PM-owner vs is_global). TDD cross-user isolation.
- **Deliverable**: doc-store anchored + scoped; #1238 closed; Radar Document source unblocked. **Rollback**: feature-flag the scoped read; the additive owner metadata is backward-compatible.
- **Depends on**: P1 convention.

### Phase 3: (c,3) stakeholders anchoring
- **Objective**: add owner + read-scoping to `stakeholders`.
- **Approach**: Alembic migration (add owner_id FK, nullable→backfill→required per m-40); scope the reads. TDD.
- **Deliverable**: `stakeholders` anchored + scoped + tests. **Rollback**: the migration is reversible (drop column); reads behind the shim.
- **Depends on**: P1.

### Phase 4: (a,3) leak-path fixes (D3)
- **Objective**: the 4 named read methods filter at the data layer (not post-hoc/optional/unscoped).
- **Approach**: `conversations.get_by_id` (+owner WHERE), `insights.get_for_object` (+principal), `knowledge_nodes` (make owner required), `artifacts.get_by_id` (filter in query). **TDD-first**: write the cross-owner-returns-none/404 test, watch it fail, then fix.
- **Deliverable**: 4 methods fixed + regression tests. **Rollback**: per-method revert (each is independent).
- **Depends on**: none (independent of P1; can run early — privacy-relevant).

### Phase 5: D4 principal-threading — #1250 lands here
- **Objective**: thread the real principal as a required param across the 40+ sites; retire the `context.get("user_id")` re-fetch.
- **Approach**: chain-by-chain (m-40) — add the required param, hold the context-fetch as a WARNING-logged shim, migrate callers, drop the shim per chain. **#1250**: route `learning.py` off `TEST_USER_ID` onto the threaded real principal (exists in `users`) → toggle works; TDD the PUT.
- **Deliverable**: principal threaded (shim logged) + #1250 verified working + tests. **Rollback**: the shim keeps old paths working during migration; revert per chain.
- **Depends on**: D4.1 origination (already in place); composes with ADR-070 D8 identity-unification ordering (cross-ref).

### Phase 6: D5 AST guards (m-41 mechanism)
- **Objective**: enforcement tests — model-without-owner fails; read-without-principal fails; `context.get("user_id")` outside boundary sites fails.
- **Approach**: mirror `TestSessionScopeCommitContract` (ADR-069 D5) + the **baseline-ratchet** pattern (F3 token-lint / F1 native-dialog precedent): snapshot existing violations, fail-on-new, ratchet to zero as P2–P7 land.
- **Deliverable**: AST guard tests in CI, baselined + ratcheting. **Rollback**: the guard is additive (a test); disable the CI step if it misfires.
- **Depends on**: lands incrementally as each population (P2–P5, P7) reaches zero.

### Phase 7: user_id→owner_id consolidation (shim-then-drop)
- **Objective**: migrate the deprecated `user_id`-string columns to `owner_id` FKs; drop the shim.
- **Approach**: per-table Alembic migration + caller migration; drop the shim once callers complete (m-40 final step). TDD each migration.
- **Deliverable**: columns migrated + shim dropped + tested. **Rollback**: each Alembic migration is reversible; sequence one table at a time.
- **Depends on**: P1 (shim), P5 (callers threaded).

### Phase 8: D1 PM-domain global-by-design exemption marker
- **Objective**: tag `products/features/work_items/intents/workflows/tasks` `is_global_pm_domain`; D5 recognizes it (no false-positive).
- **Approach**: pick the marker mechanism (column vs registry vs docstring constant — ADR-071 Open Questions; decide post-P1-evidence) + wire the D5 guard to recognize it.
- **Deliverable**: marker + D5 recognition + test. **Rollback**: additive marker.
- **Depends on**: P6 (the guard must exist to recognize the exemption).

### Parallel: #1248 jest CI (folded in per PM)
- **Objective**: fix the 6 `form-validation` jest failures + wire `tests/frontend/` into CI.
- **Approach**: diagnose the 6 failures (validator contract vs test); fix; add a CI job (`npm ci && npx jest`) on `web/static/js/**` + `tests/frontend/**` changes; commit `package-lock.json`. **Deliverable**: jest green + CI job. **Rollback**: revert the workflow step. Independent of the data-layer phases.

### Phase Z: Completion & Handoff
- [ ] All #1252 ACs met + evidence; completion matrix all-✅; ADR-071 cross-refs updated; decisions.log per phase; session log; child issues (#1238/#1250/#1248) closed-properly.

---

## Success Criteria (measurable)
1. `owner_id` FK is the only anchoring pattern on user-content tables; `user_id`-string columns dropped; D5 guard enforces it (0 violations).
2. (c,3): doc-store + stakeholders return only the principal's content (cross-user isolation test green).
3. (a,3): the 4 read methods return none/404 cross-owner (regression tests green).
4. D4: 0 `intent.context.get("user_id")` outside the boundary sites (D5 guard green); #1250 toggle persists.
5. No regression in the canonical suite; #1248 jest green + in CI.

## Test Strategy
- **DDD + TDD per phase**: domain model/contract first, then test-first for each behavior (write the failing cross-owner/scoping test, then fix).
- **Layers**: domain unit tests + repository tests (in-memory SQLite) + route tests + the D5 AST guard (enforcement) + jest (frontend, #1248) + the canonical suite (regression).
- **Privacy assertions**: every (c,3)/(a,3) fix ships with a cross-owner-isolation test.
- **Env**: `env -u ANTHROPIC_* POSTGRES_PORT=5433 venv/bin/python -m pytest` (SDK-strip per CLAUDE.md).

## Multi-Agent Coordination + Integration-Test Discipline
- **Deployment**: phases are mostly sequential (dependency-aware order below); P4 (a,3) + #1248 (jest) are independent → parallelizable. Each phase, when picked up, goes through the audit-cascade **PROMPTS gate** → executed by Lead Dev or a briefed Coding Agent subagent (DDD + TDD + close-issue-properly).
- **Routing integration tests (#521 learning)**: where a phase touches the intent/classifier/handler chain (**P5 threading**), test the FULL path (pre-classifier → intent service → handler), NOT the handler in isolation with mocked routing — a mocked-routing test would hide the exact `None`-degradation this refactor fixes.
- **Wiring integration tests (#490 learning)**: P5/P2 must exercise the REAL import/call chain (do NOT mock the internal principal-fetch), so a threading/wiring bug can't hide behind a mock. The **#1250** fix specifically gets an integration test hitting the real `PUT /api/v1/learning/settings` → real principal → real DB insert (not a mocked `user_id`).
- **Cross-validation gate**: every (c,3)/(a,3) phase ships a cross-owner-isolation test as its verification gate (proves the scoping, not just that the code runs).

## Rollback Plan
- **Per-phase, per-commit**: each phase is independently revertible (additive helpers / reversible Alembic migrations / feature-flagged scoped reads).
- **The m-40 shim is the safety net**: deprecated columns + context-fetch are held (WARNING-logged) until callers migrate, so no big-bang cutover. A failed phase reverts to the shim state.
- **Sequence-safety**: privacy-first (P2–P4) early; the broad D4 threading (P5) chain-by-chain; column drops (P7) last.

## Dependencies
- **Internal**: P2/P3/P7 depend on P1 (convention/shim); P8 depends on P6 (guard); P5 #1250 needs D4.1 origination (in place). P4 is independent (can start first — privacy).
- **External/cross-lane**: ADR-070 D8 (identity unification, RECONNECT WS-9 #1233) is prerequisite-ordered before P5 fully completes (the "one principal per human" assumption) — cross-ref, not a blocker for early phases. PPM entity-model for #1240 People (not in this refactor's scope).
- **Arch**: P0 confirm of the canonical convention + shim shape (one-line exchange).

## Recommended execution order (privacy-first + dependency-aware)
P0 (Arch-confirm) → **P4 (a,3 leak fixes — fastest privacy win, independent)** → P1 (convention/shim) → **P2 (#1238 doc-store)** → P3 (stakeholders) → **P5 (#1250 + D4 threading)** → P6 (guards, ratcheting throughout) → P7 (consolidation) → P8 (exemption marker). #1248 parallel anytime.
