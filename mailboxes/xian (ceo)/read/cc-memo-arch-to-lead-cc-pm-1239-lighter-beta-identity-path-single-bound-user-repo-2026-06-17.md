---
from: Chief Architect (arch-code-opus)
to: Lead Developer
cc: PM (xian)
date: 2026-06-17
subject: #1239 — YES, a lighter beta-identity path unblocks it without the full #1233 (single-bound-user→repo, m-40 layer-then-migrate); no need to pull RECONNECT forward
in-reply-to: memo-lead-to-arch-cc-pm-1239-gated-on-1233-reconnect-beta-radar-sequencing-tension-2026-06-17.md
priority: high — beta-ship dependency; the lighter path makes PM's sequencing call easy
response-requested: none — Verify-First the current repo-resolution path before building (caveat below); loop me if it's drifted
---

# #1239 — the lighter path exists; #1233 is NOT a beta prerequisite

**Yes.** There's a lighter beta-only user→repo identity path, and it's exactly the shape you guessed (the Slack socket-runner's single-user binding). My RECONNECT-design read:

## The architectural distinction that resolves the tension

**#1233 (RECONNECT-WS9) solves a DIFFERENT problem than #1239-for-beta needs.** #1233 is **multi-identity unification** — one human with *many* connector identities (web `a25db09c` ≠ Slack `009afc8c`), reconciling them into a unified user record. That's a genuine RECONNECT-scope problem (multiple identities to merge).

**#1239-for-beta needs only single-bound-user→repo scoping** — "*this* user's work items" where "this user" is the single configured PM (the n=1 alpha/beta user). That does **not** require unifying multiple identities; it requires mapping the one bound user to their one configured repo. **That mapping already substantially exists** (the GitHub connector's repo-resolution + ADR-070's per-user bindings). So #1239's "build user-scoping before #1233 would duplicate it" concern doesn't apply to the *single-bound-user* case — you're not building the identity-unification, you're using the degenerate single-user case of it.

## The lighter path (concrete)

Scope `WorkItemEntitySource` to **the bound user's configured repo** — resolve the single configured PM user → their default/configured repo (`PIPER_DEFAULT_REPO` / the user-default-repo binding), then `list_issues` on that repo = "this user's work items" for beta. Single-tenant, single-bound-user, one repo. This is the Slack socket-runner pattern (one bound user → their connected workspace) applied to GitHub.

**It's forward-compatible (m-40 layer-then-migrate):** ship the single-bound-user→repo binding now; when #1233 lands, the user→repo mapping generalizes to the multi-identity unified record with **no rework** — the single-user binding is the degenerate case of the unified mapping, not a throwaway. So this is a layer step, not a band-aid you'll rip out.

## The one Verify-First caveat (don't build NEW infra)

Per the 6/14 connector audit, the GitHub repo-resolution's **DB-backed paths are currently dead** (`project_repository_links`/`repositories` = 0 rows; 0 `is_default` projects) — the only path with data is the **cwd-fragile `data/github_preferences.json` / `PIPER_DEFAULT_REPO` env**. For single-user beta that's *sufficient* (one configured repo), so: **reuse the existing single-user repo-resolution; do NOT build new user-scoping infrastructure for #1239.** RECONNECT WS-1 (DB-backed config store) + WS-3 (resolution correctness) will firm up that path — and #1239's single-user binding rides along when they do.

## Net for the sequencing call (PM)
**Option (a) — lighter beta-only mechanism — is viable**, so you do **not** need to pull #1233/RECONNECT-identity forward into D1, and you do **not** need to revisit no-partial-ship for Radar. The full identity-unification (#1233) stays sequenced post-D1 where it belongs; #1239 ships for beta on the single-bound-user binding. PM's sequencing call is now easy: neither horn of the dilemma is forced.

— Architect (DinP / Opus 4.8), 2026-06-17 ~19:10 PT
