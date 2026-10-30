---
from: arch
to: lead
cc: cxo, ppm, pa
date: 2026-10-30 15:57 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2225 validated on main (47a9f431db), source read and pins re-run. One docstring line owed; the served check is still open"
---
Lead (cc CXO, PPM, PA),

**Validated against the 15:18 and 15:26 rulings.**

1. **`0bb891fe32`, the draft seam.** In the `issue_number is None` branch, `peek_pending_offer` runs after the dispatch. An occupied store passes the inner reply through, with no retained-line tail and no re-arm. An empty store keeps today's `_rearm()`. A failed peek reads as empty, which is the safe direction: the worst case is today's behaviour, and it's logged. It checks the store, not a flag, as ruled.
2. **`95416525da`, the carrier.** The re-ask sits at the final `return None` and is gated on `persist_default` plus a stored question. The guards above it (a different issue, an outside-family imperative, an exit or decline, a state question, no principal, a principal mismatch) all return before it, so a clear command still routes. Carriers without `persist_default` are unchanged. `_bind_and_dispatch` is untouched, so there's still no second confirm. A bare "yes" mid-question used to reach the same re-ask through the generic accept, and now gets there directly.
3. **Pins re-run by me:** `test_drafted_issue_repo_answer_2225.py` plus `test_repo_clarification_1567.py`, **71 passed**, on main at 47a9f431db, with Lead's venv. The tree was clean afterwards.

**Owed, one line:** `peek_pending_offer`'s docstring says "Two sanctioned readers, neither on the dispatch path". `drafted_issue`'s no-clobber check is now a third. It's the same kind as #1753's set-site guard (it reads and never consumes), so it's sanctioned, but the docstring should name it so the next reader doesn't take it for a forbidden peek. Fold it into your next commit that touches that file. It doesn't need its own unit.

**Not covered here:**
- CI Tests on 47a9f431db was in progress when I checked (22:53Z start). Your watch stands.
- No served turn. This build isn't on alpha. When a promotion carries it, CXO's three-turn script is the served check (a compose draft, then "yes", then `owner/name`, giving the created line; a later create with no repo named goes there without asking). PPM's condition re-runs row 2 plus B's confirm and the reverse case, if that promotion comes before xian's go/no-go.
- PPM strikes the letter's seventh line only on that served quote.

Verified how: `git show 0bb891fe32` and `git show 95416525da` read in full (services/ hunks); `soft_invocation.py:763` (`peek_pending_offer`, read without clear) read at 47a9f431db; pytest run as above; `gh run list --workflow Tests` (47a9f431db in progress). Layer: source and unit suite. Denominator: the two seams ruled, 2 of 2.

— Arch
