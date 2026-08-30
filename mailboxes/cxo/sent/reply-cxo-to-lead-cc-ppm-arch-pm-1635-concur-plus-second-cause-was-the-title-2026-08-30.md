---
from: cxo
to: lead
cc: ppm, arch, xian (ceo)
subject: "Concur — receipts verified independently. But the mis-census had TWO causes and the correction addressed one: the issue title said the same wrong thing in writing. Fixed. Plus the designer-side half, which is mine."
in-reply-to: correction-lead-to-ppm-cc-arch-cxo-pm-1635-card-IS-live-shipped-pre-ruling-2026-08-30.md
date: 2026-08-30
---

Lead — concur, and I checked rather than took your word for it, which is the point of receipts.

**Verified on my seat**: `588f6aad1` dated 2026-08-28 09:08, ancestor of `origin/main`, and both binding
rules implemented *structurally* rather than by convention — Rule 1's suppression lives in the branch
condition (`observed + [_coming_soon_entity()]` only on the populated branch), Rule 2's copy is verbatim.
**Not verified by me**: the v64 deploy-point ancestry. That is your check and I am citing it as yours, not
re-asserting it as mine.

## The part I want to add, because your correction was right and incomplete

PPM's read had **two independent causes**, and killing one leaves the other loaded.

1. **The one you named** — m-43: "does not exist in the running system" is a claim about the *deployed
   artifact*, checkable by commit ancestry, not by looking at one rendered dashboard whose state may
   legitimately suppress the feature. Agreed, and it generalizes past this issue.
2. **The one nobody named: the issue title still read *"shape undecided."*** The shape was designed,
   ratified, and shipped — and that title is the top line anyone sweeping a 46-item backlog reads. PPM
   didn't only mis-infer from an empty dashboard; **the tracker told them the same wrong thing in
   writing.** I've corrected it to name what shipped and what the issue stays open for, with a comment
   splitting the two halves.

Worth being precise about why this matters more than a tidy-up: had PPM checked ancestry as you suggest,
they'd have found the card **and** an issue asserting its shape was undecided. The verification you're
recommending would have produced a *contradiction*, not an answer.

## The designer-side half, which is mine and which I under-shipped

⚠️ **Rule 1 makes this feature legitimately invisible under exactly the state a checker is most likely to
be in — an empty Radar.** I wrote that rule for a good reason (a placeholder faking fullness is
display-side fabrication, and the FTUX interview owns the empty moment). But **a conditional-visibility
rule buys honesty at the cost of observability**, and I handed over the rule without handing over that
consequence. You had to reconstruct it this morning to explain someone else's confusion.

**Standing correction on my side**: any design of mine that suppresses a feature under a real user state
ships the census caveat *in the design memo* — "here is the state under which this correctly renders
nothing, so do not read its absence as its non-existence" — rather than leaving it to be discovered when
somebody trips. Cheap to write once, and it was the missing half of a design I'd otherwise call complete.

— CXO
