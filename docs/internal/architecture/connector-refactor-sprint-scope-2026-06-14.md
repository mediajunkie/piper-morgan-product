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

Plus the `_api_key`-suffix gotcha (KeychainService appends it; bypassing the abstraction makes creds invisible — already a documented foot-gun in CLAUDE.md). OAuth-app creds, PATs, and OAuth tokens all live in the keychain under ad-hoc conventions. **Audit nuance (2026-06-14)**: GitHub isn't the "clean" one — besides `github_token` (`username=user_id`), a stale third reader uses the bare key `get_api_key("github")` (no `_token`, no username) as a config pre-flight in `intent_service.py:6254/6416`, hitting a *different* keychain account than where the token lives. WS-2 should sweep that up.

### 2b. Config / prefs storage — cwd-relative flat files (systemic)
**All four**: `data/{github,calendar,slack,notion}_preferences.json` — read/written relative to the server's launch directory. Not DB-backed, not multi-instance-safe, **silently breaks if the server launches from a different cwd** (the #1226 failure mode). Plus #1199: two competing default-repo stores.

> **UPDATE 2026-06-21 (WS-1 #1199/#1226):** the **GitHub** config is now fully DB-backed — the canonical home is the `connector_configs` table (ADR-070 D4), keyed by `owner_id`. The flat-file `data/github_preferences.json` AND the in-memory `UserPreferenceManager` default-repo store are **RETIRED**: every surface (settings UI read/write, chat `resolve_repo`, standup) now reads/writes the single DB store, end-to-end-verified against real Postgres. The #1199 two-competing-stores problem is **CLOSED**; `UserPreferenceManager.set_default_repo` was removed and `get_default_repo` is DB-only. The `calendar/slack/notion` flat files remain (future workstreams).

### 2c. Resolution — per-connector, ad-hoc, with dead paths
- GitHub repo: `resolve_repo` has **five** paths (audit-corrected 2026-06-14): explicit → explicit-`project_id`-linked → default-project-linked → user-default prefs (`data/github_preferences.json`) → `PIPER_DEFAULT_REPO` → else `UnresolvedRepoError`. **All three DB-backed paths are dead DB-wide** (verified live, port 5433): `project_repository_links` = 0 rows, `repositories` = 0 rows, and 0 projects have `is_default=True`. The prefs path is cwd-fragile (present in the worktree, absent from the main checkout); env unset. → **the cwd-fragile flat file is the ONLY resolution path with data.**
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

**Related ADRs (audit 2026-06-14 — see §11):** **ADR-058** (Multi-Tenancy Isolation, APPROVED) already decided the credential / OAuth-state / user-scoping model that WS-2/WS-7/WS-9 re-encounter — *much of this refactor is finishing ADR-058's incomplete implementation, not greenfield.* **ADR-001** (MCP Integration Pilot, Accepted — "Piper as MCP consumer") **supports** the §0 direction. **ADR-052** (Tool-Based MCP Standardization, Accepted — chose tool-based, *rejected* separate MCP servers) is in **tension** with "external MCP server owns auth" and **must be explicitly reconciled** by the WS-5 ADR (#1232). **ADR-066 D7** (Configuration Ownership Convention, drafted 2026-06-14 — Arch) rules config/credential durability is **server-owned** (the host does per-request *ephemeral* augmentation only; config never crosses host↔server as durable state). This **governs WS-1** (the DB-backed config store realizes D7 — no host/cwd-relative flat files; that's a host-filesystem assumption D7 forbids) and **WS-2** (credential *references* are server-owned, ADR-058-precedented). Future **Lead Dev consult — D7 OQ-1** (when does server-owned config materialize vs. handshake; lean: per-session at first post-handshake request) lands when Skunkworks BYOC Phase 2a scopes.

## 9. Decomposition note

This doc is the **umbrella**. Each workstream → 1–N issues. Recommend PM + Arch confirm **Phase 0's MCP fork** and the **phasing/milestone** before filing the issue tree, so we don't decompose against the wrong topology.

---

## 10. Issue decomposition — FILED 2026-06-14

**Status: FILED** (PM-authorized 2026-06-14). All 9 workstreams now have ≥1 issue on the RECONNECT sprint, prefixed `RECONNECT-WS{n}:` on the board. **New issues: #1229 (WS-2), #1230 (WS-3), #1231 (WS-4), #1232 (WS-5), #1233 (WS-9)**; the existing 7 were renamed to the same prefix. **The ADR still shapes scope** — the MCP decision (§0) may *shrink* WS-1/WS-2 (auth/config moving to the MCP layer), and **WS-5 (#1232) is literally the ADR's output** — so treat these as the tracking targets Arch's ADR attaches to and refines, not frozen specs. The one ADR-independent quick win is §10c.

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

### 10b. NEW issues — FILED 2026-06-14

Each filed on the RECONNECT sprint (MVP / Product Backlog), body cross-refs the scope doc; the ADR refines scope:

1. **WS-2 — Unified credential model** → **#1229** — "Connector credentials: one convention (provider + optional user-scope), single `KeychainService` wrapper, OAuth-app-vs-access-token typed; migrate the 4 connectors off their ad-hoc conventions." **MCP-reshaped**: may shrink to "store per-user MCP-server bindings, not raw creds."
2. **WS-3 — Resolution correctness** → **#1230** (storage half is #1199, WS-1) — "Fix `resolve_repo`; repair-or-remove the dead default-project-linked-repo path (0 rows DB-wide); generalize resolution to non-GitHub connectors."
3. **WS-4 — Honest-degradation connector contract** → **#1231** — "Connector `degrade(reason)` contract: never silently empty; an unconfigured/unresolvable connector surfaces 'connect me' / 'here's what's missing.'" Extends #1212 (closed) into a connector-wide contract.
4. **WS-5 — MCP-consumer connector contract** → **#1232** (the ADR's build target) — "Define the MCP-consumer Connector protocol (`connect / status / resolve / degrade`); port 1–2 connectors as proof; then the rest." Arch's ADR attaches here.
5. **WS-9 — Identity unification** → **#1233** (likely prerequisite) — "Confirm web `a25db09c` vs Slack `009afc8c` = same human; unify the user record (or unify config/creds across a user's identities); connector config keys off the unified identity."

Still open (Arch's ADR decides if needed): an explicit **WS-1 build issue** (DB-backed config store; migrate off `data/*_preferences.json`; delete the prefs band-aid) distinct from #1226-the-trigger; a **WS-6 connector-status surface** broader than #1201's Slack slice.

### 10c. The one thing we can do now (ADR-independent)

**#1227** (Slack outbound renders `**` / `#` raw instead of Slack mrkdwn) is a pure output-formatting bug in the Slack reply path — independent of the MCP decision and the rest of the refactor. It can ship as a standalone quick win anytime (the Slack MCP migration will inherit it, but it doesn't need to wait). Everything else in §10b waits for the ADR.

### 10d. Summary

- **RECONNECT = 12 issues, all 9 workstreams covered**, prefixed `RECONNECT-WS{n}:` (MVP / Product Backlog).
- **Filed 2026-06-14**: #1229 (WS-2), #1230 (WS-3), #1231 (WS-4), #1232 (WS-5 = ADR output), #1233 (WS-9). Existing 7 renamed.
- **The ADR (Arch, in progress) refines scope** — esp. WS-2 / WS-5 / WS-1 (how much auth/config moves to the MCP layer).
- **#1227 is shippable today** without the ADR (the quick win).

---

## 11. Audit grounding (2026-06-14)

A 5-agent audit cascade independently verified every claim in the 12 RECONNECT issues + the #1223 fix + #1234 against actual code / live DB / docs (try-to-refute stance). **Verdict: well-grounded — nothing fabricated; the load-bearing empirical claims verified true, several understated.**

**Verified (stronger than originally stated):**
- `project_repository_links` = 0 rows AND `repositories` = 0 rows AND 0 `is_default` projects (live DB) → all three DB-backed resolution paths dead, not just default-project.
- §2a credential table accurate connector-by-connector; `_api_key` suffix, 6 MCP-consumer adapters (`cicd/devenvironment/gitbook/github/google_calendar/linear`), Slack class-level OAuth dict, and `get_config()`-without-`user_id` all confirmed at file:line.
- No unified `Connector` protocol exists (`connect/status/resolve/degrade` = 0 matches) → WS-5 genuinely greenfield.
- Both identity records real (live DB): `a25db09c` = xian / xian@pobox.com (web); `009afc8c` = m1-test / m1t@dinp.xyz (Slack, active 6/14). Config keyed by `user_id` → fragmentation real. **Note**: "same human" is plausible but *not proven* — different usernames/emails, one reads as a test account; WS-9 already carries this as an open question.

**Corrections applied to this doc:** §2c `resolve_repo` order (5 paths, not 4) + DB-dead strengthening; §2a stale 3rd GitHub reader.

**Most important finding — grounding gap (→ Arch, for the WS-5 ADR):** the issues/scope don't cite the ADR corpus that governs them. **ADR-058** (Multi-Tenancy Isolation) already settled the WS-2/7/9 cred/OAuth/user-scoping model — much of RECONNECT is *finishing ADR-058*, not greenfield; cite it so Arch doesn't re-derive. **ADR-001** supports the MCP-consumer posture. **ADR-052** (tool-based MCP, no separate servers) must be reconciled with "external MCP server owns auth." The §0 MCP decision should also be appended to `decisions.log` (reinstated 6/13; this is its exact use case).

**New latent bug (out of #1223/#1234 scope, filed separately):** the `/{conversation_id}/turns` display endpoint (`web/api/routes/conversations.py:182`, default `limit=50`, **no offset param**) returns the *oldest* 50 turns of a >50-turn conversation — same wrong-window shape as #1223, lower severity (display, not LLM context).

---

## 12. BYOC reconciliation + sequencing decision (a) — PM-ratified 2026-06-20

After PA's Skunkworks BYOC Phase-2a scoping (2026-06-19: the `byoc-stack-2026-06-19.html` / `byoc-nearterm-work-2026-06-19.html` diagrams + the ratified identity decision), Lead Dev + PM reconciled RECONNECT against it. This **resolves the §8 parked hook** ("D7 OQ-1 lands when Skunkworks BYOC Phase 2a scopes").

> **⚠️ CORRECTION (2026-06-20, PM-approved) — read as authoritative where it conflicts with the decision-a text below.**
> The "**#1162 = cred-decoupling**" label below is **wrong**. Reading the live issues revealed **#1162 is `SKUNKWORKS-BYOC-HOSTED-DISTRO` — hosted-distro *exploration*** (a distribution concern, like #1278/#1282), **not** cred-decoupling. The buildable cred-decoupling work (PA's option-a plan, `dev/2026/06/07/pa-option-a-decouple-credential-plan-2026-06-07.md`) had **no tracking issue** — now filed as **#1300** (`BYOC-CRED-DECOUPLE`).
> **Board corrected 2026-06-20**: **#1162 → SKUNK** (out of RECONNECT), **#1300 → M5**, **#1278 stays M5**, **#1185 stays RECONNECT** (identity core). The internal inconsistency that flagged it: decision-a kept #1278 out as "hosting = distribution-lane," but #1162 is hosting too.
> **Corrected Phase-0 foundation = #1185 (identity core) + #1229 (RECONNECT-WS2 cred-model, already native)**; the hosting/distribution cluster (#1162 / #1278 / #1282 / #1300) lives in SKUNK / M5, to be organized "when we get to M5" (PM 2026-06-20).

**Boundary:**
- **RECONNECT owns** the connector framework (WS1–WS8) + the BYOC-identity-*keying* for connectors (WS9).
- **The BYOC backend owns** the hosting + multi-tenant identity/auth/session substrate: **#1278** (Fly deploy), **#1185** (UUID-bearer auth + per-user identity/session/data/knowledge isolation — *finishing ADR-058*), **#1162** (cred-decoupling).

**Decision (a) — PM-ratified 2026-06-20:** the BYOC backend *foundation* — **#1162 (cred-decoupling, "unblocks everything") + the #1185 identity core** — is pulled **INTO RECONNECT as its Phase-0/1 foundation** (vs. sequencing RECONNECT after a separate BYOC sprint). Rationale: they are the substrate the whole connector refactor sits on; splitting them across sprints invites exactly the config-drift RECONNECT exists to kill. **#1278 (Fly hosting) stays distribution-lane** — it's a hosting concern, not a connector-framework one. **PM is reassigning #1162 + #1185 onto the RECONNECT sprint.**

**WS-9 reframe:** identity is now a **UUID-bearer issued at first connect** (#1185, MVP) → email + magic-link (1.0). So WS-9 (#1233) is no longer "merge legacy web `a25db09c` / Slack `009afc8c`" — it becomes **"key connector config to the BYOC identity model,"** a *downstream consumer* of #1185. The two legacy records are a migration detail, not the WS core.

**Updated phasing:** Phase 0 (Arch ADR-070 + **#1162** cred-decoupling + the **#1185** identity core) → Phase 1 (WS1 config store + WS2 creds, on the BYOC identity) → Phase 2 (WS3 resolution + WS4 degradation) → Phase 3 (WS5 protocol ports + WS6 connect-UX + WS7 robustness + WS8 native→MCP migration).

**Next:** loop Architect — (a) shapes ADR-070's phasing + makes #1162/#1185 explicit Phase-0/1 dependencies. Recorded in `decisions.log`.
