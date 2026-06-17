---
from: Lead Dev (lead-code-opus)
to: Chief Architect
cc: PM (xian)
date: 2026-06-17
subject: #1267 — projects-table create_all-vs-migrations + owner_id model↔migration drift (Beta-blocker, strategy call)
response-requested: pick the strategy (a/b/c) so I can implement + verify the durable fix
---

# #1267 — projects 500 on clean DBs; the durable fix is an architecture call

**Bug (PM UAT 2026-06-17)**: `GET /api/v1/projects` 500s on any DB where `project_integrations` doesn't exist (i.e. any clean dev / staging / **prod** built via `alembic upgrade head`). `list_active_projects` selectinloads the integrations → `UndefinedTableError`. I dev-repaired our DB (`create_all` the two missing tables) → **dev unblocked**. The durable fix landed in your domain.

**Two entangled issues** (full detail + evidence on #1267):
1. **create_all-vs-migrations.** `project_integrations`, `project_repository_links` (and `knowledge_nodes`/`knowledge_edges`) are created via **`create_all`, not migrations** — per `d73b3722eb03`'s own comment, and the alter-migrations guard with `IF EXISTS`. But the documented setup (`main.py:408`) is `alembic upgrade head` alone, which never runs `create_all` → tables missing on clean installs.
2. **owner_id model↔migration drift.** `4d1e2c3b5f7a` (SEC-RBAC #357) ADDs `owner_id UUID FK→users` to these tables, but the **models don't declare `owner_id`** (`ProjectIntegrationDB`, `project_repository_links` have no such field). So `create_all` builds them WITHOUT owner_id; the alter adds it only if the table pre-existed. The schema you get depends on create_all-vs-alter ordering. (My repair used `create_all` → created them WITHOUT owner_id; the list query doesn't read it so projects works, but the drift is latent.)

**Your call** (ADR-071 / SEC-RBAC owner-anchoring territory, spans several resource tables — not a unilateral Lead migration):
- **(a)** Reconcile the models to declare `owner_id` + add proper create-migrations → migration-managed.
- **(b)** Keep create_all-managed, but enforce `create_all` in setup/deploy (operational fix).
- **(c)** ADR-071-align owner-anchoring across all these resource tables (the broader fix).

Pick one and I'll implement + verify on a fresh throwaway DB (`alembic upgrade head` → tables present + projects API 200). **Beta-blocker** (projects broken on clean installs) so it shouldn't sit — but dev's unblocked, so no fire-drill (Time Lord). Detail: #1267.

— Lead Dev
