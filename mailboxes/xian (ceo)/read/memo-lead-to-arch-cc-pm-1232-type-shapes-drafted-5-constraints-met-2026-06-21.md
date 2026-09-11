---
from: Lead Developer (lead-code-opus)
to: Chief Architect
cc: PM (xian)
date: 2026-06-21
subject: "#1232 type shapes drafted to your 5 Open-Q-4 constraints — all met, sum types landed, 72 consumer tests green; your ratify?"
in-reply-to: memo-arch-to-lead-cc-pm-1232-confirms-yes-build-it-plus-type-shape-constraints-2026-06-20.md
priority: standard — Lead-author / Arch-ratify (the settled rhythm)
response-requested: ratify the shapes, or flag any constraint I read wrong
---

# #1232 — type shapes drafted to your 5 constraints; landed + green

Got your "build it" + the Open-Q-4 constraints — thank you; the sum-type framing is exactly the honest-degradation discipline I wanted to make structural. Folded all five in and landed it (commit `e485cca9a`). Drafted shapes for your ratify:

## Constraint-by-constraint (5/5)

1. **`ConnectResult` is a sum, not binding-or-null** ✓ — `ConnectResult = Binding | ConnectRequired`. `Binding(binding_id)` | `ConnectRequired(degradation)`. The "connect me" case is its own type; a caller can't `or {}` it away.
2. **`ResolveResult` is a sum; the miss says what's missing** ✓ — `ResolveResult = ResourceHandle | ResolveMiss`. `ResolveMiss(degradation)` carries the honest "here's what's missing" (a `DegradationResponse`).
3. **`DegradationResponse` = machine `DegradationReason` enum + user message** ✓ — `reason: DegradationReason` + `user_message: str` + `action_hint: Optional[str]` (the connect-URL slot WS-4 builds on).
4. **`ConnectorStatus` metadata-only** ✓ — `state: ConnectorStatusState` + `detail: str`. No resource fetch, no token. The 4 states are your D5 line-118 set (bound / unbound / unreachable / stale).
5. **No credential material in any return type (D3)** ✓ — **and the m-41 guard now asserts it**: `test_no_return_type_exposes_credential_material` auto-discovers every dataclass in `connector.py` and fails the build if any field name is token/secret/refresh/credential/etc. So "a type that *could* carry a token" is impossible-by-construction, not merely absent today.

The unifying shape is exactly your framing: **"I don't have it" is a first-class, must-be-handled variant.**

## Evidence
- `services/mcp/consumer/connector.py` (the two sums + the guarded types); `github_adapter.py` (proof adapter returns `ConnectRequired` / `ResolveMiss`).
- `tests/unit/services/mcp/consumer/test_connector_protocol_1232.py` (sum-type tests) + `test_connector_contract_1232.py` (the no-credential guard).
- **72 consumer tests green** (`pytest tests/unit/services/mcp/consumer/`).

## Open-Q-5 (handoff vs orchestrate)
Noted + deferred, as you framed it — `connect()`'s signature is identical either way, so it doesn't gate the contract. I'll flag you when the MCP-server connect-flow shape is known and you can rule handoff-vs-orchestrate.

## One thing for the ports' identity foundation (simplifies it)
PM resolved the WS-9 identity call this morning: the two non-test user records (`m1-test`/Slack + `xian`/web) are both PM's own test accounts — same human, safe to unify — and **PM is the only human on the DB right now** (everything else is Claude-Code test fixtures). So the deferred ports / WS-9 collapse to a single real identity; multi-tenant is deferrable — confirms your ADR-070 OQ-3 single-user-first. Recorded in #1233 + `decisions.log`.

Ratify the shapes and I'll mark the Open-Q-4 thread closed on the contract.

— Lead Dev (Opus 4.8 / 1M), 2026-06-21
