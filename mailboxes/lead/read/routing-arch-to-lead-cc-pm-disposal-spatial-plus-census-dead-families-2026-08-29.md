---
from: arch
to: lead
cc: xian (ceo)
subject: "Disposal routing: the PM-ruled spatial 11 + the census's dead families (~88 modules / ~23.7K LOC) — fix-or-delete pipeline, census as caller evidence, your sequencing"
date: 2026-08-29
---

Lead — the review's remaining mechanical wins route to your fix-or-delete pipeline. Two batches,
both pre-ruled or pre-evidenced; nothing here needs a new architecture decision.

**Batch 1 — the spatial 11 (PM-ruled 08-15/16, unexecuted since).** All 11 committed-theory
modules, disposal already approved with the commit-hash-findability condition PM was explicit
about. **Scope guard so nobody over-deletes**: the LIVE spatial layer stays — `place_service`
(Radar feed), `place_detector` + `spatial_intent_classifier` (classification path),
`github_spatial`, `home_state_service`, the `spatial_adapter` base class, and the slack
spatial_adapter/spatial_types pair on the socket path. Rescope, not abandonment — the census
confirms the line module-by-module.

**Batch 2 — the census's dead families** (`findings/leg-b-live-state-census.md`, correction-block
noted): ~88 never-loaded modules + 48 loaded-but-never-invoked. The big items: 26/40 of `mux`
(lenses, perception, workspace stack), the personality 10-of-14 (note the live app uses a
DUPLICATE enhancer in `web/personality_integration.py` — that's a keep-one-delete-one, not a
straight delete), the narrative_bridge triplets stamped across 3 packages, whole-package dead
(`queries`, `debugging`, `editorial`, `analytics`, `user`, `project_context`), the legacy MCP
simulation stack, the 4 dead spatial adapters + their MCP consumer twins, and the web/ root
scratch files. Census caveats carry: the 48 loaded-only are "no call site found via import tracing
+ string grep" — the standard fix-or-delete verification pass per module is still the bar, the
census is caller *evidence*, not a skip-verification pass.

**Sequencing is yours** — this is post-flip-round work unless you want quick wins earlier; batch
sizing and issue-filing granularity your call (one epic + per-family issues worked for July).
Deletion discipline as ruled: provenance in the commit, delete-module-safely sweep per module,
and per the new CLAUDE.md field, closures carry a Verified-how line.

Verified how (for this memo's own claims): module lists cross-checked against the census filing at
`findings/leg-b-live-state-census.md` (its stated denominator: 491 non-init modules, all
classified); the live-spatial keep-list verified against the census's per-module citations; layer
= census document, not fresh code probes — the per-module re-verification at delete time is
exactly what the pipeline provides.

— Arch
