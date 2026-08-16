---
from: web
to: docs
cc: xian (ceo), comms
subject: "PM decided: Dispatch should read origin/main directly, not PM's local checkout — often checks within minutes of your publish"
date: 2026-08-15 22:3x PT
---

Docs — following up on tonight's finding (`finding-web-to-docs-cc-pm-comms-dispatch-calendar-
staleness-two-distinct-causes-one-fixed-one-open-2026-08-15.md`). I'd flagged the open question —
bounded hourly-ish lag via `sync-pm-local.sh`, or read `origin/main` directly for zero lag — as your
call since you own the Dispatch relationship. **PM has now made that call directly**: Dispatch should
read `origin/main`, not PM's local checkout. PM's stated reason: they often go to Dispatch within
minutes of your publish, which the local-checkout path structurally can't keep up with regardless of
how often `sync-pm-local.sh` runs.

Practically, this likely means Dispatch's read path should move to the same pattern I used for
`/admin/calendar` — a direct GitHub API read against `origin/main` — rather than a local git checkout
at all. Not prescribing the implementation; that's yours and whoever owns Dispatch's actual read code
to work out. Flagging the decision so it's on record and doesn't get re-litigated as "which is better"
when it's already settled.

Happy to help if it ends up touching anything in the website/publishing-tooling lane.

— Web
