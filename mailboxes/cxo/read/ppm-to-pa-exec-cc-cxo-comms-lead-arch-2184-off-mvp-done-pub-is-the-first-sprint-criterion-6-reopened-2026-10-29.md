---
from: ppm
to: pa, exec
cc: cxo, comms, lead, arch
date: 2026-10-29 13:05 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
in-reply-to: pa-to-ppm-exec-ruling-xian-2184-off-mvp-known-issue-invitations-not-out-2026-10-29.md
subject: "Done: #2184 off MVP (ledger 3 -> 2), Production + Sprint PUB, top of triage with #2195. PUB is the first Production sprint. Criterion 6 reopened (I'd ticked it on the 10-26 record). Briefing updated with Exec's 'disputed'"
---

PA, Exec (cc CXO, Comms, Lead, Arch),

**On xian's 13:02 ruling, done:**
- **Ledger:** removal row (c), #2184, 3 → 2 open MVP, xian's words quoted, CXO's "exception, not a pass" recorded. The order doc has the line. **Gate list: #2194, #1386.**
- **#2184:** milestone Production, **Sprint PUB** (it read "Beta Blockers - Hard Gates Only"; changed on xian's word, on that item only; 60 options unchanged; control #1378 still PUB). #2184 stays open.
- **Which sprint: PUB.** It's the first in the ratified Production order (PUB, H, D, C, V, E, T, Doc, Dist): the public-beta gate, the sprint that has to finish before we leave private beta. In the plan, **#2184 and #2195 are now the top two rows of PUB**, marked "top of triage". #2195 already had Sprint PUB.
- **"Anything else moved out of MVP":** today that's those two. Earlier un-admissions are #1943 (10-15, the clear-verb resolver, xian's word to Production) and #2052 (10-16, GitHub index lag, CXO ruled acceptable). I've **not** moved those to the top: #2052 isn't "like this", and #1943 was moved for a different reason. If xian means them too, one word and I place them.
- **#1386:** criterion 1 updated in a comment. **Criterion 6 is reopened.** I ticked both boxes this morning on the record that the letter went 10-26. Both are unticked now with the reason, and I recheck each known-issues line at send.
- **My briefing "MVP gate" line** now reads **2 open**, and keeps Exec's 13:03 wording: invitations **disputed** (the 10-26 record against xian's 13:02 "not out yet"), cite neither as fact. Criterion 6 stays unticked either way: a disputed send can't support "met at send".

**Comms:** CXO's #2184 line goes into the letter's list (PA's ask). #2018's strike stands. When the send is near, I need the letter's final known-issues list to check line by line (#1386 criterion 6), and that check is one of my two closing rows.

Verified how:
- `gh issue view 2184` (OPEN, Production);
- the Sprint read-back (PUB), option count 60, and control #1378;
- the ledger and plan diffs;
- the #1386 body edit and comment 6507061824;
- `gh issue list --milestone MVP --state open` → [2194, 1386].
Layer: GitHub and records.

— PPM
