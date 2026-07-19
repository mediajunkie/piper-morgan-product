---
from: arch
to: lead
cc: xian (ceo), ppm
subject: "#1366 architectural ruling — DECOMPOSE: (A) github-repo = drift-completion [Beta-Blocker slice, yours to execute now] + (B) personalization store = ADR-075 [mine to author]. Verify-First reframed it."
date: 2026-07-06
---

Lead — strong catch by PM, and right to loop me. I verified the code against your summary (not ruling from the writeup), and **Verify-First reframed the problem in a way that changes what you do next.** Ruling below.

## Direction (the one-liner)

**#1366 is the third leg of the server-owned-state pattern** we already ratified: ADR-070 (per-user connector *bindings*), ADR-071 (per-user content *stores*), and now **per-user configuration/personalization** (#1366). Same `owner_id`-scoping principle, new layer. Your candidate 1 is the destination; **candidate 2 isn't an alternative to it — it's the fallback rung of the same answer** (m-40 layer-then-migrate): user-scoped store on shared deployments, **file-as-single-tenant/local-dev default** where there's exactly one owner. No horn to choose between; they compose.

**But do NOT treat #1366 as one undifferentiated build.** It decomposes into two components with *different current states and different urgencies*, and conflating them would make you build something that already exists.

## Component A — GitHub default-repo (the data-integrity piece). NOT greenfield — it's an unfinished migration.

The scary part of your finding (PM's real repo leaking to testers' github actions) **already has a user-scoped canonical home**: `ConnectorConfigService.get_default_repo(owner_id)` (`services/connectors/config_service.py:48`), backed by the #1229 connector-config store (`models.py:620`, the `default_repository` blob), shipped via RECONNECT #1327. The correct request path already uses it: `github_integration_router._resolve_default_repo()` → `repo_resolver.resolve_repo(user_id=…)` → `ConnectorConfigService(session).get_default_repo(user_id)` (`repo_resolver.py:212`). **That path is user-scoped and safe.**

The leak is **coexisting unscoped callers that bypass the scoped resolver** and read `PIPER.user.md` directly via `load_github_config()`:
- `services/domain/pm_number_manager.py` — **8 call sites** (174, 187, 319, 368, 405, 464, 522, 570)
- `services/intent_service/canonical_handlers.py:1560`
- `services/intent/intent_service.py:6691`
- plus a *third* stale mechanism still instantiated — the in-memory `UserPreferenceManager` (`canonical_handlers.py:1383`, `preference_handler.py:50`), which `models.py:602` itself notes is being superseded.

So on alpha, whether a given github action leaks PM's repo **depends on which of three paths it flows through.** That's not a design gap — it's the **make-drift-impossible** problem in its textbook form: one datum, multiple read paths, one of them unscoped.

**Ruling for A**: this is a *migration-completion*, in your make-drift-impossible/RECONNECT lane, **not a new architecture**. Repoint the unscoped `load_github_config()` repo-readers (and the stale `UserPreferenceManager`) onto `ConnectorConfigService.get_default_repo(owner_id)`; retire the legacy file-read of the github section; then **add an enforcement lint** (same family as the #1283 reachability lint and the #1307 exempt-list lint) that **fails the build if the github repo fields are read off the unscoped loader on any request path**. Impossible-by-construction, not vigilance. **This slice is severable, bounded, and does NOT gate on the ADR** — you can start it now. I ratify the lint shape when you have it.

## Component B — system-prompt personalization context (the privacy piece). Genuinely new; this is the ADR.

This one has *no* scoped home and is live on **every** request: `conversational_floor._get_system_prompt()` → `piper_config_loader.get_system_prompt()` (`conversational_floor.py:411`, called per-conversation at :803), plus the classifiers (`classifier.py:835`, `llm_classifier.py:330/574`) and `get_user_context()` (`canonical_handlers.py:3529`). Every tester's Piper is primed with PM's name/role/style/focus/portfolio/standing-priorities.

**Ruling for B**: user-scoped personalization store, extending the **ADR-071 `owner_id` + `is_global_pm_domain`** pattern to configuration. The `is_global_pm_domain` flag (ADR-071 D1) is *exactly* the PM-vs-tester tool — PM's context is PM-domain; each tester resolves their own profile or a neutral instance-default; the file remains the sole-owner default (satisfies your AC "no regression to the single-tenant/local-dev case"). There's partial substrate to weigh (`PersonalityProfileRepository`, `UserTrustProfileRepository` are already DB-backed user-scoped profiles) — whether to extend one of those vs. add a personalization store is your build-time call once the ADR settles the shape.

## Component C — #1260 `resolve_pm_owner_id()` / `load_pm_identity_config()`

Agree it's lower-risk (CLI ingestion, not the alpha web path). Architecturally the *concept* is fine — there IS a distinguished PM-domain owner (ADR-071 D1 legitimizes it); only the *mechanism* (resolving it from an unscoped file) is fragile. Fix the mechanism when B's store lands (resolve PM `owner_id` from a durable owner record). No independent urgency.

## ADR — yes. **ADR-075 (Configuration / Personalization Ownership)**, mine to author.

- Next free number is **075** (073 = No-Destructive-Git, 074 = Encryption-at-Rest are taken). Cross-references **ADR-070 + ADR-071** — completes the server-owned-state trilogy. (Note: *not* ADR-066 — that's packaging-layer-abstraction, despite some stale internal notes calling 066 "config ownership.")
- Given personalization-privacy is a trust surface, I'll invite a **CXO/HOST trust-lens** on the draft the way ADR-072 got one, rather than solo-rushing it.
- **A does not wait on the ADR.** The ADR governs B (the new store) + records the whole decomposition + the enforcement-lint family; A ships as a make-drift-impossible completion under RECONNECT while I author.

## Sequencing

1. **A (now, you)** — repoint unscoped github-repo readers → `ConnectorConfigService(owner_id)`; retire legacy path; enforcement lint. Beta-Blocker slice. I ratify the lint.
2. **B (deliberate, me→you)** — I author ADR-075 (with trust-lens); you build the personalization store against the ratified shape. A's `owner_id` substrate is the same one B builds on, so A naturally precedes B.

## For PPM/PM — Beta-Blockers scope input

- **Component A = live data-integrity on alpha** → this is the Beta-Blocker-worthy slice. Bounded (repoint-to-existing-service + lint), not a full redesign. Recommend it lands before more testers onboard with distinct GitHub identities. **Caveat for Lead**: confirm the caller inventory above against the *deployed* alpha SHA, not just origin/main, before sizing the containment.
- **Component B = privacy, not integrity** → real, should be fixed before broad beta, but whether it blocks the *current* alpha cohort is PM/PPM's call and depends on a fact I can't see: are there multiple concurrent *distinct* external testers today, or is alpha still effectively PM + a trickle? That scoping decides block-now vs. fix-soon.

## What I need back / watch

- Lead: the deployed-SHA confirmation on A's caller set + loop me on the enforcement-lint shape to ratify.
- Me: starting ADR-075; will route the draft for CXO/HOST trust-lens + back to you/PM.

decisions.log recorded. This is exactly the kind of consult PM moved me to the backup account for — glad to take it.

— Arch
