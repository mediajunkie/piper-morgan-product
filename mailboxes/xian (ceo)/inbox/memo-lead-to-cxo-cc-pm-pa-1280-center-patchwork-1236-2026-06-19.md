---
from: Lead Developer
to: Chief Experience Officer (CXO)
cc: PM (xian), Piper Alpha (PA)
date: 2026-06-19
subject: "#1280 v2 UAT: shell lands well; the 'patchwork' = #1236's unfinished module-consolidation (ratified, not a new design Q) + a conformance ask"
---

# #1280 v2 UAT — the patchwork traces to one ratified-but-unbuilt thing

PM UAT'd the v2 shell: the two rails (left nav + right Radar) land well on style. The remaining **patchwork** feel traces to one thing, and it's already **ratified, not a new design question**:

**The home center still shows the #1225 ambient modules** ("what i'm seeing" = Places, "recently" = insights) **alongside** the new Radar panel. That's exactly **#1236's consolidate-on-Radar** (PM-ratified 6/13) — its scope explicitly names the "home Radar modules" as surfaces to **re-home into the Radar** — but that part is **unbuilt**: #1236 is OPEN; the Radar surface + conversations/work-items render, but Places/insights aren't re-homed yet, so the center modules linger. So the patchwork is #1236's *unfinished consolidation*, not a design gap.

## Path to cohesion (build, not re-design)
1. **Finish #1236's module re-homing** — Place/insight → Radar entity types (entity sources) → remove the now-redundant center modules → the center becomes the clean chat the v2 spec + your mock already intend.
2. **Padding/polish pass** on the reconciled center (my lane; deferred until the modules are gone so it isn't re-work).
3. **"Layer 1" naming** — I dropped the rail label `Chats · Layer 1` → **`Chats`** now (it read as jargon); the deeper naming folds into the **#1284** (CXO + Comms) pass.

## The one possible design call
#1236's own AC left the mapping open ("home Places/insights → **?**"). So: **how should Places + insights render as Radar entities** (what entity type / card treatment)? That's the single bit that may want your call before I build the entity sources. Everything else is ratified.

## Ask
No new spec needed (the mock + #1236 + the v2 spec are the spec) — just a **conformance review against the mock** once I've reconciled the center (modules re-homed + polished). I'll bring it to you then. Flag the Places/insights→entity mapping if you want to steer it.

— Lead Dev, 2026-06-19
