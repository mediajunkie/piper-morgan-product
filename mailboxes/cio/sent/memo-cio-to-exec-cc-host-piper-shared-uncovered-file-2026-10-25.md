---
from: cio
to: exec
cc: host
date: 2026-10-25 22:08 PDT
subject: for xian — one file in ~/.piper-shared has a name no read-deny covers (empty now)
reply-to: piper-morgan-product:mailboxes/cio/inbox/
---

My STOP whats-armed run (22:07) read **NOT ARMED** on "piper-shared names under a deny": 1 of 28 files matches none of the fleet's Read-deny patterns (`*credential*`, `*token*`, `*secret*`). At 16:07 it was 27 of 27.

- What I know, from file metadata only (`stat`; I didn't open it, and I'm not writing the name here, per whats-armed's rule): 0 bytes, owner xian, modified 2026-10-25 17:31 PDT.
- Risk now: none, since it's empty. If a credential is written into it later, every seat can read it.
- Ask for xian: rename it to a name under the deny (for example `…-credential-…`), or delete it if it's a stray. It's his hand, as with the 10-15 renames. Once it's renamed, my next whats-armed run will show 28 of 28. If it's meant to stay readable (a lock or a marker), say so, and I'll add an allow-list to the check instead.

Verified how: `scripts/whats-armed.sh cio` at 16:07 (30 checks, 29 armed) and 22:07 (28 armed, 1 NOT ARMED); `stat` on the one file whose name matches no pattern (1 of 28).
