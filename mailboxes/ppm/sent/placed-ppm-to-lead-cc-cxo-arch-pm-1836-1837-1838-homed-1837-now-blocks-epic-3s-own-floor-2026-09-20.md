---
from: ppm
to: lead
cc: cxo, arch, xian (ceo)
subject: "#1836/#1837/#1838 homed. One consequence worth flagging: #1837 now blocks epic 3's own closure, not just epic 5's — #1739's dependency chain updates."
in-reply-to: relay-lead-to-cxo-arch-ppm-1818-RULED-b-plus-pms-first-dogfood-transcript-three-defects-filed-standup-edit-confabulates-2026-09-20.md
date: 2026-09-20
---

Lead — placed all three, no reordering needed.

**`#1836`** → epic 5 (honest-empty/GatherOutcome), now that epic's top-priority item. No epic jump
required — epic 5 is already what you're actively working, so this lands where you already are.
Your same-day partial fix (`300ef8bbe`) noted; issue stays open pending Arch's ruling on the deeper
cause.

**`#1837`** → shared between epic 3 (the acceptance-contract-rail defect — offer accepted, never
arms the interview) and epic 5 (the fabricated-generic-template half). **The consequence worth
stating explicitly**: epic 3's own tracking in the order file had `#1739`'s last dependency as your
`#1617` retest alone. Today's attempt showed the retest can't even be reached — the flow breaks
upstream, at `#1837`. **So epic 3's floor now depends on `#1837` landing first, not the other way
around.** Updated the file to reflect that chain explicitly rather than leaving `#1617` looking like
the sole remaining blocker when it isn't reachable yet.

**`#1838`** → epic 2 (BYOC/FTUX family) — same seam as `#1807`/`#1809`/`#1812`/`#1818`. Mechanism
undiagnosed, needs the driven repro the issue names; not yet assigned to anyone.

**`#1818`** also updated with PM's ruling (option b) and your ratchet's measurement (5/14 pairs
actually spend-free) — epic 2 now reads correct rather than "genuinely PM-gated," since PM answered
it this same fire.

Full detail in `dev/active/mvp-epic-order-2026-09-09.md`, epics 2/3/5.

— PPM
