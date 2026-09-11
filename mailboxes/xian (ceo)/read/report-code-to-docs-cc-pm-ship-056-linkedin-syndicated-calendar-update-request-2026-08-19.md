# Ship #056 LinkedIn cross-post is live — calendar row update requested

**From**: general-purpose Claude Code session (no assigned role; ran PM's Ship #056 cross-post)
**To**: Docs (calendar owner — all calendar writes route through you)
**CC**: xian (CEO/PM)
**Date**: 2026-08-19
**Action requested**: update one editorial-calendar row

---

## Syndication report

**Post**: Weekly Ship #056: Fundamentals First (pubDate 2026-08-19, theme `ship`)

The LinkedIn cross-post is live. Ship-theme posts are LinkedIn-only per routing rules, so this
completes the post's syndication — there is no Medium leg pending.

**Requested row changes** (row `pubDate = 2026-08-19`):

| Field | Current on origin/main | Requested |
|---|---|---|
| `linkedinURL` | *(empty)* | `https://www.linkedin.com/pulse/weekly-ship-056-fundamentals-first-christian-crumlish-dwwxc/` |
| `liPubDate` | *(empty)* | `2026-08-19` |
| `status` | `published` | `synced` / `distributed` (whichever your convention uses for a completed syndication leg) |
| `canonicalSite` | `distributed` | `distributed` — already correct, no change needed |
| `mediumURL` | *(empty)* | leave empty — ship-theme is LinkedIn-only, this is not a gap |

Current state verified against `origin/main` immediately before sending: `status=published`,
`canonicalSite=distributed`, and all three of `mediumURL` / `liPubDate` / `linkedinURL` empty.
So this is a clean first write to those fields — no overwrite, no conflict with a prior update.

The LinkedIn URL above is as reported by PM, who published it. I did not independently verify it
resolves — LinkedIn blocks automated fetches, so a status code from here would be noise rather
than evidence. Flagging that as an unverified-by-me field rather than implying I checked it.

## Hero-image 404 — CLOSED, no action needed (verified, not assumed)

Reporting this only to close the loop, because the cross-post ran against the broken state and
you may otherwise see a stale reference to it.

During the cross-post I hit the `alpha-launches-before-opening.png` 404 in this post's
"External relations & community" section, and reported the root cause separately (commit
`acf6bb117`) — including that it was a recurring pipeline defect that had also broken Ship #054
since Aug 5.

**You have already fixed both, and the fix is deployed.** Verified just now:

- `blog-content.json` on website `origin/main`: Ship #056 → `alpha-launches.webp`,
  Ship #054 → `reconnects-keystone.webp`. Both correct.
- Live deployed page `https://pipermorgan.ai/shipping-news/weekly-ship-056-fundamentals-first/`
  (following the 308 to the trailing-slash URL) serves `blog-images/alpha-launches.webp` and
  contains **zero** occurrences of `before-opening`.

So the layer that matters — what the deployed page actually points at — is fixed, not just the
repo. Nothing outstanding on your side.

One note for accuracy if it comes up: the bare asset URL
`https://pipermorgan.ai/assets/blog-images/alpha-launches-before-opening.png` still returns 404,
and that is correct and expected — that file never existed and nothing references it any more.
A 404 on that URL is no longer evidence of a problem, and shouldn't be read as the fix having
failed.

For the LinkedIn copy itself I substituted the working asset (`alpha-launches.webp`) at
cross-post time, so the live LinkedIn post carries the correct image.

## Source of the markdown used

The LinkedIn body was generated from
`docs/public/comms/drafts/published/weekly-ship-056-draft-2026-08-15.md` at `origin/main`
(blob `ee49e17a…`), converted with the website repo's own `publish-post.js --dry-run` at
`origin/main`, and verified byte-identical to the production `blog-content.json` entry for
hashId `245f61c02146` — so the LinkedIn text matches the published post exactly, modulo the
image-URL substitution noted above.
