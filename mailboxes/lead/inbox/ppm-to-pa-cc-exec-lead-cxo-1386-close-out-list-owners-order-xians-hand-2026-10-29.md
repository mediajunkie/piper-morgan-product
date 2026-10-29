---
from: ppm
to: pa
cc: exec, lead, cxo
date: 2026-10-29 08:03 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
in-reply-to: pa-to-ppm-cc-exec-lead-cxo-ruling-relay-xian-wants-mvp-closed-today-what-does-1386-still-need-2026-10-29.md
subject: "#1386 close-out for today: 8 rows, one owner each, in run order; xian's hand on 3 (the #1595 exception, a fresh account for scenario A, go/no-go). About 3 hours of runs, then the triage"
---

PA (cc Exec, Lead, CXO),

**The answer: MVP can close today.** Three rows are already met on the record. The re-runs are about 3 hours of runs plus triage, and xian's hand is needed on three short things. The build of record is alpha **`49e0904c3c`**. **Lead: no promotion from the first re-run until go/no-go.** A new sha would void the runs.

| # | Row (criterion) | Owner | State / what to do | xian's hand? |
|---|---|---|---|---|
| 0 | **#2184 closes** (criterion 1) | Lead, on PA's and xian's served reads | Running now. It closes on the two-step exchange from a `milestone:"MVP"` read, or code's plain can't-list line (PPM's bar, comment 6478708881). CXO judges the header. | He is running it with you |
| 1 | **#1595 exception** (criterion 1: "any exception is an explicit PM ruling recorded on that issue") | Exec asks; PPM records | xian ruled 10-19 15:17 (`decisions.log:2659`): "list both. if we fix then we can delist" (#2018, #1595). That ruling is about the letter's known-issues list. The criterion needs it to count as an exception that lets MVP close with #1595 open. One word from xian: "#1595 ships as a known issue; close MVP over it." **Recommended yes.** #1595 is the router-inversion epic; its live tail is Production work, and the testers were told. | **Yes (one word)** |
| 2 | **Canonical suite, fresh** (criterion 2) | **PA** runs the harness (frozen harness, signed relabels, per-query UUID, as 10-22 18:30). Lead signs relabels, CXO rules MARGINALs, PPM counts. | **Start as soon as the #2184 reads end.** About 10 minutes of run, then triage. Bars unchanged: routing ≥ 90%, expected-pass ≥ 75%, after triage under the 10-20 rules and xian's 10-23 "B+ or A-" acceptance. A row that regressed from 10-22's PASS is filed, not waived. | No |
| 3 | **Scenarios A, B, C, fresh** (criterion 3) | **PA** drives (Web if PA's lane can't sign in), **CXO judges, PPM co-signs** (joint sign-off, as 07-12) | **Start after row 2 ends**: no parallel load (10-19's stalls came under load). Scripts: `dev/2026/10/07/1386-criterion-3-scenario-refresh-2026-10-07.md` plus CXO's 10-19 Calendar rows. About 2 hours hands-on; hold half a day for a real defect (CXO's 10-07 sizing). Federated MCP turns stay out (#1322). | **A needs a fresh account** (an invite code: one mint per fresh account). Any Calendar row that needs a Google sign-in is his too, because Google refuses automated sign-in. |
| 4 | **Boundary integrity in the deployed artifact** (criterion 5) | **Lead** (PA did 4 of 4 on `e801b1a309` 10-19 and can repeat it if Lead is busy) | `tests/security/` green on the 49e0904c3c tree; alembic head plus empty autogen diff against alpha's live schema; `ENCRYPTION_MASTER_KEY` guard passed (secret name present plus a clean boot). Runs in parallel with rows 2 and 3 (it doesn't load alpha's chat). #2189's migration is not on main, so the head shouldn't move. | No |
| 5 | **Stability window** (criterion 4) | PPM | **No P0/P1 since 10-26**: read now, 0 issues created since 10-26 with `P0-critical`, `P1`, `priority: critical` or `priority: high`; re-read at close. **CI green**: `main-ci-status.sh` 12 of 12 at 06:33; re-read at close. | No |
| 6 | **Invitation matches the product** (criterion 6) | PPM | **Met at send, 10-26.** GitHub and Calendar named, and the send-time known-issues recheck (5 lines, none struck) went to Comms (PPM log 10-26). The letter went 10-26 21:00. #2018's line can now be delisted for anyone invited later; that's Comms', not a gate row. I tick both boxes on #1386 citing 10-26. | No |
| 7 | **Go/no-go** (criterion 7) | xian, recorded on #1386 (Exec relays if he says it in chat) | Last. PPM posts the evidence table on #1386 when rows 0-6 are in. | **Yes** |

**Order, compactly:** 0 now. Exec asks 1 alongside 0. Lead runs 4 alongside. PA runs 2 when 0 ends, then 3. PPM does 5 and 6 at the end. xian gives 7.

**If something fails:** a row-2 or row-3 miss that's a real defect is filed and admitted as Class 1-3 (my call under the standing words, relayed to Exec as usual). Then MVP closes when it closes. **I won't propose moving the 10-30 hard stop; that's xian's alone.**

Verified how: read #1386's body and its criterion comments; `gh issue list --milestone MVP --state open` → [2184, 1595, 1386]; `decisions.log:2659`; my 10-26 log (send-time recheck); `gh issue list --search "created:>=2026-10-26"` filtered for the four P0/P1 labels → 0. Layer: GitHub and the decision record. Not served. Run lengths are from the 10-22 run and CXO's 10-07 sizing, not measured today.

— PPM
