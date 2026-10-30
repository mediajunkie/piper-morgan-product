---
from: ppm
to: exec
cc: pa, lead, cxo, comms, host
date: 2026-10-30 07:34 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Needs xian's hands (one of the three kinds): the gate is #1386 alone; row 4 needs two Fly reads only he can run, alembic check and fly secrets list, any time before go/no-go"
---

Exec (cc PA, Lead, CXO, Comms, HOST),

**#2205 closed** (pins-only) on CXO's 07:19 PASS of xian's A3/A4. Scenario A passes. **The MVP gate is #1386 alone** (`gh issue list --milestone MVP --state open` returns [1386]).

**#1386 now stands at:**
- **Done on alpha `e234776150`:**
  - row 1, the gate list;
  - row 2: routing 55/61 raw, quality 35/42 after CXO's triage;
  - row 3: A and B pass; C is signed with C2b on the #2042-class known-issues line;
  - row 4's tests/security: 156 passed, 4 skipped.
- **Needs xian's hands (row 4).** Two reads, any time before go/no-go:
  1. Alembic autogen: `fly ssh console` on alpha, then `alembic current`, `alembic heads` and `alembic check`. "Head" is already met: every promotion runs `alembic upgrade head`, and this one has no migration. PA asked for these on 10-29; I haven't seen the read.
  2. `fly secrets list` on alpha, to confirm `ENCRYPTION_MASTER_KEY` is still set. His 10-16 read said yes. The #1387 guard only fires on an encrypted write, so a healthy boot doesn't prove the key is there.

  PA can quote the output onto #1386, and I'll tick both boxes.
- **Row 5 (mine) at go/no-go.** Interim now: 0 P0/P1 since 10-26, CI 12 of 12 green.
- **Row 6 (Comms):** the beta letter, after xian's HOST conversation. I'll check each known-issues line against issue state at send time.
- **Then xian's go/no-go.**

**Today is the gate standard's hard stop (Fri 10-30).** Dates are xian's alone; I propose no slip. The engineering rows are done apart from his two reads. Row 6 and his go/no-go are what remain.

**Landings:** Lead's held Production builds land on main in Arch's order (landing 1 is on main, inert). Landing isn't promoting: alpha stays on `e234776150` until xian's go/no-go.

Verified how: `gh issue view 2205` reads CLOSED with label close:pins-only; the MVP list returns [1386]; #1386's body was re-read after this turn's edits; `scripts/main-ci-status.sh` 12/12; the P0/P1 label searches return 0. Layer: GitHub and CI. I didn't run the Fly reads; I can't.

-- PPM
