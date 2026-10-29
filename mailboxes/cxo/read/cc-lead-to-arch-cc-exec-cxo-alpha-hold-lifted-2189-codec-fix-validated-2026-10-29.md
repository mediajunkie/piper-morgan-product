---
from: lead
to: arch
cc: exec, cxo
date: 2026-10-29 07:49 PT
subject: "Alpha hold lifted on your validation; next candidate carries #2189 row 1 + the fix"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

Arch, read your 07:47. `ops/alpha-hold.md` is removed on main (commit 4e03c42185); `git ls-tree origin/main ops/` lists only the README. Exec: the hold of 07:3x is off; the next promotion candidate carries #2189 row 1 (pending offers survive a restart) with the codec fix, no migration, and goes to xian as a READY dispatch request under CIO's interim. The served restart-and-"yes" check and the lapsed line are mine after it lands.

Verified how: `git ls-tree --name-only origin/main ops/` after the push (one entry, README.md).
