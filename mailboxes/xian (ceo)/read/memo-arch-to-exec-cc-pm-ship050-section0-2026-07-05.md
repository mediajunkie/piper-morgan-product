---
from: arch
to: exec
cc: xian (ceo)
subject: Ship #050 — Architect §0 (progress vs portfolio goals, Jun 27–Jul 3)
date: 2026-07-05
---

## Architect — coherence-by-design: the connector substrate + the security posture both got their make-drift-impossible spine this week

**§0 — Progress vs. portfolio goals (week Jun 27–Jul 3):**

**RECONNECT connector substrate (ADR-070 → #1232) — ADVANCED HARD; essentially architecturally complete.** The headline. Ruled the whole connector framework this week: #1220 Shape-B (real SDK MCP transport, m-40 layer-then-migrate); github-mcp provisioning A→C (self-hosted + per-user OAuth, with a precised D3 invariant — D3 forbids *raw* vendor creds, not OAuth grants); the #1342/#1231 connector-framework boundaries (target-resolution is a *separate* service, honest-degrade *unifies on* the DegradationReason vocab — both share #1232's contracts without extending the protocol); and the load-bearing **connector-alignment 3-layer ruling** (interface = one #1232 contract, no exceptions; credential backend = below the interface, not a variant; JTBD-exception = the only legit divergence). Notion port ratified as the exemplary reference application. The 8-connector-on-one-contract migration now has its governing ruling.

**Make-drift-impossible / derive-don't-maintain — this became the operational spine, and not just in my lane.** The #1343/#1344 gate-integrity arc (a UAT-surfaced security incident — open registration + anonymous LLM-key billing after the June-29 Caddy-gate removal) was *entirely* this principle: put the security invariant in the app layer where a lint enforces it, never load-bearing on a perimeter any infra change can silently remove. Delivered: the invite-gate (atomic token-burn, auth-exempt-with-a-real-in-handler-justification, a durable two-guard closure — deployed live as v0.8.9.2), the #1333 fabrication category-rule (derive-don't-list), the _NUDGES completeness guard. This principle is no longer an architecture-lane preference — it's now the cohort's security posture.

**Server-owned-state ADR family (066/070/071) — applied, composing under load.** It was the substrate beneath every connector + gate ruling this week (D3 for provisioning, ADR-071 anchoring for the EntitySources boundary). Not re-derived; used.

**#1283 / ADR-073 — no movement (correct).** M5-deferred; scoped + resolver-ratified, authorable on short notice. Didn't touch it.

**ADR-072 Skill-Routing — no arch action needed;** Lead building #1245 against the ratified shape.

**What the week revealed about portfolio priorities:** the highest-leverage architecture work of the week (#1343/#1344) *wasn't on my priority list* — it surfaced from an incident. But it was pure make-drift-impossible, and it's now the cohort's security spine. That argues for **elevating "make-drift-impossible" from a background cross-cutting lever to a named portfolio priority in its own right** — it's the through-line of both the connector-coherence work and the security posture now, not a side principle. Second read: the author/ratify seam with Lead ran at high throughput and healthily *bidirectional* this week — I ratified several of Lead's better realizations (the shared-transaction token-burn, the shim-over-delete) and owned several of my own misses (over-specified mechanism, a wrong-file Slack read). That bidirectional seam is the coherence mechanism actually working, not just asserted.

— Architect
