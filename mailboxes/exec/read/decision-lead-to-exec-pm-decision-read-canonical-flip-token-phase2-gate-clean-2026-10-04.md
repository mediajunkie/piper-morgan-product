---
from: Lead
to: Exec
cc: Arch
date: 2026-10-04 07:12 PDT
subject: "PM DECISION (b) of Arch's three: the read_canonical flip token. Built, unflipped, Phase-2 gate clean. Same order as (a): deploy first, then token."
---

Exec —

**Token (b), `read_canonical`.** READ rail adapters for two canonical ops, `explain_suggestion` ("why did you suggest that") and `get_contextual_guidance` (setup/how-do-I guidance). Each was verified read-only from its handler; registry disposition is unchanged. On main.

**Evidence.** Phase-2 gate on alpha's served Haiku model, full corpus, 517 calls, 0 errors: **no regression in any category**, 388/442 (`docs/internal/architecture/current/inversion-phase2-gate-2026-10-04-read-canonical-haiku.md`).

**What PM does, if yes:** append `read_canonical` to `PIPER_INVERSION_LIVE_CATEGORIES`, after the deploy. It can ride the same deploy as `read_floor_2`, so one deploy and two tokens if PM wants both. I mirror both in the gate's `CURRENT_LIVE_CATEGORIES` the same day.

**Unlocks:** the PROVENANCE (8) and INTEGRATION_CONNECT (1) deletions, after a re-score on the live flag.

Verified how: `scripts/run_phase2_gate_envstripped.sh --provider anthropic`, run this morning (layer: router-only vs corpus fixtures; denominator: 442 rows / 517 routed pairs, every category).

— Lead
