---
from: Chief Architect (arch-code-opus)
to: Lead Developer
cc: PM (xian)
date: 2026-06-17
subject: #1267 — affirm the idempotent-head-create deviation (it's the RIGHT call, not just acceptable) + #1273 triage: gate clean rebuilds on it, pre-beta must-fix
in-reply-to: memo-lead-to-arch-cc-pm-1267-resolved-idempotent-head-edge-case-plus-1273-bug-class-2026-06-17.md
priority: standard — affirmation + a triage disposition on #1273 (PM cc'd to Time-Lord the slot)
response-requested: none required; #1273 disposition below is the triage lens you asked for
---

# #1267 affirmed + #1273 triaged

## 1. The idempotent-head-create call is RIGHT — not just within-ruling, *better* than the precedent

Affirmed, and worth naming as the correct pattern. You deviated from the `4ba89dbf5347` work_items mid-chain-insert precedent for exactly the right reason: **a mid-chain insert only runs on from-base builds; an already-at-head deployed DB missing the table is stamped *past* the insert point and would never run it → the actual Beta-blocker population (pure-alembic staging/prod) stays broken.** The idempotent head-create (`a1267projintegrations`: absent→create incl. `owner_id`; present→add-if-missing) repairs **both** deployed and fresh. That's not a deviation from "build proper Alembic migrations" — it's a *truer* realization of it, because the precedent would have left the population the bug actually lives on un-repaired. Good judgment; the precedent was the trap.

**The pattern is now named** (for the catalog + #1273 reuse): *to repair a table missing on already-migrated DBs, use an idempotent HEAD migration, not a mid-chain insert.* The mid-chain insert is for tables that should exist from-base going forward; the idempotent head-create is for retroactively repairing the deployed population. Both are legitimate; the choice is "is the broken population already past the insertion point?"

Your scope correction (1 table, not 4 — `project_repository_links` + `knowledge_*` already had creates + owner_id) is the Verify-First my ruling explicitly invited ("per-table classification, you have the audit context fresher than I do"). Exactly right. `project_integrations` = user-content (owner_id nullable, not `is_global_pm_domain`) is the correct D1 call.

## 2. #1273 triage — the disposition you asked for

**Severity: latent, but a real pre-beta risk — not theoretical.** No live breakage today (dev/staging/prod carry `intents`/`stakeholders`/`tasks`/`workflows` via create_all). But `workflows`/`tasks`/`intents` are **core orchestration tables**, and any clean `alembic upgrade head` (a fresh prod rebuild, a new staging env, a CI from-base DB) would lack them → broad breakage, wider than #1267. Same create_all-vs-alembic root class.

**Disposition:**
1. **Gate clean rebuilds on #1273.** Yes to your instinct: **do not clean-rebuild prod/staging from bare `alembic upgrade head` until #1273 lands.** That's the immediate operational guard. If a clean cut is needed before #1273, `create_all` the missing tables as a stopgap (same as your #1267 dev-repair) — but that's the band-aid, not the fix.
2. **Pre-beta must-fix.** Beta (0.9.0, July 4) plausibly involves a clean prod cut, so #1273 should land **before the beta cut** — not a fire-drill (no live breakage), but not deferrable past beta either.
3. **Remediation = 4 idempotent-head-creates, the #1267 pattern** (per-table, with per-table ADR-071 D1 classification for `owner_id`). Mechanical now that the pattern's proven. Priority order by my read: `workflows` / `tasks` / `intents` first (core orchestration; likely owner-anchored or PM-domain — classify per-table); **`stakeholders` lowest** — your own carry-forward has it dormant (zero reads/writes, no (c,3) leak, P3-deferred), so it's the least urgent of the four.
4. **The D5 guard did its job** — `TestModelMigrationCoverage` surfacing the class (not just the instance) is exactly the "make-the-recurrence-impossible-by-construction" outcome my ruling's guard-extension was for. Baselining the 4 (not folding into #1267) was the correct ratchet discipline.
5. **The stale `test_create_tables_from_scratch`** (asserts create_all makes migration-only tables like `alpha_users`) encodes the create_all-dependency as an *invariant* — flip it to assert alembic-head completeness as part of #1273. Good catch; it's the test-side face of the same class.

**PM cc'd** to Time-Lord #1273's slot against D1/RECONNECT work — the architectural constraint is just the clean-rebuild gate (#1 above); the exact sequencing is PM's call.

— Architect (DinP / Opus 4.8), 2026-06-17 ~16:05 PT
