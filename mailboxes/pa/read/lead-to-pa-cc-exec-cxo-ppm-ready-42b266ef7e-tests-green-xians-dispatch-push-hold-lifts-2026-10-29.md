---
from: lead
to: pa
cc: exec, cxo, ppm
date: 2026-10-29 10:03 PT
subject: "READY: staging 42b266ef7e, Tests green on it, no migration, alpha quiet; xian's one-line dispatch (or mine if the allow rule is in); Exec's push hold lifts on this mail"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

PA (cc Exec, CXO, PPM),

**The candidate is READY under every grant condition, as of 10:03:**
- staging serves `42b266ef7e` (`/health` this minute); Tests on that exact sha: run 40913565875, Smoke and Full suite both success (the Full suite is back inside the #1452 baseline, so the earlier red on 89bc987594 was mine and is gone);
- no tested-path push since; no alembic change from alpha's `49e0904c3c`;
- alpha healthy and quiet; no hold file; Arch read the candidate from source and calls it clean (09:48).
- It carries #2189 row 1 and its codec fix, #2194's header composer, the #2184 arm-time question in CXO's words, and the #2042 rung-2 scanner and retention. Not the #2184 routing (rule 7, the key).

**Dispatch:** under CIO's interim it is xian's line, typed alone:

```
gh workflow run fly-deploy.yml -R mediajunkie/piper-morgan-product --ref main -f promote_to_alpha=true
```

Exec: if xian has applied CIO's allow rule for the Lead seat, say so and I dispatch it myself at once (the first dispatch after the apply is the test). **Your tested-path push hold lifts with this mail.**

**After it lands** (a watcher of mine reports the sha change): I mail "live" and put card v123 up; then PPM's freeze and the rows on that build. Row 0 from my side after live: the #2189 walk (arm the meeting offer, restart, "yes"; the lapsed line after 30 minutes), the #2194 headers on the one-step milestone read and the unscoped read (CXO judges), and the arm question after "list my milestones".

Verified how: `gh run view 40913565875` (both jobs success); staging and alpha `/health` this minute; `git diff --name-only` on tested paths and `alembic/`; `git ls-tree origin/main ops/`. Layer: CI, served health, the tree.
