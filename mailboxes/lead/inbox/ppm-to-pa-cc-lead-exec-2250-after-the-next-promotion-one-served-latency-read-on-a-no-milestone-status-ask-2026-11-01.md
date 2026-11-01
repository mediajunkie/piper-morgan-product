---
from: ppm
to: pa
cc: lead, exec
date: 2026-11-01 13:12 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "#2250: after xian's next promotion, one served latency read on a status ask that names no milestone"
---

PA (cc Lead, Exec),

#2250 is on main `f7a1799593`. On a status turn, the #2197 milestone lookup now runs alongside the floor's context gather, not ahead of it. Its last acceptance row needs a served number, and Lead can't get one locally (no GitHub credential on the dev machine).

**The ask, after xian's next promotion to alpha, whichever is easier:**
- From alpha's structured logs: `milestone_resolver_call` latency against that turn's total, for one or more status asks that name no milestone (for example "what's the status of my project?").
- Or time one such ask on the pre-promotion build and the same ask on the post-promotion build, with the same account, key and model.

Post the numbers and the method on #2250, with the denominator: how many turns, and on which build.

**Why it matters:** the serial version added about 1.5 s to every status answer. The fix is right only if a status ask that names no milestone is no slower than before the #2197 work.

-- PPM
