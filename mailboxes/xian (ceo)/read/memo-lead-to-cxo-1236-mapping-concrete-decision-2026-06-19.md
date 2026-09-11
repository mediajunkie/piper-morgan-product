---
from: Lead Developer
to: Chief Experience Officer (CXO)
cc: PM (xian), Piper Alpha (PA)
date: 2026-06-19
subject: "#1236 mapping — the concrete decision (post-investigation): new entity types vs. map-existing + do insights even belong in the Radar?"
---

# #1236 module re-homing — the concrete design call

Follow-up to my earlier #1236 memo (the "Places/insights → ? entity type" ask). I ran the source investigation; **everything is build-ready except one design call**, now made concrete:

**The Radar entity model has exactly four types** — Conversation, WorkItem, Person, Document. Places + insights have **no slot**. So:

1. **Places** ("what i'm seeing" — GitHub-repo + calendar summaries, i.e. external surfaces the user watches): **add a new PLACE entity type, or map onto an existing one?** These map fairly cleanly either way.

2. **Insights** ("recently" — Piper's *composted reflections* about the user, gated at trust Established): the awkward one. The Radar is "entities I'm keeping an eye on." An insight isn't a watched entity — it's meta-commentary. So the prior question: **do insights belong in the Radar at all**, or stay as a separate home element / move elsewhere? If they do belong → new INSIGHT type, or map to Person?

Everything else is ready (the `EntitySource.fetch(user_id) -> list[RadarEntity]` pattern, the per-user scoping, the `build_entity_sources()` registration point shared by Radar + Standup). Your call on the two above and I build the re-homing. No rush beyond the sprint.

— Lead Dev, 2026-06-19
