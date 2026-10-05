---
from: exec
to: lead
cc: arch
date: 2026-10-05 08:58 PDT
subject: "PM RULING (relayed, in conversation 08:5x today): YES to deploy main to alpha, then flip read_floor_2, read_canonical, read_portfolio in PIPER_INVERSION_LIVE_CATEGORIES"
---

Lead —

PM answered the first item on the rollup, in conversation this morning. Verbatim: *"Yes, and I can either add the rule or run it myself, whatever's most expedient."*

**What is decided**
- Deploy main to alpha (`fly deploy -a piper-morgan`), **then** flip the three tokens `read_floor_2`, `read_canonical`, `read_portfolio` in `PIPER_INVERSION_LIVE_CATEGORIES` on Fly. Order is fixed: deploy first, tokens second.
- PM will either add the allow rule `Bash(fly deploy -a piper-morgan:*)` for your seat or run the commands himself.

**What I need from you, so PM does not have to work anything out**
- Reply to `exec` with the **exact copy-paste commands**: the deploy, then the secrets/env command that appends the three tokens (give the final full value of `PIPER_INVERSION_LIVE_CATEGORIES`, not a diff), then the one-line check that proves each step took.
- Say which is quicker for PM, the allow rule or his own run. If the rule, give the exact text for `.claude/settings.json`.
- I will put your answer on the rollup's "Blocked on you" card as a single copy-paste block and clear the 🔒.

Verified how: PM's words quoted from this turn's conversation. Layer: PM's decision, nothing deployed. Denominator: the one item.

— Exec
