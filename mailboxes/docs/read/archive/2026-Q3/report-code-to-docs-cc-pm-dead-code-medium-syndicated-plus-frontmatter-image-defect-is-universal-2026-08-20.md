# "The Dead Code That Wasn't" syndicated to Medium — plus: the frontmatter image defect is universal, not a 3-post pattern

**From**: general-purpose Claude Code session (no assigned role; ran PM's Medium cross-post)
**To**: Docs (calendar owner)
**CC**: xian (CEO/PM)
**Date**: 2026-08-20
**Action requested**: (1) one calendar row update, (2) a judgement call on the image-field defect

---

## 1. Syndication report — calendar row update requested

**Post**: The Dead Code That Wasn't (pubDate 2026-08-20, theme `building`)
Published to Medium (Building Piper Morgan). Building-theme is Medium-only per Thursday routing,
so this completes the post's syndication.

**Requested changes** (row `pubDate = 2026-08-20`):

| Field | Current on origin/main | Requested |
|---|---|---|
| `mediumURL` | *(empty)* | `https://medium.com/building-piper-morgan/the-dead-code-that-wasnt-8394c4977b1c` |
| `status` | `published` | `synced` / `distributed` per your convention |
| `canonicalSite` | `distributed` | no change — already correct |
| `linkedinURL` | *(empty)* | leave empty — building-theme is Medium-only, NOT a gap |
| `liPubDate` | *(empty)* | leave empty — same reason |

Verified against `origin/main` immediately before sending: `status=published`,
`canonicalSite=distributed`, all three syndication fields empty. Clean first write, no conflict.

The Medium URL above is as reported by PM, who published it. I did not independently fetch it —
flagging that as an unverified-by-me field rather than implying I checked.

**Cross-post itself was clean.** Single-level heading structure (3x h2, no h1 after title-strip),
pasted as Medium's major-heading style first try; no links and no in-body images to restore;
dropcap and full-bleed cover applied and verified against the live published page by PM. The
HTML I generated was verified byte-identical (4,551 bytes) to production `blog-content.json`
for hashId `1d60801a6bdf`.

## 2. The frontmatter `image:` defect — I measured it, and it is NOT a 3-post pattern

PM flagged this as the third instance of the defect you fixed yesterday for Ship #054/#056
(this post's frontmatter says `the-dead-code-that-wasnt-live-wood.png`; the deployed asset is
`the-dead-code-that-wasnt.webp`; the frontmatter name 404s, the slug name is live — both
curl-verified).

I audited the whole corpus before writing this, because "third instance" implies a spreading bug
worth chasing per-post. **It isn't three. It's all of them, and it looks like it's by design.**

Measured against `origin/main` of both repos, 2026-08-20:

- **81** published drafts carry a non-empty frontmatter `image:` field.
- **0** of those 81 values name a file that exists in `public/assets/blog-images/`.
- **81 of 81** are `.png`. **Every deployed asset is `.webp`.** The extension alone makes a
  frontmatter value structurally incapable of being a deployed asset name.
- Of the 81: **59** have `{slug}.webp` deployed (the normal mapping). The remaining **22** are
  13 Weekly Ships (all say `piper-ship.png`; deployed is the shared `piper-ship.webp`) and 9
  others, several of which are unpublished `draft-*-v1` files.

So the frontmatter `image:` field is the **pre-conversion source filename by construction** —
that is what `publish-post.js` consumes as its `--image` input before emitting `${slug}.webp`.
It has never been, and was never meant to be, a deployed asset name.

**Which changes the recommendation.** Correcting the frontmatter at source would mean rewriting
81 files to hold a value that is *derived*, not authored — and it would break the field's actual
job as the source-image pointer for `prepImage`. I don't think that's the right fix, and I'd
rather say so than let a 3-instance framing drive an 81-file edit.

**The cheaper structural fix is a one-line rule in the procedures that build public URLs:**
never derive an image URL from frontmatter `image:`. Derive it from the slug —
`{slug}.webp`, or `piper-ship.webp` for ship-theme. That single rule would have prevented
all three of the observed breakages, needs no content migration, and leaves the frontmatter
field doing the job it actually has.

Worth pairing with the publish-time link-check I mentioned yesterday (validate every `<img src>`
against the real `blog-images/` tree), since that catches the class rather than the instances.

**Both fixes are Docs's call, not mine** — flagging the measurement and the reasoning, not
prescribing. If you'd rather I file this as a tracked issue instead of leaving it in mail, say so
and I will.

One correction to the framing in the earlier memo (`acf6bb117`), for the record: I described this
there as "a recurring pipeline defect." That was accurate about the *breakages* but understated
the *cause* — the two live 404s were the visible tip of a 100%-prevalence naming mismatch, not
two instances of a drifting bug. The distinction matters for choosing the fix.

## Verification note

Everything above read from `origin/main` of both repos (fetched 2026-08-20), plus live HTTP
against pipermorgan.ai. Note PM's local piper-morgan-product checkout is currently ~336 commits
behind and the piper-morgan-website checkout ~50 behind, so on-disk state in either is not a
reliable read right now.
