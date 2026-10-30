---
from: lead
to: ppm
cc: exec, arch, pa
date: 2026-10-30 15:04 PT
in-reply-to: exec-to-ppm-pa-arch-lead-cxo-comms-host-xian-chose-b-he-promotes-main-now-haiku-5-5-screen-ok-2026-10-30.md
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Row 4 on the promoted build: tests/security on ac5b69f865, 156 passed, 4 skipped, 18 files. Same counts as the 10-29 read on e234776150. On #1386 as comment 6534476265"
---

PPM (cc Exec, Arch, PA):

**Row 4 stands on the new build.** Alpha's `/health` showed `git_sha` `ac5b69f8652767b5677edfe6b76ea6a36760821b` healthy at 15:01 PT (uptime 101 s when I read it at 15:03). I ran the security suite on a detached checkout of that sha:

```
pytest tests/security -m 'not llm' --maxfail=1000 -p no:cacheprovider -o addopts=""
156 passed, 4 skipped, 1 warning in 5.40s
```

Same counts as 10-29 on `e234776150` (156 passed, 4 skipped, 18 files). The 4 skips are the suite's standing skips, the same four as main's CI. Posted on #1386 as comment 6534476265; the row-4 line in the body is yours to flip.

Nothing of mine went to main between Exec's 14:52 hold and the promotion. PA's row 2 and the scenario-B confirm plus the reverse case are PA's, on this same sha.

Verified how: the command above, run once at 15:03 PT against Postgres on 5433 in a detached worktree at `ac5b69f865`, all 18 files of `tests/security/`. Layer: the test suite on the shipped tree, not the served host. Denominator: 160 collected, 156 passed, 4 skipped, 0 failed.

-- Lead
