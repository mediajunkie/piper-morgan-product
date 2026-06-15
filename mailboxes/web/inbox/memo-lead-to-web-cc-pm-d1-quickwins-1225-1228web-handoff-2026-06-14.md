---
from: Lead Developer
to: Web
cc: PM (xian)
date: 2026-06-14
subject: D1 quick-wins handoff — #1225 (home module minimize/dismiss) + #1228 web-chat half (thinking indicator)
priority: standard — PM-blessed quick wins
response-requested: pick up at your cadence; → Review when done
---

# Two D1 quick-win frontend pieces → your lane

PM approved the D1 Track-A quick wins (**"quick wins ok but flywheel for everything else"** — these proceed DIRECTLY: implement + real-render test + → Review, **no** audit-cascade/gameplan ceremony). I shipped the backend/Slack piece; these two are squarely your active lane — you just re-skinned the home modules + wired the "What I'm seeing" panel (#1192d/#1195/#684) and you own the chat frontend — so I deliberately stayed out to avoid collision.

## #1225 — Home "what I'm seeing" modules: minimize/dismiss
The home GitHub/Calendar "place" cards (the ones you wired + re-skinned) have no way to collapse or dismiss — they eat screen real-estate (PM M3 UAT flag). **Ask**: a collapse/minimize + dismiss affordance per module card, **persisted per user** (a dismissed/collapsed card stays that way across reloads). UI polish, not behavior change. Refs #1090 (UI-1.0 plan), PDR-002 Layer 2; coordinates with the History→Radar consolidation you're near.

## #1228 — web-chat half: thinking/typing indicator
A thinking/streaming state (spinner or token streaming) on the **web chat send seam**, so the user can tell normal LLM latency from a frozen connection. I did the **Slack half** (placeholder → `chat.update` in `socket_mode_runner.py`, shipped `d1cd99ca6`; #1228 now In Progress); this web-chat half is the other surface. When it lands, #1228 → Review. Refs #1129.

## Notes
- Both are PM-blessed quick wins → direct (no flywheel). **Real-render test** before declaring done (per the `template.render()` discipline, not curl-200).
- Status: #1225 still Product Backlog — set it In Progress when you pick it up; #1228 is In Progress (Slack half shipped).
- Shout if you'd rather I take either back, or if #1225's home-module work collides with your in-flight design-floor (#1172) changes.

— Lead Dev, 2026-06-14
