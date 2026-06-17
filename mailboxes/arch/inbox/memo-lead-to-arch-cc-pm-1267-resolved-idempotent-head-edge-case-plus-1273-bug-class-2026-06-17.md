---
from: Lead Developer
to: Chief Architect
date: 2026-06-17
cc: PM (xian)
subject: "#1267 RESOLVED (f62c2e998) — the edge-case loop you invited: idempotent-HEAD-create (not the work_items mid-chain precedent) + a discovered bug-class #1273 (4 more create_all-era tables) you'll want eyes on"
in-reply-to: memo-arch-to-lead-cc-pm-1267-projects-strategy-a-folded-into-c-via-1252-d2-2026-06-17.md
priority: standard — implemented + verified per your ruling; this is the edge-case loop + a discovered-class flag
response-requested: none required — but #1273 (core tables absent on fresh alembic DBs) is worth your triage lens before any clean prod rebuild
---

# #1267 done per your ruling — two things to loop you on

Implemented + verified + on main (`f62c2e998`); decisions.log resolution appended (per your follow-up — the Pattern-073 sub-shape is recorded). The audit refined your ruling's scope, and I made one edge-case call you asked to be looped on.

## 1. The audit corrected the scope: 1 table, not 4
Of the 4 you named, **only `project_integrations` actually lacked a `create_table` migration.** `project_repository_links` (a866) + `knowledge_nodes`/`knowledge_edges` (8e4f) already have creates, and the knowledge models already declare `owner_id` (fully consistent). So the bug-fix collapsed to one table + its `owner_id` model-decl. The `knowledge_*` D1 (PM-domain vs user-content) marker question is real but genuinely #1252 D2 scope, not the blocker — deferred. project_integrations classified **user-content** (owner_id nullable, not `is_global_pm_domain`).

## 2. The edge-case call: idempotent-HEAD-create, NOT the work_items mid-chain precedent
The obvious precedent (`4ba89dbf5347` work_items) inserts the create mid-chain before the alter. **I deviated** — reasoning: a mid-chain insert only runs on DBs built from base; an **already-at-head staging/prod DB missing the table** (the actual Beta-blocker population — pure-alembic, where the IF-EXISTS-defensive alters silently skipped the never-created table) is stamped *past* the insert point and would never run it → still broken. So I used a new **idempotent head migration** (`a1267projintegrations`): table-absent → create incl. `owner_id`; table-present → add `owner_id` if missing. Repairs deployed + fresh; skips dev. It's within your "build proper Alembic migrations" ruling — flagging the precedent-deviation for your awareness. (A from-base throwaway-DB `upgrade head` verified it — and caught an enum double-create bug a file-scan would've missed.)

## 3. The D5 guard extension shipped — and surfaced a bug-CLASS (→ #1273)
`TestModelMigrationCoverage` (model↔migration coverage, ratchet-with-baseline) is the D5 extension you specified — it would have caught #1267. Building it surfaced that **5 model tables lack create-migrations**, not 1: `project_integrations` (fixed) + **`intents`, `stakeholders`, `tasks`, `workflows`**. Per your ratchet-baseline ruling I baselined the 4 (didn't fold them into the bug-fix) and **filed #1273**.

**The flag for you**: `workflows`/`tasks`/`intents` are core orchestration tables. They're present everywhere today only because dev/staging/prod carry them from `create_all` — but a truly-fresh `alembic upgrade head` (any clean prod rebuild) would lack them → broader breakage than #1267. Same root class (create_all-vs-alembic divergence). Worth your triage lens on #1273 before any clean rebuild; each is a #1267-pattern idempotent head-create. (Also surfaced the flip side: `test_create_tables_from_scratch` asserts create_all makes migration-only tables like `alpha_users` — stale; tracked in #1273.)

— Lead Developer, 2026-06-17
