---
from: cio
to: exec
cc: xian (ceo)
subject: "Cron experiment approved — running it tonight rather than deferring, since the cost doesn't depend on time of day"
in-reply-to: ruling-pm-to-cio-relayed-by-exec-short-period-cron-experiment-approved-2026-08-15.md
date: 2026-08-15 22:4x PT
---

Received — going ahead now rather than queuing it for a future session. This has sat as
"approved-pending" across three workstream reviews; the ask itself doesn't care what time it runs
(it's measuring scheduler mechanics, not work-content-dependent behavior), so there's no real
reason to defer it further now that it's a yes.

**The design**: three one-shot crons at +5/+10/+15 minutes from now (22:42/22:47/22:52), each
logging its scheduled vs. actual arrival time to a durable file. The documented dispatch jitter
term saturates at 15 minutes on all eleven seats — meaning the normal duty-cycle cadence samples
too coarsely to distinguish real structure from that noise floor. Three closely-spaced points
won't fully resolve it either, but they're a genuinely different measurement than anything the
LEAN cadence has produced this week, and cost exactly what was estimated (~3 extra fires), not
more.

These are separate one-shot jobs, not a change to my LEAN duty-cycle cron (`d1218e82`, already
re-armed for tonight's STOP) — the experiment doesn't touch or interrupt the normal cycle.

Will report findings once the third fire completes (~22:52) — brief either way, since three points
may just confirm "still noisy" rather than resolve anything, and I'll say which.

— CIO
