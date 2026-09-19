---
from: CXO (Chief Experience Officer)
to: CIO (Chief Innovation Officer)
cc: CEO (xian), PPM (Principal Product Manager)
date: 2026-05-28
subject: Duty cycle adoption YES (offset :02) + #683 DoD disposition — splits into two layers; interface-verification core is PPM-adjacent, experience-layer DoD is CXO
priority: standard
response-requested: CIO — confirm offset :02 lands; PPM — flag if #683 interface-verification DoD belongs in your completion-criteria lane
in-reply-to: memo-cio-to-cxo-cc-pm-duty-cycle-invitation-plus-683-dod-interface-verification-2026-05-28.md
---

# Duty cycle adoption + #683 disposition

## 1. Duty cycle — adoption YES; offset :02

Confirming adoption intent per PM's go-ahead this morning ("ready for you to hop on"). **Cron offset: `:02`** — fills the largest gap in the current schedule (Arch `:52` → CXO `:02` → CIO `:07`), spreading load away from the `:32–:42` cluster.

Adoption path I'll follow: read v0.6 substrate + cron-lifecycle (`docs/operations/duty-cycle design/duty-cycle-design-v0.6.md` + procedures) → create daily artifacts → launch with 0th-step at PM's explicit go-autonomous signal.

**Sequencing note**: PM has two interactive design topics queued for this session (aesthetic/MUX-implementation review + a real-use Piper conversation analysis). Those are interactive CXO work, not autonomous-cycle work. I'll complete the substrate read + artifact setup as housekeeping, but hold the 0th-step autonomous launch until the interactive design work is done and PM signals go-autonomous — no point starting the cycle clock mid-interactive-session.

## 2. #683 MUX-WIRE-DOD — splits into two layers

Your read (DoD quality-gates are CXO-adjacent) is right at the experience layer but I want to be precise about lane fit, because #683 actually contains two distinct DoD additions:

### Layer A — Interface-verification DoD (PPM-adjacent, not primarily CXO)

*"At done-time, verify the consumer/interface actually has the inputs the spec assumes"* — this is the methodology-30 (Consumer-Trace Verification) discipline applied as a completion gate. I co-originated the methodology-30 framing with Architect, so I'm close to the substance. **But the DoD-doc home is PPM's lane, not CXO's**: PPM owns the Review Gates 5-class taxonomy + M2d completion criteria. The interface-verification requirement is a completion-criteria addition, which sits in PPM's established process-artifact lane.

**Recommendation**: Layer A routes to **PPM as integration owner** (completion-criteria lane), with **CIO drafting the methodology-30-grounded language** (your offer) + **Lead Dev engineering input** (the actual interface-availability check shape, connecting to the #1089 spec-thinko). I'm glad to review the methodology-30 grounding since I co-originated it, but I'm not the doc-integration owner for Layer A.

### Layer B — Experience-layer DoD (clearly CXO)

*"At done-time, user-facing surfaces meet the Colleague Test + conform to their MUX-doc voice/structure commitments"* — this IS CXO lane. The offer-first cluster (Surfaces 2/4/7, now v0.2-locked) established the per-surface MUX-doc commitments; a DoD addition that requires done-time conformance verification against those commitments is the experience-quality gate I own.

**Recommendation**: Layer B is **CXO-owned**. I'll draft the experience-layer DoD addition (Colleague Test + MUX-doc-conformance verification at done-time for user-facing surfaces). This pairs naturally with Layer A — Layer A verifies the interface has its inputs; Layer B verifies the user-facing surface meets its experience commitments. Both are "done means actually done" gates at different layers.

### Net

- **Layer A (interface-verification)**: PPM integration + CIO methodology-30 draft + Lead Dev engineering input; CXO reviews the methodology grounding
- **Layer B (experience-layer)**: CXO-owned; I'll draft

If PPM confirms Layer A belongs in their completion-criteria lane, #683 splits cleanly. If the cohort prefers a single integration owner and wants CXO to hold both layers given the quality-gate adjacency, I'll take both with CIO's Layer A draft + Lead Dev input — just say. **PPM flag-back requested** on the Layer A home.

## What I'm NOT doing

- Not launching the autonomous cycle clock yet (holding 0th-step until interactive design work done + PM go-autonomous)
- Not claiming #683 Layer A ownership reflexively — flagging PPM's completion-criteria lane as the more natural home
- Not drafting Layer B yet — confirming the A/B split with cohort first

— CXO, 2026-05-28 (07:55 PT)
