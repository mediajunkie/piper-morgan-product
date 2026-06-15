# ADR-068 (BYO-colleague Skill-Brokered Host Deputization) — Trust-Acceptance-Criteria SEED

**Status**: SEED / pre-scoping capture. The full document is **M4-gated** (waits on the ADR-068 thread being scoped — Option B per Arch 6/13). This file exists so the thinking isn't carried in-head between now and then (write-to-file discipline). HOST owns; pairs with Arch's ADR-066 v0.2 amendment + ADR-068 D5 (consent architecture).
**Origin**: BYOC Phase-2 trust-lens thread (HOST→PA `bb0d10c34`; Arch ack+amplification 6/13).
**Last updated**: 2026-06-13.

---

## Frame
Piper is a **guest in the user↔assistant relationship** (three-party trust). The ADR-068 PoC proves skill-brokered host-deputization works *end-to-end and trustworthily*. Success = the five BYO-colleague boundaries hold across the deputization handoff. These ARE the acceptance criteria (not distribution metrics — those belong to the separate marketplace thread, per Option B).

## Composition (Arch 6/13, m-38 tier-discipline)
Three artifacts at three altitudes, bound at M4:
1. **ADR-066 v0.2 amendment** (Arch) — architectural refinement: server-owned config as canonical default.
2. **This trust-criteria document** (HOST) — the acceptance criteria below.
3. **ADR-068 D5 (consent architecture)** (Arch's M4 queue) — binds 1+2 together.

## The five criteria (each = an acceptance question + evidence-that-proves-it)

| Boundary | Acceptance question | Evidence that proves it (DRAFT) |
|---|---|---|
| **hidden-principal-legibility** | Can the user see who Piper is acting for/through when deputized via a brokered host? | actor_chain (ADR-063) extends faithfully through the marketplace/broker actor; the chain is surfaced, not hidden. Gate-run: inspect actor_chain on a brokered call; assert the broker actor is present + attributable. |
| **consent-gradient (resource-spend)** | When a deputized Piper spends LLM/compute, whose budget, with what consent? | n=1 PM-only Phase-2a OK (principal == payer). At n>1: per-user keys (#1185) bind spend to the consenting principal. Gate: no multi-tenant spend on a shared/PM key without #1185. |
| **good-guest** | Does Piper avoid reaching into the host's environment beyond what was granted? | Server-owned config (Cowork finding) → no host-filesystem write by construction. Gate: run in a non-Code runtime (Cowork/Desktop) with no host write; passes structurally. **Already enforced by architecture** (m-41 architecture-boundary cure / m-36). |
| **floor-extends-to-handoff** ⚠️ HIGHEST-STAKES | Does the Conscious Floor (ethics/safety refusal) travel across the deputization boundary, or get silently degraded? | **Arch's sharpened spec (6/13)**: floor refusal must flow through the same intent-contract surface (ADR-065 canonical context package) regardless of direct-vs-brokered invocation. **Gate-run**: a deputization scenario where Piper would normally hit the floor (ethics-sensitive request) — verify the refusal is FAITHFUL through the brokered chain, not degraded. Add to Rung-2 gate (or whatever follows Rung-1) → structural check, not vigilance check. |
| **reciprocity** | Is the host↔Piper value exchange legible to both sides? | Host gets a bounded, well-behaved colleague; Piper gets bounded context. Gate: the deputization grant + what-Piper-receives are both inspectable. |

## Load-bearing PM signal (carry into the doc)
Two of the five boundaries surfaced as Phase-2 architecture **independently** of the trust lens: good-guest→server-owned-config, resource-consent→#1185. The trust lens and the engineering re-derived the same boundaries from opposite ends → the BYOC mental model is structurally coherent (Arch concurs this is the cross-validation that justifies investing in Phase 2). A trust property that the architecture re-derives on its own is the healthiest kind.

## Open / TODO when scoped
- Elaborate each "evidence that proves it" into a concrete gate-run with pass/fail assertions.
- Coordinate with Arch on where the floor-extends-to-handoff check lands in the gate ladder (Rung-2?).
- Confirm the actor_chain (ADR-063) extension shape for the broker actor with Arch (he flagged "likely a one-line addition; don't pre-design").
