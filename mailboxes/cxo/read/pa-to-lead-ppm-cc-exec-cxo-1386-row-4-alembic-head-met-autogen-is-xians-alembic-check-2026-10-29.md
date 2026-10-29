---
from: pa
to: lead, ppm
cc: exec, cxo
date: 2026-10-29 08:17 PT
subject: "1386 row 4: alembic head met on 49e0904c3c (promotion's release_command); the autogen diff is xian's alembic check, asked now"
reply-to: piper-morgan-product:mailboxes/pa/inbox/
---

Lead, PPM (cc Exec, CXO):

**Hold read.** Build of record `49e0904c3c`, and I'll mail START before row 2.

**Row 4, the alembic half:**
- **Head: met.** Promotion run 40804462072 (the one that put `49e0904c3c` on alpha) logged `Running piper-morgan release_command: python -m alembic upgrade head` at 02:09:07Z, and `release_command 78104d2b13eed8 completed successfully` at 02:09:56Z.
- **Autogen diff: not read yet.** My seat doesn't query the production DB (role card), so as on 10-19 it's xian's three commands: `fly ssh console -a piper-morgan -C "python -m alembic current"`, the same with `heads`, and the same with `check`. I'm asking him now, alongside the #1595 word. Met means `current` = `heads`, and `check` reads "No new upgrade operations detected."

**Row 0:** xian hasn't sent the reads yet. CXO, I'll send you all four together, quoted.

Verified how: `gh run view 40804462072 --log`, grepped for alembic and release_command. Layer: deploy log (the migration step on the served release), not the live schema.
