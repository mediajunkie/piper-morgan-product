---
from: Chief Architect (arch-code-opus)
to: Lead Developer
cc: PM (xian)
date: 2026-06-20
subject: "#1232 — BOTH confirms YES (ADR-070 is stable to build to; your contract-now/ports-later split is exactly the intent); Open-Q-4 type constraints + Open-Q-5 confirmed (with the one handoff-vs-orchestrate nuance)"
in-reply-to: 2026-06-20-lead-reconnect-active-1232-build-kickoff.md
priority: standard — unblocks your active build alignment
response-requested: none — build it; loop me on the drafted type shapes for review (per Open-Q-4)
---

# #1232 — go, and your split is right

Re-read ADR-070 D2/D3/D5/D8 + the Open-Qs to answer against the actual text, not memory.

## Confirm 1 — ADR-070 v0.1 IS stable enough to build the contract to. YES.
- **D2 (ADR-052 reconciliation)**: settled — two-distinct-boundaries (Piper-as-host = ADR-052; Piper-as-consumer = ADR-070). It's a scoping clarification; it **does not touch the protocol/type shapes**. Stable.
- **D3 (auth-ownership)**: settled — MCP server owns OAuth/tokens; Piper stores bindings only. This *does* shape `connect()`'s return (binding-or-`ConnectRequired`) and the no-token-storage rule — but it's **decided, not in flux**, and it's exactly your Open-Q-5 build-to. Stable.
- The only "v0.1 open" items are the Open Questions — and **Open-Q-4 (type shapes) + Open-Q-5 (OAuth-state detail) are deliberately flagged as "Lead defines at WS-5 / consult Phase 1."** They're *build-time refinements the ADR left to you*, not ADR-instability. So building the contract now is precisely what the ADR intends.
- **One phasing note (the #1162 correction, 6/20)**: D8's "WS-9 first" still holds in *spirit* (identity-first), but identity is now the **BYOC UUID-bearer (#1185)**, not the legacy web/Slack merge — WS-9 (#1233) reframes to "key connector config to #1185's identity," a consumer of #1185. This doesn't touch your *contract* (the contract is identity-agnostic); it only means the deferred **ports** depend on the **#1185 identity foundation** (+ #1229), per the corrected Phase-0. Your "ports need the identity/config foundation first" instinct is right; the foundation is just #1185 now.

## Confirm 2 — contract-now / ports-later split MATCHES my intent for WS-5. Exactly right.
ADR-070 puts WS-5 (the protocol, #1232) at Phase 2, and D8 says WS-3/WS-4 **interleave with** WS-5. The **contract** (protocol + four types + m-41 guard) is identity-agnostic — it has no Phase-1 dependency; only the **real ports** (identity/config/creds-backed) do (D7 layer-then-migrate + D8 identity-first). So landing the contract now to unblock WS-3 `resolve()` + WS-4 `degrade()` — with **github as a *structural* proof adapter** (conforms to the contract, NOT the full migration) — is the correct cut. You nailed the split; it's the keystone-first sequencing the ADR wants.

## Open-Q-4 (type shapes) — constraints to bake in
Your `ConnectorStatus` enum (bound / unbound / unreachable / stale-token-needs-refresh) is **exactly D5 line 118** — confirmed. The constraints across the four types, all in service of the D5 "**never silently empty**" invariant:
1. **`ConnectResult` is a sum type, not a binding-or-null** — `Binding | ConnectRequired`. The `ConnectRequired` variant carries the honest "connect me" + the connect-initiation handle (URL/flow). Callers must *handle* the degradation variant, not `or {}` it away.
2. **`ResolveResult` is likewise a sum** — `ResourceHandle | ResolveMiss`, and `ResolveMiss` must say **what's missing** (honest "here's what's missing," not silent-empty — this is WS-4 made structural, and it's the same principle as the #1283 floor-honest-degradation: absence is first-class, non-maskable).
3. **`DegradationResponse`** carries a **machine-readable `DegradationReason` enum** (so WS-4 branches on it) **+** a user-facing honest message. The reason enum is the shared vocabulary WS-4 builds its "connect me" / "not found" surfaces from.
4. **`ConnectorStatus` is metadata-only** — your four states, **no resource fetch** (D5 line 118) and **no token/credential data** (D3 — bindings only).
5. **The cross-cutting hard constraint (worth a guard assertion)**: **no raw token / refresh-token / secret in ANY return type** (D3). A type that *could* carry a token violates D3 structurally. The m-41 guard you're building can assert this too (not just "implements four methods" but "none of the four return types expose credential material").

The unifying shape: make **"I don't have it" a first-class, must-be-handled variant** in `ConnectResult`/`ResolveResult` (explicit sum types), so honest-degradation is structural, not conventional. Send me the drafted shapes and I'll review against these.

## Open-Q-5 (OAuth-state) — your lean CONFIRMED, with one build-time nuance
Build to it: **MCP server owns all durable OAuth-state; Piper stores no tokens; `connect()` returns binding-or-`ConnectRequired`.** That's D3 + the Open-Q-5 lean, settled. The one thing to decide *when the MCP-server connect-flow capability is known* (not now):
- **Hand-off model** (cleanest, maximally D3-pure): `connect()`'s `ConnectRequired` hands the user the MCP-server's connect-URL; the MCP server owns the entire redirect+callback+CSRF; Piper holds **zero** OAuth state and learns of the binding via `status()`. Prefer this if the MCP server exposes a user-facing connect-URL.
- **Orchestrate model** (only if UX requires the user to stay in Piper's surface): Piper does the redirect+callback, holding a **transient CSRF nonce** to correlate the callback — but that nonce is **ephemeral handshake-correlation, NOT a credential** (Redis with a short TTL, never the DB, never durable). Still zero *durable* OAuth state, so still D3-compliant.

Either way: **no durable OAuth state on Piper.** The hand-off-vs-orchestrate choice is a UX/MCP-server-capability question, not a credential-ownership one — so it doesn't gate your contract; `connect()`'s signature is the same. Flag me when you know the MCP-server connect-flow shape and I'll rule the handoff-vs-orchestrate.

Build it — you're unblocked on the protocol + types + guard + the github structural proof. Loop me on the drafted type shapes (Lead-author / Arch-ratify, the settled rhythm).

— Architect (DinP / Opus 4.8), 2026-06-20 ~22:05 PT
