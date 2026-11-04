---
from: arch
to: exec, lead
cc: cio
date: 2026-11-03 18:28 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2264 untrack and #2238 staging guard validated; my 17:09 no-rewrite recommendation lost its premise, so it's xian's look or a rewrite"
---

Exec, Lead (cc CIO),

**1. #2264, `66e4e8fdce`: validated.** `git ls-files data/postgres` returns 0 on main, and `.gitignore:91` and `.dockerignore:20` both list `data/postgres/`. This covers future trees and images only. History still holds `d3ee15de35`.

**2. The rewrite question, for xian (Exec).** At 17:09 I recommended no rewrite unless real data turned up. That rested on the folder being Temporal-only. Lead's names-only check found an early Piper schema (`base/16384`, 144 KB, eight tables including `stakeholders`, at most a few pages each). Nobody has read the rows. So the recommendation no longer holds as stated. The honest choice for xian:
- **Look first:** xian (not an agent, per rule 8) checks whether `stakeholders` holds anyone outside xian and his agents. Lead can hand him the read-only line. If it holds only test or placeholder names, there's no rewrite.
- **Or rewrite without looking:** treat it as the worst case. The cost is a force-push that every worktree and clone must re-sync, so it's a planned window, not a fire.
My read: look first. It's 144 KB, and the answer is very likely test data from the 03-30 Alpha setup.

**3. #2238, `2e562df09e`: validated from the source.** `target_for` is an allowlist: `--staging` passes only when `FLY_APP_NAME == "piper-morgan-staging"`. Without the flag, any `FLY_APP_NAME` or `DATABASE_URL` is refused, and alpha can't pass either branch. It fails closed, so xian's 17:18 direct-insert path is sound from this seat. Lead's `fly machine exec` line is the one to put on the card.

Verified how: `git ls-files data/postgres | wc -l` = 0 and grep of both ignore files on main at 18:27; read `scripts/create_test_alpha_user.py:49-71`. Layer: repo source. Not run: anything against staging or alpha. Recorded in decisions.log 18:27.

-- Arch
