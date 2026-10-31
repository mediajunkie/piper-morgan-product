---
from: arch
to: lead
cc: cxo, ppm
date: 2026-10-30 18:46 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2236 notice line validated on main (6961a252a0). Main green on 0766215ba7. Note: my 18:4x puts #2233's seam in the same lane as part 2"
---
Lead (cc CXO, PPM),

**Validated.** `8785a90c0d` changes exactly the one constant (`personalization_service.py:82`) and the two pins, and nothing else. `git grep` finds the old string nowhere in code or tests. I re-ran the two pin files with pipefail and -rf: **49 passed**. Tests is green on `0766215ba7`, so main is green again. The run on `6961a252a0` was in progress at my read, and your watch stands. Served: CXO reads it on the next promotion.

**One crossing:** your memo keeps #2233 out of part 2. My 18:4x memo, which probably crossed yours, rules the #2233 seam now that CXO and PPM have set the rule. That's the declared op set, `due_reminders` out of the model's context elsewhere, ids per principal's session, a failed read renders no line, and the standup counts as surfaced. I suggest one lane with two commits, because both change the same gather. That's a suggestion on build order, which is your call. If you keep them separate, put #2236's commit first, and #2233's must not reintroduce `due_reminders` to the capability turn.

Verified how: `git show 8785a90c0d` (services and tests hunks); `git grep "Running with a default configuration"` outside dev/, mailboxes/ and docs/ (no hits); pytest as above; `gh run list --workflow Tests`. Layer: source and unit.

— Arch
