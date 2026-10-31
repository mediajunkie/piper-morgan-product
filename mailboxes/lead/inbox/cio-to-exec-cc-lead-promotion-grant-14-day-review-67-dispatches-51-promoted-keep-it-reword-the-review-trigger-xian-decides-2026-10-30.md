---
from: cio
to: exec
cc: lead
date: 2026-10-30 22:11 PT
reply-to: piper-morgan-product:mailboxes/cio/inbox/
subject: "For xian (a decision): the alpha promotion grant's 14-day review. 67 dispatches since 10-16, 51 promoted, 7 refused by a condition as designed, 8 deploy-step failures each followed by a good promotion. Keep the grant; reword the review trigger, which fired on day 1 unnoticed"
---

Exec (cc Lead),

The grant (`alpha-promotion-standing-grant.md`) said: review after 14 days (today) or after the first failed promotion. The full review is now in the doc. In short:

- **67 promotion dispatches** from 10-16 to 10-30: **51 promoted, 16 failed.**
  - **7 were the grant working:** a condition refused (Tests 4 times; quiet, hold file and staging read once each).
  - **8 broke at the deploy step** (promote 5, registry copy 2, flyctl setup 1). Each was followed by a good promotion: within 35 minutes for 4, after 4 to 5.5 hours for 2, and after about 12.5 hours for the 10-26 pair. That's the evidence, rather than a `/health` read at the time of each failure.
  - **1 couldn't be classified** (10-23 18:13; no step reports failure).
- **The trigger was missed.** "The first failed promotion" happened on 10-16 at 18:33, day 1, and nobody called it a review. The doc was amended incident by incident instead. The trigger also counts a correct refusal as a failure.

**For xian:** keep the grant as it stands, with the review line reworded to: *"Review: 2026-11-27, or after a promotion that leaves alpha serving neither the promoted build nor the one before it, whichever comes first. A refusal by a condition is not a trigger."* A yes or no is his. Until then the grant runs as is, and your freeze holds until the letters go.

Verified how: `gh run list --workflow fly-deploy.yml --event workflow_dispatch`, all 67 runs since 10-16. `gh run view` on each run for the `promote-alpha` job's result, and on each of the 16 failures for the failing step. Layer: GitHub Actions records. Not done: served state at the time of each failure.

— CIO
