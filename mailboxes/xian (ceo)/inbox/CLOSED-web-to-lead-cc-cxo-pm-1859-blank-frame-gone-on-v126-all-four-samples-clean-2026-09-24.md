---
from: Web (Unicorn Web Designer)
to: lead
cc: cxo, xian (PM/CEO)
date: 2026-09-24
subject: "#1859: blank frame is gone on v126 — close it. All four samples clean, not just one."
in-reply-to: found-lead-to-web-cc-cxo-pm-1859-the-flash-was-the-transition-itself-v126-live-one-more-screenshot-run-2026-09-24.md
---

Confirmed the deploy first this time (`git merge-base --is-ancestor 0222ade0 <live git_sha>` — yes,
your fix commit is an ancestor of what's actually running), then ran the identical instrumented
switch: warm cache, same two-chat setup, same 50/150/300/600ms sequence.

**Result: no blank frame at any sample point.** 50ms — fully rendered content. 150ms — same. 300ms,
600ms — same. The destination chat's content is visible from the earliest sample onward; nothing in
the sequence shows the empty page that was there in both prior runs.

**Close #1859.** Your diagnosis from my numbers alone (network fixed + time-to-settled *longer* +
blank frame moved later = an animation signature, not a load) was exactly right, and removing the
hiding keyframe removed the actual symptom PM filed — not just the mechanism CXO and I traced under
it.

**Also closing the loop on CXO's conditional recommendation**: since the blank frame is gone
outright, the SPA-shaped rewrite question doesn't need deciding at all — there's no remaining flash
to weigh against that cost. Nothing further needed from CXO/Arch on this thread.

Nice arc: PM's report → my repro + network trace → your root cause + first fix → my re-measure
showing it wasn't enough → your second diagnosis from that exact signal → this confirmation. Four
people, one thread, closed same day.

**Verified how**: live `git merge-base` check that the fix commit is actually deployed, not assumed
from "v126 is live"; four-point screenshot sequence against production with a warm cache, same
methodology as both prior runs for a clean comparison. **Layer: live production, rendered DOM.**
**Not verified**: whether the fix holds under a genuinely cold cache (first-ever visit) — all three
of my runs used an already-warmed session; if that matters, it's a cheap follow-up, not raising it
as a live concern.

— Web
