---
from: docs
to: xian (ceo)
date: 2026-08-19
subject: Ship #056 LinkedIn cross-post unblocked — hero image 404 fixed (+ same defect on Ship #054)
---

# Ship #056 LinkedIn cross-post unblocked — hero image 404 fixed (+ same defect on Ship #054)

A general-purpose session working your Ship #056 LinkedIn cross-post flagged a live 404: the
Alpha Launches teaser image embedded in Ship #056 was pointing at a filename that was never
actually deployed (the source draft's pre-conversion name, not the real `${slug}.webp` file
`publish-post.js` produces). It would have rendered as a broken image on LinkedIn.

Independently re-verified their diagnosis (live HTTP + git history — exact match), then fixed:

- **Ship #056**: hero teaser now points at `alpha-launches.webp` (live, 200).
- **Ship #054 "Clear Is Not a Measurement"**: found the identical defect while scanning the whole
  corpus for the same class — it's been a live 404 since it published on 2026-08-05, 14 days
  uncaught. Fixed the same commit, live-verified.

Both live-verified end to end: correct asset returns 200, and the actual served post HTML now
references it (not just the source commit — checked the page itself). Zero remaining non-`.webp`
`blog-images` references anywhere in the corpus after a full scan.

**You're clear to do the LinkedIn cross-post now** — the hero image will render correctly.

Filed `piper-morgan-website#33` for a mechanical guard against this defect class recurring (the
Ship hero-image convention hand-copies another post's frontmatter filename, which is structurally
never the deployed name) — that's a "should we build this" question for whoever owns that repo's
tooling priorities, not urgent.

— Docs
