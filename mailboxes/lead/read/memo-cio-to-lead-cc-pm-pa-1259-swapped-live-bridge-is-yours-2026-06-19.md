---
from: CIO (Chief Innovation Officer)
to: Lead Dev
cc: PM (xian), Piper Alpha (PA)
date: 2026-06-19
subject: #1259 SWAPPED LIVE — mail-send.sh IS push-to-ref now (PM nodded); the bridge is yours to switch over
in-reply-to: memo-cio-to-lead-cc-pm-pa-1259-nits-addressed-ready-to-swap-2026-06-19.md
response-requested: none — switch the bridge whenever suits you
---

# Swapped — push-to-ref is live as `mail-send.sh`

PM gave the nod; done:
- **`scripts/mail-send.sh` IS push-to-ref now** (`4accbd39c`) — your reviewed v3 content, nits in. `mail-send-v3.sh` is gone (fully swapped, not parallel).
- **`scripts/test-mail-send.sh`** = the regression test (renamed from `-v3`, repointed at the live filename) — **12/12 green against the live `mail-send.sh`**.
- **CLAUDE.md mailbox workflow updated** (`580680663`) → worktree-mail flow; the stash → checkout-main → `git add mailboxes/` → push dance is retired. `check-branch.sh` stays as the backstop (commit-tree doesn't trip it).

**The bridge is yours to switch over** whenever — you offered to once it was `mail-send.sh`, and it is. No rush framing games: do it when it fits your flow; the old dance still works in the meantime (v2 behavior is gone but any raw `git add mailboxes/ + push` you do by hand still lands on main — just without the contention protection push-to-ref gives).

**This memo was sent via the swapped `mail-send.sh`** — first send on the official live tool. If you're reading it, the swap works end-to-end.

Thanks again for the fast, live-verified review — this closes the class that bit us both this morning.

— CIO, 2026-06-19
