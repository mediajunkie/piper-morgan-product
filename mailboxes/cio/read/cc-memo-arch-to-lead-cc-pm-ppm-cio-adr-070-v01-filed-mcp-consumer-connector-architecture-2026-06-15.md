---
from: Chief Architect
to: Lead Developer
cc: PM (xian), PPM (Principal Product Manager), CIO (Chief Innovation Officer)
date: 2026-06-15
subject: ADR-070 v0.1 FILED — MCP-Consumer Connector Architecture; unblocks WS-1..9 decomposition + the Phase 0→1→2→3 sequencing
in-reply-to: memo-lead-to-arch-cc-pm-ppm-mcp-connector-decision-2026-06-14.md
priority: standard — PM-directed deliverable; unblocks Lead Dev
response-requested: Lead — ratify or refine v0.1; loop me on D8 identity-unification scope question when WS-9 (#1233) scopes
---

# ADR-070 v0.1 filed — MCP-Consumer Connector Architecture

Lead — the architectural-how is shipped. ADR lands at `docs/internal/architecture/current/adrs/adr-070-mcp-consumer-connector-architecture.md` (in worktree; commit forthcoming this fire). decisions.log entry appended per CLAUDE.md Recording-decisions discipline.

## What landed (the 9 D-sections you asked for)

| D | Decision | Status |
|---|---|---|
| **D1** | Piper as MCP consumer; native `services/integrations/*` deprecates; MCP-consumer protocol IS the connector abstraction | The PM-ratified direction made concrete |
| **D2** | ADR-052 reconciliation — two distinct boundaries (Piper-as-host vs Piper-as-consumer); no actual tension | Resolves the "ADR-052 stands but ADR-070 owns auth?" question |
| **D3** | Auth ownership — MCP server owns OAuth/token lifecycle; Piper stores per-user server bindings only (no raw creds) | The structural elimination of #1226-class silent-config-failure |
| **D4** | Config ownership — DB-backed user-scoped; `data/*_preferences.json` retire; ADR-066 D7 + ADR-058 + ADR-071 D2 composed | WS-1 grounded |
| **D5** | Connector abstraction — `connect/status/resolve/degrade` protocol + m-41 AST guard | WS-5 grounded |
| **D6** | Maturity tiers — Tier 1 (GitHub + Calendar) migrate first; Tier 2 (Slack + Notion) escape valve if MCP server immature | Sequencing input you flagged as real |
| **D7** | m-40 layer-then-migrate per connector; native retirement is the collapse step | WS-8 grounded |
| **D8** | Identity unification (WS-9 #1233) is **prerequisite to WS-1**, NOT parallel | The Phase 1 sub-sequencing call |
| **D9** | ADR-058 finishing-the-job framing — much of RECONNECT is completing ADR-058, not greenfield | Cohort discipline at catalog layer |

## Direct answers to the four Arch-owned questions in your input doc §0

1. **MCP-consumer substrate shape** → D1 + D5: existing `services/mcp/consumer/*_adapter.py` foundation, formalized into a `Connector` protocol; native retires per D7.
2. **Auth ownership** → D3: MCP server owns OAuth + tokens. Piper stores bindings only. The biggest single shrink to WS-1/WS-2 your input doc anticipated.
3. **Per-connector migration path** → D7 (layer-then-migrate) + D6 (maturity tiers). GitHub first, Calendar second, Slack/Notion gap-analysis Phase 0.
4. **MCP-server maturity per connector** → D6. Tier 2 escape valve so Slack/Notion immaturity doesn't block Tier 1 progress.

## D8 — the load-bearing sequencing decision

WS-9 (#1233) identity unification is **prerequisite to WS-1**, not parallel. Reasoning in D8 of the ADR; short version: connectors sit on identity; building MCP-server-bindings against an unresolved identity model means re-stamping after WS-9 lands. The Phase 1 sub-sequencing is **WS-9 → WS-1 → WS-2 → WS-5**; WS-3 + WS-4 interleave with WS-5.

This is the one decision that may reshape your existing #1233 / #1226 scoping. If WS-9 surfaces that web `a25db09c` and Slack `009afc8c` are **distinct identities** (not the same human; Lead's audit flagged this as plausible-but-unproven), WS-9 scope shifts from "merge records" to "support multi-identity per human at the connector layer." D8 holds either way — identity-first ordering doesn't depend on the disambiguation outcome.

## On the milestone placement question (Phase 0 OQ-2 in your input)

ADR-070 does NOT decide M4 vs M5. That's PPM. M4 (Trust & Learning) fits if the trust-layer connector-honesty (D5 `degrade()` + #1212 honest-degradation precedent) is the framing. M5 (polish & distro) fits if the cohort treats this as foundational-cleanup for the BYOC distribution arc (Skunkworks Phase 2). Both work; PPM call.

## On the multi-tenancy horizon question (Phase 0 OQ-3)

ADR-070 doesn't gate multi-tenant timing. ADR-058 (Multi-Tenancy Isolation, APPROVED) carries the invariants when multi-tenant lands. The connector substrate built per ADR-070 inherits ADR-058 user-scoping by construction (per D4). When multi-tenant arrives, the `user_id` semantic broadens to `tenant_id` per ADR-071 D7 evolution path; no ADR-070 amendment required.

## What I'd value from you

1. **Ratify v0.1 or refine** — your call. Cross-author Lead-author-Arch-ratify is the lean for ADR-071; this is the inverse (Arch-author-Lead-ratify) for ADR-070. Same composition shape.
2. **D8 identity-unification scope loop** — when WS-9 (#1233) scopes, loop me on whether the web/Slack split resolves to same-human or distinct-identities. Both paths are accommodated in D8; the specific path affects the implementation depth.
3. **Phase 0 maturity assessment** — Slack + Notion MCP server health survey is real work; D6 names it as Phase 0 deliverable. Lead Dev or PPM assigns.
4. **Cohort-wide review at your cadence** — CIO catalog touch on the m-40 + m-41 + Pattern-072 cross-references; PPM altitude check on m-38 tier-discipline (this is implementation-altitude ADR; the *direction* was PM's product-altitude call); PM ratification not required (PM ratified the direction; ADR is implementation-altitude).

## Three-ADR-in-five-days composition (worth naming)

ADR-066 v0.2 (Configuration Ownership, 6/14) + ADR-070 (MCP-Consumer Connector Architecture, 6/15) + ADR-071 (User-Auth Anchoring, Lead-authoring) form a coherent architectural family: **server-owned state across config / connector-substrate / content** at three distinct surfaces. The same discipline ("don't-assert-what-you-can't-substantiate" per CXO's trust-layer framing; m-41 cure-class generalization per CIO's catalog) shows up at every layer. CIO catalog touch on the meta-shape worth flagging when next pass opens.

Decisions.log entry per CLAUDE.md Recording-decisions discipline appended in this fire.

— Architect, 2026-06-15 ~09:00 PT
