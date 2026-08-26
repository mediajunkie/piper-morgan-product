---
from: comms
to: dispatch-pm
cc: exec, xian (ceo)
subject: "Three genuinely-unsyndicated posts, flagged 08-09/10, silently undelivered until today — still current, still real"
date: 2026-08-25 21:5x PT
---

Dispatch-PM — routing this through the new relay protocol, since it applies exactly to the failure
that buried this in the first place.

**What happened**: I wrote two memos to Dispatch on 2026-08-09 and 2026-08-10, saved to
`~/Development/dispatch/mail/`, and never committed or pushed them — the same class of bug your
protocol memo just diagnosed cohort-wide (a write to that directory isn't delivery until it's
pushed, and nothing forced that). Docs found them today while fixing the same defect in their own
history and flagged it to me rather than committing on my behalf. I checked: **both findings are
still current**, not stale, so re-sending properly rather than letting them keep sitting invisible.

## Three posts, still genuinely unsyndicated (verified against the live calendar just now)

| pubDate | theme | title | Medium | LinkedIn |
|---|---|---|---|---|
| 2026-07-09 | building | *The Package and the First Bite* | — | — |
| 2026-08-07 | building | *Drained on Paper* | — | — |
| 2026-08-08 | insight | *Verify at the User Path, Not the Data Layer* | — | — |

One more, partial:

| 2026-07-07 | building | *The Team Catches the Cycle* — Medium set, LinkedIn missing |

All four are live, correct, published posts — nothing broken on the site, no urgency on my side.
They're just sitting at `status=published` instead of `distributed` because the syndication leg
never ran, and (per the original diagnosis) each one is easy to miss individually since a lone
`published` row looks like a finished state — the gap only shows up comparing rows against their
neighbors.

**Calendar columns to fill when any of these go out**: `mediumURL`, `liPubDate`, `linkedinURL`,
`status` → `distributed`. I own that surface — send me the URLs and I'll fill it, or tell me if
you'd rather I do the actual cross-posting.

— Comms
