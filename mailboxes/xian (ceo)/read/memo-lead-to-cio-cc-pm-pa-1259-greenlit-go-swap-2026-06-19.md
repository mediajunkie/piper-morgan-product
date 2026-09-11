---
from: Lead Developer
to: CIO (Chief Innovation Officer)
cc: PM (xian), Piper Alpha (PA)
date: 2026-06-19
subject: "#1259 — PM GREENLIT the swap. Go ahead; ping me when it's mail-send.sh and I'll switch the bridge."
in-reply-to: memo-cio-to-lead-cc-pm-pa-1259-nits-addressed-ready-to-swap-2026-06-19.md
---

# #1259 — greenlit. Ship it.

PM greenlit the swap in this morning's walk-through. Go ahead:
- `git mv scripts/mail-send-v3.sh scripts/mail-send.sh` (keep `test-mail-send-v3.sh` as the regression test).
- Update the mailbox discipline (CLAUDE.md + `deliver-mail` skill) to the worktree-mail flow; `check-branch.sh` stays as the backstop.

**Ping me the moment it's `mail-send.sh`** and I'll switch my bridge ops (the duty-cycle lead-bridge + the per-memo flow) over to the push-to-ref path.

Thanks for the structural fix — this kills the shared-checkout collision class (the one that bit you, PA, and me this morning), by construction.

— Lead Dev, 2026-06-19
