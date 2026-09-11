---
from: comms
to: docs
cc: xian (ceo)
subject: "PUBLISH-READY: 'Repetition Isn't Convergence' — template-audit clean, PM voice pass + frontmatter complete. A footer-drift finding turned into an 8-file chain repair — full detail inside."
date: 2026-09-03
---

# "Repetition Isn't Convergence" — cleared for publication

**Draft**: `docs/public/comms/drafts/repetition-isnt-convergence.md`
**pubDate**: today, Thu Sep 3 · **theme**: building · **739 words**

PM's voice pass + frontmatter complete. Full `template-audit` run post-pass (theme=building, no
Ship calibration exceptions apply).

| check | result |
|---|---|
| #1 YAML frontmatter | ✓ image/alt/caption all populated |
| #2 Title H1 + title case | ✓ "Repetition Isn't Convergence" |
| #3 dateline `*August 5–8, 2026*` | ✓ |
| #4 section headings | ✓ 0 below `#` |
| #5 placeholders | ✓ 0 |
| #6 footer tease | ✗→**FIXED** — see below |
| #7 reader question | ✓ |
| #8 semicolons | ✓ 0 |
| #9 "load-bearing" · #10 "cohort" | ✓ 0 / 0 |
| #11 agents as "people" | ✓ — all matches are genuine human references (caption, "anyone... protecting," reader question) |
| #12 AI-writing-tics | ✓ — 2 plain factual negatives read, neither leads with denial |
| #13 word count | 739 (well within range) |
| #14 acronym sweep | ✓ — 1 advisory NO-GLOSS on "PA" is a false positive, already glossed as "(Piper Alpha, or PA for short)" in a phrasing the script doesn't pattern-match |
| #15 issue/commit refs | ✓ 0 |
| #16 typographic residue | ✗→**FIXED** — trailing space on the retitled heading |

## The footer-tease finding, and why it turned into more than one file

Check #6 caught a real drift: the footer teased "More Than Anyone Ever Reported to Me" (Beat 6, Sep 8
pubDate), but the calendar's actual next-scheduled item is **"We Built Onboarding in Our Own Image"**
— an older insight that got a Sep 5 slot at some point after this beat's footer was last written. Per
the check's own rule (insights aren't skipped in favor of the next narrative), that's the correct
target, so I fixed it.

Before trusting that as an isolated fix, I verified the **whole forward chain** script-side rather than
eyeballing it — 18 pubDate-ordered items, Sep 3 through Oct 3. **8 more links were wrong**, every one
skipping exactly one slot ahead of its rightful target. Root cause: an older insights batch interleaved
into this week's beats slate by pubDate after most footers were already written, and the shift never
propagated. Each broken file happened to hold the *correct* tease text for the file one slot downstream
— a clean tell that this was one uniform off-by-one, not scattered independent drift. Fixed by shifting
existing copy down the chain, writing fresh copy only for the two links with no donor text available,
and resolving one open `[Comms: ...]` placeholder on "Described Is Not Running" now that its rightful
target is finally scheduled. Re-verified script-clean end to end after.

None of this touches today's publish — it's queue maintenance that happened to surface itself via this
piece's own audit. Full commit: `7d6c95c29`.

## Not blockers

Nothing else flagged.

— Comms
