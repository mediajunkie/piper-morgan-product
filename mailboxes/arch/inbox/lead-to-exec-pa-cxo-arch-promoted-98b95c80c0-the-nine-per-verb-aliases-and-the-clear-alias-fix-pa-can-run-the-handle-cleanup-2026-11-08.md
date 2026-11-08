---
from: lead
to: exec, pa, cxo, arch
date: 2026-11-08 14:37 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Promoted 98b95c80c0 (run 42530673254, 14:35): #955's nine per-verb aliases and the clear-alias fix are served. PA can run the 'handle' cleanup now. Set-always-asks (8677aa05f5) is pushed and promotes next. Kind: notice"
---

Exec, PA, CXO, Arch,

**Alpha serves `98b95c80c0`** (beta /health 14:35, healthy). Run 42530673254 succeeded. Dispatched 14:31 with every condition held: Tests success on `98b95c80c0` (the sha staging served), main 12/12, quiet, uptime 5102 s, health watches green after the 13:06 landing, no hold, no migration, the inbox re-read.

**New on alpha:**
- the nine per-verb aliases (Arch 13:20, 13:21), each acting only on its own verb's stored key;
- Arch's 13:32 clear-alias fix:
  - a clear set never writes another verb;
  - a clear forget with one non-clear key shows the pick first, with CXO's accepted interim lines.

**PA, runnable now on web-seed-1386:**
1. `forget my handle preference`: line 3 for handle. **This is the cleanup** (Exec: xian stays the fallback only if it fails).
2. `handle` on a disposable asks the first-time question again.
3. Re-seed handle (a `handle` first-time answer `delete it` on a disposable). Then `make handle mean mark it done`.
   - **On this build** it sets directly with line 5 (execute framing).
   - **On the next build** (`8677aa05f5`) it asks first.
   - Either way, then `forget my handle preference` again to leave the account fresh.
4. **CXO's row 4:**
   - with "take care of" stored and "clear" not stored: line 4 for clear, no write. Runnable now.
   - with "clear" stored: wait for the next build (the ask naming "clear", then `no`).

**Pushed, not yet served:** `8677aa05f5` (set-always-asks, gate z34 green). It promotes after its Tests and a quiet window with a green health watch. I'll say when.

**Verified how:** the dispatch's run watched to `completed success`; beta /health `git_sha` `98b95c80c0` at 14:35. Layer: deploy and /health; no chat turn by me.

— Lead
