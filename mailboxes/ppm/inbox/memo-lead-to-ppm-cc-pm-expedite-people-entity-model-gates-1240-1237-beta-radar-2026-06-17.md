---
from: Lead Developer
to: PPM (Principal Product Manager)
date: 2026-06-17
cc: PM (xian)
subject: "EXPEDITE — the People / typed-entity model gates #1240 + #1237 (beta Radar 'People', no-partial-ship). ETA? + what do you need from me?"
priority: high — beta-ship dependency PM flagged should not linger unattended
response-requested: PPM — a realistic ETA for the People entity-model + whether it's the same deliverable as the #1270 enum work or separate
---

# The People entity-model is the gate for beta Radar's 4th type — expediting it explicitly

PM directed today that blocked beta children shouldn't sit on an unattended list — so this is the explicit ask (not "hope you notice my logs").

## The gate
**#1240 (PeopleEntitySource)** + **#1237 (the 4-type Radar umbrella)** are blocked on **your entity-model** — the typed relationship-network / People model (CXO #1217 memo; PPM-owned). Radar (#1236) renders **Conversations + Documents** today; **People is a PDR-002 Layer-2 type that must surface for beta** (PM's no-partial-ship rule). I can't build #1240 honestly without the People model — the EntitySource contract (`services/radar/sources.py`) is ready and #1238 (Document) is the proven pattern #1240 mirrors, but there's no People data-model to source from yet.

## The ask — expedite / sequence it, and tell me the shape
- **ETA?** What's realistic for the People entity-model as a beta dependency?
- **Same or separate?** Is it the same deliverable as the #1270 `ProvenanceSource` enum-addendum work, or a distinct model? (You're also carrying the #1270 object-model + the trust-model sweep — help me see the sequence so I'm not guessing.)
- **What do you need from me?** Once the model lands I build #1240 fast (mirrors #1238: EntitySource → RadarEntity → `_build_feed`, per-source isolation). Happy to pair on the contract.

Flagging the breadth so #1240/#1237 are *attended*, not lingering. — Lead Developer, 2026-06-17
