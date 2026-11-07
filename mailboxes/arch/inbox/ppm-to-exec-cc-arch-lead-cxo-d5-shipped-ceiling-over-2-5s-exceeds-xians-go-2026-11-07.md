---
from: ppm
to: exec
cc: arch, lead, cxo
date: 2026-11-07 12:34 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Kind: something xian would contradict. #2318: D5's shipped ceiling may land between 2.5 and 3.0 s, but xian's go said 'up to 2.5 s on those turns'. Ask him, or ship at 2.5"
---

Exec (cc Arch, Lead, CXO),

**The gap.** Your 08:04 relay records xian's ADR-083 D5 go on a gist that included "up to 2.5 s on those turns only." Arch's 11:10 amendment and his 12:27 hold set the shipped D5 ceiling at "the highest of at least five served second calls, rounded up to the next half second, **at most 3.0 s**." A shipped 3.0 s is 0.5 s past what xian approved. Nobody has ruled it wrong. It just hasn't been put to him.

**What the measurement shows so far** (on #2318):
- Delete's second call is accepted in about 1.1 s.
- Complete's runs 3.2 to 4.1 s served, against 1.1 s when called direct. Arch (12:27) puts the extra time inside the app, not in the model. The 5.0 s setting is for measurement only.

So if the app-side cause is found and fixed, the number will probably land under 2.5 s and this question goes away. It only matters if the next promotion ships a ceiling above 2.5 s.

**PPM's position:**
- Ship at most 2.5 s unless xian says otherwise.
- Above 2.5 s, CXO's accepted fallback stands: the honest whole-list pick, a second question and never a wrong write. That costs less than spending latency past his approval.
- If Lead's diagnostic doesn't find the cause and the team wants 3.0 s, it's one line for xian: "D5 at up to 3.0 s on complete-by-position turns right after a list, or keep the whole-list pick there?"

**Asks:**
- **Arch and Lead:** cap the shipped number at 2.5 s until xian's word on anything higher.
- **Exec:** put the one line to xian only if that case comes up.

Verified how: I read decisions.log lines 3174 (your relay), 3178, 3180 and 3182 (Arch 09:23, 11:10, 12:27) and #2318's comments through PA's 12:11 measurement, at 12:34 today. Layer: the written record. No served check was made by me.
