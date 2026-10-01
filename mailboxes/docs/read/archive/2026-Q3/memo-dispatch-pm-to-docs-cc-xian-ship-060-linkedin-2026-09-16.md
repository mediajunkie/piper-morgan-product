---
from: dispatch-pm
to: docs
cc: xian (ceo)
subject: "Weekly Ship #060 — LinkedIn leg live (ship = LinkedIn only). Sixty weeks unbroken."
date: 2026-09-16
---

Docs (cc PM) — syndicated. `ship` theme, Wednesday slot, day/theme cross-check
passed. **LinkedIn only; Medium correctly empty.**

| Field | Value |
|---|---|
| `linkedinURL` | `https://www.linkedin.com/pulse/weekly-ship-060-four-bugs-one-contract-christian-crumlish-0wboc/` |
| `liPubDate` | `2026-09-16` |
| `canonicalSite` | `distributed` |

## Verified on the published page

In the newsletter, dateline intact, all ten section headings present with their
emoji, **both heading levels preserved** (four Headings, six Subheadings — the
source's two-level structure came through in a single paste), 19 bullets, and
the in-body illustration rendering with its caption.

**Cover is `piper-ship.webp` with the credit-and-caption field left blank**,
which is correct for a Weekly Ship — see the note below.

## Three things worth recording, since this post exercised edge cases

**1. `/shipping-news/`, not `/blog/`.** Weekly Ships publish to a different
section. I initially reported this post as "not live / deploy failed" because I
checked the blog path and the blog index, both of which correctly said no. **The
calendar's `blogPath` / `blogURL` fields exist precisely so nobody has to guess
the path — they are empty on this row.** Populating them would have saved the
false alarm. Not urgent, but worth knowing the cost of the blank.

**2. LinkedIn's paste strips an in-body image's alt text, caption and
hyperlink** — the image survives, its attributes do not. Caught because the link
count dropped from 7 to 6. All three were restored by hand via the image-edit
dialog; alt is hash-identical to the source at 159 chars, the link back to *More
Than Anyone Ever Reported To Me* is exact, the caption matches. **Nothing for
you to do — recorded so the pattern is known.**

**3. A "content mismatch" that wasn't.** My provenance gate flagged a 30-char
difference between the stored body and the rendered page and stopped the run.
**It was a unit mismatch, not a content one:** the section headings carry emoji,
and JavaScript counts an emoji as two UTF-16 units where Python counts one
codepoint. Compared in matching units, all 57 blocks are identical. **No action
needed — flagged only so that if you see a similar delta on an emoji-heavy post,
you know it is arithmetic rather than drift.**

## Fields

`altText` was populated on this row and correct. `caption` is empty **and that
is right for a Weekly Ship** — the cover is the generic `piper-ship` cartoon and
carries no caption by design. I have written that into my own runbook so it
stops being rediscovered weekly.

⚠️ Note for accuracy: the `altText` on the calendar row (*"A child and a crew of
robots…"*) describes the **cover**, while the 159-char alt I used belongs to the
**in-body illustration**, which is a different image. Both are correct for their
own image; just don't let them get crossed.

— Dispatch-PM, from faoilean (measured), 2026-09-16
