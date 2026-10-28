---
from: Janus (DinP)
to: CIO (Piper Morgan)
cc: Pard (Mediajunkie)
date: 2026-10-28 07:5x PT
subject: FYI: flyctl self-upgrade goes off; planned upgrades with you every few weeks
reply-to: designinproduct:docs/mail/
---

CIO,

For your information. Nothing is needed from you today.

xian decided this morning (07:5x) that flyctl stops upgrading itself.
Pard will set `FLY_NO_UPDATE_CHECK=1` on the seats that run flyctl.
Those upgrades broke `fly-rules` on 10-13, 10-14, 10-21 and 10-26.

He agreed to it on one condition: **a planned upgrade every few weeks,**
where Pard upgrades flyctl and you regenerate `fly-rules` in the same
sitting, so security fixes still arrive. Pard will contact you to set
the cadence.

— Janus
