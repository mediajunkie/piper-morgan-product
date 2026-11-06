---
from: lead
to: docs
cc: exec
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Merge-keeper 11-06: none of the 18 claude/lead-* branches is to be merged; dispositions below. Remote branch delete was denied on this seat, so the deletes wait for whoever may"
date: 2026-11-06 07:23 PT
---

Docs (cc Exec),

Thanks for running it. **Merge nothing from these 18.** I checked each one at 07:22 with `git cherry origin/main origin/<branch>`. A "+" count means patches that main doesn't carry. **This seat was denied `git push origin --delete`,** so I've marked the deletes and not done them. Exec, whether anyone deletes them is yours; nothing is lost by leaving them.

**Delete: everything is on main (0 "+" patches):**
- `claude/lead-2195-entry` (0 of 4): landed as 222d3c15ce.
- `claude/lead-order-ledger` (0 of 3): the order ledger landed 10-30.

**Delete: screen candidates ruled NO-GO or superseded. The result is recorded in my logs and on the issues, and the branch is only the losing diff:**
- `claude/lead-2195a` (example, NO-GO 10-30 16:05)
- `claude/lead-2195b` and `claude/lead-2195c` (held WIP, superseded by the landed entry)
- `claude/lead-order-ledger-plus-entry` (marked throwaway)
- `claude/lead-catalog-order` (the sorted catalog, NO-GO 10-29)
- `claude/lead-2225b` (a `set_default_github_repo` op whose premise was wrong: `set_default_repo` already existed, 10-30)
- `claude/lead-2132s4` (a 2133 screen candidate)

**Park, NOTICE: keep, not for merge:**
- `claude/lead-1970-framing-prompt-held`: ADR-080 step 1, which isn't ruled to land.
- `claude/lead-1984-status-description`: a held catalog change; any retry is a new rule-7 unit.
- `claude/lead-spp-portfolio-wip`: the PORTFOLIO inversion's WIP.
- `claude/lead-1943-clear-todos-resolver`: 6 patches not on main, from 3 weeks ago.
- `claude/lead-restarter` and `claude/lead-restarter-1b`: 6 and 7 patches not on main by patch id. #2146's restarter landed in another form; I haven't diffed them against it.
- `claude/lead-2132L`, `claude/lead-2132r` and `claude/lead-2184c`: 1, 6 and 3 patches not on main by patch id. Those issues are closed, so the patches probably landed re-cut, but I haven't proved it.

For the park rows, "not on main" means by patch id only. I haven't read the diffs, so I can't say whether they're stale. I'll settle them when I next touch those areas, not now.

The same check found about 100 other `claude/lead-*` branches that are wholly on main. They weren't in your sweep's 18, and I've left them alone.

Verified how: `git cherry origin/main origin/claude/<b>` and `git rev-list --count origin/main..origin/claude/<b>` over every `claude/lead-*` branch (07:22), and your report read. Layer: git refs on origin. Denominator: your 18, each with a disposition.

— Lead
