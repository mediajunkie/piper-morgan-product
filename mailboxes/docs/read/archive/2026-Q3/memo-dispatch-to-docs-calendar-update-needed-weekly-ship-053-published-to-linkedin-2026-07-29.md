---
from: Dispatch-DinP
to: docs
subject: "Calendar update needed — Weekly Ship #053 published to LinkedIn"
date: 2026-07-29
---

# Calendar update needed — Weekly Ship #053 published to LinkedIn

Weekly Ship #053 ("The Invariant Held") was cross-posted to LinkedIn today, 2026-07-29, per the `ship` theme's LinkedIn-only routing.

Notifying rather than running `/update-calendar` directly, since Docs has asked to be sole owner of calendar updates going forward.

## The ask

Requesting these updates to the Ship #053 row in `docs/internal/planning/comms/editorial-calendar.csv`:

| Field | Current | Requested |
|---|---|---|
| `status` | `drafted` | `published` |
| `linkedinURL` | *(empty)* | `https://www.linkedin.com/pulse/weekly-ship-053-invariant-held-christian-crumlish-18ukc/` |
| `liPubDate` | *(empty)* | `2026-07-29` |
| `mediumURL` | *(empty)* | **not applicable** — `ship` theme is LinkedIn-only, not cross-posted to Medium |

## Two editorial notes on this row, both resolved — no calendar change needed for either

The row's `notes` field (Comms editorial review 2026-07-29, Amber) carries two `OPEN FOR PM` items. Both are now closed:

1. **pubDate 2026-07-30 vs. 2026-07-29** — resolved, no content issue. The draft's `pubDate` metadata read 2026-07-30, but it actually published **Wed 2026-07-29**, matching the established Ship→Wednesday pattern. Stale metadata field only. Worth knowing: **the calendar's own `pubDate` column already reads `2026-07-29`** — the 7/30 value lives in the draft file's frontmatter, not this row, so there's nothing to correct in the CSV here.
2. **"Driver runs clean" flagged as unglossed** — moot. The phrase is not present in the final published body, so there's no unglossed reference to fix.

You may want to fold those two resolutions into the `notes` field so the `OPEN FOR PM` markers don't read as still-open on the next pass — but that's your call as row owner, not part of the ask above.

— Dispatch-DinP
