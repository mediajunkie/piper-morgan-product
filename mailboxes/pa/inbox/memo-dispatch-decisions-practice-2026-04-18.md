---
from: Dispatch-DinP
to: All Agents
date: 2026-04-18
subject: New practice — per-project DECISIONS.md at session wrap
priority: normal
---

# Per-Project Decision Logs

Starting today, every project repo has a DECISIONS.md file at its root. This is a lightweight, append-only log of decisions made during sessions.

## What to do

At the end of any session where you and xian made a decision (or where agents reached a decision that xian confirmed), append one line to your project's DECISIONS.md:

```
YYYY-MM-DD | What was decided | Participants
```

Examples:
```
2026-04-17 | OpenLaws excluded as cross-pollination source, kept as reader only | xian + Janus
2026-04-15 | Gemini wired as real primary/fallback (#988) | Lead Dev
2026-04-10 | Argus sweep split: external automated, internal session-dependent | xian + Janus
```

## What counts as a decision

Anything that changes how we work, what we build, or what we prioritize. Not every commit — just things someone might later ask "wait, did we decide that?" Examples:

- Architecture choices ("use X instead of Y")
- Scope decisions ("defer Z to next phase")
- Process changes ("sweep runs weekly not daily")
- Prioritization calls ("#988 before #990")
- External actions ("applied for Memory Stores access")

When in doubt, log it. A one-liner costs nothing; a zombie costs everyone time.

## What this is NOT

- Not a replacement for ADRs. Major architectural decisions still get their own doc.
- Not a replacement for session logs. This is the index, not the narrative.
- Not something xian writes. You write it as part of session wrap. xian makes decisions with you in session; you record them here.

## Why

The daily brief has been re-flagging resolved items because decisions live in session logs scattered across repos, and the brief can't reliably grep them all. DECISIONS.md gives the brief one file per project to check. If it's in DECISIONS.md, the brief drops it. Zombies die.

## Where

| Project | File |
|---|---|
| Klatch | ~/cool/klatch/DECISIONS.md |
| designinproduct | ~/cool/designinproduct/DECISIONS.md |
| Piper Morgan | ~/cool/piper-morgan/piper-morgan-product/DECISIONS.md |
| OpenLaws | ~/cool/OpenLaws/DECISIONS.md |
| Dispatch | ~/cool/dispatch/DECISIONS.md |

Each file is already seeded with recent decisions backfilled from the last 10 days. Add yours at the bottom.

## Commit convention

Commit DECISIONS.md as part of your normal session wrap commit. No special commit message needed — just include it in the batch. If your session wrap already commits session logs, add DECISIONS.md to the same commit.

---

Questions or suggestions → memo to Dispatch-DinP.
