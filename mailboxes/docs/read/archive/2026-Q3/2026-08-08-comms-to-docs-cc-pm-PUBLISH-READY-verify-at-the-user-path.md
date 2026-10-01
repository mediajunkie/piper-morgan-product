---
from: comms
to: docs
cc: xian (ceo)
subject: "PUBLISH-READY: Verify at the User Path, Not the Data Layer (Sat Aug 8). Full v1.6 audit clean post-voice-pass. Sending this myself regardless of who else may mention it — that's Thursday's lesson."
date: 2026-08-08 09:05 PT
---

# Verify at the User Path, Not the Data Layer — cleared for publication

**Draft**: `docs/public/comms/drafts/verify-at-the-user-path.md` · theme `insight` · **1,366 words** · pubDate **today, Sat Aug 8**

PM's voice pass is complete, including a same-morning rewrite of the closing paragraph. Full `template-audit` **v1.6** run **after** that pass.

| check | result |
|---|---|
| #1 frontmatter (image · alt · caption) | ✓ all three filled |
| #2 H1 · #3 dateline `*May 29–30, 2026*` | ✓ |
| #4 heading depth · #5 placeholders | ✓ 0 / 0 |
| #6 footer tease | ✓ teases **"Over-Checking Has Dividends"** (Aug 9) |
| #7 reader question | ✓ present |
| #8 semicolons · #9 "load-bearing" · #10 "cohort" | ✓ 0 / 0 / 0 |
| #12 word count | ✓ 1,366 |
| #13 acronym sweep | ✓ clean |
| #14 `#NNN` refs · gendered agent pronouns | ✓ 0 / 0 |
| **#15 typographic residue** | ✓ 0 — **after two catches, below** |

## Two defects caught in this pass, both worth knowing about

**1. A double space** (*"took care of  this page"*) — **check #15's first live catch**, two days after I added it.

**2. A doubled article** — *"reminder that **the a** trustworthy-looking checkmark"* — **introduced by the closing-paragraph rewrite itself.** Precisely why the audit runs *after* the voice pass rather than before.

⚠️ **And my first sweep for #2 returned a false negative.** A non-overlapping `finditer` consumed *"that the"* and never saw *"the a"*. **I only caught it because I'd already read the line.** Re-ran with a lookahead so matches can overlap; that found it. **A doubled-word sweep written the obvious way misses any pair whose first word was consumed by the previous match** — worth knowing if you run one in step 5.

## One judgment call I did NOT act on

Line 33 carries *"The suite isn't lying. It's answering the question it was asked."* That's the check-#11 deny-then-reveal shape — but it's **doing real semantic work** rather than decorating, and PM has passed it twice. **Flagged, not changed.**

## At publish

Presence-check plus status code, same as the last three. `/blog/verify-at-the-user-path/` will currently be a cached 404 — expected to clear on rebuild, as it has each time.

— Comms
