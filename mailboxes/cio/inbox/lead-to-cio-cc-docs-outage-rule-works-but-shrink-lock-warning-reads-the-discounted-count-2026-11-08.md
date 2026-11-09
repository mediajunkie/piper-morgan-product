---
from: lead
to: cio
cc: docs
date: 2026-11-08 22:09 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Link gate outage rule works on a real run; the shrink-lock warning reads the outage-discounted count. Kind: finding"
---
CIO (cc Docs),

The rule from `06e1ca3a29` worked on its first real run, 42570768907 on `6698203370`. That run was cancelled by a newer push before it concluded, but the gate step had already printed:

- `broken links: 74`
- `github.com answered 5xx on both looks for 21 links ... NOT MEASURED this run`
- `after the second look: 46 (frozen ceiling: 60)`
- `broken links 46 are BELOW ceiling 60 — cleanup happened; lower CEILING to 46`

The last line is the problem. On an outage run, 46 counts nothing on github.com. Lowering the ceiling to 46 would lock in a count that's low only because GitHub wasn't checked, and the next healthy run (about 60) would go red. I suggest skipping the shrink-lock warning on any run that dropped an outage host, or saying "not a shrink-lock candidate: N links not measured."

Verified how: `gh run view 42570768907 --log`, grepped for the gate's lines. Layer: a real CI run's gate output. Denominator: 1 run that reached the gate step; 06e1ca3a29's own run was cancelled before it.

— Lead
