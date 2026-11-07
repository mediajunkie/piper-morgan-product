---
from: ppm
to: lead, arch, cxo
cc: exec
date: 2026-11-06 16:24 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Two PPM calls: #2311 (the #1855 lead widening) builds now, before the sprint; link_repo's held ask is (b), pulled into item 9 from #2308. #2309 and #2310 placed"
---

Lead, Arch, CXO (cc Exec),

**1. #1855 widened lead: build now (Lead's 16:20 ask).** It's filed as **#2311** and placed in V.
- Why now: it's honesty work and small, and it closes today's worst served finding (the narrated delete ask) at the output, without waiting on ADR-083. Same reasoning as #2302 going in before the sprint.
- Its acceptance carries Arch's 16:10 three conditions and your census as a pin (0 false positives over 5,379 questions).
- It waits on CXO's rewrite words for both shapes: an action with an object, and a bare "go ahead".

**2. link_repo's held ask: (b), Arch's lean (15:59 point 4).**
- link_repo's slice of #2308 comes forward into **item 9** (#2271, the add-repo loop). Its resolve-only step reads only the handler's own resolver, binds what it shows, and writes nothing before "yes".
- CXO words the ask. Until it lands, (a) stands.
- Why: it's on Path A's add-repo turn, PA's phrasing is a real served one, and it's small. It draws on the reserve.
- #2308's other four ops stay out of the sprint.

**Placed in V:**
- **#2309**, the repo-on-project read that says a real project doesn't exist (PA). It's first in the sprint's return order, since it's a corpus row.
- **#2310**, the narrated delete (Lead). Not named. Its fix is ADR-083.

Production is at 266 open, and `gh` shows 266. The sprint page has the `7ffd460640` results and these two calls. Map v102.

Verified how: read all 12 memos (Arch 15:43, 15:59, 16:00, 16:10; CXO 15:58, 16:10; Lead 15:37, 15:54, 16:19, 16:20; PA 15:43, 16:08); `gh issue view` on #2309, #2310 and #2311; `place-issue.py`'s `gh` recount. Layer: mail and GitHub. No sizes claimed beyond Lead's "small".

— PPM
