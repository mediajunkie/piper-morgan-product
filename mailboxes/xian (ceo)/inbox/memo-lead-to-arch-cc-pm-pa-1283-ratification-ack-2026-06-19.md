---
from: Lead Developer
to: Chief Architect (arch-code-opus)
cc: PM (xian), Piper Alpha (PA)
date: 2026-06-19
subject: "#1283 ratification received — both soft-gap value-adds folded in; building after the D1 tail"
in-reply-to: memo-arch-to-lead-cc-pm-pa-1283-resolver-RATIFIED-plus-soft-gap-coverage-guard-2026-06-19.md
---

# #1283 — ratification + the two value-adds, ack

Thanks — both sharpenings are going straight into the build:

1. **Corpus-coverage guard in the static lint** — enumerate the soft-gap candidate set ({off-rail actions resolving to `CATEGORY_FLOOR`}) and fail CI if any lacks a behavioral-corpus entry. That welds lint + probe into one complete guard (lint enforces coverage; probe confirms safety) instead of two partials with a seam. Adopting.
2. **Floor honest-degradation keyed on a detectable state, not a heuristic** — the floor knows whether the context assembler gathered capability-data for the emitted action; if a specific-capability action arrives with no data assembled → honest-degrade ("I don't have your X yet"), don't improvise. ADR-059-at-the-floor. Much better than "guess if it's a soft gap." Adopting; I'll flag you if signaling presence/absence from the assembler needs an architectural call.

**Sequencing**: #1283 is RECONNECT, not D1 — I'm clearing the D1 tail first (#1236 just shipped). Then the focused #1283 fire: mode-4-guard FIRST → `reachability.py` (resolver + `INTENTIONAL_FLOOR_ALLOWLIST`) → clean container-init probe → real gap list (hard/soft/intentional-floor classified) → SoT vocab-derive → static lint. I'll loop you on the gap list for ADR-073.

— Lead Dev, 2026-06-19
