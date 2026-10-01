# "Read the Mock First" syndicated to Medium AND LinkedIn — calendar row update requested

**From**: general-purpose Claude Code session (no assigned role; ran PM's cross-post)
**To**: Docs (calendar owner — all calendar writes route through you)
**CC**: xian (CEO/PM)
**Date**: 2026-08-23
**Action requested**: update one editorial-calendar row

---

## Syndication report — calendar row update requested

**Post**: Read the Mock First (pubDate 2026-08-23, theme `insight`, hashId `d7768541669e`)

Both legs are live. `insight` is the both-platforms theme, so this **completes** the post's
syndication — nothing pending on either platform.

Day/theme pre-flight cross-check ran clean: 2026-08-23 is a **Sunday**, and `insight` routes
to **Sat/Sun → Medium AND LinkedIn**. Day-of-week and `theme` agree, so routing proceeded on
`theme` as specified.

**Requested row changes** (row `hashId = d7768541669e`, `title = Read the Mock First`,
`pubDate = 2026-08-23`, `draftPath = docs/public/comms/drafts/published/read-the-mock-first.md`):

| Field | Current on origin/main | Requested |
|---|---|---|
| `mediumURL` | *(empty)* | `https://medium.com/building-piper-morgan/read-the-mock-first-7305ea8ce73b` |
| `linkedinURL` | *(empty)* | `https://www.linkedin.com/pulse/read-mock-first-christian-crumlish-ibvtc/` |
| `liPubDate` | *(empty)* | `2026-08-23` |
| `status` | `published` | `distributed` (the value you applied for the last dual-platform completion, The Trust Gate That Wasn't) |
| `canonicalSite` | `distributed` | no change — already correct |

Current state verified against `origin/main` immediately before sending (HEAD of origin/main =
`f0d014eb0`, row at line 402 of `docs/internal/planning/comms/editorial-calendar.csv`):
`status=published`, `canonicalSite=distributed`, `blogURL=https://pipermorgan.ai/blog/read-the-mock-first/`,
and all three of `mediumURL` / `liPubDate` / `linkedinURL` empty. Clean first write to those
fields — no overwrite, no conflict with a prior update. `draftPath` on the row already reads
`docs/public/comms/drafts/published/read-the-mock-first.md` and that file exists on `origin/main`
(verified by `git cat-file -e`) — no change requested there either.

**Unverified-by-me fields, flagged rather than implied-checked**: both URLs are as reported by PM,
who published them. I did not independently confirm either, and I did not check the canonical link
on the Medium copy. Medium and LinkedIn both block automated fetches from here, so a status code
from this session would be noise rather than evidence.

## FYI — frontmatter `image:` mismatch, if you notice it, is EXPECTED

No action requested. This post's frontmatter reads
`image: 'read-the-mock-first-chatgpt-image-aug-23-2026-at-09-52-02-am.png'` (read from
`origin/main:docs/public/comms/drafts/published/read-the-mock-first.md`), which will not match the
deployed asset name. That is the same 100%-structural naming pattern reported and root-caused on
2026-08-20 (measured 81 of 81 published drafts): frontmatter `image:` is the pre-conversion source
filename `publish-post.js` consumes as `--image`, and the deployed name is `{slug}.webp`. **I did
not check the live page for this post** — I am flagging the expected pattern, not reporting a
measured instance.

## Verification note

Per m-43, naming the layer explicitly: the calendar row, the `draftPath` existence check, and the
frontmatter read are all **branch** claims against `origin/main` (`f0d014eb0`), fetched
2026-08-23. The two syndication URLs are **PM-reported**, not measured by me. No **deployed-artifact**
claim is made anywhere in this memo.
