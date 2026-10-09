---
from: ppm
to: exec
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Workstream review, Ship #064 (PPM)"
date: 2026-10-09 09:4x PT
---

Filed ahead of the kickoff. Window Fri 10-02 to Thu 10-08. Copy also at `dev/2026/10/09/workstream-064-ppm-2026-10-09.md`.


**Window**: Friday 02 October → Thursday 08 October 2026
**Filed**: 2026-10-09 (ahead of the kickoff, as Comms did)

## One paragraph, if that's all PM reads

The week turned the beta gate from a 31-issue pile into a measured list of 14, and put a slip
ledger and a brake under it. The gate moved 28 → 31 → 30 → 14 → 13 → 14 across the window, and
the dates PM set (design partners Fri 10-23, hard stop Fri 10-30) did not move. Three entries
count as slips against the baseline, and the brake has therefore fired: the 10-06 admission, the
10-08 #1965 admission, and (logged 10-09, outside the window but caused by it) the Epic 0 Phase 3
tail not finishing on Thu 10-08. The #1965 admission was ledgered late by me, along with the #1942 close (see "What I'd
want PM to know"). The date choice (cut scope, or accept a later date) is PM's and is waiting.

## What moved

- **The gate standard and the 14.** Mon 10-05: measured all 31 open MVP issues in full (bodies and
  threads, 31 of 31) and produced the pass: 4 firm gate, 5 needing a PM ruling, 4 close-or-split,
  6 Epic 0 evidence, 12 Production. Tue 10-06: PM's rulings (relayed by Exec) were applied, four
  closed, eleven plus three moved to Production, and the gate reached 14. Decision B (the
  invitation names GitHub only; #1852 left the gate) and Decision D (an `Owner:` line, no
  backfill) went into `docs/internal/planning/beta-gate-standard.md`.
- **The slip ledger.** Every admission, close and un-admission since the 10-05 baseline is a row in
  that file with a `Gate class:` line. The brake (second slip, or more than 7 cumulative days)
  triggered on 10-08 with the #1965 admission. I proposed no date; PM chooses.
- **Date recommendation (10-04).** Recommended design partners by Fri 10-23 with Fri 10-30 as the
  outer bound, assumptions and a re-plan trigger stated. They are the baseline dates in the
  10-05 ledger row.
- **Destination rulings (10-02/03).** The 13-row Phase 3 destination thread closed 13 of 13
  agreed after I conceded C1 to CXO and held D1 on a quoted handler docstring
  (`session_activity_query` is keyed to THIS session); D1 shipped and was measured live by 09:33
  on 10-03. The 10-06 re-judge verdicts went to Lead, who landed 30 rows; I conceded two list-projects
  rows (my claim came from scorer mismatch lines, not the recorded router decision).
- **Placement discipline.** `#1923`–`#1936` and, later, `#1957`–`#1966` were placed with milestone and
  board entries as they were filed. By 10-08 evening no open issue was unmilestoned (0 of 302).
  Assignment rule decided and filed 10-05 (#1940): Assignee stays `mediajunkie`, role goes in an
  `Owner:` body line. I filed #1932 and #1935 (Production).
- **Infrastructure.** Fri 10-02: this seat moved from a session cron to the LaunchAgent cadence.
  A criteria-line script (`scripts/ppm-criteria-line.sh`) now prints MVP open, the gap versus the
  order doc, and the unmilestoned count in one run.
- **Beta invitation known-issues lines (10-07).** Keep/strike calls on each line against the
  source; #1735 was struck, then reinstated at 15:33 after CXO's source read, which I re-verified
  myself. PM approved the invitation doc as written that evening.

## What didn't move

- **The dates** (as above). Held pending PM's answer via Exec.
- **#1889 / #1963 / #1965 closure.** They wait on alpha promote, PM-provisioned OAuth-only and
  PAT-only accounts, and a served reply CXO can quote for each.
- **#1886** closure is Lead's. **Lead's sizing of criteria 2/4/5** is not in yet.
- **Roadmap v18 fold.** Waits on the date answer.

## Progress toward milestone status, not activity

Same instrument each time, not hand-counted: `sprint-truth.py` read 28 not done / 1224 done at
the 10-02 close, and 14 not done / 1235 done at the 10-06 close (0 unmilestoned both times). The
MVP-open count then went 13 on 10-07 (#1942 closed with live evidence) and 14 on 10-08 (#1965
admitted); the 10-08 figure is from the criteria line, not `sprint-truth.py`. Net: 14 fewer open
over the window, almost all of it from the 10-06 triage rulings (closes and moves to Production),
not from burn-down. **Excluding any stronger reading**: the fall from 28 to 14 is mostly scope
sorting by PM's rulings, and the closures themselves were Lead's and others' work. My own
product was the pass, the standard, the ledger and the placements. I have not myself verified a
closing proof for any of the 14 still open.

## What I'd want PM to know that isn't in a bullet above

- **I missed two ledger rows and found them myself on 10-09.** The #1942 close (10-07 17:03) and
  the #1965 admission (10-08 ~15:50) were not recorded in the slip ledger when they happened. I
  found both while preparing the weekly line, ledgered them late, and marked each row "ledgered
  late". The effect was that the brake fired on a ledger I had not kept current, and the
  triggering admission sat unrecorded for about 15 hours. Moves since then are ledgered in the
  same fire; I'd rather the process make that mechanical than rely on me remembering.
- **Two wrong claims, both fixed same day.** On #1931 I said completion was reversible from the
  todo UI; it was not, and I corrected it on the issue. On the destination rulings I conceded two
  rows when my evidence turned out to be scorer mismatch lines rather than the recorded router decision.
- **Re-armed a session cron on a LaunchAgent seat (10-07 18:33)** before re-reading the carry
  forward, and deleted it the same fire.
- **Epic 0 Phase 3 tail.** Lead's 155 → 125 recount (Arch's ruling:
  file-reference names out, filler in) leaves the ratchet ceiling at 155; that recount itself is not a
  slip and moved no days. The slip entry is that the tail itself missed Thu 10-08 21:59. Those figures (155, 125, "0 GO",
  roughly two days) are Lead's and Arch's; I have not re-measured them.
- **Open spend question for PM:** a ~$1.70 scoring run on the Lead-seat key ending `…6wAA`. Answer
  needed as "yes, on key X"; I have not confirmed which console key that is.

**Verified how:** method: read the seven PPM session logs for 10-02 through 10-08 (day-arcs and
close sections), the slip-ledger rows in `beta-gate-standard.md`, and the criteria line and CI
status this fire (10-09 09:33 PDT). Layer: my own logs and the tracker/ledger record, not a
fresh probe of alpha or of any issue's closing evidence. Denominator: 7 of 7 PPM logs in the
window; gate counts are the ones my logs state, `sprint-truth.py` for 10-02 and 10-06 and the
criteria line for 10-07/10-08; Lead's and Arch's figures are quoted, not re-measured.
