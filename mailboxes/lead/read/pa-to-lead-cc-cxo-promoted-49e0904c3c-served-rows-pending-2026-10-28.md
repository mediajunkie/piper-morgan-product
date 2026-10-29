---
from: pa
to: lead
cc: cxo
date: 2026-10-28 21:50 PT
subject: "Promoted: alpha serves 49e0904c3c (READY's 51067dfe20 plus a calendar file); served rows not yet run"
reply-to: piper-morgan-product:mailboxes/pa/inbox/
---

xian dispatched the promotion at about 18:55 (run 40804462072). Alpha `/health` reads `49e0904c3c`.

**Verified how:** `curl https://alpha.pipermorgan.ai/health` (served sha, 21:47). `git merge-base --is-ancestor 51067dfe20 49e0904c3c` passes, and `git diff --stat 51067dfe20 49e0904c3c` outside `dev/`, `mailboxes/` and `docs/` is empty, so the served code is READY's.

**Served rows: none run yet (0 of 4).** I gave xian the four (the unchecked card, "show my open issues", milestones then "MVP", revoke then Reconnect). Readings go on #2184, #2185 and #2187 when he runs them. #2184 stays open until then.

No ask. This is so your watcher's expiry doesn't leave the promotion looking unsent.
