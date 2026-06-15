---
from: Lead Developer
to: PPM (Principal Product Manager)
cc: PM (xian), CXO (Chief Experience Officer)
date: 2026-06-13
subject: #1216 provenance-field — formal handoff (Lead interim guard shipped; the data-model half is your lane)
priority: standard
response-requested: ack + rough M-placement (coordinate with PM)
---

# Handoff: #1216 provenance field

**Context.** #1216 (workstyle confabulation): asked *"what have you learned about my workstyle,"* Piper labeled two observations "real" and the rest "seed placeholders" — but **all** were seeded, and there is **no mechanism** that distinguishes seed from real. `InsightDB` (`services/database/models.py:~410`) has no `is_seed`/`source` flag; the only marker (`context_tags: 'uat-anniversary-…'`) is never surfaced to the model. So the model was *confabulating* a provenance distinction it cannot actually make.

**What Lead shipped (interim, on `main`).** The guard: filter the internal seed tags (`dev_seed` / `seed_demo_object`, plus `uat-*`) out of the floor prompt, so the model can't see — and thus can't confabulate about — them. This kills the **symptom** (the false seed-vs-real claim).

**What's still pending = your lane (per CXO's designation).** The **real** fix is a provenance field: add `source`/`is_seed` to `InsightDB` and populate it (seed scripts mark seed; real extraction marks real), so the distinction the model asserts actually exists and can be surfaced honestly.

**Coordinates with — but is distinct from — Radar.** The Radar *"surface all provenances"* honest-provenance principle (CXO thread, #1090) is the **surfacing** half; #1216 is the **data-model** half (the flag itself). The flag should land first / independently; Radar then consumes it.

**Ask:** ack + a rough M-placement (coordinate with PM — could be an M3 tail or M4). #1216 stays open as the anchor. Happy to pair on the migration/DDL if useful — it's adjacent to the #1180 ConversationDB test-infra work I'm doing tonight.

— Lead Developer, 2026-06-13
