---
from: comms
to: docs
cc: xian (ceo), exec
subject: "PUBLISH-READY: Weekly Ship #058 'What we actually had' — full template-audit clean, PM voice pass + a tightening pass complete, PM approved."
date: 2026-09-02
---

# Weekly Ship #058 — cleared for publication

**Draft**: `docs/public/comms/drafts/weekly-ship-058-draft-2026-08-29.md`
**pubDate**: today, Wed Sep 2 · **theme**: ship · **1,856 words**

PM's voice pass is complete (commit `c23912c94`). Full `template-audit` v1.11 run post-pass, Ship
calibration table applied.

| check | result |
|---|---|
| #2 Title H1 | ✓ |
| #3 dateline `*August 21–27, 2026*` | ✓ |
| #4 section headings | ✓ 0 below `##` |
| #5 placeholders | ✓ 0 |
| #7 reader question | N/A — confirmed against #056/#057 precedent, Ships close with Thanks/prev-link/P.S. instead |
| #8 semicolons | ✓ 0 |
| #9 "load-bearing" · #10 "cohort" | ✓ 0 / 0 |
| #11 agents as "people" | ✓ — only match is a blog-post title ("…That Notified Nobody") |
| #12 AI-writing-tics | ✗→**FIXED** — negation-reveal at the learning-pattern "Why it matters" line ("the failure was never X. It was Y" → stated the affirmative first) |
| #13 word count | 1,856 (Ship norm ~1,630; see note below) |
| #14 acronym sweep | ✓ clean |
| #16 typographic residue | ✗→**FIXED** — double space at the admin-gating line |
| **#1 caption · #6 tease · #15 `#NNN` refs** | **N/A by convention — `theme=ship`** |

⚠️ **On the three N/As plus #7**: they'd read as FAILs measured against a narrative. #7 isn't in the
skill's own calibration table yet — I confirmed it against #056 and #057's actual endings before
marking it N/A rather than assuming. Worth adding to the table; I'll fold it in next skill touch.

## The length note

Draft came in at 1,891 words after voice pass — above every prior Ship (#056 was the previous high at
1,547 published / #055 draft 1,761). PM and I discussed it directly: most of the length is earned (a
real connector-audit finding, a write-promotion safety catch, two substantive working-session
reflections) — this was a genuinely dense week, and PM's been pushing more emphasis on what actually
shipped, which cuts against brevity by design.

But there was real fat, not just density: **the Governance section fully restated the FTUX finding**
(five threads resolved, model produced) that Product & experience already told in complete detail —
same fact twice. Collapsed to a back-reference. Also trimmed a handful of trailing hedge/restatement
clauses that added words without adding information, and fixed a real typo caught on close read ("the
vast number of **fixed** Lead Developer has cranked out" → **fixes**). No claims, numbers, or
attributions changed — this was structural + typo-level only. **1,891 → 1,856.** PM reviewed the result
and confirmed "looks good."

## Ruling on the one thing Exec deliberately left to me

Exec's handoff flagged agent-naming inconsistency — one "**My** Chief Architect" (line 32) against bare
names everywhere else (Lead Developer, Web, Piper Alpha, Chief Innovation Officer, Chief Experience
Officer, and a second bare "Chief Architect" at line 75) — and asked me to rule rather than have it
normalize PM's prose unilaterally.

**Ruling: leave it.** It isn't drift, it's a register PM uses consistently elsewhere in this exact
draft: bare name when reporting what an agent did on its own ("Lead Developer landed…", "Web
root-caused…"), first-person possessive when narrating PM's own direct involvement ("Two of **my own**
conversations…", "**my** hard-won product mottos", "**my** efforts to factor myself out…" — all in the
Governance section). Line 32 is PM personally asking their architect a question, not reporting the
architect's independent action — the "My" is doing the same job there that "my own" does elsewhere.
Not touching it.

## Not blockers

Nothing else flagged. Previous-Ship footer link verified against the live calendar title, exact match.
Workstream order (Engineering & architecture leads, per PM's 08-29 ruling) confirmed correct — this is
the first Ship using it.

— Comms
