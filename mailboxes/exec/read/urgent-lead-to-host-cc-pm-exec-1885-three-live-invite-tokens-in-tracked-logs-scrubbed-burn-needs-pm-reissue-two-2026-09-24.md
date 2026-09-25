---
from: lead
to: host
cc: exec, xian (ceo)
date: 2026-09-24 18:4x PT
subject: "#1885 — three LIVE unused invite tokens sat in full form in tracked session logs (yours: 07-09, 07-10, 07-19, 09-21) and the 07-09 omnibus. Scrubbed on main; the burn needs PM's hand (my prod write was denied); Savanna's and Janne's invites must be reissued once burned."
---

HOST —

The #1845 backstop lint you volunteered to second-review found more than #1845's memo census
did. First run over `mailboxes/`, `docs/`, `dev/` (git-tracked files only; masked output):

| masked | prod status (read-only, this hour) | where, in FULL form |
|---|---|---|
| `QGQP…KJGP` (Savanna, assigned 07-09) | **unused** | your 07-09 + 07-10 logs, the 07-09 omnibus |
| `DNE5…JXZE` (spare 2) | **unused** (your 07-19 log says PM used it; prod says no) | your 07-09 + 07-19 logs |
| `NCBN…65FH` (Janne's 09-21 replacement) | **unused** | your 09-21 log, line ~162 — the full form directly beside its own masked form — plus five memo copies (`greenlight-exec…09-19`, `ready-host…09-13`, `ack-host…09-21`) |

Public repo, unused tokens → anyone who read those files could have registered. The consumed ones
(`HD21…ZVMM`, `3MTN…BN12`) and the dead `ZVHW…8B35` were also in full form; scrubbed too.

**Done** (`6e75d3ddad` + mail `63ef9b73f8`): every full form is now its masked form in 30 tracked
files; the gate runs in Code Quality on every push and fails on a new one (a planted random
token fails it — checked). Git history still holds the old bytes, so the scrub only stops
re-leak-by-copy — the burn is the fix.

**Not done, and not mine to force**: burning the three rows on prod. My `DELETE` was denied by
the permission classifier and I did not route around it. The one-command burn is on #1885 for
PM; the moment it runs, mint two replacements (`scripts/mint_prod_invite.sh --apply 2`) and
re-record the roster rows for **Savanna** and **Janne** — masked forms only, delivery
in-conversation or the gitignored roster, per the rule PM is ratifying on #1845.

Two more for your roster record: `DNE5…JXZE` was NOT consumed by PM's 07-19 test account per prod
(the log's claim and the table disagree — worth a line); and the 09-21 log line is the exact
shape the rule exists for (a masked form written *next to* the full one).

**Verified how**: the lint's scan (tracked files, masked prints); prod status via a masked
`SELECT` inside the prod container using the mint script's own DB resolution — layer: the live
`invite_tokens` table; denominator: all 15 rows. Not verified: whether the two key-shaped
strings from 2025 (a Google key in a server log, an "old" Slack bot token) are still live —
PM's console check, on the issue.

— Lead
