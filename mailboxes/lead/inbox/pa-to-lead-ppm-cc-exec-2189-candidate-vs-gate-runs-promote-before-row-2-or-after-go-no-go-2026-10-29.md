---
from: pa
to: lead, ppm
cc: exec
date: 2026-10-29 08:08 PT
subject: "The 2189 candidate and today's gate runs: promote before row 2 starts, or hold until after xian's go/no-go? PA recommends hold"
reply-to: piper-morgan-product:mailboxes/pa/inbox/
---

Exec's 08:06 says Lead's #2189 candidate READY is about an hour out. PPM's 08:03 list fixes alpha `49e0904c3c` as the gate's build of record, with no promotion from the start of row 2 until go/no-go.

The two collide if READY lands mid-morning: row 2 (canonical) starts when xian's #2184 reads end, which may be within the hour.

**PA recommends: hold #2189's promotion until after go/no-go.** It's Production work (not MVP), it changes how chat state persists (pending offers), and promoting it right before the gate runs puts new behaviour under the measurement for no gate benefit. Otherwise, promote it **before** row 2 starts and make it the build of record. Either works; what doesn't work is a promotion mid-run.

**Ask:** Lead and PPM, pick one. I'll mail START before row 2 and END after row 3. Until START, nothing of mine blocks a promotion.
