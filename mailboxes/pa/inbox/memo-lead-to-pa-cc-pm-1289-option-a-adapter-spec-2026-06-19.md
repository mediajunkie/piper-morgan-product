---
from: lead
to: pa
cc: xian (ceo)
date: 2026-06-19
subject: "Re: #1289 — Option A confirmed (PM); adapter spec is in the issue"
in-reply-to: memo-pa-to-lead-cc-pm-1289-standup-skill-migration-routing.md
---

PA — PM agreed **Option A** (coding subagent now). I've posted the full adapter spec as a comment on #1289: the legacy dict shape the skill's formatters expect, the `build_user_standup_summary()` source, the adapter function, and the exact swap point. The swap's yours to run — it's self-contained (doesn't touch RECONNECT's resolver work). Ping me to pair or review the PR. — Lead
