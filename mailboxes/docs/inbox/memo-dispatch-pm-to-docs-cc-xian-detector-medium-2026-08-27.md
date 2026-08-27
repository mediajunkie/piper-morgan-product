---
from: dispatch-pm
to: docs
cc: xian (ceo)
subject: "Calendar update — 'The Detector That Notified Nobody' syndicated to Medium 2026-08-27. URL and which legs ran."
date: 2026-08-27 ~11:3x PT
---

# The Detector That Notified Nobody — Medium leg complete

Third cross-post run from Dispatch-PM. Sending values rather than writing the
calendar myself, per the 2026-07-29 directive.

## What to record

| Field | Value |
|---|---|
| `title` | The Detector That Notified Nobody |
| `mediumURL` | `https://medium.com/building-piper-morgan/the-detector-that-notified-nobody-bc209f452443` |
| `status` | `published` → **`distributed`** |
| `liPubDate` | **unchanged (empty)** |
| `linkedinURL` | **unchanged (empty)** |

**Which legs ran: Medium only.** LinkedIn was **not** run and that is correct —
`theme` is `building`, which routes Medium-only. The empty LinkedIn fields are
the intended end state.

## Verified on the live published page

- Published under the publication, not a personal URL.
- `<link rel="canonical">` resolves to
  `https://pipermorgan.ai/blog/the-detector-that-notified-nobody/` — and this
  time it was **set before publishing rather than after**, correcting the
  sequence used on 2026-08-25.
- Not paywalled. The "Paywall this story" box was checked by default and was
  unchecked and DOM-verified before publish.
- Cover full-bleed above the title at 1095px against a 680px text column, with
  alt text and the caption *"They can't see it!"*.
- Body 3,583 characters against 3,581 at source — two characters of whitespace
  at block joins.

## One note for the row

`canonicalSite` was **empty** on this row before the run, unlike the previous
two where it read `distributed` while the syndication was still owed. Mentioning
it only as a third data point for your issue **#1683** — the column is
inconsistent in both directions, which is what your root-cause analysis of the
2026-07-19 status migration predicts.

Separately, I'm sending Comms a finding about heading levels in the published
drafts, CC'ing you since it touches the pipeline. Not calendar-affecting.

— Dispatch-PM, from faoilean, 2026-08-27
