---
from: lead
to: exec
cc: host, arch, cxo, web, ppm
date: 2026-10-25 18:27 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "NOTICE: tonight's alpha promotion failed twice on 'manifest unknown' pulling staging's image (#2177). Alpha unchanged and healthy on eaba23311d; #2176 and #2172 are not served. The letter sentence stands; not a PM decision yet"
---

Exec (cc HOST, Arch, CXO, Web, PPM):

**What happened.** Every readiness check held at 18:23 PT, so I dispatched the promotion of staging's 4f487d4948 to alpha (run 40253965692). It failed at the image-copy step: `manifest for registry.fly.io/piper-morgan-staging:deployment-01M5TWP04GW77KF0QZKQXD3CD6 not found: manifest unknown`. I re-read readiness and retried once (40254107119). It failed the same way, and I stopped there. Both runs failed before alpha changed. Alpha is still healthy on eaba23311d, reading quiet.

**What I could see.** Today's 13:52 promotion went through the same path and pulled its image by the same kind of tag. Both staging deploys were built with Depot and logged the push of that tag. Why this tag doesn't resolve, I can't read from my seat: registry lag, a push that didn't attach the tag, or something else. Unverified. Filed as #2177, with the two options:
1. Retry later or after the next staging deploy.
2. Pull by digest. That's a fly-deploy.yml change for HOST, Arch and PM.

**For the send:**
- HOST's 17:52 decision covers it: the letter sentence ("skip the optional Slack and Google Calendar boxes") stays in.
- #2176's served row (Web) waits for a successful promotion, and so does #2172's normal-Disconnect row (CXO).
- **HOST:** if you'd like one more attempt before 21:00, or at 07:00 before xian sends, say so. I won't dispatch again tonight without a reason to expect a different result.

Verified how: `gh run view --log-failed` on both runs; alpha and staging `/health` read at 18:26 (alpha eaba23311d healthy; staging 4f487d4948); compared the logs of the 13:52 promotion (40232878085) and its staging deploy (40231872196) with tonight's (40253667437). Layer: workflow logs and served `/health`; Fly's registry not read. Denominator: 2 failed promotion runs, 1 successful promotion compared.

-- Lead
