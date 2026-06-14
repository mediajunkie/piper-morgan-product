# Connector Refactor Sprint — Scope

**Status**: DRAFT for PM + Arch review · **Author**: Lead Dev · **Date**: 2026-06-14
**Purpose**: scope the connector-model refactor PM called for, in a shape we can decompose into issues. This is a *scope*, not a full design — it maps the debt, names the workstreams, and surfaces the decisions.

---

## 1. Why now — the trigger and the pattern

**Trigger** (#1226, M3 UAT 2026-06-14): "What should I work on?" returned a generic greeting + "no open issues," despite the repo having many. Root cause was **not** the floor code and **not** the GitHub token (present) — it was **repo resolution finding nothing**, because connector config has no stable home. "Worked the other day, broken now" couldn't be reconstructed because the config is scattered with no traceable source of truth.

**The pattern**: pulling that thread showed this is *not a GitHub bug*. Every connector has the same shape — inconsistent credential storage, cwd-relative flat-file config, ad-hoc resolution, and silent failure. The model has accreted churn (GitHub repo-resolution changed 3× in 5 weeks) and fragile storage. It needs a refactor, not another patch.

---

## 2. Current-state map (grounded, 2026-06-14)

**Connectors**: GitHub · Google Calendar · Slack · Notion · local_git (+ MCP-consumer adapters: `cicd`, `devenvironment`, `gitbook`, `github`, `google_calendar`, `linear`).

### 2a. Credential storage — four connectors, four conventions
| Connector | OAuth-app creds (global) | User token | Scoping pattern |
|---|---|---|---|
| GitHub | `github_client_id` / `github_client_secret` | `github_token` | `username=user_id` |
| Calendar | `google_calendar_client_id` / `_secret` | `google_calendar_{user_id}` | **name-interpolated** (different!) |
| Slack | `slack_client_id` / `_secret` / `slack_app_token` | `slack_bot` | `username=user_id` |
| Notion | — | `notion` (global **and** `username=user_id`) | **ambiguous** (same key both ways) |

Plus the `_api_key`-suffix gotcha (KeychainService appends it; bypassing the abstraction makes creds invisible — already a documented foot-gun in CLAUDE.md). OAuth-app creds, PATs, and OAuth tokens all live in the keychain under ad-hoc conventions.

### 2b. Config / prefs storage — cwd-relative flat files (systemic)
**All four**: `data/{github,calendar,slack,notion}_preferences.json` — read/written relative to the server's launch directory. Not DB-backed, not multi-instance-safe, **silently breaks if the server launches from a different cwd** (the #1226 failure mode). Plus #1199: two competing default-repo stores.

### 2c. Resolution — per-connector, ad-hoc, with dead paths
- GitHub repo: `resolve_repo` (explicit → default-project-linked-repo → user-default prefs → `PIPER_DEFAULT_REPO`). The **default-project path has 0 rows DB-wide** (`project_repository_links` is empty) → dead for everyone; the prefs path is cwd-fragile; env unset.
- Other connectors resolve their target resources ad-hoc, each its own way.

### 2d. Degradation — silent
No-config / no-resolution returns empty ("no open issues") or generic fallbacks instead of an honest "I'm not configured — connect me." The #876 / #1212 honest-degradation principle exists but isn't applied as a connector-wide contract.

### 2e. Connection-state robustness
- Slack OAuth state store is a class-level dict — not multi-process safe (#1109).
- `SlackClient`/`SlackIntegrationRouter` call `get_config()` without `user_id` (#1110, latent).

### 2f. Two parallel models
Native integrations (`services/integrations/{connector}/`) **and** MCP-consumer adapters (`services/mcp/consumer/*_adapter.py`). PM's standing question — "most of these connections should be MCPs probably?" — is filed as **#1220** (BETA→RELEASE: move the integration connection/auth layer to MCP).

---

## 3. Systemic problems (the decomposable themes)

- **P1 — Config has no stable home.** cwd-relative flat files → silent breakage. (#1199, #1226)
- **P2 — Credential model is inconsistent.** 4 conventions, mixed global/user scoping, OAuth-app vs token vs PAT blurred, `_api_key` foot-gun.
- **P3 — Resolution is fragile and has dead paths.** repo resolver + the empty default-project path.
- **P4 — Degradation is silent.** No "connect me" contract; failures look like outages or wrong answers.
- **P5 — No unified connector abstraction.** Every connector reimplements auth/config/resolve/degrade.
- **P6 — First-run / setup UX is not guaranteed.** A user can be in a state where a connector silently resolves nothing.
- **P7 — Connection-state robustness gaps.** (#1109, #1110)
- **P8 — Native vs MCP fork unresolved.** (#1220)

---

## 4. Target principles (what "good" looks like)

1. **One config home** — DB-backed, user-scoped, cwd-independent. No `data/*_preferences.json`.
2. **One credential convention** — provider + optional user scope, a single helper, OAuth-app vs access-token explicit and typed.
3. **A connector contract** — every connector implements the same interface: `connect()` / `status()` / `resolve(resource)` / honest `degrade(reason)`. New connectors become cheap and uniform.
4. **Honest by default** — never silently empty; an unconfigured connector surfaces "connect me," a resolution miss says what's missing.
5. **First-run guarantee** — a connector is either configured-and-resolvable or it tells the user exactly how to connect it.
6. **One target topology** — decide native-vs-MCP (#1220) and align the refactor to it, rather than maintaining two.

---

## 5. Workstreams → issues (the decomposition)

| WS | Workstream | Absorbs / refs | Decomposes into (issue seeds) |
|---|---|---|---|
| **WS-1** | DB-backed config store (kill the flat files) | #1199, #1226 | schema; migrate off `data/*_preferences.json`; read/write API; repo-default lives here |
| **WS-2** | Unified credential model | (CLAUDE.md `_api_key`) | convention doc; KeychainService wrapper; per-connector cred migration; OAuth-app vs token typing |
| **WS-3** | Resolution correctness | #1042, #1192a/b | fix `resolve_repo`; fix-or-remove the empty default-project path; resolution for non-GitHub connectors |
| **WS-4** | Honest-degradation contract | #876, #1212 | a connector `degrade()` contract; apply per connector; "connect me" surfaces |
| **WS-5** | Connector abstraction/interface | — | define the Connector protocol; port 1–2 connectors as proof; then the rest |
| **WS-6** | First-run / setup UX | #1215, #1225 | Settings per-connector audit; connection-status surface; guaranteed-resolvable-or-prompt |
| **WS-7** | Connection-state robustness | #1109, #1110 | Redis-backed OAuth state store; `user_id` propagation |
| **WS-8** | Native-vs-MCP decision + alignment | #1220 | PM/Arch decision; align the abstraction (WS-5) to the chosen topology |

---

## 6. Sequencing / phasing (proposed)

- **Phase 0 — Decide** (gates everything): the **native-vs-MCP fork (#1220)** + Arch review of the target topology. WS-5 and WS-8 can't finalize until this lands.
- **Phase 1 — Foundation**: WS-1 (config store) + WS-2 (creds) — the storage substrate everything else sits on.
- **Phase 2 — Correctness**: WS-3 (resolution) + WS-4 (honest degradation) — make it work and stop lying.
- **Phase 3 — Uniformity + UX**: WS-5 (abstraction) + WS-6 (first-run UX) + WS-7 (robustness).

Meanwhile, the GitHub prefs-file band-aid keeps M3 unblocked — it is explicitly *not* the fix and should be deleted by WS-1.

---

## 7. Open questions (PM / Arch decisions)

1. **Native vs MCP (#1220)** — the biggest fork. Do connectors become MCP consumers, or stay native with a unified abstraction? This gates WS-5/WS-8 and changes the shape of WS-1/WS-2.
2. **Milestone / sprint size** — dedicated connector sprint? Fold into M4 (Trust & Learning) or M5 (polish & distro)? A focused 1-phase slice first?
3. **Multi-tenancy horizon** — must the new model be multi-user / multi-instance-safe now, or single-user-robust first (defer #1109-class concerns)?
4. **Scope breadth** — all four connectors, or GitHub + Calendar first (the M3/M4-relevant pair) with Slack/Notion to follow?

---

## 8. Related issues

Absorbed/anchored: **#1226** (trigger), **#1199** (two stores), **#1109**, **#1110**, **#1220** (MCP). Referenced: #1042 + #1192a/b (repo-resolution history), #1215 (calendar connect), #1225 (module dismiss), #876 / #1212 (honest degradation precedent).

## 9. Decomposition note

This doc is the **umbrella**. Each workstream → 1–N issues. Recommend PM + Arch confirm **Phase 0's MCP fork** and the **phasing/milestone** before filing the issue tree, so we don't decompose against the wrong topology.
