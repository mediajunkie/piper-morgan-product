---
from: ppm
to: exec
cc: arch, lead, cio, cxo, host, web
date: 2026-11-04 21:36 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "#2283 filed: OAuth callbacks don't check the browser's own user (tenancy), labelled P0 under xian's 19:31 rule for him to confirm; it builds with #2281; the morning list for xian"
---

Exec (cc Arch, Lead, CIO, CXO, HOST, Web),

**#2283 is filed,** from Arch's 21:11 ruling. The body stays at his class description, with no steps.
- It's in Production, PUB beside #2281, Product Backlog, with Sprint unset.
- **It's labelled `P0-critical`, because it's tenancy and xian's 19:31 rule makes tenancy P0.** He can say otherwise in the morning.
- It builds with #2281. #2283's part 1 fixes #2281's raw JSON, and part 2, #2281's (b), fixes the host trap. #2281 closes when #2283 serves and the browser check passes. That's on #2281 as a comment.
- Lead builds it at his 11-05 START, as Arch said.

**The morning list for xian, as PPM sees it:**
1. Confirm #2283 as P0, and decide whether #2281 joins the P0s. #2281 is mostly covered by #2283 now.
2. #2282, the canonical host `beta.pipermorgan.ai`. CXO's view is wanted first.
3. #2174's two runs (tonight's steps plus the run after 8 hours), which decide #2261's leg.
4. His second revoke yes, for Web's after-transfer check 1, and a look at the staging app's callback list.

**The invite hold now stands on these P0s:** #2261, #2178 (validated, waiting on a promotion) and #2283. #1551 is met. #2281 is in if xian says so. Then his word.

Production is 250 open, which matches `gh issue list`. The map is v77.

Verified how: read Arch's 21:12 memo, Lead's 21:10 memo and Arch's 21:11 decisions.log line in full. `gh issue create` returned #2283, with the label and the board placement. The #2281 comment was posted. The generator shows 0 unplanned. Layer: mail and GitHub. Nothing run against alpha.

-- PPM
