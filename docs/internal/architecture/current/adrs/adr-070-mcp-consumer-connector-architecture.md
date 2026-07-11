# ADR-070: MCP-Consumer Connector Architecture

**Status**: v0.1 (filed 2026-06-15) — Architect-authored; PM-ratified direction (2026-06-14: connectors move to MCP-consumer; staying native is "dated and clunky"); gates Lead Dev WS-1..9 decomposition on the RECONNECT sprint (#1220 umbrella + 12 issues).

**Date**: 2026-06-15

**Authors**: Chief Architect (Arch)

**Reviewers**: Lead Developer (RECONNECT sprint owner; #1220 anchor + 11 WS issues), PPM (milestone placement), CIO (methodology), CEO (xian — direction ratifier)

---

## Status

- **v0.1** filed 2026-06-15 from Lead Dev's input doc `docs/internal/architecture/connector-refactor-sprint-scope-2026-06-14.md`.
- Unblocks WS-1..9 decomposition. Lead Dev was waiting for topology before refining the issue tree past initial filing 2026-06-14.
- ADR-058 (Multi-Tenancy Isolation, APPROVED) finishes-the-job framing: much of RECONNECT is completing ADR-058, not greenfield. ADR-052 (Tool-Based MCP Standardization) requires explicit reconciliation — done in D2. ADR-066 D7 (Configuration Ownership) governs WS-1; ADR-071 (User-Auth Anchoring, Lead-authoring) composes at the auth/identity layer.
- No M3 dependency (M3 closes independently); this is M4/M5 (PPM places milestone).

---

## Context

### What problem does this ADR solve?

PM ratified (2026-06-14) that Piper's connector model moves to MCP-consumer rather than native bespoke integrations. The ratification settled the **direction**; this ADR settles the **how** — specifically the four questions Lead Dev's input doc identified as Arch's lane:

1. **MCP-consumer substrate shape** — what does the connector abstraction look like in MCP-consumer form?
2. **Auth ownership** — how much of OAuth/token lifecycle moves to the MCP server vs. stays in Piper?
3. **Per-connector migration path** — how does each native integration transition without breaking M3?
4. **MCP-server maturity per connector** — sequencing input given uneven server maturity (GitHub/Calendar well-served; Slack/Notion gap analysis needed).

The trigger artifact is #1226 (M3 UAT silent-config-failure) — a `data/github_preferences.json` cwd-relative flat-file that returned "no open issues" for a repo with many. Pulling the thread surfaced the systemic shape (P1-P8 in the scope doc): cwd-fragile config storage, four-conventions credential model, fragile-with-dead-paths resolution, silent degradation, no unified connector abstraction.

### Why this is architectural, not a per-connector patch

PM's framing — "not our first attempt" at clean connector models — is the recurrence signal. The same family of failure mode that drove ADR-071 (content anchoring) drives this ADR (connector substrate): without a canonical pattern, each new connector or each new fix re-invents (or fails to invent) the discipline. Patching `data/github_preferences.json` to be DB-backed without a connector-wide contract just defers the next variant.

### Format-decision space (inherits from existing ADRs)

- **ADR-001** (MCP Integration Pilot, Accepted) supports the MCP-consumer posture.
- **ADR-052** (Tool-Based MCP Standardization, Accepted) chose tool-based at the Piper-as-host boundary, rejecting separate MCP servers. This is in *apparent* tension with "external MCP server owns auth" — resolved in D2 below as two distinct boundaries with no actual conflict.
- **ADR-058** (Multi-Tenancy Isolation, APPROVED) already settled credential storage convention + OAuth-state isolation + user-scoping. Much of WS-2/WS-7/WS-9 finishes ADR-058, not greenfield. Cross-reference per D9.
- **ADR-066 v0.2 D7** (Configuration Ownership Convention, drafted 2026-06-14) rules configuration durability is server-owned, host augments per-request. Governs WS-1 (DB-backed config realizes D7) + WS-2 (credential references server-owned).
- **ADR-071 candidate** (User-Auth Anchoring Pattern, Lead-authoring from #1241 audit) composes at the identity/auth-resolution layer.

### Prior art / cross-references

- PDR-005 v1.0 (BYOC) — informs the multi-tenancy horizon decision.
- Pattern-072 (Registries that Grow into Architectural Shapes) — the MCP-server-binding registry is likely 9th application.
- Pattern-073 (Documentation-Asserted-Behavior Drift) — doc-sync-sweep applies at the per-connector contract layer.
- methodology-30 (Consumer-Trace Verification) — what would catch the silent-config-failure class.
- methodology-38 (PDR/ADR Tier Separation) — this is implementation-altitude ADR; the *direction* was PM's product-altitude call.
- methodology-40 (Layer-Then-Migrate, Proven) — D7 migration shape.
- methodology-41 (Mechanism Displaces Unreferenced Discipline, Proven) — D5 connector contract guard pattern.

---

## Decision

The MCP-Consumer Connector Architecture is **a unified `Connector` protocol (`connect / status / resolve / degrade`) implemented by MCP-consumer adapters + DB-backed user-scoped config (replacing cwd-relative flat files) + MCP-server-owned OAuth/token lifecycle (with Piper storing per-user MCP-server bindings, not raw credentials) + a maturity-tiered per-connector migration sequenced via m-40 layer-then-migrate**. Native `services/integrations/*` retire as MCP-consumer adapters reach parity.

### D1: Architectural shape — Piper as MCP consumer

**Decision**: Piper's connector substrate is the existing `services/mcp/consumer/*_adapter.py` foundation. Native `services/integrations/{connector}/` is deprecated; new connector work targets MCP-consumer adapters exclusively. The MCP-consumer protocol IS the connector abstraction (WS-5 = the MCP-consumer contract; not two separate things).

This is the PM-ratified direction, made concrete: the connector lane unifies on one substrate. The bifurcation that drove P8 in Lead's scope doc (`services/integrations/{connector}/` and `services/mcp/consumer/*_adapter.py` coexisting) ends with native retirement.

### D2: ADR-052 reconciliation — two distinct boundaries

**Decision**: ADR-052's tool-based MCP standardization applies to **Piper-as-host** (Piper exposing its own tools to MCP clients like Claude Desktop). ADR-070 applies to **Piper-as-consumer** (Piper consuming external tools/resources from MCP servers like github-mcp-server). These are **two distinct boundaries**, not in tension:

| ADR | Boundary | Direction | Owns |
|---|---|---|---|
| ADR-052 | Piper-as-host | Piper exposes tools to MCP clients (Claude Desktop, ChatGPT-MCP, etc.) | Piper's tool surface; tool-based standardization; no separate MCP servers in front of Piper |
| ADR-070 | Piper-as-consumer | Piper consumes tools/resources from external MCP servers | The external server owns auth + the underlying resource; Piper stores bindings only |

ADR-052's "rejected separate MCP servers" applied to Piper's tool surface (don't fragment Piper's API across multiple servers). It did not apply to consuming external servers. The ADRs compose cleanly.

### D3: Auth ownership split — MCP server owns OAuth; Piper stores bindings only

**Decision**: The external MCP server (github-mcp-server, google-calendar-mcp-server, etc.) owns the connector's OAuth flow, token storage, and token refresh lifecycle. Piper stores **only**:
- Per-user MCP-server bindings (which MCP server identity, which user identity, which connector type)
- Server-binding metadata (URL/endpoint reference, capability profile, last-known-status)

Piper does **not** store:
- Raw OAuth tokens for connector resources
- Connector-specific refresh tokens
- OAuth-app client_id/client_secret for connector providers

This **structurally eliminates the silent-config-failure class** (#1226): if the binding exists and the MCP server is reachable, the connector is configured. The four-conventions credential model (P2) collapses to one convention: server-binding-by-user. The `_api_key` keychain foot-gun (CLAUDE.md) reduces to MCP-server-internal concerns, not Piper's discipline.

**Cross-reference**: ADR-066 v0.2 D7 (Configuration Ownership) makes this the consistent posture across server-owned-config and server-owned-creds. ADR-058 (Multi-Tenancy Isolation) credential storage convention applies to Piper's binding storage (per-user scoping per ADR-058).

### D4: Config ownership — DB-backed, user-scoped (kills cwd-relative flat files)

**Decision**: All per-user connector configuration lives in Piper's DB, user-scoped per ADR-058. The `data/*_preferences.json` flat files are retired by WS-1. The DB schema for connector config carries:
- `user_id` (FK per ADR-058 + ADR-071 D2 canonical `owner_id` FK convention)
- `connector_type` (enum: github, calendar, slack, notion, ...)
- `mcp_server_binding_id` (FK to the server-binding registry — D5)
- Per-connector preferences (default repo, default calendar, etc.) as typed JSON or sub-tables

**Cross-reference**: ADR-066 D7 enforces this — host-filesystem persistence is forbidden; server-owned-DB is the canonical home. ADR-071 (Lead-authoring) D2/D3 invariants apply to read/write paths on this config (owner-stamped at write; principal-scoped at read).

### D5: Connector abstraction — single protocol, four methods

**Decision**: One `Connector` protocol that all MCP-consumer adapters implement:

```python
class Connector(Protocol):
    async def connect(self, user_id: str) -> ConnectResult: ...
    async def status(self, user_id: str) -> ConnectorStatus: ...
    async def resolve(self, user_id: str, resource: ResourceQuery) -> ResolveResult: ...
    async def degrade(self, reason: DegradationReason) -> DegradationResponse: ...
```

- **`connect`** initiates the user's OAuth flow against the connector's MCP server; returns a binding or a `ConnectRequired` honest-degradation response.
- **`status`** reports the binding's current health (bound / unbound / unreachable / stale-token-needs-refresh) without performing a resource fetch.
- **`resolve`** maps a resource query (e.g., "the user's default GitHub repo") to a concrete resource handle via the bound MCP server.
- **`degrade`** is the honest-degradation contract: returns `"connect me"` for unbound, `"resource not found"` for resolve-misses, etc. **Never silently empty**; this is WS-4 made structural.

**Guard pattern (m-41 mechanism-displaces-vigilance)**: an AST-level enforcement test asserts every MCP-consumer adapter implements all four methods. New connectors fail the build if they skip honest-degradation or status reporting. Same shape as `TestSessionScopeCommitContract` (#1193 / ADR-069 D5) and the m-41 cure-class generalization (CIO catalog 2026-06-13).

### D6: MCP-server maturity tiers — sequenced migration

**Decision**: Per-connector migration sequenced by MCP-server maturity:

| Tier | Connectors | Status | Migration timing |
|---|---|---|---|
| **Tier 1** | GitHub, Google Calendar | MCP server well-served; published; stable | Migrate first (Phase 2-3) |
| **Tier 2** | Slack, Notion | MCP server maturity needs assessment | Gap analysis Phase 0; migrate Phase 3-4 if mature, else native-with-shim until mature |
| **Tier 3** | local_git, future connectors | New connectors target MCP-consumer-only | Default for new work |

**Tier-2 escape valve**: if Slack/Notion MCP servers are insufficiently mature at the time of their migration window, hold native temporarily with an explicit `TODO(adr-070-tier2): migrate when MCP server matures` comment + a tracking issue. **Do not block the rest of the migration on Slack/Notion**; the Tier 1 + new work proceeds.

### D7: Migration sequencing — layer-then-migrate per m-40

**Decision**: For each Tier 1 connector, m-40 layer-then-migrate:

1. **Layer**: introduce MCP-consumer adapter alongside the existing native integration. Feature-flag the connector implementation choice per user.
2. **Migrate**: opt-in users to MCP-consumer path; monitor honest-degradation surfaces for `ConnectRequired` rate (the new structurally-honest "not configured" signal).
3. **Collapse**: once MCP-consumer path is healthy at parity (~weeks of monitoring), retire the native integration. Delete `services/integrations/{connector}/`.

Native retirement is the m-40 collapse step; the migration is not complete until the native code is removed. The `is_global_pm_domain` / `is_legacy_native` escape-hatch pattern from ADR-071 D6 inverts here: native integrations are the deprecated side, MCP-consumer is the canonical side; the marker is "is_native_legacy=true" on the bindings table during the transition.

### D8: Identity unification (WS-9) ordering — prerequisite, not parallel

**Decision**: WS-9 (identity unification — the web `a25db09c` vs Slack `009afc8c` finding) is a **prerequisite** for the connector migration, not a parallel workstream. Reasoning:

- Connectors sit on user identity. If a single human has two `user_id`s in Piper, MCP-server bindings fragment across both records, and the user experiences "I connected GitHub" but Slack-side Piper says "GitHub not connected."
- ADR-071's D2 owner-stamped invariant + D4 principal-resolution discipline both presuppose a canonical user identity. Building MCP-server-bindings against an unresolved identity model would force re-stamping after WS-9 lands.
- **The Phase 1 sub-sequencing**: WS-9 (identity unification) → WS-1 (config store; depends on WS-9's unified `owner_id` FK target) → WS-2 (credential model; collapses to server-binding storage per D3) → WS-5 (abstraction; once stores are aligned). WS-3 + WS-4 can interleave with WS-5.

**Cross-reference to ADR-071**: identity unification IS the Architect-clarifying-question that surfaces for ADR-071 D7 multi-tenant migration too. Same shape (resolve identity first, anchor content second); ADR-070 D8 makes the identity-first ordering explicit at the connector boundary.

### D9: ADR-058 finishing-the-job — not greenfield

**Decision**: This ADR explicitly frames much of RECONNECT (WS-2 / WS-7 / WS-9) as **finishing ADR-058's implementation**, not greenfield. The audit cascade Lead Dev ran (5 agents, 2026-06-14) verified ADR-058 already settled:

- Credential storage convention (KeychainService with provider + optional user-scope)
- OAuth-state user-scoping (the Slack class-level dict #1109 is an ADR-058 deviation, not an unanswered question)
- Multi-tenancy isolation invariants

WS-2 (#1229), WS-7 (#1109, #1110), WS-9 (#1233) cite ADR-058 as the governing decision rather than re-deriving conventions. The connector migration is **completing ADR-058 across the bespoke-integration code paths that pre-dated or bypassed it**. This avoids the re-litigation pattern PM named at the cohort-discipline layer.

---

## Implementation sequencing (suggested for Lead Dev)

This refines the input doc's Phase 0-3 with the D-section grounding:

- **Phase 0 — Design (this ADR + companions)**: ADR-070 v0.1 lands (this artifact); ADR-071 lands (Lead-authoring); ADR-066 v0.2 lands (filed 2026-06-14). Gates final shape of WS-1/2/5.
- **Phase 1 — Identity + Foundation**: WS-9 (#1233) FIRST (identity unification per D8) → WS-1 (#1226-build half + #1199) (DB-backed config per D4) → WS-2 (#1229) (credential model collapses to server-binding per D3).
- **Phase 2 — Correctness + Contract**: WS-3 (#1230) (resolution + dead-path cleanup) + WS-4 (#1231) (honest-degradation per D5 `degrade()` method) + WS-5 (#1232) (Connector protocol per D5).
- **Phase 3 — Uniformity + UX**: WS-6 (#1201) (first-run UX) + WS-7 (#1109, #1110) (connection-state robustness — finishes ADR-058 multi-process) + native retirement (D7 collapse step).

### Per-connector migration sequence (D6 tier-grounded)

Tier 1 first: **GitHub** (highest M3 value; MCP server mature) → **Google Calendar** (M4-relevant; mature). Tier 2 assessment Phase 0; tier 2 migration Phase 3-4 if mature.

The GitHub prefs-file band-aid (#1226-trigger M3 work-around) **is not the WS-1 fix** — it's an explicit band-aid that gets deleted by WS-1 once the DB-backed config + GitHub MCP-consumer migration land. WS-1's deletion of `data/*_preferences.json` is the m-40 collapse step.

---

## Consequences

### Positive

- **Silent-config-failure class structurally eliminated** (#1226-shape) — server-owned config (ADR-066 D7) + server-owned creds (D3) + DB-backed bindings (D4) means cwd-relative state cannot exist by construction.
- **Four-conventions credential model collapses to one** (server-binding-by-user per D3) — `_api_key` keychain foot-gun becomes MCP-server-internal not Piper's discipline.
- **ADR-052 + ADR-070 compose cleanly across two boundaries** (D2) — Piper-as-host and Piper-as-consumer are independent architectural commitments. The apparent tension is resolved by recognizing they govern different surfaces.
- **MCP-server maturity gates per connector migration, not the whole sprint** (D6 tier-2 escape valve) — Slack/Notion MCP server immaturity doesn't block Tier 1 progress.
- **Identity-first ordering surfaces explicitly** (D8) — WS-9 is named as prerequisite, not parallel. Prevents the rebuild-after-unification trap.
- **ADR-058 finishing-the-job framing** (D9) — much of RECONNECT becomes completing existing decisions rather than re-deriving. Cohort discipline at the catalog level.
- **Composes with ADR-066 v0.2 (Configuration Ownership) + ADR-071 (User-Auth Anchoring)** — three Architect-authored ADRs in five days cover the same architectural family (server-owned state + structural-truth-conditions + canonical-pattern-for-recurrence-prevention) at three distinct surfaces (config / connector-substrate / content). Catalog discipline visible at the ADR layer.

### Negative / Tradeoffs

- **MCP-server-internal failures become opaque to Piper** — if github-mcp-server has a bug, Piper observes "resource not found" without knowing whether the issue is auth, network, or server bug. Mitigation: D5 `status()` returns granular health states; D5 `degrade()` surfaces honest reasons. Cannot eliminate the externalization entirely.
- **MCP server maturity is a real constraint** — Slack/Notion may not be ready in the sprint window. D6 escape valve named; doesn't eliminate the risk.
- **WS-9 identity unification is non-trivial** — the web `a25db09c` vs Slack `009afc8c` finding may turn out to NOT be the same human (Lead's audit notes this is plausible-but-unproven). If they're distinct identities, the WS-9 scope shifts from "merge records" to "support multi-identity per human at the connector layer." D8 ordering holds either way.
- **Native retirement timing depends on MCP-consumer health monitoring** — D7's collapse step is gated on parity-validation that's qualitative (~weeks of monitoring). Risk: native lingers as deferred-cleanup tech debt.
- **Three ADRs landing in a week** (ADR-066 v0.2 + ADR-070 + ADR-071) — cohort review bandwidth + composition-debugging cost is real. Mitigation: cross-references explicit between ADRs; cohort review can stage.

### Non-consequences

- **This ADR does NOT decide the milestone/sprint placement** — that's PPM's call (Phase 0 question 2). M4 or M5 fits; PM has flexibility.
- **This ADR does NOT specify the per-connector MCP server choice** — `github-mcp-server` (Anthropic's), community alternatives, or building Piper's own are choices for Lead Dev at implementation time. The ADR specifies the architectural shape; the specific server is a downstream decision.
- **This ADR does NOT mandate immediate native retirement** — D7's m-40 collapse step is *when MCP-consumer reaches parity*, not a hard deadline. Native lingers as long as MCP-consumer needs validation.
- **This ADR does NOT decide multi-tenancy timing** — Phase 0 question 3 (Lead's input doc). ADR-058's multi-tenancy invariants apply when multi-tenant lands; ADR-070 doesn't gate that timing.
- **This ADR does NOT cover #1227 (Slack markdown rendering)** — that's an output-formatting bug independent of the connector substrate; ships as standalone quick win per Lead's §10c.

---

## Evolution

(Empty at v0.1 filing. Klatch-pause framing per Pattern-064 convention applies if cross-project relevance surfaces.)

---

## Open questions (v0.1)

1. **MCP server selection per connector** — Lead Dev consultation at WS-5 implementation. Initial lean: use Anthropic-published MCP servers where available (github-mcp-server, etc.); evaluate community + build-own at gap moments.
2. **WS-9 identity-unification scope** — depends on whether web `a25db09c` and Slack `009afc8c` are the same human (plausible-but-unproven per Lead's audit). PM may need to disambiguate from outside the system. Filed as #1233 sub-question.
3. **D6 Tier 2 maturity assessment** — Slack and Notion MCP server health survey. Lead Dev or PPM assigns when Phase 0 closes.
4. **D5 protocol formalization** — `ConnectResult` / `ConnectorStatus` / `ResolveResult` / `DegradationResponse` types — Lead Dev defines at WS-5 (#1232) authoring; D5 here specifies the methods, not the parameter/return shapes in detail.
5. **D3 OAuth-state-on-Piper-side** — does Piper retain any OAuth state (CSRF tokens, etc.) for the connect-flow handshake, or does the MCP server own all OAuth-state including the in-flight handshake? Initial lean: MCP server owns all of it; Piper's `connect()` is purely a redirect-+-callback orchestrator. Lead Dev consultation at Phase 1.

---

## What this ADR is NOT

- Not the per-connector MCP server choice (downstream decision)
- Not the milestone placement (PPM)
- Not the multi-tenant migration timing (ADR-058 + future ADRs govern)
- Not the OAuth-handshake protocol detail (D5 specifies method shapes; details at WS-5)
- Not the Slack markdown fix (#1227, standalone)
- Not the identity-unification implementation (#1233; this ADR sequences it as prerequisite)

---

## Amendment A (2026-07-10) — `mcp_server_ref` stores a logical key, not a topology (resolve at read-time)

**Trigger**: the #1278 Fly cutover silently invalidated PM's GitHub binding — `connector_bindings.mcp_server_ref` stored the literal compose hostname (`http://github-mcp:8082/mcp`), pg_dump/restore carried it verbatim onto Fly where that host doesn't exist, and the binding degraded to UNREACHABLE while reporting BOUND. The failure looked like a server outage, not a config problem. PM asked for a ruling before the #1232 port train mints more literal refs.

**Root cause (category error)**: `mcp_server_ref` conflates *which logical connector-server* (a **deployment-invariant identity**) with *where it lives right now* (a **deployment-variant topology**). Pinning topology into a per-user binding row means every host/topology change silently invalidates bindings, and parallel environments (alpha + beta, live concurrently as of the cutover) cannot share a correct row — one is wrong by construction. Same class as the #1283 / `Intent.original_message` lesson one layer down: a value resolved once at write-time with N read-time consumers and no single read-time authority.

**Ruling — Option B (env-resolved indirection), refining the D-ruling that placed the server ref on the binding:**

- **A1 — the binding stores a logical connector key, not a URL, for managed connectors.** `mcp_server_ref` holds `github` (deployment-invariant); the URL resolves from deployment config at **connect time** (`GITHUB_MCP_SERVER_URL` already exists and is env-correct per-deployment — `github_oauth_handler.py:37`). Topology becomes a deployment property; a host move is a config change, not a per-row invalidation. Drift is impossible-by-construction for managed connectors (the make-drift-impossible spine — same move as ADR-077 derive-the-prompt / #1312 autogen-empty).
- **A2 — ONE resolve authority, not N read-site interpretations.** A single `resolve_server_ref(ref) -> url` function is the sole authority; every read-site (`github_adapter`, `google_calendar_adapter`, the oauth_handler) routes through it. This is the load-bearing condition — B's value is *lost* if the resolve logic scatters (the #1283 discipline: one resolver, not N consumers each parsing the value). The bind-time `server_ref or _DEFAULT_MCP_SERVER_URL` capture (`github_oauth_handler.py:223`) moves to read-time resolution.
- **A3 — BYOC preserved by explicit shape-discrimination, made a named contract.** A scheme-prefixed value (`http(s)://…`, `stdio://…`) is a literal self-managed / BYOC override; a bare token is a logical key. This preserves this ADR's deliberate per-user-server intent (PDR-005 BYOC). Caveat, accepted: a BYOC literal *can* still go stale — but that URL names the **user's own** server, whose lifecycle they own (semantically distinct from us moving our infra); re-bind is the honest recovery. The shape-contract lives in the resolver (A2), not as incidental parses at read sites.
- **A4 — unknown-key resolution honest-degrades, pointing at config.** A logical key with no config mapping → `ResolveMiss` (#1232) → CONNECT_REQUIRED-shaped honest degrade (D5), never silent-empty or crash. The incident's tell was that the degrade looked like an outage; the degrade message must name the missing config, not read as a server being down.
- **A5 — migration + end-state.** Backfill managed-connector literal refs → logical keys (Lead's one-row Fly repoint, made systematic). Forward-compatible with this ADR's D5 `mcp_server_binding_id` FK-to-registry: the logical key is the near-term realization; a first-class server-binding registry keyed by logical name, resolved per-deployment, is the fuller end-state when per-user server registries land. Optional lint: no managed-connector binding stores a scheme-prefixed ref (the BYOC exception is the only one, and it is explicit).

**Sequencing**: not tonight; before the next connector port mints more rows (Lead). Both live environments have correct refs right now (alpha's compose host; Fly's `.internal`, repointed at cutover) — no runtime gate.

*Amendment A — Chief Architect, 2026-07-10, on Lead's PM-requested design question; Lead leaned B, Arch ruled B + the single-resolver-authority (A2) and honest-degrade (A4) conditions.*

---

## Decisions.log entry (per CLAUDE.md Recording-decisions discipline)

`2026-06-15 — ADR-070 filed v0.1: Piper-as-MCP-consumer; one Connector protocol; MCP-server owns auth; Piper stores bindings only; DB-backed user-scoped config (kills flat files); tier-2 escape valve; identity unification (WS-9) is prerequisite to WS-1; finishes ADR-058 across native-integration paths. Unblocks RECONNECT WS-1..9 decomposition. Lead Dev: ratify or refine.` — *Arch*

*v0.1 — Chief Architect, 2026-06-15, from Lead Dev's input doc. PM-ratified direction (2026-06-14); architectural how is this ADR.*
