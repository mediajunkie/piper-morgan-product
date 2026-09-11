---
from: docs
to: xian (ceo)
date: 2026-08-20
subject: The "third instance" wasn't spreading — it's structural, and it's already fixed at the source
---

# The "third instance" wasn't spreading — it's structural, and it's already fixed at the source

Your Medium cross-post session flagged what looked like a third case of yesterday's hero-image
404 bug on "The Dead Code That Wasn't." I checked directly rather than assume the pattern: that
post has **zero images embedded in its own content** — the frontmatter `.png` filename never
appears anywhere in its live rendering. It was never actually broken.

The session that flagged it also measured the whole corpus before reporting back, and found the
real shape: **81 of 81** published posts' frontmatter `image:` field is a pre-conversion source
filename that has never matched a deployed asset — by design, not by drift. It's what
`publish-post.js` consumes to *produce* the real `{slug}.webp` file; it was never meant to be a
public URL. So "third instance" was the wrong frame — the two real breakages (Ship #054, Ship
#056) weren't three separate bugs creeping across the corpus, they were the one place the
convention got misused: a Ship's hand-built hero-teaser section, which an instruction in the
`draft-weekly-ship` skill told to pull the image URL "verbatim from frontmatter."

**Fixed at that source** (`b4838696d`): the skill now says to derive the image URL from the
post's own slug, never from frontmatter, with a live-HTTP-verify step before shipping a draft.
Alt text and caption still pull verbatim from frontmatter — those render as-is and were never the
problem. Also updated `piper-morgan-website#33` with the corrected diagnosis so the eventual
mechanical guard gets built against the right shape, not an 81-file "fix the frontmatter" chase
that would have broken the field's actual job.

Medium syndication for "The Dead Code That Wasn't" is recorded (status→distributed). Nothing
outstanding on either thread.

— Docs
