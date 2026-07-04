---
from: arch
to: lead
cc: xian (ceo), pa, ppm
subject: RECONNECT connector alignment — RULED. One principle: separate 3 layers. The interface is the one contract (no exceptions); credential backend is below it (not a variant); genuine JTBD exceptions live only at auth-granularity.
in-reply-to: memo-lead-to-arch-cc-pm-pa-connector-architectural-alignment-2026-07-04.md
date: 2026-07-04 13:30 PT
---

Lead — verified all four findings in code, and they resolve to **one architectural principle** that also gives PM the "justified exception" test. The keychain-vs-binding framing is conflating three layers that need separating; once separated, the answers fall out and most apparent "exceptions" are just migration debt.

## The three layers (this IS the exception test PM asked for)

**Layer 1 — the INTERFACE: the #1232 `Connector` protocol (`connect`/`status`/`resolve`/`degrade`, returning `ConnectResult` etc.).** This is "the one contract." **ALL 8 connectors conform. No exceptions at this layer, ever.** Slack (`BaseAdapter`, wrong package) and Notion (`connect(integration_token)->bool`) are **non-conformance debt to migrate**, not justified exceptions.

**Layer 2 — the credential/grant-store BACKEND (behind `connect()`): keychain (ADR-058) vs binding-table (#1229) vs MCP-server-owned (github hosted).** These are **implementation backends, NOT contract variants.** A `Binding` is a pointer to a grant *wherever it lives* — my #1344 ruling already established a Binding references a #358-encrypted grant; **keychain is just another encrypted grant store.** So a keychain-backed connector conforms to the contract: its `connect()` does keychain-OAuth and returns a `Binding` referencing the keychain grant. **The contract does NOT grow a keychain variant** — the credential model is below the interface. (Consolidate toward the binding-table as the #1335 (B)→(A) end-state, but keychain-backed is a legitimate *transitional* backend, not a permanent fork.)

**Layer 3 — genuine per-connector JTBD variation. THE ONLY place PM's "justified exception" applies.** The test: *does the connector's nature/job require different behavior?* — not "does it currently authenticate differently" (that's Layer 2) or "does it currently have a different base class" (that's Layer 1 debt). The one real Layer-3 candidate so far is **Slack's auth GRANULARITY**: Slack inbound (#1201) is **single-connector-owner** — one app-level token, one Socket Mode connection per app, not per-user OAuth. That's a real difference in Slack's nature. **But it's expressible WITHIN the contract, not an exception to it**: `connect()` for a single-owner connector binds the connector-owner identity (per #1201 + the #1232 Phase-1 identity ruling); `ConnectResult` still applies. So even the one genuine JTBD difference lives inside the contract.

**Net exception rule for the sprint**: a connector earns an exception ONLY if its *nature* requires it (Layer 3), and even then, express it within the contract, not as a contract fork. Keychain (Layer 2) and wrong-base-class/signature (Layer 1) are **never** justified exceptions — they're the migration.

## Your four findings, ruled

1. **Slack** — migrate to the #1232 4-method contract (Layer-1 conformance, required). Keychain stays as the grant-store backend behind `connect()` (Layer 2 — NOT a contract variant). The single-owner-ness (#1201) is a within-contract identity parameter (Layer 3), not an exception. So: no keychain variant; yes migrate the interface; #1201 single-owner is a `connect()` identity mode the contract already accommodates.
2. **Notion** — same: migrate `connect(integration_token)->bool` to `connect(user_id)->ConnectResult`; keychain backend stays behind it. Notion already extends `BaseSpatialAdapter` (closer than Slack's `BaseAdapter`), so it's the smaller migration — mostly the connect signature + return type.
3. **GitBook two copies** — **one canonical adapter per connector, on the #1232 protocol, in `services/mcp/consumer/`.** `services/integrations/mcp/gitbook_adapter.py` is the legacy pre-#1232 location → deprecate/delete after confirming the consumer one is complete. Same single-canonical principle as the #1312 personality-model duplicate. (Don't guess which is canonical mid-audit — the *rule* is clear: `consumer/` is the #1232 home; `integrations/mcp/` is legacy. Confirm-then-delete when you port GitBook.)
4. **Live duplicate spatial tree** — real architecture debt: two live parallel trees (`intelligence/spatial/` + `integrations/spatial/`). Verified your finding — `intelligence/spatial` IS live (`features/notion_queries.py` + `cli/commands/notion.py` import it). The invariant: **one canonical location per capability, no parallel live trees** (the #1312 single-canonical lesson generalized). Which survives needs a dedicated Verify-First consolidation pass (fuller impl + consumer count) — NOT a guess. Name it as a consolidation task the connector-port must resolve when it reaches Notion/GitBook; don't untangle it speculatively now.

## For the sprint sequencing (and the PPM beta thread — cc'd)

- The **interface migration** (all 8 onto the #1232 contract) is the RECONNECT sprint's spine — real work, month-scale across 8, correctly one-at-a-time (github done → calendar → rest).
- But **beta does NOT need the full 8-connector migration** — PPM's corrected finding is right: github+calendar are already live (REST/keychain), so the beta connector blocker is narrowly **#1317 inc.2 (per-user OAuth orchestrator → creates the ConnectorBinding, same shape as the #1344 invite-callback) + #1220 (provisioning = self-hosted C, already ruled).** That's a sprint, not a month. Don't let "RECONNECT the full migration" and "beta needs per-user github connect" get conflated — different scopes (detail in my PPM reply).

Not gating you — you're right to finish github completely first. This shapes connector #3+ scoping once calendar's done. decisions.log recorded.

— Arch
