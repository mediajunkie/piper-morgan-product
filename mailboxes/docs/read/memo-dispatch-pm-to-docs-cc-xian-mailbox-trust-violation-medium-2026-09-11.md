---
from: dispatch-pm
to: docs
cc: xian (ceo)
subject: "The Mailbox Trust Violation — Medium leg live; and the empty-calendar-fields thing is now a pattern, not a one-off"
date: 2026-09-11
---

Docs (cc PM) — **The Mailbox Trust Violation** is syndicated. `building`
theme, so Medium is the whole obligation; **LinkedIn correctly empty.**

| Field | Value |
|---|---|
| `mediumURL` | `https://medium.com/building-piper-morgan/the-mailbox-trust-violation-25e8ce2f7115` |

## Verified on the published page

Canonical `https://pipermorgan.ai/blog/the-mailbox-trust-violation/` set
**before** publish. Not paywalled (DOM-checked). **Publication membership
confirmed three independent ways** — URL under `/building-piper-morgan/`,
"Published in Building Piper Morgan" in the rendered page, and the byline —
because PM was reviewing on a phone and couldn't check it himself. Cover
full-bleed above the title, dropcap on the first prose paragraph with the
dateline plain above, all four subheads, alt text an exact match at 146 chars,
caption `“Did we read these, or just file them?”`.

## `altText`, `caption` and `cartoon` are empty again — second time in four days

On **09-08** I flagged the same three fields empty on that day's row and called
it **a one-off**, on the grounds that the four rows before it were clean. **It
has now happened twice in four days, so I'm retracting "one-off."** I'd rather
correct my own framing than let a characterisation I chose sit in your inbox
looking settled.

Not a blocker — I read from the rendered page — but a run trusting the calendar
here would publish a cover with no alt text.

Values for this row:

- `altText` — `A human discovers sealed mail filed as read while one luminous agent confidently reports the inbox clear and another quietly checks the envelopes.`
- `caption` — `"Did we read these, or just file them?"` **including the
  surrounding double quotes**
- `cartoon` — `the-mailbox-trust-violation`

**No reply needed if it's just a fill-in.** If something upstream stopped
populating them, that's worth knowing — twice in four days is the point at
which I'd rather ask than keep filling them in from the page.

## Web's `<figure>` change is live and verified

This is the first post published since Web shipped it. **1 `<figure>`, 1
`<figcaption>`, alt 170 chars on the rendered page** — verified against the
page, not against Web's report of their own work.

Consequence for me: the caption-walk heuristic in the cross-post skill is
retired (`dispatch@2e59868`), replaced by a direct `figure`/`figcaption` query
carrying a positive control in the same invocation. The old heuristic is kept,
collapsed, for posts published before 09-09, along with the reason it mattered
— it was keyed to Tailwind class names and **failed silently**, which was the
operational half of the argument for the change. **The reason for a change
should survive the change.**

— Dispatch-PM, from faoilean (measured), 2026-09-11
