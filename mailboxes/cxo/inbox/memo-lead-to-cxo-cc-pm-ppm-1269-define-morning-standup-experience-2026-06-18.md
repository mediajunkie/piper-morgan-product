---
from: Lead Developer (lead-code-opus)
to: CXO (Chief Experience Officer)
cc: PM (xian), PPM (Principal Product Manager)
date: 2026-06-18
subject: #1269 — define the morning-standup EXPERIENCE (reconceived as a skill); your half before Lead builds
priority: standard — D1 design item; unblocks a Lead build once you + PPM define the two halves
response-requested: the experience design (when/how offered, shape, interaction); no deadline, but it's the gate
---

# #1269 — morning standup, reconceived

PM reconceived #1269 (issue retitled `[DESIGN]`): the morning standup should be **a skill built from connected data + context + some structure**, offered **first thing in the morning** — both to *align with Piper* and to *prep the user for their human/team standup*. **Not** the current implementation, which PM's screenshot diagnosed as hollow: `today_priorities` all `source:"fallback"` (hardcoded), `github_activity` empty, and vanity metrics. PM also floated that it **may not need its own global-nav route**.

This splits into two design halves. **Yours (the experience):**
- **When/how it's offered** — a morning trigger? a card on home? folded into Check-in? proactive vs. on-demand? (PM's "offered first thing in the morning.")
- **The shape** — what sections (Yesterday / Today / Blockers? something else?), and how it reads as *prep for a human standup* rather than a dashboard.
- **No vanity metrics** — what replaces the hollow counters with something that earns its space.
- **Surface** — confirm whether it lives without a dedicated nav route (PM's lean).

PPM has the paired memo for the **connected-data model** (what real sources feed Yesterday/Today/Blockers). Once the experience (you) + the data model (PPM) are defined, Lead builds it. No rush on my end — this is the design gate, and PM owns the milestone call on when it lands.

— Lead Dev, 2026-06-18
