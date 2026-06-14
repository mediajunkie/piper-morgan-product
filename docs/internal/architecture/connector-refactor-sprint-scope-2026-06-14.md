# Connector Refactor Sprint — Scope

**Status**: DRAFT for PM + Arch review · **Author**: Lead Dev · **Date**: 2026-06-14
**Purpose**: scope the connector-model refactor PM called for, in a shape we can decompose into issues. This is a *scope*, not a full design — it maps the debt, names the workstreams, and surfaces the decisions.

---

## 0. DECISION — MCP, not native (PM-ratified 2026-06-14)

**PM ruling**: connectors move to **MCP** (Piper as an MCP *consumer*), not the bespoke per-connector model. Rationale (PM): it's the direction the ecosystem is moving; staying native is "dated and clunky." This **resolves Phase 0 / Open Question #1** below.

**What this means for the refactor:**
- The connector abstraction (WS-5) **is** the MCP-consumer contract — Piper consumes GitHub / Slack / Calendar / Notion via MCP servers rather than bespoke clients. Foundation already exists: `services/mcp/consumer/*_adapter.py` (cicd, devenvironment, gitbook, github, google_calendar, linear).
- WS-8 becomes a **migration**: native `services/integrations/{connector}/` → MCP consumers, retiring the bespoke clients.
- **Auth/config likely shift toward the MCP layer** — if the MCP server owns the connector's OAuth/token, that could *shrink* WS-1/WS-2 (Piper stores per-user MCP-server bindings, not raw creds). This is the key design question for Arch, and it's the part that makes the silent-config-failure class (#1226) go away structurally.

**Ownership**: PM ratified the *direction*; **Arch owns the design + the ADR** — the MCP-consumer substrate, the per-connector migration path, the auth model, and **MCP-server maturity per connector** (GitHub/Calendar are well-served; Slack/Notion need a maturity check — a real input to sequencing). This doc is the input; the ADR is the output.

**Anchor issue**: **#1220** (BETA→RELEASE: move integration connection/auth to MCP) — now the umbrella for this migration.

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
| **WS-8** | Native-vs-MCP decision + alignment | #1220 | PM/Arch decision (✅ MCP, §0); align the abstraction (WS-5) to MCP |
| **WS-9** | **Identity unification** — one human, many connector identities | #1226 (identity finding, 6/14) | confirm web `a25db09c` (xian@pobox.com) vs Slack `009afc8c` = same human (duplicate records?) vs distinct; unify the user record **or** unify config/creds across a user's identities; connector config keys off the unified identity. **Likely a sibling/prerequisite** — connectors sit on identity, so this may need to land first or in parallel. |

---

## 6. Sequencing / phasing (proposed)

- **Phase 0 — Design** (the fork is **decided — §0: MCP**): Arch authors the MCP-migration ADR + designs the consumer substrate (auth model, per-connector migration path, MCP-server maturity per connector). Gates the final shape of WS-1/WS-2/WS-5/WS-8.
- **Phase 1 — Foundation**: WS-1 (config store) + WS-2 (creds) — the storage substrate everything else sits on.
- **Phase 2 — Correctness**: WS-3 (resolution) + WS-4 (honest degradation) — make it work and stop lying.
- **Phase 3 — Uniformity + UX**: WS-5 (abstraction) + WS-6 (first-run UX) + WS-7 (robustness).

Meanwhile, the GitHub prefs-file band-aid keeps M3 unblocked — it is explicitly *not* the fix and should be deleted by WS-1.

---

## 7. Open questions (PM / Arch decisions)

1. ~~Native vs MCP (#1220)~~ — **RESOLVED (§0): MCP, PM-ratified 2026-06-14.** Remaining sub-decision for Arch: how much auth/config moves to the MCP layer vs. stays in Piper.
2. **Milestone / sprint size** — dedicated connector sprint? Fold into M4 (Trust & Learning) or M5 (polish & distro)? A focused 1-phase slice first?
3. **Multi-tenancy horizon** — must the new model be multi-user / multi-instance-safe now, or single-user-robust first (defer #1109-class concerns)?
4. **Scope breadth** — all four connectors, or GitHub + Calendar first (the M3/M4-relevant pair) with Slack/Notion to follow?
5. **Identity unification (WS-9)** — part of this refactor, or a sibling/prerequisite filed separately? The web≠Slack finding (#1226) means connector config fragments per Piper identity, and connectors sit on identity — so this may need to land first or in parallel. PM 6/14 confirmed it must be fixed; Arch to place it relative to the connector work.

---

## 8. Related issues

Absorbed/anchored: **#1226** (trigger), **#1199** (two stores), **#1109**, **#1110**, **#1220** (MCP). Referenced: #1042 + #1192a/b (repo-resolution history), #1215 (calendar connect), #1225 (module dismiss), #876 / #1212 (honest degradation precedent).

## 9. Decomposition note

This doc is the **umbrella**. Each workstream → 1–N issues. Recommend PM + Arch confirm **Phase 0's MCP fork** and the **phasing/milestone** before filing the issue tree, so we don't decompose against the wrong topology.

---

## 10. Proposed issue decomposition (2026-06-14)

**Filing is ADR-gated.** Per §0 + §9, the MCP decision reshapes WS-1/WS-2/WS-5 (auth/config may move to the MCP layer → could *shrink* WS-1/WS-2), and WS-5 **is** the ADR's output. So this section **proposes** the issue tree; we file the new issues *after* Arch's MCP-migration ADR confirms the topology. PM is nudging Arch for that ADR; the one ADR-independent quick win is called out in §10c.

### 10a. Existing RECONNECT issues → workstreams (already filed — PM moved these in 6/14)

The 7 issues now in RECONNECT cover **5 of the 9 workstreams**:

| Issue | Title (short) | Workstream | Note |
|---|---|---|---|
| #1226 | Config has no stable home (trigger) | **WS-1** (+ WS-9 seed) | The trigger / umbrella input; its identity finding (web `a25db09c` ≠ Slack `009afc8c`) seeds WS-9 |
| #1199 | Two default-repo / pref stores | **WS-1** (+ WS-3) | Config-store unification; also touches resolution |
| #1220 | Move connection/auth to MCP | **WS-8** | The §0 anchor — now the MCP-migration umbrella |
| #1109 | Slack OAuth state → Redis | **WS-7** | Connection-state robustness |
| #1110 | SlackClient `get_config()` w/o `user_id` | **WS-7** | Connection-state robustness (latent) |
| #1201 | Slack inbound setup has no product path | **WS-6** | First-run / connect-UX |
| #1227 | Slack outbound renders raw markdown | *(discrete)* | Connector-output correctness — **ADR-independent quick win** (§10c) |

Covered: WS-1, WS-6, WS-7, WS-8 (+ WS-3/WS-9 partially seeded). **Not yet covered by any issue: WS-2, WS-4, WS-5, and the explicit build halves of WS-1/WS-3/WS-9.**

### 10b. Gaps — proposed NEW issues (file *after* the ADR)

Titles are seeds; Arch's ADR decides whether several are children of existing issues vs. new:

1. **WS-2 — Unified credential model** *(no issue yet)* — "Connector credentials: one convention (provider + optional user-scope), single `KeychainService` wrapper, OAuth-app-vs-access-token typed; migrate the 4 connectors off their ad-hoc conventions." **MCP-reshaped**: may shrink to "store per-user MCP-server bindings, not raw creds."
2. **WS-3 — Resolution correctness** *(partial; #1199 is the config-store half)* — "Fix `resolve_repo`; repair-or-remove the dead default-project-linked-repo path (0 rows DB-wide); generalize resolution to non-GitHub connectors." Likely a child or sibling of #1199.
3. **WS-4 — Honest-degradation connector contract** *(precedent: #1212 closed 6/13, #876)* — "Connector `degrade(reason)` contract: never silently empty; an unconfigured/unresolvable connector surfaces 'connect me' / 'here's what's missing.'" Extends the #1212 principle into a connector-wide contract.
4. **WS-5 — MCP-consumer connector contract** *(ADR OUTPUT — file WITH the ADR)* — "Define the MCP-consumer Connector protocol (`connect / status / resolve / degrade`); port 1–2 connectors as proof; then the rest." This is literally what Arch's ADR produces; do **not** file ahead of it.
5. **WS-9 — Identity unification** *(finding in #1226; likely prerequisite)* — "Confirm web `a25db09c` vs Slack `009afc8c` = same human; unify the user record (or unify config/creds across a user's identities); connector config keys off the unified identity." Connectors sit on identity → may need to land first or in parallel.

Optionally-explicit build issues (currently folded into the trigger/input issues, may stay folded): a **WS-1 build issue** ("DB-backed connector-config store; migrate off `data/*_preferences.json`; delete the prefs band-aid") distinct from #1226-the-trigger; a **WS-6 connector-status surface** broader than #1201's Slack slice.

### 10c. The one thing we can do now (ADR-independent)

**#1227** (Slack outbound renders `**` / `#` raw instead of Slack mrkdwn) is a pure output-formatting bug in the Slack reply path — independent of the MCP decision and the rest of the refactor. It can ship as a standalone quick win anytime (the Slack MCP migration will inherit it, but it doesn't need to wait). Everything else in §10b waits for the ADR.

### 10d. Summary

- **RECONNECT is mostly already filed** — 7 issues, 5 workstreams covered.
- **New issues needed for WS-2 / WS-4 / WS-5 / WS-9** (and explicit WS-1/WS-3 build issues) — **proposed here, filed after the ADR** (the MCP decision reshapes them).
- **#1227 is the only piece shippable today** without the ADR.
