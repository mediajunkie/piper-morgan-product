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

### Chunk 4 — Slack Robustness · `#1109` + `#1110` (WS-7) — **DEPRIORITIZED (PM 6/25: "Slack can wait")**
OAuth state → Redis (multi-process safe) + the `_make_request` missing-`user_id` latent bug. Moved down the order; not the near-term fallback.
- **Blocked by**: mostly independent (Slack-specific). **Size**: S–M.

### Re-scope RESOLVED (PM 6/25): fold BOTH #1230 and #1231 into the ports
- **#1230** — fold (PM ratified). Resolver logic exists; remainder = data-population (#1314/#1315) + per-connector generalization (in the ports).
- **#1231** — fold too. I'd recommended pulling it forward (the live #1226 GitHub-silent-`return {}` trust bug), but PM: alpha-tester count is too low for that tester-facing urgency to drive ordering, and **order should follow Lead's context-coherence** — so do each connector's honest-degrade *while porting that connector* (one context-load), not a separate `canonical_handlers.py` pass that gets re-touched at port time. The #1232 `DegradationResponse` contract + the m-41 guard (every adapter implements degrade) enforce honest-degrade **as each connector ports** → the guarantee isn't lost by folding.

### Chunk 5 — Independents & Cleanup · `#865` + `#1316`
Not connector-framework-blocked, schedulable any time: setup-wizard componentize (#865); residual cleanup (#1316: federated_search degrade + WS-1 integration test + ADR-058 identity note).
- **Blocked by**: none. **Size**: S each.

### → M5 polish (PM call 2026-06-25) · `#1283` routing-integrity audit
Moved OUT of the active sprint to **M5 (distro & polish, before launch)** per PM. Rationale: unhandled classifier actions already fall to the floor handler safely (#1124 floor-first dispatch), so this is harden-and-contract, not fix-live-breakage. Building #1283 derives the routing gap list → feeds Arch's **ADR-073 (Routing-Integrity Contract)**, which therefore also lands in M5. Arch needs no action until then (no live block).

### Parallel track (not connector-mechanics) — Hosted-beta foundation · `#1185` (+ `#1300`)
BYO-key multi-tenant. Gated on the #1162 follow-on (app-layer invite control + RBAC #357/#1312) — we decided 6/25 to **keep the Caddy gate** for now, so #1185 waits on that. This track gates the 0.9.0 beta; distinct from finishing the connector refactor.

## Recommended order + the NEXT move

**Critical path** runs Chunk 1 → Chunk 2 (credential model → spine/ports). The one thing gating it is the **Arch WS-2 design-decision**. So:

(Updated 2026-06-25 eve — PM moved #1283 → M5, so it's no longer the unblocked starter.)

**Ordering principle (PM 6/25): by Lead's process/context-coherence, not external urgency** (tester count too low for tester-facing urgency). Stay on the dependency spine; minimize context-switching.

1. **Tomorrow AM, first action (no code)**: send Arch the WS-2 design-decision question (does MCP-binding storage shrink #1229?). The one gate on the spine.
2. **Chunk 1 (#1229) — credential-model foundation.** Prep unblocked now (read the cred surface); build to Arch's answer. Stay here rather than context-switch to filler.
3. **Chunk 2 (#1220 spine + #1317 ports)** — the bulk; **#1230 + #1231 both fold in per-connector** (resolution + honest-degrade done while in each connector's port; #1232 contract + m-41 guard enforce degrade as each ports).
4. **#1314/#1315** (data/first-run) → **#1316/#865** (cleanup), by priority. **Chunk 4 (Slack) deprioritized.**
5. **#1185 beta track** when its gate clears. **#1283 + ADR-073 → M5.**

**So the answer to "what next": fire the Arch WS-2 question, then start Chunk 1 (#1229 credential model)** — the foundation everything else builds on, and the most context-coherent place to begin.

## For PM to ratify / adjust
- The order (critical path #1229 → spine; Arch WS-2 question first)?
- The #1230/#1231 re-scope (fold into ports, don't build standalone)?
- Is Slack robustness (Chunk 4) higher priority than I've placed it (if Slack is alpha-tester-facing)? — it's now the main standalone-unblocked option since #1283 moved to M5.
- #1283 → M5 (PM-decided 2026-06-25). ✓
- #865 / #1316 / #1283 — keep in the sprint or split out as their own track?
