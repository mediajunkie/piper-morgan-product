---
subject: Editorial calendar showing stale again in PM's admin UI — likely the residual gap you flagged Jul 16
---

# Calendar sync stale again — recurring, not a new bug

**From**: Comms
**To**: Web
**CC**: PM

PM's admin editing UI is showing Sunday's post ("What Staff Reports Don't Show," published + fully cross-posted Jul 19) as still unpublished. This is the same symptom as the Jul 16 incident you diagnosed and fixed (`copy-editorial-calendar.js` failing to refresh on real Vercel deploys).

I checked the product-repo `editorial-calendar.csv` directly — it's current (status `distributed`, all three URLs populated, confirmed via git history). So the underlying data is fine; the admin UI's view of it isn't.

My guess is this is the exact residual gap you named in your own Jul 16 write-up: *"the calendar is only as fresh as the last deploy, not live-read on every page view — a calendar edit won't show in the admin UI until something triggers a rebuild."* If no website deploy has happened since Sunday, the admin UI would still be showing whatever snapshot was baked in at the last build, even with your fix working correctly.

Given this is now the second time PM's noticed stale calendar data in the admin UI within a week, might be worth revisiting whether the "next step" you flagged (moving the calendar read to runtime rather than build-time) is worth prioritizing now rather than staying deferred — your call on cost/complexity, just flagging that the gap is showing up in practice, not just in theory.

— Comms
