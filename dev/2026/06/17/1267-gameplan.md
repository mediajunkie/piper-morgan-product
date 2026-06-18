# #1267 Gameplan — Projects 500: project_integrations missing create-migration (+ model↔migration drift)

**Issue**: [#1267](https://github.com/mediajunkie/piper-morgan-product/issues/1267) — BUG: Projects 500 on clean DBs
**Role**: Lead Developer · **Date**: 2026-06-17 · **Branch**: claude/interesting-beaver-7ee19c (Option B ephemeral)
**Authority**: PM approved "do #1267" (2026-06-17, live). Arch ruling: `memo-arch-to-lead-cc-pm-1267-projects-strategy-a-folded-into-c-via-1252-d2` — (a) folded into (c) via #1252 D2. Time Lord: PM on prioritization.
**Template**: gameplan-template v9.6. **Audit-cascade**: ISSUE gate (issue exists, verified) → this GAMEPLAN doc → GAMEPLAN audit (`1267-gameplan-audit.md`) → implement.

---

## Phase −1: Infrastructure Verification (audited, not assumed)

| Item | Verified state (this session, 2026-06-17) |
|---|---|
| Migration tool | Alembic; versions in `alembic/versions/`; prod/clean path = `alembic upgrade head` (main.py-documented). |
| `create_all` | Lives in `DatabaseConnection.create_tables()` (connection.py:115). **Called only by tests** (`tests/integration/test_fresh_database_setup.py`) — **no production/startup caller**. So prod is already pure-alembic. |
| ORM base | `services/database/models.py` — `Base` subclasses; 4 tables in question: `project_integrations` (:928), `project_repository_links` (:1044), `knowledge_nodes` (:1377), `knowledge_edges` (:1449). |
| DB | PostgreSQL (5433 dev). |
| Task | **Fix broken functionality** (Beta-blocker) + light **refactor** (model↔migration reconcile, guard). |
| PM verification | PM greenlit the work live; infra above is audited from the tree (not assumed). PROCEED. |

## Phase 0: GitHub Investigation — root cause **verified AND corrected**

The issue body said *"project_integrations AND project_repository_links have no create migration"* and named 4 tables. **The audit corrects this** (investigate-before-extending — read the whole chain, don't trust the summary):

### Per-table audit matrix (the key artifact)
| Table | `create_table` migration? | owner_id in a migration? | owner_id in **model**? | Consistent? | #1267 action |
|---|---|---|---|---|---|
| **project_integrations** | ❌ **NONE** (`:928`) | ✅ `4d1e2c3b5f7a` (defensive, skips if absent) | ❌ model lacks | **NO** — the bug | **create-migration + model owner_id** |
| project_repository_links | ✅ `a866:54` | ❌ not in `4d1e` table-list (anchor = `linked_by`) | ❌ (has `linked_by`) | create ✓; owner_id = #1252 | **none for the bug** (verify only) |
| knowledge_nodes | ✅ `8e4f:75` | ✅ `4d1e2c3b5f7a` | ✅ `:1390` | **YES** | none (D1-classify → #1252) |
| knowledge_edges | ✅ `8e4f:93` | ✅ (model `:1463`) | ✅ `:1463` | **YES** | none (D1-classify → #1252) |

### Why a fresh `alembic upgrade head` doesn't error but the table is absent
`4d1e2c3b5f7a` (owner_id) is **defensive** — it wraps `project_integrations` / `knowledge_*` in `IF EXISTS (information_schema.tables …)` PL/pgSQL (docstring: *"these tables may not exist in all databases … created by other features later"*). `d73b3722eb03` (timestamptz) similarly tolerates absence. So on a clean DB the alters **silently skip** `project_integrations`, and since **nothing ever `create_table`s it**, the table is simply **absent** → `list_active_projects`'s `selectinload(integrations)` hits `UndefinedTableError` → route `except` → 500. (Empty list renders because no rows are eager-loaded.)

**Net: the bug is ONE table (`project_integrations`), not four.** The other three are already migration-covered and (for knowledge_*) model-consistent.

## Phases skipped per template's own applicability rules (transparent, not silent N/A)
- **0.5 Frontend-Backend Contract** — template: *"❌ Backend-only changes (skip)."* #1267 is DB/backend-only. SKIP.
- **0.6 Data Flow (multi-layer)** — template: *"❌ Single-layer changes (skip)."* The owner_id model-decl is a single-layer ORM change; the ADR-071 per-table classification is captured below. SKIP the layer-propagation table.
- **0.7 Conversation Design** — no conversation. SKIP.
- **0.8 Post-Completion** — APPLIES lightly: completion side-effect = `project_integrations` exists + `GET /api/v1/projects` returns 200. Captured in Success Criteria / Phase 4.

---

## The fix approach — idempotent HEAD create (decision + reasoning)

**Decision: add a NEW head migration that creates `project_integrations` idempotently (checkfirst / `IF NOT EXISTS`) with the full final schema (incl. `owner_id`).**

**Why NOT the `4ba89dbf5347` work_items precedent (mid-chain insert before the alter):** a mid-chain insert only runs on DBs built from base. **Already-deployed at-head DBs (staging/prod) that are missing the table — the exact Beta-blocker population — are stamped past the insert point and would never run it → still broken.** A new head migration runs on every DB advancing to head: creates-if-missing (repairs deployed + fresh), skips-if-present (dev, which has the table from the 6/17 dev-repair create_all). This is the only approach that repairs deployed DBs.

**owner_id in the create**: include it. `4d1e2c3b5f7a` *intended* to add owner_id (it's in the table-list) but defensively skipped it on clean DBs; since the new create is at head (after `4d1e` already ran-and-skipped), the create must carry owner_id itself. Aligns model + migration + ADR-071 D2 intent.

**⚠️ Edge-case loop to Arch (non-blocking)**: this deviates from the work_items precedent for the deployed-DB-repair reason above. Within Arch's ruling ("build proper Alembic migrations"); I'll record the choice + reasoning in decisions.log and cc Arch. Arch said "loop me on edge cases" — looping async, not gating.

## ADR-071 D1 per-table classification (Arch-requested)
- **project_integrations** → **user-content** (project-scoped config; projects are owner-anchored). `owner_id` FK → users.id, **nullable=True** (m-40 grace, matching DocumentDB + knowledge models). NOT `is_global_pm_domain`.
- knowledge_nodes / knowledge_edges → PM-domain-vs-user-content question is **real but out of bug-scope** (they already exist + are model-consistent; the `is_global_pm_domain` marker decision rides with #1252 D2, not the #1267 blocker). Flag in handoff.
- project_repository_links → user-content; anchor today is `linked_by`. owner_id alignment = #1252.

---

## Phases 1–4 (Arch's plan, refined by the audit)

### Phase 1 — Audit & classification ✅ DONE (this doc)
Output = this gameplan + the per-table matrix + the fix decision. Scope corrected from 4 tables → 1.

### Phase 2 — Implement (TDD) (~1–1.5hr, down from 2–3 given narrowed scope)
1. **RED**: write the regression test FIRST (real, not curl-200):
   - `tests/integration/test_fresh_database_setup.py` (or a new `test_1267_project_integrations_migration.py`): on a DB built via **`alembic upgrade head`** (the prod path, NOT `create_all`), assert `project_integrations` table exists; insert a project + an integration; assert `list_active_projects` returns the project with its integration (no `UndefinedTableError`). This fails today on a pure-alembic DB.
2. **GREEN**:
   - New Alembic head migration `create project_integrations` (idempotent / checkfirst), full schema: `id`, `project_id` FK→projects, `type` (IntegrationType enum — reuse existing PG enum if present, else create), `name`, `config` JSON, `is_active`, `created_at` timestamptz, `owner_id` UUID FK→users nullable + index.
   - Add `owner_id` Column to `ProjectIntegrationDB` model (nullable=True, index).
3. **create_all retirement (for these tables)**: make the alembic path complete so `create_all` isn't masking the gap. Augment `test_fresh_database_setup` to assert the **alembic-upgrade-head** path produces `project_integrations` (the #1267 regression guard), so create_all can't silently hide a future missing-create.
4. Run unit + integration; verify "N passed".

### Phase 3 — D5 guard extension (~30–45min)
Extend the ADR-071 D5 guard (model↔migration coverage): assert **every `Base` model `__tablename__` has a corresponding `op.create_table` in `alembic/versions/`**. This catches the "model exists, no create migration" class (would have caught #1267). **Ratchet-with-baseline**: if the guard surfaces OTHER already-drifted tables, baseline them + file a follow-up issue — do NOT expand #1267 to fix all of them (scope discipline). Read the existing guard first to extend in-idiom.

### Phase 4 — Verify on fresh DB (~15–30min)
Throwaway DB → `alembic upgrade head` → assert all 4 tables present + `GET /api/v1/projects` (with ≥1 project + integration) returns **200**. Cross-owner scoping sanity on project_integrations.owner_id.

---

## Test strategy (real verification, per the "no curl-200" discipline)
- **Regression (the load-bearing one)**: fresh DB via **`alembic upgrade head`** (not create_all) → table exists → projects API 200. Mirrors the actual prod build path that's broken.
- **Unit**: model has owner_id; migration is idempotent (re-runnable / skip-if-present).
- **Guard (Phase 3)**: model↔migration coverage assertion (ratchet).
- ❌ NOT acceptable: "I ran create_all and it worked" (that's the band-aid the bug hid behind).

## Success criteria
- [ ] `alembic upgrade head` on a clean DB creates `project_integrations` (idempotent on DBs that already have it).
- [ ] `GET /api/v1/projects` returns 200 with ≥1 project + integration (no `UndefinedTableError`).
- [ ] `ProjectIntegrationDB` model declares `owner_id` (matches migration; ADR-071 D2).
- [ ] D5 guard asserts model↔migration coverage; baseline ratcheted; any other gaps filed (not fixed here).
- [ ] decisions.log: resolution line (per Arch follow-up) + the idempotent-head-vs-precedent decision.
- [ ] Tests green ("N passed"); evidence in issue; PM approves close.

## Rollback plan
- Migration `downgrade()` drops `project_integrations` (guarded). Model owner_id revert is a one-line diff. Guard is additive (revert = remove the assertion). Each phase commits separately → granular revert.

## Dependencies / composition
- **#1252 D2** — this Phase-2 IS a #1252 increment (label TBD, e.g. P7.5); knowledge_* D1 marker + link-table owner_id defer to #1252.
- **ADR-071 D1/D2/D5** — classification (D1), owner_id (D2), guard extension (D5).
- **decisions.log** — append resolution + Pattern-073 sub-shape note (Arch follow-up memo); optional CIO catalog flag.
- **Arch cc** — the idempotent-head edge-case decision.
