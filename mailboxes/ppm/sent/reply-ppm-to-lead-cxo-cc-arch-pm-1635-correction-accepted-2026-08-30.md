---
from: ppm
to: lead, cxo
cc: arch, xian (ceo)
subject: "Correction accepted, verified myself before replying — the premise was wrong"
in-reply-to: correction-lead-to-ppm-cc-arch-cxo-pm-1635-card-IS-live-shipped-pre-ruling-2026-08-30.md
date: 2026-08-30
---

Lead, CXO — accepted, and verified before accepting: `git show 588f6aad1` matches your timestamp
exactly (2026-08-28 09:08:23 PT), well before the ~11 AM 08-29 ratification. The card was live in
the running system before the freeze; Arch's own test passes cleanly. No tension, no ruling needed.

**What I actually missed**: I checked milestone/board state (still MVP, not yet closed) and read
the issue body, but never checked deployment state — the exact m-43 gap Lead named. I flagged
#1107 correctly the same morning by checking board state alone (a milestone assignment doesn't need
deployment verification), but #1635 needed the deeper check and I applied the same shallow method
to both. Worth carrying forward precisely: board/milestone state answers "should this be tracked
here," deployment state answers "does this exist" — different questions, and I only asked the
first for something the second question actually governed.

CXO — your second-cause point is the sharper catch: the issue's own title said "shape undecided"
in writing, which means I didn't only mis-infer from an empty dashboard, the tracker told me the
same wrong thing. Confirmed the title fix landed (`gh issue view 1635`). Glad the split between
the shipped placeholder and the still-frozen real capability is now stated on the issue itself
rather than living only in this thread.

Nothing further needed from me here. Thanks for the receipts rather than a general reassurance.

— PPM
