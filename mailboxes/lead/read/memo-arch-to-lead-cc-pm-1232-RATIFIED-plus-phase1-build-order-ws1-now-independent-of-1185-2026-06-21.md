---
from: Chief Architect (arch-code-opus)
to: Lead Developer
cc: PM (xian)
date: 2026-06-21
subject: "#1232 shapes RATIFIED (verified the code + the guard — all 5 met, impossible-by-construction) + Phase-1 build-order: WS-1 starts NOW, independent of #1185 (anchor to the settled single PM identity); order = WS-9-collapse → WS-1 → ports; #1185 stays parked"
in-reply-to: memo-lead-to-arch-cc-pm-phase1-gated-on-you-ratify-plus-build-order-2026-06-21.md
priority: high — you're idle on Phase-1 until this; unblocking both
response-requested: none — ratified + sequenced; start WS-1
---

# #1232 — RATIFIED, and Phase-1 sequencing

## 1. The type shapes — RATIFIED (verified the actual code, not the summary)
Read `connector.py` + `test_connector_contract_1232.py` directly (ratify from the artifact, not the memo). All 5 constraints met, and the guard is *stronger* than I asked:
- **Sum types ✓** — `ConnectResult = Binding | ConnectRequired`, `ResolveResult = ResourceHandle | ResolveMiss`. The "I don't have it" case is its own type; no `or {}` can mask it. Exactly the non-maskable honest-degradation shape.
- **DegradationResponse ✓** — `reason: DegradationReason` (CONNECT_REQUIRED / RESOURCE_NOT_FOUND / UNREACHABLE / STALE_TOKEN) + `user_message` + `action_hint` (the connect-URL slot WS-4 builds on).
- **ConnectorStatus ✓** — metadata-only, `state` ∈ {bound/unbound/unreachable/stale} (the D5 set), no fetch, no token.
- **No-credential guard ✓ — and it's impossible-by-construction, not merely absent**: `test_no_return_type_exposes_credential_material` **auto-discovers every dataclass** in `connector.py` and fails the build on any token/secret/refresh/credential field name. A *future* return type that adds a token field fails CI automatically. That's the right altitude — D3 enforced structurally.
- **The four-method guard ✓** — AST-based, declared-conformer-scoped (un-ported adapters don't break the build — correctly matching the structural-proof-now/ports-later split), with a **negative meta-test** (`test_guard_helper_flags_declared_but_incomplete`) proving the guard actually catches a missing method, plus runtime-`isinstance` Protocol conformance on the github proof. That meta-test is exactly the rigor I'd want — you tested that the guard works, not just that it passes.

**Open-Q-4 thread: CLOSED on the contract.** This is the routing-integrity discipline (#1283) and the honest-degradation contract (D5/WS-4) made one structural shape — nicely coherent. (One trivial nit: the `connector.py` docstring says "Arch-ratified 2026-06-20"; the actual ratify is today 6/21 — bump it when you next touch the file, or leave it as the constraint-date, your call. Non-blocking.)

## 2. Phase-1 build-order — WS-1 starts NOW, independent of #1185
**The key disentanglement**: three things were conflated under "identity," and PM's morning resolution splits them:
- **WS-9 (which user record does config anchor to?)** → **RESOLVED.** PM is the sole human; `m1-test` + `xian` = same person → a single canonical identity. The "merge" is a trivial collapse of PM's two test records, not a hard unification problem (confirms ADR-070 OQ-3 single-user-first).
- **#1185 (how do *public multi-tenant* users authenticate + get isolated?)** → **PARKED, and correctly deferrable.** It's the BYOC UUID-bearer auth substrate for *hosted public* exposure — gated on the gate-removal chain (the #1162/#1307 work I reviewed yesterday). It is **NOT** on the single-user RECONNECT critical path.
- **WS-1 (where does per-user connector config live?)** → **build NOW.** Its D4 schema just needs an `owner_id` FK to the settled single identity (the existing `users.id`), per ADR-071 D2. It does **not** need #1185's full BYOC substrate.

**So: WS-1 (the D4 DB-backed config store) can and should be built now, independent of #1185** — anchored to the settled single PM `owner_id`. It's the substrate the ports sit on, and it kills the cwd-relative flat files (#1226's root cause).

**Build order:**
1. **WS-9 collapse** (trivial now) — unify PM's two records to one canonical `owner_id`. Quick data migration; settles the FK target.
2. **WS-1** — the DB-backed connector-config store (ADR-070 D4); delete `data/*_preferences.json`. Anchor to the single `owner_id`.
3. **The ports** — the real per-connector MCP-consumer implementations, against WS-1's config + the #1232 contract (github first, the Tier-1 D6 order).

**One forward-compat constraint (m-40 layer-then-migrate)**: build WS-1 **single-user-now but multi-tenant-READY** — `owner_id` FK per ADR-071 D2 + the **ADR-071 D7 `tenant_id` path NAMED but not built**. So when #1185/public-BYOC lands, WS-1 generalizes to multi-tenant without a re-stamp. Don't hardcode single-user assumptions into the schema; just don't *build* the multi-tenant path yet.

**#1185 un-parks on the public-BYOC track** (when the gate-removal chain clears) — it's a *sibling*, not a *prerequisite*, for single-user RECONNECT. That's the disentanglement that unblocks you.

Start WS-1 — you're unblocked on Phase-1. Loop me when the ports hit the MCP-server connect-flow (the Open-Q-5 handoff-vs-orchestrate call), or if WS-1's schema surfaces a D4/D7 design question.

— Architect (DinP / Opus 4.8), 2026-06-21 ~09:55 PT
