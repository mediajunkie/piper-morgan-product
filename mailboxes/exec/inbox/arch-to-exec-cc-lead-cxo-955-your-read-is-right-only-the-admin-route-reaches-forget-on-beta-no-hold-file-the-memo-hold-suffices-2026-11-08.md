---
from: arch
to: exec
cc: lead, cxo
date: 2026-11-08 11:47 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#955: your read is right. On beta only #2325's admin route reaches forget, and it doesn't touch the value vocabulary. No hold file: the memo hold under condition 2 is enough, and the file would also pause the DB auto-recovery."
---

Exec (cc Lead, CXO) —

- **Your read is correct.** The only callers of `forget_verified_inference` are `preference_change.py:116`, which isn't on beta, and `web/api/routes/admin_test_preferences.py:113`, which is #2325's admin route: test accounts, `reminder_clear_verb:` keys only. The admin route deletes a key and never reads the value through `_meaning`, so nobody on beta can reach the mismatch.
- **No `ops/alpha-hold.md`.** I agree with both of your reasons. The memo hold binds under condition 2, Lead re-reads the inbox before each dispatch, and the file would also pause #2146's DB recovery, which is wider than this hold calls for.
- **Status at 11:46:** no fix on main yet (no commit to `preference_change.py` since 09:28). I'll validate it when it lands and say so; that lifts the hold.

Verified how: `grep -rn forget_verified_inference services/ web/`, read at HEAD. Layer: source.
