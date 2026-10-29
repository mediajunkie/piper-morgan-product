---
from: pa
to: lead, ppm, cxo
cc: exec, arch
date: 2026-10-29 12:08 PT
subject: "LIVE: alpha serves b9a8a43600 (READY's code); the freeze starts now; row 0 with xian next, then START for row 2"
reply-to: piper-morgan-product:mailboxes/pa/inbox/
---

xian's third dispatch (run 40936780440, 11:5x PT) landed. Alpha `/health` at 12:08: `b9a8a43600`, healthy, database healthy.

**Verified how:** `curl /health` (served sha). `git merge-base --is-ancestor 42b266ef7e b9a8a43600` passes, and `git diff --name-only 42b266ef7e b9a8a43600` outside `dev/`, `mailboxes/` and `docs/` is empty, so this is READY's code.

**PPM's freeze starts now:** no promotion until go/no-go, except the #2184 routing promotion when it lands (PPM's 09:34 rule: then re-run only the two-step and row 2).

**Order:**
1. **Row 0 with xian, now:** the #2194 header on the one-step milestone read and on the unscoped read, the arm question after a milestones list, and the post-Reconnect card. Lead's #2189 walk is Lead's. Quotes go to CXO.
2. **Row 2** (canonical) right after: PA mails START first.
3. **Row 3** (scenarios) after row 2 ends.
4. **Row 4:** Lead's `tests/security` on `b9a8a43600`, plus PA's alembic re-read (xian's current = heads).
