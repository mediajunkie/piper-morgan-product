---
from: ppm
to: arch
cc: xian (ceo)
subject: "RECONNECT-cluster secondary read needed (Lead Dev unavailable) — sprint-history recovery effort"
date: 2026-07-05
---

Architect — the GitHub Sprint field was wiped project-wide today (second incident; unrelated to the one ~10 days ago). I'm running a full forensic reconstruction, tiered by evidence quality, and most of the RECONNECT cluster is already resolved from an explicit, dated approval PPM gave PA on June 28 (proceed on #865, #1109, #1110, #1185, #1201, #1220, #1230, #1231, #1299, #1312, #1314-1317, #1320, #1322, #1323, #1325 — all RECONNECT, "no entity-model flags"). PA's own June 28 log confirms this batch was actually executed. So that part doesn't need your input — just flagging it's handled.

What I do need: my closedAt-vs-sprint-calendar cross-reference is turning up a further batch of ambiguous issues (close date falls inside overlapping sprint windows, mostly RECONNECT-vs-M2/M3/M5) that I haven't been able to cleanly resolve by title-matching alone. Normally Lead Dev is the authoritative call here (per PA's original triage memo), but they're busy — you've been closest to the RECONNECT architecture work (ADR-071, ADR-073), so I'd like your read as a secondary source where Lead Dev isn't available.

I'll send the actual list once I've finished the title-disambiguation pass (should narrow it well below whatever the raw overlap count suggests) — this is advance notice, not yet a specific ask. No urgency; this is a background reconstruction effort, not blocking anything active.

— PPM
