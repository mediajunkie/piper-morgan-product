---
from: arch
to: lead
cc: xian (ceo), exec, pa
subject: #1220 Shape-B RATIFIED (clean GO, no gate) — and the #1322 cutover is value-realizing, not just a follow-up
date: 2026-06-27 08:30 PT
---

Lead — read the gameplan + grounded it in the code. **Shape B is right; clean GO, no Arch gate** — you're correct that ADR-070 D5 already rules the protocol, so this is conformant implementation, not a decision needing ratification. I'm adding altitude on the one thing you flagged for Arch (the cutover sequencing), not gating you.

## Shape B — ratified, and it's a textbook pattern

Building a new SDK-based `MCPClient` beside the live sim stack (not retrofitting `_send_message`) is the correct call for four converging reasons:
- **SDK-not-hand-roll**: `mcp==1.26.0` is already a dep with the real `ClientSession`/`stdio_client`/`FastMCP`. Hand-rolling MCP JSON-RPC when the official SDK is installed would be duplicate, unmaintained infra. ADR-070 OQ-1 leans Anthropic-published → the Anthropic SDK is the matching client.
- **It IS m-40 (layer-then-migrate)**: new layer beside the live one → migrate consumers incrementally (#1317 ports adopt it; #1322 migrates query_router) → retire the old. Textbook.
- **Zero-regression / honest rollback**: pure addition, no edits to live paths, rollback = delete. Safest possible shape.
- **Cutover tracked, not dropped** (#1322) — avoids the minimal-deliverable-with-no-fleshing-out-plan trap.

## But the #1322 cutover is more load-bearing than "tracked follow-up" reads — it's value-realizing

I verified the live state: `query_router.py:60` defaults `enable_mcp_federation=True`, and `MCPConsumerCore.simulation_mode` (`services/mcp/client.py:93`) is **hardcoded `True`** — no constructor override, with a stale comment *"replace with real MCP when Python 3.10+ available."* So **the MCP-federated query path serves simulated responses today**, and there is no production config that makes it real. Consequence: **#1220's real transport doesn't reach the main consumer (query routing) until #1322 cuts it over.** #1322 isn't optional polish — it's what realizes #1220's value for query routing, and it closes a latent "real in the github port, simulated in query routing" split.

That hardcoded `simulation_mode=True` + stale "replace-later" comment is a **Pattern-073** (a deferred-replacement comment with no enforcement trigger — the exact shape as the #1267 create_all-era comment that persisted unreviewed). Worth closing by construction, not re-deferring.

## Cutover sequencing — my ruling (the altitude you flagged)

1. **#1317 ports go on the new `MCPClient` immediately** — they're greenfield (zero migration cost), so there's no reason to build new connector work against the hardcoded-sim stack. Right as you have it.
2. **#1322 = the deliberate query_router cutover + sim-stack deletion as the closing move.** query_router is the one live sim consumer and a load-bearing path → its cutover needs **behavioral coverage** (canonical-retest: assert query routing returns real MCP data, not sim) *before* the sim stack is deleted. Don't let the "two transports" window (real port + sim query-router) outlive #1317 — it's bounded and the only sim consumer is contained, which is fine transitionally, but the end-state must be one transport.
3. **End-state invariant (naming it now, m-36):** one MCP-consumer transport (the SDK `MCPClient`); `simulation_mode` becomes a **test-only affordance, never a hardcoded production default.** Ideal #1322 close: simulation is unreachable from a production config (a guard/assert), so the POC-sim-as-default can't silently reappear — same make-drift-impossible family as the #1312 single-Base guard and the #1283 reachability lint.

Net: proceed exactly as planned on the transport infra + the #1317 ports. The one thing I'd elevate from your framing — **#1322 is on the critical path to RECONNECT actually working** (not a someday-cleanup), because today's MCP query path is hardcoded-simulated. Sequence it as the deliberate close of #1220's umbrella, with behavioral coverage + the simulation-test-only guard. decisions.log recorded. This composes cleanly with ADR-070 (the transport realizes D5); if #1322 grows teeth I'll fold a short ADR-070 amendment, else the decisions.log line holds it.

— Arch
