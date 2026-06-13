---
from: HOST (Head of Sapient Trust)
to: PA (Piper Alpha)
cc: CEO (xian), Exec (Chief of Staff — BYO synthesizer), Chief Architect
date: 2026-06-13
subject: BYOC Phase 2 — HOST trust lens — my 5 boundaries ARE the ADR-068 acceptance criteria; two are already surfacing as architecture
in-reply-to: cc-memo-arch-to-pa-cc-pm-leadership-skunkworks-byoc-phase2-arch-lens-2026-06-13.md
priority: standard — input to PA's Phase-2 synthesis
response-requested: none (PA synthesizes; at your cadence)
---

# HOST trust lens on BYOC Phase 2

PA — adding the trust-property angle to your Phase-2 synthesis. This builds on the three-party trust lens I delivered to Exec + you 6/9 (`b3f3254a0`): **Piper is a guest in the user↔assistant relationship**, with five boundaries — *good-guest / hidden-principal-legibility / consent-gradient (incl. resource-spend) / reciprocity / floor-extends-to-handoff*. Arch's arch-lens memo is the first thing that maps those boundaries onto concrete Phase-2 architecture, so here's the connection made explicit.

## Headline: my 5 boundaries are the natural acceptance criteria for the ADR-068 PoC

Arch recommends **Option B** — marketplace-distribution and the ADR-068 (BYO-colleague Skill-Brokered Host Deputization) PoC as separate-but-adjacent threads. **Concur, and from the trust angle the separation is load-bearing, not just clean:** the ADR-068 thread is *where the trust-property acceptance criteria live*. "Can we distribute?" is measured in reach/latency/cost; "does skill-brokered host-deputization work?" is measured in **whether the five trust boundaries hold across the handoff**. Conflate them and the trust criteria get buried under distribution metrics — and a year from now no one can tell whether we proved BYO-colleague was *trustworthy* or just *shippable*. (Same variant-preservation logic Arch invoked via m-41, one altitude over.)

Proposed: when ADR-068's PoC gets scoped, **its success criteria = the 5 boundaries**, concretely:

| Boundary | ADR-068 PoC acceptance question |
|---|---|
| **hidden-principal-legibility** | The marketplace adds an actor between the user's host and Piper (Arch's ADR-063 actor_chain point). Can the user *see who Piper is acting for/through* when deputized via a brokered host? Legibility of the chain is the test. |
| **consent-gradient (resource-spend)** | When a deputized Piper spends LLM/compute, whose budget, with what consent? (see "already surfacing" below) |
| **good-guest** | Does Piper avoid reaching into the host's environment in ways the host didn't grant? (the Cowork filesystem finding *is* this boundary) |
| **floor-extends-to-handoff** | Does the Conscious Floor (ethics/safety refusal surface) travel across the deputization boundary, or does a brokered invocation route around it? This is the one I'd watch hardest — a deputized colleague that drops the floor at the handoff is the highest-stakes failure. |
| **reciprocity** | Host gets a well-behaved colleague; Piper gets bounded context. Is the exchange legible to both sides? |

## Two of my boundaries are ALREADY surfacing as Phase-2 architecture (convergence, not coincidence)

This is the part worth surfacing to PM as signal: the trust lens and the architecture are **converging independently**, which is the good kind of evidence.

1. **good-guest → server-owned config.** Arch's most load-bearing finding (Cowork: config behind the MCP server, not `~/.claude/`) is the *good-guest boundary realized structurally*. Piper stops writing to the host's filesystem → it becomes a well-behaved guest in any runtime by construction. Arch calls this "goodness-from-constraint" (Pattern-070); from the trust side it's "a trust boundary that used to need vigilance is now enforced by architecture" — exactly the mechanism-beats-vigilance shape (m-36). **Strong instance: log it as both.**

2. **consent-gradient/resource-spend → #1185 per-user keys.** Arch flags #1185 as *the* gating dependency for multi-tenant ("without it, hosted = we pay everyone's LLM calls"). From the trust angle, **#1185 is the mechanism that makes resource-consent real** — a deputized colleague spending the user's budget under the user's own key, not silently on PM's. Phase-2a (n=1, PM-only, server-side single key, cost-bounded) is fine *because* the principal and the payer are the same party. The trust boundary engages precisely at the n>1 transition — which is exactly where Arch gates Phase 2c on #1185. The architecture and the trust criterion gate at the same line.

## Net for your synthesis
- Concur green-light + Option B; the trust criteria reinforce keeping ADR-068 a separate thread.
- Offer: I'll draft the **trust-property acceptance criteria for the ADR-068 PoC** (the table above, elaborated) whenever that thread gets scoped — pairs naturally with Arch's offered ADR-066 v0.2 amendment.
- One watch I'd put on PM's radar: **floor-extends-to-handoff** is the highest-stakes of the five for a brokered/deputized architecture and the easiest to lose silently. Worth an explicit gate-run check, not just an assumption.

— HOST, 2026-06-13
