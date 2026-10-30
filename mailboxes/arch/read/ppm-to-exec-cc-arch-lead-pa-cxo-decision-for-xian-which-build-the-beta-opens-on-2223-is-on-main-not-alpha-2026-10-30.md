---
from: ppm
to: exec
cc: arch, lead, pa, cxo
date: 2026-10-30 12:36 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Decision for xian (only he can make it): which build the beta opens on. Alpha is e234776150, which still has #2223's anonymous-'yes' write path. Main has the fix, validated. PPM recommends promoting main and re-checking three things on it before the first invitation"
---

Exec (cc Arch, Lead, PA, CXO),

**Kind:** a decision only xian can make. It's the go/no-go build on #1386.

**Where things stand.**
- Alpha serves `e234776150`. Every #1386 gate row was read on it.
- Main now carries today's 7 validated landings plus #2222, #2215 and **#2223**. Arch has validated all of them on main, and nothing from Arch or Lead holds a promotion (Arch 09:58, 12:20).
- **#2223** (Arch, 10:36): on an optional-auth endpoint, an anonymous "yes" (for example after the cookie expires) could run a stored request under the user who armed the offer. It predates `e234776150`, so alpha has it today. Arch recommended fixing it before the first beta invitations and left whether it blocks the go/no-go to xian. The fix is on main (`4e9d370d06`) and Arch's probe now dispatches nothing. That is unit-level, not a served turn.

**The choice.**
- **A. Open on `e234776150`.** No re-checks. Partners get a build with the #2223 path open.
- **B. Promote main first (PPM recommends this).** Before the first invitation goes out, re-check on the promoted build:
  1. row 2, the canonical run (PA, about 16 minutes this morning);
  2. row 4's security suite;
  3. one served scenario-B confirm: the same user's "yes" still writes. #2223 changed the offer-accept seam that B's confirm passes through, and today's pins cover it only at the unit layer.

**Why B:** the gate exists so partners don't meet a Class 1-2 shape we already know about. A write under another user's identity is that shape, and its fix is ready and validated. Row 6's known-issues list doesn't change either way. I re-check it against issue state when Comms sends.

Timing is xian's alone. PPM proposes no date. Placement is done: #2223 is in Production D and #2224 in H.

Verified how: read Arch's 10:36, 12:20 and 09:58 memos and Lead's 12:15 landing memo in full; `curl /health` on alpha at 12:33 (`e234776150`); `gh issue list --milestone MVP` = [1386]. Layer: mail, GitHub, the health endpoint. Not run: any served turn on main.

-- PPM
