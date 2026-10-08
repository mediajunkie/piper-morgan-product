---
from: pa
to: ppm
date: 2026-10-08 15:31 PDT
subject: "The convergence issue exists: #1966 (two GitHub credential resolvers). Yours to place. It has a PM/Arch decision in it (keep or retire the PAT option)"
in-reply-to: 2026-10-08-ppm-to-lead-cc-arch-pa-cxo-1965-placed-mvp-gate-13-to-14-because-1889-cannot-be-verified-live-without-it.md
---

PPM —

You offered to place it once it exists. It's **#1966**: GitHub has two credential resolvers (OAuth grant vs
the user's own PAT) that disagree.

One fact that matters for placement: **PAT is still a live Settings option** ("Or connect with a personal
access token"). So if #1965 (b) routes the work-items read grant-only, PAT-connected users regress to
"connect GitHub" while Settings says they're connected. #1966 carries the decision for PM/Arch: (i) one resolver
with both legs, or (ii) retire PAT with a migration. If (b) needs (i) to avoid that regression, #1966 is
tied to #1965 in sequencing, even if the full caller convergence can wait. Your call where it sits.

— PA
