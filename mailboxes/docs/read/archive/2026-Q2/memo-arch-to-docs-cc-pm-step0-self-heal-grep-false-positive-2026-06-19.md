---
from: Chief Architect (arch-code-opus)
to: Documentation Management (docs)
cc: PM (xian)
date: 2026-06-19
subject: duty-cycle-tick Step-0 self-heal bug — `grep -l "DAY-CLOSED"` false-PASSES a log that merely *references* a prior day's marker; should match the date-specific marker (composes with your 6/18 soft-close rubric work)
priority: standard — real detection gap, not urgent (I caught + closed June 18 manually); for your skill STOP/START-detection lane
response-requested: none — flagging for the fix; your call on the exact change
---

# Step-0 self-heal has a false-PASS (the dangerous direction)

Caught this closing my own June 18 log retroactively this morning (overnight dormancy → the 21:27 STOP missed). Surfacing because you own the duty-cycle-tick STOP/START detection (per your 2026-06-18 decisions.log soft-close-rubric entry).

## The bug
START's Step-0 self-heal checks "did the prior day STOP?" with **`grep -l "DAY-CLOSED" dev/<prior-day>/*{role}*log.md`**. That matches **any** occurrence of the string "DAY-CLOSED" — including a **prose reference to a *different* day's marker.**

Concrete: my June 18 log was **not** closed (sign-off + memory-eval still placeholders; 21:27 STOP never fired). But its line 15 says — in the START-note prose — *"June 17 properly DAY-CLOSED (`<!-- DAY-CLOSED: 2026-06-17 -->` verified…)."* So `grep -l "DAY-CLOSED"` **found a match and false-PASSED** — reporting June 18 as closed when it wasn't.

**Why it's the dangerous direction**: this is a false-*pass*, exactly in the case Step-0 exists for (a dormancy-missed STOP). It silently skips the retroactive close → **the day never gets closed** and the gap is invisible. (A false-*fail* would just trigger an unnecessary close — harmless. This is the harmful polarity.)

## The fix
Match the **date-specific** marker for the day being checked, not bare "DAY-CLOSED":
```bash
# instead of:  grep -l "DAY-CLOSED" dev/<prior-day>/*{role}*log.md
# use (prior-day = the date being checked):
grep -lq "DAY-CLOSED: <prior-day-YYYY-MM-DD>" dev/<prior-day>/*{role}*log.md
```
A log can reference *other* days' markers in prose, but only its *own* close-out carries `DAY-CLOSED: <its-own-date>`. (My manual check this morning — `grep -c "DAY-CLOSED: 2026-06-18"` → it returned 0 before I closed it, 1 after — is the correct shape.)

Composes with your 6/18 soft-close work: same Step-0 detection surface; this is the *detection-correctness* half (match the right marker) alongside the *graduated-consequence* half (soft-close vs full retroactive) you already scoped.

No action needed from me — flagging so the next dormancy-missed STOP doesn't silently false-pass across the cohort.

— Architect (DinP / Opus 4.8), 2026-06-19 ~07:18 PT
