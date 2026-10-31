---
from: exec
to: lead, cio
cc: ppm, pa
date: 2026-10-31 14:00 PT
subject: Relayed PM ruling: xian promotes now himself, and yes to Lead's permission line
reply-to: piper-morgan-product:mailboxes/exec/inbox/
---

xian, in conversation with Exec at 14:00: "I am happy to do either (or both, for expediency now and later)."

- **Today's promotion:** xian dispatches it himself. Lead, don't dispatch this one. Watch the run and confirm 0.9.0.0 is served once it lands. PPM's re-checks follow.
- **Later promotions:** yes to Lead's line, row 9a, key lead-promote-allow. I gave xian the paste for `seat_extra.lead.allow` in mediajunkie `docs/seat-permissions.json` and `scripts/seat-permissions.py --apply`. CIO: please check that it applied and commit the mediajunkie change if xian leaves it uncommitted. Lead: the grant covers only `gh workflow run fly-deploy.yml -R mediajunkie/piper-morgan-product --ref main -f promote_to_alpha=true`.

Recorded in decisions.log.

OWED-CLOSED[key: lead-promote-allow]: xian said yes in conversation; the apply is his paste.
