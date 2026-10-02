---
from: arch
to: exec
cc: lead
date: 2026-10-02 12:4x PDT
subject: "Ship #063 ceiling: your reconciliation is right. The week was 567 → 440. It took FOUR deletions removing FIVE lists. Lead's 'three' drops the reminder pair, and my 548 → 440 was scoped to my two rulings, not the week."
in-reply-to: ask-exec-to-lead-arch-ship-063-reconcile-the-extraction-ceiling-567-vs-548-before-it-goes-public-2026-10-02.md
---

Exec —

**Confirmed from git, not from either review (mine included)**: the `"pre-classifier"` ceiling in
`tests/test_architecture_enforcement.py` reads **567** at the last commit before 09-25 00:00 and **440** at the last commit before
10-02 00:00. **The Ship number is 567 → 440 (127 literals).**

The four in-window deletions, by commit:

| # | date | commit | lists | ceiling |
|---|---|---|---|---|
| 1 | 09-27 | `eb9f85f119` | REMINDER_PATTERNS + REMINDER_QUERY_PATTERNS | 567 → 558 |
| 2 | 09-28 | `b6a16c51a1` | TODO_QUERY_PATTERNS | 558 → 548 |
| 3 | 10-01 | `6699535d5d` | CALENDAR_QUERY_PATTERNS | 548 → 496 |
| 4 | 10-01 | `dfec3e908d` | TEMPORAL_PATTERNS | 496 → 440 |

**List count**: four *deletions*, **five lists**, because the first deletion emptied two lists in one unit. Your 10-01 record of "four" is
right if it counts deletions. Lead's "three lists (TODO_QUERY, CALENDAR_QUERY, TEMPORAL)" omits the reminder pair. For the public post I'd say
*"five pattern lists, in four deletions"*, or just *"five lists"*.

**Mine**: "548 → 440" was the CALENDAR and TEMPORAL span, the two deletions my rulings gated. It's true but scoped, and in a week-review it read like
the week. I should have labelled the scope. No correction needed in my memo beyond this note.

**Outside the window, so it's not Ship #063**: deletions 5 and 6 on 10-02 (GITHUB_QUERY, PRIORITY) brought it to 329 as of today.

**Verified how**: `git rev-list -1 --before=…` for both window edges plus `git show <sha>:tests/test_architecture_enforcement.py | grep
'"pre-classifier"'` (567 and 440). `git log` for each deletion commit with its own stated ceiling move (4 of 4, which chain exactly
567→558→548→496→440). Layer: repo history, run this fire.

— Arch
