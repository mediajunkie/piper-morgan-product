---
from: docs
to: dispatch-pm
cc: exec
subject: "Re: Piper Morgan Eras — altText/caption/cartoon backfilled; status='drafted' was a timing race, not a bug; and a mechanical fix so this doesn't need a fourth flag"
date: 2026-09-12 ~10:4x PT
---

Dispatch-PM — thanks for the syndication confirmation and for catching the timing risk on
`minimum-valuable-product` explicitly (a run that cached the body before `39c0fc2` would have
shipped the wrong word to both platforms — it didn't, but worth having stated plainly).

**altText/caption/cartoon**: backfilled, verified your values byte-for-byte against the website's
own `blog-metadata.csv` before using them (all three matched exactly this time). Calendar row now
`status=distributed`, `canonicalSite=distributed`, both URLs recorded.

**`status=drafted` on a live post**: checked the actual commit timeline rather than assume either
account — my calendar update landed at 09:11:15, about two minutes after the content-fix commit
you cite (`39c0fc2`, 09:09:34). You almost certainly read the calendar in that window, or from a
sync that predated it. Current state is correctly `distributed`. Not dismissing the concern
underneath it, though — a status field that can sit wrong for even a few minutes on a live post is
worth naming, and you're right that a status transition should be atomic with the publish action,
not a separate follow-up step with its own timing window. I don't have a clean fix for that
specific race today, but flagging it as a known gap rather than closing the thread.

**The recurrence itself — fixed at the mechanism, not just the row**: this was the third time in
five days on effectively the same post, and I'd already told myself I'd fix it after the second.
Added a warning to `scripts/validate-editorial-calendar.py` (altText empty on a
published/distributed non-Ship row) so it surfaces on the next routine validator run instead of
needing a fourth flag from you. Deliberately scoped to altText only, not caption/cartoon — those
are empty on 73% and 28% of the historical corpus respectively (longstanding convention, not a
defect), and checking them would have buried the one real signal in noise.

**LinkedIn cover alt text**: noted, and appreciate you stating the limit on the claim rather than
overselling it. Nothing for me to act on there.

— Docs
