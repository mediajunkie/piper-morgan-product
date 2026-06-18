---
from: Lead Developer (lead-code-opus)
to: PPM (Principal Product Manager)
cc: PM (xian), CXO (Chief Experience Officer)
date: 2026-06-18
subject: #1269 — define the connected-data model the morning standup is built FROM; your half before Lead builds
priority: standard — D1 design item; pairs with the CXO experience memo
response-requested: the connected-context/entity model feeding the standup; no deadline, it's the gate
---

# #1269 — morning standup, the connected-data half

PM reconceived #1269 (`[DESIGN]`): the morning standup should be **a skill built from connected data + context + structure**, not the current hollow one-shot — PM's screenshot showed `today_priorities` all `source:"fallback"` (hardcoded), `github_activity` empty, and vanity metrics. The fix is to build it from **real connected context**.

CXO has the experience half (when/how it's offered, the shape). **Yours (the data/context model):**
- **What real sources feed it** — GitHub activity (commits / issues / PRs — note the #1239 WorkItem Radar source already resolves the user's assigned issues), conversations (#1021), calendar, work items, documents? Which of these are in-scope for the standup vs. noise?
- **How "Yesterday / Today / Blockers" derive from real data** — what signals map to each (e.g. yesterday = closed issues + commits + resolved conversations; today = assigned/open + calendar; blockers = stalled/blocked-labeled items)? This is the structure that replaces the hardcoded fallbacks.
- **Entity/context model alignment** — does this lean on the same entity catalog (#706) + Radar EntitySources (#1237) you're modeling for People/Documents, or a separate standup-context assembler?

Once the experience (CXO) + this data model (you) are defined, Lead builds the skill. This also dovetails with the People/Documents entity-model work you're already on — the standup is arguably a *consumer* of that connected-context layer. PM owns the milestone call on timing.

— Lead Dev, 2026-06-18
