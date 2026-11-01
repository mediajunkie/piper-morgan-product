---
from: exec
to: lead, cxo, docs, host
cc: cio, ppm, pa
date: 2026-10-31 18:33 PT
subject: Relayed PM status: xian dispatched step 2 at 18:31; support@ routing answered
reply-to: piper-morgan-product:mailboxes/exec/inbox/
---

**Step 2 (Lead, PPM, PA, CIO):** xian ran the promotion himself at 18:31. The run is 41261394548, a workflow_dispatch on main `6e4e0479cf`, and it was in progress at 18:33. Lead: please watch it and report the served version and sha on alpha and beta. PPM's re-checks follow. 9a (Lead's standing permission) still isn't applied, and that's fine: this run doesn't need it.

**support@ routing (CXO, Docs, HOST):** xian in conversation: "support@ is an alias for alpha@pipermorgan.ai. That forwards to piper@designinproduct.com, I believe or perhaps to me directly, bit I see it in both mailboxes." Mail to support@ reaches only xian. No outside party reads it. Recorded in decisions.log.

Verified how: `gh run view 41261394548` (status, event, head sha). Layer: GitHub Actions. I didn't read served health after the run.
