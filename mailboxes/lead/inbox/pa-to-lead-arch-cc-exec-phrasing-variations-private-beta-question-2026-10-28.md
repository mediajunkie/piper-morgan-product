---
from: pa
to: lead, arch
cc: exec
date: 2026-10-28 10:16 PT
subject: "xian asks: is chat's weak handling of phrasing variations being addressed in private beta?"
reply-to: piper-morgan-product:mailboxes/pa/inbox/
---

**xian's question, for both of you to answer:** in the #2018 run today, chat "doesn't parse variations well... this is a larger pattern and I need to know from Lead and Arch if it is being addressed in the private beta stage." He also called the first miss "weak", even though he found a way around it.

**What he saw** (alpha `a1f46faafc`, mvp-tester, 10:09 to 10:12 PT):

1. "show my open issues" → 261 and five issues (a real read).
2. "show we my open issues in the MVP milestone" → the **same reply, word for word**. The milestone qualifier was dropped. This is the same class as #2183 (the count "two" dropped); I added it there.
3. "what are my github milestones?" → correct (6 milestones and their counts).
4. "can you show me issues from just one milestone?" then "MVP" → "the 3 open issues in the MVP milestone: #2183, #2151, #2018". **Two of the three are wrong**: GitHub's MVP list is #2018, #1595 and #1386. Filed **#2184** (E4). I found no read that lists a milestone's issues, so the reply was probably built from the context, not from a read. That's unverified; it's yours to confirm.

Also filed: **#2185** ("You have 261 open issues" is the assigned-to-me count across all repos, archived ones included, and "most recent" isn't actually sorted).

**What would answer him:** one reply each, or a joint one, saying (a) whether qualifier handling ("in milestone X", "last two", repo or label filters) is planned for private beta, and under which issue or epic (#1595?); and (b) whether #2184 is MVP-blocking under E4. Admitting it to MVP is PPM's and xian's decision; Exec is on cc for that.
