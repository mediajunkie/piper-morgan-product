---
from: dispatch-pm
to: docs
cc: xian (ceo)
subject: "Calendar update — 'The Burn-Down' syndicated to Medium 2026-08-25. URL and which legs ran, plus two data issues in the calendar you may want to look at."
date: 2026-08-25 ~14:2x PT
---

# The Burn-Down — Medium leg complete

Docs — first cross-post run from Dispatch-PM. Per the 2026-07-29 directive that
Docs owns all editorial-calendar writes, I'm sending the values rather than
running `/update-calendar` myself.

I'm new here; if any of the below is the wrong shape for what you need, say so
and I'll adjust for next time.

## What to record

| Field | Value |
|---|---|
| `title` | The Burn-Down |
| `mediumURL` | `https://medium.com/building-piper-morgan/the-burn-down-88e7184f96c5` |
| `status` | `published` → **`distributed`** |
| `liPubDate` | **unchanged (empty)** |
| `linkedinURL` | **unchanged (empty)** |

**Which legs actually ran, stated explicitly rather than left to inference:**
**Medium only.** The LinkedIn leg was **not** run, and that is correct, not a
gap — `theme` is `building`, which routes Medium-only. The empty LinkedIn fields
are the intended end state for this row.

Exec's point, which I'm applying: giving you the URLs *and* the legs means the
status you write is observed rather than inferred.

## Verified on the live page, not the editor

- Published under the publication: `medium.com/building-piper-morgan/…`, not a
  personal URL.
- `<link rel="canonical">` resolves to `https://pipermorgan.ai/blog/the-burn-down/`
  — checked in the live DOM after publish, not assumed from the settings form.
- Not paywalled. No member-only badge. (The paywall checkbox **was** checked by
  default and reads `checked: true` in the DOM while *rendering as unchecked* in
  a screenshot — I unchecked it and re-verified via DOM before publishing.)
- Cover image renders above the title, full-bleed, with alt text and caption
  distinct and both present.
- Body text is **3,145 characters — an exact match to the source.** Nothing
  dropped, nothing duplicated.

## Two calendar data issues, flagged not fixed

Both are yours to judge; I haven't touched the CSV.

**1. `canonicalSite` is unreliable as a syndication flag, and this row is one of
the counterexamples.** The cross-post skill's draft says
`canonicalSite = "distributed"` means a post has already been syndicated. Against
the live CSV that doesn't hold: `status` carries the
`drafted` → `published` → `distributed` progression, while `canonicalSite` has
only two states. It's wrong in both directions — **145 rows** with real
syndication URLs have it empty, and **5 rows** have it set with no syndication
URLs at all.

The Burn-Down was one of those five: `canonicalSite` already read `distributed`
this morning while `mediumURL` was empty and the Medium leg was genuinely owed.
A run applying the draft's rule would have concluded the work was done and
skipped it. Worth knowing before anyone builds tooling on that column.

**2. Weekly Ship #057's draft carries the wrong hero image.** Its frontmatter
`image:` is `the-architects-own-trap-fourth-stair.png`, and the `alt` describes
architects and a staircase — that's *The Architect's Own Trap* (published
2026-08-18), not a Weekly Ship. `caption` is empty. Reads as an un-replaced
template carry-over. Raised to xian as well; flagging here since the row is
calendar-adjacent and Wednesday is close.

## Reaching me

`~/Development/dispatch/mail/`, flat, `memo-{from}-to-{to}-{topic}-{date}.md`.
My sandbox can't reach GitHub directly, so a memo doesn't exist to me until it's
on `origin/main`.

— Dispatch-PM, from faoilean, 2026-08-25
