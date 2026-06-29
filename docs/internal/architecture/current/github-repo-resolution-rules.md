# GitHub Repository Resolution Rules (RECONNECT #1327)

**Status**: AS-BUILT (explicit + default tiers live via #1042) · ROADMAP (trust-gated tiers → M4). Doc-of-record per #1327 ("write the rules into a durable doc").
**Owners**: Lead Dev (impl) · Architect (trust-gradient tiers, OQ-2). **Last updated**: 2026-06-29.

## The hierarchy (PM decision 2026-06-28, #1327 Q1)
When a GitHub chat query needs a target (which repo / whose items), resolve in order:

1. **Explicit** — the user named the repo/scope → use it.
2. **Infer + trust-gated** — Piper has a confident inference AND the trust gradient (OQ-2) permits *suggesting* it → suggest. *(M4 — trust-gradient dependency.)*
3. **Ask** — if not inferable/permitted, ask a clarifying question. *(M4.)*
4. **Smart default** — if asking is disallowed (e.g. a standing order against clarifying questions): **default-repo / last-accessed** if one exists, else **get-all** (user-wide).

Plus a meta-feature: Piper can **explain these rules** if asked ("how do you decide which repo?"). *(Later layer.)*

## As-built — what already exists (the verify-before-extend finding)
The backbone is **`services/integrations/github/repo_resolver.py::resolve_repo()`** (Issue **#1042**), a pure, async, per-call decision tree. It already implements the **now-buildable ends** of PM's hierarchy:

| `resolve_repo()` path | maps to #1327 tier | status |
|---|---|---|
| 1. explicit `owner/name` arg | **Tier 1 (explicit)** | ✅ live |
| 2. project-linked repo (by `linked_at`) | a form of *infer* (NOT trust-gated) | ✅ live |
| 2.5. default-project repo (#1192b) | *infer* | ✅ live |
| 3. user `default_repository` (connector_configs DB store, #1226/#1199) | **Tier 4 (default-repo)** | ✅ live |
| 4. `PIPER_DEFAULT_REPO` env (dev escape hatch) | fallback | ✅ live |
| 5. `UnresolvedRepoError` | → Tier 3 ask / honest-degrade hook | ✅ live |

**The get-all bottom is query-type-specific:**
- **Repo-optional** queries (list issues / list PRs / stale PRs) already run **user-wide** (`assignee:@me` / `author:@me`) — the #1322 connector reads. Unresolved → **get-all**. ✅ live.
- **Repo-required** queries (branches / labels / milestones / releases / "issue #N in repo X") cannot get-all → unresolved must **ask / honest-degrade** ("which repo?"), never silent-empty (#1231). `UnresolvedRepoError` is the hook for that.

So the **explicit (1)** and **smart-default (4)** ends of PM's hierarchy are **already built**. Tiers **2–3** (infer-and-*suggest* / *ask*) are the **trust-gated** layer — they depend on the OQ-2 trust gradient and land in **M4** (Architect-owned). The existing project/default-project paths *infer* but resolve **silently** (no suggest/ask) — that is the correct pre-trust-gradient behavior.

## Remaining gaps (#1327 now-buildable, built ON TOP of `resolve_repo()`)
1. **Conversational set-default** — a "set my default repo to owner/name" chat intent → `ConnectorConfigService.set_default_repo`. (The GUI set-default already exists via Settings → `/github/preferences`.) **NEW.**
2. **Connector repo-scoped reads** — branches / labels / milestones / releases via the OAuth connector, resolving the repo through `resolve_repo()` and honest-degrading on `UnresolvedRepoError`. (The connector adapter currently exposes user-wide issues/PRs only.) **NEW.**
3. **Repo-config cutover** (RECONNECT sweep, sibling of #1329) — `/github/repositories` (repo dropdown) + `/github/preferences` are still native-PAT; cut them to the connector binding.
4. **Explain-the-rules meta-feature** — "how do you decide which repo?" renders this hierarchy. Later layer.

## Relationship to #1230
**#1230** ("fix `resolve_repo` + d") is the connector-era resolver-correctness issue; `resolve_repo()` (#1042) **is** that resolver, and it exists and works. #1327 supersedes the connector-era half. **Recommendation (PPM call):** reconcile #1230 into #1327 — the resolver is built; the remaining "correctness" is precisely the gaps above. Avoid carrying #1230 as if the resolver were unbuilt.

## Trust-gradient linkage (Architect / OQ-2, M4)
Tiers 2–3 (infer-and-suggest, ask) require the trust gradient to decide *when Piper may suggest vs must ask vs must stay silent*. That is the OQ-2 design (Architect). Until it lands, the live behavior is: **explicit → silent-infer (project / default-project / user-default) → get-all (repo-optional) or honest-degrade (repo-required)** — a safe subset of the full hierarchy, with no clarifying-question or unsolicited-suggestion behavior yet.
