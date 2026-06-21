# #1232 (RECONNECT WS-5) — MCP-consumer Connector contract — Gameplan

**Issue**: #1232. **Governing ADR**: ADR-070 (MCP-Consumer Connector Architecture, v0.1). **Date**: 2026-06-20. **Author**: Lead Dev. **PM-go**: 2026-06-20 (activate RECONNECT, start the ADR-070 build).

## Problem
No unified `Connector` protocol exists (greenfield — `connect/status/resolve/degrade` = 0 matches, `class *Connector` = 0 matches). The MCP-consumer foundation exists (`consumer_core.py` + 6 adapters) but each wires it ad hoc. WS-3 (`resolve`) and WS-4 (`degrade`) have **no contract to build to**. This is the keystone that unblocks them.

## Scope (PM-approved direction; split per ADR-070 D8 + Open-Q-4)
**THIS build (the contract + proof — buildable now):**
1. The `Connector` protocol (`connect/status/resolve/degrade`, ADR-070 D5).
2. The four result types (`ConnectResult` / `ConnectorStatus` / `ResolveResult` / `DegradationResponse`) — Open-Q-4 assigns these to Lead Dev.
3. The **m-41 AST-guard** test (a protocol-declaring adapter must implement all four methods).
4. Adapt **one** adapter (`github`) as a **structural proof** the contract fits the existing `consumer_core` foundation.

**DEFERRED (post Phase-1, per ADR-070 D8):** the real per-connector PORTS with identity/config/creds backing — they need WS-9 (identity) → WS-1 (config) → WS-2 (creds) first. The github proof here is **structural only** (conforms to the protocol; does not wire real MCP-server bindings / DB config).

## Design (from ADR-070 D5 + Open-Q-4/5; pending Arch confirm — see Pending)
- **Protocol** (async, four methods): `connect(user_id) -> ConnectResult` · `status(user_id) -> ConnectorStatus` · `resolve(user_id, resource) -> ResolveResult` · `degrade(reason) -> DegradationResponse`.
- **`ConnectorStatus`** = enum of binding health: `BOUND` / `UNBOUND` / `UNREACHABLE` / `STALE` (token-needs-refresh). Per D5.
- **`connect()`** returns a binding **or** a `ConnectRequired` honest-degradation response. Per Open-Q-5 lean: the MCP server owns OAuth-state; Piper's `connect()` is a redirect+callback **orchestrator** — **no raw token storage** (D3).
- **`degrade()`** is the honest-degradation contract: `ConnectRequired` (unbound), `ResourceNotFound` (resolve-miss), `Unreachable`. **Never silently empty** — WS-4 made structural.
- **`DegradationResponse`** carries a machine reason + a human "connect me / here's what's missing" surface.

## KEY design decision — the AST-guard must NOT break the build for un-ported adapters
ADR-070 D5 says "every MCP-consumer adapter implements all four methods; new connectors fail the build if they skip." Taken literally that breaks the build now — **5 of 6 adapters won't conform** (only `github` is ported as the proof). Resolution: the guard enforces on **protocol-declaring** adapters only (a class that subclasses a `ConnectorBase` / is registered as a `Connector`), not every file under `services/mcp/consumer/`. As each adapter ports (declares conformance), the guard enforces it. This keeps ADR-070's intent ("a declared connector can't skip honest-degradation") without a flag-day. Mirrors the `TestSessionScopeCommitContract` (#1193 / ADR-069 D5) declared-surface pattern.

## Phases (TDD)
**Phase 1 — protocol + types** (`services/mcp/consumer/connector.py`, NEW): the `Connector` Protocol + the 4 result types + a `runtime_checkable` conformance check. Tests: type construction/round-trip; status enum states; `ConnectRequired` degradation; a `@runtime_checkable` `isinstance` conformance probe. (~8–10 tests)

**Phase 2 — m-41 AST-guard** (`tests/test_architecture_enforcement.py` or a new `tests/.../test_connector_contract_1232.py`): AST/inspection test asserting every **protocol-declaring** adapter implements all four methods. Scoped to declared conformers (not all 6 files) — see KEY decision. Tests: a conforming stub passes; a stub missing `degrade` fails.

**Phase 3 — github structural proof**: make `github_adapter` declare + satisfy the `Connector` protocol (thin methods over the existing `MCPConsumerCore`; `resolve`/`degrade` honest stubs where the real binding/config is deferred). Tests: `github_adapter` satisfies the protocol + passes the guard. **Regression**: the 9 modules importing `services.mcp.consumer` + the 6 adapters still import + their existing tests stay green (the protocol is additive; the github change is declare-conformance + thin methods).

**Phase 4 — close-out**: comment #1232 (contract DONE; ports deferred per D8 → tracked); update the scope doc / decisions.log; #1232 stays OPEN (the ports are its remaining scope) OR PM/Arch decide to split the ports into a follow-up. Surface to PM/Arch.

## STOP conditions
- ADR-070 D2 (ADR-052 reconciliation) / D3 (auth-ownership) turn out still-in-flux in a way that changes the protocol/type shapes → STOP, fold Arch's answer (the kickoff memo asks). Build behind the marker meanwhile.
- The AST-guard, as written, fails the build for un-ported adapters → STOP (must be declared-conformer-scoped, per KEY decision).
- The github proof would require real MCP-server bindings / DB config to conform → STOP (that's the deferred port, not this scope) — keep the proof structural.

## Rollback
- All-new files (`connector.py` + the test) + a thin additive change to `github_adapter` (declare conformance + 4 thin methods). Rollback = revert the github declaration + delete the new files; no existing behavior changes (the protocol is additive; nothing consumes it yet until WS-3/4).

## Success criteria
- `Connector` protocol + 4 types defined, typed, tested.
- AST-guard enforces the 4-method contract on declared conformers without breaking the build.
- `github_adapter` conforms (structural proof).
- WS-3 / WS-4 now have a contract to build to.
- Ports deferred + tracked (D8). #1232 dispositioned with PM/Arch.

## Pending Arch (kickoff memo 2026-06-20)
- Confirm ADR-070 v0.1 is stable to build the contract to (D2/D3 not in flux re: shapes).
- Confirm the contract-now / ports-later split matches WS-5 intent.
- Open-Q-4 (type shapes) review; Open-Q-5 (OAuth-state) lean confirmed.
