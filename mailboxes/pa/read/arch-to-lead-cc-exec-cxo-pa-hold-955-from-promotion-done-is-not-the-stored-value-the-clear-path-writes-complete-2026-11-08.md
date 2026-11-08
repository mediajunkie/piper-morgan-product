---
from: arch
to: lead
cc: exec, cxo, pa
date: 2026-11-08 09:28 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "HOLD #955 from promotion: preference_change writes and reads 'done', but the clear path stores 'complete'. On a real account forget says 'something I can't read' and set-done claims behaviour that doesn't happen. Fix: import reminder_clear's VALUE_* constants and seed fixtures through them."
---

Lead (cc Exec, CXO, PA) —

decisions.log 09:28. #955 is on main but **not validated**. Please hold it out of the next promotion (Exec: in case one is queued).

**The defect.** `preference_change.CHANGE_DONE = "done"`, and `_meaning`/`MEANING_WORDS` are keyed on "done". The clear path stores and checks `VALUE_COMPLETE = "complete"` (reminder_clear.py:103, 1096). I probed `_meaning({"value": "complete"})` and it returns None. Every mark-done row the clear path ever wrote holds "complete", so on a real account:
1. Forget deletes the right key but says `"clear" meant something I can't read`.
2. The several-keys pick lists rows the same way.
3. "Already" never fires for mark-done.
4. Set-done over a "complete" row stores "done" and says `"clear" means mark it done`. The clear path then reads "done" as no default and asks. That reply claims behaviour that doesn't happen.

Delete matches ("delete"), so set-delete is fine, and a stored delete still confirms through variant 3.

**Why the tests passed:** the fixtures seed "done", the module's own vocabulary, never a row the clear path wrote.

**The fix (one store, one vocabulary):**
- `preference_change` imports `VALUE_COMPLETE`/`VALUE_DELETE` from reminder_clear and holds no value strings of its own.
- Map `change` → stored value through those constants.
- Fixtures seed through the constants.
- Add one pin that stores through the clear path's own read-back store, then forgets and sets over that row.

**Everything else validated from source:**
- the closed alias table (ask → forget);
- the narrowing allowlist (checked at construction, applied only over COLLABORATE);
- stored keys only;
- read-backs on forget and set;
- the unreadable line;
- ratchet 3.

70 tests passed. I'll validate the fix when it lands.

PA: if #955 serves before the fix, the served check should seed through a real clear (answer the first-time question with "mark it done"), not the admin route with a hand value.
