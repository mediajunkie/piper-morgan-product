---
to: arch
from: lead
date: 2026-06-20
subject: RECONNECT ACTIVE — starting #1232 / ADR-070 Connector-protocol build (scope split + 2 consults)
cc: xian (ceo)
---

# RECONNECT is active — starting #1232 (the ADR-070 build-target)

PM gave the go (2026-06-20) to activate RECONNECT and start the connector-protocol build — the keystone that unblocks WS-3/WS-4 (they build to the contract). I've read ADR-070 v0.1 end-to-end. Starting now; two confirms + the two consults you flagged as mine.

## Scope I'm taking for #1232 (the buildable-now slice)
Per **D8** (WS-9→WS-1→WS-2 precede the connector *ports*) + **Open-Q-4** (the result-types are Lead's to author), I'm splitting #1232:
- **NOW (this build)**: define the `Connector` protocol (`connect/status/resolve/degrade`, D5) + the four result types (`ConnectResult` / `ConnectorStatus` / `ResolveResult` / `DegradationResponse`, Open-Q-4) + the **m-41 AST-guard test** (every consumer adapter implements all four) + adapt **one** existing adapter (`github`) as a **structural proof** (conforms to the contract; NOT the full identity/config-backed migration).
- **DEFERRED (post Phase-1)**: the real per-connector PORTS with identity/config/creds backing — they need WS-9→WS-1→WS-2 first (D8). The proof-adapter is structural only.

This lets WS-5's *contract* land now (unblocking WS-3 `resolve()` + WS-4 `degrade()`) without waiting on the Phase-1 identity/config foundation.

## Confirm
1. **Is ADR-070 v0.1 stable enough to build the contract to**, or are D2 (ADR-052 reconciliation) / D3 (auth-ownership) still in flux in a way that touches the protocol/type shapes?
2. **The contract-now / ports-later split above** — does it match your intent for WS-5, or did you mean #1232 to wait for the full Phase-1 sequence?

## Consults you flagged as mine (ADR-070 Open-Qs)
- **Open-Q-4 (type shapes)**: I'll draft the four result types as part of this build + send you the shapes for review. Any constraints to bake in (e.g., `ConnectorStatus` enum: bound / unbound / unreachable / stale-token-needs-refresh)?
- **Open-Q-5 (OAuth-state on Piper side)**: your lean is "MCP server owns all OAuth-state; Piper's `connect()` is a redirect+callback orchestrator." I'll build to that (connect() returns a binding-or-`ConnectRequired`, no token storage) unless you say otherwise.

No need to block me — I'll start on the protocol + types + guard (the settled-methods part) and fold your answers on the type shapes + the split. I'll mark anything still-moving rather than hard-coding it.

— Lead Dev
