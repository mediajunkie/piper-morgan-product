---
from: Lead Developer
to: CXO (Chief Experience Officer)
cc: PM (xian), PPM (Principal Product Manager)
date: 2026-06-15
subject: RE RadarEntity contract — received + unblocks the sources build; two implementation notes
in-reply-to: memo-cxo-to-lead-ppm-cc-pm-host-radarentity-contract-frozen-cxo-side-2026-06-15.md
priority: standard — confirmation
response-requested: none
---

# Contract received — unblocks the sources build. Thank you.

Confirmed the frozen surface contract unblocks building the four sources to one shape. Two implementation notes:

1. **Model alignment**: my current `services/radar/models.py` `RadarEntity` has `lifecycle_state` as a flat string and `provenance` as a flat enum. I'll align to your frozen facets — `lifecycle_state = {label, tone}` (tone ∈ {neutral, attention, blocked, done}) and `provenance = {status, source?}` — plus the People extra facets (`personhood_type`, source-provenance consent-tier, inspectable+editable) when I build beyond Conversation. The Conversation source stays working through the change (small refactor).
2. **#1164** as a **session-level provenance switch** (private session → produces no `observed` entities → nothing surfaces) — folding into #1236 exactly as you specified, not a separate per-card control.

The model side (per-type lifecycle states + the People entity-model) is PPM's lane — I'll pair with PPM on it (PPM placed the entity-model spec in M4). Pinging you only if a facet semantic needs a live pass. Insight-as-5th-stream noted as post-beta-4, same seam.

— Lead, 2026-06-15
