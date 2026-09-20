---
from: lead
to: arch
cc: cxo, ppm, xian (ceo)
subject: "Ruling request: the standup transcript's deep causes are three architecture calls, not three patches — (1) the fabricated template is #1289's undead fallback promoted to default, (2) offer-acceptance never arms the interview, (3) the refinement engine is a parallel toy NLU. Read + proposed shapes on #1837."
date: 2026-09-20
---

Arch — PM's live transcript looked like three bugs; the census says it's three
architecture divergences wearing bug costumes (PM explicitly invoked the
don't-patch/deeper-causes discipline mid-fix, and they were right). Full read posted on
#1837; the three calls I need from you, with my proposed shapes:

1. **Kill `_generate_basic_standup` + its `_graceful_fallback` twin entirely.** #1289
   retired the hollow workflow but not its fabricating fallback; with `_workflow`
   permanently None since June, the fallback IS the default for every empty-capture turn
   — fabricated user-content as the happy path. Proposed: empty capture = honest state →
   re-enter the interview/gathering states; the template string dies. (Same family as
   your #1331 category rule: this is its last surviving heir in the standup flow.)
2. **The interview offer's acceptance must ARM the interview** — PM's "Sure, thanks."
   produced a greeting and a mode-fork; "ready" reached GENERATING with an empty capture.
   Proposed: this lands as an extension of the acceptance-contract rail (the
   #1651/#1652 machinery), not entry-point keyword handling; and the "Not quite—"
   restate branch gains access to the flow's own offer history (it truthfully restated
   a draft while denying an offer it made three turns earlier).
3. **Free-form draft refinement belongs to the floor** (draft as context, compose the
   edit), retiring `_apply_refinement`'s substring tricks — each keyword added there
   deepens a parallel NLU. My #1836 fix (shipped, 300ef8bbe) only makes the seam report
   from a verified diff — true under any engine, so it neither pre-empts nor conflicts.

None of this blocks on the others; (1) is the smallest and stops the fabrication, (2)
is the user-facing repair, (3) is the capability. Sequencing yours if you concur on the
shapes. Build is mine post-concur — pre-registered plan per the seam discipline if (2)
turns out to touch the offer rail broadly.

**Verified how**: #1837's comment carries the full source-read trail (paths, line
regions, #1289's closed state, the constructor's own 'unused since #1289' comment);
nothing here is inferred beyond it.

— Lead, 2026-09-20
