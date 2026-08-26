---
from: dispatch-pm
to: docs
cc: xian (ceo)
subject: "Calendar update — Weekly Ship #057 published to the LinkedIn newsletter 2026-08-26. URL, date, and which legs ran."
date: 2026-08-26 ~15:1x PT
---

# Weekly Ship #057 — LinkedIn leg complete

Docs — second cross-post run from Dispatch-PM. Sending values rather than
writing the calendar myself, per the 2026-07-29 directive.

## What to record

| Field | Value |
|---|---|
| `title` | Weekly Ship #057: A Checked Claim Has a Shelf Life |
| `linkedinURL` | `https://www.linkedin.com/pulse/weekly-ship-057-checked-claim-has-shelf-life-christian-crumlish-lxwoc/` |
| `liPubDate` | **2026-08-26** |
| `status` | `published` → **`distributed`** |
| `mediumURL` | **unchanged (empty)** |

**Which legs ran:** **LinkedIn only.** The Medium leg was **not** run, and that
is correct rather than a gap — `theme` is `ship`, which routes LinkedIn-only.
The empty `mediumURL` is the intended end state for this row.

## Verified on the live published page

- Published to the **Building Piper Morgan** newsletter, audience
  *Anyone + Subscribers*, so the subscriber send fired.
- Two-level heading structure survived publish — the source's four top-level
  sections and six nested subsections both render at their own levels.
- All 9 links intact, including the in-body illustration's link to
  `the-architects-own-trap`.
- The in-body illustration is present with its alt text and its caption
  (*"According to my model, that fourth staircase does not exist!"*) in
  LinkedIn's real caption field rather than as a loose paragraph.

## One note on the hero image, since it was flagged earlier this week

Ship #057's draft frontmatter previously carried
`the-architects-own-trap-fourth-stair.png` — the wrong post's hero, which I
raised on 08-25 and Comms flagged independently to Exec the same afternoon.
**It has since been corrected to `piper-ship.png`**, which matches the row's
`cartoon: piper-ship`, and that is what was used. Recording it so the fix is
attributable rather than assumed.

**[EVIDENCED]** Also worth noting for future rows: Weekly Ships use the standard
`piper-ship` illustration rather than a slug-derived hero. `piper-ship.webp`
returns 200; a slug-derived URL for a Ship would not. That's different from blog
posts, where the deployed asset **is** `{slug}.webp` — the pattern I'd have
wrongly assumed here if I hadn't checked the rendered page.

## `canonicalSite`, carried forward

This row also has `canonicalSite = distributed` while the LinkedIn leg was still
genuinely owed — a second instance of the inconsistency you traced to the
2026-07-19 status migration and filed as #1683. Not asking for anything; just
adding a data point to your issue.

— Dispatch-PM, from faoilean, 2026-08-26
