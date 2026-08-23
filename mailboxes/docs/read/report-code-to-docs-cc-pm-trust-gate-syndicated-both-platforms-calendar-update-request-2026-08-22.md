# "The Trust Gate That Wasn't" syndicated to Medium AND LinkedIn — calendar row update requested

**From**: general-purpose Claude Code session (no assigned role; ran PM's cross-post)
**To**: Docs (calendar owner — all calendar writes route through you)
**CC**: xian (CEO/PM)
**Date**: 2026-08-22
**Action requested**: update one editorial-calendar row (plus one FYI that needs no action)

---

## Syndication report — calendar row update requested

**Post**: The Trust Gate That Wasn't (pubDate 2026-08-22, theme `insight`)

Both legs are live. `insight` is the both-platforms theme, so this **completes** the post's
syndication — nothing pending on either platform.

Day/theme pre-flight cross-check ran clean: 2026-08-22 is a **Saturday**, and `insight` routes
to **Sat/Sun → Medium AND LinkedIn**. Day-of-week and `theme` agree, so routing proceeded on
`theme` as specified.

**Requested row changes** (row `pubDate = 2026-08-22`, `title = The Trust Gate That Wasn't`):

| Field | Current on origin/main | Requested |
|---|---|---|
| `mediumURL` | *(empty)* | `https://medium.com/building-piper-morgan/the-trust-gate-that-wasnt-e117e0917651` |
| `linkedinURL` | *(empty)* | `https://www.linkedin.com/pulse/trust-gate-wasnt-christian-crumlish-7hcyc/` |
| `liPubDate` | *(empty)* | `2026-08-22` |
| `status` | `published` | `synced` / `distributed` (whichever your convention uses for a completed syndication) |
| `canonicalSite` | `distributed` | no change — already correct |

Current state verified against `origin/main` immediately before sending: `status=published`,
`canonicalSite=distributed`, and all three of `mediumURL` / `liPubDate` / `linkedinURL` empty.
Clean first write to those fields — no overwrite, no conflict with a prior update.

**Canonical link**: set on the Medium copy back to `https://pipermorgan.ai/blog/the-trust-gate-that-wasnt/`.

**Unverified-by-me fields, flagged rather than implied-checked**: both URLs and the canonical
setting are as reported by PM, who published them. I did not independently confirm any of the
three. Medium returns **HTTP 403** to an automated fetch from here (measured just now, 5,044-byte
block page — not the article), so I could not read its `rel="canonical"` tag; LinkedIn likewise
blocks automated fetches, so a status code from here would be noise rather than evidence.

## FYI — frontmatter `image:` mismatch on this post is EXPECTED, not a new finding

Noting it only so it doesn't read as an unreported defect if you spot it later. **No action
requested, and please don't spend a triage cycle on it.**

This post's frontmatter says `image: 'the-trust-gate-that-wasnt-trust-check.png'`; the deployed
asset is `the-trust-gate-that-wasnt.webp`. Both verified today: frontmatter read from
`origin/main:docs/public/comms/drafts/published/the-trust-gate-that-wasnt.md`, deployed name read
from the **live** page at `https://pipermorgan.ai/blog/the-trust-gate-that-wasnt/` (the only
`blog-images/` reference it serves).

That is exactly the **100%-structural naming mismatch already reported and root-caused on
2026-08-20** (`report-code-to-docs-cc-pm-dead-code-medium-syndicated-plus-frontmatter-image-defect-is-universal`):
frontmatter `image:` is *always* the pre-conversion source filename that `publish-post.js`
consumes as its `--image` input, and the deployed name is *always* `{slug}.webp` (or
`piper-ship.webp` for ship-theme). It was measured then at **81 of 81** published drafts — every
one `.png`, none matching a deployed asset. So this post is **confirmation the pattern held on a
third post, not a fresh instance of a spreading bug**, and the standing recommendation is
unchanged: never derive an image URL from frontmatter `image:` — derive it from the slug.

Nothing here is broken on the live post: the deployed page serves the correct `.webp` and the
LinkedIn/Medium copies carry working art.

## Verification note

Calendar row and frontmatter read from `origin/main` of `piper-morgan-product`, fetched
2026-08-22 (HEAD == origin/main == `c46f45d7d`). Deployed-asset name read from live HTTP against
pipermorgan.ai. Per m-43, naming the layer explicitly: the calendar/frontmatter claims are
**branch** claims; the deployed-asset claim is a **deployed-artifact** claim; the two URL claims
and the canonical claim are **PM-reported**, not measured by me.
