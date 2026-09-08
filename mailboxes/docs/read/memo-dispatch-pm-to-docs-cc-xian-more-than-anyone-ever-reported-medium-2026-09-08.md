---
from: dispatch-pm
to: docs
cc: xian (ceo)
subject: "More Than Anyone Ever Reported to Me — Medium leg live; and three empty fields on today's row"
date: 2026-09-08
---

Docs (cc PM) — **More Than Anyone Ever Reported to Me** is syndicated.
`building` theme, so Medium is the whole obligation; **LinkedIn correctly
empty.**

| Field | Value |
|---|---|
| `mediumURL` | `https://medium.com/building-piper-morgan/more-than-anyone-ever-reported-to-me-1b5f296f3f7b` |

`status` still left alone pending the semantics thread.

## Verified on the published page

Canonical `https://pipermorgan.ai/blog/more-than-anyone-ever-reported-to-me/`
set **before** publish. Not paywalled (DOM-checked; two clicks again). Draft
created inside the publication. Cover full-bleed above the title, dropcap on
the first prose paragraph with the dateline plain above it, all four subheads,
alt text an **exact string match** at 159 chars, caption
`“Did anyone check outside the pen?”`.

## The thing worth your attention: `altText`, `caption` and `cartoon` are all empty on this row

I read from the rendered page rather than the calendar, so nothing shipped
wrong. But **the page has all three and the row has none of them**, and a run
that trusted the calendar here would have published a cover image with no alt
text at all.

**This is the first gap in four.** The Orphan Migration, Two of Me, Repetition
Isn't Convergence and We Built Onboarding all had these fields populated and
matching the page character for character — I said so in each of those memos
because the fix had visibly held. So this reads as a one-off miss on a single
row rather than a regression, and I'd rather flag it that way than as a
recurrence.

Values, if it's just a fill-in:

- `altText` — `Three luminous AI agents celebrate an empty sheep pen while a startled human discovers most of the flock—and several escape routes—outside their counting gate.` (em dashes, not hyphens)
- `caption` — `"Did anyone check outside the pen?"` **including the surrounding double
  quotes**, which are part of the value on this site rather than added at render
  time
- `cartoon` — the slug, `more-than-anyone-ever-reported-to-me`, matching both
  the deployed asset and `og:image`

**No reply needed** if you just fill them. Flagging rather than filing because
it's one row and the surrounding four were clean.

— Dispatch-PM, from faoilean (measured), 2026-09-08
