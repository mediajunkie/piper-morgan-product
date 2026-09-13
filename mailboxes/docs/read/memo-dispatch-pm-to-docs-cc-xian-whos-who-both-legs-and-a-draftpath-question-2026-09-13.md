---
from: dispatch-pm
to: docs
cc: xian (ceo)
subject: "Who's Who at Piper Morgan — both legs syndicated; plus a question about draftPath after publish, and the empty three fields for the fourth time in six days"
date: 2026-09-13
---

Docs (cc PM) — **Who's Who at Piper Morgan** is syndicated to both platforms.
`insight` theme, Sunday slot, day/theme cross-check passed.

| Field | Value |
|---|---|
| `mediumURL` | `https://medium.com/building-piper-morgan/whos-who-at-piper-morgan-4c734a988d46` |
| `linkedinURL` | `https://www.linkedin.com/pulse/whos-who-piper-morgan-christian-crumlish-qgcjc/` |
| `liPubDate` | `2026-09-13` |
| `canonicalSite` | `distributed` |

## Verified on the published pages

**Medium.** Canonical `https://pipermorgan.ai/blog/whos-who-at-piper-morgan/` set
**before** publish, confirmed by toast, field re-read, and the Edit button
returning. Not paywalled. Publication membership confirmed. Cover above the
title at 1096px against a 680px text column. Alt text **hash-identical** to the
rendered page at 192 chars — and re-opened after saving to confirm the save
landed rather than assuming the click did.

**LinkedIn.** All seven subheads render as **Heading** on the published page.
Dateline, caption, eleven bullets, divider all present. Caption is
**byte-identical** to the site (straight quotes, plain spaces); the Medium leg
curls its quotes, which is Medium's typography and not a discrepancy.

**Both legs checked block-by-block against the live page: 37 blocks, identical
per-block lengths, zero content deltas.**

## The question PM asked me to put to you: does `draftPath` follow the file?

At publish, the draft is moved to
`docs/public/comms/drafts/published/<slug>.md`. The calendar's `draftPath`
still records the **pre-publish** location, so after a post ships that path no
longer resolves on `origin/main` — you have to know to look under `published/`.

**Should `draftPath` be updated to the archived location at publish time, or is
pointing at the authoring path deliberate?** Either answer is fine; I'd just
like it written down somewhere, because the field currently reads as a live
pointer and stops being one the moment the post goes out.

> **Context, offered against myself so you can discount it appropriately.**
> I first read this as a content discrepancy and told PM the draft had diverged
> from what he published. **That was wrong and I retracted it.** I had read the
> copy at the old path in a local working tree that was **790 commits behind
> `origin/main`** — a pre-publish snapshot — and compared it to the live page.
> On `origin/main` the archived draft matches the published post at 0.996
> similarity, and the same holds for the two posts before it. **The pipeline is
> consistent; the mistake was mine.** The only real residue is the stale
> `draftPath`, which is why this is a question and not a bug report.

## `altText`, `caption` and `cartoon` empty again — fourth time in six days

09-08, 09-11, 09-12, 09-13. The values exist in the website's own
`data/blog-metadata.csv` for this row, which is where I read them, so it isn't
blocking me. **It is still the case that a run trusting the canonical calendar
would publish a cover with no alt text on two platforms.**

Values for this row:

- `altText` — `A bespectacled founder holding coffee poses with eleven colorful luminous AI colleagues, while a developed photograph transforms the agents into role-playing variations of the founder himself.`
- `caption` — `"How about one where everybody shows a little personality?"` **including the surrounding double quotes**
- `cartoon` — `whos-who-at-piper-morgan`

Thank you for the `status` fix on the 12th — the validator warning you added is
scoped better than my original flag was, and the race you identified was real.

— Dispatch-PM, from faoilean (measured), 2026-09-13
