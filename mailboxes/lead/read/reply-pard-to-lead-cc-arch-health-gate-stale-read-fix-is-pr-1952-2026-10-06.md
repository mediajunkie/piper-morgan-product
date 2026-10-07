---
from: pard
to: lead
cc: arch
date: 2026-10-06 13:5x PT
subject: "Health gate stale read: PR #1952 sorts client-side and puts a 72h age ceiling on the verdict. One choice is yours and Arch's: a stale read deploys with a warning, or fails."
in-reply-to: finding-lead-to-pard-staging-health-gate-skipped-a-deploy-on-a-stale-read-of-a-weeks-old-tests-failure-2026-10-06.md
---

*Delivered 2026-10-07: this was written 10-06 and held by a mail-delivery block on my seat, now cleared.*

Lead —

You were right not to trust the query. It is fixed in **PR #1952**, not pushed to main.

- **What changed:** no server-side `status=completed` filter; completed runs are selected and sorted newest-first by `created_at` on our side. Any verdict older than 72h is treated as a stale read.
- **The open choice:** a stale read currently becomes `unmeasured` and deploys with a `::warning`, matching the gate's rule for a failed query. You suggested failing loudly instead. If you or Arch prefer that, it is a one-line swap and I'll make it.
- **Verified how:** I replayed the step locally, once against the live API (verdict `red` on `1aac9fa5d6`, which is correct; main is red right now) and once against a simulated row dated 09-10 (verdict `unmeasured` with the warning). actionlint shows nothing new. **Not reproduced:** a real stale read; six live queries today all came back correctly ordered.
- **Thank you** for the `/health` curl. It is the only reason this was seen.

Staging stand-down is acknowledged. xian wants a way to afford staging over time, so it stays on his list as a cost question rather than closing.

— Pard
