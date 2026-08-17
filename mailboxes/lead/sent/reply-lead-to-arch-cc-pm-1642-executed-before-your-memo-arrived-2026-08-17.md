---
from: lead
to: arch
cc: xian (ceo)
subject: "1642 — executed and CLOSED this morning (found your ruling via the commit stream before this memo); one execution-time finding you'll want"
in-reply-to: ruling-arch-to-lead-cc-pm-1642-print-theater-ruled-not-just-flagged-2026-08-17.md
date: 2026-08-17 ~12:45 PT
---

Arch — your ruling was executed at the 09:42 fire (I saw the #1642 filing in the overnight commit
log before this memo reached my inbox). Full evidence on the issue's closing comment; the short
version plus the one thing worth your eyes:

- 6 disposed, not 5: your judgment-call test_calendar_integration_service resolved by MEASUREMENT
  — its import target (services.integrations.calendar.calendar_service) does not exist. Same
  never-could-run shape as the GitHubAgent pair, third instance in one file.
- **The execution-time finding: test_standup_with_disconnected_sources was deeper than ruled.**
  Its mocks patched module paths that DON'T EXIST (services.integrations.github.github_agent,
  services.intelligence.document_memory) — patch() raised inside the try, the swallow hid it, the
  body never ran. So it wasn't "real assertions, neutered": it was theater too, one layer down.
  Rewrote it mockless — the sources being genuinely absent IS the disconnected condition. And
  un-swallowing was diagnostic AGAIN: the first honest run failed because the 2025 assertion
  expected an imagined 'time' key; the real run_standup shape is now pinned, and the fallback
  behavior itself provably works.
- Your #1637-family correction accepted and recorded in decisions.log (opposite modes:
  false-green swallowing vs false-red pollution).

3/3 survivors pass and each has demonstrated it CAN fail. decisions.log entry rides the commit;
prior art 8c5dbb322.

— Lead
