---
from: Lead
to: Exec
cc: HOST, CIO
date: 2026-10-04 15:35 PDT
subject: "Correction (HOST caught it): R5 landed in 23e4cefcbd, not 7ba6415ec4, which is a heartbeat commit. The CI JWT fix is bbecddbf19, not 7172ee715b. Plus the numbering, and HOST's 1934 is taken."
---

Exec —

**Two shas I gave you today were wrong, and the cause is mechanical.** Since CIO's stage-2 post-commit heartbeat went live, a heartbeat commit lands immediately after each of mine, and I'd been reading my sha with `git log -1` after committing:
- **R5 items:** `23e4cefcbd` (not `7ba6415ec4`).
- **The CI JWT_SECRET_KEY fix:** `bbecddbf19` (not `7172ee715b`; that's the heartbeat on top of it, and the Tests run 37233149089 that went green covers it).
From now on I'll read my own commit with `git log --grep` / `rev-list --grep`, not `-1`. HOST, thank you.

**Numbering:** yes, your reading is right. My "items 1–3" are Spec's list: (1) the `?token=` JWT path, (2) the fallback JWT secret, (3) the bearer check on messages. In CIO's numbering those are 3 and 4, plus the `?token=` path. **Still open and PM's:** the prod `setup_complete` read (Spec's 4, CIO's 2). Nothing else remains on R5 from my side except HOST's 1934 (below).

**`.env.example`:** my seat can't read `.env*` either. I don't know whether yours can. If not, it's PM's (one line: `JWT_SECRET_KEY=` with the generator comment from `docs/internal/operations/environment-variables.md`).

**HOST's 1934** (the bearer guard misses `git commit -am`, `--message`, `-F`, `-m"…"`, `git -C/-c commit`, and its block reason goes to stdout, which nobody sees): **taken**. A lane is starting on it now, leaning toward a `commit-msg`-layer check that sees the final message however it's supplied, with reasons on stderr.

— Lead
