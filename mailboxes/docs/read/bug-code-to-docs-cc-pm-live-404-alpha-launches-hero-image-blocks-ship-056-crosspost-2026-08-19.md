# Live 404: Ship #056 hero image — blocks LinkedIn cross-post

**From**: general-purpose Claude Code session (no assigned role; working PM's Ship #056 LinkedIn cross-post)
**To**: Docs
**CC**: xian (CEO/PM)
**Date**: 2026-08-19
**Priority**: Blocking — PM's Ship #056 cross-post is held on this

---

## The defect

`https://pipermorgan.ai/assets/blog-images/alpha-launches-before-opening.png` returns **404**.

Verified live 2026-08-19:

```
404 text/html   <-  .../alpha-launches-before-opening.png
200 image/webp  <-  .../alpha-launches.webp
```

**Where it's referenced**: Weekly Ship #056 "Fundamentals First"
(https://pipermorgan.ai/shipping-news/weekly-ship-056-fundamentals-first), in the
**"External relations & community"** section — the Alpha Launches teaser image, wrapped in a
link to /blog/alpha-launches/. It renders 0x0 on the live page.

**Impact**: blocking the LinkedIn cross-post of Ship #056. LinkedIn fetches referenced images
at paste/publish time; a 404 hero either drops silently or posts broken.

## Root cause (investigated, not guessed)

The referenced filename is the **pre-conversion source image name**, which is never deployed.

- `publish-post.js` converts the source image to WEBP named `${slug}.webp`. For the Alpha
  Launches post that is `alpha-launches.webp` — committed once, in `b32cb9cfb`
  ("content(alpha-launches): publish Beat 22"), and live (HTTP 200).
- `alpha-launches-before-opening.png` was **never committed to the website repo, at any path,
  in the entire history**. Confirmed via `git log --all --diff-filter=ADR -- '*alpha-launches*'`
  (one result only: `alpha-launches.webp`).
- The string `before-opening` appears in the website repo in **exactly one commit** — `a44abc424`,
  the Ship #056 publish itself. The reference was introduced by that publish; the file never existed.
- Where the wrong name came from: the Alpha Launches draft frontmatter
  (`docs/public/comms/drafts/published/alpha-launches.md`) carries
  `image: 'alpha-launches-before-opening.png'`, and the editorial-calendar row for Alpha Launches
  has `cartoon = alpha-launches-before-opening`. The Ship #056 drafting notes say the hero was
  taken "frontmatter verbatim" — so the source-image name was copied straight into a public URL
  without being mapped through the `${slug}.webp` conversion the publish pipeline actually performs.

**Suggested fix**: point the reference at `https://pipermorgan.ai/assets/blog-images/alpha-launches.webp`
(verified 200, 95,440 bytes, image/webp). The alt text and caption already in the post are correct
and need no change. That is a `blog-content.json` edit for hashId `245f61c02146` — the
`--mode=edit-pass` path, not a republish.

## This is a recurring defect, not a one-off

A scan of all posts in `blog-content.json` for `blog-images` references not ending in `.webp`
returned **two** hits — both Weekly Ships, both 404:

| Post | Referenced (404) | Actually deployed |
|---|---|---|
| Weekly Ship #054 "Clear Is Not a Measurement" | `reconnects-keystone-keystone-arch.png` | `reconnects-keystone.webp` |
| Weekly Ship #056 "Fundamentals First" | `alpha-launches-before-opening.png` | `alpha-launches.webp` |

**Ship #054 has been broken on the live site since it published (Aug 5) and nobody caught it.**
Same shape: source-image name copied verbatim into a public URL instead of the deployed
`${slug}.webp` name.

Worth considering a mechanical guard, since prose discipline has now missed this twice: the Ship
hero block is built by hand from another post's frontmatter, and the frontmatter name is
systematically *not* the deployed name. A link-check of `<img src>` against the actual
`public/assets/blog-images/` tree at publish time would catch the whole class. Filing that is
Docs's call, not mine — flagging the pattern.

## Verification method

Everything above was checked against `origin/main` of both repos (fetched 2026-08-19), plus live
HTTP against pipermorgan.ai. Nothing was inferred from a local checkout — note that PM's
piper-morgan-product checkout is currently 180 commits behind and the piper-morgan-website
checkout is 48 behind, so on-disk state in either is not a reliable read right now.

To re-verify after the fix:

```
curl -s -o /dev/null -w "%{http_code} %{content_type}\n" \
  https://pipermorgan.ai/assets/blog-images/alpha-launches.webp
```

Expect `200 image/webp`. Then confirm the live Ship #056 page renders the teaser at non-zero size —
a 200 on the asset alone is not proof the post references it (that's the layer distinction: asset
availability vs. what the page actually points at).
