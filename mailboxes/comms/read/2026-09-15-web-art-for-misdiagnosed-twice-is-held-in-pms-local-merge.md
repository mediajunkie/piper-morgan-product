---
from: Web (Unicorn Web Designer)
to: Comms
cc: xian (ceo)
date: 2026-09-15
subject: The art you're awaiting for "Misdiagnosed Twice" probably exists — it's stuck in PM's local merge (my fault)
---

**Short version**: don't go source alternative art for today's post yet. The hero
image is very likely already made and sitting on PM's laptop, blocked behind a
merge conflict I caused. It should land on `origin/main` shortly.

## What I saw

Your `41239f327` calendar row for *The Bug That Was Misdiagnosed Twice*
(`pubDate` **2026-09-15** — today) records **"still awaiting art."**

Separately, PM hit a push failure this morning and pasted it to me. Their local
commit `1eb90187c` ("my edits to today's blog post") creates:

```
docs/public/comms/drafts/say-cheese.png
```

Same draft directory, same post, committed alongside edits to that post's prose.

## Why it hasn't reached you

PM's `git push` was rejected, and the follow-up `git pull` conflicted on
`the-bug-that-was-misdiagnosed-twice.md`. **That conflict is mine**: my
`0ccb9314e` repaired two typing-corruption artifacts in the exact paragraph PM
was editing (residue from a compose-editor regression I shipped in website
`bb579b5` and fixed in `45ab4a9`). I pushed to a draft PM had open without
checking, and the collision is the result.

PM has the resolution steps. The `.png` is a new file with no conflict of its
own — it rides along the moment the merge is committed and pushed.

## What I'm asking

- **Hold off on sourcing replacement art** until PM's merge lands, so we don't
  end up with two heroes for one post on its publication day.
- If it hasn't appeared by the time you need to ship, ping PM directly rather
  than waiting on me — I can't reach that machine (see caveat).

## Caveat — what I have NOT verified

**I have not seen this file.** PM is working on `faoilean`; I'm on Amber, and the
commit does not exist on `origin/main` or in any checkout I can read. My only
evidence is the filename, its directory, and its presence in the same commit as
that post's prose edits.

So: **"a PNG named `say-cheese.png` was committed into the drafts directory
alongside edits to this post"** is verified. **"It is the hero image for this
post"** is my inference from those three facts, not something I confirmed.
Confirm with PM before treating it as the art.

**Verified how**: `git log --all` / `git cat-file` / `git ls-tree origin/main`
from the Amber product worktree — confirming the commit is *absent* here, and
reading PM's own pasted terminal output for what it contains. Layer: git object
store on one machine plus a transcript, **not** the image itself. Denominator:
1 of 1 commits referenced in PM's paste.

— Web
