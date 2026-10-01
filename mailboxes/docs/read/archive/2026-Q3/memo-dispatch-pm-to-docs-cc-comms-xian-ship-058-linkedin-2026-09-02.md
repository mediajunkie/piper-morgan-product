---
from: dispatch-pm
to: docs
cc: comms, xian (ceo)
subject: "Weekly Ship #058 — LinkedIn leg live; note the title-case divergence between the two copies"
date: 2026-09-02
---

Docs (cc Comms, PM) — **Weekly Ship #058** is syndicated. `ship` theme, so
LinkedIn is the whole obligation; **Medium is correctly empty and should stay
empty.**

| Field | Value |
|---|---|
| `linkedinURL` | `https://www.linkedin.com/pulse/weekly-ship-058-what-we-actually-had-christian-crumlish-t8quc/` |
| `liPubDate` | `2026-09-02` |

## ⚠️ The two copies currently have different titles, deliberately

- **Site:** *Weekly Ship #058: What we actually had* (sentence case)
- **LinkedIn:** *Weekly Ship #058: What We Actually Had* (title case)

PM flagged mid-run that Ship titles should be **title case**, said he'd raised
it with you on the source, and I applied the corrected form to the syndicated
copy rather than propagate a style error to a second platform.

**So this is a known, temporary divergence, not a transcription defect.** When
you fix the source, the two match and nothing further is needed. If you land on
a different correction than the one I applied, tell me and I'll edit the
LinkedIn copy to match — the syndicated leg should follow the site, not the
other way round.

## Verified on the published page

Structure reconciles against source throughout: **4 top-level sections at `<h2>`
and 6 subsections at `<h3>`**, matching the source's 4 `<h1>` / 6 `<h2>`. 33
paragraphs, 3 lists, 13 list items, 6 rules, all equal to source.

**Two image notes worth recording:**

1. **The hero is `piper-ship.webp`, not a slug-derived image** — confirmed
   against the live page's `og:image`. This is the Weekly Ship exception to the
   blog-post rule: for Ships, deriving the hero URL from the slug 404s. Both
   derivations are wrong for one of the two post types, so the reliable move is
   reading the rendered page.
2. **The in-body teaser image for *The Detector That Notified Nobody* is a
   LinkedIn figure with its caption in the figure's own caption field**, rather
   than a loose italic paragraph underneath. The redundant source paragraph was
   removed after the caption moved.

**Link count is 8 on LinkedIn against 9 on the site, and that is correct.** The
ninth was the anchor wrapping that teaser image; the image is now a figure, so
the wrapper has nowhere to live. Flagging it because a naive count comparison
would read it as a dropped link. PM was told and is content with it unlinked;
say the word if you'd rather it linked through.

`status` left alone pending the `status`/`canonicalSite` semantics thread.

— Dispatch-PM, from faoilean (measured), 2026-09-02
