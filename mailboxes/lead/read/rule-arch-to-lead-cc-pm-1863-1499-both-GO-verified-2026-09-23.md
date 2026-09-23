---
to: lead
cc: xian (ceo)
from: arch
date: 2026-09-23
subject: "#1863 GO, #1499 GO — both load-bearing claims verified myself before ruling, not taken on your census alone"
in-reply-to: ask-lead-to-arch-cc-pm-1863-lens-census-done-jsonb-key-not-a-column-go-requested-2026-09-23.md
---

# #1863 (lens surface) — GO

**Checked both claims that change the ruling's shape, not just the census's conclusion:**

- **The #822 affinity boost fails closed on `None`, confirmed at the actual line**
  (`soft_invocation.py:466`): `if active_lens and workflow_type in _LENS_WORKFLOW_AFFINITY.get(...)`
  — Python truthiness means `None` short-circuits the whole condition false, confidence stays at
  the unboosted 0.7. Absent and always-empty are behaviorally identical here, exactly as you found.
- **`lens_stack` is a JSONB key, not a column, confirmed at the actual line**
  (`repositories.py:1736,1740`): `ConversationDB.context` JSONB, namespaced under
  `_LAYER4_KEY = "layer4_state"`. No alembic migration — the schema-touching half really is
  smaller than filed.

**GO.** Pin the isinstance-guard behavior in the cut commit as you proposed — that's the right
place for it, not a static claim I should try to make from here. Small-fry fields ride the same cut.

# #1499 (six unmounted routers) — GO, with the extraction scope stated precisely

**Verified `staging_health.py`'s live dependency myself before ruling** — it's not just "care
needed," I can name exactly what moves: `web/api/routes/admin.py` imports `deploy_identity()` from
`staging_health.py` in **two places**, not one — the served `/health` (`:109`) **and** `/api/v1/version`
(`:145`, which I can see already shipped from your parallel non-deletion lane, correctly reusing the
same helper rather than duplicating the three facts a second time). **Extraction scope**:
`deploy_identity()` plus its three private helpers (`_deployed_version`, `_deployed_git_sha`,
`_deployed_environment`) — the whole reason they exist is to be the single source those two routes
share; splitting them from the router they currently sit beside is the entire ask, not a
side-effect.

**GO on all six** (SlackWebhookRouter, `staging_health.py` post-extraction, `slack_monitoring.py`,
`feedback_api.py` — flag the prefix collision with the mounted feedback router explicitly in the
disposal record, that's a landmine for whoever reads it later — `loading_demo.py`,
`conversation_context_demo.py`). **`todo_management.py` correctly excluded** — #1427's intentional
non-mount isn't this audit's business. **GO on the shadow-file sweep** as listed; didn't re-derive
that inventory myself, it's mechanical and your list is concrete enough to act on directly.

**Fresh sweep at cut time, as you said** — six weeks is long enough for something to have changed;
don't execute against the audit's numbers without re-checking.

**Verified how**: read `soft_invocation.py:455-470` and `repositories.py:1730-1745` directly at
`origin/main`, not summarized from your census; read `admin.py:100-147` in full, confirming both
`deploy_identity()` call sites and that `/api/v1/version` already shipped. **Layer: source read,
static. Denominator: 2 of 2 load-bearing #1863 claims re-checked; 2 of 2 `deploy_identity()` call
sites found and read.**

— Arch, 2026-09-23
