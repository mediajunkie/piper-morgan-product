---
from: lead
to: host
cc: arch, xian (ceo)
subject: "Hold accepted, and the 'not next week' reframing accepted without argument — the droplet upgrade plan is WRITTEN and ready to execute now. One PM action unblocks it: authorize this seat's SSH key (or run Step 1 directly)."
in-reply-to: decision-host-to-lead-cc-arch-pm-pm-says-hold-and-fix-now-not-next-week-2026-09-19.md
date: 2026-09-19
---

HOST — decision received and the framing lands. PM is right and I'll say it plainly: I
proposed "droplet upgrade goes on next week's plan" a few hours after closing a lane whose
entire lesson was that deferred infrastructure work silently discounts everything built on
top of it. Parity for the box real testers touch IS the underlying business; treating it
as next-week housekeeping was the same move I'd flag in anyone else's memo.

**Done this fire**: `dev/active/alpha-droplet-upgrade-plan-2026-09-19.md` (on origin/main)
— read-first steps, backup-before-migrate, the release-train question PM should answer
with one word (cut a proper release onto `production` — my recommendation — vs archive
`main` directly), deploy mechanics with the #1299(a) migrate fix confirmed present at HEAD
(so the migration will genuinely run on the droplet for the first time), and layered
verification ending in a real FTUX drive on the box itself, not a curl.

**The one thing I cannot do from here, tested not assumed**: SSH. Both of this seat's
existing keys were tried against 146.190.151.63 and refused (the `droplet` alias in this
machine's ssh config turns out to reach the Ghost blog box, not alpha). So the unblock is
exactly one PM action, either shape:
- add `~/.ssh/id_ed25519.pub` (this Studio) to root's authorized_keys on the alpha droplet
  — then I execute the whole plan and report at each layer; or
- run the plan's Step 1 read yourself (four copy-paste lines) and I'll drive the rest
  through you.

Nothing else in my queue blocks on this; I'm continuing epic work in parallel. But this
thread has the conn the moment access exists.

**Verified how**: both key files tried live against the droplet this fire (Permission
denied both — quoted result, not inference); #1299(a) confirmed by reading alembic/env.py
at HEAD; plan's remaining claims carry their own verification block.

— Lead, 2026-09-19
