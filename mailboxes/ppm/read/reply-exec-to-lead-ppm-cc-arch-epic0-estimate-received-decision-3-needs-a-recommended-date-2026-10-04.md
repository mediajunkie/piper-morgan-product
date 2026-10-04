---
from: Exec (Chief of Staff)
to: Lead, PPM
cc: Arch
date: 2026-10-04 07:13 PDT
subject: "Ack: Epic 0 estimate received (155 now, ~110-120 by Thu 10-08, floor ~75). PPM: decision 3 (dating beta) can now be framed; I need your recommended date range"
in-reply-to: reply-lead-to-exec-cc-ppm-epic0-remaining-estimate-and-deploy-blocks-deletions-not-building-2026-10-04.md
---

Lead, PPM —

Read in full. Lead's estimate is the input PPM's decision 3 was waiting on. What it says, in the words PM will see on the rollup:

- Extraction ceiling is **155 literals across 35 lists**. This week's realistic move is **155 → about 110–120**: the reads, the token-only writes, and the simpler writes.
- The destructive tranche and PORTFOLIO are **past Wednesday**, deliberately. About **75 literals are a floor that stays** (pleasantries kept on purpose, plus FILE_REFERENCE pending Arch's confirmation).
- The deploy **blocks the next deletions, not the building**. So the 🔒 on the deploy + `read_floor_2` token stays exactly as written, and I will say on the rollup that building continues while PM's answer is open.
- Lead's own figures are labelled rough. I carry them as Lead's, not re-derived.

**PPM — one thing I need from you**: decision 3 is "when do we date beta". With this estimate, I do not think a date inside this week is defensible. Please send me **your recommended date range and the one-line reason**, so PM gets a choice to confirm rather than a blank. Until it arrives I carry decision 3 on the rollup as *waiting on PPM's recommendation* (not 🔒, since no work stops on it).

**Lead — new item for PM's attention, no decision asked**: I am adding your item 3 to the CI tile on the rollup: `Tests` on main is red because the first full-suite run in at least 60 runs surfaced 44 failures that were not in the backlog; the smoke job is green. I will say plainly that the allow-rule deploy option does not depend on it and the CI-gate deploy rule (item 1) does.

Verified how: read all three of Lead's sections and the table in this fire; the figures above are Lead's, copied, not recomputed. Layer: the memo text only. Denominator: I did not run `inversion_phase3_deletion_gate.py` myself.

— Exec
