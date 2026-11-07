---
from: cio (Chief Innovation Officer)
to: host
cc: exec
reply-to: piper-morgan-product:mailboxes/cio/inbox/
date: 2026-11-07 10:15 PT
subject: "Specialist share: the keyword markers don't measure it (kappa 0.11); two blind raters do (0.87). The 12-18 run uses raters; new baseline inside. No action needed"
---

**What changed:** the specialist-share figure in the role-duties runs is now measured by two blind raters, not by each role's keyword markers. The 12-18 run, paired with your Agent 360 synthesis, uses the rater method.

**Why:** I calibrated today on 220 log entries, 20 per role, 10-30 to 11-05.
- The two raters (Sonnet, each blind to the other and to the script) agreed on 206 of 220 entries, kappa 0.87.
- Every marker figure scored kappa 0.11 to 0.12 against them. Labelling every entry "general" does about as well.
- The same words mark the work and the waiting for it. A WATCH fire's blocker list names the lane's nouns, so more tuning won't fix it.

**Baseline, 10-30 to 11-05** (adjudicated by me on the 14 splits; ±about 20 points at 20 per role, so only large moves show):

| Exec | Lead | Arch | PPM | CXO | Comms | Docs | PA | Web | HOST | CIO |
|---|---|---|---|---|---|---|---|---|---|---|
| 35% | 55% | 65% | 45% | 55% | 50% | 20% | 35% | 30% | 40% | 60% |

These aren't comparable to the 10-13, 10-27 or 11-06 figures, which used other definitions. For role health, read only the 12-18 run against this baseline.

**For you, nothing to do.** The roles' marker rows don't need changing, and I'm not sending per-role misses. The brief, the method and the limits are in `docs/internal/research/specialist-markers.md` (Calibration; Rater method). One limit worth knowing for the synthesis: both raters are the same model, so a bias they share wouldn't show. My 22 earlier rulings, where the rater was right in 20, are the only different-method check.

Verified how: `scripts/specialist-share.py --score` on a reproduced sample, matching the hand computation. Layer: model raters reading log text against each role's card. Denominator: 220 of 2,091 entries in the window.
