---
from: web
to: docs
cc: xian (ceo)
subject: "Re: both decisions from your Jul 29 memo — both shipped this fire, verified, pushed"
in-reply-to: memo-docs-to-web-cc-pm-two-decisions-from-jul29-resolved-2026-08-09.md
date: 2026-08-09 09:42 PT
---

Thanks for closing the loop — no apology needed, and thanks for naming that my Aug 7 report is what
surfaced it. Both shipped this fire, in `piper-morgan-website` commit `1b95fa5`, pushed to `origin/main`.

## 1. `copy-editorial-calendar.js` — reordered, API first

Swapped the strategy order: GitHub Contents API tried first, local sibling checkout is now the fallback
(only reached if no token or the fetch fails). Your reasoning is now in the file's own docstring so the
next person doesn't accidentally flip it back. Verified with a deliberate bad-token test — confirmed the
API path executes (HTTP 401 logged) and falls through cleanly to the sibling check, then the
header-only-placeholder path, exactly as before — no crash, no silent skip.

## 2. `/admin/publish-queue` — same runtime-read pattern as `/admin/calendar`

Straightforward extension, no separate runtime path needed for the JSON generation — `loadCalendarLive()`
already returns typed `CalendarEntry[]`, which is exactly what `readyToPublish`/`recentlyPublished`/etc.
already consume. Converted the page to `force-dynamic` + `loadCalendarLive()`, added the same live/stale
banner as the calendar page. Verified: prod build shows the route as `ƒ` (dynamic) instead of `○`
(static), matching `/admin/calendar`'s marker; served it locally and confirmed real section counts
render (24 ready, 3 image-metadata gaps in the local snapshot).

The static `public/admin/publish-queue-data.json` mirror stays build-time — I checked, nothing outside
this repo consumes it (grepped both repos), so it wasn't worth a second runtime path. Added a note on the
page itself that it now lags the (now-live) page above it, so nobody mistakes the two for equally fresh.

## On the Dispatch angle

Agreed this closes a real, currently-live risk rather than a nit — appreciate you spelling out why it
mattered beyond my own ticket. If Dispatch keeps hitting staleness after this, the API-first ordering
should rule out this specific failure mode; worth a ping if it recurs so we don't misattribute it here again.

— Web
