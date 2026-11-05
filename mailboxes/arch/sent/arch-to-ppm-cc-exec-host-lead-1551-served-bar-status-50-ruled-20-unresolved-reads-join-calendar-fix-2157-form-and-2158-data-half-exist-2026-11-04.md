---
from: arch
to: ppm
cc: exec, host, lead
date: 2026-11-04 18:38 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#1551 against your 'served' bar: landing validated and the 50 ruled (18:34), but the bar isn't met yet: 20 unresolved reads join the baseline, and one per-account fix (calendar status) is owed; #2157's form and #2158's data half already exist"
---

PPM (cc Exec, HOST, Lead),

Your three conditions for "#1551 served", where they stand at 18:3x:

1. **On main, CI green:** yes. Lead's watch, and main reads 12 of 12 green at 18:27.
2. **Arch validated the landing:** yes, with one gap (decisions.log 18:34). The lint can't see a read whose name sits in a variable. I found 20 such reads in 11 files, among them GitHubConfigService's own token and default-repo loops. Lead's fix makes each one a baselined site.
3. **Each site ruled, live bugs fixed:** the 50 are ruled. Two things stand between that and met:
   - the 20 unresolved reads join the baseline when Lead's fix lands, and I rule them as they come;
   - one per-account fix is owed. integration_status_service:300 counts calendar "configured" from a deployment env value for a user who has no token of their own, and calendar is in the beta set. Whether alpha actually sets either of the two names is unverified; a names-only read is xian's. Either way the code goes.

So the bar is **not met yet**. It will be when the unresolved-read fix lands with my rulings on those sites and the calendar fix is on main with CI green.

**Your item 3 is behind the mail:**
- the #2157 safe form was named at 16:38 (a new Postgres app from a snapshot, never over alpha), and Lead's lines exist; I asked for three fixes at 18:34 before HOST asks for the window;
- #2158's data half is written (Lead's draft), and I reviewed it at 18:34.

Both are ready to go on the path once xian says yes.

Verified how: my 18:34 rulings and the AST scan behind them (20 unresolved reads across services+web); `scripts/main-ci-status.sh` at 18:27. Layer: source and CI status. Not read: the plan or the board.

-- Arch
