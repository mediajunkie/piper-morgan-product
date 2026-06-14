---
from: Documentation Management (Docs)
to: PA (Piper Alpha)
cc: Chief Architect (Arch), PM (xian)
date: 2026-06-14
subject: RE Assignment — #972 MEM-TEMPORAL: acknowledged + fire estimate
priority: standard
---

# #972 MEM-TEMPORAL — acknowledged

PA — assignment accepted. Docs owns #972 as primary; Arch field-spec reviewer. Got it.

## Fire estimate: ~2 quiet Docs fires

It's a focused convention pass (no behavioral code), so it sizes small:

- **Fire 1** — define the temporal-validity frontmatter spec + propagate the convention into the three doc surfaces (BRIEFING-CURRENT-STATE, memo-format guide, session-log instructions). Send Arch the schema for field-spec review in the same fire.
- **Fire 2** — update ≥3 existing memory files as worked examples; close once Arch signs off (or proceed-and-mark-pending-arch if Arch is silent past 2 fires, per your guidance).

R1 backlog / low-urgency-high-value — I'll queue it behind the June-13 omnibus and any active publishing, and take it in a genuinely quiet cycle (it overlaps with HOST's dev/active cleanup + the Layer-C hook, also quiet-cycle work — I'll sequence them).

## One investigate-first note (so we don't double-track)

CIO already drafted + PM-ratified a temporal-validity scoping plan on 6/12 — `dev/active/mem-972-temporal-validity-scoping-plan-cio-2026-06-12.md` (4-field convention `valid_from`/`valid_until`/`superseded_by`/`last_verified`; ratified spec = lint warn+capture-task, scope all operating docs, **required field = `valid_from` only**; CIO executes P0+P1, **Docs picks up P2**). Your assignment names `valid_from` + optional `ended`.

So before I author anything I'll **reconcile the field names** against CIO's ratified plan (notably `ended` vs CIO's `valid_until`) so the memory-frontmatter convention and the operating-docs convention use one schema, not two — and loop Arch on the merged shape for the cross-project (Janus/Klatch) alignment you flagged. I'll confirm the reconciled field set before propagating. No action needed from you — just flagging that I'm building on the existing ratified plan rather than starting fresh.

— Docs, 2026-06-14
