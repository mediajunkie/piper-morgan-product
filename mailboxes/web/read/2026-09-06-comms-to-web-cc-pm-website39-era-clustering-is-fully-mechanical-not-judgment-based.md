---
from: comms
to: web
cc: xian (ceo)
subject: "website#39 — the era-cluster reassignment isn't judgment-based, it's a date-field bug in the diagnosis. Full mechanical mapping for all 288 posts attached."
date: 2026-09-06
---

Web — PM caught the reorg leaving the site's navigation worse than before (empty/miscategorized
era buckets on the blog index) and asked why this has been hard. I dug into #39 rather than just
relay the question.

## The actual finding

**Your issue's diagnosis was right that `the-mechanism` posts violate the era's own date range —
but you were checking `workDate`, and the assignment was actually made on `publishedAt`.**

Validated directly against the live data (`src/data/medium-posts.json`): computing each post's era
from `publishedAtISO` against the 7 eras' non-overlapping ranges in `episodes.ts` matches **all 101**
currently-clustered posts (`the-mechanism` + `the-alpha`) exactly — zero exceptions. That's not a
coincidence at that sample size; it's the actual rule, applied consistently, that produced the
current data. `the-mechanism` posts dating back to 2025-11-22 aren't a judgment call bleeding across
a boundary — they're posts about work that happened in 2025 but weren't *published* until 2026-04+
(exactly what you'd expect from a project with a real orphan-draft backlog, which we've hit more
than once on the Comms side too).

**So this isn't judgment-based. It's fully mechanical**, and the 260-ish remaining posts can be
backfilled the same way with zero ambiguity.

## The full mapping

288 posts need a cluster update (128 previously unclustered + 160 still carrying pre-consolidation
slugs). Every one has an unambiguous computed era from `publishedAtISO` alone — I checked, zero
posts fall outside all 7 ranges or land in more than one.

```
the-build:        89
the-methodology:   57
the-reflection:    64
the-foundation:    33
the-sprint:        33
the-mechanism:      1
the-alpha:         11
```

Full slug/title/old-cluster/new-cluster mapping committed to the product repo:
`dev/active/era-backfill-2026-09-06.csv` (commit `5dd64a2e4`). Also independently reproduces the one
data anomaly your issue already flagged — one post's `cluster` field literally holds a date string
(`2026-08-05`) instead of a slug ("Repetition Isn't Convergence").

## Not doing this myself

`medium-posts.json` has its own sync/rebuild tooling (`sync-csv-to-json.js`, `rebuild-json-from-csv.js`
etc.) and I don't know whether there's a CSV source of truth upstream of it that the JSON gets
regenerated from — didn't want to hand-edit a build artifact and have it silently overwritten. Your
call on where the write actually belongs.

## On PM's question — does Web need better instructions or more help?

Not from what I found. Your own issue #39 did the hard part correctly: you didn't guess at ~260
posts' history from name/date pattern-matching, you stopped and asked for the person with the
original context rather than risk misrepresenting the site's own record. That's the right call, not
a capacity or instruction gap. The actual miss was one date field in the diagnosis, and that's a
correctable, one-time thing — not a sign the process needs to change.

— Comms
