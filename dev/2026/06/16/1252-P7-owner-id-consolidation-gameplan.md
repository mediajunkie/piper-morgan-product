# #1252 P7 — `user_id`-string → `owner_id` UUID FK consolidation (ADR-071 D2)

**Author**: Lead Dev · **Date**: 2026-06-16 · **Status**: SCOPED + grounded; ready for execution with Arch sequencing-sign-off.
**Parent**: #1252 consolidating refactor · **ADR**: ADR-071 D2 (owner_id UUID FK → users.id canonical; user_id-string deprecated; none forbidden).

## Problem
User-content ownership is recorded inconsistently: some tables use a **`user_id` String** column, the canonical ones use **`owner_id` UUID FK → users.id**. D2 consolidates to the canonical form.

## Grounded inventory (models.py, 2026-06-16)
| Table | Current owner col | Type | → Target | Rows (alpha) | non-UUID values |
|---|---|---|---|---|---|
| `insights` | `user_id` | `String(255)` not-null | `owner_id` UUID FK | 33 | **0** |
| `conversations` | `user_id` | `String` not-null | `owner_id` UUID FK | 490 | **0** |
| `artifacts` | `owner_id` | `String` not-null | `owner_id` UUID FK (type only) | 1 | **0** |
| `feedback` / `memory` / `standup` | (per gameplan §"tables") | **VERIFY** — not confirmed in this pass; grep their models before migrating | ? | ? |
| **Already canonical** (no work): projects, repositories, uploaded_files, knowledge_nodes, knowledge_edges, todo_lists, list_memberships, lists | `owner_id` | UUID (FK) | — | — | — |
| Out of D2 scope (already UUID): audit_logs, ethics_audit_log, user_api_keys (`user_id` UUID) | `user_id` | UUID | naming-only; defer | — | — |

**Backfill reality (DB query 2026-06-16)**: every existing `user_id`/`owner_id` string is a valid UUID-string → **backfill is a clean `CAST(... AS uuid)`**, no legacy-value disposition needed (confirms P1: stored value = `JWTClaims.sub`, the UUID form of `users.id`). Defensive handling for the *theoretical* non-UUID row still belongs in the migration, but the alpha data is clean.

> ⚠️ **SCOPE-DISCOVERY 2026-06-16 (during execution attempt) — STOP-condition #1, the gameplan under-estimated this**: the DB data is clean, BUT the **unit tests pervasively use non-UUID owner/user_id identifiers** (`"alpha"`, `"beta"`, `"user-A"`, `"user-1"`). `CrossDialectUUID.process_result_value` calls `uuid.UUID(value)` on load (SQLite) → it **ValueErrors on any non-UUID string**. So converting a column `String → CrossDialectUUID` breaks **every test that creates+loads a row with a non-UUID identifier**: ~**8 files** for insights (incl. `test_composting_pipeline`, `test_morning_standup_structured_items_1034`, `test_push_mode_1032`, `test_pull_mode_1030`, persistence-wiring, repo 1031/1035), ~**10+ files** for conversations (intent handlers, lifecycle, context-assembler, conversational-floor, …), plus the artifact repo tests (`user-1/A/B`). **P7's type-conversion is therefore an all-or-nothing, ~18-test-file, multi-hour effort** (every non-UUID test identifier → a real UUID), not the quick migration the DB-clean backfill implied. **Value = D2 consistency, NOT correctness** (the (a,3)/anchoring correctness already shipped this session) → no urgency (alpha not precious). **Options surfaced to PM**: (a) full effort now, table-by-table, green at each step; (b) non-breaking additive first (add `owner_id` nullable + backfill migration, keep `user_id` + all tests; defer the breaking reader-migration/drop); (c) re-prioritize P7 below higher-value D1. Awaiting PM's pick before executing.

## Approach — per-table, m-40 layer-then-migrate (one table per increment)
For each target table:
1. **Alembic up**: add `owner_id` UUID FK → `users.id`, **nullable** (alongside the existing column).
2. **Backfill**: `UPDATE … SET owner_id = CAST(user_id AS uuid)` (guard the non-UUID case → leave NULL + log, do NOT fail the migration). For `artifacts`: cast the existing string `owner_id` into a new UUID column.
3. **FK validity**: confirm cast UUIDs exist in `users` (orphans → decide: D1 `is_global_pm_domain`/PM-owner per the #1238 disposition, or null+flag). **Query before the not-null step.**
4. **Shim** (repo layer): read/write `owner_id`; keep reading the legacy column as fallback during transition (mirrors the m-40 shim already used for the (a,3) fixes).
5. **Make `owner_id` not-null** once backfill + FK validity verified.
6. **Drop the legacy column** — LAST, after a soak period (separate increment; the riskiest/irreversible step).
- **TDD per table**: cross-owner scoping test (like `TestGetByIdScoping1252`) + an Alembic up/down round-trip test. Real Postgres (integration), not mocked.

## Rollback
Each `up` is reversible (`down` drops `owner_id`); reads stay behind the shim until the drop. The legacy-column drop (step 6) is the only irreversible step → gate it on a soak + explicit go.

## Dependencies / sequencing — **wants Arch sign-off**
- **Orphan-owner disposition** (step 3) ties to the **#1238 ingest-anchoring fork** (configured-PM-owner vs `is_global_pm_domain`) — same decision class; resolve consistently with Arch's #1238 ruling.
- **Order**: recommend `artifacts` first (1 row, type-only change, smallest blast radius) → `insights` (33) → `conversations` (490, most-read; highest care) → verify+do feedback/memory/standup. Arch to confirm.
- The (a,3) read-scoping for insights/conversations is **already shipped** (this session) using the string column — so P7 is purely the column-type/name consolidation underneath an already-correct read layer (lower risk than if reads were unscoped).

## Out of scope / deferred
- `Stakeholder` model — **dormant** (zero reads/writes; verified 2026-06-16) → no P3 migration now; fold in here only if/when stakeholders are used.
- `user_id`-UUID tables (audit/ethics/api_keys) — naming-consistency only, not a type fix; defer (not a leak).

## Done =
All target tables on `owner_id` UUID FK; backfill verified (0 NULL owner on user-content); legacy string columns dropped (post-soak); cross-owner + migration round-trip tests green; D5/anchoring guards still green.
