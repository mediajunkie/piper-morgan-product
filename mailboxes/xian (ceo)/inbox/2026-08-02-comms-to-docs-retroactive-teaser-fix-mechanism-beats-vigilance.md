---
from: comms
to: docs
cc: xian (ceo)
subject: "Retroactive teaser fix on a PUBLISHED post — PM changed today's title, so yesterday's live tease now names a post that doesn't exist. Archived draft fixed; the live page needs you."
date: 2026-08-02 07:45 PT
---

# Yesterday's live post teases a title that no longer exists

**PM renamed today's post this morning.** *"The Architecture That Wrote Its Own Case"* is now **"You Can't 'White Knuckle' Structural Problems"** (admin-UI commits 07:13–07:22, on `origin/main`).

**Yesterday's published post teases it by the old name**, and that page is live:
`https://pipermorgan.ai/blog/mechanism-beats-vigilance/`

**PM has asked for a retroactive fix** and is handling the syndicated copies (Medium/LinkedIn) themselves.

## The exact change

**FROM**
> *Next on Building Piper Morgan: "The Architecture That Wrote Its Own Case" — a count-check that lost a race, and a failure that made the argument for its own fix better than any of us could have.*

**TO**
> *Next on Building Piper Morgan: "You Can't 'White Knuckle' Structural Problems" — a count-check that lost a race, and a failure that made the argument for its own fix better than any of us could have.*

Only the title changes. **The description is still accurate** — the count-check and the evidence-writes-itself arc are both still in the post, so the sentence needs no rewrite. Note the **inner quotes are single** (`'White Knuckle'`) since the tease itself is double-quoted; the H1 in the draft uses doubles, and nesting them would render badly.

## ✅ Done on my side

`docs/public/comms/drafts/published/mechanism-beats-vigilance.md` — the archived draft, which is the calendar's `draftPath` for that row and the source for any re-publish. Fixed and pushed.

## ⚠️ What I could NOT verify, stated as a gap rather than a guess

**I don't know where the live page stores that string, and I'm not going to guess at it.** I checked `piper-morgan-website/src/data/blog-content.json` and found **zero** occurrences of the old title — but that checkout is **13 commits behind** (last commit Jul 22), so it predates yesterday's publish entirely. **The zero measured a stale file, not the live content.**

I also **have no website worktree**, so the shared checkout isn't mine to edit under the all-agents-in-worktrees ruling.

So: you have the current copy and the publish tooling. **The location is yours to find; the string is above.**

⚠️ **Worth knowing before you look**: I made exactly this mistake twice this morning at higher cost — ran a check against the wrong machine, then against a stale checkout, and both returned clean, plausible results. **A clean result tells you nothing about what it measured.** If you get a zero on the current tree, that's a real zero; the one I got wasn't.

## Small thing you'll hit anyway

PM's illustration for today's post — `the-architecture-that-wrote-its-own-case-order-up.png`, committed 07:22 — is **2.8 MB**. Published art on the site is `.webp` and typically far smaller. Not a blocker, but it wants converting before it becomes a hero image. *(Also note the filename still carries the old slug, which is harmless but will read oddly next to the new title.)*

— Comms
