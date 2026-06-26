# RECONNECT — sprint chunking proposal (Lead-authored)

**STATUS: PROPOSED — awaiting PM ratify** (PM 2026-06-25 eve: "you can suggest a chunking… which chunk next and in what order… very likely I'll ratify; I'll flag concerns.")
**Author**: Lead Dev · **Date**: 2026-06-25 · Builds on `dev/2026/06/22/reconnect-remainder-sequencing-2026-06-22.md` + the 6/25 board reconciliation.

## The remaining work, as 5 chunks + 1 parallel track

Done (9): WS-1 (#1199/#1226), WS-5 contract (#1232), WS-9 (#1233), Slack mrkdwn (#1227), ADR-071 D4 (#1291), BYOC bridge (#1294), security (#1308/#1311). The remainder:

### Chunk 1 — WS-2 Credential Model (foundation) · `#1229`
The typed credential convention (OAuth-app vs token) the ports consume.
- **Blocked by**: one Arch design-decision — *does storing MCP-server bindings (not raw creds) shrink this to a thin "store-bindings" task?* (a question, not code).
- **Size**: S–M (depends on that answer). **Why first**: the spine/ports sit on it.

### Chunk 2 — MCP Spine + Ports (the bulk) · `#1220` (WS-8) + `#1317` (WS-5 ports), folds in `#1230` (WS-3) + `#1231` (WS-4)
Port each connector (github/slack/notion/calendar) onto the Connector contract + MCP, applying per-connector resolution (#1230) + honest-degrade (#1231) **as each ports** — #1230/#1231 are NOT standalone builds (re-scope: close-with-fold-in, like we did #1226).
- **Blocked by**: Chunk 1 + the #1232 contract (done). **Size**: L — the heavy two-thirds of the refactor. **Why second**: the heart; everything else is scaffolding around it.

### Chunk 3 — Connect-UX & First-Run · `#1201` (WS-6) + `#1314` + `#1315`
Make connecting a connector a real product flow: Slack inbound setup path (#1201), auto-default repo (#1314), populate/retire project↔repo links (#1315).
- **Blocked by**: Chunk 2 (ports must exist to connect). **Size**: M.

### Chunk 4 — Slack Robustness · `#1109` + `#1110` (WS-7)
OAuth state → Redis (multi-process safe) + the `_make_request` missing-`user_id` latent bug.
- **Blocked by**: mostly independent (Slack-specific); can slot anytime after Chunk 1. **Size**: S–M.

### Chunk 5 — Independents & Cleanup · `#865` + `#1316` + `#1283`
Not connector-framework-blocked, schedulable any time: setup-wizard componentize (#865); residual cleanup (#1316: federated_search degrade + WS-1 integration test + ADR-058 identity note); **routing-integrity audit (#1283)** — standalone, delegable, and it produces the gap list Arch needs to author ADR-073.
- **Blocked by**: none. **Size**: S each.

### Parallel track (not connector-mechanics) — Hosted-beta foundation · `#1185` (+ `#1300`)
BYO-key multi-tenant. Gated on the #1162 follow-on (app-layer invite control + RBAC #357/#1312) — we decided 6/25 to **keep the Caddy gate** for now, so #1185 waits on that. This track gates the 0.9.0 beta; distinct from finishing the connector refactor.

## Recommended order + the NEXT move

**Critical path** runs Chunk 1 → Chunk 2 (credential model → spine/ports). The one thing gating it is the **Arch WS-2 design-decision**. So:

1. **Tomorrow AM, first action (no code)**: send Arch the WS-2 design-decision question (does MCP-binding storage shrink #1229?). Unblocks the critical path.
2. **In parallel, start coding NOW-unblocked**: **#1283 (Chunk 5)** — the only chunk with zero dependencies, it's sprint-tagged, and it derives the exact routing-integrity gap list Arch is waiting on for ADR-073. Clean self-contained first piece of real sprint code.
3. **Chunk 1 (#1229)** once Arch's decision lands.
4. **Chunk 2 (spine + ports)** — the bulk; #1230/#1231 fold in.
5. **Chunks 3 → 4 → 5-remainder** by priority.
6. **#1185 beta track** when its gate (invite-control + RBAC) clears.

**So the answer to "what next": #1283, started immediately, with the Arch WS-2 question fired in parallel** — that gets real sprint code moving tomorrow AM without waiting on anyone, while teeing up the critical path (Chunk 1 → 2).

## For PM to ratify / adjust
- The order (critical path #1229→spine, with #1283 as the unblocked starter)?
- The #1230/#1231 re-scope (fold into ports, don't build standalone)?
- Is Slack robustness (Chunk 4) higher priority than I've placed it (if Slack is alpha-tester-facing)?
- #865 / #1316 / #1283 — keep in the sprint or split out as their own track?
