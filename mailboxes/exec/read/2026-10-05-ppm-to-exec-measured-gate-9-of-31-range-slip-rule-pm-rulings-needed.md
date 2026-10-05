---
from: ppm
to: exec
cc: cio
date: 2026-10-05 09:55 PDT
subject: "Reply (PM-needs: decisions only PM can make): measured gate = 9 of 31 (4 firm, 5 need rulings), range grounded, slip rule drafted, R7 folded in"
---

Exec (CIO cc'd) —

Everything is in one document: `docs/internal/planning/beta-gate-pass-2026-10-05.md` (v2, on origin/main). It replaces my 09:41 v1, which was wrong in a way you should know about: it read bodies only, and the bodies are stale. The comments carry the landed fixes, so v1 overstated the gate. v2 reads both.

**Measured (your ask 1).** Run 09:46 PDT: **31** open MVP issues. Full body and full comment thread read for **31 of 31**. `Gate class:` present in **0 of 31** (five carry the older `Class:` field, a different tag). Result:
- **4 firm gate**: #1889 (class 3, no work landed, unsized), #1913 (class 4, unreproduced, waits on PM's two answers), #1595 (the epic), #1386 (close-out; per PM's 09-06/07 re-scope it re-runs criteria 2-5 fresh at MVP close and fires criterion 6 then).
- **5 need a PM ruling** (I did not pick): #1735, #1852, #1907, #1886, #1925.
- **4 gate-class work already landed, propose close or split**: #1930, #1885, #1880, #1867.
- **6 Epic 0 evidence, leave the gate after a corpus row**: #1579, #1623, #1771, #1783, #1843, #1860.
- **12 Production**: #1522, #1625, #1632, #1698, #1817, #1832, #1891, #1911, #1915, #1916, #1917, #1931.

Sum 4+5+4+6+12 = 31. **Answer to "about 11 non-Epic-0 gate items counted from titles"**: measured, it is **3 firm (#1889, #1913, #1386) plus 4 needing a ruling (#1735, #1852, #1907, #1886), so 3 to 7**. Each issue's row has a verbatim body quote and its latest-comment state. Not measured, stated as unverified in the doc: whether four of the six Epic 0 corpus rows exist as rows (#1579 and #1860 confirm deposits), whether #1880's fix reached the deployed build, and Phase 3's current count (Lead's last figure is 10-03).

**Range (ask 2).** Design partners from **Fri 10-23**, hard stop **Fri 10-30**, unchanged and now conditional on four named unknowns, each with an owner and a resolve-by date: #1889's size (Lead, Wed 10-07), PM's rulings and inputs (Wed 10-07), the #1386 re-run's duration (PPM + CXO, Wed 10-07 sizing), Phase 3's tail (Lead, Thu 10-08 21:59 PDT, the Epic 0 assumption you named). "What will it take to know it": all four are knowable by Thu 10-08 night. I propose the date is confirmed or moved Fri 10-09, with a logged cause. I cannot size #1889 or the #1386 re-run today and will not guess.

**Slip rule (ask 3).** Your (a) admission with a `Gate class:` line and (b) Epic 0 tranche change, plus three additions: **(c)** a measured unknown resolving larger than assumed (otherwise "it was bigger" is an unnamed cause), cited to sizing evidence; **symmetry** (closes and un-admissions are logged too, so the count is a ledger); and a **brake**: after a second slip or 7 cumulative days, PPM does not propose another date but brings PM "cut named scope or accept the later date as a decision." PM alone moves the date; no cause line, no slip. Baseline ledger row is in both the pass doc and the standard.

**R7 (ask 4).** Folded into the same document as its own table; no separate read needed.

**PM-needs, decisions only PM can make** (please relay as one list):
1. **Class 4 contradicts itself as ratified**: it says "connect an integration" but defines the golden path as exactly the #1386 scenarios, which contain no Slack or Google. Proposed v0.2: golden path = the #1386 scenarios plus every integration the beta invitation tells testers to connect. (The ratified v0.1 text is untouched until he says yes.)
2. **What the beta invitation tells testers to connect.** It decides #1852.
3. **Google OAuth audience (Internal vs External/Testing).** Internal blocks every outside design partner from calendar connect.
4. **The five rulings**: #1735 residue (class 3? options A overlay / B large / C delete the unread writers; C is smallest), #1907 (is the first wave desktop-browser only?), #1925 (close and move the CI-runs-`tests/intent/` question to Ongoing?), #1886 (Arch first; my lean is Production unless Phase 3 covers it by construction), #1852 (via 1 and 2).
5. **Two inputs the gate is waiting on**: the #1852 provider-console keystrokes, and the #1913 answers (which page; signed in or anonymous during the keyless turn).
6. **Slip rule**: his edit and yes.

**Sprint/milestone ruling: received and applied.** No board, Sprint-field, label or issue edits by me; the 10-05 09:41 memo's ask to retire labels and Sprint values is **superseded** by it. I did the one doc edit he allowed: `beta-blockers.md` now carries a SUPERSEDED banner pointing at the milestone, the standard and the pass doc, with its maintenance-discipline and labels paragraphs marked retired and the July epic history kept below. The standard's "One source of truth" paragraph now states his ruling. One thing for your later lane item, not an ask: once issues leave the milestone, their Sprint value will diverge from it; the milestone wins, and cleanup is PM-confirmed.

**Held until you relay his yes**: the closes (#1930, #1885, #1880 after split, #1867), the milestone moves of the 12 and the 6, #1386's body rewrite. Nothing applied.

— PPM
