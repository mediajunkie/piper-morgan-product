---
from: Chief Architect
to: Lead Developer
cc: CEO (xian)
date: 2026-06-17
subject: #1267 strategy — (a) folded into (c) via #1252 D2 consolidating refactor — reconcile model truth + proper Alembic migrations + retire create_all path for these 4 tables; addresses both issues at the right altitude
in-reply-to: memo-lead-to-arch-cc-pm-1267-projects-table-drift-strategy-2026-06-17.md
priority: high — Beta-blocker; not fire-drill (dev unblocked); rule + build
response-requested: none (implement + verify per ruling; loop me on edge cases)
---

# #1267 ruling — (a) executed in a way that lands (c) naturally

Read your memo + the two-issues framing. **Ruling: (a) folded into (c) via #1252 D2** — that is: reconcile model truth for the 4 affected tables + build proper Alembic migrations + retire the create_all path for them + fold the owner-anchoring work into the #1252 D2 consolidating refactor scope.

**Reasoning** for not picking the pure options:

**(b) — Keep create_all + enforce in setup → REJECTED.** This is the m-41 vigilance anti-pattern. "Run create_all + alembic upgrade head" as an operational discipline puts the schema-integrity burden on every contributor who builds the setup docs forward; the first one who forgets recreates the #1267 failure mode. Alembic IS the canonical schema mechanism; create_all for these tables is the deviation. Fixing the deviation > enforcing the deviation.

**(c) — Full ADR-071 owner-anchoring across all resource tables → REJECTED for the bug fix scope.** Full (c) is the right long-term posture — and it's already in flight via #1252. But coupling the beta-blocker bug fix to the full cohort-wide refactor would extend the bug's lifetime. The (c) outcome is BIGGER than #1267 needs; (c) lands incrementally via #1252 itself.

**(a) — Reconcile models + proper migrations → THE RULING, with one fold.** The fold: while we're doing (a) for these 4 tables (ProjectIntegrationDB + project_repository_links + knowledge_nodes + knowledge_edges), bring them into the #1252 D2 consolidating-refactor scope so the owner-anchoring drift gets resolved as the same work-unit. That's (a) executed at the right architectural altitude.

## Concrete shape

For each of the 4 affected tables (ProjectIntegrationDB / project_repository_links / knowledge_nodes / knowledge_edges):

1. **Reconcile model truth — declare `owner_id` in the model class.** This is the source-of-truth alignment (ADR-071 D2 — `owner_id` FK to `users.id` canonical; consolidating refactor scope). Where these tables are user-content (likely all 4 are, though knowledge_nodes/edges may need a closer look — they could be in the PM-domain global-by-design cluster per ADR-071 D1; you have the audit context fresher than I do; ruling: **per-table classification, NOT bulk anchoring**).
2. **Build proper Alembic migrations — kill the create_all path for these tables.** Generate creates via Alembic; remove from `Base.metadata.create_all` invocation if the create_all is selective; remove the table-level `create_all` if it's whole-DB. The `d73b3722eb03` comment hinting at this gets honored by completing the migration-coverage, not by keeping the comment.
3. **Per-table classification per ADR-071 D1**: knowledge_nodes / knowledge_edges may be in the PM-domain cluster (if they represent shared cohort knowledge graph) — apply the `is_global_pm_domain=true` exemption marker per Fire 53 #1238 disposition; alternatively, if they're per-user knowledge graphs, they're standard D2 owner_id-anchored. Your audit + Verify-First check decides.
4. **AST guard composability (ADR-071 D5)**: extend the guard to assert no model is created without its corresponding Alembic migration. This catches the original drift class — "model exists but no migration" is itself an instance of the recurrence PM named. Lint-level catch.

## Sequencing

This is bigger than a one-liner fix but smaller than the full #1252 cohort rollout. Concrete:

- **Phase 1 — Audit & classification** (~30-60 min): per-table classification (PM-domain vs. user-content per ADR-071 D1); model declarations needed; migration scope; create_all retirement scope. Output: a tiny gameplan doc to ground execution.
- **Phase 2 — Implement** (~2-3hr): model edits + Alembic migrations + create_all retirement + cross-table tests (cross-owner scoping on the user-content tables; `is_global_pm_domain=true` on the PM-domain tables per the marker pattern).
- **Phase 3 — Guard extension** (~30-45 min): D5 guard tweak to assert model↔migration coverage; ratchet baseline.
- **Phase 4 — Verify on fresh DB** (~15-30 min): your concrete verification ("fresh throwaway DB → `alembic upgrade head` → tables present + projects API 200") + the cross-owner cross-table tests.

Total scope ~4-6hr. Beta-blocker; not fire-drill (dev unblocked per your note); PM is Time Lord on absolute prioritization vs other queued work.

## Composes with

- **#1252 D2 consolidating refactor** — these 4 tables fold into the same scope. The Phase 2 work IS a #1252 P-something increment; you choose the increment label (P7-and-a-half? P9?).
- **ADR-071 D1 (PM-domain global-by-design exemption)** — knowledge_nodes/edges may be the next concrete instance after #1238 doc-store; pattern application.
- **ADR-071 D5 (m-41 guard pattern)** — extension to model↔migration coverage is the right generalization. Same "make-impossible-by-construction" shape; same AST-guard altitude.
- **Pattern-073 (Documentation-Asserted-Behavior Drift)** — `d73b3722eb03`'s comment hinting at create_all is a sub-instance: the comment described the deviation; the deviation persisted. Flagging for CIO catalog touch if useful.

## decisions.log entry to append

```
2026-06-17 11:15 PT — #1267 projects-table strategy (Arch ruling): (a) folded into (c) via #1252 D2 consolidating refactor — reconcile model truth + proper Alembic migrations + retire create_all path for the 4 affected tables (ProjectIntegrationDB / project_repository_links / knowledge_nodes / knowledge_edges); per-table ADR-071 D1 classification (user-content vs PM-domain); D5 guard extension to model↔migration coverage. Option (b) rejected as m-41 vigilance anti-pattern; full (c) rejected for bug-fix scope (lands incrementally via #1252 itself). — Arch
```

## On the "no fire-drill" framing

Your "dev unblocked; PM is Time Lord on prioritization" framing is correct. PM may want this done today (beta-blocker), or may want it sequenced against other queued work. Per the new "no rush is antipattern" discipline, that's PM's explicit-trigger call to make — not yours or mine to defer with vague framing.

Default lean: **do it next** in your queue unless PM rules otherwise (he sees this memo via cc).

— Architect, 2026-06-17 ~11:15 PT
