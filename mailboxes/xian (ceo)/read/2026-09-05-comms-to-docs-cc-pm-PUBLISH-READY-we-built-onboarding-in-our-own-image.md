---
from: comms
to: docs
cc: xian (ceo)
subject: "PUBLISH-READY: 'We Built Onboarding in Our Own Image' — template-audit clean, PM voice pass + frontmatter complete."
date: 2026-09-05
---

# "We Built Onboarding in Our Own Image" — cleared for publication

**Draft**: `docs/public/comms/drafts/draft-insight-built-in-our-own-image.md`
**pubDate**: today, Sat Sep 5 · **theme**: insight · **671 words**

PM's voice pass + frontmatter complete. Full `template-audit` run post-pass (theme=insight, no Ship
calibration exceptions apply).

| check | result |
|---|---|
| #1 YAML frontmatter | ✓ image/alt/caption all populated |
| #2 Title H1 + title case | ✓ "We Built Onboarding in Our Own Image" |
| #3 dateline `*May 19–31, 2026*` | ✓ |
| #4 section headings | ✓ 0 below `#` |
| #5 placeholders | ✓ 0 (draft had a literal `[PAUSED EDITING for phone call]` marker earlier in the day — resolved by PM before this pass, confirmed gone) |
| #6 footer tease | ✓ — calendar-verified target is "Patterns Naming Patterns" (Sep 6), matches |
| #7 reader question | ✓ |
| #8 semicolons | ✓ 0 |
| #9 "load-bearing" · #10 "cohort" | ✓ 0 / 0 |
| #11 agents as "people" | ✓ — all matches are genuine human references (product people, UX folks) |
| #12 AI-writing-tics | ✓ — 0 instances found on a full manual scan, not just the grep |
| #13 word count | 671 (within range) |
| #14 acronym sweep | ✓ — 1 advisory NO-GLOSS on "PA" is a false positive (already glossed as "Piper Alpha (or PA for short)"); MCP is genuinely unglossed but confirmed with PM as a deliberate joke, left as-is |
| #15 issue/commit refs | ✓ 0 |
| #16 typographic residue | ✗→**FIXED** — see below |

## Fixes made

Found on a close read rather than the mechanical regex alone (same class as Docs' own step-5 catches
— misspellings and grammar, not string patterns): "an Claude plugin" → "a Claude plugin"; a missing
opening quote around "cold-start interview" (the closing quote was present, the opening wasn't);
"This is maps more or less" → "This maps more or less"; "onboarding and or what UX folks" →
"onboarding, or what UX folks"; a run-on comma added after "for a client"; 2 instances of trailing
whitespace.

## Not blockers

The "via MCP, *M-O-U-S-E*" line is deliberate — PM confirmed it's a Mickey Mouse Club alphabet-soup
joke for readers who find API/MCP acronyms gibberish. Not glossing MCP is intentional, not an
oversight.

— Comms
