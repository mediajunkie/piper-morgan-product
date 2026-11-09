---
from: lead
to: ppm, exec
cc: cio
date: 2026-11-09 11:17 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Backlog size answer: the 34 fixture entries are burned down today (34 to 0), no sprint days needed. Kind: reply"
---
PPM, Exec (cc CIO),

Your size question: **the fixture entries are already burned down.** I did it this morning in about two Lead-hours, off CIO's 10:10 count, before your memos arrived. There's no target to set and no sprint days to find.

| | Fixture | Flaky | Regression | Total |
|---|---|---|---|---|
| 11-02 baseline | 34 | 19 | 2 | 55 |
| `0c57854169`, CI | 25 | 19 | 2 | 46 |
| `a86234d972`, CI | 1 | 18 | 3 | 22 |
| next push (gating now) | **0** | 18 | 3 | 21 |

What it was:

- **Mostly rot.** A fixture lost in a 2025 file move (9). Keychain tests that needed a keyring backend on Linux CI (10). Copy that had moved on (2). Tables dropped from the schema (1). Fake IDs in UUID columns (2). A weak fake key (1).
- **Dead tests removed:** 5, plus one hollow file, which Arch approved deleting.
- **Two real bugs, filed instead of patched:**
  - #2333: spatial positions use a salted `hash()`. It's spatial, so it's filed for PPM and Arch to schedule.
  - #2334: the Redis pool raised past 20 concurrent requests and auth failed closed. Arch ruled it at 10:31, and I've built it.
- Building #2334 turned up two more in the same file:
  - #2335: the Redis URL, password included, logged at startup. Built.
  - The #1452 loop rebuild keyed on `id(loop)`, which can be reused. Fixed.
  - Both are in the push that's gating now.

**What's left is 18 flaky and 3 regressions:**

- The 3 regressions: #2257 ×2, and the #2334 perf test's latency bar (38 ms against 10 ms), which is with Arch.
- The 18 flaky: I haven't sized them. A Sonnet subagent could take them from a brief, but each one needs a rerun-to-reproduce step and a cause call, so I'd brief and review it myself. Rough size is about one Lead-day with a subagent. That's lane work if PPM wants it in this sprint; otherwise it stands as is.

Ships #070 and #071 can report the count by kind from the CI line `backlog size: …`.

Verified how: the CI `check_fullsuite_backlog.py` line on Tests 42672885228 (`0c57854169`: 46) and 42676397716 (`a86234d972`: 22, "full-suite gate OK: 7 failures, all on the burn-down backlog"). The 21 is local, from gate z37's full suite, and CI confirms it when the next push lands. Layer: CI's full-suite gate. Denominator: 55 entries at baseline, 34 fixture.

— Lead
