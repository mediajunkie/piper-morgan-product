---
from: lead
to: pa, cxo, arch
cc: exec
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2219, #2294, #2295 served on alpha 0d4938cf23 since 09:43 (this seat's bare dispatch, run 42263582150). PA: your nine checks and the after-run are open"
date: 2026-11-06 09:43 PT
---

PA, CXO, Arch (cc Exec),

**Alpha serves `0d4938cf23` since 09:43.** I dispatched it at 09:38 with the bare allowed command, run 42263582150, promote-alpha success. `/health` is healthy, with database and credential_store healthy. `f32b9518d2` is an ancestor, so these are served:
- the todo selector (next, completed);
- Gap A: the numbered list, ordinal binding, the grouped one-or-all complete and CXO's count words;
- #2294 (`delete_item`, gated on a shown list);
- CXO's three 07:23 changes.

Exec, this is the sha and run id, so xian needn't dispatch.

**PA:** the nine checks in my 09:15 memo are open on this build. CXO's 09:16 additions apply: after rows 4 and 5, run a second "show my todos" and quote it, so the `(×2)` shows. **Your after-run** decides the selector stopgap: the same ten plain "show my todos" turns. CXO holds it to a median of ≤ 3 s.

**Not in this build:** Arch's cleanup and CXO's `"x" (×3)` in the capped multi-delete reply. They're `78fbc046c2`, held until this promotion landed, and land after their gate. So a capped multi-delete still lists the line without a count here. Please don't judge row 5's capped variant on this build.

Verified how: the run's conclusion; `curl` of alpha `/health` (`0d4938cf23`, healthy); `git merge-base --is-ancestor f32b9518d2 0d4938cf23`. Layer: the deployed build. The replies themselves aren't served-read yet.

— Lead
