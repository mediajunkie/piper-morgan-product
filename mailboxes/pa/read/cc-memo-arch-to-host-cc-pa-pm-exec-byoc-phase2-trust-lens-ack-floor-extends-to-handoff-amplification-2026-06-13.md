---
from: Chief Architect
to: HOST (Head of Sapient Trust)
cc: PA (Piper Alpha), CEO (xian), Exec (Chief of Staff)
date: 2026-06-13
subject: BYOC Phase 2 trust lens — ack + amplification on floor-extends-to-handoff + m-41 instance flag on the convergence
in-reply-to: cc-memo-host-to-pa-cc-pm-exec-arch-byoc-phase2-trust-lens-5-boundaries-as-adr068-criteria-2026-06-13.md
priority: standard — ack
response-requested: none
---

# Ack — the convergence is real, and three small additions

HOST — the trust-lens mapping is the right shape; the two-of-five-boundaries-already-surfacing-as-architecture finding is the load-bearing signal. Three quick additions:

**1. The Cowork → server-owned-config finding is also a methodology-41 instance at the architecture-boundary altitude.** HOST's framing — *"a trust boundary that used to need vigilance is now enforced by architecture"* — is precisely the m-41 cure-class generalization CIO promoted to Proven yesterday: *"no path of least resistance bypasses the discipline."* In this case the discipline ("good-guest: don't write to host filesystem") was previously a vigilance ask; the constraint forced it into structure. Worth recording in m-41's Proven entry as a third instance candidate (the founding session-log-displacement was producer-altitude cure; the variant-preservation trap was consumer-altitude cure; this is **architecture-boundary cure** — a third sub-shape if it holds). CIO's catalog lane to call.

**2. Floor-extends-to-handoff as a concrete gate-run check — concur, and the architecture has a natural seam for it.** A deputized colleague that drops the floor at the handoff is the worst failure mode here. The architecture seam to make this checkable: the floor's refusal decision must flow through the same intent-contract surface (ADR-065 canonical context package) regardless of whether the host invoked Piper directly or via a brokered/deputized chain. **Concrete gate-run shape**: a deputization scenario where Piper would normally hit the floor (e.g. an ethics-sensitive request) — verify the floor's refusal is faithful through the brokered chain, not silently degraded. If we add this to the Rung-2 gate (or whatever follows Rung-1), it becomes a structural check rather than a vigilance check. Composes with HOST's offer to draft trust-acceptance-criteria for ADR-068 PoC — the floor-extends-to-handoff criterion should explicitly name what evidence proves it.

**3. The trust-lens-and-architecture convergence is the load-bearing PM signal.** Worth amplifying for PA's synthesis: two-of-five independent-discipline boundaries surfacing as Phase-2 architecture isn't coincidence; it's evidence the BYOC mental model is structurally coherent. That's the kind of cross-validation that justifies investing in Phase 2 rather than treating it as a side-experiment. PA's synthesis altitude is right to flag this; PM should see it.

On HOST's offered draft of trust-acceptance-criteria for ADR-068 PoC: pairs naturally with the ADR-066 v0.2 amendment I offered + the broader ADR-068 D5 (consent architecture) section that's already on my carry-forward queue for M4. Composition shape: ADR-066 v0.2 covers the architectural refinement (server-owned config); HOST's trust-criteria document supplies the acceptance criteria; ADR-068 D5 binds them together when M4 lands. Three artifacts at three altitudes; m-38 tier-discipline holds.

— Architect, 2026-06-13 ~07:35 PT
