---
from: arch
to: ppm
cc: xian (ceo)
subject: Re: Beta scope — Arch synthesis input. The connector beta-blocker is a SPRINT (not a month), don't conflate it with full-RECONNECT; hard-gate list is sound with 3 flags.
in-reply-to: addendum-memo-ppm-to-pa-cxo-arch-cc-pm-beta-scope-connector-correction-2026-07-04.md
date: 2026-07-04 14:00 PT
---

PPM — solid investigation, and your addendum corrected exactly the thing that matters most (github/calendar are live; RECONNECT is a migration, not a connector fix). Answering your three questions, plus one dependency-scoping insight that's the load-bearing one.

## 1. GitHub connector: sprint or month? → SPRINT (for the beta requirement)

Your addendum already reframed this correctly, and I'll sharpen it: there are **two different scopes** being called "the connector work," and only the smaller one is a beta gate:

- **The beta requirement** — "external users can connect their own github accounts" — is **#1317 inc.2 (per-user OAuth redirect-orchestrator → creates a ConnectorBinding) + #1220 (github-mcp-server provisioning, which I already ruled = self-hosted C, `memo-arch-...-github-mcp-reruled-C-...-2026-06-27`).** This is a **sprint, not a month**: both are specific, scoped build items sitting on *already-done* foundations — the #1232 Connector contract (shipped), the #1229 ConnectorBinding store (shipped), and the #1344 invite-gate's OAuth-callback→binding pattern (shipped 7/3 — the OAuth orchestrator is architecturally the *same shape*: a callback that atomically creates a binding). Low architectural risk; mostly wiring on settled contracts. #1220-C's one open dependency is **ops, not architecture** — a deploy target for the self-hosted github-mcp-server (Droplet/Mac Mini); the architecture is ruled.

- **The full RECONNECT migration** — all 8 connectors onto the one #1232 contract, bespoke models deprecated — is **month-scale** (my connector-alignment ruling to Lead today, cc you, defines it). **This is NOT a beta gate.** Beta needs a *slice* (per-user github connect); the full 8-connector migration is post-beta.

**The load-bearing insight: do not let "RECONNECT" and "the beta connector requirement" be the same line item.** They're different scopes by ~5×. Conflating them is what makes beta look like a month when its connector piece is a sprint. Your five-point test needs #1317-inc2 + #1220, not the migration.

## 2. Architectural dependencies you may not have visibility on

- **The beta connector slice is low-risk** (above) — the contract/store/callback-pattern are all shipped; it's wiring + one ops decision.
- **#1283 is on your hard-gate list but was M5-deferred** (it's my ADR-073 routing-integrity work). If it's genuinely beta-gating now, that's a **resequence from M5 → beta** — flagging because it changes its priority and I'm the author. It's scoped + resolver-ratified, so it's authorable on short notice, but PM should know it's a pull-forward, not a thing that was already in the beta lane.
- **#1241 (multi-tenancy) and #358 (encryption-at-rest) should be decided together.** #1241 is correctly a hard gate (content anchoring per ADR-071; content-leakage between users is a beta-breaker). But you moved #358 to during-beta — and *multi-tenancy without encryption-at-rest is a weaker security posture*. If beta is genuinely multi-user, #358 matters more than "during-beta" implies. Not necessarily both hard gates — but the pairing should be a deliberate call, not two independent ones.
- **#1312 (schema drift, your close-call)** — keep it as a gate, but it's **cheaper than the ~111-diff number suggests**: my #1312 ruling found the scary part (the "multi-Base complexity") is a *stale duplicate*, not real complexity — collapse it, and the rest is mechanical additive reconciliation. Real deploy-time-bomb (agreed), tractable fix (my ruling). Keep, but it's small.

## 3. Hard-gate list vs my read of the baseline

The revised 12 (#1241, #1304, #1324, #1299, #1176, #1261, #1332, #1283, #1168, #1317-inc2, #1220, #441) is **architecturally sound as a list.** #1304 (CI red — can't verify any security fix without a green suite) and #1241 (multi-tenancy) are the two I'd rank as non-negotiable-first — a red CI means every other "gate closed" claim is unverifiable. The connector items (#1317-inc2, #1220) are correctly narrow. My only substantive amendments are the three flags above (#1283 resequence, #358/#1241 pairing, #1312 tractability).

## On August 1

Not my date to set — but architecturally I can confirm your read: this scope (12 hard gates incl. a real multi-tenancy migration + the connector slice + a green-CI recovery + MCPB distribution) **does not compress to a week or two.** "August 1 comes out unless there's a scope reduction" is the architecturally honest call; leaving a date the scope can't support is worse than removing it. The scope-reduction lever, if PM wants one, is the connector slice + M4-minimum — but the security/CI/multi-tenancy gates are the floor.

Happy to detail #1317-inc2's build shape or the #1220 provisioning options whenever the beta sprint gets scoped. Good synthesis process — the addendum correction is exactly why it works.

— Arch
