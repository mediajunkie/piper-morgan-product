---
from: Web (Unicorn Web Designer)
to: xian (PM/CEO)
cc: exec, pard
date: 2026-09-20
subject: "Correction to last night's Vercel memo — I cited website#37 wrongly. Recommendation unchanged, evidence now actually checked."
in-reply-to: finding-web-to-pm-cc-exec-pard-vercel-at-100pct-is-74pct-build-tool-inputs-served-publicly-2026-09-19.md
---

Short, and before you decide anything on it.

**What I got wrong.** Last night I justified *move, not delete* with: *"website#37 ('publish should
archive the source image') says we want the archive; it just doesn't need to be served."*

**#37 is a different repo and a different directory.** It's about the *product* repo's
`docs/public/comms/drafts/` staging area and moving a draft's source image to `drafts/published/`
at publish time. It says nothing about the website repo's `public/assets/blog-images/source/`
tree — the 240 MB in question. It's also **closed and complete since 09-12**, not a live intent.

I took it from a one-line summary in my own carry-forward rather than opening the issue. Citing a
fragment, which is the thing I'd been catching all day in other people's checks and then did here.

**What's actually true, now measured.** I checked what that citation was standing in for — whether
these originals exist anywhere else:

| | distinct basenames |
|---|---|
| website `public/assets/blog-images/source/` | 172 |
| product `drafts/{published,images-archive}/` | 202 |
| **overlap** | **0** |

Full comparison, not a sample. **Those 172 files are the only copies in git.** So *move, not
delete* holds — and for a better reason than I gave: deleting would destroy the sole original.

**Your own words are the right precedent, and they're a closer fit than what I claimed.** From #37,
on the analogous product-repo case:

> *"Move it to an ignored staging dir — safer, keeps the original, still gets it out of the git
> surface."*

Different directory, so it's a precedent rather than a ruling — but "ignored staging dir, keeps the
original, off the git surface" is exactly the proposal.

**Nothing else changes.** The 240.7 MB / 74%-of-payload measurement, the "served publicly and needed
by nothing at build or publish time" finding, and the dedup caveat all stand as sent — those I did
check. **Still held for your word, either order**, per Exec's sequencing.

**Verified how**: `gh issue view 37` read in full, body and both closing comments, this morning;
overlap computed across all extensionless basenames under each tree via `git ls-tree -r origin/main`
in both repos. Correction also posted on website#43 itself, so it lands at the claim rather than
only in mail. **Not verified**: whether originals exist outside git (your local disk, cloud) — can't
see that, and it's another reason to prefer move over delete.

— Web
