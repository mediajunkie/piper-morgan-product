---
from: Lead Developer
to: Chief Architect
cc: xian (CEO)
date: 2026-07-08
subject: "#1312 drift inventory complete — three rulings needed before remediation"
---

# #1312 schema-drift audit done — three Arch rulings gate remediation

The full classified inventory is at `docs/internal/architecture/current/schema-drift-inventory-1312.md`
(committed to main today). Short version: env.py model-imports fix landed (autogen now compares
complete metadata; upgrade path verified unaffected — deploy-safe); 241 drift ops classified into
6 buckets; remediation deliberately NOT started with today's alpha deploy pending. The proposed
sequence (§6) starts with a model-side-only pass (no DDL, ~70% of the diff collapses) — that part
I'll run without further ceremony post-deploy. What I need from you are the judgment calls:

## Ruling 1 — Multi-Base (the issue's original Arch flag)
`services/personality/models.py` runs its own `declarative_base()`, so its tables are invisible
to alembic's `target_metadata` entirely. Options: (a) unify onto the shared
`services.database.connection.Base` (one metadata, one authority — my lean, since alembic is
provably the sole live schema authority now that `create_all` has zero callers); (b) register
multiple metadatas with alembic (preserves module independence, more env.py machinery).

## Ruling 2 — `todo_lists`: finish or excise
The audit's headline: `TodoListDB` + 5 indexes + FK re-points (`list_items.list_id`,
`list_memberships`) exist in the MODEL; no migration ever created the table. #479 fixed the
symptom by routing DI around the broken `TodoListRepository` — the orphan is still armed for
whoever touches that class next. The live Todos surface runs on `todo_items` (fine). Options:
(a) **finish** — write the create-migration, un-orphan the repo class; (b) **excise** —
consolidate the todo-list concept onto the live `lists` table (universal_list_repository
already has a compat wrapper) and delete the orphan classes. 75%-pattern rule says pick one;
I lean (b) excise — the universal-list rail is the one that's actually alive — but this is a
product-shape call as much as architecture (PM cc'd for that reason).

## Ruling 3 — The MUX phase-0 family
`conversation_links` (whole table), `conversation_turns.parent_id`, `features.lifecycle_state`,
`todo_items.lifecycle_state` all trace to migration 601 (MUX multichat phase-0): DB-side shipped,
model-side never merged. Autogen proposes DESTROYING all of it. Options per the inventory §7:
(a) park-with-model — declare matching models now so the drift stops and the data stays;
(b) defer-to-MUX-resume — leave the drift, suppress via include_object filter in env.py;
(c) drop with MUX sign-off. I lean (a) park-with-model: cheap, reversible, keeps autogen's
end-state (empty diff) reachable without waiting on the MUX roadmap.

No urgency gate on my side beyond: the model-side-only pass (step 1) doesn't need these rulings;
steps 2–3 (the reconciliation migration) do. Whenever you get to it this week works.

— Lead
