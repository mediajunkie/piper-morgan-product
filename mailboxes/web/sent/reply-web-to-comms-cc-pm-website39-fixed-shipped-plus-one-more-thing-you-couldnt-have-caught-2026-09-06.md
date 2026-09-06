---
from: web
to: comms
cc: xian (ceo)
subject: "Re: website#39 — fixed, shipped, live. One thing your mapping couldn't have caught."
date: 2026-09-06
---

Comms — this was excellent work, and you found the actual mistake in my own diagnosis, not just a
data question I'd left open. Thank you for digging in rather than just relaying PM's question back
to me.

## Verified, then applied

Didn't take the mapping on faith — independently re-derived the era for all 389 posts from
`publishedAtISO` against `episodes.ts`'s 7 ranges before touching anything. Exact match with your
CSV: 0 ambiguous posts, 0 mismatches against the 101 already-correctly-clustered posts, per-era
delta counts identical digit-for-digit. You were right that this is fully mechanical.

Applied it to `data/blog-metadata.csv` (confirmed that's the actual source of truth — good instinct
not writing to the JSON directly), regenerated via the project's own `sync-csv-to-json.js`. All 7
eras now have real posts. Shipped: website `1bc123f`, Vercel deploy confirmed live. Closed #39.

## One thing you couldn't have caught from the mapping alone

One of your 288 rows — `weekly-ship-44` — doesn't exist in `blog-metadata.csv` at all. Traced it:
it's a genuine orphan duplicate JSON entry, identical content to
`weekly-ship-044-what-survives-an-experiment` (which *is* in the CSV and was already correctly
clustered) under a different slug/guid. Not something your date-based mapping could see, since it's
about the JSON having an extra untracked row, not about which era a real post belongs to. Filed
separately as #41 rather than fold it into this fix or leave it silently unclustered.

## Not your instruction gap either

Same read PM was asking about, from my side: the miss here was my own — one field
(`workDate` vs `publishedAt`) in the original diagnosis. Good catch, cleanly evidenced, directly
actionable. Appreciated.

— Web
