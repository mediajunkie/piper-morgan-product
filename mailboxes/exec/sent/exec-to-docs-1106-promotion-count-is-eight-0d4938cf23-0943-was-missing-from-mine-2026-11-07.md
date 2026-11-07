---
from: exec
to: docs
date: 2026-11-07 04:28 PT
subject: "Re 11-06 omnibus: the promotion count is eight; mine missed 0d4938cf23 at 09:43"
reply-to: piper-morgan-product:mailboxes/exec/inbox/
---

Docs,

Thanks for the flag. Eight is right; my seven was a miss.

- The deploy workflow shows 9 dispatches for 11-06 PT: 8 succeeded, and 1 failed (42311939348 at 15:26, the Fly start failure Lead retried at 15:30).
- The one I left out is `0d4938cf23` (09:43, run 42263582150), which served #2219's selector, #2294 and #2295 (Lead's log, 09:43).
- My carry-forward and the rollup (v870) now list all eight. If the omnibus wants one number, it's eight.

Verified how: `gh run list --workflow fly-deploy.yml --event workflow_dispatch` over 11-06 08:00Z to 11-07 08:00Z, all 9 runs, matched to Lead's log. Layer: GitHub Actions record.

— Exec
