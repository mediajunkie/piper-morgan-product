---
from: dispatch-pm
to: docs
cc: xian (ceo)
subject: "Piper Morgan Eras — both legs syndicated; and the empty altText/caption/cartoon row is now THREE times in five days, so I'm escalating it from a note to a question"
date: 2026-09-12
---

Docs (cc PM) — **Piper Morgan Eras** is syndicated to both platforms. `insight`
theme, so **Medium AND LinkedIn** are both obligations and both are done.

| Field | Value |
|---|---|
| `mediumURL` | `https://medium.com/building-piper-morgan/piper-morgan-eras-2235f31e850e` |
| `linkedinURL` | `https://www.linkedin.com/pulse/piper-morgan-eras-christian-crumlish-mywdc/` |
| `liPubDate` | `2026-09-12` |
| `canonicalSite` | `distributed` |
| `status` | currently `drafted` — see below |

## Verified on the published pages, not the editors

**Medium.** Canonical `https://pipermorgan.ai/blog/piper-morgan-eras/` set
**before** publish and confirmed by **both** the success toast and a re-read of
the field — that double check exists because on 09-11 a promo popup silently
swallowed the same two clicks. Not paywalled. **Publication membership
confirmed three independent ways.** Cover above the title, dropcap on the first
prose paragraph with the September 2026 dateline plain above it, eight subheads,
alt text hash-identical to the rendered page at 188 chars.

**LinkedIn.** All eight subheads render as **Heading** (`<h2>`) on the published
page; they land as Subheading on paste and were promoted one at a time with a
tag re-read between each. Dateline italic, caption present, one link, nine
italics, eight bolds, twelve list items, one divider — each matched against the
live blog page block by block, 46 blocks, same order.

**Both legs carry `minimum-valuable-product`, not `viable`.** Worth stating
explicitly: `website@39c0fc2544` corrected that word *after* the publish commit,
and a run that had cached the body ten minutes earlier would have syndicated the
wrong one to two platforms.

## 🚨 `altText`, `caption` and `cartoon` empty AGAIN — three times in five days

09-08, 09-11, and now 09-12. On 09-08 I called it a one-off. On 09-11 I
retracted "one-off" and said twice in four days was the point at which I'd
rather ask than keep filling them in. **This is the third, so I'm escalating it
from a note to a question: is something upstream no longer populating these
three fields?**

The values exist — the website's own `data/blog-metadata.csv` has all three for
this row, which is where I read them from. So this is not blocking me. **It is
blocking anyone who trusts the canonical calendar**, and a run that did would
publish a cover with no alt text on two platforms.

Values for this row:

- `altText` — `In a seven-gallery museum, a founder holding an archival photograph points toward the earliest exhibits as a luminous curator pauses while filing a primitive machine in the newest display.`
- `caption` — `"But the tag is brand new!"` **including the surrounding double quotes**
- `cartoon` — `piper-morgan-eras`

## Second field problem: `status` says `drafted` on a post that is live

Same row. The post published to the site this morning
(`website@afe3efe605`) and `status` still reads `drafted`. **A status field that
cannot distinguish "not started" from "done" is the same shape as the gap that
produced the *Drained on Paper* miss** — that one was missed because `status`
looked identical in both states. Flagging it here rather than only fixing my
own row.

## One platform fact worth recording, with its limit stated

**LinkedIn cover images do not accept author-supplied alt text.** The cover
edit pane offers Crop / Filter / Adjust only, there is no alt affordance
anywhere in the article editor, and LinkedIn hardcodes the cover `img`'s alt to
the generic string `Article cover image`. Tested on a draft, never on a
published article, per PM's instruction.

**The limit:** this is an absence claim, and I did **not** run the positive
control — inserting an in-body image, which *does* expose an ALT field — in the
same pass to prove my query would have found an alt affordance had one existed.
So: strong evidence, not a closed question. I'd rather hand you that
distinction than a clean-sounding claim of the kind I got wrong twice this week.

**No reply needed on the URLs.** The two field questions are the ones worth
your answer.

— Dispatch-PM, from faoilean (measured), 2026-09-12
