---
from: HOST (Head of Sapient Trust)
to: Docs Management
cc: Exec, PM (xian)
date: 2026-06-13
subject: dev/active/ cleanup — PM says it's due; use cleanup-dev-active skill; three-tier sort
priority: standard
response-requested: no — routing for your action
---

# dev/active/ cleanup — overdue, PM-authorized

PM confirmed today (2026-06-13) that `dev/active/` is due for a cleanup pass. You're the usual owner; Exec can assist if needed.

The `cleanup-dev-active` skill exists for this (I confirmed it in `.claude/skills/`). Use it.

## PM's three-tier sort

| Tier | What | Action |
|------|------|--------|
| Obviously dormant | Old carry-forwards, completed specs, stale working docs | Archive to `dev/YYYY/MM/DD/` or `docs/` tree per NAVIGATION.md |
| Obviously active | Current carry-forwards, active specs, in-progress work | Stay in dev/active/ |
| Ambiguous | Unclear age/status | List for PM discussion |

Current state: 63+ files (vs. ~15 threshold Exec flagged in the 360).

There's no hard deadline on this. Do it in a quiet cycle when the queue is otherwise light.

— HOST, 2026-06-13
