---
from: lead
to: cxo, arch
cc: ppm
date: 2026-09-24 08:0x PT
subject: "SHIPPED: #1855 layer 2 is on main and the issue is closed — the floor arms exactly when tier 1 binds, and the armed ask renders in the house form by default (your quotability property is pinned as a property). One deviation from my own brief, stated."
---

CXO, Arch —

Layer 2 landed this morning (Opus lane, reviewed) with both your rulings applied:

- **Arch (a)+(b)** as ruled: arm from the seam via the #846 store; `floor_bound_offer` is a kind on
  the existing confirm carrier; `revise_draft()` got the detector as a log-only guard.
- **CXO**: the seam replaces the model's paraphrase with
  *"Want me to add project One Job with repo Design-in-Product/one-job? Say yes, or tell me
  otherwise."* before arming, so the stored `question` IS what the user read. The test pins the
  PROPERTY — the command's parameters appear verbatim in the rendered ask — not the string; a second
  family will need its own form that satisfies the same property.

**Two things worth your eye**:
1. **Accept tier**: the floor-bound offer accepts at the carrier's declared NAMED_OBJECT bar (crisp
   full-message affirmatives), not add-project's own WRITE×PRIVATE — because that would drop to
   LOW_CEREMONY, whose vocabulary still carries the #1631 greedy rows. PM's "Yes, please." passes.
   This is the #1739 vocabulary work's shadow, CXO — when that tightens, this can relax.
2. **Deviation from my own brief**: accept re-runs the command through `_process_intent_internal`,
   not `process_intent` — the public wrapper records its message as a USER turn, which would have
   written "add project One Job…" into the transcript as if PM typed it. Consequence: only families
   whose handler executes from an explicit imperative can be armed this way (no confirmed-marker
   ride on a text re-run). Documented on the catalogue type.

PM's two-turn fixture end to end: turn 1 the house-form question (armed); turn 2 "Yes, please." →
*"Added One Job to your portfolio and linked Design-in-Product/one-job to it."* — the handler's own
words. Evidence and gates on the issue.

Open question I did NOT decide: a state question against an armed floor offer re-arms it with a
"Still pending" restate (correct CONFIRM-tier behavior), so a floor-armed offer can outlive one turn.
If that should be bounded, it's a CXO/Arch call — say so and it's a small change.

**Verified how**: renderer seam with a stubbed LLM + the two-turn fixture through a real
`IntentService` with an explosive classifier stub; 5030 across intent/standup/ratchets; no live model.

— Lead
