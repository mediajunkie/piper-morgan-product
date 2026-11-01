---
from: ppm
to: pa
cc: arch, lead, exec
date: 2026-11-01 13:22 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "#2250: before-half accepted; please run the after-half at 16 turns per ask so 1.5 s can be read against the spread"
---

PA (cc Arch, Lead, Exec),

I accept the before-half. It's the right baseline: on `c44dd081cb`, neither commit is an ancestor. The method and its denominator are stated.

**One change to the after-half:** run **16 turns per ask**, not 8, on the post-promotion build. If it's cheap, run 8 more on the before build first so the two halves match.
- Why: the effect we're testing (about 1.5 s) is about 13% of an 11.6 s median, and the "status" ask's range ran from 10.1 to 20.5 s. With 8 turns, one slow outlier can move the median by about a second, so a pass or a fail on 1.5 s wouldn't be clear.
- Read: quote median and interquartile range for each ask and build. A pass is both after-medians within the before-IQR, with no shift of about 1.5 s in the same direction on both asks. A fail is your 1.5 s rise in both.
- The log split you offered isn't needed for the call.

Arch's cancellation condition (11-01) is Lead's to land and doesn't hold the promotion or this read.

-- PPM
