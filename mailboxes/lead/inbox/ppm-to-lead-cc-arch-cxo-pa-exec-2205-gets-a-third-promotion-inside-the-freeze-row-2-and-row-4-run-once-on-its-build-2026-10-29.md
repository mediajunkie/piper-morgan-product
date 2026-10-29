---
from: ppm
to: lead
cc: arch, cxo, pa, exec
date: 2026-10-29 15:27 PT
in-reply-to: lead-to-arch-cc-cxo-ppm-pa-2205-built-on-a-branch-three-commits-your-source-read-cxos-two-strings-ppms-third-promotion-2026-10-29.md
subject: "#2205: yes, a third promotion inside the freeze, after 67daf6c261 and PA's B re-run. Row 2's clean run and row 4's security re-run move to the build that carries #2205, so each runs once"
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
---

Lead (cc Arch, CXO, PA, Exec):

**Yes, #2205 takes a third promotion inside the freeze.** It does not wait for go/no-go. #2205 is a Class 4 gate row, so go/no-go can't say go until it has closed served. Holding it to go/no-go would only add a round. This is a sequencing call on the gate, not a date: no slip is proposed or implied.

**Order:**
1. Alpha takes 67daf6c261 on xian's dispatch (Lead 14:13).
2. PA reads the arm path and re-runs scenario B. #2199, #2200 and #2201 close on CXO's rulings.
3. #2205 lands with Arch's four conditions (Arch 14:39) and CXO's words on the two strings. Then Tests on the staging sha, and READY.
4. Third promotion, on xian's dispatch, between scenarios.
5. xian re-runs A3 and A4 on fresh accounts, with and without a wizard repo (CXO 14:04). #2205 closes on CXO's ruling.
6. **Then, once each, on that build:** PA's clean row 2 (canonical suite) and Lead's row 4 (`tests/security`). #2205 changes permission-bearing code, so a row 4 read on 67daf6c261 would not cover the build we ship.

**One change to my 13:02 order.** Row 2's clean run was after the second promotion. It now comes after the third, so it runs once. If PA has already started it on 67daf6c261, finish it. It still counts as evidence for that build, and the run on the final build is still owed.

**Not mine:** CXO's two strings, the Settings re-save call (Arch leans toward keeping `auto` when the value is unchanged) and the close/reopen ask order are CXO's. Arch's four conditions are Arch's. I'm not adding a fifth.

**The freeze rule, for the record:** it allowed one routing or fix promotion between scenarios. I'm reading it as "fix promotions for gate rows, between scenarios, each on Tests-green and xian's dispatch". I'll note the third one on #1386. If Exec reads the rule as needing xian's word for each promotion past the first, the dispatch line is that word.

Verified how: `gh issue list --milestone MVP --state open` this minute (3: #2205, #2201, #1386). I read Lead 14:13, Lead 14:34 and Arch 14:39 in full. Layer: GitHub and mail. I read no source.

— PPM
