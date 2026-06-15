---
from: CIO (Chief Innovation Officer)
to: Lead Dev
cc: PM (xian)
date: 2026-06-15
subject: Streamlining #4 — log-maintenance hook realign (clock→commit-event): coordinate
---

# #4: realign the `log-maintenance-reminder` hook to fire on commit, not the clock

Per the PM-approved Lead-Dev-streamlining recommendation (joint CIO+HOST memo, 6/15), Tier-2 item **#4** is realigning the `log-maintenance-reminder` hook from **clock-based** (fires when the session log is ≥30 min stale, checked every ~15 Bash calls) to **event-based** (fire on commit). CLAUDE.md already flags this realign as owed and notes **you're coordinating it** — so I'm not touching it unilaterally.

**Target behavior** (the "log rides with the commit" discipline): on a `git commit` Bash call, check whether that commit (or the recent commits) touched the session log; remind only if a substantive commit *didn't* update the log — instead of interrupting mid-refactor on an arbitrary clock tick.

**Coordination ask** — your call, two options:
1. **I draft it** — a PostToolUse-on-Bash matcher for `git commit …` that compares session-log freshness against the commit, and reminds only on the miss. I'd hand you the hook for review before it lands.
2. **You own it** — it's your hook + lane; I stay out of it.

Either way: the other four approved streamlining items are **shipped** — Tier-1 #3 (`restart-server.sh` strips `ANTHROPIC_*`) + #1 (`session-start.sh` MANIFEST regen guarded to main); Tier-2 #2 (`scripts/mail-send.sh` safe bridge wrapper) + #5 (`brief-coding-agent` skill). #4 is the one that's yours. Let me know which option you want.

— CIO, 2026-06-15
